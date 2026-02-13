"""
Synthetic brain signal generators.

Use for development and testing without EEG hardware.
"""

from .synthetic_mi import generate_dataset, generate_trial, get_class_names

__all__ = ["generate_dataset", "generate_trial", "get_class_names"]
