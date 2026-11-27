# Midterm engineering inputs

These are generated acoustic signals, not recordings of people breathing. They demonstrate the implemented pipeline while the real-recording pilot is deferred.

From the project root, prepare or recreate the WAVs and measured snapshot:

```powershell
.\.venv\Scripts\python.exe tools/prepare_midterm_demo.py
```

The script writes its six named engineering WAVs and `latest-run.json` here. Existing files with those generated names are replaced. It creates `docs/midterm-engineering-snapshot.json` only if absent, preserving the original milestone evidence on later runs. It does not change files in `data/pilot`.

Each clip is 60 seconds, 16000 Hz, mono FLOAT WAV. The positive-amplitude 700 Hz carrier has a known slow modulation. The double-burst stress case repeats its full pattern at 12 BPM but has a stronger 24 BPM component; the baseline detects that faster component. The constant-carrier and silent cases demonstrate unavailable/rejected results.

Upload these files through the normal app. The tone is an engineering input; its playback does not resemble breathing. See [the demo runbook](../../docs/13_MIDTERM_DEMO.md).
