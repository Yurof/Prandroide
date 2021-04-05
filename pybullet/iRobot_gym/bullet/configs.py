from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple

from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class SensorConfig(YamlDataClassConfig):
    type: str = None
    name: str = None
    params: Dict[str, Any] = None
    frequency: float = None


@dataclass
class ActuatorConfig(YamlDataClassConfig):
    type: str
    name: str
    params: Dict[str, Any] = None


@dataclass
class VehicleConfig(YamlDataClassConfig):
    urdf_file: str = None
    debug: bool = False
    actuators: List[ActuatorConfig] = field(default_factory=lambda: [])
    sensors: List[SensorConfig] = field(default_factory=lambda: [])


@dataclass
class GoalConfig(YamlDataClassConfig):
    goal_position: List[float] = field(default_factory=lambda: [])
    goal_size: float = None


@dataclass
class SimulationConfig(YamlDataClassConfig):
    time_step: float = None
    rendering: bool = None


@dataclass
class PhysicsConfig(YamlDataClassConfig):
    gravity: float = None


@dataclass
class TaskSpec(YamlDataClassConfig):
    task_name: str = None
    params: Dict[str, Any] = field(default_factory=lambda: {})


@dataclass
class VehicleSpec(YamlDataClassConfig):
    name: str = None
    sensors: List[str] = field(default_factory=lambda: [])


@dataclass
class WorldSpec(YamlDataClassConfig):
    name: str = None
    rendering: bool = None
    sdf: str = None
    physics: PhysicsConfig = None
    simulation: SimulationConfig = None
    goal: GoalConfig = None


@dataclass
class AgentSpec(YamlDataClassConfig):
    id: str
    vehicle: VehicleSpec = VehicleSpec()
    task: TaskSpec = TaskSpec()
    starting_position: List[float] = field(default_factory=lambda: [])
    starting_orientation: List[float] = field(default_factory=lambda: [])


@dataclass
class ScenarioSpec(YamlDataClassConfig):
    world: WorldSpec = None
    agents: AgentSpec = None
