import mne
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# Parameters
alpha_band = (8, 13)  # alpha frequency range

def compute_alpha_power(raw, channel_name, alpha_band):
    """Compute average alpha power in the given band for a channel."""
    data, times = raw[channel_name, :]
    # Compute power spectral density
    psd, freqs = mne.time_frequency.psd_array_welch(data[0], sfreq=raw.info['sfreq'],
                                                    fmin=alpha_band[0], fmax=alpha_band[1],
                                                    n_fft=2048)
    # Average power in alpha band
    alpha_power = np.mean(psd)
    return alpha_power

# Get all preprocessed files
all_files = glob.glob(r"C:\Users\Parvathi\EEG_Alpha_Asymmetry\data\S*/*_preprocessed.fif")
all_files.sort()  # optional, to keep subject order consistent

subjects = []
f3_powers = []
f4_powers = []
asymmetries = []

for file in all_files:
    print(f'Processing {file}...')
    raw = mne.io.read_raw_fif(file, preload=True)
    
    # Pick EEG channels only
    raw.pick_types(eeg=True)
    
    # Rename channels if needed
    raw.rename_channels({'F3..': 'F3', 'F4..': 'F4'})
    
    # Compute alpha power
    try:
        alpha_f3 = compute_alpha_power(raw, 'F3', alpha_band)
        alpha_f4 = compute_alpha_power(raw, 'F4', alpha_band)
    except ValueError:
        print(f"Channel F3 or F4 not found in {file}, skipping...")
        continue
    
    subjects.append(os.path.basename(file).split('_')[0])  # S001, S002, etc.
    f3_powers.append(alpha_f3)
    f4_powers.append(alpha_f4)
    
    # Compute asymmetry (log F4 - log F3)
    asymmetry = np.log(alpha_f4) - np.log(alpha_f3)
    asymmetries.append(asymmetry)

# Plotting
x = np.arange(len(subjects))
width = 0.35

fig, ax1 = plt.subplots(figsize=(12, 6))

# Bar plot for F3 and F4
ax1.bar(x - width/2, f3_powers, width, label='F3 Alpha Power', color='skyblue')
ax1.bar(x + width/2, f4_powers, width, label='F4 Alpha Power', color='salmon')
ax1.set_ylabel('Alpha Power (µV²)')
ax1.set_xticks(x)
ax1.set_xticklabels(subjects)
ax1.set_xlabel('Subjects')
ax1.set_title('F3 vs F4 Alpha Power and Asymmetry')
ax1.legend(loc='upper left')

# Line plot for asymmetry on secondary axis
ax2 = ax1.twinx()
ax2.plot(x, asymmetries, color='green', marker='o', label='Alpha Asymmetry')
ax2.set_ylabel('Alpha Asymmetry (log(F4) - log(F3))')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.show()