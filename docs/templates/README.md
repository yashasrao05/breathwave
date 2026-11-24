# Data templates

The CSV files contain headers only. Copy them to data or results folders when implementation reaches the relevant stage. Do not add fabricated sample measurements.

## Recordings

recordings.csv has one row per original file:
- recording_id: stable unique ID.
- participant_id: anonymous P1/P2-style ID.
- file_path: path relative to the project root, using forward slashes.
- dataset_role: development or evaluation.
- source_type: real or synthetic.
- duration_s: measured duration.
- pace_label: descriptive requested pace, not reference BPM.
- microphone_distance_cm, device, conditions: actual recording notes.
- analysis_start_s and analysis_end_s: the common scoring interval in original clip time.
- reference_method: event_timestamps or timed_count.
- manual_complete_cycles and reference_window_duration_s: only for a timed-count reference.
- event_labels_scorable: true or false.
- notes: uncertainties and relevant conditions.

For timed counts, the analysis start/end must match the timed reference window, and the duration field must equal their difference. Timestamp-reference rates are derived from annotations, not typed from the intended pace.

## Annotations

annotations.csv has one row per manually marked event:
- recording_id and event_index.
- event_time_s: seconds from the original recording start.
- event_type: cycle_burst_maximum or inhale_start.
- labeler_id: anonymous ID.
- scorable: true or false.
- notes.

Use at least three valid events for a provisional timestamp-based rate reference. Only cycle_burst_maximum events support the planned peak-event F1. Do not mix event types in one rate series. Original annotations remain unchanged across added-noise trials.

## Results

results.csv has one row per attempted method result:
- run_id, recording_id, dataset_role, source_type.
- condition: original or added_white_noise.
- target_added_snr_db and achieved_added_snr_db: blank for original.
- noise_seed: blank for original.
- method: peak or acf.
- analysis_start_s and analysis_end_s.
- reference_bpm and estimated_bpm.
- absolute_error_bpm: blank if either rate is unavailable.
- status and reason.
- candidate_count: peak method only.
- tp, fp, fn, precision, recall, f1: peak method and scorable event labels only.
- config_id: identifier of the saved settings.
- notes.

Unavailable estimates remain rows. CSV blanks are missing values, not zero. Runtime input errors should also remain visible with a status and reason.

## Contributions

contributions.csv logs actual completed work:
- date, member_id, task.
- files_or_evidence.
- verification.
- notes.

The planned ownership table is not a completed contribution log. Record shared work as shared work with both participants identified.
