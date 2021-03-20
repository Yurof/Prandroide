import os
import random
import urllib.request
import zipfile
from typing import List, Tuple

from iRobot_gym import core
from iRobot_gym.bullet.actuators import BulletActuator, Motor
from iRobot_gym.bullet.configs import SensorConfig, VehicleConfig, ActuatorConfig, SceneConfig
from iRobot_gym.bullet.sensors import Lidar, PoseSensor, AccelerationSensor, VelocitySensor, BulletSensor, \
    FixedTimestepSensor
from iRobot_gym.bullet.vehicle import IRobot
from iRobot_gym.envs.specs import WorldSpec, VehicleSpec
from .world import World
from ..core.agent import Agent

base_path = os.path.dirname(os.path.abspath(__file__))

def load_sensor(config: SensorConfig) -> BulletSensor:
    if config.type == 'lidar':
        return Lidar(name=config.name, type=config.type, config=Lidar.Config(**config.params))
    if config.type == 'pose':
        return PoseSensor(name=config.name, type=config.type, config=PoseSensor.Config(**config.params))
    if config.type == 'acceleration':
        return AccelerationSensor(name=config.name, type=config.type, config=AccelerationSensor.Config(**config.params))
    if config.type == 'velocity':
        return VelocitySensor(name=config.name, type=config.type, config=VelocitySensor.Config(**config.params))


def load_actuator(config: ActuatorConfig) -> BulletActuator:
    if config.type == 'motor':
        return Motor(name=config.name, config=Motor.Config(**config.params))

def load_vehicle(spec: VehicleSpec) -> core.Vehicle:
    config_file = f'{base_path}/../../models/{spec.name}/{spec.name}.yml'
    if not os.path.exists(config_file):
        raise NotImplementedError(f'No vehicle with name {spec.name} implemented.')

    config = VehicleConfig()
    config.load(config_file)
    config.urdf_file = f'{os.path.dirname(config_file)}/{config.urdf_file}'
    requested_sensors = set(spec.sensors)
    available_sensors = set([sensor.name for sensor in config.sensors])

    if not requested_sensors.issubset(available_sensors):
        raise NotImplementedError(f'Sensors {requested_sensors - available_sensors} not available.')
    sensors = list(filter(lambda s: s.name in requested_sensors, config.sensors))
    sensors = [FixedTimestepSensor(sensor=load_sensor(config=c), frequency=c.frequency, time_step=0.01) for c in
               sensors]
    actuators = [load_actuator(config=c) for c in config.actuators]
    car_config = IRobot.Config(urdf_file=config.urdf_file)
    vehicle = IRobot(sensors=sensors, actuators=actuators, config=car_config)
    return vehicle


def load_world(spec: WorldSpec, agents: List[Agent]) -> core.World:
    scene_path = f'{base_path}/../../models/scenes'
    config_file = f'{scene_path}/{spec.name}/{spec.name}.yml'

    config = SceneConfig()
    config.load(config_file)
    config.simulation.rendering = spec.rendering

    config.sdf = resolve_path(file=config_file, relative_path=config.sdf)

    world_config = World.Config(
        name=spec.name,
        sdf=config.sdf,
        map_config=config.map,
        time_step=config.simulation.time_step,
        gravity=config.physics.gravity,
        rendering=config.simulation.rendering,
    )

    return World(config=world_config, agents=agents)


def resolve_path(file: str, relative_path: str) -> str:
    file_dir = os.path.dirname(file)
    return f'{file_dir}/{relative_path}'