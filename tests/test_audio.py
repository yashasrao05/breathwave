"""M1 checks using generated WAV bytes, not real breathing recordings."""

from io import BytesIO
import unittest

import numpy as np
import soundfile as sf

from dsp import AUDIO_CONFIG, prepare_audio, read_wav


def wav_bytes(samples, sample_rate, subtype="FLOAT", format="WAV"):
    buffer = BytesIO()
    sf.write(buffer, samples, sample_rate, format=format, subtype=subtype)
    return buffer.getvalue()


def tone(sample_rate=16000, duration=30, frequency=500, amplitude=0.2):
    time = np.arange(round(sample_rate * duration)) / sample_rate
    return amplitude * np.sin(2 * np.pi * frequency * time)


class AudioInputTests(unittest.TestCase):
    def test_mono_and_stereo_at_multiple_sample_rates(self):
        for sample_rate in (8000, 16000, 44100, 48000):
            for channels in (1, 2):
                with self.subTest(rate=sample_rate, channels=channels):
                    signal = tone(sample_rate)
                    samples = signal if channels == 1 else np.column_stack((signal, 0.5 * signal))
                    recording = read_wav(wav_bytes(samples, sample_rate))
                    prepared = prepare_audio(recording)
                    self.assertEqual(recording["channels"], channels)
                    self.assertEqual(recording["source_sample_rate"], sample_rate)
                    self.assertEqual(prepared["sample_rate"], 16000)
                    self.assertEqual(len(prepared["audio"]), 30 * 16000)
                    self.assertTrue(np.isfinite(prepared["audio"]).all())
                    expected_peak = 0.2 if channels == 1 else 0.15
                    middle = prepared["audio"][1000:-1000]
                    self.assertAlmostEqual(float(np.max(np.abs(middle))), expected_peak, delta=0.002)

    def test_dc_removal_does_not_change_original_samples(self):
        samples = tone() + 0.1
        recording = read_wav(wav_bytes(samples, 16000))
        original = recording["original_audio"].copy()
        prepared = prepare_audio(recording)
        np.testing.assert_array_equal(recording["original_audio"], original)
        self.assertAlmostEqual(prepared["dc_offset"], 0.1, places=6)
        self.assertAlmostEqual(float(prepared["audio"].mean()), 0, places=10)
        self.assertAlmostEqual(float(np.max(prepared["audio"])), 0.2, places=6)

    def test_downsampling_suppresses_out_of_band_alias(self):
        samples = tone(48000, frequency=11000)
        prepared = prepare_audio(read_wav(wav_bytes(samples, 48000)))
        output_rms = float(np.sqrt(np.mean(prepared["audio"][1000:-1000] ** 2)))
        self.assertLess(output_rms, 0.002)

    def test_empty_corrupt_and_non_wav_files(self):
        for data, message in (
            (b"", "empty"),
            (b"this is not a WAV", "Could not read"),
            (wav_bytes(tone(), 16000, subtype="PCM_16", format="FLAC"), "Unsupported audio format"),
            (wav_bytes(np.empty(0), 16000), "no audio samples"),
        ):
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                read_wav(data)

    def test_duration_boundaries_and_unsupported_sample_rate(self):
        for duration in (29.9, 120.1):
            with self.subTest(duration=duration), self.assertRaisesRegex(ValueError, "30 to 120"):
                read_wav(wav_bytes(tone(8000, duration), 8000))
        self.assertEqual(read_wav(wav_bytes(tone(8000, 120), 8000))["duration_s"], 120)
        with self.assertRaisesRegex(ValueError, "at least 8000"):
            read_wav(wav_bytes(tone(4000), 4000))
        with self.assertRaisesRegex(ValueError, "one or two channels"):
            read_wav(wav_bytes(np.column_stack([tone()] * 3), 16000))

    def test_silence_dc_only_and_cancelling_stereo(self):
        signal = tone()
        for samples in (np.zeros_like(signal), np.full_like(signal, 0.2), np.column_stack((signal, -signal))):
            with self.subTest(shape=samples.shape), self.assertRaisesRegex(ValueError, "No usable sound"):
                prepare_audio(read_wav(wav_bytes(samples, 16000)))

    def test_non_finite_audio(self):
        for value in (np.nan, np.inf):
            samples = tone()
            samples[100] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "invalid sample values"):
                read_wav(wav_bytes(samples, 16000))

    def test_quiet_signal_is_not_peak_normalized(self):
        prepared = prepare_audio(read_wav(wav_bytes(tone(amplitude=0.0001), 16000)))
        self.assertLess(float(np.max(np.abs(prepared["audio"]))), 0.00011)


if __name__ == "__main__":
    unittest.main()
