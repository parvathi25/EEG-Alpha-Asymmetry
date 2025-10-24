# EEG Alpha Asymmetry Analysis

This repository contains scripts for analyzing **EEG Alpha Asymmetry** - a neurophysiological measure often associated with emotional processing and frontal cortical activity. The project includes data preprocessing, computation of alpha band power, and visualization of asymmetry indices across participants.
The data used for this project was taken from the [EEG Motor Movement/Imagery Dataset](https://physionet.org/content/eegmmidb/1.0.0) from **Physionet**. 3 readings each were taken from the S001, S002 and S003 files.

---

## Data Preprocessing

The EEG preprocessing pipeline was **adapted from the HMNN Lab’s EEG Preprocessing Pipeline**, which includes the following steps:

- Band-pass filtering (1–40 Hz)  
- Re-referencing to average reference  
- Bad channel detection and interpolation  
- Independent Component Analysis (ICA) for artifact removal (eye blinks, muscle noise, etc.)  
- Saving clean data in `.fif` format  

Minor modifications were made to ensure compatibility with the current dataset and analysis requirements.

---

## Alpha Asymmetry Analysis

The analysis focuses on **frontal alpha asymmetry**, computed between the left (F3) and right (F4) channels.

- **Alpha band range:** 8–13 Hz  
- **Computation:**  
  Mean alpha power was estimated for F3 and F4 using Welch’s method.  
  Alpha asymmetry was calculated as:

  \[
  A = \log_{10}(P_{F4}) - \log_{10}(P_{F3})
  \]

- **Interpretation:**  
  - **Positive values:** Greater right hemisphere alpha power (relative left activation)  
  - **Negative values:** Greater left hemisphere alpha power (relative right activation)  

Both the individual alpha power values and the asymmetry index are visualized for each subject.

---

## Visualization

Two main plots are generated for each subject:

1. **Bar graph** showing alpha asymmetry summary across the subjects.
2. **Double Bar Graph** comparing individual alpha power at F3 and F4, overlayed with a **Line Plot** showing alpha asymmetry trends across subjects.  

All visual outputs are saved in the `results/` directory.

---

## Requirements

- Python 3.10+  
- MNE  
- NumPy  
- Matplotlib  
- SciPy  

Install dependencies using:

```bash
pip install -r requirements.txt
```
---

## Acknowledgment

Preprocessing methodology adapted from the HMNN Lab EEG Preprocessing Pipeline.
Further analysis and visualization scripts were developed independently for this project.
