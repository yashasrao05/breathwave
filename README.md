# Respiration Rate Estimator

A student‑level **Streamlit** GUI that estimates respiration rate from recorded audio using a transparent digital‑signal‑processing (DSP) pipeline.

---

## 📅 Project Timeline
- **Prepared:** 27 November 2026
- **Mid‑term target:** 28 November 2026 (prototype)
- **Final target:** TBD (after mid‑term checkpoint)

---

## 🔧 Current State (as of 27 Nov 2026)
- **M5 (mid‑term) software & preparation** – complete.
- **Real‑recording validation (M4)** – deferred; recordings to be supplied later.
- The app supports:
  - WAV upload and microphone recording.
  - Playback, original‑audio inspection, and saving.
  - DSP preparation, filtering, envelope extraction, and a provisional peak‑based BPM estimate.
- Autocorrelation and noise‑study stages are slated for the final‑project phase (F1‑F5).

---

## 🚀 Quick Start
```powershell
# 1. Create a virtual environment (once)
python -m venv .venv

# 2. Install dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 3. Launch the app
.\.venv\Scripts\python.exe -m streamlit run app.py
```
Open the app at <http://localhost:8501> (it may open automatically). Use **Ctrl+C** to stop.

---

## 🎙️ Using the Prototype
1. **Upload a WAV** file **or** record audio (microphone permission required).
2. Provide 30–120 s of audio (preferably ~60 s). Accepts mono or stereo WAVs, ≥ 8 kHz, ≤ 50 MB.
3. The UI shows original duration, sample rate, channels, and playback controls.
4. Click **Analyze audio** to run the pipeline and obtain:
   - Provisional BPM (peak‑based).
   - Candidate marker count.
   - Analyzed duration.
5. Inspect waveforms, spectrogram, and envelope with markers.
6. Settings panel displays filter cut‑offs, RMS window/hop, and envelope sample rate.
7. Cycle‑detection details expose marker times, prominence threshold, median interval, and variability.
8. Changing or removing the input clears previous results.

---

## 🛠️ DSP Details (see `docs/01_PROJECT_BLUEPRINT.md` for full specs)
- **Audio band‑pass:** 100–2000 Hz Butterworth, 2nd‑order SOS, forward‑backward filtering.
- **RMS extraction:** 250 ms windows every 50 ms.
- **Envelope band‑pass:** 0.1–0.8 Hz Butterworth at 20 Hz sample rate.
- **Resampling:** Anti‑aliased polyphase FIR to 16 kHz.
- **Silence guard:** RMS > 0.000001 after DC removal.
- **Peak detection (M3):** Minimum spacing 1.25 s, prominence ≥ 0.15 × (95th‑5th percentile) of envelope.

---

## 📂 Repository Layout
| Path | Purpose |
| ---- | ------- |
| `app.py` | Streamlit UI, audio I/O, and result display |
| `dsp.py` | Core DSP functions (pre‑processing, filters, RMS, envelope, peak detection) |
| `requirements.txt` | Python dependencies |
| `tests/` | Unit tests for preparation, filtering, envelope, peak‑rate, and GUI regression |
| `docs/` | Design documents, blueprints, prompts, and progress reports |
| `data/` | Placeholder for pilot recordings (`data/pilot/README.md`) |

---

## 📚 Documentation
- **Start here:** `docs/00_START_HERE.md`
- **Blueprint:** `docs/01_PROJECT_BLUEPRINT.md`
- **Implementation prompts:** `docs/02_IMPLEMENTATION_PROMPTS.md`
- **Mid‑term checkpoint:** `docs/03_MIDTERM_CHECKPOINT.md`
- **Final evaluation plan:** `docs/04_FINAL_EVALUATION_PLAN.md`
- **Report & viva guide:** `docs/05_REPORT_AND_VIVA.md`
- **Progress & handoff:** `docs/06_PROGRESS_AND_HANDOFF.md`
- **Pilot guide & worksheet:** `docs/10_M4_PILOT_GUIDE.md`, `docs/11_M4_PILOT_WORKSHEET.md`
- **Mid‑term presentation & demo:** `docs/12_MIDTERM_PRESENTATION.md`, `docs/13_MIDTERM_DEMO.md`
- **Audit:** `docs/14_M5_AUDIT.md`

---

## ✅ Run the Checks
```powershell
# Unit tests
.\.venv\Scripts\python.exe -m unittest discover -s tests -v

# Dependency sanity check
.\.venv\Scripts\python.exe -m pip check
```
These tests use generated engineering audio; they do **not** validate real‑recording accuracy.

---

## 📋 Mid‑term Materials
- **Presentation:** `docs/12_MIDTERM_PRESENTATION.md`
- **Demo run‑book:** `docs/13_MIDTERM_DEMO.md`
- **Audit checklist:** `docs/14_M5_AUDIT.md`

---

## 📈 Next Steps
- **M4:** Record 2–3 real breathing clips, fill `docs/11_M4_PILOT_WORKSHEET.md`, and validate the prototype.
- **F1‑F5:** After the mid‑term checkpoint, add autocorrelation, quality reporting, evaluation, noise study, and final audit.

---

## 🧾 License
This project is for educational purposes. See the `LICENSE` file for details.
