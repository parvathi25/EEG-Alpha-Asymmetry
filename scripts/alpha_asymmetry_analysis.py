import mne
import glob
import os
import matplotlib.pyplot as plt
import numpy as np

alpha_band = (8, 13)  # Hz

all_files = glob.glob(r"C:\Users\Parvathi\EEG_Alpha_Asymmetry\data\S*/*_preprocessed.fif")

# Prepare lists for plotting
subjects = []
asymmetries = []

for file in all_files:
    raw = mne.io.read_raw_fif(file, preload=True)
    raw.pick_types(eeg=True)
    raw.rename_channels({'F3..': 'F3', 'F4..': 'F4'})

    if 'F3' not in raw.ch_names or 'F4' not in raw.ch_names:
        print(f"F3 or F4 not found in {file}, skipping...")
        continue

    # Compute PSD
    psd_f3, freqs = mne.time_frequency.psd_array_welch(
        raw['F3', :][0][0], sfreq=raw.info['sfreq'], fmin=alpha_band[0], fmax=alpha_band[1], n_fft=2048
    )
    psd_f4, _ = mne.time_frequency.psd_array_welch(
        raw['F4', :][0][0], sfreq=raw.info['sfreq'], fmin=alpha_band[0], fmax=alpha_band[1], n_fft=2048
    )

    # Average alpha power
    power_f3 = psd_f3.mean()
    power_f4 = psd_f4.mean()

    # Compute log alpha asymmetry
    alpha_asymmetry = np.log(power_f4) - np.log(power_f3)

    subjects.append(os.path.basename(file).split('_')[0])
    asymmetries.append(alpha_asymmetry)

# Plot all subjects in a single figure
plt.figure(figsize=(10,5))
plt.bar(subjects, asymmetries, color='skyblue')
plt.axhline(0, color='red', linestyle='--')
plt.ylabel('Alpha Asymmetry (log F4 - log F3)')
plt.title('Frontal Alpha Asymmetry Across Subjects')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()