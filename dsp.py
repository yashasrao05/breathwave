"""Audio input and preparation helpers, independent of the Streamlit GUI."""

from io import BytesIO
from math import gcd

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly


AUDIO_CONFIG = {
    "sample_rate": 16000,
    "min_source_sample_rate": 8000,
    "min_duration_s": 30,
    "max_duration_s": 120,
    "max_upload_bytes": 50 * 1024 * 1024,
    "silence_rms": 1e-6,
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
