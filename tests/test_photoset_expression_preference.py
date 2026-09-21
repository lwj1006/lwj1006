import unittest
from fenjue.modes.photoset_template.expressions import apply_e_expression_preference, EXPRESSION_POLICY
from fenjue.modes.photoset_template.library import load_template, prompt_for_shot
from fenjue.modes.photoset_template.refined import prompt_for_refined_shot

class ExpressionPreferenceTests(unittest.TestCase):
    def test_real_646_toothy_smile_and_geometry(self):
        t=load_template('646_A_3')
        outputs=[prompt_for_shot('青雀',t,s) for s in t.shots]
        target=next(p for p in outputs if 'loose C beside the cheek' in p)
        self.assertNotIn('broad toothy smile',target)
        self.assertIn('subtle closed-mouth smile',target)
        self.assertIn('other hand under the opposite jaw',target)
        self.assertIn('cream train with an orange stripe',target)

    def test_expression_only_and_negative_preservation(self):
        source='Task.\nLook left with a broad tooth-revealing smile without copying the model. Keep both hands on the cup. Blow a kiss. Lips are puckered. Avoid a forced grin.\n[NEGATIVE]\ntoothy smile, pout, wrong outfit.'
        result=apply_e_expression_preference(source)
        self.assertNotIn('Look left with a broad tooth-revealing smile',result)
        self.assertIn('Look left with a subtle closed-mouth smile without copying the model.',result)
        self.assertIn('Keep both hands on the cup.',result)
        self.assertNotIn('Blow a kiss',result)
        self.assertNotIn('Lips are puckered',result)
        self.assertIn('Avoid a forced grin.',result)
        self.assertIn('toothy smile, pout, wrong outfit.',result)

    def test_variants_and_e2_isolation(self):
        for variant in ('095','095_ADAPTED','095_A_3','623_A_3'):
            t=load_template(variant)
            for shot in t.shots:
                output=prompt_for_shot('青雀',t,shot)
                self.assertIn(EXPRESSION_POLICY,output)
                self.assertNotIn('slightly pouty expression',output)
                self.assertNotIn('small closed-mouth pout',output)
                self.assertNotIn(EXPRESSION_POLICY,prompt_for_refined_shot('青雀',t,shot))

    def test_567_observed_geometry_survives(self):
        t=load_template('567_A_3')
        for shot in t.shots:
            p=prompt_for_shot('青雀',t,shot)
            self.assertIn('[CURRENT SHOT]',p)
            if shot.index==6:
                self.assertIn('denim',p)
                self.assertIn('glass',p)

if __name__=='__main__': unittest.main()
