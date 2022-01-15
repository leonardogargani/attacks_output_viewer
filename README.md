# Attacks output viewer

Data visualization application for CPA/Template attacks output, mainly based on:
- [PyQt5](https://pypi.org/project/PyQt5)
- [PyQtGraph](https://www.pyqtgraph.org)
- [NumPy](https://numpy.org)


## Input data

The input data is a set of 16 CSV files, each one composed by 256 columns and about 140k lines.

The values contained inside those files are real numbers between -1.0 and 1.0.

## Features to implement

The requested features that need to be implemented are the following:
- [ ] Smooth zoom and scrolling
- [ ] Popup labels on mouse pointing
- [ ] Signal generation on click (propagate x, y, plot info data)
- [ ] Control over the X-range
- [ ] Control over the plotted lines to show/hide
- [ ] Highlights of peaks
