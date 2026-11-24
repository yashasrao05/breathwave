# Final evaluation plan

Compare peak detection and autocorrelation quantitatively on a small real-recording pilot, then measure how controlled added noise affects both methods. Keep the configuration fixed during testing and report failed estimates.

## Dataset and development split

Target 6 evaluation clips: 2 participants at 3 comfortable breathing paces, preferably about 60 seconds per clip. Use the 2 or 3 midterm development clips separately where possible. Record new evaluation takes after tuning. If any development clips are reused, label those results as development or descriptive results and state the overlap.

Do not infer achieved BPM from the requested pace. Derive the reference from manual full-cycle labels. These recordings are a small convenience sample of two participants; noise realizations do not increase participant count.

Preserve original files and document the analyzed time interval. Use the common central interval for both methods and the reference. Keep an inventory in recordings.csv and annotations in annotations.csv, using the supplied schemas.

## Reference events and rate

The default timestamp event for event-scoring is cycle_burst_maximum: the amplitude maximum of the dominant inhale-related burst, identified once per full inhale-exhale cycle from replay and the unfiltered RMS display. Use a partner's full-cycle notes when helpful. The labeler should not see automatic peak markers while assigning reference events.

If inhale and exhale cannot be distinguished reliably, mark event labels unscorable and explain why. Do not force an event F1 result. A clear manual cycle count can still support a descriptive rate comparison when its interval is documented.

Use at least three reference events within the common interval. Reference BPM = 60 times (K minus 1) divided by the difference between the last and first reference event times. This is an average cycle rate, while the peak estimator uses a median interval; irregular breathing can make the statistics differ.

Inhale-onset timestamps may be retained for rate evaluation, but do not score them directly against envelope maxima. Reference labels are manual audio-based measurements, not a physiological gold standard.

## Event matching

Declare a tolerance of plus or minus 0.5 seconds before final testing. This is a project choice that must be stated in the report.

Match only scorable cycle_burst_maximum labels to predicted cycle peaks. Use one-to-one matching that maximizes the number of matches within tolerance and then minimizes total timing error. With regular, well-separated events this can be implemented clearly; confirm duplicate detections cannot match the same reference event.

- TP: matched reference-prediction pairs.
- FP: unmatched predicted markers.
- FN: unmatched scorable reference markers.
- Precision = TP / (TP + FP).
- Recall = TP / (TP + FN).
- F1 = 2 TP / (2 TP + FP + FN).

With valid reference events and zero predictions, set recall and F1 to zero; precision is undefined and should be blank with a reason. With no scorable reference labels, mark event metrics unavailable. Missing labels are not zero detection accuracy.

Autocorrelation provides a period estimate, not cycle timestamps, so assign event precision/recall/F1 only to peak detection.

## Rate metrics

For each valid method estimate, absolute error = abs(estimated BPM minus reference BPM). MAE is the mean absolute error across the stated set of recordings.

Report:
- number of recordings and valid manual references;
- each method's MAE on its valid estimates;
- each method's valid-estimate coverage: valid estimates divided by eligible recordings or trials;
- paired MAE comparison on clips/trials where both methods return a valid estimate;
- individual clip results, including failures.

An unavailable estimate has a blank BPM and error plus a status/reason. Do not substitute zero BPM or silently remove the row. Always state the denominator of MAE and coverage. Error among only surviving estimates can improve while the method is failing more often.

For event metrics, provide per-clip values and optionally pooled TP/FP/FN totals for each condition. State which aggregation is used; do not average counts and call them pooled metrics.

## Added noise

Evaluate the original-recording condition separately, then add white Gaussian noise at SNR values 20, 10, 5, 0, and minus 5 dB.

Use 3 fixed seeds, for example 11, 22, and 33. For each recording, generate an independent seeded noise sequence. Reuse its direction across SNR levels by scaling it, which gives a paired severity comparison. Both estimators must receive the exact same noisy audio for each trial.

Mix noise into mono, DC-removed source audio at its source sample rate before resampling and filtering. Calculate reference signal power over the central evaluation interval and scale the noise using that same interval:

- Ps = mean(source samples squared).
- Pn = mean(noise samples squared).
- target noise power = Ps / (10 raised to SNR_dB / 10).
- scale factor = sqrt(target noise power / Pn).
- mixture = source + scale factor times noise.

Guard zero power. Verify achieved added-noise SNR numerically from the clean source and added noise components. Do not peak-normalize the source and mixture separately or clip the noisy mixture before processing. If playback needs attenuation, create a separate playback copy.

Real recordings already contain unknown noise. Therefore this is added-noise SNR relative to the original recording, not a known true clean-breathing SNR. White-noise results also do not establish robustness to speech, fan noise, or microphone handling.

## Trial counts and reproducibility

With 6 eligible evaluation clips:
- Original condition: 6 clips processed by both methods.
- Added-noise conditions: 6 clips times 5 SNRs times 3 seeds = 90 mixtures.
- Two estimators produce 180 noisy method-result rows, plus 12 original-condition rows.

These are planned counts. Actual counts must reflect the available data and exclusions. Preserve all attempted trials and reasons for ineligibility.

Save the configuration snapshot, source recording IDs, analysis intervals, seeds, package versions, per-trial rows, summaries, and figures. Per-trial rows should include both the target and achieved added-noise SNR. The original condition has no seed and no numeric added-noise SNR; do not encode it as 0 dB.

## Aggregation and figures

For each method and SNR, average errors over valid seeds within each recording, then summarize across recordings with equal recording weight. Report the count of valid seeds and recordings. Compute coverage across all eligible trials. For paired comparison, use trials where both methods are valid.

Produce:
1. An original-recording table with reference and both estimates/errors.
2. A method summary table with MAE, coverage, and denominators.
3. An MAE-versus-added-noise-SNR plot with one line per method.
4. A coverage-versus-SNR plot or accompanying table.
5. Peak-event metrics where labels support them.

Show the original-condition baseline separately or as clearly labeled horizontal reference lines. Do not pretend it is another finite-SNR point. With this small pilot, per-recording values or ranges are more useful than claims of population-level statistical significance.

## Synthetic mode

Optional known rates: 12, 18, and 24 BPM. Generate an audible carrier or filtered-noise signal modulated at that full-cycle rate and pass it through the same pipeline. Keep a fixed seed and label synthetic rows distinctly. A double-burst condition is useful for explaining harmonic and cycle ambiguity.

Use synthetic checks to verify implementation and known-rate behavior. Keep synthetic and real-data summaries separate.

## Evaluation completion

The study is complete only when actual recordings, manual references, the frozen protocol, all attempted result rows, and reproducible summaries exist. Implementing the sweep button does not complete the experiment.
