from pathlib import Path
import unittest

from fenjue.runtime import batch
from fenjue.modes.original.plans import CHARACTER_PROFILES, KNOWN_CHARACTER_NAMES, required_identity_tokens_for
from fenjue.modes.photoset_template.library import load_template, prompt_for_shot
from fenjue.modes.photoset_template.refined import prompt_for_refined_shot


ZZZ_ADDITIONS = ('希希芙', '德蕾琪娜·挽昼', '林德薇恩', '艾尔妲')
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

    def test_three_related_characters_have_separate_complete_reference_sets(self):
        expected = {
            '德蕾琪娜·挽昼': ['德蕾琪娜·挽昼1.png', '德蕾琪娜·挽昼2.png'],
            '林德薇恩': ['林德薇恩1.png', '林德薇恩2.png', '林德薇恩3.png'],
            '艾尔妲': ['艾尔妲1.png', '艾尔妲2.png', '艾尔妲3.png'],
        }
        all_paths = []
        for name, names in expected.items():
            paths = list(map(Path, batch.reference_files_for_character(name)))
            self.assertEqual([p.name for p in paths], names)
            self.assertTrue(all(p.is_file() and p.parent.name == '绝区零' for p in paths))
            self.assertIn(name, batch.ZENLESS_ZONE_ZERO_CHARACTERS)
            self.assertNotIn(name, batch.WUTHERING_WAVES_CHARACTERS)
            self.assertEqual(batch._parse_character_selection(name), [name])
            all_paths.extend(paths)
        self.assertEqual(len(all_paths), len(set(all_paths)))
        self.assertFalse((batch.PROJECT_DIR / 'assets' / '绝区零' / '德蕾琪娜·挽昼2.jpeg').exists())
        self.assertNotEqual(batch._parse_character_selection('艾尔妲'), batch._parse_character_selection('艾尔黛拉'))

    def test_three_reference_profiles_remain_distinct_in_production(self):
        expected = {
            '德蕾琪娜·挽昼': ('compact human proportions', 'fringe covering her left eye', 'gold rings beside the neck'),
            '林德薇恩': ('high twin tails rooted separately', 'four-petal front plates and hot-pink diamond centers'),
            '艾尔妲': ('tall mature feminine human proportions', 'loose silver-white hair falling from the rear crown', 'four-point star drop earrings'),
        }
        for tid in ('045_A_3', '248_A_3', '532_A_3', '599_A_3', '604_A_3', '606_A_3'):
            template = load_template(tid)
            for shot in template.shots:
                for name, facts in expected.items():
                    for assembler in (prompt_for_shot, prompt_for_refined_shot):
                        with self.subTest(template=tid, shot=shot.index, character=name, mode=assembler.__name__):
                            result = assembler(name, template, shot)
                            for fact in facts + tuple(required_identity_tokens_for(name)):
                                self.assertIn(fact, result)
                            self.assertNotRegex(result, r'[\u4e00-\u9fff]')
                            self.assertNotIn('The four-panel reference shows', result)


if __name__ == '__main__':
    unittest.main()
