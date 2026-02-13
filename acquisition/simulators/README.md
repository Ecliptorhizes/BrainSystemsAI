# Synthetic Motor Imagery Signals

## What is this?

Fake EEG data that mimics real motor imagery. No hardware needed.

## The idea (simple)

- **Left hand imagery** → more activity in C4 (right brain)
- **Right hand imagery** → more activity in C3 (left brain)

I add a 12 Hz sine wave to the right channel for each class, plus noise.
A classifier can learn to tell them apart — just like with real EEG.

## Usage

```python
from acquisition.simulators.synthetic_mi import generate_dataset, get_class_names

data, labels = generate_dataset(trials_per_class=20)
# data: (40, 8, 1000) = 40 trials, 8 channels, 1000 samples each
# labels: [0,0,...,1,1,...]
```

## Run the test

```bash
python -m acquisition.simulators.test_synthetic
```
