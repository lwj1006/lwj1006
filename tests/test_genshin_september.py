import unittest
from pathlib import Path
from fenjue.runtime import batch
from fenjue.modes.original.plans import CHARACTER_PROFILES,required_identity_tokens_for
from fenjue.modes.photoset_template.library import load_template,prompt_for_shot
from fenjue.modes.photoset_template.refined import prompt_for_refined_shot

NAMES=('八重神子','申鹤','哥伦比娅','刻晴','夜兰','珊瑚宫心海')
class SeptemberGenshinTests(unittest.TestCase):
    def test_new_characters_selectable_by_name_number_and_alias(self):
        for name in NAMES:
            self.assertEqual(batch._parse_character_selection(name),[name])
            self.assertEqual(batch._parse_character_selection(str(batch.CHARACTER_SEQUENCE.index(name)+1)),[name])
            self.assertEqual(batch.CHARACTER_SEQUENCE.count(name),1)
            self.assertIn(name,batch.GENSHIN_IMPACT_CHARACTERS)
            self.assertNotIn(name,batch.HONKAI_STAR_RAIL_CHARACTERS)
            self.assertEqual(len(batch.reference_files_for_character(name)),3)
            self.assertTrue(batch.reference_files_for_character(name)[1].endswith('_bust.png'))
            for path in batch.reference_files_for_character(name):self.assertTrue(Path(path).is_file())
        self.assertEqual(batch._parse_character_selection('心海'),['珊瑚宫心海'])
        self.assertEqual(batch.HONKAI_STAR_RAIL_CHARACTERS[0],'Saber')
        self.assertEqual(len(batch.HONKAI_STAR_RAIL_CHARACTERS),24)
    def test_identity_and_occlusion_survive_real_production_prompts(self):
        for tid in ('045_A_3','116_A_3','244_A_3','248_A_3','532_A_3','538_A_3','607_A_3'):
            t=load_template(tid)
            for name in NAMES:
                for assemble in (prompt_for_shot,prompt_for_refined_shot):
                    with self.subTest(character=name,template=tid,mode=assemble.__name__):
                        p=assemble(name,t,t.shots[0])
                        for token in required_identity_tokens_for(name):self.assertIn(token,p)
                        self.assertIn(CHARACTER_PROFILES[name]['interaction_rule'],p)
                        self.assertNotIn('tall elongated proportions',p)
                        self.assertNotIn('tall slender proportions and a long neck',p)
                        self.assertNotIn('Do not enforce hidden eyes',p)
                        self.assertEqual('[EXCLUSIVE PHOTOSET GARMENT]' in p,assemble is prompt_for_shot)
                        if name=='申鹤':
                            self.assertIn('diagonal fringe naturally crossing her anatomical right eye',p)
                            self.assertIn('Do not part or shorten the fringe just to expose both eyes',p)
                        if name=='哥伦比娅':
                            self.assertIn('fixed pearl-white geometric lattice blindfold covering both eyes',p)
                            self.assertNotIn('This is the unmasked version',p)
                        if name=='夜兰':self.assertIn('do not add the fur collar or dice pendant',p)
                        if name=='刻晴':self.assertIn('not animal ears or horns',p)
if __name__=='__main__':unittest.main()
