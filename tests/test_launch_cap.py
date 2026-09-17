import unittest
from collections import defaultdict
from types import FunctionType,SimpleNamespace
from unittest.mock import Mock
from pathlib import Path
from fenjue.runtime import batch

class LaunchCapTests(unittest.TestCase):
    def run_fake(self,args=(),wait_effect=None,runs=1385):
        env=dict(batch.main.__globals__)
        for name in batch.main.__code__.co_names:
            if name in env and callable(env[name]) and name!='GenerationLimitReached':env[name]=Mock()
        record=defaultdict(lambda:'test')
        env.update(TOTAL_RUNS=runs,MAX_RUNS_PER_LAUNCH=80,sys=SimpleNamespace(argv=['test',*args]),time=Mock(),pyautogui=SimpleNamespace(),CALIBRATION_FILE=Mock(),ART_DIRECTION_PLANS=[],LAST_RUNTIME_CONFIG_REVISION='test')
        returns={'startup_character_selection':['test'],'startup_scene_selection':None,'startup_clothing_selection':None,'startup_start_time_selection':None,'load_used_character_clothing_themes':{},'load_used_character_art_plans':{},'load_used_character_batch':[],'reference_files_for_character':['ref'],'choose_character_plan_and_action':(record,record),'propagation_profile_for':record,'required_identity_tokens_for':[],'viewer_distance_for':'test','choose_shot_scale':record,'choose_compatible_clothing_theme':'test','outfit_with_optional_black_hosiery':('test',False),'choose_composition_plan':record,'prompt_template_name':'test','prompt_for_art_direction':'test','collect_cooldown_tags':[]}
        for name,value in returns.items():env[name]=Mock(return_value=value)
        env['resolve_run_character']=Mock(side_effect=lambda name,n:name)
        env['with_image_prompt_prefix']=Mock(side_effect=lambda p:p)
        env['wait_for_generation']=Mock(side_effect=wait_effect)
        env['print']=Mock()
        FunctionType(batch.main.__code__,env)()
        return env
    def test_long_queue_stops_at_80_successes_and_saves_only_80(self):
        e=self.run_fake()
        self.assertEqual(e['send_prompt'].call_count,80)
        self.assertEqual(e['record_completed_run'].call_count,80)
        self.assertEqual(e['record_run_session_progress'].call_args.args,(80,))
    def test_command_line_cannot_override_hard_limit(self):
        self.assertEqual(self.run_fake(['--runs','9999'])['send_prompt'].call_count,80)
    def test_short_run_and_once_keep_their_limits(self):
        self.assertEqual(self.run_fake(runs=3)['send_prompt'].call_count,3)
        self.assertEqual(self.run_fake(['--once'])['send_prompt'].call_count,1)
    def test_retries_also_stop_at_80_sends_without_false_success(self):
        detection=SimpleNamespace(resume_at=None,screenshot_path=Path('unused.png'))
        e=self.run_fake(wait_effect=batch.GenerationLimitReached(detection))
        self.assertEqual(e['send_prompt'].call_count,80)
        self.assertEqual(e['recover_after_generation_limit'].call_count,79)
        e['record_completed_run'].assert_not_called()
        e['record_run_session_progress'].assert_not_called()

if __name__=='__main__':unittest.main()
