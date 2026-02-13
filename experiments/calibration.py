"""
Calibration experiment: record motor imagery data for decoder training.

Usage:
    python -m experiments.calibration --synthetic   # No hardware
    python -m experiments.calibration              # With EEG
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="BCI calibration session")
    parser.add_argument("--synthetic", action="store_true", help="Use synthetic data (no EEG)")
    parser.add_argument("--config", default="configs/calibration.yaml", help="Config path")
    args = parser.parse_args()

    if args.synthetic:
        print("Running calibration with synthetic data (Phase 1 placeholder)")
        # TODO: Generate synthetic motor imagery, save for offline training
    else:
        print("Running calibration with EEG (requires hardware)")
        # TODO: Stream from EEG, show cues, record trials


if __name__ == "__main__":
    main()
