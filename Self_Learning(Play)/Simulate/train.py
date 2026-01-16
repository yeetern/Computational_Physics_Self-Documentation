from stable_baselines3 import PPO
from eco_env import PredatorHuntEnv

if __name__ == "__main__":
    env = PredatorHuntEnv(seed=0, max_steps=300)

    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        n_steps=2048,
        batch_size=256,
        learning_rate=3e-4,
        gamma=0.99,
    )
    model.learn(total_timesteps=200_000)
    model.save("ppo_predator")
    print("Saved: ppo_predator.zip")
