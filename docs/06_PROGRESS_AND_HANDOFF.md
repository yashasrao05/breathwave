# Progress and handoff

Use this file as the state record between chats. Update it after each implementation stage. Planned requirements elsewhere are not evidence of completed work.

## Current state

| Field | State |
| --- | --- |
| Last updated | 24 November 2026 |
| Active milestone | Midterm prototype |
| Active stage | M1 implemented and verified; ready for M2 |
| Documentation pack | Created |
| Application code | M1 app.py, dsp.py, requirements.txt, and tests implemented |
| Real recordings | Not collected in this workspace |
| Manual labels | Not created |
| GUI verification | Upload/preparation and recording-mode UI checked in browser; physical microphone capture and audible playback pending |
| DSP verification | M1 decoding/preparation checks pass; filtering and estimation not started |
| Experimental results | Not produced |
| Next action | Send M2 for filters, RMS envelope, and plots |
| Final-project phase | Planned; do not start before midterm review |

## Stage tracker

| Stage | Scope | Status | Evidence |
| --- | --- | --- | --- |
| P0 | Read reference documents and inspect workspace | Complete | Context audit below; no implementation started |
| M1 | App shell and audio input | Implemented and verified; physical capture pending | 13 tests pass, HTTP checks pass, browser upload/preparation checked; docs/07_M1_VERIFICATION.md |
| M2 | Filters, envelope, plots | Not started | |
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

M1 AUDIO_CONFIG in dsp.py implements a 16000 Hz processing rate, minimum 8000 Hz source rate, 30 to 120 second duration, 50 MiB upload limit, and 0.000001 RMS silence guard. The reader accepts mono or stereo WAV-family files and retains the original decoded amplitudes. Channel averaging and DC removal precede polyphase FIR resampling. No analysis band-pass, RMS envelope, or estimator is implemented yet. Final evaluation settings are not frozen.

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
