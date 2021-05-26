import time
from time import sleep
import gym
from iRobot_gym.envs import SimpleNavEnv
import os
import csv
import numpy as np


ListePosition = []


class SimEnv():

    def __init__(self, env, sleep_time):
        self.env = gym.make(env+str('-v0'))
        self.env.reset()
        self.sleep_time = sleep_time
        self.obs, self.rew, self.done, self.info = self.env.step([0, 0])

    def mouvement(self, c, n=1):
        for _ in range(n):
            obs, rew, done, info = self.env.step(c)
            time.sleep(self.sleep_time)
            if self.done:
                break
            # self.env.render()

        return obs, rew, done, info

    def start(self):

        self.i = 0
        # start timers
        then = time.time()
        moyenn = []
        while not self.done and self.info['pose'][0] < 100:
            try:
                self.obs, self.rew, self.done, self.info = self.mouvement([
                                                                          1, 1])
                x, y, z, roll, pitch, yaw = self.info['pose']
                # print(self.i, x, y)
                print(self.obs)
                print("info", self.info)
                self.env.get_laserranges()
                self.i += 1
                moyenn.append(self.info['velocity'][0])
                # print(self.info['velocity'][0])
            except KeyboardInterrupt:
                print('All done')
                break
        now = time.time()
        print(self.i)
        print("\ntook %f seconds of execution\n" % (now - then))
        print("real time is:", self.info['time'])
        print('mean velocity', np.mean(moyenn))
        print("\n ")
        self.env.close()

    def rotation(self):

        self.i = 0
        # start timers
        then = time.time()
        moyenn = []
        while not self.done and (self.info['pose'][5] < 0 or self.i < 2):
            try:
                self.obs, self.rew, self.done, self.info = self.mouvement([
                                                                          1, -1])
                x, y, z, roll, pitch, yaw = self.info['pose']
                print(self.i, yaw)
                self.i += 1
                time.sleep(self.sleep_time)
                moyenn.append(self.info['velocity'][0])

                # print(self.info['velocity'][0])
            except KeyboardInterrupt:
                print('All done')
                break
        now = time.time()
        print(self.i)
        print("\ntook %f seconds of execution\n" % (now - then))
        print("real time is:", self.info['time'])
        print('mean velocity', np.mean(moyenn))
        print("\n ")
        self.env.close()


if __name__ == "__main__":
    env1 = 'blank'
    sleep_time = 0.01
    simEnv = SimEnv(env1, sleep_time)
    simEnv.start()