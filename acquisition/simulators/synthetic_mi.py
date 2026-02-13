"""
Synthetic Motor Imagery (MI) Signal Generator

This creates FAKE brain signals that look like real motor imagery.
Use this to develop and test your BCI pipeline WITHOUT needing EEG hardware.

HOW IT WORKS (simple version):
-----------------------------
When you imagine moving your LEFT hand, the right side of your brain (C4) gets
more active. When you imagine moving your RIGHT hand, the left side (C3) does.
Real EEG measures this. We FAKE it by adding stronger "activity" to the right
channels for each imagined movement.

We create:
  - Class 0 (left hand):  stronger signal in channel C4 (right side)
  - Class 1 (right hand): stronger signal in channel C3 (left side)

The rest is just noise + a bit of structure so a classifier can learn it.
"""

import numpy as np
from typing import Tuple, List


# Channel indices for our 8-channel setup (matches configs/device.yaml)
# C3 = left motor cortex, C4 = right motor cortex (these matter for hand imagery)
CHANNEL_C3 = 2  # Left hemisphere - active during RIGHT hand imagery
CHANNEL_C4 = 3  # Right hemisphere - active during LEFT hand imagery


def generate_trial(
    sampling_rate: int,
    duration_sec: float,
    num_channels: int,
    class_label: int,
    trial_id: int = 0,
) -> np.ndarray:
    """
    Generate ONE trial of fake EEG data for a given motor imagery class.

    A "trial" = one period where you imagine a movement (e.g., 4 seconds).

    Parameters
    ----------
    sampling_rate : int
        How many samples per second (e.g., 250 Hz)
    duration_sec : float
        How long the trial lasts in seconds (e.g., 4.0)
    num_channels : int
        Number of EEG channels (e.g., 8)
    class_label : int
        0 = left hand imagery, 1 = right hand imagery
    trial_id : int
        Just for adding a bit of randomness between trials

    Returns
    -------
    data : np.ndarray
        Shape (num_channels, num_samples) - one trial of fake EEG
    """
    num_samples = int(sampling_rate * duration_sec)

    # Start with random noise (this is like "brain baseline" + measurement noise)
    rng = np.random.default_rng(seed=trial_id)
    data = rng.normal(0, 1, size=(num_channels, num_samples))

    # Add a fake "motor imagery" signal to the relevant channel
    # Real motor imagery causes ~8-30 Hz oscillations; we approximate with a sine wave
    t = np.arange(num_samples) / sampling_rate  # time in seconds
    frequency = 12.0  # Hz - in the mu/beta range
    motor_signal = np.sin(2 * np.pi * frequency * t)

    # Scale it so it's noticeable but not huge
    signal_strength = 0.5 + 0.1 * (trial_id % 5)  # Slight variation per trial

    if class_label == 0:
        # LEFT hand imagery -> RIGHT brain (C4) is more active
        data[CHANNEL_C4, :] += signal_strength * motor_signal
    elif class_label == 1:
        # RIGHT hand imagery -> LEFT brain (C3) is more active
        data[CHANNEL_C3, :] += signal_strength * motor_signal
    else:
        raise ValueError(f"class_label must be 0 or 1, got {class_label}")

    return data.astype(np.float32)


def generate_dataset(
    sampling_rate: int = 250,
    duration_sec: float = 4.0,
    num_channels: int = 8,
    trials_per_class: int = 20,
    num_classes: int = 2,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate a full dataset of synthetic motor imagery trials.

    This is what you'd get from a calibration session: many trials,
    each with a label (which movement was imagined).

    Parameters
    ----------
    sampling_rate : int
        Samples per second (default 250, like many EEG systems)
    duration_sec : float
        Length of each trial in seconds (default 4.0)
    num_channels : int
        Number of EEG channels (default 8)
    trials_per_class : int
        How many trials per class (e.g., 20 left-hand + 20 right-hand)
    num_classes : int
        Usually 2 (left hand, right hand)
    seed : int
        Random seed for reproducibility

    Returns
    -------
    data : np.ndarray
        Shape (n_trials, n_channels, n_samples)
        All trials stacked together
    labels : np.ndarray
        Shape (n_trials,) - 0 or 1 for each trial
    """
    all_trials = []
    all_labels = []

    trial_counter = 0
    for class_label in range(num_classes):
        for _ in range(trials_per_class):
            trial_data = generate_trial(
                sampling_rate=sampling_rate,
                duration_sec=duration_sec,
                num_channels=num_channels,
                class_label=class_label,
                trial_id=trial_counter + seed,
            )
            all_trials.append(trial_data)
            all_labels.append(class_label)
            trial_counter += 1

    # Stack into one big array: (n_trials, n_channels, n_samples)
    data = np.stack(all_trials, axis=0)
    labels = np.array(all_labels, dtype=np.int64)

    return data, labels


def get_class_names() -> List[str]:
    """Return human-readable names for each class."""
    return ["left_hand", "right_hand"]
