#!/usr/bin/python
# -*- coding: utf-8 -*-
import gym
import gym_fastsim
import time
import os
import csv
import argparse
import pickle
from controllers.follow_wall import Follow_wallController
from controllers.forward import ForwardController
from controllers.rulebased import RuleBasedController
from controllers.braitenberg import BraitenbergController
from controllers.novelty_ctr import NoveltyController
# from controllers.novelty.nsga2 import *

ListePosition = []


class SimEnv():

    def __init__(self, env, ctr, file_name, sleep_time, display):
        if env == "kitchen":
            self.env = gym.make("kitchen-v1")
        elif env == "maze_hard":
            self.env = gym.make("maze-v0")
        elif env == "race_track":
            self.env = gym.make("race_track-v0")
        self.env.reset()
        self.sleep_time = sleep_time
        self.display = display
        self.map_size = self.env.get_map_size()

        self.obs, self.rew, self.done, self.info = self.env.step([0, 0])

        # initialize controllers
        if ctr == "forward":
            self.controller = ForwardController(self.env, verbose=False)
        elif ctr == "wall":
            self.controller = Follow_wallController(self.env, verbose=False)
        elif ctr == "rule":
            self.controller = RuleBasedController(self.env, verbose=False)
        elif ctr == "brait":
            self.controller = BraitenbergController(self.env, verbose=False)
        elif ctr == "novelty":
            self.controller = NoveltyController(self.env, file_name)

        if(self.display):
            self.env.enable_display()

    def mouvement(self, c, n=1):
        for _ in range(n):
            obs, rew, done, info = self.env.step(c)
            #print("Valeur de obs :" + str(obs))
            #print("Valeur de rew :" + str(rew))
            #print("Valeur de done :" + str(done))
            #print("Valeur de info :" + str(info))
            if(self.display):
                time.sleep(self.sleep_time)
            if self.done:
                break
            self.env.render()

        return obs, rew, done, info

    def start(self):
        # start timers
        then = time.time()
        self.i = 0

        while (not self.done) and self.i<5000:
            try:
                command = self.controller.get_command()
                self.obs, self.rew, self.done, self.info = self.mouvement(
                    command)
                x, y, theta = self.info['robot_pos']
                ListePosition.append(
                    [self.i, x, (self.map_size-y), theta, self.info["dist_obj"], self.obs])
                self.controller.reset()
                self.i += 1
            except KeyboardInterrupt:
                print('All done')
                break
        now = time.time()
        print("%d timesteps took %f seconds" % (self.i, now - then))
        self.env.close()


def save_result(map_name, controller):
    base_path = os.path.dirname(os.path.abspath(__file__))
    path = f'{base_path}/../results/{map_name}/fastsim_{controller}_'
    i = 1
    if os.path.exists(path+str(i)+".csv"):
        while os.path.exists(path+str(i)+".csv"):
            i += 1
    with open(path+str(i)+".csv", 'w', newline='') as file:
        writer = csv.writer(file)
        print("\ndata saved as ", file)
        writer.writerow(["steps", "x", "y", "roll",
                         "distance_to_obj", "lidar"])
        writer.writerows(ListePosition)

def save_result_ind(criteria, file_name):
    base_path = os.path.dirname(os.path.abspath(__file__))
    path = f'{base_path}/../results/individuals/{criteria}/FastSim/{file_name}'
    if os.path.exists(path+".csv"):
        os.remove(path+".csv")
    with open(path+".csv", 'w', newline='') as file:
        writer = csv.writer(file)
        print("\ndata saved as ", file)
        writer.writerow(["steps", "x", "y", "roll",
                         "distance_to_obj", "lidar"])
        writer.writerows(ListePosition)


def save_result_as(map_name, name):
    base_path = os.path.dirname(os.path.abspath(__file__))
    path = f'{base_path}/../results/{map_name}/fastsim_{name}_'
    i = 1
    if os.path.exists(path+str(i)+".csv"):
        while os.path.exists(path+str(i)+".csv"):
            i += 1
    with open(path+str(i)+".csv", 'w', newline='') as file:
        writer = csv.writer(file)
        print("\ndata saved as ", file)
        writer.writerow(["steps", "x", "y", "roll",
                         "distance_to_obj", "lidar"])
        writer.writerows(ListePosition)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Launch fastsim simulation run.')
    parser.add_argument('--env', type=str, default="maze_hard",
                        help='choose between kitchen, maze_hard and race_track')
    # "forward", "wall", "rule", "brait", "novelty
    parser.add_argument('--ctr', type=str, default="novelty",
                        help='choose between forward, wall, rule, brait and novelty')
    parser.add_argument('--sleep_time', type=int, default=0,
                        help='sleeping time between each step')
    parser.add_argument('--display', type=bool, default=True,
                        help='True or False')
    parser.add_argument('--file_name', type=str,
                        default='NoveltyFitness/3/maze_nsfit3-gen59-p0', help='file name for')
    parser.add_argument('--criteria', type=str,
                        default='null', help='choose between "Fitness", "NoveltySearch", "NoveltyFitness"')

    args = parser.parse_args()
    env = args.env
    ctr = args.ctr
    file_name = args.file_name
    sleep_time = args.sleep_time
    display = args.display
    criteria = args.criteria
    file_name2 = file_name.split("/")[-1]

    simEnv = SimEnv(env, ctr, file_name, sleep_time, display)
    simEnv.start()
    #save_result_as("race_track", "braitenberg")
    if criteria == "null":
        save_result(env, ctr)
    else:
        save_result_ind(criteria, file_name2)

