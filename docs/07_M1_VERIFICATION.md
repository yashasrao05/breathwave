# M1 verification

M1 implements the app shell and audio preparation. Verification was performed on 24 November 2026. This stage does not estimate breathing rate and has not been validated on real breathing recordings.

## Implemented behavior

- WAV upload, microphone widget, original-audio playback control, and Analyze audio action.
- Original duration, sample rate, and channel count.
- Header validation before sample loading, with limits of 30 to 120 seconds, at least 8000 Hz, one or two channels, and 50 MiB.
- Checks for empty, corrupt, unsupported, non-finite, silent, or unusable audio.
- Channel averaging, DC removal, and anti-aliased polyphase resampling to 16000 Hz.
- Preservation of original decoded samples and amplitude; no peak normalization.
- Removal of old preparation results when input changes or becomes invalid.

Audio helpers are independent of Streamlit. The only filtering in M1 is the FIR low-pass operation inherent in sample-rate conversion; the planned breathing-audio and envelope band-passes begin in M2.

## Tested versions

| Component | Version |
| --- | --- |
| Python | 3.12.10 |
| Streamlit | 1.67.0 |
| NumPy | 2.5.5 |
| SciPy | 1.18.1 |
| Matplotlib | 3.11.2 |
| SoundFile | 0.14.0 |

The app uses the standard microphone widget arguments available from the planned minimum Streamlit version. GUI test helpers for staged file uploads and recordings use the tested Streamlit 1.67 API; older AppTest versions may not support those test helpers.

## Automated checks

These commands completed successfully from the project root:

```powershell
.\.venv\Scripts\python.exe -m py_compile app.py dsp.py tests/test_audio.py tests/test_app.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
```

**Result:** 13 tests passed in 13.311 seconds; no broken package requirements.

Eight audio tests cover mono/stereo WAV at 8000, 16000, 44100, and 48000 Hz; duration boundaries; corrupt and unsupported input; non-finite samples; DC removal; silence and phase-cancelling stereo; preservation of quiet amplitudes; and suppression of out-of-band aliasing during downsampling. The anti-alias check requires output RMS below 0.002 for a 0.2-amplitude 11000 Hz tone resampled from 48000 to 16000 Hz.

Five Streamlit tests cover empty upload state, recording-mode state reset, successful upload/preparation followed by corrupt-file replacement, silent-input error reporting, and a generated WAV staged through the recording widget. None use actual microphone capture.

## Browser checks

The server was launched on 127.0.0.1:8501. Its health endpoint returned HTTP 200 with body ok; its root page returned HTTP 200.

The actual browser GUI was checked using .cache/m1-test-tone.wav, a generated 30-second, 44100 Hz, mono PCM WAV:

1. Uploaded the file through the browser file chooser.
2. Confirmed displayed duration 30.0 s, sample rate 44100 Hz, and Mono.
3. Confirmed the audio element loaded 30 seconds of media with readyState 4 and no media error.
4. Clicked Analyze audio and observed Audio prepared successfully with 16000 Hz mono output.
5. Selected Record audio and confirmed the previous success result cleared and the Record control appeared.

These are engineering checks with a tone. They do not measure respiration-rate accuracy.

Screenshots:

- [Upload and prepared result](screenshots/m1-upload-prepared.png).
- [Recording mode](screenshots/m1-recording-mode.png).

## Manual checks still required

- [ ] On the intended demo device, launch the app and select Record audio.
- [ ] Allow the browser microphone permission yourself if prompted.
- [ ] Record 30 to 120 seconds of comfortable breathing, then stop.
- [ ] Confirm the recorded clip appears with plausible duration and metadata.
- [ ] Play the clip and confirm audible sound through the intended speakers/headphones.
- [ ] Click Analyze audio and confirm preparation succeeds or gives a useful input message.
- [ ] Upload a real breathing WAV and repeat playback/preparation.

Actual microphone capture and audible output remain pending. The hardware checks are separate from the successful widget and media-loading checks.

## Environment note and next stage

The restricted execution shell could not resolve the package server initially, denied loopback HTTP access, and stalled the first runtime checks. Those attempts were interrupted. Approved execution outside that restriction installed the declared dependencies and completed the successful tests and server checks. The application did not require a workaround in its own logic.

The QA server is stopped after verification; use the README launch command to run the app. The original reference ZIP and private planning Page remain planning snapshots; current source and this progress record are the implementation state.

Next stage: M2 filtering, RMS envelope extraction, and plots. No M2 or final-project features were added during M1.
