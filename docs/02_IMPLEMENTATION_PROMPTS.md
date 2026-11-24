# Implementation prompts

Copy Prompt 0 into a new implementation chat. Then send M1 through M5 one at a time. F1 through F5 are reserved for continuing after the midterm checkpoint. The code fences contain prompts, not application code.

If the new chat cannot read this project folder, attach the reference documents first. The prompts alone do not contain every technical detail.

## Prompt 0 Establish the working context

~~~text
We are implementing a two-member student DSP project: "GUI App for Contactless Respiration-Rate Estimation from Audio Using Digital Signal Processing."

Read README.md and docs/00_START_HERE.md through docs/06_PROGRESS_AND_HANDOFF.md, especially the technical blueprint. Inspect the actual project files and any applicable repository instructions. Do not assume the planned app or results exist. An earlier chat mentioned files under another user's C: directory; those are not evidence of this workspace's implementation.

Our immediate goal is the MIDTERM PROTOTYPE. We will implement sequentially using M1 through M5. Do not build final-stage features before I start F1. Stop after each numbered stage, update docs/06_PROGRESS_AND_HANDOFF.md, and tell me the next prompt.

Use Python Streamlit, NumPy, SciPy, Matplotlib, and SoundFile. Keep the solution at a solid student-project level with ordinary readable functions, limited dependencies, and DSP decisions both members can explain. Follow the blueprint's starting defaults, and record any evidence-based change consistently in code and docs.

Never invent recordings, annotations, measured accuracy, experiment results, or team contributions. Do not call synthetic checks real-data validation. Distinguish implemented, verified, manually pending, and planned. Preserve existing work and inspect before editing.

For each stage: implement its scope, perform appropriate checks, explain the important DSP decisions, record files and checks, and stop. If a missing real recording blocks validation, finish the independent code, identify exactly what data is needed, and leave that validation pending.

For now, return a brief status and your understanding of M1. Do not start implementation until I send M1.
~~~

## M1 Create the app shell and audio input

~~~text
Implement stage M1 only, following docs/01_PROJECT_BLUEPRINT.md.

Create a small requirements.txt and Streamlit app with WAV upload, microphone recording using st.audio_input, playback, an Analyze action, and a clear educational scope note. Require Streamlit >=1.40 and use arguments compatible with the tested version. Add minimal audio decoding/preparation helpers, display original duration/sample rate/channel count, and provide readable handling for empty, corrupt, silent, unsupported-rate, or out-of-duration files.

Preserve actual amplitudes for quality checks. Use mono conversion, DC removal, and anti-aliased resampling to 16000 Hz. Do not add estimation methods, noise experiments, or a dashboard framework yet. Keep source files simple.

Verify audio reading using generated WAV bytes at two supported sample rates and with mono/stereo data, plus invalid input. Launch or smoke-test the app as the environment permits. Do not claim microphone hardware capture was verified unless it actually was.

Add actual setup/launch instructions to the root README without losing the reference-pack index. Update the progress file. Explain what works, what still needs manual verification, and stop before M2.
~~~

## M2 Implement the filtering and RMS envelope

~~~text
Implement M2 only on top of the verified M1 work.

Read the blueprint and current status. In dsp.py, implement the shared configuration, audio band-pass, 250 ms RMS frames every 50 ms with center timestamps, and the 0.1 to 0.8 Hz envelope band-pass at the correct 20 Hz envelope sample rate. Start with N=2 Butterworth SOS filters and sosfiltfilt. Keep DSP functions independent of Streamlit.

Expose the original waveform, audio spectrogram, raw RMS, and filtered rhythm in the app. Show the design settings and analysis interval, excluding the first/last 5 seconds only after filtering the full clip. Explain the distinction between the audio band and rhythm band. Return meaningful messages for degenerate signals and filtering failures.

Use a deterministic amplitude-modulated acoustic signal to check that the known slow envelope survives the audio filter and extraction. Verify matching array lengths and frame-center times. Add only small meaningful tests where helpful.

Update the progress file and record all actual settings. Stop before peak detection in M3.
~~~

## M3 Add the peak based prototype estimate

~~~text
Implement M3 only.

Add candidate cycle detection using find_peaks with the blueprint's initial prominence and spacing rules. Calculate BPM from the median accepted interval, guard insufficient markers, and return unavailable with reasons when appropriate. Show cycle markers, candidate count, analyzed duration, and peak BPM in the GUI.

Keep the result provisional where cycle interpretation is ambiguous. Do not assume every inhale and exhale burst is a separate breath, automatically halve all estimates, clamp a rate into range, or use reference labels to select detections.

Verify deterministic synthetic acoustic cases at 12, 18, and 24 BPM and invalid cases such as silence. For those clean engineering signals, aim for absolute error <=2 BPM; report actual outcomes and investigate failures. This is an implementation sanity check, not a claim about real-world accuracy.

If real clips are already available, inspect them and identify likely duplicate or missed markers. Otherwise state that real-data validation remains pending. Update the progress file and stop before M4.
~~~

## M4 Check real recordings and stabilize the prototype

~~~text
Perform M4: pilot validation and targeted fixes, without adding final-project features.

Use docs/03_MIDTERM_CHECKPOINT.md to work with 2 or 3 real WAV clips and manual full-cycle labels or counts. If files are not available, finish the recording/labeling instructions and leave the real-data checks pending; do not invent files or results.

For each available clip, record the analyzed interval, manual reference method, reference BPM, peak estimate, error, candidate count, and observations. Inspect double counting, missed cycles, filtering edges, silence, and recording quality. Make only evidence-based fixes using these development clips and document any changes to the defaults. Keep the code, blueprint, and actual settings synchronized.

Choose a reliable example for the demo if the pilot supports one, and retain a failed or difficult case to explain limitations. Do not tune separately using each clip's true BPM or present the pilot as broad accuracy.

Record actual checks and remaining limitations. Stop before M5.
~~~

## M5 Complete the midterm checkpoint and stop

~~~text
Complete M5 using docs/03_MIDTERM_CHECKPOINT.md.

Audit the actual prototype against the checklist. Fix only issues that prevent the midterm demo. Check setup, upload, playback, the plots, peak markers, invalid-input behavior, and readable labels. Record microphone capture as a separate manual check if it was not verified.

Prepare a short midterm presentation outline or Markdown slide content using only features and pilot results that exist. Save actual screenshots when the environment can capture them; otherwise provide the exact capture list. Include filter choices, limitations, remaining final-project work, and actual individual contributions. Do not invent contribution entries.

Update the progress file with COMPLETE, PARTIAL, or PENDING evidence for each midterm acceptance item. If real-data validation or GUI verification is pending, clearly mark the midterm checkpoint incomplete.

STOP AT THE MIDTERM CHECKPOINT. Do not add autocorrelation, quality scoring, SNR sweeps, or optional features. Return the launch command, demonstrated behavior, unresolved checks, and the saved continuation location. Wait for my instruction to begin F1.
~~~

## F1 Add independent autocorrelation and quality reporting

~~~text
The midterm has been reviewed. Begin F1, the first final-project stage.

Read the current implementation and handoff first. Preserve the working prototype. Add an independent ACF estimator on the same central filtered envelope, following the blueprint: mean removal, normalized autocorrelation, positive local maxima at lags 1.25 to 10 seconds, and BPM = 60 / selected lag. Do not seed the lag search with the peak BPM or reference rate.

Show both estimates, selected lag, ACF plot, method disagreement, and the documented Low/Medium/High heuristic quality indicator. Handle unavailable results and weak evidence honestly. Record why agreement is not proof of correctness.

Check known-rate engineering signals, silence, weak periodicity, and double-burst or harmonic cases. Report actual outcomes without reference-driven corrections. Explain the quality thresholds and keep them configurable in one place. Update the progress file and stop before F2.
~~~

## F2 Prepare manual labels and freeze the evaluation

~~~text
Perform F2 using docs/04_FINAL_EVALUATION_PLAN.md and docs/templates/README.md.

Build the small CSV loading and validation path needed for recordings and annotations. Use 6 real clips from two members at three comfortable paces when available, and separate development clips from evaluation clips. Do not manufacture missing data.

Use manual full-cycle markers to derive the reference rate over the same analyzed interval. For event F1, use the same cycle event in reference and prediction, a predeclared +/-0.5 second one-to-one matching tolerance, and mark ambiguous labels as unscorable. Onset labels are not interchangeable with envelope maxima.

Implement reference BPM, absolute error, MAE, valid-estimate coverage, and peak-event precision/recall/F1 with clear handling of missing predictions, absent labels, and invalid inputs. ACF is evaluated for rate, not assigned event-detection F1.

Freeze and save the configuration and label protocol before final testing. Validate metric calculations with a few hand-checkable examples, including duplicate detections and missing estimates. Update status and stop before the SNR experiment.
~~~

## F3 Run the method comparison and noise study

~~~text
Implement and run F3 according to docs/04_FINAL_EVALUATION_PLAN.md.

Add evaluation.py and a modest Evaluation tab with real-clip selection, both methods, results tables, and CSV export. Evaluate original recordings and added white noise at 20, 10, 5, 0, and -5 dB SNR with three fixed seeds. Use identical noisy audio for both methods, add noise before preprocessing, verify the achieved added-noise SNR, and do not clip mixtures before analysis.

Use the frozen configuration. Export all per-recording, per-SNR, per-seed results including unavailable estimates. Distinguish the original-recording condition from added-noise conditions and explain that existing noise in a real recording is unknown.

Produce MAE versus SNR for both methods and valid-estimate coverage alongside it. Average trials within recordings before summarizing across recordings. Include a same-valid-clips comparison where possible. Do not count repeated noisy mixtures as independent people.

If real data is absent, finish the experiment implementation and deterministic checks, but leave real-data tables and conclusions pending. Do not substitute synthetic results for a real-recording experiment. Update the progress file and stop before F4.
~~~

## F4 Add the optional synthetic demonstration if time permits

~~~text
Perform F4 only if required features and real-data evaluation are complete or clearly tracked as externally pending.

Add a small synthetic-audio mode with known BPM, duration, and added-noise SNR. Use amplitude-modulated filtered noise or another audible carrier with one clear full-cycle modulation. Include a double-burst example as an explicit stress case if it is simple to explain.

Label all outputs Synthetic. Keep synthetic and real-recording results in separate groups, and pass synthetic audio through the same pipeline. Provide a fixed seed for repeatability. Do not add a third estimator or large simulation framework.

If this feature would delay required work, record it as omitted and move to the final audit. Update the progress file and stop before F5.
~~~

## F5 Audit the final project and prepare the handoff

~~~text
Complete F5 using docs/05_REPORT_AND_VIVA.md.

Audit the GUI and actual code, reproduce the exported method comparison and SNR summaries from saved settings/seeds, and verify that report tables match those outputs. Make a clean-environment launch check where feasible and document any check that cannot be performed.

Prepare report content, final demo notes, limitations, and the actual contribution summary. Describe the exact filter design and forward-backward response, the two independent methods, manual reference protocol, metrics, pilot size, missing-estimate coverage, and existing-noise limitation. Use actual numbers only.

Retain the midterm milestone record. Update README setup steps and docs/06_PROGRESS_AND_HANDOFF.md with final status, versions, commands, evidence paths, and unresolved issues. Return a clear list of completed requirements and any remaining blockers. Do not declare the project complete if required real-data evaluation remains pending.
~~~

## Repair prompt

~~~text
Repair the current stage without advancing to another stage.

Read the failing output, current code, blueprint, and progress file. Reproduce the issue, identify the cause, and make the smallest understandable fix. Preserve working behavior. Rerun only the relevant checks and any directly affected check. If a design default changes, update the blueprint and configuration record together.

Report the failure, fix, actual verification, and remaining uncertainty. Keep missing real-data or microphone checks pending. Stop at the current stage.
~~~

## Resume prompt

~~~text
Resume this DSP project from its actual saved state.

Read README.md and docs/00_START_HERE.md through docs/06_PROGRESS_AND_HANDOFF.md, inspect existing code and results, and compare them with the recorded status. Do not restart from scratch or trust a checklist without evidence.

Identify the current stage, completed work, failed or pending checks, frozen settings, available recordings, and next authorized step. If the midterm checkpoint is reached, remain there unless I explicitly ask to start the final-project phase.

Return a concise status and next prompt. Do not add features in this context-recovery turn.
~~~
