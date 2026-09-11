from pathlib import Path
import hashlib
import json
import unittest
from fenjue.runtime import batch
from fenjue.modes.original.plans import required_identity_tokens_for
from fenjue.modes.photoset_template.library import load_template, prompt_for_shot

class ZzzFrontReferenceTests(unittest.TestCase):
    def test_added_fronts_preserve_original_pair_and_production_identity(self):
        root = batch.PROJECT_DIR
        manifest = json.loads((root / 'assets_reference_archive/zzz_front_additions.json').read_text(encoding='utf-8'))
        self.assertEqual(len(manifest), 13)
        sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        template = load_template('045_A_3')
        for name, item in manifest.items():
            with self.subTest(name=name):
                refs = [Path(p) for p in batch.reference_files_for_character(name)]
                self.assertEqual(refs, [root / item['generated']] + [root / p for p in item['originals']])
                self.assertEqual(sha(refs[0]), item['generated_sha256'])
                self.assertEqual([sha(p) for p in refs[1:]], item['original_sha256'])
                text = prompt_for_shot(name, template, template.shots[0])
                for token in required_identity_tokens_for(name):
                    self.assertIn(token, text)
                self.assertIn('[EXCLUSIVE PHOTOSET GARMENT]', text)
        self.assertTrue(all(len(batch.reference_files_for_character(n)) >= 3 for n in batch.ZENLESS_ZONE_ZERO_CHARACTERS))
