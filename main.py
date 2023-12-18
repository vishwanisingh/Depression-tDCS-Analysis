import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import fftpack,  signal
import time
import mne


"""
Evaluation index
0-30 : poor
30 - 50 : fair
50 - 80 : good
80 - 100 : excellent

Extract file ---> collective data ---> raw quality assessment (amplitude * power frequency ratio * alpha band psd ratio)
----> Bad channel removal ----- Not needed [sampling rate correction (500Hz)] ------ filtering (butterworth bandpass - tune coefficient)
----- rereferencing ----- epoching ----- ERP ----- baseline removal ---- 

filtering:
- eye blinks/movemnet removal - EOG correction
- line filter/notch filter - 50 Hz powrt line removal
- butterworth / FIR bandpass - removes frequencies out of this bound
- 

"""
map = {
    1: 'P8',
	2: 'T8',
	3: 'CP6',
	4: 'FC6',
	5: 'F8',
	6: 'F4',
	7: 'C4',
	8: 'P4',
	9: 'AF4',
	10: 'Fp2',
	11: 'Fp1',
	12: 'AF3',
	13: 'Fz',
	14: 'FC2',
	15: 'Cz',
	16: 'CP2',
	17: 'PO3',
	18: 'O1',
	19: 'Oz',
	20: 'O2',
	21: 'PO4',
	22: 'Pz',
	23: 'CP1',
	24: 'FC1',
	25: 'P3',
	26: 'C3',
	27: 'F3',
	28: 'F7',
	29: 'FC5',
	30: 'CP5',
	31: 'T7',
	32: 'P7'
}

# Load the EEG file

folder_path = 'E:/IITD/Depression-IITD/Depression-Sample-dataset-AIIMS/'
sham_or_active = 'Active/' # Active
patient = 'Preeti singh/'
pre_post_intervention = 'pre/'
directory = folder_path + sham_or_active + patient + pre_post_intervention
file_path = directory + '20230718202514_Preeti singh_22.08.23-01_GNG.easy'

# Load EEG data from a file
data = np.loadtxt(file_path, delimiter='\t')

# Extract EEG channels
eeg_data = data[:, :32]
# TODO: 32
num_channels= 32
num_samples = len(eeg_data)
print("EEG data shape", eeg_data.shape)

# EEG sampling rate and duration
sampling_rate = 500 
time_eeg = np.arange(0, num_samples) / sampling_rate

# Frequency bands
# delta_band = (0.5, 4)  # Delta (0.5 - 4 Hz)
# theta_band = (4, 8)    # Theta (4 - 8 Hz)
# alpha_band = (8, 13)   # Alpha (8 - 13 Hz)
# beta_band = (13, 30)   # Beta (13 - 30 Hz)
# gamma_band = (30, 100)  # Gamma (30 - 100 Hz)


def plot_graph(eeg_data, title, activate):

    if 1 in activate:
        # Compute and plot time domain analysis and look for sudden jumps, baseline drifts, and irregularities in the signal.
        plt.figure(figsize=(12, 8))
        for i in range(num_channels):
            plt.plot(time_eeg, eeg_data[:, i])
            plt.xlabel('Time')
            plt.ylabel('Amplitude')
            plt.title(f'{title} - Time-Amplitude - Channel {map[i+1]}')
            plt.savefig(f'Graphs/time-amplitude/{map[i+1]}-{title}-EEG.png')
            plt.pause(0.01)
            plt.close()

    if 2 in activate:
        # Compute and plot FFT to look for certain frequnecy 
        plt.figure(figsize=(10, 5))
        for i in range(num_channels):
            fft_result = np.fft.fft(eeg_data[:, i])
            fft_freq = np.fft.fftfreq(len(eeg_data[:, i]), d=1/sampling_rate)

            plt.plot(fft_freq[:len(eeg_data[:, i])//2], np.abs(fft_result[:len(eeg_data[:, i])//2]))
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('FFT Magnitude')
            plt.title(f'{title} - FFT Magnitude Spectrum - Channel {map[i+1]}')
            plt.savefig(f'Graphs/fft/{map[i+1]}-{title}.png')
            plt.pause(0.01)
            plt.close()

    if 3 in activate:
        # Compute and plot power spectral density using Welch's method - frequency distribution 
        # Welch's method - Converts time domain to frequency domain using FFT and plots - power/frequncy vs frequency 
        # psd_per_channel = []
        plt.figure(figsize=(12, 8))
        for i in range(num_channels):
            frequencies, psd = signal.welch(eeg_data[:, i], fs=sampling_rate, nperseg=1024)
            plt.plot(frequencies, 10 * np.log10(psd))
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Power/Frequency (dB/Hz)')
            plt.title(f'{title} - Power Spectrum - Channel {map[i+1]}')
            plt.savefig(f'Graphs/psd-frequency/{map[i+1]}-{title}.png')
            plt.pause(0.01)
            plt.close()

            # TODO: Is this correct way or these powers should not be summed and be discrete values ? 
            # Else how to identifiy abnormalities and peaks in this?
            # Compute power in each frequency band
            # delta_power = np.sum(psd[(frequencies >= delta_band[0]) & (frequencies < delta_band[1])])
            # theta_power = np.sum(psd[(frequencies >= theta_band[0]) & (frequencies < theta_band[1])])
            # alpha_power = np.sum(psd[(frequencies >= alpha_band[0]) & (frequencies < alpha_band[1])])
            # beta_power = np.sum(psd[(frequencies >= beta_band[0]) & (frequencies < beta_band[1])])
            # gamma_power = np.sum(psd[(frequencies >= gamma_band[0]) & (frequencies < gamma_band[1])])

            # Store the power in each frequency band for this channel
            # band_powers = {
            #     'Delta': delta_power,
            #     'Theta': theta_power,
            #     'Alpha': alpha_power,
            #     'Beta': beta_power,
            #     'Gamma': gamma_power
            # }

            # psd_per_channel.append(band_powers)
            # print(f'Channel {i+1} - Band Powers: {psd_per_channel[i]}')

            # TODO: cross check value an dplot 
            # plt.figure(figsize=(10, 6))
            # plt.plot(frequencies, 10 * np.log10(np.array([delta_power]*len(frequencies))), label='Delta')
            # plt.plot(frequencies, 10 * np.log10(np.array([theta_power]*len(frequencies))), label='Theta')
            # plt.plot(frequencies, 10 * np.log10(np.array([alpha_power]*len(frequencies))), label='Alpha')
            # plt.plot(frequencies, 10 * np.log10(np.array([beta_power]*len(frequencies))), label='Beta')
            # plt.plot(frequencies, 10 * np.log10(np.array([gamma_power]*len(frequencies))), label='Gamma')
            # plt.xlabel('Frequency (Hz)')
            # plt.ylabel('Power/Frequency (dB/Hz)')
            # plt.title(f'Power Spectrum - Channel {i + 1}')
            # plt.legend()
            # plt.grid(True)
            # plt.show()

    if 4 in activate:
        # Compute and plot statistical analysis
        for i in range(num_channels):

            # Time-domain features
            mean_values = np.mean(eeg_data[:, i], axis=0)  # Mean for each channel
            std_dev_values = np.std(eeg_data[:, i], axis=0)  # Standard deviation for each channel
            max_values = np.max(eeg_data[:, i], axis=0)  # Maximum amplitude for each channel
            min_values = np.min(eeg_data[:, i], axis=0)  # Minimum amplitude for each channel
            median_values = np.median(eeg_data[:, i], axis=0)  # Median for each channel

            # Print the calculated features
            print(f"Mean values for channel {map[i+1]}:", mean_values)
            print(f"Standard deviation for each channel {map[i+1]}:", std_dev_values)
            print(f"Maximum amplitude for each channel {map[i+1]}:", max_values)
            print(f"Minimum amplitude for each channel {map[i+1]}:", min_values)
            print(f"Median for each channel {map[i+1]}:", median_values)



# Step 1 - Raw graph with line filter (50Hz)
plot_graph(eeg_data, "1--Raw graph with line filter", [1,2,3])

# Step 2 - Not required : Notch filtering to see if line filter vs notch filter is any different
f0 = 50.0  
Q = 30.0 
b, a = signal.iirnotch(f0, Q, sampling_rate)
filtered_eeg_data = signal.filtfilt(b, a, eeg_data)
# eeg_data = filtered_eeg_data
# If notch filtering is to be added - then add eeg_data = filtered_eeg_data
plot_graph(filtered_eeg_data, "2--Notch filtered graph", [1,2,3]) # Check FFT graph

# Step 3 - Removing mean from each signal - baseline removal 
# Removing mean - centers the signal around 0 - removes dc offset
channel_means = np.mean(eeg_data, axis=0) 
eeg_data_without_mean = eeg_data - channel_means # TODO:
eeg_data = eeg_data_without_mean
# Median filtering - removes impulse noises or outliers
# kernel_size = 5
# filtered_signal = signal.medfilt(eeg_data, kernel_size)
# eeg_data = filtered_signal
plot_graph(eeg_data, "3--Mean removed", [1]) # Check time-amplitude graph

# Step 4 - Bandpass filtering
# Design and apply bandpass filter - smoothes or enhances signals by removing unwanted frequencies
lowcut = 0.01 #Hz
highcut = 45.0 #Hz
nyq = 0.333 * sampling_rate # 1/2 (when signal phase locked) or 1/3
low = lowcut / nyq
high = highcut / nyq
b, a = signal.butter(4, [low, high], btype='band')
filtered_signal = signal.filtfilt(b, a, eeg_data)
eeg_data = filtered_signal

# FIR filter
# numtaps = 101
# fir_filter = signal.firwin(numtaps, [low, high], pass_zero=False)
# filtered_signal = signal.lfilter(fir_filter, 1.0, eeg_data)


print("Filtered Signal:", filtered_signal.shape)
plot_graph(eeg_data, "4-- Bandpass filtered", [2]) # Check psd graph

# Step 5 - EOG Correction Filter - reduce artifcats by eye movements # TODO: 
# plot_graph(eeg_data, "5--EOG corrected filter", [1]) # Check time-amplitude graph 
# print("EOG Corrected Signal:", eog_corrected_signal.shape)

# Step 6 - Re referencing - 
channel_means = np.mean(eeg_data, axis=1, keepdims=True)
eeg_data_avg_referenced = eeg_data - channel_means
eeg_data = eeg_data_avg_referenced
plot_graph(eeg_data, "5--rereferenced", [1]) # Check time-amplitude graph 

# Step 7 - Epoching
epoch_samples = 1000 # 2 seconds
overlap_samples = 250  # 0.5 seconds
segments = []

for i in range(0, len(eeg_data) - epoch_samples + 1, epoch_samples - overlap_samples):
    epoch = eeg_data[i:i + epoch_samples]
    segments.append(epoch)

num_epochs_to_plot = 5
for i in range(num_epochs_to_plot):
    plt.figure(figsize=(10, 4))
    plt.plot(segments[i])
    plt.xlabel('Time (samples)')
    plt.ylabel('Amplitude')
    plt.title(f'Epoch {i+1}')
    plt.show()