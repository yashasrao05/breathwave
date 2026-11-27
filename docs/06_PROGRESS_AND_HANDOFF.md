# Progress and handoff

Use this file as the state record between chats. Update it after each implementation stage. Planned requirements elsewhere are not evidence of completed work.

## Current state

| Field | State |
| --- | --- |
| Last updated | 27 November 2026 |
| Active milestone | Midterm prototype |
| Active stage | M5 software/demo preparation complete and reverified after M4 scope closure; stopped at midterm; real-recording pilot deferred |
| Documentation pack | Created |
| Application code | M1–M3 pipeline implemented; M4 Save original WAV control added |
| Real recordings | None available; user confirmed on 27 November 2026 |
| Manual labels | None available; pilot guide and empty worksheet prepared |
| GUI verification | M2/M3 browser evidence retained; M5 full suite includes six passing GUI checks; physical capture, audible playback, and browser file save pending |
| DSP verification | Latest M5 audit: 31 tests pass in 15.850 s; all six generated demo results/settings match the preserved snapshot; real-recording validation pending |
| Experimental results | Engineering sanity checks only; real-recording evaluation pending |
| Next action | Use M5 presentation/demo materials; later resume deferred M4 with real clips and references, update acceptance evidence; await explicit F1 instruction |
| Final-project phase | Planned; do not start before midterm review |

## Stage tracker

| Stage | Scope | Status | Evidence |
| --- | --- | --- | --- |
| P0 | Read reference documents and inspect workspace | Complete | Context audit below; no implementation started |
| M1 | App shell and audio input | Implemented and verified; physical capture pending | 13 tests pass, HTTP checks pass, browser upload/preparation checked; docs/07_M1_VERIFICATION.md |
| M2 | Filters, envelope, plots | Implemented and verified | 21 tests pass; browser plot screenshots and engineering measurements in docs/08_M2_VERIFICATION.md |
| M3 | Peak estimate and markers | Implemented and verified on engineering inputs | 31 tests pass; known-rate and stress results plus browser screenshots in docs/09_M3_VERIFICATION.md |
| M4 | Pilot support and real-recording checks | Software/preparation complete under revised scope; real-data validation deferred | User authorized recordings later; save control, guide, and worksheet ready; no real pilot results |
| M5 | Midterm checkpoint | Software/demo preparation complete and reverified; overall validation checkpoint partial | Six-slide content, demo runbook, acceptance audit, preserved snapshot; latest 31-test and launch checks pass |
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

M2 adds the 100–2000 Hz audio band-pass and 0.1–0.8 Hz envelope band-pass, both Butterworth design N=2 using SOS forward-backward filtering. Each band-pass is fourth order per pass with effective response order eight. RMS uses 250 ms windows and a 50 ms hop, center timestamps, and a 20 Hz envelope rate. The full clip is filtered before a mask selects frame centers in [5 seconds, duration minus 5 seconds). Spectrogram display uses 512-sample Hann windows with 256-sample overlap.

M3 adds find_peaks on the central filtered envelope with a default prominence fraction of 0.15 and minimum spacing of 1.25 seconds (25 samples). At least three markers are required; BPM is 60/median(intervals). Flat RMS, negligible rhythm variation, too few markers, or an out-of-range result produce unavailable BPM. Available results are provisional. The flat-envelope fraction is 0.01; interval CV above 0.2 adds a warning. Per-run configuration, marker times/prominences, intervals, and interval variability are retained. ACF, final quality scoring, and the SNR experiment remain unimplemented. Final evaluation settings are not frozen.

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

## M3 update on 27 November 2026

- Implemented: detect_cycles in dsp.py, provisional/unavailable BPM fields, candidate marker times and properties, intervals and variability, GUI rate/count/duration summary, prominence tuning with stale-result clearing, and marker overlays on the RMS/rhythm plots.
- Checks: 31 tests passed in 15.754 seconds; syntax compilation and pip check passed. Local health and root endpoints both returned HTTP 200.
- Known-rate engineering results: 12 BPM returned 12.00 with 10 markers; 18 BPM returned 17.910448 with 15 markers; 24 BPM returned 24.00 with 20 markers. Absolute errors were 0, 0.089552, and 0 BPM, within the planned 2 BPM sanity threshold.
- Failure cases: constant-carrier audio returned unavailable with zero candidates; silence was rejected with a readable input message. Two markers and out-of-range interval cases return no BPM. A two-burst stress pattern with a 12 BPM full-pattern rate returned 24 BPM, confirming an unresolved harmonic/double-counting limitation. No automatic halving was applied.
- Browser check: uploaded .cache/m3-known-18bpm-engineering.wav, a generated 60-second PCM WAV. Verified 17.9 provisional BPM, 15 candidates, a 50-second analyzed interval, warnings, and aligned marker overlays. Screenshots: docs/screenshots/m3-rate-summary.png and docs/screenshots/m3-cycle-markers.png.
- Documentation: README, blueprint, and docs/09_M3_VERIFICATION.md describe current settings, checks, and limitations. No real breathing clips were found outside the ignored engineering cache; real-data validation remains pending.
- Next stage: M4 only. Obtain 2–3 real recordings and manual full-cycle references, inspect duplicate/missed events, and make evidence-based pilot fixes. The midterm checkpoint is not complete yet; M4 and M5 remain.

## M4 update on 27 November 2026

- Data audit: no real WAV/FLAC/MP3/M4A clips or populated manual-reference files were found in the project. The user confirmed that no recordings or manual counts/timestamps are available elsewhere. Generated .cache fixtures remain engineering inputs, not pilot data.
- Implemented collection support: app.py now offers Save original WAV for both uploaded and recorded inputs, using the original audio bytes and a downloadable WAV filename. Files are not automatically written into the project; save and rename each take into data/pilot.
- Prepared: data/pilot/README.md, docs/10_M4_PILOT_GUIDE.md, and docs/11_M4_PILOT_WORKSHEET.md. They define collection, common analysis intervals, manual timestamp/count references, rate error, duplicate/missed-cycle review, documented tuning, and demo selection. Worksheet records are empty.
- Verification: six GUI tests passed in 15.323 seconds, including saving after analysis without losing its rate. Python syntax compilation passed. Actual browser download completion, physical capture, and audible playback remain manual checks. The DSP code was unchanged; the 31-case M3 baseline remains the latest full-suite result.
- Pilot outcome: no real-recording estimates, manual reference rates, errors, inspected cycles, accepted tuning decisions, reliable demo clip, or difficult real example can be reported yet. Existing filter and detection defaults remain unchanged; no individual student contributions were invented.
- Status: M4 partial. Real-data completion requires at least two real clips with manual references and documented app results/observations. The midterm checkpoint remains incomplete.
- Next action: collect 2–3 recordings using Save original WAV and fill the pilot worksheet, then resume M4. No M5 presentation or final-project features were added.

## M5 update on 27 November 2026

- Scope revision: the user explicitly requested completing M5 now and provisioning real recordings later. M5 packaging is complete; M4 real-recording work remains deferred and the overall midterm validation checkpoint remains partial. Missing data was not treated as permission to invent results.
- Prepared: six-slide Markdown presentation with speaker notes and actual M2/M3 screenshots; demo runbook with generated-input sequence, fallback, device checks, and deferred-M4 resume prompt; item-by-item acceptance audit; tools/prepare_midterm_demo.py; six generated WAVs in data/midterm_engineering; docs/midterm-engineering-snapshot.json with actual settings/results. WAVs are ignored by Git and can be regenerated. The script preserves the original snapshot on reruns and writes current results into latest-run.json.
- Checks: all 31 existing tests passed in 16.231 seconds; app.py/dsp.py compilation and pip check passed. The local launch succeeded; health and home page returned HTTP 200. The audit server was stopped. A restricted test attempt stalled and was interrupted; the successful run used the approved execution context from earlier stages.
- Generated-file outputs: 12, 18, 24 BPM returned 12.00, 17.910448, 24.00; the 12 BPM full-pattern double-burst stress returned 24.00; constant carrier unavailable; silence rejected. These are engineering checks only. No real results, manual labels, noise experiments, or ACF comparisons were created.
- Baseline DSP and GUI code unchanged in M5. No new browser capture was performed; existing screenshots retain their M2/M3 provenance. Microphone hardware capture, audible playback, browser download completion, real-data pilot, and actual individual contributions remain pending.
- Next action: present/rehearse the documented prototype; use the deferred-M4 resume prompt when recordings become available. Stop at the midterm. Do not start F1 until explicitly instructed.

## M4 scope closure on 27 November 2026

- User instruction: complete the work possible now and supply recordings later. M4 software/preparation is complete under this revised scope; this supersedes the earlier partial stage label, without completing its real-data acceptance items.
- Ready now: original-WAV saving, recording/labeling instructions, an empty pilot worksheet, the pilot folder, engineering verification, and the deferred-validation resume prompt in docs/13_MIDTERM_DEMO.md. M5 presentation/demo packaging already exists.
- Deferred: provide 2–3 real WAVs with manual full-cycle references, compare the current baseline over the same interval, inspect duplicate/missed cycles, and document actual results and any supported fixes. Update the worksheet, presentation, and acceptance audit when that evidence exists.
- No source code or DSP defaults changed during this scope update; no tests were rerun for documentation-only changes. The existing verification records retain their dates and limits. The overall validation checkpoint remains partial, and final-project implementation remains unstarted.

## M5 confirmation after M4 scope closure on 27 November 2026

- User instruction: implement M5 now, retaining the agreed deferral of real recordings. Inspected the existing M5 materials and acceptance checklist; the six-slide content, demo runbook, screenshots, baseline snapshot, and continuation prompt are already present and consistent with implemented features.
- Full suite: 31 tests passed in 15.850 seconds, including six GUI tests. Dependency checks found no broken requirements; compilation of app.py, dsp.py, and tools/prepare_midterm_demo.py passed.
- Regenerated the six explicitly labeled engineering WAVs and compared latest-run.json against the original milestone snapshot: all settings and results match. The original snapshot's SHA-256 remained unchanged. Clean 12/18/24 BPM inputs return 12.00/17.910448/24.00; the double-burst failure remains 12-to-24 BPM, constant carrier unavailable, silence rejected.
- Launch verification: the documented project environment started Streamlit at 127.0.0.1:8501; health returned HTTP 200 with body ok and the home page returned HTTP 200. The owned server was stopped after checking. A status-check command needed a variable-name correction; the app did not require a fix.
- Visually reviewed the saved M3 rate-summary and cycle-marker screenshots. They remain readable and retain their original generated-input provenance; no new browser or physical-device verification is claimed. All 65 local links across 19 Markdown files resolve.
- Scope outcome: M5 software/demo preparation is complete. Source code and DSP settings did not need changes. Real-data pilot results, physical microphone capture, audible playback, browser download completion, and individual contribution entries remain deferred or manual. The overall validation checkpoint stays partial. Rehearse using docs/13_MIDTERM_DEMO.md; resume its deferred-M4 prompt when recordings arrive. Stop here before F1.

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

- Checkpoint status: M5 preparation COMPLETE under revised scope; overall validation checkpoint PARTIAL; see docs/14_M5_AUDIT.md for all acceptance statuses.
- Launch command: `.\.venv\Scripts\python.exe -m streamlit run app.py` from the project root. Existing Windows Python 3.12.10 environment and library versions above verified; health/root HTTP 200.
- Demo inputs: generated 12/18/24 BPM, double-burst, constant-carrier, and silence WAVs in data/midterm_engineering. No real demo recording selected. Regenerate using tools/prepare_midterm_demo.py.
- Actual filter/envelope/detection settings: docs/midterm-engineering-snapshot.json; no M5 change or final-evaluation freeze.
- Pilot reference/output table: pending; empty worksheet remains docs/11_M4_PILOT_WORKSHEET.md. Generated-signal results are separately labeled in the snapshot and presentation.
- Screenshots: docs/screenshots/m3-rate-summary.png, m3-cycle-markers.png, m2-waveforms.png, m2-spectrogram.png; actual M2/M3 browser runs on generated inputs.
- Known limitations: possible inhale/exhale double counting, unresolved harmonic stress failure, initial filter/margin choices, no real-data accuracy established, no ACF/quality/SNR evaluation yet.
- Unverified acceptance items: physical microphone capture, audible playback, actual downloaded-file round trip, real references/outputs and cycle inspection, individual contribution log.
- Presentation content: docs/12_MIDTERM_PRESENTATION.md. Demo and later-recording procedure: docs/13_MIDTERM_DEMO.md.
- User instruction to continue to final project: none; remain stopped at midterm.

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
