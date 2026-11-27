"""M3 engineering cases and failure checks, separate from real-data validation."""

import unittest

import numpy as np

from dsp import AUDIO_CONFIG, analyze_audio, detect_cycles, prepare_audio, read_wav
from test_audio import tone, wav_bytes
from test_processing import modulated_tone


def candidate_case(peak_times):
    """Known event timings for interval arithmetic, not a model of breathing audio."""
    times = np.arange(0, 60, 0.05)
    rhythm = np.zeros_like(times)
    for peak_time in peak_times:
        rhythm += np.maximum(1 - np.abs(times - peak_time), 0)
    return {
        "config": AUDIO_CONFIG.copy(),
        "envelope_time_s": times,
        "rhythm": rhythm,
        "analysis_mask": (times >= 5) & (times < 55),
        "envelope_sample_rate": 20,
        "flat_envelope": False,
    }


class EstimationTests(unittest.TestCase):
    def test_known_rates_through_full_wav_pipeline(self):
        for bpm in (12, 18, 24):
            with self.subTest(known_bpm=bpm):
                recording = read_wav(wav_bytes(modulated_tone(bpm / 60), 16000))
                result = analyze_audio(prepare_audio(recording))
                self.assertEqual(result["rate_status"], "provisional")
                self.assertLessEqual(abs(result["peak_bpm"] - bpm), 2)
                self.assertGreaterEqual(result["candidate_count"], 3)
                self.assertTrue(result["analysis_mask"][result["peak_indices"]].all())
                np.testing.assert_array_equal(result["peak_times_s"], result["envelope_time_s"][result["peak_indices"]])
                self.assertTrue((result["intervals_s"] >= result["min_peak_spacing_s"] - 1e-10).all())
                self.assertEqual(len(result["peak_prominences"]), result["candidate_count"])

    def test_median_interval_is_used_despite_one_long_gap(self):
        result = detect_cycles(candidate_case([6, 11, 16, 25]))
        np.testing.assert_allclose(result["intervals_s"], [5, 5, 9])
        self.assertAlmostEqual(result["peak_bpm"], 12)
        self.assertGreater(result["interval_cv"], 0.2)

    def test_fewer_than_three_markers_does_not_report_a_rate(self):
        result = detect_cycles(candidate_case([10, 30]))
        self.assertEqual(result["candidate_count"], 2)
        self.assertIsNone(result["peak_bpm"])
        self.assertEqual(result["rate_status"], "unavailable")
        self.assertIn("at least 3", result["rate_reason"])

    def test_out_of_range_rate_is_unavailable_not_clamped(self):
        result = detect_cycles(candidate_case([6, 26, 46]))
        self.assertEqual(result["candidate_count"], 3)
        self.assertIsNone(result["peak_bpm"])
        self.assertIn("outside", result["rate_reason"])

    def test_constant_carrier_and_silence_cannot_supply_bpm(self):
        result = analyze_audio(prepare_audio(read_wav(wav_bytes(tone(), 16000))))
        self.assertIsNone(result["peak_bpm"])
        self.assertEqual(result["candidate_count"], 0)
        self.assertIn("variation", result["rate_reason"])
        with self.assertRaisesRegex(ValueError, "No usable sound"):
            analyze_audio(prepare_audio(read_wav(wav_bytes(tone(amplitude=0), 16000))))

    def test_nearby_peaks_respect_minimum_spacing(self):
        case = candidate_case([])
        times = case["envelope_time_s"]
        case["rhythm"] = np.sin(2 * np.pi * times)
        result = detect_cycles(case)
        self.assertGreater(result["candidate_count"], 0)
        self.assertTrue((np.diff(result["peak_times_s"]) >= 1.25 - 1e-10).all())

    def test_double_burst_pattern_is_not_silently_halved(self):
        time = np.arange(60 * 16000) / 16000
        amplitude = 1 + 0.65 * np.sin(2 * np.pi * 0.4 * time) + 0.1 * np.sin(2 * np.pi * 0.2 * time)
        samples = 0.15 * amplitude * np.sin(2 * np.pi * 700 * time)
        result = analyze_audio(prepare_audio(read_wav(wav_bytes(samples, 16000))))
        self.assertEqual(result["rate_status"], "provisional")
        self.assertGreater(result["peak_bpm"], 22)

    def test_prominence_override_is_recorded_without_changing_defaults(self):
        prepared = prepare_audio(read_wav(wav_bytes(modulated_tone(0.3), 16000)))
        result = analyze_audio(prepared, prominence_fraction=0.3)
        self.assertEqual(result["config"]["peak_prominence_fraction"], 0.3)
        self.assertEqual(AUDIO_CONFIG["peak_prominence_fraction"], 0.15)
        for fraction in (0, -0.1, np.nan, 1.1):
            with self.subTest(fraction=fraction), self.assertRaisesRegex(ValueError, "prominence fraction"):
                analyze_audio(prepared, prominence_fraction=fraction)

    def test_invalid_or_empty_envelopes_are_handled(self):
        case = candidate_case([])
        self.assertIsNone(detect_cycles(case)["peak_bpm"])
        case["rhythm"][10] = np.nan
        with self.assertRaisesRegex(ValueError, "finite envelope"):
            detect_cycles(case)


if __name__ == "__main__":
    unittest.main()
