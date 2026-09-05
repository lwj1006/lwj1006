from pathlib import Path
import unittest
from unittest.mock import patch

from fenjue.runtime import batch
from fenjue.modes.original.plans import required_identity_tokens_for
from fenjue.modes.photoset_template.library import load_template, prompt_for_shot
from fenjue.modes.photoset_template.refined import prompt_for_refined_shot


STAR_RAIL_NAMES = ('Saber', '阿格莱雅', '火花', '花火', '青雀', '昔涟', '大丽花', '大黑塔',
                   '知更鸟·晴歌', '知更鸟', '停云', '忘归人', '符玄', '流萤', '爻光', '遐蝶',
                   '阮·梅', '卡芙卡', '姬子', '灵砂', '绯英', '银狼', '银狼LV.999', '风堇')


class StarRailIntegrationTests(unittest.TestCase):
    def test_all_current_images_are_reachable_exactly_once(self):
        self.assertEqual(list(STAR_RAIL_NAMES), batch.HONKAI_STAR_RAIL_CHARACTERS)
        paths = [Path(p) for name in STAR_RAIL_NAMES for p in batch.reference_files_for_character(name)]
        self.assertEqual(len(paths), 54)
        self.assertEqual(len(paths), len(set(paths)))
        self.assertTrue(all(p.is_file() for p in paths))
        self.assertEqual(set(paths), set((batch.PROJECT_DIR / 'assets' / '星铁').iterdir()))
        self.assertFalse(set(STAR_RAIL_NAMES) & set(batch.GENSHIN_IMPACT_CHARACTERS))

    def test_launcher_names_numbers_and_random_aliases(self):
        first = batch.CHARACTER_SEQUENCE.index('Saber') + 1
        self.assertEqual(batch._parse_character_selection(f'{first}-{first + 23}'), list(STAR_RAIL_NAMES))
        self.assertEqual(batch._parse_character_selection('Saber,忘归人,银狼LV.999'), ['Saber', '忘归人', '银狼LV.999'])
        self.assertEqual(batch._parse_character_selection('阮梅,阮•梅,只更鸟晴歌'), ['阮·梅', '知更鸟·晴歌'])
        for alias in ('H', 'hsr', 'starrail', '星铁', '星铁随机', '崩坏星穹铁道'):
            with self.subTest(alias=alias), patch.object(batch, '_select_character_random_pool') as select:
                self.assertIsNone(batch._parse_character_selection(alias))
                select.assert_called_once_with('星铁')

    def test_incompatible_forms_do_not_share_references(self):
        def files(name):
            return [Path(p).name for p in batch.reference_files_for_character(name)]
        self.assertEqual(files('停云'), ['停云2.png'])
        self.assertEqual(files('忘归人'), ['停云1.png', '停云3.png'])
        self.assertEqual(files('银狼'), ['银狼1.png'])
        self.assertEqual(files('银狼LV.999'), ['银狼2.png', '银狼3.png'])
        for first, second in [('火花', '花火'), ('知更鸟', '知更鸟·晴歌')]:
            self.assertFalse(set(files(first)) & set(files(second)))

    def test_identity_survives_every_shot_in_representative_e_and_e2_templates(self):
        for tid in ('002', '045', '244', '248', '532', '538'):
            template = load_template(tid + '_A_3')
            for shot in template.shots:
                for name in STAR_RAIL_NAMES:
                    for assembler in (prompt_for_shot, prompt_for_refined_shot):
                        with self.subTest(template=tid, shot=shot, name=name, mode=assembler.__name__):
                            text = assembler(name, template, shot)
                            for token in required_identity_tokens_for(name):
                                self.assertIn(token, text)
                            self.assertNotRegex(text, r'[\u4e00-\u9fff]')
                            self.assertEqual('[JAPANESE ANIME DRAWING DIRECTION]' in text, assembler is prompt_for_shot)

    def test_fixed_hats_species_traits_and_companions_remain_distinct(self):
        expected = {
            '大丽花': ['large white wide-brim hat', 'claw glove'],
            '大黑塔': ['pointed witch hat', 'ordinary human joints'],
            '风堇': ['small burgundy cap', 'not her body wings'],
            '菲比': ['oversized white wide-brim hat'],
            '停云': ['one large fluffy brown fox tail', 'white foxes are separate companions'],
            '忘归人': ['multiple large pale pink-white fluffy fox tails'],
            '知更鸟': ['wings behind the ears', 'makeup artists'],
            '遐蝶': ['pointed ears', 'dragon and butterflies are separate creatures'],
            '灵砂': ['red coloration on the hands fading along the forearms'],
            '绯英': ['two long pale pink rabbit-like ear structures', 'its tail'],
            '流萤': ['separate suit depiction'],
        }
        template = load_template('045_A_3')
        for name, snippets in expected.items():
            for assembler in (prompt_for_shot, prompt_for_refined_shot):
                text = assembler(name, template, template.shots[0])
                for snippet in snippets:
                    with self.subTest(name=name, snippet=snippet, mode=assembler.__name__):
                        self.assertIn(snippet, text)


if __name__ == '__main__':
    unittest.main()
