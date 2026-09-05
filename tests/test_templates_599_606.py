"""Guard inspected shot evidence against loader clipping and E/E2 sanitization loss."""
import re
import unittest

from fenjue.modes.original.plans import required_identity_tokens_for
from fenjue.modes.photoset_template.descriptions import TEMPLATE_DESCRIPTIONS
from fenjue.modes.photoset_template.library import load_template, list_template_ids, prompt_for_shot
from fenjue.modes.photoset_template.refined import prompt_for_refined_shot, _neutralize_outfit_color_locks

COUNTS = dict(zip(range(599, 607), (7, 7, 5, 2, 5, 8, 9, 4)))
FIELDS = ('Frame', 'Body', 'Hands', 'Expression', 'Outfit', 'Scene', 'Light')


def normalized(text):
    return re.sub(r'[^a-z0-9]+', ' ', text.lower()).strip()


class NewPhotosetPrecisionTests(unittest.TestCase):
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
                for character in ('千夏', '菲比', '莫宁'):
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

    def test_specific_hand_contacts_gaze_and_orientation_stay_distinct(self):
        cases = {
            (599, 1): ('slim metal fork', 'spread palm bears weight'),
            (600, 3): ('open book',),
            (601, 5): ('Horizontal chest-up', 'Close both eyes'),
            (602, 2): ('Both hands are outside the frame', 'lower-left edge'),
            (603, 3): ('right palm plants at lower left', 'left palm at lower center'),
            (604, 2): ('right overall strap has slipped', 'forearm passes above the crown'),
            (604, 3): ('Look upward to the right',),
            (604, 6): ('Look directly toward the viewer',),
            (605, 2): ('between the index and middle fingertips', 'between the thumb and index finger'),
            (605, 5): ('Lay both hands flat',),
            (605, 7): ('both hands into separate loose fists',),
            (605, 8): ('Horizontal table-level close portrait',),
            (606, 4): ('Look down-left toward the peony', 'Both hands and forearms are outside'),
        }
        for (tid, n), facts in cases.items():
            template = load_template(f'{tid}_A_3')
            for assembler in (prompt_for_shot, prompt_for_refined_shot):
                output = assembler('菲比', template, template.shots[n - 1])
                for fact in facts:
                    with self.subTest(template=tid, shot=n, mode=assembler.__name__, fact=fact):
                        self.assertIn(fact.lower(), output.lower())

    def test_identity_fixed_hat_and_separate_mode_style_rules(self):
        for tid in COUNTS:
            template = load_template(f'{tid}_A_3')
            for character in ('千夏', '菲比', '莫宁'):
                for assembler in (prompt_for_shot, prompt_for_refined_shot):
                    output = assembler(character, template, template.shots[0])
                    for token in required_identity_tokens_for(character):
                        self.assertIn(token, output)
                    if character == '菲比':
                        self.assertIn('oversized white wide-brim hat', output)
                    self.assertEqual('[JAPANESE ANIME DRAWING DIRECTION]' in output, assembler is prompt_for_shot)
                    self.assertEqual('Do not lock the garment to the photoset reference' in output, assembler is prompt_for_refined_shot)


if __name__ == '__main__':
    unittest.main()
