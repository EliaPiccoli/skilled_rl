# import utils file and load the method custom_atari_wrapper
# import sys
# sys.path.append("./utils")
import numpy as np
import os
from stable_baselines3.common.env_util import make_atari_env, make_vec_env
from stable_baselines3.common.vec_env import VecFrameStack, VecTransposeImage
import matplotlib.pyplot as plt
from tqdm import tqdm
import gc
import cv2
import argparse
import atari_py

from gym import spaces
from gym.envs.classic_control import CartPoleEnv

parser = argparse.ArgumentParser()
parser.add_argument("--env", help="Name of the environment to use i.e. Pong, Breakoout, etc.",
                    type=str, required=True, choices=["Breakout", "Pong", "CartPole-v1",
                                                      'Ms_Pacman', 'Seaquest', 'Qbert', 'Asteroids',
                                                      'Enduro', 'Space_Invaders', 'Road_Runner', 'Beam_Rider'])

args = parser.parse_args()

class CartPoleImageWrapper(CartPoleEnv):
    def __init__(self, *args, **kwargs):
        super(CartPoleImageWrapper, self).__init__(*args, **kwargs)
        self.observation_space = spaces.Box(low=0, high=255, shape=(84, 84, 1), dtype=np.uint8)
        self.render_mode = 'rgb_array'
        self.max_episode_steps = MAX_EP_LEN
    def _get_image_observation(self):
        # Render the CartPole environment
        cartpole_image = self.render()

        # Convert the image to grayscale
        grayscale_image = cv2.cvtColor(cartpole_image, cv2.COLOR_RGB2GRAY)

        # Resize the image to 84x84 pixels
        resized_image = cv2.resize(grayscale_image, (84, 84))

        return np.expand_dims(resized_image, axis=-1)

    def seed(self, seed=None):
        self.np_random = np.random.RandomState(seed)
        return [seed]

    def reset(self):
        self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        return self._get_image_observation()

    def step(self, action):
        observation, reward, terminated, done, info = super(CartPoleImageWrapper, self).step(action)
        return self._get_image_observation(), reward, terminated, info



N_ENVS = 1
FRAME_STACK = 4
NUM_EPS = 1000
MAX_EP_LEN = 100
ENV_NAME = args.env  # "Pong"

# Create the environment
if ENV_NAME.lower() in atari_py.list_games():
    ENV_NAME = ENV_NAME.replace('_', '')
    ENV_NAME = ENV_NAME+"NoFrameskip-v4"
    vec_env = make_atari_env(ENV_NAME, n_envs=N_ENVS)
else:
    if ENV_NAME == "CartPole-v1":
        env = CartPoleImageWrapper()
        vec_env = make_vec_env(lambda: env, n_envs=N_ENVS)
    else:
        raise NotImplementedError(ENV_NAME + " not implemented yet, try CartPole-v1 or one atari game")

vec_env = VecFrameStack(vec_env, n_stack=FRAME_STACK)
obs = vec_env.reset()

if ENV_NAME.lower() in atari_py.list_games():
    vec_env.render("rgb_array")

SAVE_DIR = "../data/" + ENV_NAME

# Create a directory data with subdirectory "breakout" using os to store the frames
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


frame_count = 0
for i in tqdm(range(1, NUM_EPS + 1)):
    ep_path = SAVE_DIR + f"/{i}"
    if not os.path.exists(ep_path):
        os.makedirs(ep_path)

    done = False
    step = 0

    while not done:
        action = vec_env.action_space.sample()
        new_obs, rewards, dones, infos = vec_env.step(
            [action])  # we need to pass an array of actions in step, one action for each environment

        # obs = obs.reshape(N_ENVS, FRAME_STACK, FRAME_SIZE, FRAME_SIZE, CHANNELS)
        # new_obs = new_obs.reshape(N_ENVS, FRAME_STACK, FRAME_SIZE, FRAME_SIZE)
        new_obs = new_obs.transpose(0, 3, 1, 2)

        new_observations = new_obs[0]
        new_frame = new_observations[-1]


        cv2.imwrite(ep_path + f"/{step}.png", new_frame)
        step += 1
        frame_count += 1


        obs = new_obs
        done = dones[0]

    obs = vec_env.reset()
    # if frame_count >= 1000000:
    #    print("1M frames reached")
    #    break

vec_env.close()
print(f"\n{ENV_NAME} data created - total frames: {frame_count}")
