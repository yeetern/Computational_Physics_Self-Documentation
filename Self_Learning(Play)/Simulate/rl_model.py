from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation


@dataclass
class Params:
    width: int = 20
    height: int = 20
    init_prey: int = 60

    prey_init_energy: int = 10
    predator_init_energy: int = 25

    prey_metabolism: int = 1
    predator_metabolism: int = 1

    prey_gain_from_grass: int = 4
    predator_gain_from_prey: int = 12

    prey_reproduce_energy: int = 18
    predator_die_energy: int = 0

    grass_regrow_prob: float = 0.08
    grass_init_cover: float = 0.50

    prey_vision: int = 2  # prey avoids predator if within this radius


class Grass(Agent):
    def __init__(self, unique_id, model: Model, grown: bool = True):
        super().__init__(unique_id, model)
        self.grown = grown


class Prey(Agent):
    def __init__(self, unique_id, model: Model, energy: int):
        super().__init__(unique_id, model)
        self.energy = energy

    def _neighbors(self):
        return self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)

    def _move_random(self):
        new_pos = self.random.choice(self._neighbors())
        self.model.grid.move_agent(self, new_pos)

    def _move_away_from(self, predator_pos):
        neigh = self._neighbors()
        # maximize distance
        best = max(neigh, key=lambda p: (p[0]-predator_pos[0])**2 + (p[1]-predator_pos[1])**2)
        self.model.grid.move_agent(self, best)

    def _move_toward_grass(self):
        # look in Moore radius 1 for grown grass; else random
        neigh = self._neighbors()
        best = None
        for p in neigh:
            cell = self.model.grid.get_cell_list_contents([p])
            if any(isinstance(o, Grass) and o.grown for o in cell):
                best = p
                break
        if best is None:
            self._move_random()
        else:
            self.model.grid.move_agent(self, best)

    def _eat(self):
        cell = self.model.grid.get_cell_list_contents([self.pos])
        for o in cell:
            if isinstance(o, Grass) and o.grown:
                o.grown = False
                self.energy += self.model.p.prey_gain_from_grass
                break

    def _reproduce(self):
        if self.energy >= self.model.p.prey_reproduce_energy:
            self.energy //= 2
            baby = Prey(self.model.next_id(), self.model, energy=self.model.p.prey_init_energy)
            self.model.grid.place_agent(baby, self.pos)
            self.model.schedule.add(baby)

    def step(self):
        if self.pos is None:
            return
        self.energy -= self.model.p.prey_metabolism

        # avoid learning predator if close
        pred_pos = self.model.predator_pos
        if pred_pos is not None:
            dx = abs(self.pos[0] - pred_pos[0])
            dy = abs(self.pos[1] - pred_pos[1])
            if dx*dx + dy*dy <= self.model.p.prey_vision**2:
                self._move_away_from(pred_pos)
            else:
                self._move_toward_grass()
        else:
            self._move_toward_grass()

        self._eat()
        self._reproduce()

        if self.energy <= 0 and self.pos is not None:
            self.model.grid.remove_agent(self)
            try:
                self.model.schedule.remove(self)
            except Exception:
                pass


class RLEcoModel(Model):
    """
    Learning predator is NOT a Mesa agent in schedule.
    We treat predator as controlled state: position + energy.
    """
    def __init__(self, p: Params, seed: int = 0):
        super().__init__(seed=seed)
        self.p = p
        self.grid = MultiGrid(p.width, p.height, torus=True)
        self.schedule = RandomActivation(self)

        # Place grass (not scheduled)
        for x in range(p.width):
            for y in range(p.height):
                grown = (self.random.random() < p.grass_init_cover)
                g = Grass(self.next_id(), self, grown=grown)
                self.grid.place_agent(g, (x, y))

        # Place prey
        for _ in range(p.init_prey):
            a = Prey(self.next_id(), self, energy=p.prey_init_energy)
            self.schedule.add(a)
            self.grid.place_agent(a, (self.random.randrange(p.width), self.random.randrange(p.height)))

        # Predator state
        self.predator_energy = p.predator_init_energy
        self.predator_pos = (self.random.randrange(p.width), self.random.randrange(p.height))

        self.steps = 0

    def _wrap(self, x, y):
        return (x % self.grid.width, y % self.grid.height)

    def predator_move(self, action: int):
        # 8 directions
        dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        dx, dy = dirs[action]
        x, y = self.predator_pos
        self.predator_pos = self._wrap(x + dx, y + dy)

    def predator_hunt(self) -> int:
        """Eat ONE prey in predator cell if any. Return number eaten (0/1)."""
        cell = self.grid.get_cell_list_contents([self.predator_pos])
        prey_list = [o for o in cell if isinstance(o, Prey)]
        if not prey_list:
            return 0
        victim = self.random.choice(prey_list)
        if victim.pos is not None:
            self.grid.remove_agent(victim)
        try:
            self.schedule.remove(victim)
        except Exception:
            pass
        self.predator_energy += self.p.predator_gain_from_prey
        return 1

    def regrow_grass(self):
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell = self.grid.get_cell_list_contents((x, y))
                for o in cell:
                    if isinstance(o, Grass) and (not o.grown):
                        if self.random.random() < self.p.grass_regrow_prob:
                            o.grown = True
                        break

    def step(self, predator_action: int) -> int:
        """Advance one tick. Returns prey_eaten (0/1)."""
        self.steps += 1

        # predator consumes energy each step (metabolism)
        self.predator_energy -= self.p.predator_metabolism

        # predator acts (move then hunt)
        self.predator_move(predator_action)
        prey_eaten = self.predator_hunt()

        # environment acts (prey)
        self.schedule.step()

        # grass regrowth
        self.regrow_grass()

        return prey_eaten

    def is_done(self) -> bool:
        prey_left = sum(1 for a in self.schedule.agents if isinstance(a, Prey))
        if prey_left == 0:
            return True
        if self.predator_energy <= self.p.predator_die_energy:
            return True
        return False

    def prey_count(self) -> int:
        return sum(1 for a in self.schedule.agents if isinstance(a, Prey))
