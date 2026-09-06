from pathlib import Path
import unittest

from fenjue.runtime import batch
from fenjue.modes.original.plans import CHARACTER_PROFILES, KNOWN_CHARACTER_NAMES, required_identity_tokens_for
from fenjue.modes.photoset_template.library import load_template, prompt_for_shot
from fenjue.modes.photoset_template.refined import prompt_for_refined_shot


ZZZ_ADDITIONS = ('希希芙', '德蕾琪娜·挽昼', '林德薇恩')
WW_ADDITIONS = ('奥古斯塔', '清宵', '折枝', '漂泊者', '弗洛洛', '穗穗')
REPLACEMENTS = ('千咲', '琳奈', '绯雪')


class CharacterReferenceIntegrationTests(unittest.TestCase):
    def test_menu_profiles_and_game_pools_agree(self):
        sequence = batch.CHARACTER_SEQUENCE
        self.assertEqual(len(sequence), len(set(sequence)))
        self.assertEqual(set(sequence), set(batch.CHARACTER_REFERENCES))
        self.assertEqual(set(sequence), set(KNOWN_CHARACTER_NAMES))
        self.assertTrue(set(sequence) <= set(CHARACTER_PROFILES))
        pools = [batch.ZENLESS_ZONE_ZERO_CHARACTERS, batch.WUTHERING_WAVES_CHARACTERS,
                 batch.ENDFIELD_CHARACTERS, batch.GENSHIN_IMPACT_CHARACTERS,
                 batch.HONKAI_STAR_RAIL_CHARACTERS]
        self.assertEqual(sequence, sum(pools, []))
        for group, expected, directory in ((pools[0], ZZZ_ADDITIONS, '绝区零'),
                                           (pools[1], WW_ADDITIONS + REPLACEMENTS, '鸣潮')):
            for name in expected:
                with self.subTest(character=name):
                    self.assertIn(name, group)
                    self.assertTrue(all(Path(p).parent.name == directory for p in batch.CHARACTER_REFERENCES[name]))

    def test_replacement_refs_use_only_the_new_sets(self):
        for name, expected in {'千咲': ['千咲1.png', '千咲2.png', '千咲3.jpg'],
                               '琳奈': ['琳奈1.jpg', '琳奈2.jpg'],
                               '绯雪': ['绯雪1.png', '绯雪2.png']}.items():
            self.assertEqual([Path(p).name for p in batch.reference_files_for_character(name)], expected)
        for name in ZZZ_ADDITIONS + WW_ADDITIONS + REPLACEMENTS:
            for path in batch.reference_files_for_character(name):
                self.assertTrue(Path(path).is_file(), path)
        self.assertEqual(Path(batch.reference_files_for_character('漂泊者')[0]).name, '漂泊者2.png')

    def test_new_identity_evidence_reaches_both_production_modes(self):
        # Ordinary, hand/prop, close-up and complex framing templates.
        for tid in ('002_A_3', '045_A_3', '350_A_3', '538_A_3'):
            template = load_template(tid)
            for name in ZZZ_ADDITIONS + WW_ADDITIONS + REPLACEMENTS:
                for assembler in (prompt_for_shot, prompt_for_refined_shot):
                    with self.subTest(template=tid, character=name, mode=assembler.__name__):
                        result = assembler(name, template, template.shots[0])
                        for token in required_identity_tokens_for(name):
                            self.assertIn(token, result)
                        self.assertIn(CHARACTER_PROFILES[name]['interaction_rule'], result)
                        self.assertNotRegex(result, r'[\u4e00-\u9fff]')
                        self.assertEqual('[JAPANESE ANIME DRAWING DIRECTION]' in result,
                                         assembler is prompt_for_shot)

    def test_critical_visual_distinctions_survive(self):
        template = load_template('350_A_3')
        def prompt(name):
            return prompt_for_shot(name, template, template.shots[0])
        self.assertIn('her right eye amber gold and her left eye sapphire blue', prompt('林德薇恩'))
        self.assertIn('white snake with its own head and green bow is a separate companion', prompt('希希芙'))
        self.assertIn('huge white brush tuft and painted crane are props', prompt('折枝'))
        self.assertIn('paired dark faceted triangular hair ornaments', prompt('德蕾琪娜·挽昼'))
        self.assertIn('turquoise elongated four-point star earrings', prompt('琳奈'))
        self.assertIn('white blossom ornament beside the topknot', prompt('绯雪'))
        self.assertIn('oversized white wide-brim hat', prompt('菲比'))

    def test_corrected_game_classification_stays_stable(self):
        self.assertIn('林德薇恩', batch.ZENLESS_ZONE_ZERO_CHARACTERS)
        self.assertNotIn('林德薇恩', batch.WUTHERING_WAVES_CHARACTERS)
        self.assertTrue(all(Path(path).parent.name == '绝区零'
                            for path in batch.reference_files_for_character('林德薇恩')))
        self.assertIn('卡芙卡', batch.HONKAI_STAR_RAIL_CHARACTERS)
        self.assertNotIn('卡芙卡', batch.GENSHIN_IMPACT_CHARACTERS)
        self.assertTrue(all(Path(path).parent.name == '星铁'
                            for path in batch.reference_files_for_character('卡芙卡')))


if __name__ == '__main__':
    unittest.main()
