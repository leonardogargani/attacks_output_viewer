"""Script to detect the peak of each plot

Script that detects the peaks saving the results in a .csv file.
If the corresponding flag is enabled, it also plots each byte saving a png so that the user can statically open it.
"""

import os
import gc
import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib


NPY_DIRECTORY = "../../data/output/npy/"
PNG_DIRECTORY = "../../data/output/png/"
CSV_DIRECTORY = "../../data/output/csv/"


# If the script is executed with the "--save-png" flag, then generate png images
if len(sys.argv) == 2 and sys.argv[1] == "--save-png":
    SAVE_PNG_PLOTS = True
else:
    SAVE_PNG_PLOTS = False


x_peaks_values = np.empty((16,), dtype=int)
y_peaks_values = np.empty((16,), dtype=np.float64)
peaks_lines = np.empty((16,), dtype=int)

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

        y_peak = max(correlation_values.min(initial=0), correlation_values.max(initial=0), key=abs)
        x_peak_array, peak_line_array = np.where(correlation_values == y_peak)
        x_peak = x_peak_array[0]
        peak_line = peak_line_array[0]

        print(f'Peak value    = {y_peak}')
        print(f'Sample number = {x_peak}')

        if SAVE_PNG_PLOTS:
            os.makedirs(f'{PNG_DIRECTORY}', exist_ok=True)
            # Use the Agg non-interactive backend to save the plots
            matplotlib.use('agg')
            # Automatically set simplification and chunking parameters to reasonable settings to speed up plotting
            matplotlib.style.use('fast')
            # Simplify paths by removing "invisible" points to reduce file size and increase rendering speed
            matplotlib.rcParams['path.simplify'] = True
            # Set threshold of similarity below which vertices will be removed in the simplification process
            matplotlib.rcParams['path.simplify_threshold'] = 1.0

            bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
            arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60")
            kw = dict(xycoords='data', textcoords="axes fraction",
                      arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")

            # Plot the byte and highlight the peak
            print('Saving plot...')
            fig = plt.figure(figsize=(12, 4))
            plt.ylim(-1.1*float(abs(y_peak)), 1.3*float(abs(y_peak)))
            plt.plot(correlation_values)

            ax = plt.gca()
            text = f'Line {peak_line}, x={x_peak}, y={y_peak:.3f}'
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
    os.rmdir(CSV_DIRECTORY)
    exit()
