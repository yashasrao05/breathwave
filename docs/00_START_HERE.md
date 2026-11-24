# Start here

The immediate goal is a usable midterm prototype for a two-member student DSP project. Build the smallest clear implementation that can load real breathing audio, show the processing stages, mark candidate breathing cycles, and estimate breaths per minute.

## Project brief

**Title:** GUI App for Contactless Respiration-Rate Estimation from Audio Using Digital Signal Processing.

**Platform:** Python Streamlit app running in a browser on a local computer.

**User:** someone who can click buttons, record or upload audio, and inspect results without editing source code. A documented command may launch the app; normal use happens through the GUI.

**Execution level:** a tidy course project with ordinary Python functions, clear plots, and measured results. Keep dependencies and abstraction modest. Both members must be able to explain their work and the complete pipeline.

## Instructor requirements

- Explain the filter type, order, cutoffs, and reasons for the choices.
- Distinguish the audible audio band from the slow breathing rhythm in the envelope.
- Compare peak detection and autocorrelation quantitatively in the final results.
- Include a numerical noise robustness study with an error table or curve versus SNR.
- Document each member's individual contribution.
- Retain the educational scope.

## Milestones

| Midterm prototype | Final project |
| --- | --- |
| WAV upload, microphone recording, playback | Independent autocorrelation estimate and plot |
| Mono conversion, DC removal, audio filtering | Heuristic signal-quality indicator |
| Waveform, spectrogram, RMS envelope | Controlled added noise on real recordings |
| Envelope filtering, cycle markers, peak BPM | Quantitative comparison and SNR curves |
| Basic invalid-input messages | Optional synthetic-audio demonstration |
| Two or three manually checked real clips | Six-recording pilot, CSV exports, report, viva material |

The labels describe milestones, not marks or a percentage of implementation effort.

## Two implementation sessions

**Session 1:** run M1 through M5 and reach the midterm checkpoint. Reserve time around that session to record clips, inspect annotations, and rehearse. The five calendar days before the working midterm date do not require five build sessions.

**Session 2:** after the midterm is reviewed, run F1 through F5. Add the second method, complete the experiments, and prepare the final handoff. Do not rewrite the working prototype for visual polish.

No estimated number of hours guarantees reliable behavior on real audio. If recording quality or double counting blocks the prototype, spend the available time inspecting that issue before adding features.

## Reading order

1. This file.
2. Project blueprint.
3. Implementation prompts.
4. Midterm checkpoint.
5. Progress and handoff.

Read the final evaluation plan and report guide before starting session 2.

## Operating the prompts

Send Prompt 0 once at the beginning of an implementation chat. Then send only the next stage prompt. Each stage should implement its own scope, run appropriate checks, update the progress file, and return a concise explanation.

The prompts require stopping between stages because the user wants sequential implementation. At M5, stop development at the midterm checkpoint. Continuing to F1 requires the user's explicit instruction to start the final-project phase.

If a stage fails, use the repair prompt. If the chat loses context or a new chat takes over, use the resume prompt. Never treat these planned documents as evidence of existing code.

## Practical boundaries

Use a small set of files: app.py, dsp.py, and later evaluation.py, plus requirements, documentation, data, and results. Add a separate audio helper only if it makes the code clearer. A few meaningful DSP tests are appropriate; a large test framework is unnecessary.

Avoid accounts, databases, live streaming, medical interpretation, machine learning, elaborate classes, and a third required estimator. Normal input and analysis should work without changing source code.
