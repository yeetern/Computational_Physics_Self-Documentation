from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Type

from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


# -----------------------------
# Parameters
# -----------------------------
@dataclass
class Params:
    width: int = 50
    height: int = 50

    init_prey: int = 120
    init_pred: int = 40

    # Energy & metabolism
    prey_init_energy: int = 10
    pred_init_energy: int = 20
    prey_metabolism: int = 1
    pred_metabolism: int = 2

    # Feeding gains
    prey_gain_from_grass: int = 4
    pred_gain_from_prey: int = 12

    # Reproduction thresholds & costs
    prey_reproduce_energy: int = 18
    pred_reproduce_energy: int = 30
    reproduce_cost: int = 8  # energy cost paid by parent

    # Grass dynamics
    grass_regrow_prob: float = 0.05  # per cell per step if empty
    grass_init_cover: float = 0.50   # initial fraction of cells with grown grass


# -----------------------------
# Agents
# -----------------------------
class Grass(Agent):
    """
    One Grass patch per cell. 'grown=True' means edible this step.
    We do NOT schedule Grass to avoid activation-order pitfalls.
    """
    def __init__(self, unique_id, model: Model, grown: bool = True):
        super().__init__(unique_id, model)
        self.grown = grown


class Prey(Agent):
    """Prey: wander, eat grass, reproduce, die."""
    def __init__(self, unique_id, model: Model, energy: int):
        super().__init__(unique_id, model)
        self.energy = energy

    def move(self):
        if self.pos is None:
            return  # already removed in this tick
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_pos = self.random.choice(neighbors)
        self.model.grid.move_agent(self, new_pos)

    def eat(self):
        if self.pos is None:
            return
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cellmates:
            if isinstance(obj, Grass) and obj.grown:
                obj.grown = False
                self.energy += self.model.p.prey_gain_from_grass
                break

    def reproduce(self):
        if self.pos is None:
            return
        if self.energy >= self.model.p.prey_reproduce_energy:
            self.energy -= self.model.p.reproduce_cost
            baby = Prey(self.model.next_id(), self.model, energy=self.model.p.prey_init_energy)
            self.model.schedule.add(baby)
            self.model.grid.place_agent(baby, self.pos)

    def die_if_needed(self):
        if self.pos is None:
            return
        if self.energy <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    def step(self):
        if self.pos is None:
            return
        self.energy -= self.model.p.prey_metabolism
        self.move()
        self.eat()
        self.reproduce()
        self.die_if_needed()


class Predator(Agent):
    """Predator: wander, hunt one prey in cell, reproduce, die."""
    def __init__(self, unique_id, model: Model, energy: int):
        super().__init__(unique_id, model)
        self.energy = energy

    def move(self):
        if self.pos is None:
            return
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_pos = self.random.choice(neighbors)
        self.model.grid.move_agent(self, new_pos)

    def hunt(self):
        if self.pos is None:
            return
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        prey_list = [a for a in cellmates if isinstance(a, Prey)]
        if prey_list:
            victim = self.random.choice(prey_list)
            # Remove victim safely
            if victim.pos is not None:
                self.model.grid.remove_agent(victim)
            # schedule.remove is safe even if already removed elsewhere in this tick
            try:
                self.model.schedule.remove(victim)
            except Exception:
                pass
            self.energy += self.model.p.pred_gain_from_prey

    def reproduce(self):
        if self.pos is None:
            return
        if self.energy >= self.model.p.pred_reproduce_energy:
            self.energy -= self.model.p.reproduce_cost
            baby = Predator(self.model.next_id(), self.model, energy=self.model.p.pred_init_energy)
            self.model.schedule.add(baby)
            self.model.grid.place_agent(baby, self.pos)

    def die_if_needed(self):
        if self.pos is None:
            return
        if self.energy <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    def step(self):
        if self.pos is None:
            return
        self.energy -= self.model.p.pred_metabolism
        self.move()
        self.hunt()
        self.reproduce()
        self.die_if_needed()


# -----------------------------
# Helpers for DataCollector
# -----------------------------
def count_agents(model: Model, cls: Type[Agent]) -> int:
    return sum(1 for a in model.schedule.agents if isinstance(a, cls))


def grass_cover(model: Model) -> float:
    """Fraction of cells whose Grass is grown. Robust across Mesa versions."""
    grown = 0
    total = model.grid.width * model.grid.height

    for x in range(model.grid.width):
        for y in range(model.grid.height):
            cell = model.grid.get_cell_list_contents((x, y))
            for obj in cell:
                if isinstance(obj, Grass):
                    grown += 1 if obj.grown else 0
                    break

    return grown / total if total > 0 else 0.0


# -----------------------------
# Model
# -----------------------------
class EcoModel(Model):
    def __init__(self, p: Optional[Params] = None, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self.p = p or Params()

        self.grid = MultiGrid(self.p.width, self.p.height, torus=True)
        # Schedule only animals (no grass)
        self.schedule = RandomActivation(self)

        # Place one Grass per cell (not scheduled)
        for x in range(self.p.width):
            for y in range(self.p.height):
                grown = (self.random.random() < self.p.grass_init_cover)
                g = Grass(self.next_id(), self, grown=grown)
                self.grid.place_agent(g, (x, y))

        # Place prey
        for _ in range(self.p.init_prey):
            a = Prey(self.next_id(), self, energy=self.p.prey_init_energy)
            self.schedule.add(a)
            x = self.random.randrange(self.p.width)
            y = self.random.randrange(self.p.height)
            self.grid.place_agent(a, (x, y))

        # Place predators
        for _ in range(self.p.init_pred):
            a = Predator(self.next_id(), self, energy=self.p.pred_init_energy)
            self.schedule.add(a)
            x = self.random.randrange(self.p.width)
            y = self.random.randrange(self.p.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters={
                "Prey": lambda m: count_agents(m, Prey),
                "Predator": lambda m: count_agents(m, Predator),
                "GrassCover": grass_cover,
            }
        )

        self.running = True

    def regrow_grass(self):
        # Model-level grass regrowth
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell = self.grid.get_cell_list_contents((x, y))
                for obj in cell:
                    if isinstance(obj, Grass) and (not obj.grown):
                        if self.random.random() < self.p.grass_regrow_prob:
                            obj.grown = True
                        break

    def step(self):
        self.datacollector.collect(self)

        # Animals act
        self.schedule.step()

        # Grass regrows
        self.regrow_grass()

        # Stop condition (optional)
        if count_agents(self, Prey) == 0 and count_agents(self, Predator) == 0:
            self.running = False
