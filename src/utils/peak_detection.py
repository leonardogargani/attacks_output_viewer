import numpy as np
from matplotlib import pyplot as plt
import os
import matplotlib
import gc

matplotlib.use('agg')

NPY_DIRECTORY = "../../data/output/npy/"
PNG_DIRECTORY = "../../data/output/png/"
TXT_DIRECTORY = "../../data/output/txt/"

xMax = np.empty((16,), dtype=int)
yMax = np.empty((16,), dtype=np.float64)
lineMax = np.empty((16,), dtype=int)

for byte_number in range(16):
    print('-------------------- Byte #' + str(byte_number) + ' --------------------')
    print('Loading file...')
    correlation_values = np.load(NPY_DIRECTORY + str(byte_number).zfill(2) + '.npy', mmap_mode='r+')

    # Check if the array contains only NaN values
    if np.all(np.isnan(correlation_values)):
        print('[WARNING] File contains only NaN values, peak detection aborted')

        # Save results
        xMax[byte_number] = -1
        yMax[byte_number] = -1
        lineMax[byte_number] = -1

    else:
        # Replacing NaN values by 0
        where_are_NaNs = np.isnan(correlation_values)
        correlation_values[where_are_NaNs] = 0

        peak = np.nanmax(correlation_values)
        index, line_number = np.where(correlation_values == peak)

        print('Peak value    =', peak)  # Ymax
        print('Sample number =', index[0])  # Xmax
        print('Byte value    =', format(line_number[0], 'b').zfill(8))  # lineMax

        if not os.path.exists(PNG_DIRECTORY + str(byte_number).zfill(2) + '_peak.png'):
            os.makedirs(PNG_DIRECTORY, exist_ok=True)

            print('Saving plot...')

            fig = plt.figure(figsize=(12, 4))
            plt.plot(correlation_values)
            # plt.plot(correlation_values[:, line_number], color='blue', linewidth=0.01)
            plt.ylim([-1, 1.3])
            ax = plt.gca()
            xmax = index[0]
            ymax = peak
            text = "x={}, y={:.3f}".format(xmax, ymax)
            bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
            arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60")
            kw = dict(xycoords='data', textcoords="axes fraction",
                      arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
            ax.annotate(text, xy=(xmax, ymax), xytext=(0.94, 0.96), **kw)
            plt.title('Byte #' + str(byte_number).zfill(2))
            plt.savefig(str(PNG_DIRECTORY + str(byte_number).zfill(2)) + '_peak.png')
            # Free memory
            plt.close(fig)
            del fig, ax
            gc.collect()

        # Save results
        xMax[byte_number] = index[0]
        yMax[byte_number] = peak
        lineMax[byte_number] = line_number[0]

# Write results to txt file
if not os.path.exists(TXT_DIRECTORY):
    os.makedirs(TXT_DIRECTORY, exist_ok=True)

f = open(TXT_DIRECTORY + 'peak.txt', 'w+')
for i in range(16):
    s = str(lineMax[i]) + ',' + str(xMax[i]) + ',' + str(yMax[i]) + '\r\n'
    f.write(s)
f.close()
