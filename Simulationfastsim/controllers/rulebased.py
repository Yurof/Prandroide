import random
from numpy import array


class RuleBasedController:

    def __init__(self, env, verbose=False):

        self.env = env
        self.verbose = verbose

        # behavioral parameters
        self.threshold = 150
        self.speed = 0.7

    def get_command(self):

        # get lasers data
        laserRanges = self.env.get_laserranges()
        laserRanges = [100 - i for i in laserRanges]
        if sum(laserRanges[:5]) > self.threshold:
            if self.verbose:
                print("WALL L", sum(laserRanges[:5]))
            return [-self.speed, self.speed]

        elif sum(laserRanges[5:]) > self.threshold:
            if self.verbose:
                print("WALL R", sum(laserRanges[5:]))
            return [self.speed, -self.speed]
        else:
            if self.verbose:
                print("NO WALL ", sum(laserRanges[:5]), sum(laserRanges[5:]))
            return [self.speed, self.speed]

    def reset(self):
        self.threshold = 200
        self.speed = 0.7