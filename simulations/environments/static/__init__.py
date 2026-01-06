"""
Static Environments Package

This package provides fixed, unchanging environmental configurations
for the brain simulation system.

Key components:
- blueprints: Core abstract classes and interfaces
- builders: Factory functions for creating environments
- validation: Tools for verifying configurations and environments
- configurations: YAML-based environment specs

Example usage:

    from simulations.environments.static.builders import build_environment_from_config
    from simulations.environments.static.validation import EnvironmentValidator
    
    # Load and build environment
    env = build_environment_from_config("configurations/basic_grid.yaml")
    
    # Validate
    EnvironmentValidator.validate_all(env)
    
    # Use
    sensory_input = env.get_sensory_input()
    reward = env.compute_reward(action=0)
"""

from .blueprints import (
    StaticEnvironment,
    EnvironmentMetadata,
    SensoryField,
    SensoryFieldConfig,
    WorldState,
    RewardStructure,
    create_sensory_field,
)

from .builders import (
    load_config,
    validate_grid_config,
    validate_continuous_config,
    GridEnvironmentBuilder,
    ContinuousEnvironmentBuilder,
    build_environment_from_config,
    SimpleGridEnvironment,
    SimpleContinuousEnvironment,
)

from .validation import (
    ConfigValidator,
    EnvironmentValidator,
    ConsistencyChecker,
)

__all__ = [
    # Blueprints
    "StaticEnvironment",
    "EnvironmentMetadata",
    "SensoryField",
    "SensoryFieldConfig",
    "WorldState",
    "RewardStructure",
    "create_sensory_field",
    # Builders
    "load_config",
    "validate_grid_config",
    "validate_continuous_config",
    "GridEnvironmentBuilder",
    "ContinuousEnvironmentBuilder",
    "build_environment_from_config",
    "SimpleGridEnvironment",
    "SimpleContinuousEnvironment",
    # Validation
    "ConfigValidator",
    "EnvironmentValidator",
    "ConsistencyChecker",
]
