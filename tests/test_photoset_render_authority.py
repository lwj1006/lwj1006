import unittest
from fenjue.modes.photoset_template.library import load_template,prompt_for_shot,ANIME_FACE_DETAIL,PHOTOSET_RENDER_AUTHORITY
from fenjue.modes.photoset_template.refined import prompt_for_refined_shot
from fenjue.modes.original.plans import required_identity_tokens_for

class RenderAuthorityTests(unittest.TestCase):
    def test_a3_and_e2_include_face_rules_after_final_assembly(self):
        for tid in (139,599,607,622,626,632):
            t=load_template(f'{tid}_A_3')
            for character in ('艾尔妲','菲比','莫宁'):
                for fn in (prompt_for_shot,prompt_for_refined_shot):
                    with self.subTest(template=tid,character=character,mode=fn.__name__):
                        output=fn(character,t,t.shots[0])
                        self.assertIn(ANIME_FACE_DETAIL,output)
                        self.assertIn(PHOTOSET_RENDER_AUTHORITY,output)
                        for token in required_identity_tokens_for(character):
                            self.assertIn(token,output)
                        if character=='菲比':
                            self.assertIn('oversized white wide-brim hat',output)

    def test_recolor_permission_does_not_override_garment_construction(self):
        t=load_template('622_A_3')
        e=prompt_for_shot('艾尔妲',t,t.shots[0])
        e2=prompt_for_refined_shot('艾尔妲',t,t.shots[0])
        self.assertIn('[EXCLUSIVE PHOTOSET GARMENT]',e)
        self.assertIn('Match its color, neckline',e)
        self.assertNotIn('E2 permits changing clothing color only',e)
        self.assertIn('E2 permits changing clothing color only',e2)
        self.assertIn('Do not lock the garment to the photoset reference',e2)
        self.assertNotIn('depth of field',e2.split('[NEGATIVE]')[0])
        self.assertIn('ivory structured corset-style top',e)
        for output in (e,e2):
            self.assertIn('visible vertical seams',output)
            self.assertIn('tiered tulle skirt',output)

if __name__=='__main__':
    unittest.main()
