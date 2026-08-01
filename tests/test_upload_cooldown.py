import tempfile
import unittest
from pathlib import Path
from unittest import mock

from fenjue.runtime import batch


class UploadCooldownTests(unittest.TestCase):
    def setUp(self) -> None:
        self.original_state_file = batch.UPLOAD_COUNTER_STATE_FILE
        self.temp_dir = tempfile.TemporaryDirectory()
        batch.UPLOAD_COUNTER_STATE_FILE = Path(self.temp_dir.name) / "upload_state.json"
        batch._upload_counter_loaded = True
        batch._uploaded_images_since_cooldown = 0
        batch._upload_window_started_at = 0.0
        batch._last_upload_counter_at = 0.0

    def tearDown(self) -> None:
        batch.UPLOAD_COUNTER_STATE_FILE = self.original_state_file
        batch._upload_counter_loaded = False
        batch._uploaded_images_since_cooldown = 0
        batch._upload_window_started_at = 0.0
        batch._last_upload_counter_at = 0.0
        self.temp_dir.cleanup()

    def test_first_upload_time_is_preserved_across_later_uploads(self) -> None:
        with mock.patch.object(batch.time, "time", return_value=1_000.0):
            batch.record_uploaded_image_count(4)
        with mock.patch.object(batch.time, "time", return_value=1_500.0):
            batch.record_uploaded_image_count(4)

        self.assertEqual(batch._uploaded_images_since_cooldown, 8)
        self.assertEqual(batch._upload_window_started_at, 1_000.0)
        self.assertEqual(batch._last_upload_counter_at, 1_500.0)

    def test_threshold_wait_uses_30_minute_minimum_after_20_slow_rounds(self) -> None:
        batch._uploaded_images_since_cooldown = 80
        batch._upload_window_started_at = 1_000.0
        batch._last_upload_counter_at = 11_000.0

        with (
            mock.patch.object(batch.time, "time", return_value=11_000.0),
            mock.patch.object(batch, "wait_with_echo") as wait_mock,
            mock.patch.object(batch, "refresh_chatgpt_web_after_upload_cooldown") as refresh_mock,
            mock.patch.object(batch, "_reset_upload_counter_state") as reset_mock,
        ):
            batch.apply_upload_cooldown_if_needed(4)

        wait_mock.assert_called_once()
        self.assertEqual(wait_mock.call_args.args[:2], (1_800, "Upload cooldown"))
        refresh_mock.assert_called_once_with()
        reset_mock.assert_called_once_with("cooldown completed")

    def test_fast_uploads_still_wait_until_three_hour_window_ends(self) -> None:
        batch._uploaded_images_since_cooldown = 80
        batch._upload_window_started_at = 1_000.0
        batch._last_upload_counter_at = 6_000.0

        with (
            mock.patch.object(batch.time, "time", return_value=6_000.0),
            mock.patch.object(batch, "wait_with_echo") as wait_mock,
            mock.patch.object(batch, "refresh_chatgpt_web_after_upload_cooldown"),
            mock.patch.object(batch, "_reset_upload_counter_state"),
        ):
            batch.apply_upload_cooldown_if_needed(4)

        self.assertEqual(wait_mock.call_args.args[0], 5_800)

    def test_expiry_is_measured_from_first_upload_not_last_upload(self) -> None:
        batch._uploaded_images_since_cooldown = 40
        batch._upload_window_started_at = 1_000.0
        batch._last_upload_counter_at = 11_700.0

        with (
            mock.patch.object(batch.time, "time", return_value=11_801.0),
            mock.patch.object(batch, "_reset_upload_counter_state") as reset_mock,
        ):
            expired = batch._reset_upload_counter_if_window_expired()

        self.assertTrue(expired)
        reset_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
