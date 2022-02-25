"""Script to detect the peak of each plot

Script that plots each byte and saves it so that the user can statically open it.
It also detects the peaks saving the results in a .csv file.
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import os
import gc

NPY_DIRECTORY = "../../data/output/npy/"
PNG_DIRECTORY = "../../data/output/png/"
CSV_DIRECTORY = "../../data/output/csv/"


# Use the Agg non-interactive backend, to save the plots
matplotlib.use('agg')

x_peaks_values = np.empty((16,), dtype=int)
y_peaks_values = np.empty((16,), dtype=np.float64)
peaks_lines = np.empty((16,), dtype=int)

os.makedirs(f'{PNG_DIRECTORY}', exist_ok=True)
os.makedirs(f'{CSV_DIRECTORY}', exist_ok=True)

try:
    for byte_number in range(16):
        correlation_values = np.load(f'{NPY_DIRECTORY}{str(byte_number).zfill(2)}.npy', mmap_mode='r+')
        print(f'-------------- Byte #{byte_number} --------------')

        # Check if the array contains only NaN values
        if np.all(np.isnan(correlation_values)):
            print('[WARNING] File contains only NaN values, peak detection aborted')
            x_peaks_values[byte_number] = -1
            y_peaks_values[byte_number] = -1
            peaks_lines[byte_number] = -1
            continue

        # Replace NaN values with 0
        correlation_values[np.isnan(correlation_values)] = 0

        y_peak = np.nanmax(correlation_values)
        x_peak_array, peak_line_array = np.where(correlation_values == y_peak)
        x_peak = x_peak_array[0]
        peak_line = peak_line_array[0]

        print(f'Peak value    = {y_peak}')
        print(f'Sample number = {x_peak}')

        # Plot the byte and highlight the peak
        print('Saving plot...')
        fig = plt.figure(figsize=(12, 4))
        plt.plot(correlation_values)
        plt.ylim([-1, 1.3])
        ax = plt.gca()
        text = f'Line {peak_line}, x={x_peak}, y={y_peak:.3f}'
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60")
        kw = dict(xycoords='data', textcoords="axes fraction",
                  arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
        ax.annotate(text, xy=(x_peak, y_peak), xytext=(0.94, 0.96), **kw)
        plt.title(f'Byte #{str(byte_number).zfill(2)}')
        plt.savefig(f'{str(PNG_DIRECTORY + str(byte_number).zfill(2))}_peak.png')

        plt.close(fig)
        del fig, ax
        gc.collect()

        # Save results
        x_peaks_values[byte_number] = x_peak
        y_peaks_values[byte_number] = y_peak
        peaks_lines[byte_number] = peak_line

    # Save information about the peaks inside a .csv file
    peaks_file = open(f'{CSV_DIRECTORY}peaks.csv', 'w+')
    for i in range(16):
        line = f'{peaks_lines[i]},{str(x_peaks_values[i])},{str(y_peaks_values[i])}\r\n'
        peaks_file.write(line)
    peaks_file.close()

except FileNotFoundError:
    print('[ERROR] No .npy file found. Run "csv_to_npy_conversion.py" script before.')
    os.rmdir(PNG_DIRECTORY)
    os.rmdir(CSV_DIRECTORY)
    exit()
