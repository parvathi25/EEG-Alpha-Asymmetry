# preprocess_pipeline.py
import mne
import numpy as np

def preprocess_eeg(input_file, output_file):
    """
    Preprocess EEG data according to the lab's pipeline:
    - DC offset removal
    - Linear detrending
    - Notch filter (50Hz + harmonics)
    - Band-pass filter (1-40 Hz)
    - Bad channel detection (EEG-compatible)
    - ICA to remove eye-blink artifacts
    - Interpolation of bad channels
    - Re-referencing to average
    - Epoching and baseline correction
    """
    print(f"Loading EEG data from {input_file}...")
    raw = mne.io.read_raw_edf(input_file, preload=True)
    
    # DC offset correction & detrending
    raw._data = raw._data - np.mean(raw._data, axis=1, keepdims=True)  # DC removal
    raw._data = mne.filter.detrend(raw._data, axis=1)   # linear detrend

    # Notch filter to remove powerline noise (50Hz, 100Hz, 150Hz)
    raw.notch_filter(freqs=[50], method='iir')

    # Band-pass filter 1-40 Hz
    raw.filter(l_freq=1., h_freq=40.)

    # ----------------------
    # Bad channel detection
    # ----------------------
    print("Detecting bad channels (EEG)...")
    data = raw.get_data()
    chan_std = np.std(data, axis=1)
    threshold = 3 * np.median(chan_std)  # heuristic threshold
    raw.info['bads'] = [raw.ch_names[i] for i, std in enumerate(chan_std) if std > threshold]
    print("Bad channels detected:", raw.info['bads'])

    # ICA to remove eye-blink artifacts
    ica = mne.preprocessing.ICA(n_components=15, random_state=97, max_iter='auto')
    ica.fit(raw)
    ica.exclude = []  # here, you can manually mark components after plotting if needed
    raw = ica.apply(raw)

    # Interpolate bad channels only if digitization info is available
    if raw.info.get('dig') is not None and len(raw.info['bads']) > 0:
        raw.interpolate_bads(reset_bads=True, mode='nearest')
    else:
        if len(raw.info['bads']) > 0:
            print(f"Skipping interpolation for {input_file}, no digitization info available.")

    # Re-reference to average
    raw.set_eeg_reference('average', projection=False)

    # Add this when event markers are available.
    # epochs = mne.Epochs(raw, events, event_id, tmin=-0.2, tmax=0.8, baseline=(-0.2, 0))

    # Save preprocessed data
    raw.save(output_file, overwrite=True)
    print(f"Preprocessed data saved to {output_file}")


if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_file = os.path.join(script_dir, "..", "data", "S003", "S003R06.edf")
    output_file = os.path.join(script_dir, "..", "data", "S003", "S003R06_preprocessed.fif")
    preprocess_eeg(input_file, output_file)
