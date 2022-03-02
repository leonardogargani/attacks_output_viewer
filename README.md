# Attacks output viewer

Data visualization application for CPA/Template attacks output, mainly based on [PyQt5](https://pypi.org/project/PyQt5),
[PyQtGraph](https://www.pyqtgraph.org), and [NumPy](https://numpy.org).

Further information can be found in the [complete report](report/report.pdf).


## Input data

The input data is a set of 16 CSV files, each one composed by 256 columns and about 30k lines.

The values contained inside those files are real numbers between -1.0 and 1.0.


## Run instructions

First, place the CSV files inside the `data/input/csv/` directory.

Then, as a preprocessing step, run the two initial scripts as specified right below (respect the execution order).

1. Convert the `.csv` files into `.npy` files:
    ```bash
    python utils/csv_to_npy_conversion.py
    ```
   If the script has been successfully executed, then you should find all your new `.npy` files inside
   the `data/output/npy/` directory.

2. Detect the peak of each file, store the result, and generate some images of those bytes:
    ```bash
    python utils/peak_detection.py
    ```
   If the script has been successfully executed, then you should find all the `.png` files inside
   the `data/output/png/` directory and the `peaks.csv` file inside the `data/output/csv/` directory.

Finally, execute the program:
```bash
python main.py
```


## How to use a new set of data

If you need to change the CSV files you want to visualize, you must delete all the `.csv` files under `data/input/csv/`,
add there the new set of `.csv` files, and then re-run the two initial scripts that will overwrite the content
under `data/output/`.


## Codebase structure

After running the two initial scripts, the structure of the codebase will be the following:
```txt
|-- attacks_output_viewer
|   |-- data
|   |   |-- input
|   |   |   `-- csv
|   |   |       |-- 0.csv
|   |   |       |-- 1.csv
|   |   |       |-- 2.csv
|   |   |       |-- 3.csv
|   |   |       |-- 4.csv
|   |   |       |-- 5.csv
|   |   |       |-- 6.csv
|   |   |       |-- 7.csv
|   |   |       |-- 8.csv
|   |   |       |-- 9.csv
|   |   |       |-- 10.csv
|   |   |       |-- 11.csv
|   |   |       |-- 12.csv
|   |   |       |-- 13.csv
|   |   |       |-- 14.csv
|   |   |       |-- 15.csv
|   |   |       `-- README.md
|   |   `-- output
|   |       |-- csv
|   |       |   `-- peaks.csv
|   |       |-- npy
|   |       |   |-- 00.npy
|   |       |   |-- 01.npy
|   |       |   |-- 02.npy
|   |       |   |-- 03.npy
|   |       |   |-- 04.npy
|   |       |   |-- 05.npy
|   |       |   |-- 06.npy
|   |       |   |-- 07.npy
|   |       |   |-- 08.npy
|   |       |   |-- 09.npy
|   |       |   |-- 10.npy
|   |       |   |-- 11.npy
|   |       |   |-- 12.npy
|   |       |   |-- 13.npy
|   |       |   |-- 14.npy
|   |       |   `-- 15.npy
|   |       |-- png
|   |       |   |-- 00_peak.png
|   |       |   |-- 01_peak.png
|   |       |   |-- 02_peak.png
|   |       |   |-- 03_peak.png
|   |       |   |-- 04_peak.png
|   |       |   |-- 05_peak.png
|   |       |   |-- 06_peak.png
|   |       |   |-- 07_peak.png
|   |       |   |-- 08_peak.png
|   |       |   |-- 09_peak.png
|   |       |   |-- 10_peak.png
|   |       |   |-- 11_peak.png
|   |       |   |-- 12_peak.png
|   |       |   |-- 13_peak.png
|   |       |   |-- 14_peak.png
|   |       |   `-- 15_peak.png
|   |       `-- README.md
|   |-- README.md
|   |-- report
|   |   |-- config_files
|   |   |   |-- config.tex
|   |   |   `-- title_page.tex
|   |   |-- img
|   |   |   |-- ...
|   |   |   `-- ...
|   |   |-- report.pdf
|   |   `-- report.tex
|   |-- src
|   |   |-- graph_window.py
|   |   |-- main.py
|   |   |-- main_window.py
|   |   |-- ui
|   |   |   |-- graph_window.ui
|   |   |   `-- main_window.ui
|   |   `-- utils
|   |       |-- csv_to_npy_conversion.py
|   |       `-- peaks_detection.py
```


TODOs:
- when created, add the images to the codebase structure (inside the report subdirectory)

