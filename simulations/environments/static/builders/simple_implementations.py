"""
Simple reference implementations of static environments.

These implementations demonstrate the StaticEnvironment interface
and can serve as baselines for testing.
"""

from typing import Tuple
import numpy as np

from ..blueprints import (
    StaticEnvironment,
    EnvironmentMetadata,
    RewardStructure,
)


class SimpleGridEnvironment(StaticEnvironment):
    """
    Simple 2D grid environment reference implementation.
    
    Features:
    - Discrete grid world (e.g., 10x10)
    - 4-directional movement (up, down, left, right)
    - One-hot encoded sensory output
    - Simple reward structure (goal at fixed location)
    """
    
    def __init__(
        self,
        metadata: EnvironmentMetadata,
        dimensions: Tuple[int, ...],
        reward_structure: RewardStructure,
        goal_position: Tuple[int, int] = (9, 9),
    ):
        """
        Initialize grid environment.
        
        Args:
            metadata: Environment metadata
            dimensions: Grid dimensions
            reward_structure: Reward configuration
            goal_position: Location of goal (default: bottom-right)
        """
        super().__init__(metadata)
        self.dimensions = dimensions
        self.reward_structure = reward_structure
        self.goal_position = goal_position
        self._agent_position = (0, 0)
    
    def initialize(self) -> None:
        """Initialize the grid environment."""
        self._agent_position = (0, 0)
        self._state = {
            "agent_position": self._agent_position,
            "goal_position": self.goal_position,
            "grid_width": self.dimensions[0],
            "grid_height": self.dimensions[1],
        }
        self._is_initialized = True
    
    def get_sensory_input(self) -> np.ndarray:
        """
        Get one-hot encoded sensory input with goal awareness.
        
        Returns:
            np.ndarray: One-hot encoded grid showing agent and goal positions
        """
        sensory = np.zeros(self.metadata.sensory_output_shape, dtype=np.float32)
        sensory[self._agent_position] = 1.0
        sensory[self.goal_position] = 0.5  # Mark goal with lower value to avoid confusion
        return sensory
    
    def compute_reward(self, action: int) -> float:
        """
        Compute reward based on action and current position.
        
        Actions:
            0: Move up
            1: Move down
            2: Move left
            3: Move right
        
        Args:
            action: Action index
            
        Returns:
            float: Reward value
        """
        if action < 0 or action >= self.metadata.num_actions:
            raise ValueError(f"Invalid action: {action}")
        
        # Update position
        new_x, new_y = self._agent_position
        
        if action == 0:  # Up
            new_x = max(0, new_x - 1)
        elif action == 1:  # Down
            new_x = min(self.dimensions[0] - 1, new_x + 1)
        elif action == 2:  # Left
            new_y = max(0, new_y - 1)
        elif action == 3:  # Right
            new_y = min(self.dimensions[1] - 1, new_y + 1)
        
        self._agent_position = (new_x, new_y)
        
        # Compute reward
        if self._agent_position == self.goal_position:
            reward = 1.0
        else:
            reward = -0.01  # Small penalty for each step
        
        return reward


class SimpleContinuousEnvironment(StaticEnvironment):
    """
    Simple continuous field environment reference implementation.
    
    Features:
    - Continuous 2D field with feature channels
    - 8-directional movement
    - Gaussian-encoded sensory output
    - Gradient-based reward structure
    """
    
    def __init__(
        self,
        metadata: EnvironmentMetadata,
        dimensions: Tuple[int, ...],
        feature_channels: int,
        reward_structure: RewardStructure,
        goal_position: Tuple[float, float] = None,
    ):
        """
        Initialize continuous environment.
        
        Args:
            metadata: Environment metadata
            dimensions: Field dimensions
            feature_channels: Number of feature channels
            reward_structure: Reward configuration
            goal_position: Goal location in continuous space
        """
        super().__init__(metadata)
        self.dimensions = dimensions
        self.feature_channels = feature_channels
        self.reward_structure = reward_structure
        
        if goal_position is None:
            goal_position = (dimensions[0] - 1.0, dimensions[1] - 1.0)
        self.goal_position = goal_position
        self._agent_position = np.array([0.0, 0.0], dtype=np.float32)
    
    def initialize(self) -> None:
        """Initialize the continuous environment."""
        self._agent_position = np.array([0.0, 0.0], dtype=np.float32)
        self._state = {
            "agent_position": self._agent_position.copy(),
            "goal_position": self.goal_position,
            "field_width": self.dimensions[0],
            "field_height": self.dimensions[1] if len(self.dimensions) > 1 else 1,
        }
        self._is_initialized = True
    
    def get_sensory_input(self) -> np.ndarray:
        """
        Get Gaussian-encoded sensory input.
        
        Returns:
            np.ndarray: Multi-channel sensory field
        """
        sensory = np.zeros(self.metadata.sensory_output_shape, dtype=np.float32)
        
        # Create Gaussian around agent position
        sigma = 2.0
        x, y = self._agent_position
        
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                dist = np.sqrt((i - x)**2 + (j - y)**2)
                value = np.exp(-(dist**2) / (2 * sigma**2))
                
                for c in range(self.feature_channels):
                    sensory[i, j, c] = value
        
        return sensory
    
    def compute_reward(self, action: int) -> float:
        """
        Compute reward based on distance to goal.
        
        Actions (8-directional):
            0: North, 1: Northeast, 2: East, 3: Southeast
            4: South, 5: Southwest, 6: West, 7: Northwest
        
        Args:
            action: Action index
            
        Returns:
            float: Reward value (distance-based)
        """
        if action < 0 or action >= self.metadata.num_actions:
            raise ValueError(f"Invalid action: {action}")
        
        # Movement vectors for 8-directional
        movements = {
            0: (1, 0),    # North
            1: (1, 1),    # Northeast
            2: (0, 1),    # East
            3: (-1, 1),   # Southeast
            4: (-1, 0),   # South
            5: (-1, -1),  # Southwest
            6: (0, -1),   # West
            7: (1, -1),   # Northwest
        }
        
        dx, dy = movements[action]
        new_x = np.clip(self._agent_position[0] + dx, 0, self.dimensions[0] - 1)
        new_y = np.clip(self._agent_position[1] + dy, 0, self.dimensions[1] - 1)
        
        self._agent_position = np.array([new_x, new_y], dtype=np.float32)
        
        # Reward based on distance to goal
        distance = np.sqrt(
            (self._agent_position[0] - self.goal_position[0])**2 +
            (self._agent_position[1] - self.goal_position[1])**2
        )
        
        max_distance = np.sqrt(
            self.dimensions[0]**2 + self.dimensions[1]**2
        )
        
        reward = 1.0 - (distance / max_distance)
        
        return reward
