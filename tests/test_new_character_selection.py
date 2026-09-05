import contextlib
import io
import unittest
from unittest.mock import patch

from fenjue.runtime import batch
from fenjue.modes.photoset_template import mode
from fenjue.modes.photoset_refined import mode as refined_mode


class NewCharacterSelectionTests(unittest.TestCase):
    def test_every_menu_entry_selects_by_name_and_displayed_number(self):
        for number, name in enumerate(batch.CHARACTER_SEQUENCE, 1):
            for choice in (name, str(number)):
                with self.subTest(character=name, choice=choice):
                    with patch('builtins.input', return_value=choice) as read, contextlib.redirect_stdout(io.StringIO()) as output:
                        self.assertEqual(batch.prompt_character_selection(), [name])
                    read.assert_called_once()
                    self.assertIn(f'{number}. {name}', output.getvalue())
                    with patch.object(batch, 'noninteractive_selection_enabled', return_value=False), patch('builtins.input', return_value=choice) as read, contextlib.redirect_stdout(io.StringIO()) as output:
                        self.assertEqual(mode._choose_characters([], batch), (name,))
                    read.assert_called_once()
                    self.assertIn(f'{number:>2}={name}', output.getvalue())
                    self.assertEqual(mode._choose_characters(['--characters', choice], batch), (name,))
                    batch.validate_reference_files_for_characters([name])

    def test_wanzhou_aliases_and_mixed_new_characters(self):
        for alias in ('挽昼', '德蕾琪娜挽昼', '德蕾琪娜•挽昼', '德蕾琪娜·挽昼'):
            self.assertEqual(batch._parse_character_selection(alias), ['德蕾琪娜·挽昼'])
        self.assertEqual(mode._choose_characters(['--characters', '希希芙，挽昼，奥古斯塔，风堇'], batch),
                         ('希希芙', '德蕾琪娜·挽昼', '奥古斯塔', '风堇'))

    def test_refined_entry_uses_same_character_selector_and_star_rail_pool(self):
        self.assertIs(refined_mode.base_mode, mode)
        with patch.object(batch, '_active_character_random_pool_name', '全部'), patch('builtins.input', return_value='H'), patch.object(batch, 'noninteractive_selection_enabled', return_value=False), contextlib.redirect_stdout(io.StringIO()) as output:
            selected = refined_mode.base_mode._choose_characters([], batch)
            self.assertEqual(set(selected), set(batch.HONKAI_STAR_RAIL_CHARACTERS))
            self.assertEqual(len(selected), 24)
            self.assertIn('H = 星铁随机', output.getvalue())


if __name__ == '__main__':
    unittest.main()
