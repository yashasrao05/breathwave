# Midterm checkpoint

The working target is 28 November 2026. Reach this checkpoint in session 1, then retain the prototype for demonstration. The goal is a functional baseline with a few manually checked real recordings.

## Acceptance checklist

Mark items complete only when supported by actual evidence.

- [ ] Dependencies install and the documented command launches the app.
- [ ] WAV upload decodes a supported recording and reports its metadata.
- [ ] Microphone recording is present and capture is manually verified on the demo machine.
- [ ] Uploaded and recorded audio can be played back.
- [ ] Mono conversion, DC removal, resampling, and filtering are implemented.
- [ ] Waveform and spectrogram are readable and have units.
- [ ] Raw RMS and filtered envelope are visible with correct time alignment.
- [ ] Candidate cycle markers and the analyzed interval appear on the envelope.
- [ ] Peak BPM is calculated from accepted intervals.
- [ ] Silence, short input, corrupt input, and insufficient markers produce useful messages.
- [ ] At least two real clips have manual reference measurements and documented outputs.
- [ ] One real example has been inspected for inhale/exhale double counting.
- [ ] Actual filter settings, limitations, and tuning decisions are recorded.
- [ ] The contribution log reflects work each member actually performed.
- [ ] The midterm presentation accurately separates completed and future work.

A failed microphone test or missing real recordings makes the checkpoint partial. The upload path may still be demonstrated, but the presentation must state the limitation.

## Collecting the pilot recordings

Record 2 or 3 clips for the midterm. A quiet room and roughly 60-second clips are useful starting conditions. Use comfortable breathing and keep the microphone position consistent. Record the approximate distance, device, and background conditions; do not claim reliable operation at a distance that was not tested.

Use anonymous IDs such as P1 and P2. Each participant should agree to having their clip used in this educational demo. Keep filenames predictable and log device/browser details if relevant.

A partner can note complete breathing cycles during recording. Later, replay the clip and inspect the waveform and raw RMS. Count full inhale-exhale cycles, not separate sound bursts.

For the reference rate, annotate a consistent event once per full cycle and retain events in the same central analysis interval as the app. With K manually marked events:
- reference BPM = 60 times (K minus 1) divided by (last event time minus first event time).
- Use at least three events for a provisional reference.
- Record the reference event and uncertainty.

If only a hand count over a timed window is available, reference BPM = 60 times completed cycles divided by window seconds. Label this as a count-based reference and retain that window; it has boundary uncertainty and does not support timestamp F1.

## Preliminary results

Create a real results file during M4, not while drafting this plan. Include:
- recording ID and conditions;
- analysis start/end;
- reference method, count, or event timestamps;
- reference BPM and peak BPM;
- absolute error in BPM, or an unavailable status;
- candidate marker count;
- observations about duplicate markers, missed cycles, and noise.

Two or three examples show prototype behavior. They do not establish broad accuracy or clinical validity.

## Demo sequence

1. Launch the app using the documented command.
2. Load a previously checked real clip and play a short segment.
3. Show the original waveform and acoustic spectrogram.
4. Explain audio filtering and RMS envelope extraction.
5. Show the slow filtered envelope, analyzed interval, and candidate markers.
6. Compare the peak BPM with the manual reference for that clip.
7. Show one limitation or invalid-input example.
8. Identify autocorrelation, quality reporting, and SNR evaluation as remaining work.

Keep checked WAV files available locally in case browser microphone access fails during the presentation. A recording fallback does not count as verification of the live capture feature.

## Six slide outline

| Slide | Content |
| --- | --- |
| 1 | Problem, objectives, educational scope |
| 2 | Pipeline from audio to envelope to peak BPM |
| 3 | Exact initial filter and RMS settings, with reasons |
| 4 | Actual GUI screenshots and one checked example |
| 5 | Preliminary results table and observed limitations |
| 6 | Member contributions and final-project work |

Suggested screenshots: input with playback; waveform and spectrogram; envelope with markers and BPM. Use screenshots of the actual app. Do not present a generated mockup as a working implementation.

## Stop and preserve the milestone

At M5, save the actual configuration, demo clips, results table, screenshot paths, limitations, setup command, and tested versions. Record the checkpoint as COMPLETE or PARTIAL in the progress file.

The next phase begins only when the user sends F1 or otherwise explicitly asks to continue beyond the midterm. Keep the midterm record after final-project changes.
