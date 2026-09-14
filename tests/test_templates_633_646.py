"""Guard inspected shot evidence against loader clipping and E/E2 sanitization loss."""
import hashlib
import json
import re
import unittest

from fenjue.modes.original.plans import required_identity_tokens_for
from fenjue.modes.photoset_template.descriptions import TEMPLATE_DESCRIPTIONS
from fenjue.modes.photoset_template.library import load_template, list_template_ids, prompt_for_shot
from fenjue.modes.photoset_template.refined import prompt_for_refined_shot, _neutralize_outfit_color_locks

COUNTS = {633: 7, 634: 5, 635: 4, 636: 4, 637: 7, 638: 6, 639: 7, 640: 7, 641: 4, 642: 4, 643: 6, 644: 8, 645: 8, 646: 8}
FIELDS = ('Frame', 'Body', 'Hands', 'Expression', 'Outfit', 'Scene', 'Light')


def normalized(text):
    return re.sub(r'[^a-z0-9]+', ' ', text.lower()).strip()


class Batch633PrecisionTests(unittest.TestCase):
    def test_original_image_bytes_and_source_order(self):
        root = load_template('633_A_3').markdown_path.parent.parent
        manifest = json.loads((root / 'import_633_646.json').read_text(encoding='utf-8'))
        self.assertEqual(set(manifest), {str(tid) for tid in COUNTS})
        for tid, count in COUNTS.items():
            entries = manifest[str(tid)]
            self.assertEqual(len(entries), count)
            self.assertEqual([e['source_number'] for e in entries], sorted(e['source_number'] for e in entries))
            for n, entry in enumerate(entries, 1):
                self.assertEqual(entry['image'], f'{n}.jpeg')
                data = (root / str(tid) / entry['image']).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry['sha256'])
                self.assertTrue(data.startswith(bytes.fromhex('ffd8ff')))

    def test_inventory_order_menu_and_untruncated_ready_blocks(self):
        available = list_template_ids()
        for tid, count in COUNTS.items():
            template = load_template(f'{tid}_A_3')
            self.assertIn(f'{tid}_A_3', available)
            self.assertIn(str(tid), TEMPLATE_DESCRIPTIONS)
            self.assertEqual(len(template.shots), count)
            markdown = template.markdown_path.read_text(encoding='utf-8')
            raw_blocks = re.findall(r'## 2\. Ready-to-Use Prompt\s*\n(.*?)\n## 3\. Negative Prompt', markdown, re.S)
            self.assertEqual(len(raw_blocks), count)
            for n, (shot, raw) in enumerate(zip(template.shots, raw_blocks), 1):
                with self.subTest(template=tid, shot=n):
                    self.assertEqual(shot.index, n)
                    self.assertEqual(shot.reference_image.name, f'{n}.jpeg')
                    self.assertTrue(shot.reference_image.is_file())
                    self.assertLessEqual(len(raw.strip()), 3500)
                    self.assertEqual(' '.join(raw.split()), ' '.join(shot.ready_prompt.split()))

    def test_every_evidence_sentence_survives_real_e_and_e2_assembly(self):
        for tid in COUNTS:
            template = load_template(f'{tid}_A_3')
            for shot in template.shots:
                evidence = shot.section_text.split('## 2. Ready-to-Use Prompt')[0]
                for character in ('千夏', '菲比', '莫宁', '芙宁娜'):
                    for assembler in (prompt_for_shot, prompt_for_refined_shot):
                        output = assembler(character, template, shot)
                        self.assertNotRegex(output, r'[\u4e00-\u9fff]')
                        for field in FIELDS:
                            match = re.search(rf'(?:^|\n){field}: (.*?)(?=\n\n|$)', evidence, re.S)
                            self.assertIsNotNone(match, (tid, shot.index, field))
                            for sentence in re.split(r'(?<=[.!?])\s+', match.group(1)):
                                # E2 intentionally recolors clothing and rewrites punctuation.
                                expected = _neutralize_outfit_color_locks(sentence) if assembler is prompt_for_refined_shot else sentence
                                with self.subTest(template=tid, shot=shot.index, character=character, mode=assembler.__name__, field=field, sentence=sentence):
                                    self.assertIn(normalized(expected), normalized(output))

    def test_all_new_templates_are_selectable_by_theme(self):
        from fenjue.modes.photoset_template.descriptions import TEMPLATE_THEME_DEFINITIONS, template_ids_for_theme
        available = list_template_ids()
        themed = set().union(*(set(template_ids_for_theme(code, available)) for code in TEMPLATE_THEME_DEFINITIONS))
        for tid in COUNTS:
            self.assertIn(f'{tid}_A_3', themed)

    def test_identity_fixed_hat_and_separate_mode_style_rules(self):
        for tid in COUNTS:
            template = load_template(f'{tid}_A_3')
            for character in ('千夏', '菲比', '莫宁', '芙宁娜'):
                for assembler in (prompt_for_shot, prompt_for_refined_shot):
                    output = assembler(character, template, template.shots[0])
                    for token in required_identity_tokens_for(character):
                        self.assertIn(token, output)
                    if character == '菲比':
                        self.assertIn('oversized white wide-brim hat', output)
                    if character == '芙宁娜':
                        self.assertIn('Render bareheaded.', output)
                    self.assertEqual('[EXCLUSIVE PHOTOSET GARMENT]' in output, assembler is prompt_for_shot)
                    self.assertEqual('Do not lock the garment to the photoset reference' in output, assembler is prompt_for_refined_shot)


if __name__ == '__main__':
    unittest.main()
