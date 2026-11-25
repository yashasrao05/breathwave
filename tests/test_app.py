"""GUI smoke checks; browser permission and real microphone capture are manual."""

from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest

from test_audio import tone, wav_bytes


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


class AppTests(unittest.TestCase):
    def test_upload_view_starts_without_input(self):
        app = AppTest.from_file(str(APP_PATH)).run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.radio[0].value, "Upload WAV")
        self.assertEqual(len(app.get("file_uploader")), 1)
        self.assertTrue(app.button[0].disabled)

    def test_record_view_clears_previous_preparation(self):
        app = AppTest.from_file(str(APP_PATH)).run(timeout=30)
        app.session_state["audio_token"] = ("Upload WAV", "previous-recording")
        app.session_state["prepared_audio"] = {"status": "old result"}
        app.session_state["analysis"] = {"status": "old analysis"}
        app.radio[0].set_value("Record audio").run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.get("audio_input")), 1)
        self.assertNotIn("prepared_audio", app.session_state)
        self.assertNotIn("analysis", app.session_state)
        self.assertTrue(app.button[0].disabled)

    def test_upload_prepare_then_replace_with_corrupt_input(self):
        app = AppTest.from_file(str(APP_PATH)).run(timeout=30)
        audio = wav_bytes(tone(44100), 44100, subtype="PCM_16")
        app.file_uploader[0].set_value(("test-tone.wav", audio, "audio/wav")).run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.get("audio")), 1)
        self.assertEqual([metric.value for metric in app.metric], ["30.0 s", "44,100 Hz", "Mono"])
        app.button[0].click().run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.success[0].value, "Audio filtered and envelope extracted successfully.")
        self.assertEqual(app.session_state["prepared_audio"]["sample_rate"], 16000)
        self.assertEqual(app.session_state["analysis"]["envelope_sample_rate"], 20)
        self.assertEqual(len(app.get("image")), 3)
        app.file_uploader[0].set_value(("broken.wav", b"invalid", "audio/wav")).run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.error), 1)
        self.assertEqual(len(app.success), 0)
        self.assertNotIn("prepared_audio", app.session_state)
        self.assertNotIn("analysis", app.session_state)
        self.assertTrue(app.button[0].disabled)

    def test_silent_upload_reports_error_after_analyze(self):
        app = AppTest.from_file(str(APP_PATH)).run(timeout=30)
        audio = wav_bytes(tone(amplitude=0), 16000)
        app.file_uploader[0].set_value(("silence.wav", audio, "audio/wav")).run(timeout=30)
        app.button[0].click().run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertIn("No usable sound", app.error[0].value)
        self.assertEqual(len(app.success), 0)

    def test_recording_widget_accepts_staged_wav(self):
        app = AppTest.from_file(str(APP_PATH)).run(timeout=30)
        app.radio[0].set_value("Record audio").run(timeout=30)
        audio = wav_bytes(tone(), 16000, subtype="PCM_16")
        app.audio_input[0].set_value(("staged-recording.wav", audio, "audio/wav")).run(timeout=30)
        app.button[0].click().run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.get("audio")), 1)
        self.assertEqual(app.success[0].value, "Audio filtered and envelope extracted successfully.")


if __name__ == "__main__":
    unittest.main()
