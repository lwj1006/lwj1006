import hashlib
import json
import unittest
from pathlib import Path
from fenjue.runtime import batch
from fenjue.modes.original.plans import required_identity_tokens_for
from fenjue.modes.photoset_template.library import load_template, prompt_for_shot

ROOT = Path(__file__).resolve().parents[1]

class GenshinReferenceTests(unittest.TestCase):
    def test_three_references_and_original_provenance(self):
        manifest = json.loads((ROOT / "assets_reference_archive/genshin_three_refs.json").read_text(encoding="utf-8"))
        self.assertEqual(set(manifest), set(batch.GENSHIN_IMPACT_CHARACTERS))
        self.assertEqual(len(list((ROOT / "assets_reference_archive/原神").iterdir())), 12)
        for name, entry in manifest.items():
            with self.subTest(name=name):
                actual = [Path(p).resolve() for p in batch.reference_files_for_character(name)]
                self.assertEqual(actual, [(ROOT / p).resolve() for p in entry["references"]])
                self.assertEqual(len(actual), 3)
                for p, digest in zip(actual, entry["sha256"]):
                    self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), digest)
                self.assertEqual(actual[2].read_bytes(), (ROOT / entry["official_archive"]).read_bytes())

    def test_real_e_prompt_preserves_identity_and_template_outfit(self):
        for name in batch.GENSHIN_IMPACT_CHARACTERS:
            for tid in ("045_A_3", "607_A_3"):
                with self.subTest(name=name, tid=tid):
                    t = load_template(tid)
                    prompt = prompt_for_shot(name, t, t.shots[0])
                    for token in required_identity_tokens_for(name):
                        self.assertIn(token, prompt)
                    self.assertIn("[EXCLUSIVE PHOTOSET GARMENT]", prompt)
                    self.assertIn("[EXPRESSION AND VISIBILITY]", prompt)
                    if name == "哥伦比娅":
                        self.assertIn("fully visible pale lavender-violet half-lidded eyes", prompt)
                        self.assertNotIn("both eyes remain fully concealed", prompt)
