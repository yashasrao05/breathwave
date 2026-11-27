# Midterm demo and deferred checks

M5 is prepared as of 27 November 2026. The user explicitly deferred recordings until later. Use this runbook to demonstrate the software without implying that real breathing performance has been measured.

## Prepare locally

From a PowerShell terminal in `D:\Projects\DSP`, using the installed project environment:

```powershell
.\.venv\Scripts\python.exe tools/prepare_midterm_demo.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open `http://localhost:8501`. For first-time setup or moving to another computer, follow [README](../README.md). The preparation script recreates six clearly named engineering WAVs and measures them into `data/midterm_engineering/latest-run.json`. It preserves the original saved M5 snapshot. No editing of source code is needed to operate the app. There is no synthetic-generation mode inside the GUI at this milestone.

## Four-minute GUI sequence

1. State: “This is a generated acoustic test signal. Real-recording validation is pending.” Choose Upload WAV and select `data/midterm_engineering/engineering-18bpm.wav`.
2. Show 60-second duration, 16000 Hz, mono metadata and the audio player. If demonstrating playback, use a comfortable speaker level; the sound is a carrier tone, not breathing. Audible output still needs an actual listening check.
3. Leave the prominence fraction at 0.15. Click Analyze audio. Expect approximately **17.9 provisional BPM**, **15 candidate markers**, and **50.0 s** analyzed duration.
4. Show original/filtered waveforms, spectrogram, and the RMS/envelope plots. Explain the 700 Hz acoustic carrier versus the slow 0.3 Hz modulation. Point out aligned markers, five-second gray margins, and the 5–55 second interval.
5. Open Filter and envelope settings and Cycle detection details. Explain BPM = 60 / 3.35 s ≈ 17.91. Explain why a marker remains a candidate full-cycle event.
6. Upload `engineering-double-burst-12bpm.wav` and analyze at the same defaults. Expect **24 BPM**, although the full pattern repeats at **12 BPM**. Explain the unresolved possibility of counting separate inhale/exhale bursts.
7. If time permits, analyze `engineering-constant-carrier.wav` to show Unavailable or `engineering-silence.wav` to show rejection. Do not represent either result as zero BPM.
8. Show the Record audio control and Save original WAV option if an input is present. State that physical recording and downloaded-file verification are separate pending checks. Finish with remaining work from slide 6.

## Fallback

If the local app cannot start during the presentation, show the saved M2/M3 screenshots and engineering snapshot. Call this a screenshot walkthrough, not a live demo. Screenshots show actual earlier browser runs, not real breathing recordings. Downloaded demo inputs can be regenerated with the command above; keep them available locally before the presentation.

## Checks to do on the actual demo machine

- [ ] Start with the documented command and open the app in the chosen browser.
- [ ] Listen to uploaded playback and confirm audible output.
- [ ] Allow microphone access, record at least 30 seconds, stop, and confirm metadata and audible playback.
- [ ] Analyze the captured clip. A meaningful unavailable result is allowed; do not promise a valid rate from arbitrary capture.
- [ ] Save original WAV, locate the downloaded file, rename it, and re-upload it successfully.
- [ ] Confirm both members' actual contribution entries before claiming individual ownership.

The automated recording-widget test stages WAV bytes; it does not satisfy the physical microphone checklist.

## Deferred real-recording task

This work stays assigned to M4 even though M5 packaging has now been completed. No recording or placeholder result is added to the pilot table.

| Task | Location / evidence to retain | Completion condition |
| --- | --- | --- |
| Collect 2–3 real clips | `data/pilot/`; [collection guide](10_M4_PILOT_GUIDE.md) | At least two usable WAVs with device/conditions and participant agreement recorded |
| Make independent manual references | [Pilot worksheet](11_M4_PILOT_WORKSHEET.md) | Consistent full-cycle events or timed counts in the same central interval; uncertainty documented |
| Compare baseline to references | Worksheet/results | Actual reference BPM, predicted BPM or unavailable reason, error, candidate count, and duplicate/missed-cycle inspection |
| Revise settings only if supported | Blueprint, config, progress | Common evidence-based choice; baseline and any revised outputs retained |
| Update the presentation | Slides 4–6 in the presentation document | Add real results with source/conditions; keep engineering examples labeled separately |
| Close remaining acceptance items | [M5 audit](14_M5_AUDIT.md) | Evidence-backed statuses, including actual contributions and device checks |

Resume prompt:

```text
Resume deferred M4 validation after M5 packaging. Read docs/06_PROGRESS_AND_HANDOFF.md,
docs/10_M4_PILOT_GUIDE.md, docs/11_M4_PILOT_WORKSHEET.md, and docs/14_M5_AUDIT.md.
Inspect the real WAVs and manual references I have now provided. Run and document the
pilot, inspect duplicate/missed cycles, and make only evidence-based prototype fixes.
Update the midterm results and pending acceptance items. Preserve the original
engineering snapshot. Do not start F1 or other final-project features.
```

After the midterm, F1 may start only on explicit instruction. Deferred real-data work remains required for the final project even if other software work proceeds first.
