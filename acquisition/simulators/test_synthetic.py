"""
Quick test: run this to see synthetic data in action.

Usage:
    python -m acquisition.simulators.test_synthetic
"""

import numpy as np

from .synthetic_mi import generate_dataset, get_class_names


def main():
    print("Generating synthetic motor imagery data...")
    data, labels = generate_dataset(trials_per_class=20, duration_sec=2.0)

    print(f"  Data shape: {data.shape}  (trials, channels, samples)")
    print(f"  Labels: {labels}")
    print(f"  Classes: {get_class_names()}")

    # Quick sanity check: use channel variance (like band power) - C3 vs C4 differ by class
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.model_selection import cross_val_score

    # Simple feature: variance of each channel (C3/C4 have different power per class)
    n_trials, n_channels, n_samples = data.shape
    X = np.var(data, axis=2)  # shape: (n_trials, n_channels)
    y = labels

    clf = LinearDiscriminantAnalysis()
    scores = cross_val_score(clf, X, y, cv=5)
    print(f"\n  Classifier accuracy (5-fold CV, channel variance): {scores.mean():.1%}")
    print("  (High accuracy = synthetic data is separable, pipeline works!)")


if __name__ == "__main__":
    main()
