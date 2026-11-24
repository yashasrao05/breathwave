# Respiration Rate Estimator

Build a student-level Streamlit GUI that estimates respiration rate from recorded audio using a transparent DSP pipeline. The immediate goal is a working midterm prototype. Continue to the final project only after the midterm checkpoint is reviewed.

**Prepared:** 23 November 2026. **Working midterm target:** 28 November 2026, based on the latest planning discussion. The originally pasted announcement lists 24 October 2026; confirm the actual final submission date separately.

**Current state:** M1 audio input and preparation are implemented. The app supports WAV upload, microphone recording, playback, input validation, mono conversion, DC removal, and resampling to 16000 Hz. Filtering, plots, and BPM estimation belong to later stages. No real breathing recordings or experimental accuracy results have been added.

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

## Use M1

1. Choose **Upload WAV** or **Record audio**. Allow microphone access when recording.
2. Provide 30 to 120 seconds of audio, preferably around 60 seconds. Use mono or stereo WAV with a sample rate of at least 8000 Hz, up to 50 MB.
3. Inspect the original duration, sample rate, channels, and playback.
4. Click **Analyze audio** to prepare the signal. M1 reports audio preparation only; no breathing rate is calculated yet.

Changing or removing the input clears the previous preparation result. Original decoded samples retain their amplitude; preparation averages channels, subtracts the mono mean, and uses polyphase FIR resampling when needed. Near-silence is checked after DC removal with an RMS threshold of 0.000001. This threshold is an input guard, not a calibrated signal-quality score.

The microphone works through the browser. Use localhost for the local demo. Microphone permission, actual capture, and audible playback must be checked on the demo device. The app keeps the current audio in the running session and does not save recordings to a data folder automatically.

## Check M1

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
```

These checks use generated audio for engineering validation. They do not establish accuracy on real breathing recordings. See the progress log for verified checks and pending manual checks.

[M1 verification](docs/07_M1_VERIFICATION.md) records the tested versions, 13 passing tests, browser checks, screenshots, and microphone/playback checklist. The current GUI tests use Streamlit 1.67's AppTest upload helpers.

## Source files

- [app.py](app.py): Streamlit input, playback, metadata, and preparation action.
- [dsp.py](dsp.py): shared audio limits, WAV decoding, mono conversion, DC removal, and resampling.
- [requirements.txt](requirements.txt): application dependencies.
- [tests](tests/): audio preparation and GUI regression checks.

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
