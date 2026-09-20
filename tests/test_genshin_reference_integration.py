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
        self.assertGreaterEqual(len(list((ROOT / "assets_reference_archive/原神").iterdir())), len(manifest))
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
                        self.assertIn("fixed pearl-white geometric lattice blindfold covering both eyes", prompt)
                        self.assertNotIn("This is the unmasked version", prompt)

    def test_new_characters_are_selectable_and_keep_star_rail_pool_intact(self):
        for name in ('芙宁娜', '雷电将军', '胡桃', '八重神子', '神里绫华', '宵宫', '甘雨', '申鹤', '荧', '奥黛塔', '刻晴', '夜兰', '珊瑚宫心海'):
            self.assertEqual(batch._parse_character_selection(name), [name])
            index = batch.CHARACTER_SEQUENCE.index(name) + 1
            self.assertEqual(batch._parse_character_selection(str(index)), [name])
            self.assertIn(name, batch.CHARACTER_RANDOM_POOLS['原神'])
            self.assertNotIn(name, batch.HONKAI_STAR_RAIL_CHARACTERS)
        self.assertEqual(batch.HONKAI_STAR_RAIL_CHARACTERS[0], 'Saber')
        self.assertEqual(len(batch.HONKAI_STAR_RAIL_CHARACTERS), 24)

    def test_new_identities_keep_fixed_features_without_locking_clothes(self):
        from fenjue.modes.photoset_template.refined import prompt_for_refined_shot
        from fenjue.modes.original.plans import CHARACTER_PROFILES
        for tid in ('045_A_3', '248_A_3', '532_A_3', '538_A_3'):
            t = load_template(tid)
            for name in ('芙宁娜', '雷电将军'):
                for assembler in (prompt_for_shot, prompt_for_refined_shot):
                    with self.subTest(name=name, tid=tid, mode=assembler.__name__):
                        prompt = assembler(name, t, t.shots[0])
                        self.assertNotRegex(prompt, r'[\u4e00-\u9fff]')
                        for token in required_identity_tokens_for(name):
                            self.assertIn(token, prompt)
                        self.assertIn(CHARACTER_PROFILES[name]['interaction_rule'], prompt)
                        self.assertEqual('[EXCLUSIVE PHOTOSET GARMENT]' in prompt, assembler is prompt_for_shot)
                        if name == '芙宁娜':
                            self.assertIn('Render bareheaded.', prompt)
                            self.assertIn('Do not transfer the royal-blue and white costume palette', prompt)
                        else:
                            self.assertIn('one small dark beauty mole below her right eye', prompt)
                            self.assertIn('Do not force a purple costume or sword gesture', prompt)

    def test_new_character_aliases(self):
        for alias, canonical in [('神里凌华', '神里绫华'), ('萤', '荧'), ('女主角萤', '荧'), ('女主角荧', '荧')]:
            self.assertEqual(batch._parse_character_selection(alias), [canonical])

    def test_eight_new_profiles_in_real_e_and_e2_prompts(self):
        from fenjue.modes.original.plans import CHARACTER_PROFILES
        from fenjue.modes.photoset_template.refined import prompt_for_refined_shot
        features = {
            '胡桃': 'white five-petal flower-shaped pupils',
            '八重神子': 'two outward-drooping pink fox ears',
            '神里绫华': 'exactly one very long high rear ponytail',
            '宵宫': 'red-and-purple floral marking on her left upper arm',
            '甘雨': 'exactly two dark red-black curved horns',
            '申鹤': 'Preserve the natural right-eye fringe occlusion',
            '荧': 'scarf fabric, not long hair',
            '奥黛塔': 'Ignore the dark blue silhouette',
        }
        for name, feature in features.items():
            for tid in ('045_A_3', '244_A_3', '248_A_3', '532_A_3', '538_A_3'):
                t = load_template(tid)
                for assemble in (prompt_for_shot, prompt_for_refined_shot):
                    with self.subTest(name=name, tid=tid, mode=assemble.__name__):
                        prompt = assemble(name, t, t.shots[0])
                        self.assertNotRegex(prompt, r'[\u4e00-\u9fff]')
                        self.assertIn(feature, prompt)
                        self.assertIn(CHARACTER_PROFILES[name]['interaction_rule'], prompt)
                        for token in required_identity_tokens_for(name):
                            self.assertIn(token, prompt)
                        self.assertEqual('[EXCLUSIVE PHOTOSET GARMENT]' in prompt, assemble is prompt_for_shot)

    def test_hatless_characters_and_furina_eyes_in_production(self):
        from fenjue.modes.photoset_template.refined import prompt_for_refined_shot
        for name in ('芙宁娜', '胡桃'):
            for tid in ('045_A_3', '244_A_3', '248_A_3', '532_A_3', '538_A_3'):
                t = load_template(tid)
                for assemble in (prompt_for_shot, prompt_for_refined_shot):
                    p = assemble(name, t, t.shots[0])
                    self.assertIn('Render bareheaded.', p)
                    self.assertIn('overrides general signature-hat preservation', p)
                    self.assertNotIn('Preserve the fixed top hat', p)
                    self.assertNotIn('Preserve the fixed plum-decorated hat', p)
                    if name == '芙宁娜':
                        self.assertIn('light blue iris with a dark blue droplet-shaped pupil', p)
                        self.assertIn('deep blue iris with a light blue droplet-shaped pupil', p)
                        self.assertNotIn('deeper violet-blue', p)
