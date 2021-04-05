from typing import Any

import gym

from .definitions import Pose, Velocity
from .vehicles import Vehicle
from iRobot_gym.tasks import Task


class Agent:

    def __init__(self, id: str, vehicle: Vehicle, task, starting_position, starting_orientation):
        self._id = id
        self._vehicle = vehicle
        self._task = task
        self._starting_position = starting_position
        self._starting_orientation = starting_orientation

    @property
    def id(self) -> str:
        return self._id

    @property
    def starting_position(self) -> str:
        return self._starting_position

    @property
    def starting_orientation(self) -> str:
        return self._starting_orientation

    @property
    def vehicle_id(self) -> Any:
        return self._vehicle.id

    @property
    def action_space(self) -> gym.Space:
        return self._vehicle.action_space

    @property
    def observation_space(self) -> gym.Space:
        return self._vehicle.observation_space

    def step(self, action):
        observation = self._vehicle.observe()
        self._vehicle.control(action)
        return observation, {}

    def done(self, state) -> bool:
        return self._task.done(agent_id=self._id, state=state)

    def reward(self, state, action) -> float:
        return self._task.reward(agent_id=self._id, state=state, action=action)

    def reset(self, pose: Pose):
        self._vehicle.reset(pose=pose)
        self._task.reset()
        observation = self._vehicle.observe()
        return observation
