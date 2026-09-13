import unittest
from unittest.mock import patch
from fenjue.runtime import batch
from fenjue.modes.photoset_template import mode
from fenjue.modes.photoset_template.library import load_template, prompt_for_shot

class CombinedPoolTests(unittest.TestCase):
    def setUp(self):
        self.old = batch.active_character_random_pool_name()
    def tearDown(self):
        batch._select_character_random_pool(self.old)
    def test_game_combinations(self):
        expected = set(batch.GENSHIN_IMPACT_CHARACTERS + batch.ZENLESS_ZONE_ZERO_CHARACTERS)
        for value in ('绝区零+原神', 'Z+G', '原神全人物 + 绝区零 随机', '原神，绝区零', '原神 绝区零'):
            self.assertIsNone(batch._parse_character_selection(value))
            self.assertEqual(set(batch.active_character_random_pool()), expected)
    def test_game_plus_named_character_and_duplicates(self):
        for value in ('原神全人物 + 星间雅 随机', '原神+星见雅', '原神+胡桃+星见雅+星见雅随机'):
            self.assertIsNone(batch._parse_character_selection(value))
            pool=batch.active_character_random_pool()
            self.assertEqual(set(pool), set(batch.GENSHIN_IMPACT_CHARACTERS + ['星见雅']))
            self.assertEqual(len(pool),len(set(pool)))
    def test_named_random_and_fixed_lists(self):
        self.assertEqual(batch._parse_character_selection('胡桃,星间雅'), ['胡桃','星见雅'])
        self.assertIsNone(batch._parse_character_selection('胡桃+星间雅 随机'))
        self.assertEqual(batch.active_character_random_pool(), ['胡桃','星见雅'])
        self.assertIsNone(batch._parse_character_selection('G'))
        self.assertEqual(batch.active_character_random_pool(),batch.GENSHIN_IMPACT_CHARACTERS)
    def test_invalid_input_keeps_previous_pool(self):
        batch._parse_character_selection('原神+星见雅')
        before=batch.active_character_random_pool_name()
        for value in ('原神+不存在', '原神+1', '胡桃+不存在随机'):
            with self.assertRaises(ValueError):batch._parse_character_selection(value)
            self.assertEqual(batch.active_character_random_pool_name(),before)
    def test_real_e_startup_uses_union(self):
        selected=mode._choose_characters(['--characters','原神全人物 + 星间雅 随机'],batch)
        self.assertEqual(set(selected),set(batch.GENSHIN_IMPACT_CHARACTERS+['星见雅']))
        self.assertEqual(len(selected),len(set(selected)))
    def test_rotation_only_resets_selected_union(self):
        batch._parse_character_selection('原神+星见雅')
        pool=batch.active_character_random_pool()
        outside=next(n for n in batch.CHARACTER_SEQUENCE if n not in pool)
        used=pool[:-1]+[outside]
        with patch.object(batch,'save_used_character_batch') as save:
            self.assertEqual(batch.choose_character_batch(used),[pool[-1]])
            save.assert_not_called()
            used.append(pool[-1])
            chosen=batch.choose_character_batch(used)
            self.assertTrue(set(chosen)<=set(pool))
            self.assertEqual(used,[outside])
            save.assert_called_once_with([outside])
    def test_skirk_final_prompt_has_no_conflicting_old_adaptation(self):
        t=load_template('045_A_3');p=prompt_for_shot('丝柯克',t,t.shots[0])
        self.assertNotIn('one large high rear ponytail',p)
        self.assertNotIn('crystalline right arm',p)
        self.assertNotIn('mature athletic proportions',p)
        self.assertIn('crystalline left arm',p)
        self.assertIn('without exaggerating the bust',p)
        self.assertIn('[EXCLUSIVE PHOTOSET GARMENT]',p)
