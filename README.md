# Attacks output viewer

Data visualization application for CPA/Template attacks output, based on [PyQtGraph](https://www.pyqtgraph.org)
and [PySide](https://wiki.qt.io/Qt_for_Python).


## Input data

The input data is a set of CSV files, each one with 256 columns and about 100k lines.

The values contained inside those files are real numbers between -1.0 and 1.0.

## Features to implement

The requested features that need to be implemented are the following:
- [ ] Smooth zoom and scrolling
- [ ] Popup labels on mouse pointing
- [ ] Signal generation on click (propagate x, y, plot info data)
- [ ] Control over the X-range
- [ ] Control over the plotted lines to show/hide
- [ ] Highlights of peaks
