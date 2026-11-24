# Report and viva guide

Explain the DSP decisions using the actual implementation and measurements. Keep the report readable enough that either team member can trace a recording from input to estimate.

## Report structure

1. **Problem and scope:** audio-based respiration-rate estimation, GUI requirement, educational use, and tested microphone conditions.
2. **Objectives and requirements:** inputs, plots, two methods, signal quality, and noise evaluation.
3. **System design:** architecture and a pipeline figure.
4. **Preprocessing:** channel conversion, DC removal, resampling, duration checks, and amplitude handling.
5. **Filter design:** Butterworth IIR choice, design N, resulting band-pass order, SOS representation, forward-backward application, exact cutoffs, and actual combined frequency response.
6. **Envelope extraction:** RMS formula, 250 ms window, 50 ms hop, 20 Hz sequence, frame-center timing, and rhythm filtering.
7. **Estimators:** peak prominence/spacing, interval-to-BPM conversion, ACF lag selection, unavailable results, and double-counting risks.
8. **Quality indicator:** exact heuristic rules, development process, and limits.
9. **Evaluation protocol:** participants/clips, development overlap, manual events, analysis window, matching tolerance, noise scaling, seeds, and frozen settings.
10. **Results:** actual original-recording comparison, MAE versus SNR, coverage, supported event metrics, and optional separate synthetic results.
11. **Discussion:** failure examples, false or missed cycles, harmonics, recording quality, and small-sample limitations.
12. **Contributions and conclusion:** actual individual work, achieved objectives, and modest future improvements.
13. **References and reproducibility appendix:** package versions, launch instructions, configuration, and experiment commands.

Do not insert expected accuracy values into the results section. Leave data-dependent prose unfinished until the exported results exist.

## Planned ownership

| Member | Main responsibility | Supporting responsibility |
| --- | --- | --- |
| Member 1 | Audio input, decoding, preprocessing, filtering, waveform and spectrogram | Noise mixing and evaluation GUI |
| Member 2 | Envelope extraction, peak detection, BPM, autocorrelation | Quality rules, reference metrics, comparison |
| Both | Recording, manual inspection, integration, demo | Report review, limitations, viva |

This is a proposed division, not a contribution record. Log actual completed tasks, checks, and evidence in contributions.csv. Use real names only when preparing the submission. Each person should understand both estimators and the common preprocessing.

## Viva questions to prepare

- Why filter audible audio and its envelope at different frequencies?
- What do 0.1 and 0.8 Hz mean in BPM?
- Why use a Butterworth IIR filter for this prototype?
- What does SciPy N=2 mean for a band-pass?
- What changes when the filter is applied forward and backward?
- Why use SOS, and why is this processing offline?
- How do RMS window length and hop differ?
- Why is the envelope sample rate 20 Hz?
- How does one complete breathing cycle differ from one sound burst?
- Why use a median peak interval?
- Why exclude zero lag in autocorrelation?
- How can harmonics or multiple-period peaks produce the wrong rate?
- How were manual reference events chosen and how uncertain are they?
- Why must reference timestamps and predicted timestamps represent the same event?
- What do precision, recall, F1, MAE, and valid-estimate coverage measure?
- How was noise scaled to the target SNR?
- Why is original-recording noise unknown?
- Why can low error among successful estimates hide poor coverage?
- What can six clips from two participants establish?
- Which function, result, and debugging decision did each member contribute?

Practice with actual plots rather than memorizing generic definitions.

## Final handoff checklist

- [ ] A fresh launch follows documented commands without code edits.
- [ ] Both estimators and invalid-result behavior are demonstrated.
- [ ] The configuration matches the report and exported settings.
- [ ] Original and noisy real-recording comparisons exist.
- [ ] All attempted trials, failures, and denominators are retained.
- [ ] Synthetic results, if present, are labeled separately.
- [ ] Figures have units, legends, and stated populations.
- [ ] Both members can explain one successful and one difficult case.
- [ ] Contribution records describe actual work.
- [ ] The midterm checkpoint record remains available.
