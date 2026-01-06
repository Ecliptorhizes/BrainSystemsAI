"""
Builder utilities for constructing static environments.

This module provides factory functions and builders for creating
environment instances from configurations.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np

from ..blueprints import (
    StaticEnvironment,
    EnvironmentMetadata,
    WorldState,
    RewardStructure,
    SensoryFieldConfig,
    create_sensory_field,
)


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load environment configuration from YAML file.
    
    Args:
        config_path: Path to YAML config file
        
    Returns:
        Dict: Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file not found
        yaml.YAMLError: If config is invalid YAML
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    
    if not isinstance(config, dict):
        raise ValueError("Config must be a YAML dictionary")
    
    return config


def validate_grid_config(config: Dict[str, Any]) -> None:
    """
    Validate a grid environment configuration.
    
    Args:
        config: Configuration dictionary
        
    Raises:
        ValueError: If config is invalid
    """
    required_fields = ["name", "world", "sensory", "actions", "reward"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
    
    world_config = config.get("world", {})
    if world_config.get("type") != "grid":
        raise ValueError("Grid config must have world.type='grid'")
    
    dimensions = world_config.get("dimensions", [])
    if not isinstance(dimensions, list) or len(dimensions) < 2:
        raise ValueError("Grid world must have at least 2 dimensions")
    
    for dim in dimensions:
        if not isinstance(dim, int) or dim <= 0:
            raise ValueError("All dimensions must be positive integers")
    
    num_actions = config.get("actions", {}).get("num_actions", 4)
    if num_actions < 1:
        raise ValueError("Must have at least one action")


def validate_continuous_config(config: Dict[str, Any]) -> None:
    """
    Validate a continuous field environment configuration.
    
    Args:
        config: Configuration dictionary
        
    Raises:
        ValueError: If config is invalid
    """
    required_fields = ["name", "world", "sensory", "actions", "reward"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
    
    world_config = config.get("world", {})
    if world_config.get("type") != "continuous_field":
        raise ValueError("Continuous config must have world.type='continuous_field'")
    
    dimensions = world_config.get("dimensions", [])
    if not isinstance(dimensions, list) or len(dimensions) < 1:
        raise ValueError("Continuous world must have at least 1 dimension")


class GridEnvironmentBuilder:
    """Builder for grid-based static environments."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize builder with configuration.
        
        Args:
            config: Grid environment configuration
        """
        validate_grid_config(config)
        self.config = config
    
    def build(self) -> "SimpleGridEnvironment":
        """
        Build a grid environment.
        
        Returns:
            SimpleGridEnvironment: Constructed environment
        """
        from .simple_implementations import SimpleGridEnvironment
        
        world_config = self.config.get("world", {})
        dimensions = tuple(world_config.get("dimensions", []))
        
        sensory_config = self.config.get("sensory", {})
        output_shape = tuple(sensory_config.get("output_shape", dimensions))
        
        num_actions = self.config.get("actions", {}).get("num_actions", 4)
        
        metadata = EnvironmentMetadata(
            name=self.config.get("name", "UnnamedGrid"),
            environment_type="grid",
            dimensions=dimensions,
            sensory_output_shape=output_shape,
            num_actions=num_actions,
            description=self.config.get("description"),
        )
        
        reward_config = self.config.get("reward", {})
        reward_structure = RewardStructure(
            reward_type=reward_config.get("type", "discrete"),
            min_reward=reward_config.get("min_reward", -1.0),
            max_reward=reward_config.get("max_reward", 1.0),
        )
        
        return SimpleGridEnvironment(
            metadata=metadata,
            dimensions=dimensions,
            reward_structure=reward_structure,
        )


class ContinuousEnvironmentBuilder:
    """Builder for continuous field static environments."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize builder with configuration.
        
        Args:
            config: Continuous field environment configuration
        """
        validate_continuous_config(config)
        self.config = config
    
    def build(self) -> "SimpleContinuousEnvironment":
        """
        Build a continuous field environment.
        
        Returns:
            SimpleContinuousEnvironment: Constructed environment
        """
        from .simple_implementations import SimpleContinuousEnvironment
        
        world_config = self.config.get("world", {})
        dimensions = tuple(world_config.get("dimensions", []))
        feature_channels = world_config.get("feature_channels", 1)
        
        sensory_config = self.config.get("sensory", {})
        output_shape = tuple(sensory_config.get("output_shape", 
                                                 dimensions + (feature_channels,)))
        
        num_actions = self.config.get("actions", {}).get("num_actions", 8)
        
        metadata = EnvironmentMetadata(
            name=self.config.get("name", "UnnamedContinuous"),
            environment_type="continuous_field",
            dimensions=dimensions,
            sensory_output_shape=output_shape,
            num_actions=num_actions,
            description=self.config.get("description"),
        )
        
        reward_config = self.config.get("reward", {})
        reward_structure = RewardStructure(
            reward_type=reward_config.get("type", "continuous"),
            min_reward=reward_config.get("min_reward", -1.0),
            max_reward=reward_config.get("max_reward", 1.0),
        )
        
        return SimpleContinuousEnvironment(
            metadata=metadata,
            dimensions=dimensions,
            feature_channels=feature_channels,
            reward_structure=reward_structure,
        )


def build_environment_from_config(config_path: str) -> StaticEnvironment:
    """
    Factory function to build environment from config file.
    
    Args:
        config_path: Path to YAML config file
        
    Returns:
        StaticEnvironment: Constructed environment
        
    Raises:
        ValueError: If config type is unknown
    """
    config = load_config(config_path)
    
    world_type = config.get("world", {}).get("type")
    
    if world_type == "grid":
        builder = GridEnvironmentBuilder(config)
        env = builder.build()
    elif world_type == "continuous_field":
        builder = ContinuousEnvironmentBuilder(config)
        env = builder.build()
    else:
        raise ValueError(f"Unknown world type: {world_type}")
    
    env.initialize()
    return env
