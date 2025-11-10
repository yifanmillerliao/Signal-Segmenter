# segmentation.py
import os
from typing import List, Tuple, Optional, Dict, Any
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
import pathlib

TIME_COL = "time (s)"
CH1_COL  = "CH1 (V)"
CH2_COL  = "CH2 (V)"
CH3_COL  = "CH3 (V)"

def read_data_positional(path: str) -> pd.DataFrame:
    """
    Read data by column POSITION, skipping the first header line entirely.
    Expected first 4 numeric columns: time, CH1, CH2, CH3.

    Returns a DataFrame with columns [TIME_COL, CH1_COL, CH2_COL, CH3_COL],
    sorted by time.

    Raises:
        FileNotFoundError, ValueError
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file does not exist: {path}")

    try:
        df = pd.read_csv(
            path,
            sep=r"[,\s]+",
            engine="python",
            header=None,
            skiprows=1,
            comment="#",
            na_filter=True,
        )
    except Exception as e:
        raise ValueError(f"Failed to read input file '{path}': {e}")

    if df.shape[1] < 4:
        raise ValueError(
            f"Expected at least 4 columns (time, CH1, CH2, CH3). Found {df.shape[1]}."
        )

    df = df.iloc[:, :4].copy()

    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=df.columns[:4]).reset_index(drop=True)

    if df.empty:
        raise ValueError("No valid numeric data rows after cleaning.")

    df.columns = [TIME_COL, CH1_COL, CH2_COL, CH3_COL]
    df = df.sort_values(TIME_COL).reset_index(drop=True)
    return df

def _segment_df(df: pd.DataFrame, t0: float, half_window_s: float, time_zero: str = "start") -> pd.DataFrame:
    """
    Extract [t0-a, t0+a] and rebase time to 0 if requested.
    time_zero:
      - "start": segment starts at t=0 (subtract t_start)
      - "peak":  peak is t=0        (subtract t0)
      - "none":  keep original times
    """
    t_start, t_end = t0 - half_window_s, t0 + half_window_s
    seg = df.loc[
        (df[TIME_COL] >= t_start) & (df[TIME_COL] <= t_end),
        [TIME_COL, CH1_COL, CH2_COL, CH3_COL],
    ].copy()

    if seg.empty:
        return seg

    if time_zero == "start":
        seg[TIME_COL] = seg[TIME_COL] - t_start
    elif time_zero == "peak":
        seg[TIME_COL] = seg[TIME_COL] - t0

    return seg.reset_index(drop=True)

def estimate_sampling_period(time_series: pd.Series) -> float:
    """Robustly estimate sampling period (seconds) via median Δt."""
    dt = np.diff(time_series.values)
    if len(dt) == 0:
        return float("nan")
    return float(np.median(dt))


def detect_peaks_ch1(
    df: pd.DataFrame,
    min_prominence: Optional[float] = None,
    min_distance_seconds: Optional[float] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Detect local maxima in CH1 using scipy.signal.find_peaks.

    Returns:
        peaks_idx, peak_times, peak_vals, props

    Notes:
      - If min_prominence is None, uses ~10% of robust range (95th-5th pct).
      - If min_distance_seconds is provided, it's converted to samples via median dt.
    """
    t = df[TIME_COL].values
    y = df[CH1_COL].values

    distance_samples = None
    if min_distance_seconds is not None and len(df) > 1:
        dt = estimate_sampling_period(df[TIME_COL])
        if np.isfinite(dt) and dt > 0:
            distance_samples = max(1, int(round(min_distance_seconds / dt)))

    if min_prominence is None:
        rng = np.percentile(y, 95) - np.percentile(y, 5)
        min_prominence = 0.1 * rng if np.isfinite(rng) else None

    peaks, props = find_peaks(y, prominence=min_prominence, distance=distance_samples)
    return peaks, t[peaks], y[peaks], props

def _save_segment_plot(
    seg: pd.DataFrame,
    dest_path: str,
    title: str,
    dpi: int = 150,
) -> str:
    """
    Save a compact plot of CH1–CH3 vs time for this segment at dest_path.
    """
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(seg[TIME_COL], seg[CH1_COL], label="CH1")
    ax.plot(seg[TIME_COL], seg[CH2_COL], label="CH2")
    ax.plot(seg[TIME_COL], seg[CH3_COL], label="CH3")
    ax.set_title(title)
    ax.set_xlabel(TIME_COL)
    ax.set_ylabel("V")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(dest_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return dest_path

def cut_and_save_segments(
    df: pd.DataFrame,
    peak_times: np.ndarray,
    half_window_s: float,
    outdir: str,
    float_format: str = "%.9f",
    save_plots: bool = False,
    img_format: str = "jpg",
    time_zero: str = "start",
    base_stem: str = "segment_",
) -> dict:
    """
    Save each segment's TSV (and optional plot) with identical base names:
      <base_stem>segmen<###>.txt and <base_stem>segmen<###>.<img_format>
    """
    if not (isinstance(half_window_s, (int, float)) and half_window_s > 0):
        raise ValueError("half_window_s must be a positive number.")

    os.makedirs(outdir, exist_ok=True)

    txt_files, plot_files = [], []

    for i, t0 in enumerate(peak_times, start=1):
        seg = _segment_df(df, t0, half_window_s, time_zero=time_zero)
        if seg.empty:
            continue

        base = f"{base_stem}segment{i:03d}"
        txt_path = os.path.join(outdir, f"{base}.txt")
        seg.to_csv(txt_path, sep="\t", index=False, float_format=float_format)
        txt_files.append(txt_path)

        if save_plots:
            img_path = os.path.join(outdir, f"{base}.{img_format.lower()}")
            _save_segment_plot(
                seg,
                dest_path=img_path,
                title=f"Segment {i}",
            )
            plot_files.append(img_path)

    return {"txt_files": txt_files, "plot_files": plot_files}

def segment_all(
    input_path: str,
    out_dir: str,
    half_window_s: float,
    min_prominence: Optional[float] = None,
    min_distance_seconds: Optional[float] = None,
    save_plots: bool = False,
    img_format: str = "jpg",
    time_zero: str = "start",
) -> Dict[str, Any]:
    # ...
    df = read_data_positional(input_path)

    peaks_idx, peak_times, peak_vals, _ = detect_peaks_ch1(
        df,
        min_prominence=min_prominence,
        min_distance_seconds=min_distance_seconds,
    )

    saved_txt: List[str] = []
    saved_imgs: List[str] = []
    first_segment_df: Optional[pd.DataFrame] = None

    if len(peak_times) > 0:
        base_stem = pathlib.Path(input_path).stem

        saved = cut_and_save_segments(
            df,
            peak_times,
            half_window_s=half_window_s,
            outdir=out_dir,
            save_plots=save_plots,
            img_format=img_format,
            time_zero=time_zero,
            base_stem=base_stem,
        )
        saved_txt = saved["txt_files"]
        saved_imgs = saved["plot_files"]

        first_segment_df = _segment_df(df, peak_times[0], half_window_s, time_zero=time_zero)

    return {
        "df": df,
        "peaks_idx": peaks_idx,
        "peak_times": peak_times,
        "peak_vals": peak_vals,
        "saved_files": saved_txt,
        "plot_files": saved_imgs,
        "first_segment_df": first_segment_df,
    }
