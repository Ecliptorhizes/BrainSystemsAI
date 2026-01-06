"""
Blueprints for static environment system.

This package provides the core abstractions and base classes for building
static environments.
"""

from .environment_template import (
    StaticEnvironment,
    EnvironmentMetadata,
)
from .sensory_field import (
    SensoryField,
    SensoryFieldConfig,
    GridSensoryField,
    ContinuousSensoryField,
    FeatureVectorField,
    create_sensory_field,
)
from .world_state import (
    WorldState,
    RewardStructure,
    WorldStateBuilder,
)

__all__ = [
    "StaticEnvironment",
    "EnvironmentMetadata",
    "SensoryField",
    "SensoryFieldConfig",
    "GridSensoryField",
    "ContinuousSensoryField",
    "FeatureVectorField",
    "create_sensory_field",
    "WorldState",
    "RewardStructure",
    "WorldStateBuilder",
]
