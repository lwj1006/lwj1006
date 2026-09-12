from __future__ import annotations

import unittest
from unittest.mock import patch

from fenjue.modes.original.plans import (
    active_character_profile_variant,
    propagation_profile_for,
    required_identity_tokens_for,
)
from fenjue.modes.photoset_template.library import list_template_ids, load_template, prompt_for_shot
from fenjue.runtime import batch


class CharacterVariantTests(unittest.TestCase):
    def tearDown(self) -> None:
        batch.set_character_variant("哥伦比娅", "blindfold")

    def test_legacy_blindfold_migrates_to_unmasked_three_refs(self) -> None:
        batch.set_character_variant("哥伦比娅", "blindfold")

        references = batch.reference_files_for_character("哥伦比娅")
        tokens = required_identity_tokens_for("哥伦比娅")

        self.assertEqual(len(references), 3)
        self.assertTrue(references[0].endswith("哥伦比娅_front.png"))
        self.assertIsNone(active_character_profile_variant("哥伦比娅"))
        self.assertNotIn("fixed pearl-white translucent geometric blindfold covering both eyes", tokens)

    def test_unmasked_variant_uses_only_bare_eye_references_and_profile(self) -> None:
        batch.set_character_variant("哥伦比娅", "unmasked")

        references = batch.reference_files_for_character("哥伦比娅")
        tokens = required_identity_tokens_for("哥伦比娅")
        profile = propagation_profile_for("哥伦比娅")

        self.assertEqual(len(references), 3)
        self.assertTrue(references[0].endswith("哥伦比娅_front.png"))
        self.assertTrue(references[1].endswith("哥伦比娅_waist.png"))
        self.assertIsNone(active_character_profile_variant("哥伦比娅"))
        self.assertIn("fully visible pale lavender-violet half-lidded eyes", tokens)
        self.assertNotIn("fixed pearl-white translucent geometric blindfold covering both eyes", tokens)
        self.assertIn("Never add the geometric blindfold", profile["interaction_rule"])

    def test_unmasked_variant_survives_real_e_prompt_assembly(self) -> None:
        batch.set_character_variant("哥伦比娅", "unmasked")
        template = load_template(list_template_ids()[0])

        prompt = prompt_for_shot("哥伦比娅", template, template.shots[0])

        self.assertIn("fully visible pale lavender-violet half-lidded eyes", prompt)
        self.assertIn("This is the unmasked version", prompt)
        self.assertNotIn("fixed pearl-white translucent geometric blindfold covering both eyes", prompt)

    def test_saved_variant_selection_does_not_prompt(self) -> None:
        selected = batch.configure_character_variants(
            ["哥伦比娅"],
            arguments=["E"],
            saved_variants={"哥伦比娅": "blindfold"},
        )

        self.assertEqual(selected["哥伦比娅"], "unmasked")

    def test_removed_choice_never_prompts(self) -> None:
        with patch("builtins.input", side_effect=AssertionError("Removed eye option must not prompt")):
            selected = batch.configure_character_variants(["哥伦比娅"], arguments=["E"])

        self.assertEqual(selected["哥伦比娅"], "unmasked")
        self.assertEqual(len(batch.reference_files_for_character("哥伦比娅")), 3)


if __name__ == "__main__":
    unittest.main()
