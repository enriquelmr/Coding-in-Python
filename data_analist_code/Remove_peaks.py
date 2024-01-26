import numpy as np
import pandas as pd
from scipy.signal import find_peaks

# Assuming 'data' is your numpy array of relative humidity values
df=pd.read_csv(f'2023-06_SEHUL_monthly-data.csv', sep=',',encoding="iso-8859-1", comment="#")
data = df['RH_ThHyg1_per100_avg']

def find_adjacent_peaks(data, threshold_difference, num_adjacent_min=1, num_adjacent_max=4):
    peaks = []
    
    for num_adjacent in range(num_adjacent_min, num_adjacent_max + 1):
        peaks_indices, _ = find_peaks(data, height=threshold_difference)
        for peak_idx in peaks_indices:
            if peak_idx >= num_adjacent and peak_idx + num_adjacent < len(data):
                peak_range = list(range(peak_idx - num_adjacent, peak_idx + num_adjacent + 1))
                peaks.append(peak_range)
    
    return peaks

threshold_difference = 10  # Set the threshold for peak identification (difference > 10)
adjacent_peaks = find_adjacent_peaks(data, threshold_difference)

# Print the indices of the identified adjacent peaks
print(adjacent_peaks.size())