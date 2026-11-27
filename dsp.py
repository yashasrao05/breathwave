"""Audio preparation, envelopes, and candidate peak rates, independent of Streamlit."""

from io import BytesIO
from math import gcd

import numpy as np
import soundfile as sf
from scipy.signal import butter, find_peaks, resample_poly, sosfiltfilt


AUDIO_CONFIG = {
    "sample_rate": 16000,
    "min_source_sample_rate": 8000,
    "min_duration_s": 30,
    "max_duration_s": 120,
    "max_upload_bytes": 50 * 1024 * 1024,
    "silence_rms": 1e-6,
    "audio_band_hz": (100.0, 2000.0),
    "envelope_band_hz": (0.1, 0.8),
    "filter_design_order": 2,
    "rms_window_s": 0.25,
    "rms_hop_s": 0.05,
    "edge_margin_s": 5.0,
    "peak_prominence_fraction": 0.15,
    "min_cycle_markers": 3,
    "flat_envelope_fraction": 0.01,
    "interval_cv_warning": 0.2,
}


def read_wav(audio_bytes):
    """Decode a mono/stereo WAV, checking its header before loading samples."""
    if not audio_bytes:
        raise ValueError("The audio file is empty. Upload or record a WAV sample.")
    if len(audio_bytes) > AUDIO_CONFIG["max_upload_bytes"]:
        raise ValueError("The audio file is too large. Use a WAV file under 50 MB.")

    try:
        with sf.SoundFile(BytesIO(audio_bytes)) as audio_file:
            if audio_file.format not in {"WAV", "WAVEX", "RF64"}:
                raise ValueError("Unsupported audio format. Please upload a WAV file.")
            source_rate = audio_file.samplerate
            channels = audio_file.channels
            if audio_file.frames == 0:
                raise ValueError("This WAV contains no audio samples. Record again.")
            duration = audio_file.frames / source_rate
            if channels not in (1, 2):
                raise ValueError("Use a mono or stereo WAV file (one or two channels).")
            if source_rate < AUDIO_CONFIG["min_source_sample_rate"]:
                raise ValueError("The sample rate is too low. Use at least 8000 Hz.")
            if not AUDIO_CONFIG["min_duration_s"] <= duration <= AUDIO_CONFIG["max_duration_s"]:
                raise ValueError(
                    f"This clip is {duration:.1f} seconds long. Use 30 to 120 seconds; "
                    "about 60 seconds is recommended."
                )
            original = audio_file.read(dtype="float64", always_2d=True)
    except (RuntimeError, OSError) as error:
        raise ValueError("Could not read this WAV file. It may be damaged or unsupported.") from error

    if len(original) != audio_file.frames:
        raise ValueError("The WAV is incomplete. Export or record the file again.")
    if not np.isfinite(original).all():
        raise ValueError("The recording contains invalid sample values. Export a new WAV file.")

    return {
        "original_audio": original,
        "source_sample_rate": source_rate,
        "channels": channels,
        "duration_s": duration,
        "subtype": audio_file.subtype,
        "original_peak": float(np.max(np.abs(original))),
    }


def prepare_audio(recording):
    """Average channels, remove DC, and resample without peak normalization."""
    mono = recording["original_audio"].mean(axis=1)
    dc_offset = float(mono.mean())
    centered = mono - dc_offset
    rms = float(np.sqrt(np.mean(centered**2)))
    if not np.isfinite(rms):
        raise ValueError("The sample amplitudes cannot be processed. Export a new WAV file.")
    if rms <= AUDIO_CONFIG["silence_rms"]:
        raise ValueError(
            "No usable sound remains after channel averaging and DC removal. "
            "Check the microphone and record again in a quiet room."
        )

    target_rate = AUDIO_CONFIG["sample_rate"]
    source_rate = recording["source_sample_rate"]
    if source_rate == target_rate:
        prepared = centered.copy()
    else:
        divisor = gcd(source_rate, target_rate)
        prepared = resample_poly(centered, target_rate // divisor, source_rate // divisor)

    if not np.isfinite(prepared).all():
        raise ValueError("Audio preparation failed. Try exporting a new WAV file.")
    if float(np.sqrt(np.mean(prepared**2))) <= AUDIO_CONFIG["silence_rms"]:
        raise ValueError("No usable sound remains at 16000 Hz. Try another recording.")

    return {
        "status": "prepared",
        "audio": prepared,
        "sample_rate": target_rate,
        "duration_s": len(prepared) / target_rate,
        "dc_offset": dc_offset,
        "source_rms_after_dc": rms,
        "resampled": source_rate != target_rate,
    }


def bandpass_filter(samples, sample_rate, band_hz, order):
    """Apply an IIR Butterworth band-pass in SOS form, forward and backward."""
    samples = np.asarray(samples, dtype=np.float64)
    if samples.ndim != 1 or samples.size == 0 or not np.isfinite(samples).all():
        raise ValueError("Filtering needs a non-empty, finite mono signal.")
    low, high = band_hz
    if not 0 < low < high < sample_rate / 2 or order < 1:
        raise ValueError("Invalid filter settings: cutoffs must be below the Nyquist frequency.")
    sos = butter(order, band_hz, btype="bandpass", fs=sample_rate, output="sos")
    try:
        filtered = sosfiltfilt(sos, samples)
    except ValueError as error:
        raise ValueError("The signal is too short for forward-backward filtering.") from error
    if not np.isfinite(filtered).all():
        raise ValueError("Filtering produced invalid samples. Try a different recording.")
    return filtered


def rms_envelope(samples, sample_rate, window_s, hop_s):
    """Return frame RMS and center times for half-open audio frames."""
    samples = np.asarray(samples, dtype=np.float64)
    if samples.ndim != 1 or not np.isfinite(samples).all() or sample_rate <= 0:
        raise ValueError("Envelope extraction needs finite mono audio and a valid sample rate.")
    window = round(window_s * sample_rate)
    hop = round(hop_s * sample_rate)
    if window < 1 or hop < 1 or samples.size < window:
        raise ValueError("The audio is too short for the selected RMS window, or the window/hop is invalid.")
    starts = np.arange(0, samples.size - window + 1, hop)
    # Cumulative energy avoids copying every overlapping frame into a matrix.
    with np.errstate(over="ignore", invalid="ignore"):
        energy = np.concatenate(([0.0], np.cumsum(samples**2)))
        mean_square = (energy[starts + window] - energy[starts]) / window
    if not np.isfinite(mean_square).all():
        raise ValueError("The sample energy is too large for envelope extraction.")
    rms = np.sqrt(np.maximum(mean_square, 0.0))
    times = (starts + window / 2) / sample_rate
    return times, rms


def analyze_audio(prepared, prominence_fraction=None):
    """Filter the full clip, extract RMS, then detect central candidate cycles."""
    config = AUDIO_CONFIG.copy()
    if prominence_fraction is not None:
        if not np.isfinite(prominence_fraction) or not 0 < prominence_fraction <= 1:
            raise ValueError("The prominence fraction must be greater than zero and at most one.")
        config["peak_prominence_fraction"] = float(prominence_fraction)
    samples = prepared["audio"]
    sample_rate = prepared["sample_rate"]
    if sample_rate != config["sample_rate"]:
        raise ValueError("Prepare the recording at 16000 Hz before running analysis.")
    filtered = bandpass_filter(
        samples, sample_rate, config["audio_band_hz"], config["filter_design_order"]
    )
    times, rms = rms_envelope(
        filtered, sample_rate, config["rms_window_s"], config["rms_hop_s"]
    )
    envelope_rate = sample_rate / round(config["rms_hop_s"] * sample_rate)
    rhythm = bandpass_filter(
        rms, envelope_rate, config["envelope_band_hz"], config["filter_design_order"]
    )
    duration = len(samples) / sample_rate
    start = config["edge_margin_s"]
    end = duration - config["edge_margin_s"]
    mask = (times >= start) & (times < end)
    if start >= end or np.count_nonzero(mask) < 3:
        raise ValueError("Not enough audio remains after excluding the first and last five seconds.")
    central_rms = rms[mask]
    if float(np.sqrt(np.mean(filtered**2))) <= config["silence_rms"]:
        raise ValueError("No usable sound remains in the audio filter band. Try another recording.")
    warnings = []
    span = float(np.percentile(central_rms, 95) - np.percentile(central_rms, 5))
    flat_envelope = span <= max(
        float(np.median(central_rms)) * config["flat_envelope_fraction"], np.finfo(float).eps
    )
    if flat_envelope:
        warnings.append(
            "The RMS envelope has very little amplitude variation. "
            "Filtered edge effects can still appear; a repeating breathing pattern is not established."
        )
    analysis = {
        "status": "processed",
        "config": config,
        "sample_rate": sample_rate,
        "audio_time_s": np.arange(len(samples)) / sample_rate,
        "filtered_audio": filtered,
        "envelope_time_s": times,
        "rms": rms,
        "rhythm": rhythm,
        "envelope_sample_rate": envelope_rate,
        "analysis_start_s": start,
        "analysis_end_s": end,
        "analysis_mask": mask,
        "warnings": warnings,
        "flat_envelope": flat_envelope,
    }
    analysis.update(detect_cycles(analysis))
    if analysis["interval_cv"] is not None and analysis["interval_cv"] > config["interval_cv_warning"]:
        analysis["warnings"].append(
            "Candidate intervals vary substantially. Missed bursts, duplicate bursts, or irregular "
            "breathing may affect this provisional estimate."
        )
    return analysis


def detect_cycles(analysis):
    """Find candidate peaks and estimate BPM without identifying inhale/exhale phases."""
    config = analysis["config"]
    times = np.asarray(analysis["envelope_time_s"])
    rhythm = np.asarray(analysis["rhythm"])
    mask = np.asarray(analysis["analysis_mask"], dtype=bool)
    if (times.ndim != 1 or rhythm.shape != times.shape or mask.shape != times.shape
            or not np.isfinite(times).all() or not np.isfinite(rhythm).all()
            or np.any(np.diff(times) <= 0)):
        raise ValueError("Cycle detection needs aligned, finite envelope samples and increasing times.")

    minimum_spacing = 1 / config["envelope_band_hz"][1]
    result = {
        "peak_indices": np.empty(0, dtype=int),
        "peak_times_s": np.empty(0),
        "peak_prominences": np.empty(0),
        "intervals_s": np.empty(0),
        "candidate_count": 0,
        "peak_bpm": None,
        "interval_cv": None,
        "prominence_threshold": None,
        "min_peak_spacing_s": minimum_spacing,
        "rate_status": "unavailable",
        "rate_reason": "Insufficient envelope samples for cycle detection.",
    }
    central_indices = np.flatnonzero(mask)
    if central_indices.size < 3:
        return result
    central = rhythm[mask]
    span = float(np.percentile(central, 95) - np.percentile(central, 5))
    if analysis["flat_envelope"] or span <= np.finfo(float).eps:
        result["rate_reason"] = "Insufficient envelope variation to support a breathing-rate estimate."
        return result

    threshold = config["peak_prominence_fraction"] * span
    distance = int(np.ceil(minimum_spacing * analysis["envelope_sample_rate"]))
    peaks, properties = find_peaks(central, distance=distance, prominence=threshold)
    full_indices = central_indices[peaks]
    peak_times = times[full_indices]
    intervals = np.diff(peak_times)
    result.update({
        "peak_indices": full_indices,
        "peak_times_s": peak_times,
        "peak_prominences": properties["prominences"],
        "intervals_s": intervals,
        "candidate_count": len(peaks),
        "prominence_threshold": threshold,
    })
    if len(peaks) < config["min_cycle_markers"]:
        result["rate_reason"] = (
            f"Only {len(peaks)} candidate markers found; at least {config['min_cycle_markers']} "
            "are needed. Try a clearer or longer recording."
        )
        return result

    bpm = float(60 / np.median(intervals))
    result["interval_cv"] = float(np.std(intervals) / np.mean(intervals))
    low_bpm, high_bpm = (60 * frequency for frequency in config["envelope_band_hz"])
    if not low_bpm <= bpm <= high_bpm:
        result["rate_reason"] = (
            f"The candidate rate is outside the {low_bpm:g}–{high_bpm:g} BPM search range; "
            "no estimate is reported."
        )
        return result
    result.update({
        "peak_bpm": bpm,
        "rate_status": "provisional",
        "rate_reason": f"Based on {len(peaks)} candidate markers and {len(intervals)} intervals.",
    })
    return result
