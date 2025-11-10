# Signal Segmenter GUI

Peaks-based segmentation of multi-channel scope data with a Tkinter + Matplotlib GUI.  
Saves per-peak segments (TXT) and matching quick plots (JPG). Windows .exe via PyInstaller.

## Features
- Position-based parsing of scope exports 
- Peak detection on CH1; segments all channels around each peak
- Time rebase (segment starts at t=0)
- GUI: two plots (full + segment preview), load/out/time/start controls
- Quiet saving of all segment plots and TXT files

