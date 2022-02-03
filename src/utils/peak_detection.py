import numpy as np
from matplotlib import pyplot as plt
import os

NPY_DIRECTORY = "../../sample_data/npy/"
PNG_DIRECTORY = "../../sample_data/png/"

plot_enable = False

for byte_number in range(1, 17):
    print('Loading byte ' + str(byte_number) + '...')
    correlation_values = np.load(NPY_DIRECTORY + str(byte_number) + '.npy')
    # Replacing NaN values by 0
    where_are_NaNs = np.isnan(correlation_values)
    correlation_values[where_are_NaNs] = 0
    # Find the absolute maximum of all the entries and its index in the array
    peak = np.amax(correlation_values)
    index, line_number = np.where(correlation_values == peak)

    plt.figure(figsize=(12, 4))
    plt.plot(correlation_values, 'gray')
    plt.plot(correlation_values[:, line_number], color='blue', linewidth=0.01)
    plt.ylim([-1, 1])
    ax = plt.gca()
    xmax = index[0]
    ymax = peak
    text = "x={}, y={:.3f}".format(xmax, ymax)
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data', textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.94, 0.96), **kw)

    plt.title('Byte #' + str(byte_number))

    if plot_enable:
        plt.show()

    if not os.path.exists(PNG_DIRECTORY + str(byte_number) + '_peak.png'):
        os.makedirs(PNG_DIRECTORY, exist_ok=True)
        print('Saving plot ' + str(byte_number) + '...')
        plt.savefig(str(PNG_DIRECTORY + str(byte_number)) + '_peak.png')

    print('--------- Byte #' + str(byte_number) + ' ---------')
    print('Peak value    =', peak)
    print('Sample number =', index[0])
    print('Byte value    =', "{0:b}".format(line_number[0]))
