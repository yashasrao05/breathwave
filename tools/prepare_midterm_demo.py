"""Prepare repeatable engineering WAVs for the midterm, not breathing data."""

import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dsp import AUDIO_CONFIG, analyze_audio, prepare_audio, read_wav


def main():
    output = ROOT / "data" / "midterm_engineering"
    output.mkdir(parents=True, exist_ok=True)
    time = np.arange(60 * 16000) / 16000
    carrier = np.sin(2 * np.pi * 700 * time)
    cases = []
    for bpm in (12, 18, 24):
        samples = 0.15 * (1 + 0.65 * np.sin(2 * np.pi * bpm / 60 * time)) * carrier
        cases.append((f"engineering-{bpm}bpm.wav", samples, bpm))
    double_envelope = 1 + 0.65 * np.sin(2 * np.pi * 0.4 * time) + 0.1 * np.sin(2 * np.pi * 0.2 * time)
    cases.extend([
        ("engineering-double-burst-12bpm.wav", 0.15 * double_envelope * carrier, 12),
        ("engineering-constant-carrier.wav", 0.15 * carrier, None),
        ("engineering-silence.wav", np.zeros_like(time), None),
    ])
    rows = []
    for name, samples, known_bpm in cases:
        path = output / name
        # FLOAT WAV avoids quantization differences from the original engineering checks.
        sf.write(path, samples, 16000, subtype="FLOAT")
        row = {"file": path.relative_to(ROOT).as_posix(), "source_type": "synthetic_engineering",
               "known_full_pattern_bpm": known_bpm}
        try:
            result = analyze_audio(prepare_audio(read_wav(path.read_bytes())))
            bpm = result["peak_bpm"]
            row.update(status=result["rate_status"], estimated_bpm=bpm,
                       candidate_count=result["candidate_count"],
                       absolute_error_bpm=abs(bpm - known_bpm) if bpm is not None and known_bpm is not None else None,
                       reason=result["rate_reason"])
        except ValueError as error:
            row.update(status="input_rejected", estimated_bpm=None, reason=str(error))
        rows.append(row)
    snapshot = {"milestone": "M5 midterm prototype", "source_type": "synthetic_engineering",
                "note": "Not real breathing validation. Not the frozen final-evaluation configuration.",
                "config": AUDIO_CONFIG, "cases": rows}
    report = json.dumps(snapshot, indent=2) + "\n"
    (output / "latest-run.json").write_text(report, encoding="utf-8")
    destination = ROOT / "docs" / "midterm-engineering-snapshot.json"
    # Keep the original milestone evidence if DSP changes in later project stages.
    if not destination.exists():
        destination.write_text(report, encoding="utf-8")
    print(f"Prepared {len(rows)} engineering WAVs in {output}")
    for row in rows:
        print(f"{Path(row['file']).name}: {row['status']}, BPM={row['estimated_bpm']}")
    print(f"Original milestone snapshot (preserved): {destination}")
    print(f"Current measured results: {output / 'latest-run.json'}")


if __name__ == "__main__":
    main()
