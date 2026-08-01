from __future__ import annotations

import unittest

from fenjue.modes.photoset_template.library import (
    _adapt_shot_prompt,
    _compact_rewritten_shot_prompt,
    _has_explicit_reference_role_lock,
    load_template,
    prompt_for_shot,
)


class PhotosetPromptPreservationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = (
            "Create one finished image for Template 350, shot 2. "
            "Portrait close three-quarter view from near floor level. "
            "Lie prone along the wooden porch, prop both elbows beneath the shoulders, "
            "cup both cheeks with open palms, and raise both lower legs behind. "
            "Place a half watermelon with a spoon very large in the lower foreground "
            "and look straight into camera with a relaxed small smile. "
            "Dress the selected character in a loose pale gray-white micro-striped "
            "short-sleeve henley shirt and relaxed black athletic shorts. "
            "Treat this as one exact arrangement: preserve the stated orientation, crop, "
            "camera angle, support surface, arm paths, hand contacts, leg geometry, and prop placement. "
            "Character references control canonical face, hair, fixed identity accessories, "
            "age impression, and proportions; never copy the photoset person's identity or hairstyle."
        )

    def test_standardized_prompt_has_an_explicit_role_lock(self) -> None:
        self.assertTrue(_has_explicit_reference_role_lock(self.source))

    def test_shot_actions_and_props_survive_runtime_adaptation(self) -> None:
        adapted = _compact_rewritten_shot_prompt(_adapt_shot_prompt("千夏", self.source))

        self.assertIn("cup both cheeks with open palms", adapted)
        self.assertIn("raise both lower legs behind", adapted)
        self.assertIn("half watermelon with a spoon", adapted)
        self.assertIn("relaxed small smile", adapted)
        self.assertIn("short-sleeve henley shirt", adapted)
        self.assertNotIn("Create one finished image for Template", adapted)

    def test_morning_crystalline_legs_survive_a3_prompt_assembly(self) -> None:
        template = load_template("002_A_3")
        prompt = prompt_for_shot("莫宁", template, template.shots[0])

        self.assertIn(
            "two non-flesh translucent silver-white crystalline synthetic legs",
            prompt,
        )
        self.assertIn(
            "internal cyan-blue diamond facets and tiny star-like specks",
            prompt,
        )
        self.assertIn(
            "never render exposed leg areas as ordinary skin or flesh legs",
            prompt,
        )
        self.assertIn(
            "Template clothing, hosiery, and footwear may cover them normally",
            prompt,
        )

    def test_dan_low_waist_wings_survive_a3_prompt_assembly(self) -> None:
        template = load_template("002_A_3")
        prompt = prompt_for_shot("丹", template, template.shots[0])

        self.assertIn(
            "exactly one pair of low-set wings rooted at the left and right rear waist",
            prompt,
        )
        self.assertIn("wing roots at upper-hip level", prompt)
        self.assertIn("never shoulder-blade or upper-back wings", prompt)
        self.assertIn(
            "wings extending outward from the waist and sweeping downward beside the outer thighs",
            prompt,
        )
        self.assertIn("clear center-back gap", prompt)
        self.assertIn("never to the shoulders, shoulder blades, spine, or upper back", prompt)


if __name__ == "__main__":
    unittest.main()
