# M3 verification

M3 adds candidate cycle detection and a provisional peak-interval BPM estimate. Checks were completed on 27 November 2026 using generated engineering signals. Real breathing recordings have not yet been tested.

## Implemented method

1. Use the filtered envelope frame centers in the central interval, excluding five seconds at each end.
2. Reject nearly constant RMS envelopes using the existing 1% percentile-span-to-median guard. Also guard a negligible filtered-envelope percentile span.
3. Set minimum peak prominence to 0.15 times the central filtered envelope's 95th-to-5th percentile span.
4. Call SciPy find_peaks with at least 1.25 seconds between markers: 25 samples at the 20 Hz envelope rate.
5. Retain candidate indices, original-clip times, prominences, and consecutive intervals.
6. With at least three markers, calculate BPM = 60 / median(intervals in seconds).
7. Report unavailable if there are too few markers or the candidate rate lies outside 6–48 BPM. No output is clamped and no result is automatically halved.

All available estimates are labeled provisional. A candidate marker can correspond to a sound burst rather than a complete inhale-exhale cycle. Interval coefficient of variation above 0.2 triggers a variability warning, not a confidence score.

The Detection settings slider permits prominence fractions 0.05 to 0.80 in steps of 0.05. Changing it clears the old analysis and requires a new Analyze action. The actual fraction and amplitude threshold appear in Cycle detection details and are stored with the result. Default values in AUDIO_CONFIG remain unchanged by a per-run override.

## Verification commands and results

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m py_compile app.py dsp.py tests/test_estimation.py tests/test_app.py
.\.venv\Scripts\python.exe -m pip check
```

**31 tests passed in 15.754 seconds.** Syntax checks passed and pip check found no broken requirements. The local health endpoint returned HTTP 200 with body ok, and the app root returned HTTP 200.

The nine new estimator tests cover known rates through the WAV pipeline, median-interval arithmetic with a long gap, too few markers, an out-of-range interval estimate, silence/constant-carrier inputs, minimum spacing, a double-burst stress case, configuration overrides, and invalid envelopes. A new GUI test checks that changing prominence clears a previous rate. Existing GUI checks verify valid and unavailable displays, input replacement, recording mode, and plot rendering.

## Single modulation engineering results

Each 60-second signal uses a positive amplitude envelope on an audible 700 Hz carrier. The full WAV pipeline is run with default settings. These are known-rate implementation checks, not real-recording performance results.

| Known cycle rate in BPM | Estimated peak BPM | Absolute error in BPM | Candidate markers | Median interval in seconds |
| --- | --- | --- | --- | --- |
| 12 | 12.000000 | 0.000000 | 10 | 5.000 |
| 18 | 17.910448 | 0.089552 | 15 | 3.350 |
| 24 | 24.000000 | 0.000000 | 20 | 2.500 |

All meet the planned error threshold of at most 2 BPM on these constructed cases. The 20 Hz envelope grid contributes timing quantization; for example, 18 BPM has a period of about 3.333 seconds, while the measured median candidate interval is 3.350 seconds.

Markers are restricted to the central mask and retain their original recording timestamps. Their plotted RMS locations are projections of the filtered-envelope detection times, not a separate RMS-peak detector.

## Unavailable and stress cases

| Case | Observed behavior |
| --- | --- |
| Constant 500 Hz carrier | No supported amplitude rhythm; zero candidate markers and unavailable BPM |
| Silence | Rejected during preparation with a readable no-usable-sound message |
| Two known candidate markers | Count retained as two; BPM unavailable because three are required |
| Three markers 20 seconds apart | Candidate rate outside the search range; no BPM reported or clamping |
| Two bursts per five-second full pattern | 20 markers over the central interval and 24 BPM, despite a 12 BPM full-pattern rate |

The double-burst case is a known failure of full-cycle interpretation. Its amplitude envelope contains both 0.2 Hz and stronger 0.4 Hz components. Regular intervals alone cannot identify the intended full breath. The result stays provisional, and the GUI warns that inhalation/exhalation bursts may be counted separately. A manual full-cycle reference is required to assess this on real recordings; no ground-truth-driven correction was inserted.

## Browser verification

Uploaded .cache/m3-known-18bpm-engineering.wav through the actual browser chooser and ran Analyze audio. Confirmed:

- Original 60-second, 16000 Hz, mono metadata and playback controls.
- Peak BPM displayed as 17.9 with a provisional label and warning.
- Fifteen candidate markers and a 50.0-second analyzed duration.
- Central interval shown as 5.00–55.00 seconds.
- Candidate markers aligned on the signed filtered envelope and projected onto raw RMS.
- Marker count and interval-based explanation separated from verified full-cycle counts.

Screenshots:

- [Provisional rate summary](screenshots/m3-rate-summary.png).
- [Candidate cycle markers](screenshots/m3-cycle-markers.png).

The generated fixture is not a real breathing recording. Actual microphone capture and audible speaker playback remain manual checks.

## Next stage

M4 needs 2–3 real breathing WAV clips with manual full-cycle counts or consistent event timestamps. Inspect duplicate and missed markers before accepting the baseline for the midterm. Record actual reference intervals, rate errors, settings, and failure observations. No real audio was found in the workspace outside the generated cache fixtures during M3.

No ACF method, final quality score, noise sweep, or final-project result is implemented in this stage. M4 and M5 still precede the midterm checkpoint. The QA server is stopped after verification; use the README launch command to run the app.
