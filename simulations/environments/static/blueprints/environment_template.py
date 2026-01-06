"""
Base template for all static environments.

This module defines the abstract interface that all static environments must implement.
Static environments provide fixed, unchanging configurations for sensory inputs and 
world states.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np


@dataclass
class EnvironmentMetadata:
    """Metadata about a static environment."""
    
    name: str
    environment_type: str  # "grid", "continuous_field", etc.
    dimensions: Tuple[int, ...]
    sensory_output_shape: Tuple[int, ...]
    num_actions: int
    num_reward_values: Optional[int] = None
    description: Optional[str] = None
    creation_timestamp: Optional[str] = None


class StaticEnvironment(ABC):
    """
    Abstract base class for static environments.
    
    A static environment is a fixed world configuration that does not change
    during the course of simulation. It provides:
    - Sensory inputs (e.g., visual fields, feature maps)
    - Reward structure (deterministic)
    - State that may be accessed but not modified
    
    Static environments are useful for:
    - Baseline behavior testing
    - Reproducible training scenarios
    - Controlled evaluation conditions
    """
    
    def __init__(self, metadata: EnvironmentMetadata):
        """
        Initialize a static environment.
        
        Args:
            metadata: EnvironmentMetadata describing the environment
        """
        self.metadata = metadata
        self._state: Dict[str, Any] = {}
        self._is_initialized = False
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the environment state.
        
        This should set up all internal structures and state needed
        to generate sensory inputs and compute rewards.
        
        Raises:
            RuntimeError: If initialization fails or is invalid
        """
        pass
    
    @abstractmethod
    def get_sensory_input(self) -> np.ndarray:
        """
        Return the current sensory input from the environment.
        
        Returns:
            np.ndarray: Sensory input with shape metadata.sensory_output_shape
        """
        pass
    
    @abstractmethod
    def compute_reward(self, action: int) -> float:
        """
        Compute reward for a given action.
        
        In a static environment, the reward is deterministic and depends
        only on the current state and action (no stochasticity).
        
        Args:
            action: Integer action index (0 to num_actions - 1)
            
        Returns:
            float: Reward value
            
        Raises:
            ValueError: If action is out of valid range
        """
        pass
    
    def step(self, action: int) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """
        Take a step in the environment.
        
        Returns the new sensory input and reward.
        
        Args:
            action: Integer action to take
            
        Returns:
            (sensory_input, reward, info): 
                - sensory_input: Updated sensory input
                - reward: Reward for the action
                - info: Additional information dict
        """
        if not self._is_initialized:
            raise RuntimeError("Environment not initialized. Call initialize() first.")
        
        reward = self.compute_reward(action)
        sensory_input = self.get_sensory_input()
        
        info = {
            "action": action,
            "reward": reward,
            "state_snapshot": self._get_state_snapshot()
        }
        
        return sensory_input, reward, info
    
    def reset(self) -> np.ndarray:
        """
        Reset the environment to its initial state.
        
        Returns:
            np.ndarray: Initial sensory input
        """
        self.initialize()
        return self.get_sensory_input()
    
    def get_state(self) -> Dict[str, Any]:
        """
        Return the current environment state (read-only).
        
        Returns:
            Dict: Copy of the current state
        """
        return self._state.copy()
    
    def _get_state_snapshot(self) -> Dict[str, Any]:
        """Create a snapshot of the current state for logging."""
        return self._state.copy()
    
    def validate(self) -> bool:
        """
        Validate that the environment is correctly configured.
        
        Returns:
            bool: True if valid, False otherwise
            
        Raises:
            ValueError: If validation fails with detailed error message
        """
        if not self._is_initialized:
            raise ValueError("Environment not initialized")
        
        # Check sensory input shape
        sensory = self.get_sensory_input()
        if sensory.shape != self.metadata.sensory_output_shape:
            raise ValueError(
                f"Sensory output shape mismatch: "
                f"expected {self.metadata.sensory_output_shape}, "
                f"got {sensory.shape}"
            )
        
        # Check reward range (if specified)
        if self.metadata.num_reward_values:
            for action in range(self.metadata.num_actions):
                reward = self.compute_reward(action)
                if not isinstance(reward, (int, float, np.number)):
                    raise ValueError(f"Reward must be numeric, got {type(reward)}")
        
        return True
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.metadata.name}, "
            f"type={self.metadata.environment_type}, "
            f"dims={self.metadata.dimensions})"
        )
