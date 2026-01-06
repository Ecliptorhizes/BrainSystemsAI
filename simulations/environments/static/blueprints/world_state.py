"""
World state management for static environments.

This module handles the storage and access of static world configuration,
including dimensions, features, and reward structures.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple
import numpy as np


@dataclass
class RewardStructure:
    """Definition of how rewards are distributed in the environment."""
    
    reward_type: str  # "discrete", "continuous", "sparse"
    values: Optional[np.ndarray] = None  # Pre-computed reward values
    min_reward: float = -1.0
    max_reward: float = 1.0
    description: Optional[str] = None


@dataclass
class WorldState:
    """
    Immutable representation of a static world configuration.
    
    This class stores all information needed to define and reproduce
    a static environment.
    """
    
    # Basic properties
    name: str
    world_type: str  # "grid", "continuous_field", "abstract"
    dimensions: Tuple[int, ...]
    
    # Sensory properties
    sensory_encoding: str  # "one_hot", "gaussian", "linear"
    sensory_output_shape: Optional[Tuple[int, ...]] = None
    
    # Action properties
    num_actions: int = 4  # Default to 4-directional movement
    action_descriptions: Dict[int, str] = field(default_factory=dict)
    
    # Reward properties
    reward_structure: Optional[RewardStructure] = None
    
    # State representation
    state_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate state after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """Validate world state configuration."""
        if not self.name:
            raise ValueError("World must have a name")
        
        if len(self.dimensions) == 0:
            raise ValueError("World must have at least one dimension")
        
        for dim in self.dimensions:
            if dim <= 0:
                raise ValueError("All dimensions must be positive integers")
        
        if self.num_actions < 1:
            raise ValueError("Must have at least one action")
        
        if self.sensory_output_shape is None:
            # Default to world dimensions if not specified
            self.sensory_output_shape = self.dimensions
    
    def get_state_property(self, key: str) -> Any:
        """
        Get a property from state_data.
        
        Args:
            key: Property key
            
        Returns:
            Any: Property value
            
        Raises:
            KeyError: If key not found
        """
        return self.state_data[key]
    
    def get_state_property_safe(self, key: str, default: Any = None) -> Any:
        """
        Get a property from state_data with default fallback.
        
        Args:
            key: Property key
            default: Default value if key not found
            
        Returns:
            Any: Property value or default
        """
        return self.state_data.get(key, default)
    
    def compute_total_states(self) -> int:
        """
        Compute the total number of possible discrete states.
        
        Returns:
            int: Product of all dimensions (for grid worlds)
        """
        if self.world_type == "grid":
            total = 1
            for dim in self.dimensions:
                total *= dim
            return total
        else:
            # For continuous worlds, return -1 to indicate infinite states
            return -1
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Get metadata.
        
        Args:
            key: Metadata key
            default: Default value
            
        Returns:
            Any: Metadata value or default
        """
        return self.metadata.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert world state to dictionary.
        
        Returns:
            Dict: Dictionary representation
        """
        return {
            "name": self.name,
            "world_type": self.world_type,
            "dimensions": self.dimensions,
            "sensory_encoding": self.sensory_encoding,
            "sensory_output_shape": self.sensory_output_shape,
            "num_actions": self.num_actions,
            "action_descriptions": self.action_descriptions,
            "reward_structure": {
                "reward_type": self.reward_structure.reward_type,
                "min_reward": self.reward_structure.min_reward,
                "max_reward": self.reward_structure.max_reward,
            } if self.reward_structure else None,
            "state_data_keys": list(self.state_data.keys()),
            "metadata": self.metadata,
        }
    
    def __repr__(self) -> str:
        return (
            f"WorldState("
            f"name={self.name}, "
            f"type={self.world_type}, "
            f"dims={self.dimensions}, "
            f"actions={self.num_actions})"
        )


class WorldStateBuilder:
    """Builder pattern for constructing WorldState objects."""
    
    def __init__(self):
        self._name: Optional[str] = None
        self._world_type: Optional[str] = None
        self._dimensions: Tuple[int, ...] = ()
        self._sensory_encoding: str = "one_hot"
        self._sensory_output_shape: Optional[Tuple[int, ...]] = None
        self._num_actions: int = 4
        self._action_descriptions: Dict[int, str] = {}
        self._reward_structure: Optional[RewardStructure] = None
        self._state_data: Dict[str, Any] = {}
        self._metadata: Dict[str, Any] = {}
    
    def with_name(self, name: str) -> "WorldStateBuilder":
        self._name = name
        return self
    
    def with_type(self, world_type: str) -> "WorldStateBuilder":
        self._world_type = world_type
        return self
    
    def with_dimensions(self, *dimensions: int) -> "WorldStateBuilder":
        self._dimensions = dimensions
        return self
    
    def with_sensory_encoding(self, encoding: str) -> "WorldStateBuilder":
        self._sensory_encoding = encoding
        return self
    
    def with_sensory_output_shape(self, shape: Tuple[int, ...]) -> "WorldStateBuilder":
        self._sensory_output_shape = shape
        return self
    
    def with_num_actions(self, num_actions: int) -> "WorldStateBuilder":
        self._num_actions = num_actions
        return self
    
    def with_action_descriptions(self, descriptions: Dict[int, str]) -> "WorldStateBuilder":
        self._action_descriptions = descriptions
        return self
    
    def with_reward_structure(self, reward_structure: RewardStructure) -> "WorldStateBuilder":
        self._reward_structure = reward_structure
        return self
    
    def with_state_data(self, **kwargs) -> "WorldStateBuilder":
        self._state_data.update(kwargs)
        return self
    
    def with_metadata(self, **kwargs) -> "WorldStateBuilder":
        self._metadata.update(kwargs)
        return self
    
    def build(self) -> WorldState:
        """Build the WorldState."""
        if not self._name or not self._world_type:
            raise ValueError("name and world_type are required")
        
        return WorldState(
            name=self._name,
            world_type=self._world_type,
            dimensions=self._dimensions,
            sensory_encoding=self._sensory_encoding,
            sensory_output_shape=self._sensory_output_shape,
            num_actions=self._num_actions,
            action_descriptions=self._action_descriptions,
            reward_structure=self._reward_structure,
            state_data=self._state_data,
            metadata=self._metadata,
        )
