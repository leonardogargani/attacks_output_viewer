# Attacks output viewer

Data visualization application for CPA/Template attacks output, mainly based on:
- [PyQt5](https://pypi.org/project/PyQt5)
- [PyQtGraph](https://www.pyqtgraph.org)
- [NumPy](https://numpy.org)


## Input data

The input data is a set of 16 CSV files, each one composed by 256 columns and about 140k lines.

The values contained inside those files are real numbers between -1.0 and 1.0.


## Run instructions

First, place the CSV files inside the *sample_data/csv/* directory.

Then, as a preprocessing step, run the script to convert the `.csv` files into `.npy` files:
```bash
python utils/csv_to_npy_converter.py
```

Generate the images highlighting the peaks:
```bash
python utils/peak_detection.py
```

Finally, execute the program:
```bash
python main.py
```


## Features to implement

The requested features that need to be implemented are the following:
- [ ] Smooth zoom and scrolling
- [ ] Popup labels on mouse pointing
- [ ] Signal generation on click (propagate x, y, plot info data)
- [ ] Control over the X-range
- [ ] Control over the plotted lines to show/hide
- [ ] Highlights of peaks
