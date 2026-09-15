import unittest
from dataclasses import replace
from fenjue.modes.photoset_template.library import load_template,prompt_for_shot,_e_source_prompt,_e_coherent_surface_text,_compact
from fenjue.modes.photoset_template.refined import prompt_for_refined_shot
from fenjue.modes.original.plans import required_identity_tokens_for

class EFigureCoherenceTests(unittest.TestCase):
    def test_scene_light_and_character_anatomy_are_unified_without_changing_e2(self):
        for tid in ('116_A_3','361_A_3','607_A_3'):
            t=load_template(tid)
            for name in ('申鹤','青雀','仪玄','菲比','莫宁'):
                for shot in t.shots:
                    with self.subTest(template=tid,character=name,shot=shot.index):
                        e=prompt_for_shot(name,t,shot)
                        self.assertIn('[WHOLE-FIGURE COHERENCE]',e)
                        self.assertIn('head-to-body scale, shoulder width and torso-to-limb proportions',e)
                        self.assertIn('consistent light direction, shadow hue, edge softness',e)
                        self.assertIn('Preserve character-specific nonhuman materials',e)
                        for token in required_identity_tokens_for(name):self.assertIn(token,e)
                        self.assertIn('[EXCLUSIVE PHOTOSET GARMENT]',e)
                        self.assertNotIn('[WHOLE-FIGURE COHERENCE]',prompt_for_refined_shot(name,t,shot))
    def test_render_cleanup_keeps_material_and_direction_evidence(self):
        source='Realistic photo texture. realistic photography. Realistic glass, cotton weave and warm light from upper left.'
        cleaned=_e_coherent_surface_text(source)
        self.assertNotIn('Realistic photo texture',cleaned)
        self.assertNotIn('realistic photography',cleaned)
        self.assertIn('Realistic glass, cotton weave and warm light from upper left.',cleaned)
    def test_e_reads_tail_after_legacy_limit_and_honors_explicit_prompt_override(self):
        t=load_template('089_A_3');shot=t.shots[0]
        self.assertGreater(len(shot.full_ready_prompt),len(shot.ready_prompt))
        self.assertEqual(_e_source_prompt(t,shot),shot.full_ready_prompt)
        changed=replace(shot,ready_prompt='Reproduce this shot. A unique replacement pose.')
        self.assertEqual(_e_source_prompt(t,changed),changed.ready_prompt)
    def test_six_studio_shots_keep_distinct_observed_actions(self):
        t=load_template('116_A_3')
        anchors={1:'hold a narrow brush upright beside the canvas',2:'supports that palette horizontally at chest height',3:'rest the hands loosely together on the nearer upper thigh',4:'brace the open hand on an illustrated magazine',5:'pinch the striped shirt collar beside the shoulder',6:'hands meeting at the bottom edge'}
        for shot in t.shots:
            p=prompt_for_shot('申鹤',t,shot)
            self.assertIn(anchors[shot.index],p)
            self.assertNotIn('Realistic photo texture',p)
            self.assertNotIn('soft volume on top',p)
            self.assertNotIn('or gently bites',p)
            self.assertNotIn('or legs gently crossed',p)
            self.assertLess(len(_e_source_prompt(t,shot)),2500)
    def test_sofa_preserves_clothing_and_pose(self):
        t=load_template('361_A_3')
        for shot in t.shots:
            p=prompt_for_shot('青雀',t,shot)
            self.assertIn('white ribbed spaghetti-strap cropped camisole',p)
            self.assertIn('light gray-blue denim short shorts',p)
            self.assertIn('warm sunlight from upper image-left',p)
        self.assertIn('both knees raised large in the foreground',prompt_for_shot('青雀',t,t.shots[2]))
        self.assertIn('plant the image-right palm on the cushion',prompt_for_shot('青雀',t,t.shots[1]))

if __name__=='__main__':unittest.main()
