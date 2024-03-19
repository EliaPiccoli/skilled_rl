# import numpy as np
# SEED = 0
# np.random.seed(SEED)

# import os
# from PIL import Image
# from baselines.common.atari_wrappers import make_atari, WarpFrame

# envs = [
#     #train
#     'BreakoutNoFrameskip-v4',
#     'FishingDerbyNoFrameskip-v4',
#     'FreewayNoFrameskip-v4',
#     'GravitarNoFrameskip-v4',
#     'KangarooNoFrameskip-v4',
#     'MontezumaRevengeNoFrameskip-v4',
#     'MsPacmanNoFrameskip-v4',
#     'RobotankNoFrameskip-v4',
#     'SpaceInvadersNoFrameskip-v4',
#     'VideoPinballNoFrameskip-v4',
#     #eval
#     'PongNoFrameskip-v4'
# ]
# NUM_EPS = 100
# IMG_SZ = 84

# for i, e in enumerate(envs):
#     env = WarpFrame(make_atari(e, max_episode_steps=100), width=IMG_SZ, height=IMG_SZ, grayscale=True)
#     obs = env.reset()
#     datadir = f"data/{i}"

#     print("Collecting data for env:", e)
#     for ep in range(NUM_EPS):
#         os.makedirs(f"{datadir}/{ep}", exist_ok=True)
#         obs = env.reset()
#         timestep = 0
#         img = Image.fromarray(np.squeeze(obs))
#         img.save(f"{datadir}/{ep}/{timestep}.png")
        
#         while True:
#             obs, r, done, _ = env.step(env.action_space.sample())
#             timestep += 1
#             img = Image.fromarray(np.squeeze(obs))
#             img.save(f"{datadir}/{ep}/{timestep}.png")
#             if done:
#                 break
# print("GenerateData complete - saved in:", datadir)

import numpy as np
SEED = 0
np.random.seed(SEED)

import os
from PIL import Image
import gymnasium as gym
from gymnasium.wrappers import AtariPreprocessing

ENV = "BeamRiderNoFrameskip-v4"
NUM_EPS = 1
IMG_SZ = 84

# wrappers = [
#     AtariPreprocessing,
#     FireResetWrapper,
#     ClipRewardWrapper
# ]

# Create and set-up the environment.
env = gym.make(ENV)
env = AtariPreprocessing(env)
obs = env.reset()
datadir = f"data/{ENV}_{IMG_SZ}"

for ep in range(NUM_EPS):
    os.makedirs(f"{datadir}/{ep}", exist_ok=True)
    obs, info = env.reset()
    timestep = 0
    img = Image.fromarray(obs)
    img.save(f"{datadir}/{ep}/{timestep}.png")
    
    while True:
        obs, r, done, trunc, info = env.step(env.action_space.sample())
        timestep += 1
        img = Image.fromarray(obs)
        img.save(f"{datadir}/{ep}/{timestep}.png")
        if done or trunc:
            break
print("GenerateData complete - saved in:", datadir)