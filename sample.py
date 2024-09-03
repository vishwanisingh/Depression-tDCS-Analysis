# Install mne, matplotlib using command : pip3 install mne matplotlib

import mne
import matplotlib.pyplot as plt

# Set minimum and maximum freq band here for both groups
FMIN = 0
FMAX = 45

# Set names of your groups
GROUP1 = 'GROUP1'
GROUP2 = 'GROUP2'

# Save vhdr files in same directory where this py file is and replace filename here
raw_1 = mne.io.read_raw_brainvision(vhdr_fname)
raw_2 = mne.io.read_raw_brainvision(vhdr_fname)

# Pass list of all channels here
ALL_CHANNELS = raw_1.info['ch_names']

# Do mne signal preprocessing here
#
#

# Function to set custom montage
def set_montage(raw):
    mont1020 = mne.channels.make_standard_montage('standard_1020')
    ind = [i for (i, channel) in enumerate(mont1020.ch_names) if channel in ALL_CHANNELS]
    mont1020_new = mont1020.copy()
    mont1020_new.ch_names = [mont1020.ch_names[x] for x in ind]
    kept_channel_info = [mont1020.dig[x+3] for x in ind]
    mont1020_new.dig = mont1020.dig[0:3]+kept_channel_info
    raw.set_montage(mont1020_new)
    return raw

fig, ax = plt.subplots()
raw_1.plot_psd(picks=raw_1.info['ch_names'], average=True, fmin=FMIN, fmax=FMAX, ax=ax, show=False, color='blue', dB=False)
raw_2.plot_psd(picks=raw_2.info['ch_names'], average=True, fmin=FMIN, fmax=FMAX, ax=ax, show=False, color='red', dB=False)

# dB = True plots PSD in decibels (logarithmic)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Power/Frequency (microV^2/Hz)')
ax.set_title('Power Spectral Density Comparison')

ax.text(0.8, 0.9, GROUP1, color='blue', transform=ax.transAxes)
ax.text(0.8, 0.85, GROUP2, color='red', transform=ax.transAxes)

plt.ylim(0, 8)
plt.show()

# Call set montage function with raw data 
# Sample syntax : raw_1 = set_montage(raw_1)
