# Progress and handoff

Use this file as the state record between chats. Update it after each implementation stage. Planned requirements elsewhere are not evidence of completed work.

## Current state

| Field | State |
| --- | --- |
| Last updated | 25 November 2026 |
| Active milestone | Midterm prototype |
| Active stage | M2 implemented and verified; ready for M3 |
| Documentation pack | Created |
| Application code | M1 input/preparation and M2 filtering/envelope/plots implemented |
| Real recordings | Not collected in this workspace |
| Manual labels | Not created |
| GUI verification | Input and all M2 plots checked in browser; physical microphone capture and audible playback pending |
| DSP verification | 21 tests pass, including filtering, RMS timing, and known-modulation checks; estimators not started |
| Experimental results | Engineering sanity checks only; real-recording evaluation pending |
| Next action | Send M3 for peak detection and candidate BPM |
| Final-project phase | Planned; do not start before midterm review |

## Stage tracker

| Stage | Scope | Status | Evidence |
| --- | --- | --- | --- |
| P0 | Read reference documents and inspect workspace | Complete | Context audit below; no implementation started |
| M1 | App shell and audio input | Implemented and verified; physical capture pending | 13 tests pass, HTTP checks pass, browser upload/preparation checked; docs/07_M1_VERIFICATION.md |
| M2 | Filters, envelope, plots | Implemented and verified | 21 tests pass; browser plot screenshots and engineering measurements in docs/08_M2_VERIFICATION.md |
| M3 | Peak estimate and markers | Not started | |
| M4 | Real-recording pilot | Not started | |
| M5 | Midterm checkpoint | Not started | |
| F1 | ACF and quality | Not started | |
| F2 | Labels, metrics, frozen protocol | Not started | |
| F3 | Method comparison and SNR study | Not started | |
| F4 | Optional synthetic mode | Not started | |
| F5 | Final audit and report | Not started | |

## Context audit on 24 November 2026

- Read README.md and docs/00_START_HERE.md through docs/06_PROGRESS_AND_HANDOFF.md.
- Inspected the workspace inventory: reference documents, header-only CSV templates, and the reference ZIP are present. No application code, requirements file, real recordings, or measured results are present.
- Checked for AGENTS.md in the project and its parent directories; none were found.
- Confirmed that the immediate milestone is the midterm prototype, with sequential stages M1 through M5. Final-project features remain deferred.
- M1 scope: create requirements and a simple Streamlit GUI for WAV upload, microphone recording, playback, metadata, and an Analyze action; add audio validation, mono conversion, DC removal, and resampling to 16000 Hz. Filtering, envelope extraction, and rate estimation start in later stages.
- No dependencies were installed, application code written, or runtime checks performed during P0.
- Next authorized step: wait for the user's M1 instruction, as specified by Prompt 0.

## Actual configuration

Shared AUDIO_CONFIG in dsp.py implements a 16000 Hz processing rate, minimum 8000 Hz source rate, 30 to 120 second duration, 50 MiB upload limit, and 0.000001 RMS silence guard. The reader accepts mono or stereo WAV-family files and retains the original decoded amplitudes. Channel averaging and DC removal precede polyphase FIR resampling.

M2 adds the 100–2000 Hz audio band-pass and 0.1–0.8 Hz envelope band-pass, both Butterworth design N=2 using SOS forward-backward filtering. Each band-pass is fourth order per pass with effective response order eight. RMS uses 250 ms windows and a 50 ms hop, center timestamps, and a 20 Hz envelope rate. The full clip is filtered before a mask selects frame centers in [5 seconds, duration minus 5 seconds). Spectrogram display uses 512-sample Hann windows with 256-sample overlap. Peak detection and estimators remain unimplemented; final evaluation settings are not frozen.

Tested environment: Windows, Python 3.12.10, Streamlit 1.67.0, NumPy 2.5.5, SciPy 1.18.1, Matplotlib 3.11.2, and SoundFile 0.14.0. A project-local .venv is installed; py launcher discovery failed, so Python 3.12 was invoked using its existing executable path during setup.

When code exists, record: audio band and N; filtering procedure; processing sample rate; RMS window/hop; envelope band and N; analysis margins; peak rules; ACF rules; quality thresholds; tested versions; configuration snapshot path; freeze date.

## M1 update on 24 November 2026

- Implemented: app.py, dsp.py, requirements.txt, .streamlit/config.toml, .gitignore, tests/test_audio.py, and tests/test_app.py. Updated README launch/use instructions and synchronized the input limits in the blueprint.
- Checks: Python syntax compilation passed; unittest discover ran 13 tests successfully; pip check found no broken requirements; local health endpoint and app root both returned HTTP 200.
- Browser evidence: a generated 30-second, 44100 Hz WAV uploaded, displayed correct metadata, loaded in the audio player with no media error, and prepared successfully at 16000 Hz mono. Switching to Record audio cleared the old result and showed the Record control.
- GUI screenshots: docs/screenshots/m1-upload-prepared.png and docs/screenshots/m1-recording-mode.png. The uploaded tone is an engineering fixture, not breathing data.
- Environment note: restricted-shell runtime checks stalled and the loopback request was denied. Those runs were interrupted. Dependency installation, successful tests, and local server checks ran with approved execution outside that restriction. No app logic was changed to bypass the restriction.
- Pending manual checks: actual browser microphone permission/capture, audible speaker playback, and real breathing clips. A staged WAV verified the recording-widget code path, not microphone hardware.
- Student contributions: none inferred or entered. Implementation assistance and automated checks do not establish either member's individual contribution.
- Next stage: M2 only. Filtering, plots, envelope extraction, peak BPM, ACF, quality scoring, and noise experiments remain unimplemented.

## M2 update on 25 November 2026

- Implemented: bandpass_filter, rms_envelope, and analyze_audio in dsp.py; waveform, spectrogram, and RMS/rhythm displays in app.py; shared M2 configuration; stale-analysis clearing; flat-envelope warnings.
- Tests: 21 unittest cases passed in 27.590 seconds after correcting the GUI test's image-element lookup. Syntax checks and pip check passed. The health endpoint returned HTTP 200 with body ok.
- Engineering checks: 0.2, 0.3, and 0.4 Hz amplitude modulation of a 700 Hz carrier survived the WAV pipeline. Correlations with the expected rhythm were 0.999939, 0.999945, and 0.999962. Test-only spectral checks found the same known frequencies. No rate estimator was added to the app.
- Timing: a 60-second case produces 1196 RMS frames, from 0.125 to 59.875 seconds; 1000 frame centers lie in the central 5–55 second interval. The full filtered audio and envelope remain available for display.
- Browser verification: uploaded the generated 60-second, 44100 Hz .cache/m2-am-engineering.wav; confirmed successful analysis, the 5–55 second interval, three plot figures, their axes/units, the 700 Hz spectrogram carrier, and aligned raw RMS/filtered rhythm. Saved screenshots under docs/screenshots/m2-*.png.
- Files: tests/test_processing.py adds eight engineering tests. README and blueprint reflect implemented behavior. Details and numerical results are in docs/08_M2_VERIFICATION.md.
- Pending: real breathing recordings, microphone hardware capture, audible playback, and pilot-based filter validation. No performance conclusions or individual student contributions were invented.
- Next authorized stage: M3 only. No peak detection, candidate count, BPM, ACF, final quality score, or noise experiment is implemented.

## Stage update template

Copy this section for each completed or attempted stage:
- Date and stage:
- Implemented files and behavior:
- Commands or checks actually run:
- Measured outputs and evidence paths:
- Manual checks completed:
- Pending checks or missing data:
- Design changes and reason:
- Actual member contributions:
- Next authorized stage:

Use Complete, Partial, Pending, or Failed with a reason. An implemented microphone widget is not the same as verified capture. A result table template is not an experiment.

## Midterm snapshot

To be filled during M5:
- Checkpoint status:
- Launch command and tested environment:
- Demo recording IDs:
- Actual filter and envelope settings:
- Pilot reference and output table:
- Screenshots:
- Known limitations:
- Unverified acceptance items:
- Presentation content:
- User instruction to continue to final project:

Do not remove this snapshot during session 2.

## Final evaluation snapshot

To be filled during F2 to F5:
- Development and evaluation recording IDs:
- Reference label protocol and matching tolerance:
- Frozen configuration path:
- Seeds and SNR levels:
- Per-trial results and summaries:
- MAE and coverage denominators:
- Exclusions and failed estimates:
- Reproduction command:
- Report and contribution records:

## Open matters

- Confirm the actual final submission date. The old pasted deadline and the working midterm date differ.
- Collect real audio and manual labels.
- Verify microphone capture on the intended demo machine.
- Inspect whether inhale/exhale bursts cause duplicate cycle detections.
- Validate starting filter and peak settings on development recordings.
