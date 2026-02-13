# BCI Basics: Motor Imagery

## What is Motor Imagery?

**Motor imagery** is imagining a movement without actually performing it. When you imagine moving your right hand, your motor cortex shows patterns similar to when you actually move it. These patterns can be detected with EEG.

## Why Motor Imagery?

- **Non-invasive:** No surgery; electrodes on the scalp
- **Intent-based:** You control by thinking, not by moving
- **Learnable:** Users can improve with practice

## The BCI Loop

```
Brain (imagine movement) → EEG electrodes → Preprocessing → Feature extraction
    → Classifier → Command (e.g., "left") → Robot → Feedback
```

## Key Frequencies

- **Mu rhythm (8–12 Hz):** Suppressed when you move or imagine movement
- **Beta rhythm (13–30 Hz):** Also modulated by motor activity
- Typical bandpass for motor imagery: **8–30 Hz**

## Common Approaches

1. **Band power + LDA:** Simple, robust
2. **CSP (Common Spatial Patterns):** Learns optimal spatial filters
3. **Riemannian geometry:** Works on covariance matrices; state-of-the-art for EEG

## References

- Wolpaw & Wolpaw, *Brain-Computer Interfaces: Principles and Practice*
- Blankertz et al., "The BCI Competition" series
