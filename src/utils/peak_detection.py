"""
Script that plots each byte and detects its peak saving the result in a CSV file.
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import os
import gc


NPY_DIRECTORY = "../../data/output/npy/"
PNG_DIRECTORY = "../../data/output/png/"
CSV_DIRECTORY = "../../data/output/csv/"


matplotlib.use('agg')

xMax = np.empty((16,), dtype=int)
yMax = np.empty((16,), dtype=np.float64)
lineMax = np.empty((16,), dtype=int)

for byte_number in range(16):
    print(f'-------------------- Byte #{byte_number} --------------------')
    print('Loading file...')
    correlation_values = np.load(f'{NPY_DIRECTORY}{str(byte_number).zfill(2)}.npy', mmap_mode='r+')

    # Check if the array contains only NaN values
    if np.all(np.isnan(correlation_values)):
        print('[WARNING] File contains only NaN values, peak detection aborted')

        # Save results
        xMax[byte_number] = -1
        yMax[byte_number] = -1
        lineMax[byte_number] = -1

    else:
        # Replace NaN values by 0
        correlation_values[np.isnan(correlation_values)] = 0

        peak = np.nanmax(correlation_values)
        index, line_number = np.where(correlation_values == peak)

        print(f'Peak value    = {peak}')  # Ymax
        print(f'Sample number = {index[0]}')  # Xmax
        print(f'Byte value    = {format(line_number[0], "b").zfill(8)}')  # lineMax

        if not os.path.exists(f'{PNG_DIRECTORY}{str(byte_number).zfill(2)}_peak.png'):
            os.makedirs(f'{PNG_DIRECTORY}', exist_ok=True)

            print('Saving plot...')

            fig = plt.figure(figsize=(12, 4))
            plt.plot(correlation_values)
            plt.ylim([-1, 1.3])
            ax = plt.gca()
            xmax = index[0]
            ymax = peak
            text = f'Line {line_number[0]}, x={xmax}, y={ymax:.3f}'
            bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
            arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60")
            kw = dict(xycoords='data', textcoords="axes fraction",
                      arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
            ax.annotate(text, xy=(xmax, ymax), xytext=(0.94, 0.96), **kw)
            plt.title(f'Byte #{str(byte_number).zfill(2)}')
            plt.savefig(f'{str(PNG_DIRECTORY + str(byte_number).zfill(2))}_peak.png')
            # Free memory
            plt.close(fig)
            del fig, ax
            gc.collect()

        # Save results
        xMax[byte_number] = index[0]
        yMax[byte_number] = peak
        lineMax[byte_number] = line_number[0]

# Write results to txt file
if not os.path.exists(CSV_DIRECTORY):
    os.makedirs(CSV_DIRECTORY, exist_ok=True)

f = open(f'{CSV_DIRECTORY}peak.csv', 'w+')
for i in range(16):
    s = f'{lineMax[i]},{str(xMax[i])},{str(yMax[i])}\r\n'
    f.write(s)
f.close()
