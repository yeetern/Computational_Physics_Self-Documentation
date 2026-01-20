import mesa
import numpy as np
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider

# -----------------------------
# 1. Advanced Parameters & Constants
# -----------------------------
GRID_WIDTH = 20
GRID_HEIGHT = 20

# -----------------------------
# 2. Intelligent Agents
# -----------------------------

class Grass(Agent):
    def __init__(self, unique_id, model, grown=True):
        super().__init__(unique_id, model)
        self.grown = grown

class Animal(Agent):
    """
    Base class for intelligent animals with vision and metabolism.
    """
    def __init__(self, unique_id, model, energy, vision, speed):
        # We initialize the parent (Mesa Agent) first
        super().__init__(unique_id, model)
        self.energy = energy
        self.vision = vision  # Radius of sight
        self.speed = speed    # Cells per step

    def get_local_entities(self, entity_type):
        """Returns list of specific agents within vision radius."""
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, radius=self.vision, include_center=False
        )
        return [obj for obj in neighbors if isinstance(obj, entity_type)]

    def move_towards(self, target_pos):
        """Smart movement: step towards a specific target cell."""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        # Pick the step that minimizes distance to target
        best_step = min(possible_steps, key=lambda p: self.get_distance(p, target_pos))
        self.model.grid.move_agent(self, best_step)

    def move_away_from(self, target_pos):
        """Smart evasion: step away from a specific target cell."""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        # Pick the step that maximizes distance from target
        best_step = max(possible_steps, key=lambda p: self.get_distance(p, target_pos))
        self.model.grid.move_agent(self, best_step)

    def get_distance(self, pos1, pos2):
        # Calculate Euclidean distance
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        return np.sqrt(dx*dx + dy*dy)

    def random_move(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_pos = self.random.choice(neighbors)
        self.model.grid.move_agent(self, new_pos)


class Prey(Animal):
    """
    Smart Prey: 
    - Flee Predators
    - Eat Grass
    - Betray friends if 'selfish'
    """
    def __init__(self, unique_id, model, energy=10, altruism=0.5):
        # --- FIX: Use 'model' directly, not 'self.model' ---
        super().__init__(unique_id, model, energy, vision=model.prey_vision, speed=1)
        self.altruism = altruism  # 0.0 = Selfish (Betrayer), 1.0 = Altruistic

    def step(self):
        if not self.pos: return
        
        self.energy -= self.model.prey_metabolism
        
        # 1. Detect Threats
        predators = self.get_local_entities(Predator)
        
        if predators:
            nearest_pred = predators[0] # Simply take the first seen for speed
            
            # --- BETRAYAL MECHANIC ---
            # If selfish and cornered, swap spots with a neighbor prey (push them into danger)
            neighbors = self.model.grid.get_cell_list_contents(
                self.model.grid.get_neighborhood(self.pos, True, False)
            )
            neighbor_prey = [obj for obj in neighbors if isinstance(obj, Prey)]
            
            if self.altruism < 0.3 and neighbor_prey:
                # "Betrayal": Swap positions with a friend to confuse predator
                victim = self.random.choice(neighbor_prey)
                my_pos = self.pos
                victim_pos = victim.pos
                # Simple swap
                self.model.grid.move_agent(self, victim_pos)
                self.model.grid.move_agent(victim, my_pos)
            else:
                # Run normally
                self.move_away_from(nearest_pred.pos)
        else:
            # 2. Look for Food if safe
            grass_patches = self.get_local_entities(Grass)
            edible_grass = [g for g in grass_patches if g.grown]
            
            if edible_grass:
                target = min(edible_grass, key=lambda g: self.get_distance(self.pos, g.pos))
                if self.pos == target.pos:
                    self.eat()
                else:
                    self.move_towards(target.pos)
                    # Try to eat after moving
                    self.eat()
            else:
                self.random_move()

        # 3. Reproduce or Die
        if self.energy >= self.model.prey_reproduce_energy:
            self.reproduce()
        if self.energy <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cellmates:
            if isinstance(obj, Grass) and obj.grown:
                obj.grown = False
                self.energy += self.model.grass_gain
                break

    def reproduce(self):
        self.energy /= 2
        baby = Prey(self.model.next_id(), self.model, energy=self.energy, altruism=self.random.random())
        self.model.grid.place_agent(baby, self.pos)
        self.model.schedule.add(baby)


class Predator(Animal):
    """
    Smart Predator:
    - Hunt Prey
    - Pack Tactics (Gain efficiency near friends)
    """
    def __init__(self, unique_id, model, energy=20):
        # --- FIX: Use 'model' directly, not 'self.model' ---
        super().__init__(unique_id, model, energy, vision=model.pred_vision, speed=1)

    def step(self):
        if not self.pos: return
        
        self.energy -= self.model.pred_metabolism
        
        # 1. Hunt
        prey_nearby = self.get_local_entities(Prey)
        if prey_nearby:
            target = min(prey_nearby, key=lambda p: self.get_distance(self.pos, p.pos))
            if self.pos == target.pos:
                self.eat_prey(target)
            else:
                self.move_towards(target.pos)
                # Check if we landed on any prey
                cell_prey = [obj for obj in self.model.grid.get_cell_list_contents([self.pos]) if isinstance(obj, Prey)]
                if cell_prey:
                    self.eat_prey(cell_prey[0])
        else:
            self.random_move()

        # 2. Reproduce or Die
        if self.energy >= self.model.pred_reproduce_energy:
            self.reproduce()
        if self.energy <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    def eat_prey(self, prey):
        # --- COLLABORATION MECHANIC ---
        # Check for other predators nearby ("The Pack")
        pack_mates = self.get_local_entities(Predator)
        efficiency_boost = len(pack_mates) * 2  # More energy gained if eating with friends
        
        self.energy += self.model.pred_gain + efficiency_boost
        
        self.model.grid.remove_agent(prey)
        self.model.schedule.remove(prey)

    def reproduce(self):
        self.energy /= 2
        baby = Predator(self.model.next_id(), self.model, energy=self.energy)
        self.model.grid.place_agent(baby, self.pos)
        self.model.schedule.add(baby)


# -----------------------------
# 3. The Model
# -----------------------------

class AdvancedEcoModel(Model):
    def __init__(self, 
                 width=GRID_WIDTH, height=GRID_HEIGHT,
                 init_prey=50, init_pred=10,
                 prey_vision=3, pred_vision=5,
                 grass_regrowth_rate=0.1):
        
        super().__init__() 
        
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.running = True
        
        # Config params
        self.prey_vision = prey_vision
        self.pred_vision = pred_vision
        self.prey_metabolism = 1
        self.pred_metabolism = 1
        self.grass_gain = 5
        self.pred_gain = 15
        self.prey_reproduce_energy = 20
        self.pred_reproduce_energy = 30
        self.grass_regrowth_rate = grass_regrowth_rate

        # Initialize Grass
        for x in range(width):
            for y in range(height):
                grown = self.random.random() < 0.5
                g = Grass(self.next_id(), self, grown)
                self.grid.place_agent(g, (x, y))

        # Initialize Prey
        for _ in range(init_prey):
            p = Prey(self.next_id(), self)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(p, (x, y))
            self.schedule.add(p)

        # Initialize Predators
        for _ in range(init_pred):
            p = Predator(self.next_id(), self)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(p, (x, y))
            self.schedule.add(p)

        self.datacollector = DataCollector(
            model_reporters={
                "Prey": lambda m: sum(1 for a in m.schedule.agents if isinstance(a, Prey)),
                "Predators": lambda m: sum(1 for a in m.schedule.agents if isinstance(a, Predator)),
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        
        # Grass Regrowth
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell_contents = self.grid.get_cell_list_contents((x,y))
                grass = next((obj for obj in cell_contents if isinstance(obj, Grass)), None)
                if grass and not grass.grown:
                    if self.random.random() < self.grass_regrowth_rate:
                        grass.grown = True


# -----------------------------
# 4. Visualization
# -----------------------------

def portrayal(agent):
    if agent is None: return
    
    # 🌿 GRASS
    if isinstance(agent, Grass):
        if agent.grown:
            return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "#4caf50", "Layer": 0}
        else:
            return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "#e8f5e9", "Layer": 0}
    
    # 🐑 PREY
    if isinstance(agent, Prey):
        # Darker green for altruistic, purple for selfish/betrayers
        color = "blue" if agent.altruism > 0.3 else "purple"
        return {
            "Shape": "circle", "r": 0.6, "Filled": "true", "Color": color, "Layer": 1,
            "text": "🐑", "text_color": "white"
        }
    
    # 🐺 PREDATOR
    if isinstance(agent, Predator):
        return {
            "Shape": "circle", "r": 0.8, "Filled": "true", "Color": "red", "Layer": 2,
            "text": "🐺", "text_color": "white"
        }

# Chart
chart_element = ChartModule([
    {"Label": "Prey", "Color": "blue"},
    {"Label": "Predators", "Color": "red"}
])

# Sliders
model_params = {
    "init_prey": Slider("Initial Prey", 50, 10, 200, 10),
    "init_pred": Slider("Initial Predators", 10, 1, 50, 1),
    "prey_vision": Slider("Prey Vision Radius", 3, 1, 10, 1),
    "pred_vision": Slider("Predator Vision Radius", 5, 1, 10, 1),
    "grass_regrowth_rate": Slider("Grass Regrowth Rate", 0.1, 0.01, 1.0, 0.05),
}

# Launch
if __name__ == "__main__":
    grid = CanvasGrid(portrayal, GRID_WIDTH, GRID_HEIGHT, 600, 600)
    server = ModularServer(
        AdvancedEcoModel, 
        [grid, chart_element], 
        "Advanced Eco Sim: Betrayal & Vision", 
        model_params
    )
    server.port = 8521
    server.launch()