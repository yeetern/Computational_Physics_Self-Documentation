import numpy as np
from stable_baselines3 import PPO
from eco_env import PredatorHuntEnv

def run(policy, episodes=20):
    env = PredatorHuntEnv(seed=0, max_steps=300)
    scores, eats = [], []
    for _ in range(episodes):
        obs, _ = env.reset()
        total_r = 0.0
        total_eat = 0
        while True:
            if policy is None:
                action = env.action_space.sample()
            else:
                action, _ = policy.predict(obs, deterministic=True)
            obs, r, term, trunc, info = env.step(action)
            total_r += float(r)
            total_eat += int(info["prey_eaten"])
            if term or trunc:
                break
        scores.append(total_r)
        eats.append(total_eat)
    return np.mean(scores), np.mean(eats)

if __name__ == "__main__":
    r0, e0 = run(None, episodes=30)
    print(f"Random: mean_reward={r0:.2f}, mean_eats={e0:.2f}")

    model = PPO.load("ppo_predator")
    r1, e1 = run(model, episodes=30)
    print(f"Trained: mean_reward={r1:.2f}, mean_eats={e1:.2f}")
