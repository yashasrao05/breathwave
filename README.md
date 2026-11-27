# Respiration Rate Estimator

Build a student-level Streamlit GUI that estimates respiration rate from recorded audio using a transparent DSP pipeline. The immediate goal is a working midterm prototype. Continue to the final project only after the midterm checkpoint is reviewed.

**Prepared:** 23 November 2026. **Working midterm target:** 28 November 2026, based on the latest planning discussion. The originally pasted announcement lists 24 October 2026; confirm the actual final submission date separately.

**Current state:** M5 midterm preparation is complete with real-recording validation deferred by user instruction. The overall validation checkpoint remains partial. The app supports WAV upload, microphone recording controls, playback, saving original audio, preparation, filtering, plots, candidate markers, and a provisional peak-based BPM. Autocorrelation and the noise study remain for the final-project phase.

**M4 status:** software and preparation complete under the revised scope agreed on 27 November 2026; real-recording validation deferred until recordings are supplied. The app offers **Save original WAV**, and the collection guide and worksheet are ready. No real-recording accuracy is claimed.

**Midterm materials:** [six-slide presentation content](docs/12_MIDTERM_PRESENTATION.md), [demo runbook](docs/13_MIDTERM_DEMO.md), and [M5 acceptance audit](docs/14_M5_AUDIT.md). Actual member contributions, microphone capture, and audible playback still need manual evidence. Development is stopped at the midterm; no final-stage features were added.

To prepare repeatable generated demo inputs, run:

```powershell
.\.venv\Scripts\python.exe tools/prepare_midterm_demo.py
```

Then upload `data/midterm_engineering/engineering-18bpm.wav` through the app. These files are generated acoustic signals, not real breathing recordings. The saved [engineering snapshot](docs/midterm-engineering-snapshot.json) records measured results and current baseline settings.

## Run the app

Use Python 3.12 for the tested development environment. From a PowerShell terminal in the project folder, set up a virtual environment once:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If several Python versions are installed, use the path to your Python 3.12 executable for the first command. Virtual-environment activation is optional; the commands below call its Python directly.

Launch the app:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open [the local app](http://localhost:8501) if the browser does not open automatically. Use Ctrl+C in the terminal to stop it.

## Use the prototype

1. Choose **Upload WAV** or **Record audio**. Allow microphone access when recording.
2. Provide 30 to 120 seconds of audio, preferably around 60 seconds. Use mono or stereo WAV with a sample rate of at least 8000 Hz, up to 50 MB.
3. Inspect the original duration, sample rate, channels, and playback.
   Use **Save original WAV** to download the original input, and rename each take before starting another recording.
4. Click **Analyze audio** to run the pipeline and obtain a provisional peak-based BPM, candidate count, and analyzed duration. Unusable estimates appear as **Unavailable** with a reason.
5. Inspect the waveforms, spectrogram, and envelope with candidate markers. Gray waveform/envelope margins mark the first and last five seconds, excluded from cycle detection.
6. Open **Filter and envelope settings** to see the actual cutoffs, filter design, RMS window/hop, and envelope sample rate.
7. Inspect **Cycle detection details** for marker times, actual prominence threshold, median interval, and interval variability. **Detection settings** offers a prominence-fraction slider for pilot tuning; changing it clears the previous result until you analyze again.

Changing or removing the input clears the previous preparation result. Original decoded samples retain their amplitude; preparation averages channels, subtracts the mono mean, and uses polyphase FIR resampling when needed. Near-silence is checked after DC removal with an RMS threshold of 0.000001. This threshold is an input guard, not a calibrated signal-quality score.

M2 uses a 100–2000 Hz Butterworth audio band-pass, RMS windows of 250 ms every 50 ms, and a 0.1–0.8 Hz Butterworth envelope band-pass at 20 Hz. Both bands use SciPy design N=2 with SOS forward-backward filtering: fourth order per pass and effective response order eight. These are initial choices for pilot testing. The full clip is filtered before the central interval is selected. A warning appears for nearly constant RMS envelopes, since filtering edges can otherwise resemble a slow pattern.

M3 uses a minimum marker spacing of 1.25 seconds and an initial prominence threshold of 0.15 times the central filtered envelope's 95th-to-5th percentile span. At least three candidate markers are required. BPM is 60 divided by the median interval; out-of-range results are not clamped. Flat RMS envelopes do not supply a BPM. Rates remain provisional because separate inhalation and exhalation bursts can cause double counting. Do not automatically halve outputs or tune a separate setting using each clip's reference rate.

The microphone works through the browser. Use localhost for the local demo. Microphone permission, actual capture, and audible playback must be checked on the demo device. The app keeps the current audio in the running session and does not save recordings to a data folder automatically.

## Collect the M4 pilot

Record 2 or 3 real breathing clips, preferably about 60 seconds each. Use Save original WAV, rename each take, and place it in [data/pilot](data/pilot/README.md). Follow the [M4 pilot guide](docs/10_M4_PILOT_GUIDE.md) and fill the [pilot worksheet](docs/11_M4_PILOT_WORKSHEET.md) with manual reference measurements before reviewing the estimate.

The deferred M4 pilot requires actual reference rates, app outputs, errors, and observations about duplicate or missed cycles. The worksheet contains empty planning records, not results. Current DSP settings remain unchanged until real development recordings support a revision. M4 software/preparation and M5 packaging are complete; the missing pilot does not require repeating those stages. Follow the resume prompt in the demo runbook when recordings become available; update the presentation and audit with actual evidence.

## Run the checks

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
```

These checks use generated audio for engineering validation. They do not establish accuracy on real breathing recordings. See the progress log for verified checks and pending manual checks.

[M1 verification](docs/07_M1_VERIFICATION.md) records the tested versions, 13 passing tests, browser checks, screenshots, and microphone/playback checklist. The current GUI tests use Streamlit 1.67's AppTest upload helpers.

[M2 verification](docs/08_M2_VERIFICATION.md) records that stage's 21 passing tests, known-modulation engineering measurements, timing checks, settings, and plot screenshots.

[M3 verification](docs/09_M3_VERIFICATION.md) records the current 31 passing tests, known-rate results, unavailable cases, the double-burst limitation, and browser screenshots. These engineering checks do not replace the real-recording pilot.

The M4 save-control change was checked with the six GUI tests and Python syntax compilation. Saving retained the current analysis in AppTest. Actual microphone capture, browser file saving, and real-data validation remain manual checks.

## Source files

- [app.py](app.py): Streamlit input, playback, settings, provisional rate summary, and signal plots with candidate markers.
- [dsp.py](dsp.py): shared configuration, preparation, SOS filtering, RMS extraction, cycle candidates, and interval-based BPM.
- [requirements.txt](requirements.txt): application dependencies.
- [tests](tests/): audio preparation, filtering, envelope, peak-rate, and GUI regression checks.

## Planning reference pack

**Private reference page:** [Respiration audio project implementation guide](https://chatgpt.com/space/page_afb4aa01c48481918bc14b93a6553274). The local files below are the working copies to update during implementation; the Page is a planning reference snapshot.

## Start another implementation chat

1. Open this project folder in the new chat, or attach the reference pack if the chat cannot access it.
2. Read [Start here](docs/00_START_HERE.md).
3. Copy **Prompt 0** from [Implementation prompts](docs/02_IMPLEMENTATION_PROMPTS.md).
4. Send prompts **M1 to M5**, one at a time. Review the output of each step.
5. Stop at the [Midterm checkpoint](docs/03_MIDTERM_CHECKPOINT.md).
6. After the midterm, explicitly start **F1 to F5** to complete the final project.

The prompts request actual implementation and verification. They are designed to preserve a simple codebase that both team members can explain.

## Reference documents

| File | Purpose |
| --- | --- |
| [Start here](docs/00_START_HERE.md) | Goal, reading order, milestones, and how to resume |
| [Project blueprint](docs/01_PROJECT_BLUEPRINT.md) | Architecture, DSP settings, formulas, GUI, and failure behavior |
| [Implementation prompts](docs/02_IMPLEMENTATION_PROMPTS.md) | Copyable startup, sequential build, repair, and resume prompts |
| [Midterm checkpoint](docs/03_MIDTERM_CHECKPOINT.md) | Acceptance checklist, pilot procedure, demo, and presentation outline |
| [Final evaluation plan](docs/04_FINAL_EVALUATION_PLAN.md) | Method comparison, SNR protocol, annotation rules, and metrics |
| [Report and viva guide](docs/05_REPORT_AND_VIVA.md) | Report outline, contribution division, and viva questions |
| [Progress and handoff](docs/06_PROGRESS_AND_HANDOFF.md) | Honest status, decisions, checks, and next step |
| [Data templates](docs/templates/README.md) | CSV schemas for recordings, annotations, results, and contributions |

The relative links above are portable when the folder is moved. The project blueprint is the technical source of truth; the progress file records the settings and behavior actually implemented. Update both when an agreed technical decision changes.

## Scope

The required methods are peak detection and autocorrelation. The final result includes quantitative comparison and error versus added-noise SNR. Synthetic audio is an optional engineering aid. This is an educational DSP demonstration, not a medical diagnostic tool.

Do not claim the work is complete from screenshots alone. Keep real measurements, settings, and commands used for verification.
