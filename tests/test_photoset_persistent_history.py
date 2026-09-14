import json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from fenjue.modes.photoset_template import mode as m
from fenjue.modes.photoset_template.session import PhotosetSessionError

class PersistentHistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for key,name in [('USED_SHOT_FILE','used_photoset_shots.json'),('USED_TEMPLATE_FILE','used_character_photoset_templates.json')]:
            p=patch.object(m,key,self.root/name);p.start();self.addCleanup(p.stop)
        self.template=SimpleNamespace(template_id='337_A_3',shots=tuple(SimpleNamespace(index=i) for i in (1,2,3)))
    def test_exhausted_shots_never_clear_or_repeat(self):
        history={'337_A_3':[1,2,3]}
        self.assertEqual(m._select_random_unused_shots(self.template,2,history),[])
        self.assertEqual(history,{'337_A_3':[1,2,3]})
    def test_garment_used_by_other_character_is_not_assigned_to_ayaka(self):
        history={'千夏':['337_A_3']}
        result=m._resolve_template_assignments((self.template,),('神里绫华',),history,['337_A_3','338_A_3'])
        self.assertEqual(result,())
        self.assertEqual(history,{'千夏':['337_A_3']})
    def test_legacy_log_garment_is_blocked_for_every_character(self):
        entry={'theme':'西格莉卡: photoset 337_A_3 outfit system (scene-only strong outfit, not cycle-counted)'}
        (self.root/'clothing_theme_usage_log.jsonl').write_text(json.dumps(entry,ensure_ascii=False)+'\n',encoding='utf-8')
        history=m._load_used_templates(['337_A_3'])
        self.assertEqual(m._resolve_template_assignments((self.template,),('神里绫华',),history,['337_A_3']),())
    def test_exhausted_full_library_does_not_clear_character_history(self):
        history={'神里绫华':['337_A_3']}
        self.assertEqual(m._resolve_template_assignments((self.template,),('神里绫华',),history,['337_A_3']),())
        self.assertEqual(history,{'神里绫华':['337_A_3']})
    def test_invalid_history_stops_and_preserves_original_bytes(self):
        for filename,reader in [('used_photoset_shots.json',lambda:m._load_used_shots((self.template,))),('used_character_photoset_templates.json',lambda:m._load_used_templates(['337_A_3']))]:
            for contents in ('{broken','[]','{"x":false}'):
                p=self.root/filename;p.write_text(contents,encoding='utf-8')
                with self.subTest(file=filename,contents=contents):
                    with self.assertRaises(PhotosetSessionError):reader()
                    self.assertEqual(p.read_text(encoding='utf-8'),contents)
    def test_successful_legacy_log_restores_missing_character_template_only(self):
        entry={'time':'2026-07-25T20:10:38','theme':'西格莉卡: photoset 337_A_3 outfit system (scene-only strong outfit, not cycle-counted)'}
        (self.root/'clothing_theme_usage_log.jsonl').write_text(json.dumps(entry,ensure_ascii=False)+'\n',encoding='utf-8')
        h=m._load_used_templates(['337_A_3'])
        self.assertEqual(h,{'西格莉卡':['337_A_3']})
        self.assertFalse(m.USED_SHOT_FILE.exists())
        self.assertEqual(m._load_used_templates(['337_A_3']),h)
    def test_normal_restart_reads_success_without_L(self):
        h={};m._mark_shot_used(self.template,self.template.shots[0],h)
        loaded=m._load_used_shots((self.template,))
        scheduled=m._build_assigned_photoset_schedule((('神里绫华',self.template),),3,loaded)
        self.assertEqual({shot.index for _,_,shot in scheduled},{2,3})
    def test_same_garment_cannot_be_assigned_twice_in_one_batch(self):
        result=m._resolve_template_assignments((self.template,self.template),('千夏','神里绫华'),{},['337_A_3'])
        self.assertEqual(len(result),1)
    def test_normal_restart_keeps_global_garment_lock(self):
        h={};m._mark_template_used('千夏',self.template,h,2)
        loaded=m._load_used_templates(['337_A_3','338_A_3'])
        self.assertEqual(m._resolve_template_assignments((self.template,),('神里绫华',),loaded,['337_A_3','338_A_3']),())
    def test_completed_shot_alone_locks_whole_garment(self):
        m.USED_SHOT_FILE.write_text(json.dumps({'337_A_3':[2]}),encoding='utf-8')
        loaded=m._load_used_templates(['337_A_3','338_A_3'])
        self.assertEqual(m._resolve_template_assignments((self.template,),('神里绫华',),loaded,['337_A_3','338_A_3']),())
        self.assertEqual(m._load_used_shots((self.template,)),{'337_A_3':[2]})
    def test_normal_activation_blocks_used_garment_for_all_or_numeric_counts(self):
        for count in (None, 2):
            batch=SimpleNamespace(ACTIVE_PROMPT_MODE='E',reference_files_for_character=lambda name:[])
            with patch.object(m,'list_template_ids',return_value=['337_A_3','338_A_3']), patch.object(m,'_load_used_templates',return_value={'千夏':['337_A_3']}), patch.object(m,'_choose_templates',return_value=(self.template,)), patch.object(m,'_choose_characters',return_value=('神里绫华',)), patch.object(m,'_choose_shots_per_template',return_value=count), patch.object(m,'save_new_session') as save:
                with self.assertRaises(SystemExit) as stopped:
                    m.activate(batch,['E'])
                self.assertEqual(stopped.exception.code,0)
                save.assert_not_called()
    def test_L_continues_current_garment_despite_global_lock(self):
        schedule=tuple(('神里绫华',self.template,shot) for shot in self.template.shots)
        batch=SimpleNamespace(ACTIVE_PROMPT_MODE='E',reference_files_for_character=lambda name:[])
        with patch.object(m,'list_template_ids',return_value=['337_A_3']), patch.object(m,'_load_used_templates',return_value={'神里绫华':['337_A_3']}), patch.object(m,'load_session',return_value={'mode':'E','next_index':1}), patch.object(m,'_restore_saved_schedule',return_value=schedule), patch.object(m,'_choose_templates') as choose:
            m.activate(batch,['L'])
            choose.assert_not_called()
            self.assertEqual(batch.TOTAL_RUNS,2)
            self.assertEqual([shot.index for _,shot in m._active_shot_schedule],[2,3])
    def test_loading_preserves_temporarily_absent_shots_and_templates(self):
        h={'337_A_3':[1,99],'999_A_3':[2]}
        m.USED_SHOT_FILE.write_text(json.dumps(h),encoding='utf-8')
        self.assertEqual(m._load_used_shots((self.template,)),h)

if __name__=='__main__':unittest.main()
