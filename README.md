Signal Segmenter (3-Channel Peak-Aligned GUI)

Signal Segmenter is a desktop application for segmenting electrical time-series signals from three channels (CH1–CH3).
It loads a .txt data file, automatically detects peaks in CH1, and extracts short, user-defined time windows around each peak — saving each as both .txt data files and .jpg visual plots.

This project combines scientific signal processing with a user-friendly Python GUI, and was developed as part of an undergraduate research toolkit at the University of Chicago.

✨ Features

3-channel visualization: CH1, CH2, CH3 vs time.

Automatic peak detection using scipy.signal.find_peaks.

Configurable segmentation window [t_peak - a, t_peak + a].

Time rebasing: each output segment starts at t = 0.

Batch export:

TXT: <inputFileStem>segmen###.txt

JPG: <inputFileStem>segmen###.jpg

GUI visualization:

Left panel: full original signal.

Right panel: first extracted segment.

Cross-platform compatibility (Windows executable via PyInstaller).

🧠 Overview

This app was designed for analyzing electrical signal recordings — for instance, from soft electronics, sensors, or stretchable circuit experiments.
It provides an automated way to extract and visualize repeated transient responses in multi-channel time-series data.

🧩 Project Structure
signal-segmenter/
├─ segmentation.py        # Core segmentation logic (I/O, peak detection, exports)
├─ gui_app.py             # Tkinter GUI with Matplotlib visualization
├─ test_segment.py        # Minimal test of core functions (no GUI)
├─ requirements.txt
└─ README.md


The program separates signal logic and user interface for clarity and maintainability:

segmentation.py: data handling, peak detection, segmentation.

gui_app.py: event-driven GUI that imports and calls the core functions.

📄 Input Data Format

Expected file type: .txt (required)

Column	Meaning	Notes
1	time (s)	time points
2	CH1 (V)	channel 1 (used for peak detection)
3	CH2 (V)	channel 2
4	CH3 (V)	channel 3

The first line (header) is ignored.

The program reads the first four numeric columns starting from the second line.

Supports both whitespace and comma separators.

Example:

time (s) CH1 (V) CH2 (V) CH3 (V)
0.00 2.59 0.004 0.0007
0.01 2.59 0.002 0.0036
...

📤 Output Files

For each detected peak, the app saves:

Data file:
<inputFileStem>segmen001.txt, <inputFileStem>segmen002.txt, …
→ tab-separated file with time (s), CH1 (V), CH2 (V), CH3 (V)
→ time starts at 0.0 for each segment

Image file:
<inputFileStem>segmen001.jpg, <inputFileStem>segmen002.jpg, …
→ plot of CH1–CH3 vs time for each segment

(Optional) Summary file:
peak_times_summary.txt — lists all detected peak indices, times, and CH1 values.

🖥️ GUI Workflow

LOAD

Input a .txt file path or use the file browser.

The left plot shows the full signal.

OUT

Choose or create an output directory.

TIME

Enter the half-window a (in seconds) for segmentation.

START

Peaks are detected automatically.

Segments [t_peak−a, t_peak+a] are saved as TXT + JPG files.

The right panel shows Segment #1.

🧪 Quick Start (Developers)

Install dependencies

python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt


Run a test

python test_segment.py


Launch GUI

python gui_app.py

🧰 Build a Windows Executable (Optional)

If you want to distribute a standalone .exe version:

pyinstaller --noconfirm --onefile --windowed --name Segmenter gui_app.py


If some libraries fail to import (e.g., SciPy, Matplotlib), use:

pyinstaller --noconfirm --onefile --windowed --name Segmenter ^
  --collect-submodules matplotlib --collect-data matplotlib ^
  --collect-submodules scipy --collect-data scipy ^
  gui_app.py


Output:
→ dist/Segmenter.exe

📐 Implementation Highlights

Peak detection:
scipy.signal.find_peaks with adaptive prominence (10% of robust amplitude range).

Segmentation logic:
Uses [t_peak−a, t_peak+a] on CH1 timestamps, applies same window to CH2 & CH3.

Rebased time axis:
Each segment starts at 0 (configurable).

GUI design:
Dual Matplotlib canvases + independent toolbars for zoom/pan.

Output consistency:
Matching TXT/JPG naming per segment for clean dataset exports.

📈 Example Code (Core API)
from segmentation import segment_all

res = segment_all(
    input_path=r"D:\data\example.txt",
    out_dir=r"D:\data\segments_out",
    half_window_s=2.0,
    save_plots=True,
    img_format="jpg",
    time_zero="start",
)

print("Detected peaks:", len(res["peak_times"]))
print("Segments saved:", len(res["saved_files"]))

🎓 Academic Context

Developed by Miller Liao, undergraduate researcher in Physics and Statistics at the University of Chicago.
This project demonstrates:

Practical scientific programming

Data visualization and automation

Peak-based time-series segmentation

Usable software design for lab workflows

🧭 Future Extensions

Add GUI segment browser (choose segment N to display)

Adjustable peak detection parameters (min_prominence, min_distance)

Optional CSV/TSV and PNG/DPI settings

Command-line batch mode

📝 License

MIT License (or your chosen license).
