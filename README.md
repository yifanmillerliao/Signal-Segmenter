Signal Segmenter (3-Channel, Peak-Aligned)

A lightweight desktop app for segmenting electrical time-series from three channels (CH1–CH3). It loads a .txt export, automatically detects peaks on CH1, lets you choose a half-window a (seconds), and saves segments around each peak as both tab-separated text files and quick plot images. Time within each segment is rebased to start at t = 0.

Built with a clean separation between the core signal logic and a Tkinter + Matplotlib GUI. Suitable for research workflows and reproducible analysis.

Features

3-channel input: CH1, CH2, CH3 vs time.

Automatic peak detection on CH1 (SciPy find_peaks with adaptive default parameters).

Windowed segmentation: for each detected peak, saves [t_peak − a, t_peak + a].

Time rebasing per segment (starts at t = 0); optional “peak at 0” supported in core API.

Batch export:

TXT: <inputFileStem>segmen###.txt (tab-separated; columns: time (s), CH1 (V), CH2 (V), CH3 (V)).

Images: <inputFileStem>segmen###.jpg (overlay plot of CH1–CH3 vs time).

GUI preview: left panel shows the full recording; right panel previews Segment #1 after processing.

Robust input parsing: ignores the first header line and reads the first four numeric columns by position.

Optional one-file Windows executable via PyInstaller.

Project Structure
segmentation.py       # Core: I/O, peak detection, segmentation, exports
gui_app.py            # Tkinter GUI: two plots + controls
test_segment.py       # Quick smoke test for the core (no GUI)
requirements.txt
README.md


The core (segmentation.py) exposes pure functions (no prints/UI) and returns data or raises exceptions.

The GUI (gui_app.py) handles user interaction and plotting, importing the core as a library.

Input Data Format

File type: .txt (required).

The first line is treated as a header and ignored.

From the second line onward, the first four numeric columns are interpreted as:

time (s)    CH1 (V)    CH2 (V)    CH3 (V)


Delimiters: whitespace or commas are both accepted.

Data are sorted by time internally.

Outputs

For each detected peak i:

TXT (tab-separated):
<inputFileStem>segmen<i:03d>.txt
Columns: time (s), CH1 (V), CH2 (V), CH3 (V) with time rebased to start at 0 within the segment.

Image (overlay plot):
<inputFileStem>segmen<i:03d>.jpg
Compact visualization of CH1–CH3 vs rebased time for the same segment.

Optional summary (if enabled):
peak_times_summary.txt with peak indices, absolute times, and CH1 peak values.

Quick Start (Developers)

Create and activate a virtual environment, then install dependencies:

python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt


(Or: pip install numpy pandas scipy matplotlib pyinstaller)

Smoke test the core (no GUI):

python test_segment.py


Run the GUI:

python gui_app.py

Using the App (GUI)

LOAD: Paste a .txt file path or browse to select one. Left panel plots CH1–CH3 vs time.

OUT: Choose or create an output folder.

TIME: Enter the half-window a in seconds (e.g., 2.0) and confirm.

START: The app detects peaks on CH1, saves segments [t_peak − a, t_peak + a] as TXT and JPG, and previews Segment #1 in the right panel.

Notes:

**Input must be a .txt file; output must be a directory.**

Filenames of TXT and images match: <inputFileStem>segmen###.

Methods & Design Notes

Peak detection: scipy.signal.find_peaks with an adaptive default prominence (~10% of robust range based on the 95th–5th percentile difference). An optional minimum peak distance (in seconds) can be enabled in the core API.

Segmentation: Filters rows within [t_peak − a, t_peak + a]. Time is rebased per segment to t = 0 (configurable in the core; “peak at 0” also supported).

Parsing: Skips the header line and reads the first 4 numeric columns (time, CH1, CH2, CH3), allowing whitespace or commas as delimiters.

Architecture: The core returns structured results (DataFrames, arrays, and saved file paths). The GUI manages state and validates inputs.

Core API Example

pyinstaller --noconfirm --onefile --windowed --name Segmenter gui_app.py


If you encounter missing module/data issues (matplotlib/scipy), try:

pyinstaller --noconfirm --onefile --windowed --name Segmenter ^
  --collect-submodules matplotlib --collect-data matplotlib ^
  --collect-submodules scipy --collect-data scipy ^
  gui_app.py


The executable will be created at dist/Segmenter.exe.

What This Demonstrates (for Applications)

Practical scientific software engineering: separation of logic and UI, robust I/O, clear validation, reproducible outputs.

Applied signal processing: automatic peak detection, windowed segmentation, and time normalization.

Visualization and UX for research tools: dual-panel design with live preview and batch export.

Packaging and deployment: optional single-file executable for easy distribution.

Roadmap (Potential Enhancements)

Segment selector in the GUI (preview any segment N).

UI controls for min_prominence and min_distance_seconds.

CSV/TSV toggle, custom image DPI/size.

Optional preprocessing (denoising, resampling).

CLI mode for headless batch runs.

Requirements

Python 3.10+

numpy, pandas, scipy, matplotlib

pyinstaller (only for building the executable)

Acknowledgments

Developed by Miller Liao (UChicago). Thanks to the open-source Python community for the scientific stack.
