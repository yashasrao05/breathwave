# M2 verification

M2 implements audio filtering, RMS envelope extraction, and the signal plots. Verification was performed on 25 November 2026. Peak detection and respiration-rate estimation remain for M3.

## Implemented settings

| Stage | Actual setting |
| --- | --- |
| Processing audio | 16000 Hz mono, after DC removal and resampling |
| Audio band-pass | 100–2000 Hz, Butterworth IIR |
| Filter design | SciPy N=2, SOS, sosfiltfilt for both bands |
| Order | Fourth-order band-pass per pass; effective forward-backward response order eight |
| RMS window | 250 ms, or 4000 samples |
| RMS hop | 50 ms, or 800 samples |
| Envelope sample rate | 20 Hz |
| Envelope band-pass | 0.1–0.8 Hz, Butterworth IIR |
| Central interval | Frame centers from 5 seconds up to, but excluding, duration minus 5 seconds |
| Spectrogram | Prepared audio before band-pass; 512-sample Hann window; 256-sample overlap; PSD |

Both filters run on their complete input arrays before the central interval is selected. The displayed rhythm is signed. Waveform display bins preserve minima and maxima without changing the analysis data.

The acoustic band concerns audible sound; the envelope band concerns its slow energy variations. The envelope cutoffs define the planned 6–48 BPM search range, not a medical classification. The cutoffs are initial engineering choices to assess with real pilot recordings.

## Automated verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m py_compile app.py dsp.py tests/test_audio.py tests/test_app.py tests/test_processing.py
.\.venv\Scripts\python.exe -m pip check
```

**Result:** all 21 tests passed in 27.590 seconds. Syntax checks passed and pip check found no broken requirements. The initial GUI image-count assertion queried the wrong AppTest element name; it was corrected from imgs to image before the successful rerun. No DSP algorithm change was needed for that test correction.

The new tests cover RMS frame counts/center times and constant-signal RMS amplitude; carrier preservation and stop-band rejection; envelope drift/fast-variation rejection; known slow modulations; full-length array alignment and central masks; invalid or short filtering inputs; and a flat-envelope warning. Existing input/GUI checks also pass, including clearing previous analysis when the recording changes.

## Known modulation measurements

The engineering signal is an audible 700 Hz carrier with a positive amplitude envelope modulated at the known frequency. Each case is 60 seconds long and passes through WAV decoding, preparation, audio filtering, RMS extraction, and envelope filtering.

| Known modulation in Hz | Dominant filtered rhythm in Hz | Correlation with expected rhythm |
| --- | --- | --- |
| 0.2 | 0.2 | 0.999939 |
| 0.3 | 0.3 | 0.999945 |
| 0.4 | 0.4 | 0.999962 |

Frequency inspection is a test-only FFT check, not an estimator exposed in the app. Correlations were calculated over the central interval against a sinusoid at the known modulation frequency. These checks establish signal preservation for these constructed inputs, not accuracy on real breathing recordings.

Each 60-second case produces 1196 RMS frames at center times 0.125 through 59.875 seconds. Adjacent centers are 0.05 seconds apart. The central 5–55 second interval contains 1000 centers, from 5.025 through 54.975 seconds. Raw RMS and filtered rhythm have matching time arrays and lengths. The first/last five seconds are retained in plots and shaded.

## Browser verification

The localhost health endpoint returned HTTP 200 with body ok. A generated 60-second, 44100 Hz mono PCM WAV, .cache/m2-am-engineering.wav, was uploaded and analyzed through the actual browser GUI.

Verified:

- Correct original metadata and successful analysis status.
- Central interval shown as 5.00–55.00 seconds, with a 50.00-second span.
- Original mono-average and audio-band-pass waveforms on matching time axes.
- Input-audio spectrogram with a visible 700 Hz carrier and acoustic-frequency units.
- Raw RMS and signed filtered envelope on aligned time axes with shaded edge margins.
- Readable titles, units, and explanation of the acoustic versus envelope bands.

Screenshots of that engineering input:

- [Waveforms](screenshots/m2-waveforms.png).
- [Spectrogram](screenshots/m2-spectrogram.png).
- [RMS and filtered envelope](screenshots/m2-envelope.png).

## Limitations and next stage

Real breathing recordings, microphone hardware capture, and audible speaker playback remain unverified. The nearly constant RMS warning uses a 1% percentile-span-to-median heuristic; it is not a calibrated confidence or final signal-quality indicator. Filtering artifacts near clip boundaries may persist beyond the shaded margins.

Tested versions remain Python 3.12.10, Streamlit 1.67.0, NumPy 2.5.5, SciPy 1.18.1, Matplotlib 3.11.2, and SoundFile 0.14.0. No additional dependencies were installed for M2. As in M1, successful runtime checks used approved execution outside the restricted shell.

The QA server is stopped after verification. Launch with the README command to use the app. M3 will add candidate cycle detection and a peak-interval BPM estimate; neither is present in M2.
