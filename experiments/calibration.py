"""
Calibration experiment: record motor imagery data for decoder training.

Usage:
    python -m experiments.calibration --synthetic   # No hardware (generates fake data)
    python -m experiments.calibration              # With EEG (not yet implemented)
"""

import argparse
from pathlib import Path

import numpy as np
import yaml


def load_config(config_path: str) -> dict:
    """Load calibration config from YAML. Returns defaults if file not found."""
    path = Path(config_path)
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f)
    return {
        "classes": ["left_hand", "right_hand"],
        "trial": {"duration_sec": 4.0, "cue_duration_sec": 1.0, "rest_between_sec": 2.0},
        "trials_per_class": 20,
    }


def run_synthetic_calibration(config: dict, output_dir: str = "data/calibration") -> None:
    """
    Generate synthetic motor imagery data (no EEG needed).

    Saves data and labels to output_dir for later use in training the decoder.
    """
    from acquisition.simulators import generate_dataset, get_class_names

    trials_per_class = config.get("trials_per_class", 20)
    duration_sec = config.get("trial", {}).get("duration_sec", 4.0)
    num_classes = len(config.get("classes", ["left_hand", "right_hand"]))

    print(f"  Generating {trials_per_class} trials per class ({num_classes} classes)")
    print(f"  Trial duration: {duration_sec} sec")
    print(f"  Classes: {get_class_names()}")

    data, labels = generate_dataset(
        trials_per_class=trials_per_class,
        duration_sec=duration_sec,
        num_classes=num_classes,
    )

    # Save to disk
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    np.save(out_path / "data.npy", data)
    np.save(out_path / "labels.npy", labels)

    print(f"\n  Saved to {out_path.absolute()}")
    print(f"  data.npy: shape {data.shape}")
    print(f"  labels.npy: shape {labels.shape}")


def main():
    parser = argparse.ArgumentParser(description="BCI calibration session")
    parser.add_argument("--synthetic", action="store_true", help="Use synthetic data (no EEG)")
    parser.add_argument("--config", default="configs/calibration.yaml", help="Config path")
    parser.add_argument("--output", default="data/calibration", help="Output directory for saved data")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.synthetic:
        print("Running calibration with synthetic data (no hardware needed)\n")
        run_synthetic_calibration(config, output_dir=args.output)
    else:
        print("Running calibration with EEG (requires hardware)")
        print("  Not yet implemented. Use --synthetic to test with fake data.")


if __name__ == "__main__":
    main()
