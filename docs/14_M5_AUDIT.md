# M5 audit and milestone record

**Date:** 27 November 2026. **Working presentation target:** 28 November 2026.

**M5 preparation: COMPLETE within the revised scope. Overall midterm validation checkpoint: PARTIAL.** The user explicitly authorized completing M5 now and provisioning real recordings later. The prototype, presentation content, demo inputs, and continuation instructions are prepared; outstanding acceptance evidence is retained below. This does not mark the deferred M4 pilot complete or certify real breathing performance.

## Acceptance audit

| Original midterm acceptance item | Status | Evidence / remaining work |
| --- | --- | --- |
| Dependencies and documented launch command | COMPLETE in existing environment | M5 pip check: no broken requirements; local server starts, health and root return HTTP 200. New-machine installation not repeated. |
| WAV upload and metadata | COMPLETE for engineering WAVs | Existing M3 browser capture; M5 upload GUI regression and generated demo files |
| Microphone control and physical capture | PARTIAL | Control and staged-byte path pass GUI tests; actual permission/capture needs demo-device check |
| Uploaded and recorded audio playback | PARTIAL | Audio player and staged recording path verified; actual speaker listening and real captured playback pending |
| Mono, DC removal, resampling, filtering | COMPLETE in code and engineering checks | Audio and processing tests; exact defaults saved in snapshot |
| Readable waveform/spectrogram with units | COMPLETE | M2 browser screenshots, M5 three-figure GUI checks; original code unchanged |
| RMS and filtered envelope alignment | COMPLETE | Frame-center tests, M2/M3 browser screenshots |
| Candidate markers and analyzed interval | COMPLETE | M3 browser screenshots; estimator and GUI tests |
| Peak interval BPM | COMPLETE on engineering inputs | 12, 18, 24 BPM checks; provisional output and median arithmetic tests |
| Silence, short/corrupt input, insufficient markers | COMPLETE for tested cases | Audio, GUI, and estimator failure tests return errors/unavailable appropriately |
| At least two real clips with references/outputs | PENDING — deferred | No recordings or labels available; data/pilot folder, guide, and worksheet prepared |
| Real inhale/exhale double-counting inspection | PENDING — deferred | Generated stress case exposes the risk; no real-event review yet |
| Actual settings, limitations, tuning record | COMPLETE for current baseline | Snapshot, blueprint, M3 verification; no pilot tuning performed |
| Actual individual contribution log | PENDING | Header-only contributions.csv; no ownership inferred or fabricated |
| Accurate presentation separating current/future work | COMPLETE as Markdown content | docs/12_MIDTERM_PRESENTATION.md, six slides with honest engineering results and pending items |

Save original WAV is additional collection support: its AppTest control retains the analysis result. The actual browser download and re-upload remain a device check in the runbook.

## M5 checks performed

- Full existing suite: **31 tests passed in 16.231 seconds** on 27 November 2026. Six are GUI tests; no new tests were needed for presentation documents.
- Python compilation: app.py and dsp.py passed; pip check reported no broken requirements.
- Documented app launch using the existing virtual environment succeeded at 127.0.0.1:8501. Health endpoint and home page both returned HTTP 200. The audit server was stopped afterward.
- Regenerated six engineering WAVs, then processed their saved bytes through the same DSP pipeline. Results: 12→12.00, 18→17.910448, 24→24.00; double-burst full pattern 12→24.00; constant carrier unavailable; silence rejected.
- Reused actual browser screenshots from M2/M3. No new browser capture, physical microphone test, speaker listening, or manual breathing annotation was performed during M5.
- Runtime tests required the same approved execution outside the restricted runtime used in earlier stages; a stalled restricted test run was interrupted before the successful run. No app logic was changed for the environment.

## Confirmation after M4 scope closure, 27 November 2026

The user requested M5 after agreeing to defer recordings. The existing implementation and presentation materials were inspected and reverified; no additional application features or DSP changes were needed.

- **31 tests passed in 15.850 seconds**, including all six GUI tests. Dependency checks and compilation of the app, DSP module, and demo-preparation script passed.
- All six regenerated engineering results and configuration values match the original milestone snapshot. A SHA-256 comparison confirmed that the saved snapshot was unchanged.
- The app launched in the existing environment; health returned HTTP 200 with body ok and the home page returned HTTP 200. The owned server was stopped afterward.
- The saved M3 rate-summary and cycle-marker screenshots were visually reviewed for readability; their original capture dates and generated-input provenance remain unchanged. No fresh browser capture or hardware test was performed.
- All 65 local links in 19 Markdown documents resolve. The presentation, runbook, pilot worksheet, and continuation instructions are ready for use.

**M5 software/demo preparation is complete under the agreed scope.** The acceptance table above still records outstanding real-data, device, and contribution evidence. Supplying recordings later resumes the pilot; it does not require repeating M1–M5 software preparation.

## Preserved milestone artifacts

- [Presentation content](12_MIDTERM_PRESENTATION.md): six slides with speaker notes and actual screenshots.
- [Demo runbook](13_MIDTERM_DEMO.md): launch, generated-input sequence, fallback, device checklist, deferred-data procedure and resume prompt.
- [Configuration and measured engineering snapshot](midterm-engineering-snapshot.json): actual AUDIO_CONFIG and all six case results, labeled synthetic_engineering. This is a midterm record, not final-evaluation freezing.
- [Engineering input folder](../data/midterm_engineering/README.md): WAVs prepared locally, ignored by Git; regenerate with tools/prepare_midterm_demo.py. Current rerun measurements go to latest-run.json; original snapshot is preserved.
- Screenshots: [rate summary](screenshots/m3-rate-summary.png), [cycle markers](screenshots/m3-cycle-markers.png), [waveforms](screenshots/m2-waveforms.png), [spectrogram](screenshots/m2-spectrogram.png). Original M2/M3 input provenance is documented in those stages' verification records.
- [Deferred pilot guide](10_M4_PILOT_GUIDE.md), [worksheet](11_M4_PILOT_WORKSHEET.md), and [contribution log](templates/contributions.csv).

## Configuration and environment

16000 Hz processing; audio 100–2000 Hz; RMS 250 ms / 50 ms; 20 Hz envelope; envelope 0.1–0.8 Hz; Butterworth N=2 SOS forward-backward for both bands; first/last five-second exclusion; peak spacing 1.25 s, prominence fraction 0.15, at least three markers; BPM from median intervals. See the full snapshot for input limits and guards.

Tested environment remains Windows, Python 3.12.10, Streamlit 1.67.0, NumPy 2.5.5, SciPy 1.18.1, Matplotlib 3.11.2, SoundFile 0.14.0. These are installed tested versions, not a newly pinned lockfile.

## Limitations and continuation

No real breathing rate accuracy, event precision/recall/F1, ACF comparison, confidence/quality score, or SNR robustness result exists. Regular candidate intervals do not prove full-cycle detection; the stress case doubles the intended full-pattern rate. Acoustic cutoffs, margins, and prominence remain starting choices. No automatic halving or reference-driven correction is used.

M5 preparation stops here. Resume deferred M4 when recordings are available, then update this audit and the presentation with actual evidence. Individual contributions and demo-device checks can also be added later, before claiming completion of those items. Final-project implementation F1–F5 requires a separate explicit user instruction. The original M5 snapshot must remain available after later changes.
