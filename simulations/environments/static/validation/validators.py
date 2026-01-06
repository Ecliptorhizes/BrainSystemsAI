"""
Validation tools for static environment configurations.

This module provides utilities to verify that environment configurations
are valid and consistent.
"""

from typing import Dict, Any, List, Optional
import numpy as np

from ..blueprints import StaticEnvironment, EnvironmentMetadata


class ConfigValidator:
    """Validates environment configurations."""
    
    @staticmethod
    def validate_schema(config: Dict[str, Any]) -> List[str]:
        """
        Validate configuration schema.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            List[str]: List of error messages (empty if valid)
        """
        errors = []
        
        required_fields = ["name", "world", "sensory", "actions", "reward"]
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        # Check world config
        world = config.get("world", {})
        if "type" not in world:
            errors.append("Missing world.type")
        elif world["type"] not in ["grid", "continuous_field", "abstract"]:
            errors.append(f"Unknown world type: {world['type']}")
        
        if "dimensions" not in world:
            errors.append("Missing world.dimensions")
        elif not isinstance(world["dimensions"], list):
            errors.append("world.dimensions must be a list")
        else:
            for i, dim in enumerate(world["dimensions"]):
                if not isinstance(dim, int) or dim <= 0:
                    errors.append(
                        f"world.dimensions[{i}] must be a positive integer, "
                        f"got {dim}"
                    )
        
        # Check sensory config
        sensory = config.get("sensory", {})
        if "encoding" not in sensory:
            errors.append("Missing sensory.encoding")
        
        # Check actions
        actions = config.get("actions", {})
        if "num_actions" in actions:
            if not isinstance(actions["num_actions"], int) or actions["num_actions"] < 1:
                errors.append("actions.num_actions must be a positive integer")
        
        # Check reward
        reward = config.get("reward", {})
        if "type" not in reward:
            errors.append("Missing reward.type")
        elif reward["type"] not in ["discrete", "continuous", "sparse"]:
            errors.append(f"Unknown reward type: {reward['type']}")
        
        return errors
    
    @staticmethod
    def validate_consistency(config: Dict[str, Any]) -> List[str]:
        """
        Validate consistency between configuration components.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            List[str]: List of error messages (empty if valid)
        """
        errors = []
        
        world = config.get("world", {})
        sensory = config.get("sensory", {})
        
        dimensions = world.get("dimensions", [])
        output_shape = sensory.get("output_shape")
        
        if output_shape:
            if len(output_shape) != len(dimensions):
                errors.append(
                    f"sensory.output_shape dimensions ({len(output_shape)}) "
                    f"must match world.dimensions ({len(dimensions)})"
                )
        
        reward = config.get("reward", {})
        min_reward = reward.get("min_reward", -1.0)
        max_reward = reward.get("max_reward", 1.0)
        
        if min_reward >= max_reward:
            errors.append(
                f"reward.min_reward ({min_reward}) must be < "
                f"reward.max_reward ({max_reward})"
            )
        
        return errors
    
    @staticmethod
    def validate_all(config: Dict[str, Any]) -> bool:
        """
        Validate configuration comprehensively.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            bool: True if valid
            
        Raises:
            ValueError: If validation fails with detailed errors
        """
        schema_errors = ConfigValidator.validate_schema(config)
        consistency_errors = ConfigValidator.validate_consistency(config)
        
        all_errors = schema_errors + consistency_errors
        
        if all_errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(
                f"  - {err}" for err in all_errors
            )
            raise ValueError(error_msg)
        
        return True


class EnvironmentValidator:
    """Validates environment instances."""
    
    @staticmethod
    def validate_sensory_output(env: StaticEnvironment) -> List[str]:
        """
        Validate sensory output from environment.
        
        Args:
            env: StaticEnvironment instance
            
        Returns:
            List[str]: List of error messages
        """
        errors = []
        
        try:
            sensory = env.get_sensory_input()
        except Exception as e:
            errors.append(f"Failed to get sensory input: {e}")
            return errors
        
        if not isinstance(sensory, np.ndarray):
            errors.append(
                f"Sensory output must be numpy array, got {type(sensory)}"
            )
        
        if sensory.shape != env.metadata.sensory_output_shape:
            errors.append(
                f"Sensory shape mismatch: expected "
                f"{env.metadata.sensory_output_shape}, got {sensory.shape}"
            )
        
        if np.isnan(sensory).any():
            errors.append("Sensory output contains NaN values")
        
        if np.isinf(sensory).any():
            errors.append("Sensory output contains infinite values")
        
        return errors
    
    @staticmethod
    def validate_rewards(env: StaticEnvironment) -> List[str]:
        """
        Validate reward computation.
        
        Args:
            env: StaticEnvironment instance
            
        Returns:
            List[str]: List of error messages
        """
        errors = []
        
        for action in range(env.metadata.num_actions):
            try:
                reward = env.compute_reward(action)
            except Exception as e:
                errors.append(f"Failed to compute reward for action {action}: {e}")
                continue
            
            if not isinstance(reward, (int, float, np.number)):
                errors.append(
                    f"Reward must be numeric, got {type(reward)} "
                    f"for action {action}"
                )
            elif np.isnan(reward):
                errors.append(f"Reward is NaN for action {action}")
            elif np.isinf(reward):
                errors.append(f"Reward is infinite for action {action}")
        
        return errors
    
    @staticmethod
    def validate_all(env: StaticEnvironment) -> bool:
        """
        Validate environment comprehensively.
        
        Args:
            env: StaticEnvironment instance
            
        Returns:
            bool: True if valid
            
        Raises:
            ValueError: If validation fails
        """
        sensory_errors = EnvironmentValidator.validate_sensory_output(env)
        reward_errors = EnvironmentValidator.validate_rewards(env)
        
        all_errors = sensory_errors + reward_errors
        
        if all_errors:
            error_msg = f"Environment validation failed for {env.metadata.name}:\n"
            error_msg += "\n".join(f"  - {err}" for err in all_errors)
            raise ValueError(error_msg)
        
        return True


class ConsistencyChecker:
    """Checks consistency properties of static environments."""
    
    @staticmethod
    def check_determinism(env: StaticEnvironment, num_samples: int = 10) -> bool:
        """
        Verify that environment is deterministic.
        
        Args:
            env: StaticEnvironment instance
            num_samples: Number of samples to test
            
        Returns:
            bool: True if deterministic
            
        Raises:
            ValueError: If environment is not deterministic
        """
        for action in range(min(num_samples, env.metadata.num_actions)):
            # Get sensory outputs
            sensory1 = env.get_sensory_input().copy()
            reward1 = env.compute_reward(action)
            
            env.reset()
            
            sensory2 = env.get_sensory_input().copy()
            reward2 = env.compute_reward(action)
            
            if not np.allclose(sensory1, sensory2):
                raise ValueError(
                    f"Sensory output not deterministic for action {action}"
                )
            
            if reward1 != reward2:
                raise ValueError(
                    f"Reward not deterministic for action {action}: "
                    f"{reward1} vs {reward2}"
                )
        
        return True
    
    @staticmethod
    def check_bounds(env: StaticEnvironment) -> bool:
        """
        Verify that rewards are within expected bounds.
        
        Args:
            env: StaticEnvironment instance
            
        Returns:
            bool: True if all rewards are within bounds
            
        Raises:
            ValueError: If any reward is out of bounds
        """
        min_bound = -1e6
        max_bound = 1e6
        
        for action in range(env.metadata.num_actions):
            reward = env.compute_reward(action)
            
            if reward < min_bound or reward > max_bound:
                raise ValueError(
                    f"Reward out of expected bounds for action {action}: {reward}"
                )
        
        return True
