# Project blueprint

Implement a compact offline audio-analysis app. A complete recording is processed after capture or upload. M1 input/preparation, M2 filtering/envelope plots, and M3 candidate peak detection/BPM are implemented as of 27 November 2026. Real-recording pilot validation is pending; it determines whether the initial settings need revision.

## Initial settings

| Setting | Starting value | Reason and qualification |
| --- | --- | --- |
| Input | WAV upload and Streamlit microphone widget | Keep decoding and demonstration straightforward |
| Audio sample rate | Resample accepted audio to 16000 Hz | One processing rate simplifies frame sizes and filters |
| Source sample rate | Accept at least 8000 Hz | Lower rates do not support our intended audio band well |
| Clip duration | 30 to 120 seconds; recommend about 60 | Several full cycles are needed, especially at low rates |
| Upload size and channels | Up to 50 MiB; one or two channels | M1 input limits; reject other channel counts before decoding samples |
| Silence guard | RMS at most 0.000001 after channel averaging and DC removal | M1 rejects silence or near-silence; this is not a calibrated quality score |
| Audio filter | Butterworth IIR band-pass, 100 to 2000 Hz | Initial choice to reduce rumble and out-of-band content; validate on pilot clips |
| Audio design parameter | SciPy butter N=2, output="sos" | Fourth-order band-pass per pass |
| Application | sosfiltfilt | Forward and backward processing of completed recordings |
| RMS window | 250 ms | Smooth short sound fluctuations before rhythm analysis |
| RMS hop | 50 ms | Envelope sample rate is 20 Hz |
| Envelope filter | Butterworth IIR band-pass, 0.1 to 0.8 Hz, N=2, SOS | Initial rhythm range of 6 to 48 breaths/minute |
| Analysis margins | Ignore first and last 5 seconds for estimates | Initial precaution for starting, stopping, and filtering edges; inspect edge effects |
| Peak spacing | At least 1.25 seconds | Derived from the maximum search rate of 48 BPM |
| Peak prominence | Start at 0.15 times the envelope 95th-to-5th percentile span | Relative threshold; expose for pilot tuning, then freeze |
| Minimum markers | Three accepted cycle markers | Two intervals give a provisional estimate; few cycles limit reliability |

The input, filter, envelope, and peak-detection defaults are implemented through M3, but are not measured optimum choices. A 5-second margin does not guarantee all filter transients are removed. Inspect the plots and change the policy if evidence warrants it, before the final evaluation is frozen.

Use one shared configuration in dsp.py. Do not duplicate defaults in the UI, evaluation code, and report. When users change a tuning control, include the actual setting in the displayed run details and exported results.

## Filter order and frequency interpretation

The raw microphone waveform contains audible sound. Breathing rate is a slow repetition of sound energy. Apply the 100 to 2000 Hz filter to the audio and the 0.1 to 0.8 Hz filter to the RMS envelope.

SciPy band-pass design with N=2 produces a fourth-order band-pass for each pass. Forward-backward application squares the magnitude response and has an effective response order of eight. It uses future samples, so this procedure is suitable for a completed clip.

Describe the design parameter, resulting single-pass order, SOS representation, and forward-backward application. Do not simply call the entire operation a second-order filter. The specified Butterworth critical frequencies are single-pass minus-3-dB points; after forward-backward application they are approximately minus-6-dB points. Plot the actual combined response for the report.

The 6 to 48 BPM range is a project search range. It is not a medical classification of normal breathing.

## Processing sequence

1. Decode the audio as floating-point samples. Keep the actual input sample rate and channel count for display.
2. Reject unsupported, corrupt, empty, non-finite, or out-of-duration input with a plain message.
3. Convert stereo to mono by channel averaging. Check that the result is not effectively silent.
4. Remove DC by subtracting the mean. Resample to 16000 Hz with an anti-aliasing method such as resample_poly. Upsampling does not recover missing acoustic information.
5. Retain the original amplitude information for silence and clipping checks. If playback or display normalization is used, keep it separate from quality checks.
6. Apply the audio band-pass in SOS form using sosfiltfilt.
7. For every 250 ms frame spaced by 50 ms, calculate RMS = sqrt(mean(frame squared)).
8. Timestamp each RMS frame at its center. The RMS window is not the hop; use 20 Hz when designing the envelope filter.
9. Apply the envelope band-pass at 0.1 to 0.8 Hz. The resulting rhythm signal may be negative; do not rectify it again.
10. Use the central analysis interval after the 5-second margins. Analyze the full clip before cropping so the crop itself does not create filter edges.
11. Detect peaks, retain their times and properties, and estimate rate. In the final project, also estimate rate independently from autocorrelation.
12. Return data and status to the GUI. Keep DSP functions independent of Streamlit.

## Peak detection baseline

Use scipy.signal.find_peaks with distance expressed in envelope samples and a prominence threshold derived from the central envelope span. Guard a near-zero span and invalid arrays.

One full inhale-exhale cycle is one breath. Two audible bursts can occur within that cycle. Peak spacing and prominence reduce some duplicate detections, but they do not guarantee one peak per breath.

Inspect candidate markers against manual cycles during pilot work. Show detected markers as candidate cycle events until verified. If a clip repeatedly produces two markers per breath, document the failure and adjust the envelope or event-selection rule using development recordings. Do not silently divide every output by two or use the reference BPM to select peaks.

For at least three accepted markers at times t:
- intervals = diff(t), in seconds.
- BPM_peak = 60 / median(intervals).
- Store marker count, intervals, and interval variability.
- If the estimate is outside 6 to 48 BPM, or the data cannot support an estimate, return unavailable with a reason. Do not clamp it to a boundary.

For strongly ambiguous cycles, the app may show a provisional candidate estimate with a warning. A number must not imply that the cycle interpretation has been validated.

M3 reports all available estimates as provisional. The GUI offers a prominence-fraction slider from 0.05 to 0.80, in steps of 0.05, defaulting to 0.15. Actual settings are stored with each analysis; changing the setting invalidates the displayed result. Marker spacing is derived from the maximum search frequency: 1/0.8 = 1.25 seconds, or 25 envelope samples. Three or more markers are required. Results outside 6–48 BPM return no BPM instead of being clamped.

The existing M2 flat-RMS heuristic (central percentile span at most 1% of median RMS) now prevents reporting an estimate from that degenerate envelope. With usable variation, candidate times, prominences, intervals, and interval coefficient of variation are retained. A coefficient above 0.2 triggers an interval-variability warning, not a confidence score. A two-burst engineering pattern can yield a doubled estimate even with regular intervals; no automatic division by two is applied. This must be examined with manual full-cycle references in M4.

## Autocorrelation baseline for the final project

Use the same central filtered envelope and remove its mean. Compute its autocorrelation and normalize by the zero-lag energy. Handle zero energy explicitly.

Search positive local maxima only at lags corresponding to 1.25 to 10 seconds. Exclude zero lag. Select the strongest positive local maximum in that interval and calculate BPM_acf = 60 / lag_seconds. If there is no valid positive maximum, return unavailable.

Keep this estimator independent of the peak-based BPM and all reference labels. Show the selected lag on the ACF plot. Document its susceptibility to harmonics and multiple-period peaks. A peak at twice the true period or half the true period is a possible failure, not a reason to insert a reference-driven correction.

For quality reporting, note whether the analyzed duration contains at least three periods at the selected lag. A short window can still yield a mathematical peak without supporting a reliable estimate.

## Signal-quality indicator for the final project

Use Low, Medium, or High with a brief reason. It is a documented heuristic, not a probability of correctness.

Start with these provisional rules:
- Low: silent or clipped input, insufficient cycles, a method unavailable, weak ACF periodicity below 0.3, or method disagreement greater than 4 BPM.
- High: both methods valid, at least three ACF periods in the window, interval coefficient of variation at most 0.2, selected normalized ACF peak at least 0.5, and method difference at most 2 BPM.
- Medium: valid results that satisfy neither rule.

Evaluate Low first. Define clipping on unnormalized decoded samples; use a documented threshold such as at least 1% of samples near full scale for bounded PCM input. For floating-point WAV, record the amplitude convention and avoid unsupported clipping claims.

These thresholds must be reviewed on development clips and frozen before testing. Agreement can occur when both methods are wrong. The pilot cannot calibrate a confidence probability.

## GUI

Use one analysis page for the midterm:
- Brief project description and educational scope note.
- Upload or Record input choice, audio player, and Analyze button.
- Duration, sample rate, and the interval actually analyzed.
- Peak-based BPM, candidate cycle count, and status.
- Waveform, spectrogram, and raw RMS plus filtered rhythm with markers.
- A small settings expander for pilot tuning and an explanation of the two frequency bands.

Add an Evaluation tab in the final project for labeled clips, method comparison, SNR sweep, a table, and CSV download. Add the ACF estimate and quality indicator to the analysis view.

Every plot needs a descriptive title, units, and a readable time axis. Spectrogram frequency is acoustic frequency in Hz; the rhythm plot time axis is seconds. Downsample only plotted waveform points if needed; do not accidentally decimate the analysis signal.

M2 displays the original mono-average waveform and filtered waveform with extrema-preserving display bins. The spectrogram uses prepared 16000 Hz mono audio before the audio band-pass: 512-sample Hann windows, 256-sample overlap, and PSD in dB relative to 1 input-unit squared per Hz. The RMS and signed filtered envelope appear on separate aligned axes. A display warning is issued when the central RMS 95th-to-5th percentile span is at most 1% of its median, with a machine-epsilon floor; this is a heuristic flat-envelope warning, not the final quality indicator.

## Project files and interfaces

Keep the initial code in app.py and dsp.py. Add evaluation.py when needed. Use functions with short docstrings and a plain result dictionary; no framework of base classes is needed.

The result dictionary should include:
- status and message;
- actual configuration and sample rates;
- time arrays, original/filtered audio, RMS and rhythm arrays;
- analysis start/end times;
- peak times, intervals, peak BPM;
- final-stage ACF lags/values, selected lag, ACF BPM, quality and reasons.

Use None for an unavailable estimate, not 0 BPM. Invalid measurements must remain visible in exported evaluation rows.

Dependencies: Streamlit at least 1.40, NumPy, SciPy, Matplotlib, and SoundFile. Verify any widget keyword arguments against the version installed and record the tested versions. Keep decoding utilities in dsp.py or a small audio helper. Do not add MP3 support until the required WAV path works.

## Verification

Use deterministic amplitude-modulated audio for engineering sanity checks at 12, 18, and 24 BPM. It must be an audible carrier or filtered-noise signal with a known amplitude cycle; a 0.2 Hz sine passed as raw audio is not a realistic test of the acoustic filter. Sanity checks do not replace recordings.

Check mono/stereo inputs, more than one sample rate, silence, short audio, and corrupt bytes. Confirm a real clip does not show obvious inhale/exhale double counting. Accept that some recordings will fail.

Launch the app and inspect its real GUI. Import success alone does not verify the microphone, playback, upload, or plots. Where browser microphone permission or hardware is unavailable, record the unverified step and supply a manual check.

## Technical references

- [Streamlit microphone recording](https://docs.streamlit.io/develop/api-reference/widgets/st.audio_input)
- [Streamlit 1.40 release notes](https://docs.streamlit.io/develop/quick-reference/release-notes/2024#version-1400)
- [SciPy Butterworth design and order](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html)
- [SciPy SOS forward-backward filtering](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfiltfilt.html)
- [SciPy forward-backward response](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html)
- [SciPy peak detection](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html)
- [SciPy correlation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlate.html)
