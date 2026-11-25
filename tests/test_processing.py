"""M2 engineering checks. Generated signals are not real breathing validation."""

import unittest

import numpy as np

from dsp import AUDIO_CONFIG, analyze_audio, bandpass_filter, prepare_audio, read_wav, rms_envelope
from test_audio import tone, wav_bytes


def modulated_tone(rate_hz, duration=60, sample_rate=16000):
    """A known slow amplitude cycle on an audible 700 Hz carrier."""
    time = np.arange(round(duration * sample_rate)) / sample_rate
    return 0.15 * (1 + 0.65 * np.sin(2 * np.pi * rate_hz * time)) * np.sin(2 * np.pi * 700 * time)


class ProcessingTests(unittest.TestCase):
    def test_rms_count_center_times_and_amplitude(self):
        times, rms = rms_envelope(np.full(30 * 16000, 0.2), 16000, 0.25, 0.05)
        self.assertEqual(len(rms), 596)
        self.assertAlmostEqual(times[0], 0.125)
        self.assertAlmostEqual(times[-1], 29.875)
        np.testing.assert_allclose(np.diff(times), 0.05, atol=1e-12)
        np.testing.assert_allclose(rms, 0.2, atol=1e-10)

    def test_known_modulations_survive_the_full_wav_pipeline(self):
        for frequency in (0.2, 0.3, 0.4):
            with self.subTest(modulation_hz=frequency):
                samples = modulated_tone(frequency)
                recording = read_wav(wav_bytes(samples, 16000))
                prepared = prepare_audio(recording)
                result = analyze_audio(prepared)
                mask = result["analysis_mask"]
                rhythm = result["rhythm"][mask]
                expected = np.sin(2 * np.pi * frequency * result["envelope_time_s"][mask])
                self.assertGreater(float(np.corrcoef(rhythm, expected)[0, 1]), 0.99)
                spectrum = np.abs(np.fft.rfft(rhythm - rhythm.mean()))
                frequencies = np.fft.rfftfreq(len(rhythm), d=1 / result["envelope_sample_rate"])
                # Frequency inspection is a test oracle only; there is no app rate estimator in M2.
                self.assertAlmostEqual(float(frequencies[np.argmax(spectrum[1:]) + 1]), frequency, places=3)
                self.assertEqual(len(result["filtered_audio"]), len(prepared["audio"]))
                self.assertEqual(len(result["audio_time_s"]), len(prepared["audio"]))
                self.assertEqual(len(result["rms"]), len(result["rhythm"]))
                self.assertEqual(len(result["rhythm"]), len(result["envelope_time_s"]))
                self.assertEqual(result["analysis_start_s"], 5)
                self.assertEqual(result["analysis_end_s"], 55)
                self.assertEqual(np.count_nonzero(mask), 1000)
                self.assertLess(result["envelope_time_s"][0], 5)
                self.assertGreater(result["envelope_time_s"][-1], 55)
                self.assertLess(float(rhythm.min()), 0)
                self.assertGreater(float(rhythm.max()), 0)

    def test_audio_band_retains_carrier_and_rejects_remote_frequencies(self):
        gains = {}
        for frequency in (20, 500, 5000):
            source = tone(duration=5, frequency=frequency)
            filtered = bandpass_filter(source, 16000, AUDIO_CONFIG["audio_band_hz"], 2)
            gains[frequency] = float(np.sqrt(np.mean(filtered[16000:-16000] ** 2)) / np.sqrt(np.mean(source**2)))
        self.assertGreater(gains[500], 0.95)
        self.assertLess(gains[20], 0.02)
        self.assertLess(gains[5000], 0.02)

    def test_envelope_band_rejects_slow_drift_and_fast_modulation(self):
        time = np.arange(120 * 20) / 20
        gains = {}
        for frequency in (0.01, 0.3, 3):
            source = np.sin(2 * np.pi * frequency * time)
            filtered = bandpass_filter(source, 20, AUDIO_CONFIG["envelope_band_hz"], 2)
            gains[frequency] = float(np.sqrt(np.mean(filtered[400:-400] ** 2)) / np.sqrt(np.mean(source[400:-400] ** 2)))
        self.assertGreater(gains[0.3], 0.95)
        self.assertLess(gains[0.01], 0.02)
        self.assertLess(gains[3], 0.02)

    def test_flat_rms_warns_without_claiming_a_breathing_pattern(self):
        result = analyze_audio(prepare_audio(read_wav(wav_bytes(tone(), 16000))))
        self.assertTrue(result["warnings"])
        self.assertIn("very little amplitude variation", result["warnings"][0])

    def test_filters_reject_short_non_finite_and_invalid_settings(self):
        for samples in (np.empty(0), np.ones(5), np.array([np.nan] * 30)):
            with self.subTest(length=len(samples)), self.assertRaises(ValueError):
                bandpass_filter(samples, 20, (0.1, 0.8), 2)
        with self.assertRaisesRegex(ValueError, "Invalid filter settings"):
            bandpass_filter(np.ones(100), 20, (0.1, 12), 2)

    def test_rms_rejects_short_and_invalid_input(self):
        for samples in (np.empty(0), np.ones(10), np.array([np.inf] * 5000)):
            with self.subTest(length=len(samples)), self.assertRaises(ValueError):
                rms_envelope(samples, 16000, 0.25, 0.05)

    def test_analysis_rejects_unprepared_sample_rate(self):
        with self.assertRaisesRegex(ValueError, "16000 Hz"):
            analyze_audio({"audio": np.ones(100), "sample_rate": 8000})


if __name__ == "__main__":
    unittest.main()
