"""
Sensory field definitions for static environments.

This module defines how sensory information is represented and encoded
in static environments (e.g., grid layouts, continuous fields, feature maps).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple, Union
import numpy as np


@dataclass
class SensoryFieldConfig:
    """Configuration for a sensory field."""
    
    field_type: str  # "grid", "continuous", "feature_vector"
    dimensions: Tuple[int, ...]
    encoding: str  # "one_hot", "gaussian", "linear", "binary"
    value_range: Tuple[float, float] = (0.0, 1.0)
    dtype: type = np.float32


class SensoryField(ABC):
    """
    Abstract base class for sensory fields in static environments.
    
    A sensory field represents how the environment's state is converted
    into sensory signals that can be processed by neural networks.
    """
    
    def __init__(self, config: SensoryFieldConfig):
        """
        Initialize a sensory field.
        
        Args:
            config: SensoryFieldConfig describing the field
        """
        self.config = config
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate field configuration."""
        if len(self.config.dimensions) == 0:
            raise ValueError("Field dimensions cannot be empty")
        
        if self.config.value_range[0] >= self.config.value_range[1]:
            raise ValueError("value_range must be (min, max) with min < max")
    
    @abstractmethod
    def encode(self, state: Union[np.ndarray, int]) -> np.ndarray:
        """
        Encode state information into sensory signal.
        
        Args:
            state: Raw state information to encode
            
        Returns:
            np.ndarray: Encoded sensory signal
        """
        pass
    
    def get_output_shape(self) -> Tuple[int, ...]:
        """Get the shape of the encoded sensory output."""
        return self.config.dimensions
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"type={self.config.field_type}, "
            f"dims={self.config.dimensions})"
        )


class GridSensoryField(SensoryField):
    """
    Sensory field for discrete grid-based environments.
    
    Used for 2D/3D grid worlds where sensory input is a grid of values.
    """
    
    def __init__(self, config: SensoryFieldConfig):
        super().__init__(config)
        if config.field_type != "grid":
            raise ValueError("GridSensoryField requires field_type='grid'")
    
    def encode(self, state: Union[np.ndarray, int]) -> np.ndarray:
        """
        Encode grid state into sensory signal.
        
        Args:
            state: Either a grid array or a position index
            
        Returns:
            np.ndarray: Encoded sensory grid
        """
        if isinstance(state, np.ndarray):
            # Already a grid, just ensure correct shape and range
            encoded = state.astype(self.config.dtype)
        else:
            # State is a position, create one-hot encoding
            encoded = np.zeros(self.config.dimensions, dtype=self.config.dtype)
            if self.config.encoding == "one_hot":
                flat_idx = int(state)
                encoded.flat[flat_idx] = 1.0
            else:
                # For continuous position encoding
                encoded.flat[int(state)] = 1.0
        
        # Clip to value range
        min_val, max_val = self.config.value_range
        encoded = np.clip(encoded, min_val, max_val)
        
        return encoded


class ContinuousSensoryField(SensoryField):
    """
    Sensory field for continuous environments.
    
    Used for continuous-valued sensory inputs like feature maps or
    spatially distributed signals.
    """
    
    def __init__(self, config: SensoryFieldConfig):
        super().__init__(config)
        if config.field_type != "continuous":
            raise ValueError("ContinuousSensoryField requires field_type='continuous'")
    
    def encode(self, state: np.ndarray) -> np.ndarray:
        """
        Encode continuous state into sensory signal.
        
        Args:
            state: Continuous-valued array
            
        Returns:
            np.ndarray: Encoded sensory signal
        """
        if not isinstance(state, np.ndarray):
            raise TypeError("ContinuousSensoryField requires numpy array input")
        
        encoded = state.astype(self.config.dtype)
        
        # Clip to value range
        min_val, max_val = self.config.value_range
        encoded = np.clip(encoded, min_val, max_val)
        
        return encoded


class FeatureVectorField(SensoryField):
    """
    Sensory field for discrete feature vectors.
    
    Used for representing environments as fixed feature sets
    (e.g., object presence, property values).
    """
    
    def __init__(self, config: SensoryFieldConfig):
        super().__init__(config)
        if config.field_type != "feature_vector":
            raise ValueError("FeatureVectorField requires field_type='feature_vector'")
        
        if len(config.dimensions) != 1:
            raise ValueError("FeatureVectorField must have 1D dimensions")
    
    def encode(self, state: Union[np.ndarray, list]) -> np.ndarray:
        """
        Encode feature vector state.
        
        Args:
            state: Feature vector (1D array or list)
            
        Returns:
            np.ndarray: Encoded feature vector
        """
        if isinstance(state, list):
            state = np.array(state)
        
        if state.shape != self.config.dimensions:
            raise ValueError(
                f"Feature vector shape mismatch: "
                f"expected {self.config.dimensions}, got {state.shape}"
            )
        
        encoded = state.astype(self.config.dtype)
        
        # Clip to value range
        min_val, max_val = self.config.value_range
        encoded = np.clip(encoded, min_val, max_val)
        
        return encoded


def create_sensory_field(config: SensoryFieldConfig) -> SensoryField:
    """
    Factory function to create appropriate sensory field type.
    
    Args:
        config: SensoryFieldConfig
        
    Returns:
        SensoryField: Appropriate field instance
        
    Raises:
        ValueError: If field_type is unknown
    """
    if config.field_type == "grid":
        return GridSensoryField(config)
    elif config.field_type == "continuous":
        return ContinuousSensoryField(config)
    elif config.field_type == "feature_vector":
        return FeatureVectorField(config)
    else:
        raise ValueError(f"Unknown sensory field type: {config.field_type}")
