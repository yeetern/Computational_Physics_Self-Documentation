import numpy as np
import gymnasium as gym
from gymnasium import spaces
from rl_model import RLEcoModel, Params


class PredatorHuntEnv(gym.Env):
    """
    Single-agent RL: control predator; prey+grass are environment dynamics.
    Observation (discrete):
      - 8 neighbor prey bits (0/1)
      - 8 neighbor grass-grown bits (0/1)
      - direction-to-nearest-prey (0..8) where 0..7 are 8 dirs, 8 = none
      - predator energy bin (0..2)
    Action:
      - 8 directions
    """
    metadata = {"render_modes": []}

    def __init__(self, seed=0, max_steps=300):
        super().__init__()
        self.seed_val = seed
        self.max_steps = max_steps

        self.action_space = spaces.Discrete(8)
        self.observation_space = spaces.MultiDiscrete([2]*8 + [2]*8 + [9] + [3])

        self.model = None

        self.dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        p = Params(width=20, height=20, init_prey=60)
        self.model = RLEcoModel(p=p, seed=self.seed_val)
        self.t = 0
        return self._obs(), {}

    def _energy_bin(self, e):
        if e < 10: return 0
        if e < 25: return 1
        return 2

    def _wrap(self, x, y):
        return (x % self.model.grid.width, y % self.model.grid.height)

    def _nearest_prey_dir(self):
        # find nearest prey by squared distance on torus (approx: wrap distance)
        px, py = self.model.predator_pos
        best = None
        best_d2 = 10**9

        for a in self.model.schedule.agents:
            if a.pos is None:
                continue
            x, y = a.pos
            dx = min(abs(x - px), self.model.grid.width - abs(x - px))
            dy = min(abs(y - py), self.model.grid.height - abs(y - py))
            d2 = dx*dx + dy*dy
            if d2 < best_d2:
                best_d2 = d2
                best = (x, y)

        if best is None:
            return 8  # none

        # map vector to one of 8 dirs (coarse)
        vx = best[0] - px
        vy = best[1] - py
        sx = 0 if vx == 0 else (1 if vx > 0 else -1)
        sy = 0 if vy == 0 else (1 if vy > 0 else -1)

        # find matching direction index
        for i, (dx, dy) in enumerate(self.dirs):
            if (dx, dy) == (sx, sy):
                return i
        # if purely horizontal/vertical not in dirs? (it is included)
        return 8

    def _obs(self):
        px, py = self.model.predator_pos

        prey_bits = []
        grass_bits = []
        for dx, dy in self.dirs:
            nx, ny = self._wrap(px + dx, py + dy)
            cell = self.model.grid.get_cell_list_contents((nx, ny))
            prey_bits.append(1 if any(o.__class__.__name__ == "Prey" for o in cell) else 0)
            grass_bits.append(1 if any(o.__class__.__name__ == "Grass" and o.grown for o in cell) else 0)

        n_dir = self._nearest_prey_dir()
        ebin = self._energy_bin(self.model.predator_energy)
        return np.array(prey_bits + grass_bits + [n_dir] + [ebin], dtype=np.int64)

    def step(self, action):
        self.t += 1
        prey_eaten = self.model.step(int(action))

        # reward: eat prey big positive, small step cost, death penalty
        reward = 10.0 * prey_eaten - 0.02

        terminated = self.model.is_done()
        truncated = self.t >= self.max_steps

        if terminated and self.model.predator_energy <= 0:
            reward -= 10.0  # died

        return self._obs(), reward, terminated, truncated, {
            "prey_left": self.model.prey_count(),
            "pred_energy": self.model.predator_energy,
            "prey_eaten": prey_eaten
        }
