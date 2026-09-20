import unittest
from unittest.mock import patch
from fenjue.runtime import batch
from fenjue.modes.original.plans import active_character_profile_variant
from fenjue.modes.photoset_template.library import load_template, prompt_for_shot

class CharacterVariantTests(unittest.TestCase):
    def test_current_blindfold_and_legacy_unmasked_use_matching_images_and_profile(self):
        t=load_template('116_A_3')
        for saved in ('blindfold','unmasked'):
            with self.subTest(saved=saved):
                batch.set_character_variant('哥伦比娅',saved)
                self.assertEqual(batch.active_character_variants()['哥伦比娅'],'blindfold')
                refs=batch.reference_files_for_character('哥伦比娅')
                self.assertEqual(len(refs),3)
                self.assertTrue(refs[1].endswith('哥伦比娅_bust.png'))
                self.assertTrue(refs[2].endswith('哥伦比娅_official.png'))
                self.assertIsNone(active_character_profile_variant('哥伦比娅'))
                prompt=prompt_for_shot('哥伦比娅',t,t.shots[0])
                self.assertIn('fixed pearl-white geometric lattice blindfold covering both eyes',prompt)
                self.assertNotIn('This is the unmasked version',prompt)
                self.assertNotIn('Never add the geometric blindfold',prompt)
                self.assertNotIn('fully visible pale lavender-violet half-lidded eyes',prompt)
    def test_startup_and_saved_selection_do_not_reintroduce_unmasked_choice(self):
        for saved in ({},{'哥伦比娅':'unmasked'},{'哥伦比娅':'blindfold'}):
            with patch('builtins.input',side_effect=AssertionError('No appearance menu')):
                selected=batch.configure_character_variants(['哥伦比娅'],arguments=['E'],saved_variants=saved)
            self.assertEqual(selected['哥伦比娅'],'blindfold')

if __name__=='__main__':unittest.main()
