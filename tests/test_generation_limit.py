from __future__ import annotations

import unittest

from fenjue.vision.generation_limit import (
    is_generation_limit_text,
    parse_reset_delay_seconds,
)


class GenerationLimitTextTests(unittest.TestCase):
    def test_parses_english_minutes(self) -> None:
        text = (
            "You've hit the Plus plan limit for image generations requests. "
            "You can create more images when the limit resets in 26 minutes."
        )
        self.assertTrue(is_generation_limit_text(text))
        self.assertEqual(parse_reset_delay_seconds(text), 26 * 60)

    def test_parses_english_hours_and_minutes(self) -> None:
        text = "Image generation limit resets in 1 hour 27 minutes."
        self.assertTrue(is_generation_limit_text(text))
        self.assertEqual(parse_reset_delay_seconds(text), 87 * 60)

    def test_parses_chinese_hours_and_minutes(self) -> None:
        text = "你目前的图片生成次数已用完，请等待 1 小时 27 分钟后恢复更多次数。"
        self.assertTrue(is_generation_limit_text(text))
        self.assertEqual(parse_reset_delay_seconds(text), 87 * 60)

    def test_rejects_unrelated_generation_text(self) -> None:
        text = "Image generation completed in 26 minutes."
        self.assertFalse(is_generation_limit_text(text))


if __name__ == "__main__":
    unittest.main()
