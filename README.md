# BrainSystemsAI — Brain-Controlled Robotics

Control robots with your brain using **motor imagery** (the "muscle memory" in your mind). This project builds a **Brain-Computer Interface (BCI)** that reads brain signals from electrodes on your head and translates them into robot commands.

---

## Goal

- **Hardware:** EEG or similar electrodes on your head to capture brain activity
- **Decoding:** Translate motor imagery (imagining movement) into commands
- **Control:** Send those commands to a robot in real time

When you imagine moving your hand left, the robot moves left. When you imagine grasping, it grasps.

---

## About This Project

This is a **personal project** — a fun exploration of brain-computer interfaces and robotics. The work is **open for others to use and build on**; I share it so people outside my immediate community can see the discoveries and contribute or adapt the ideas.

I also plan to **publish** the methodology and results as the project matures, so the research can reach a broader audience.

---

## Project Structure

```
BrainSystemsAI/
├── acquisition/          # Brain signal acquisition (EEG, streaming)
├── decoding/             # Motor imagery → commands (features, classifiers)
├── control/              # Commands → robot (interfaces, mapping)
├── experiments/          # Calibration, offline/online tests
├── configs/              # Device configs, electrode layouts
└── docs/                 # Theory, roadmap, hardware setup
```

---

## Roadmap

| Phase | Goal |
|-------|------|
| **1. Foundation** | Signal acquisition pipeline (EEG driver, streaming, synthetic signals for dev) |
| **2. Decoding** | Motor imagery classifier (feature extraction, calibration, offline decoding) |
| **3. Simulation** | Test with simulated robot/cursor before real hardware |
| **4. Hardware** | Connect to real robot, safety checks |
| **5. Closed Loop** | Real-time brain-controlled robot |

See [docs/roadmap.md](docs/roadmap.md) for details.

---

## Requirements

- Python 3.9+
- EEG device (e.g., OpenBCI, Emotiv) or synthetic data for development
- Robot with controllable interface (ROS, serial, API)

---

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run with synthetic signals (no hardware): `python -m experiments.calibration --synthetic`
3. Calibrate with your EEG: `python -m experiments.calibration`
4. Control robot: `python -m control.run`

---

## Disclaimer

This is a research/educational project. Not for medical or clinical use. Use EEG hardware safely and follow manufacturer guidelines.
