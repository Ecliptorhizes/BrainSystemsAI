# Development Roadmap

Phased approach to building a brain-controlled robot. Each phase builds on the previous.

---

## Phase 1 — Foundation (Signal Acquisition)

**Goal:** Get brain signals flowing into the system.

### Tasks
- [ ] Set up EEG device driver (OpenBCI, Emotiv, or similar)
- [ ] Implement streaming pipeline (real-time or buffered)
- [ ] Build synthetic signal generator for development without hardware
- [ ] Basic preprocessing: bandpass filter (8–30 Hz for motor imagery), notch (50/60 Hz)

### Deliverables
- `acquisition/eeg/` — working EEG stream
- `acquisition/simulators/` — synthetic motor imagery data
- `acquisition/preprocessing/` — filter pipeline

---

## Phase 2 — Decoding (Motor Imagery → Commands)

**Goal:** Decode imagined movements from EEG.

### Tasks
- [ ] Feature extraction: band power, CSP, or Riemannian
- [ ] Train classifier (LDA, SVM, or Riemannian classifier)
- [ ] Calibration protocol: user imagines left/right/grasp while recording
- [ ] Offline evaluation: accuracy on held-out calibration data

### Deliverables
- `decoding/feature_extraction/` — feature pipeline
- `decoding/motor_imagery/` — classifier
- `decoding/calibration/` — calibration script
- `experiments/calibration.py` — run calibration session

---

## Phase 3 — Simulation (Test Without Robot)

**Goal:** Validate the full pipeline with a simulated robot or cursor.

### Tasks
- [ ] Map decoded classes to simulated actions (e.g., cursor move, virtual arm)
- [ ] Run online BCI with visual feedback
- [ ] Tune parameters (trial length, smoothing, thresholds)

### Deliverables
- Simulated robot or cursor controlled by decoded commands
- Feedback UI for calibration and testing

---

## Phase 4 — Hardware (Real Robot)

**Goal:** Connect to a physical robot.

### Tasks
- [ ] Implement robot interface (ROS, serial, HTTP)
- [ ] Safety: emergency stop, velocity limits, workspace bounds
- [ ] Command mapping: decoded class → robot action (move, grasp, etc.)

### Deliverables
- `control/robot_interface/` — working robot driver
- `control/command_mapping/` — action mapping
- Safety documentation

---

## Phase 5 — Closed Loop (Real-Time Control)

**Goal:** Control the robot in real time with your brain.

### Tasks
- [ ] Real-time decoding loop (low latency)
- [ ] Feedback: visual or proprioceptive (robot position)
- [ ] Adaptive decoding (optional): online recalibration

### Deliverables
- End-to-end brain-controlled robot
- Performance metrics and documentation
