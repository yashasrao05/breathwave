# M4 real recording pilot guide

Collect 2 or 3 real breathing recordings, establish a manual reference for each, and compare the current peak-based estimate with that reference. As agreed on 27 November 2026, M4 software/preparation is complete and this real-recording pilot is deferred until the user supplies recordings and manual references.

The collection workflow and worksheet are ready. No real-data results, filter tuning, successful demo clip, or difficult real example have been established. M5 presentation/demo packaging is already prepared; resume only the deferred pilot when data arrive, then update its results and acceptance evidence. Do not repeat earlier implementation stages.

## Collect and save the recordings

1. Launch the app using the README command and select Record audio. Allow microphone access yourself if requested.
2. Use a quiet room and a steady microphone position. Breathe comfortably; aim for about 60 seconds. The app accepts 30 to 120 seconds.
3. Stop recording and check that the duration and audio playback are plausible.
4. Select Save original WAV. The download is the original audio bytes, not the filtered or resampled signal.
5. Rename the file and place it in data/pilot. Suggested names are P1_take1.wav and P2_take1.wav. Save each take before starting another recording so it is not lost when the current widget changes.
6. Record the anonymous participant ID, device, approximate microphone distance, conditions, and any interruptions. Obtain the participant's agreement for use in the course demonstration.

Start with one quiet take from each member. A third take may capture a different comfortable pace or naturally noisier conditions. Keep it labeled as a development recording. Requested pace is not the reference rate. Do not claim the app works at distances or noise levels that were not tested.

The browser typically saves downloads to its configured Downloads location; move the files using the file manager. The app does not automatically write the recording into the project folder. Uploading an existing WAV and selecting Save original WAV also preserves that original input.

## Establish the reference before inspecting the estimate

Use the actual interval shown by the app: start 5 seconds, end recording duration minus 5 seconds. For an exactly 60-second clip, this is 5.00–55.00 seconds. A 60.4-second clip instead uses 5.00–55.40 seconds. Record the displayed interval, not an assumed 50-second duration.

If collecting labels before pressing Analyze, the interval can be calculated from the displayed duration. Confirm it against the exact interval after analysis. Keep reference notes separate from the automatic candidate markers and BPM until the initial manual reference is recorded.

### Preferred reference using timestamps

Listen to the recording and mark one consistent event per full inhale-exhale cycle, such as the start of each inhale. Use original-recording time in seconds, not time from the beginning of the cropped interval. Retain events inside the common analysis interval and use at least three events for a provisional reference.

For K manually marked cycle events:

```text
reference BPM = 60 * (K - 1) / (last event time - first event time)
```

Keep the event definition consistent. Mark uncertain events and timestamp precision. If the sound does not let you distinguish full cycles, mark the reference uncertain instead of labeling every audible burst as one breath. A partner's observation during recording can help identify complete cycles.

The app's peak method uses the median interval; this reference formula uses the average interval. For irregular breathing, report that difference in statistics when interpreting errors.

### Simple fallback using a timed count

Count complete inhale-exhale cycles over the same documented interval, then calculate:

```text
reference BPM = 60 * manually counted cycles / counted window duration
```

Use the actual window duration in seconds. Partial cycles at the boundaries and uncertain manual counts affect this rough reference, especially for short clips. Record the counting rule and uncertainty. A count-based reference supports a preliminary rate comparison, not event-timestamp precision, recall, or F1.

An intended pace, an automatically detected candidate count, or the app's displayed BPM is not a manual reference.

## Compare the current baseline

Upload the saved clip and start with prominence fraction 0.15. Keep all current DSP defaults for the first pass. Click Analyze audio and record:

- Filename, original duration, source sample rate, and conditions.
- Exact analysis interval and manual reference method, events/count, and reference BPM.
- Peak BPM or unavailable status and reason.
- Candidate marker count, prominence fraction, actual prominence threshold, and interval variability.
- Absolute error in BPM when both reference and estimate are available.
- Observations about duplicate bursts, missed events, edges, silence, speech, and handling noise.

```text
absolute error in BPM = abs(estimated BPM - reference BPM)
```

Keep an unavailable estimate in the worksheet with its reason. Leave its numerical error blank. Do not replace it with zero BPM or silently exclude the recording.

Use [the pilot worksheet](11_M4_PILOT_WORKSHEET.md) for the small midterm set. The existing CSV schemas in docs/templates remain available for the final evaluation; an automated evaluation tab is not needed for M4.

## Inspect cycle interpretation and recording quality

- Check one full inhale-exhale cycle against the audible bursts and candidate markers. Two regular bursts can produce a doubled rate with very low interval variability.
- Check whether weak cycles are missed or nearby peaks are selected inconsistently.
- Inspect the first and last five seconds and the central interval for filtering artifacts. The shaded margins do not guarantee all transients have vanished.
- Listen for speech, direct airflow, clipping/distortion, microphone contact, and abrupt background sounds. Record the observation without treating the current provisional indicator as a calibrated quality measure.
- Save screenshots of the rate summary and marked envelope for each usable example. Keep the original WAV and manual notes alongside them.

M3's generated two-burst stress case returned 24 BPM for a full pattern of 12 BPM. This is a known limitation to investigate, not evidence that all estimates should be divided by two.

## Make only evidence based fixes

If recordings reveal a problem, first improve the recording or inspect the event interpretation. Compare changes using these development clips and keep the original baseline results.

A prominence change is available in Detection settings. Record the before/after fraction and reason. Do not choose a separate value for every clip just because it makes the answer match its reference BPM. Choose one explainable baseline for the demo and record any operating limits. Filtering or event-selection changes need observed evidence, appropriate checks, and synchronized documentation.

Do not add ACF, confidence percentages, automatic halving, a noise sweep, or a third estimator during this stage. Final-project comparison and evaluation remain separate work.

## Select examples and finish the deferred pilot

When the pilot supports it, retain one reliable real clip for the demo and one difficult or failed real case for explaining limitations. Record the selection and reasons in the worksheet. With two or three development clips, describe the findings as a small pilot rather than broad accuracy.

The deferred pilot is complete only after at least two real clips have documented manual references, actual app results, cycle inspection, and recorded limitations. Save the working settings and update the progress log, presentation, and M5 audit. Closing M4 software/preparation under the revised scope does not satisfy these real-data acceptance items. Use the resume prompt in [the demo runbook](13_MIDTERM_DEMO.md) when the recordings are available; final-project features still require a separate instruction.

## Verification status

- Recording save support is implemented using the original audio bytes.
- AppTest checks exercise the save-control click path and confirm it retains the current analysis. This does not verify a physical microphone or a browser's final download location.
- Six GUI tests passed in 15.323 seconds on 27 November 2026; Python syntax compilation passed. DSP code and defaults were unchanged, so the prior M3 full-suite result remains 31 passing tests.
- Actual microphone capture, downloaded-file playback on the demo device, manual labels, pilot errors, tuning decisions, and demo selection remain pending.
