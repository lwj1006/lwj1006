# 辟夊ｯ謠千､ｺ隸肴ｨ｡蠑丞､肴衍 Feedback

譌･譛滂ｼ・026-06-08

## 扈楢ｮｺ

譁ｰ蜉蜈･逧・A/B 蜈･蜿｣謨ｴ菴灘庄逕ｨ縲・ 讓｡蠑丈ｿ晄戟蜴溷・遞ｳ螳壽ｨ｡譚ｿ・沓 讓｡蠑丈ｼ壼惠霑占｡梧慮蛻・困蛻ｰ譁ｰ逧・悟惻譎ｯ / 鞫・ｽｱ蟶・/ 莠ｺ迚ｩ / 譛崎｣・榊屁蝮玲槍蠖ｱ蟶域ｨ｡譚ｿ・梧ｲ｡譛臥峩謗･謾ｹ蜉ｨ蜴溷星蜉ｨ蜈･蜿｣縲・
逶ｮ蜑榊ｻｺ隶ｮ・壼庄莉･扈ｧ扈ｭ菫晉蕗 B 讓｡蠑丈ｽ應ｸｺ螳樣ｪ悟・蜿｣・御ｽ・ｸ崎ｦ∵･逹謚雁ｮ・崛謐｢謌宣ｻ倩ｮ､逕滉ｺｧ讓｡譚ｿ縲・ 讓｡蠑冗ｻ捺桷譏ｯ蟇ｹ逧・ｼ悟ｷｲ菫ｮ豁｣隨ｬ荳霓ｮ蜿醍鴫逧・ｸｻ隕∬ｯｯ蟇ｼ謗ｪ霎橸ｼ帛黄菴吩ｸｻ隕∬ｧょｯ溽せ譏ｯ謠千､ｺ隸埼柄蠎ｦ蛛城柄・瑚ｷ大崟蜷朱怙隕∫恚譛崎｣・揀驥榊柱譫・崟譚・㍾譏ｯ蜷ｦ陲ｫ遞驥翫・
## 蟾ｲ閾ｪ豬矩｡ｹ逶ｮ

1. 譁ｰ譁・ｻｶ隸ｭ豕墓｣譟･騾夊ｿ・ｼ・   - `fenjue/modes/photographer/templates.py`
   - `fenjue_prompt_mode_launcher.py`

2. A/B 蜈･蜿｣騾ｻ霎第｣譟･騾夊ｿ・ｼ・   - A 讓｡蠑擾ｼ壻ｿ晄戟 `fenjue.runtime.batch` 蜴溷ｧ・`prompt_for_art_direction`
   - B 讓｡蠑擾ｼ夊ｿ占｡梧慮 monkeypatch 蛻ｰ `fenjue.modes.photographer.templates.prompt_for_art_direction`
   - 蜴・`start_fenjue_v3.bat` 豐｡譛芽｢ｫ謾ｹ蜉ｨ

3. B 讓｡蠑乗歓譬ｷ 200 譚｡謠千､ｺ隸搾ｼ・   - 隕・尠 24 荳ｪ plan
   - 豈乗擅驛ｽ蛹・性荳泌宵蛹・性荳谺｡・・     - `[SCENE]`
     - `[PHOTOGRAPHER]`
     - `[CHARACTER]`
     - `[OUTFIT]`
   - 菫ｮ豁｣蜷取歓譬ｷ髟ｿ蠎ｦ闌・峩・・279 蛻ｰ 4941 蟄礼ｬｦ
   - 菫ｮ豁｣蜷主ｹｳ蝮・柄蠎ｦ・・579 蟄礼ｬｦ
   - 菫ｮ豁｣蜷手ｯｯ蟇ｼ鬘ｹ譽譟･・・ 鬘ｹ

4. 譛崎｣・唖髯､貂・黒螟肴衍騾夊ｿ・ｼ・   - 逶ｮ譬・恪陬・錐蟾ｲ莉主ｽ灘燕莉｣遐∽ｸｭ遘ｻ髯､
   - `hosiery_tea_room` 荵溷ｷｲ遘ｻ髯､

5. 譚ｯ蟄・謇矩Κ鬟朱勦螟肴衍・・   - 豐｡蜀榊書邇ｰ譏取仞豁｣蜷鷹ｼ灘干窶懈焔諡ｿ譚ｯ蟄・/ 謾ｾ荳区擶蟄・/ 諡ｿ邇ｻ迺・擶 / 諡ｿ逑ｶ蟄絶晉噪謠剰ｿｰ
   - 蠖灘燕讓｡譚ｿ譛画・遑ｮ雍滄擇郤ｦ譚滂ｼ壻ｸ崎ｦ∬ｮｩ謇区響譚ｯ蟄舌・ｩｬ蜈区擶縲・･ｮ逕ｨ邇ｻ迺・擶縲∫童蟄舌・･ｮ譁吝ｮｹ蝎ｨ

## 蟾ｲ菫ｮ豁｣鬟朱勦轤ｹ

### 1. `photograph-like anime key visual` 蜿ｯ閭ｽ隸ｯ蟇ｼ謌仙・螳・
B 讓｡蠑丞ｼ螟ｴ邇ｰ蝨ｨ譛我ｸ蜿･・・
```text
Create one coherent photograph-like anime key visual with one character.
```

髣ｮ鬚俶弍逕ｨ謌ｷ諠ｳ隕∫噪譏ｯ窶懷ワ鞫・ｽｱ蟶井ｸ譬ｷ扈・ｻ・判髱｢窶晢ｼ御ｸ肴弍隶ｩ蝗ｾ蜒丞序謌千悄莠ｺ鞫・ｽｱ謌門濠蜀吝ｮ樊槍蠖ｱ縲Ａphotograph-like` 蜿ｯ閭ｽ陲ｫ蜈ｶ莉匁ｨ｡蝙狗炊隗｣荳ｺ photorealistic / realistic photo縲・
蟾ｲ謾ｹ謌撰ｼ・
```text
Create one coherent photographer-composed anime key visual with one character, not photorealistic.
```

### 2. 蜿榊ｰ・ｱｻ蝨ｺ譎ｯ譛俄憺｢晏､紋ｺｺ迚ｩ窶晁ｯｯ蛻､鬟朱勦

蠖灘燕 plan 驥梧怏 mirror / reflection / acrylic / glass 遲牙・邏縲よｨ｡譚ｿ雍滄擇隸堺ｹ溷・莠・`Avoid: extra people`縲・
霑吩ｸ肴弍荳･譬ｼ遏帷崟・御ｽ・ｨ｡蝙句庄閭ｽ謚岩憺復荳ｭ蜿榊ｰ・晉判謌千ｬｬ莠御ｸｪ莠ｺ・悟ｰ､蜈ｶ譏ｯ・・ - `trend_mirror_studio`
 - `greenhouse_terrace_reflection`
 - `transparent_acrylic_display_wall`
 - `mirror_fragment_corner`

蟾ｲ蝨ｨ蜿榊ｰ・嶌蜈ｳ蝨ｺ譎ｯ荳ｭ陦･荳蜿･・・
```text
Reflections may show abstract fragments or partial echoes only, never a second character or duplicate person.
```

### 3. 豬ｷ謚･蟄怜摎蜥娯懃ｦ∵ｭ｢譁・ｭ冷晏ｭ伜惠霓ｻ蠕ｮ蜀ｲ遯・
`graphic_poster_studio` 霑咏ｱｻ plan 莨壼・邇ｰ・・
```text
large unreadable letter blocks
decorative non-readable letters
```

菴・ｴ滄擇郤ｦ譚滄㈹蜷梧慮譛会ｼ・
```text
text, watermark
```

逕ｨ謌ｷ荵句燕蝟懈ｬ｢ Ellen Joe 驍｣蠑豬ｷ謚･諢滂ｼ御ｽ・崟蜒乗ｨ｡蝙句ｮｹ譏捺滑窶徑etter blocks窶晉炊隗｣謌千悄螳櫁恭譁・∬ｧ定牡蜷阪´ogo 謌門刀迚悟ｭ励・
蟾ｲ蝨ｨ豬ｷ謚･ / 蟄怜摎逶ｸ蜈ｳ蝨ｺ譎ｯ荳ｭ陦･荳蜿･・・
```text
Typography-like shapes must be abstract graphic blocks with no readable words, letters, logos, or brand text.
```

### 4. 窶懈焔菫晄戟 empty窶昜ｸ榊ｺ碑ｯｯ莨､閾ｪ辟ｶ蜉ｨ菴・
蜴溽ｺｦ譚滂ｼ・
```text
Hands stay simple, empty, and anatomically readable.
```

霑咎㈹逧・empty 譛ｬ諢乗弍窶應ｸ肴響迚ｩ菴凪晢ｼ御ｸ肴弍窶應ｸ榊・隶ｸ謇狗｢ｰ螟ｴ蜿・/ 謇ｶ譬・/ 謾ｾ蝨ｨ譯碁擇窶昴ゆｸｺ莠・∩蜈肴ｨ｡蝙区滑謇狗判蠕怜Ψ遑ｬ・悟ｷｲ謾ｹ謌撰ｼ・
```text
Hands stay simple, empty of objects, and anatomically readable.
```

## 蜑ｩ菴呵ｧょｯ溽せ

### 1. 謠千､ｺ隸肴紛菴灘￥髟ｿ

B 讓｡蠑丈ｿｮ豁｣蜷主ｹｳ蝮・ｺｦ 4579 蟄礼ｬｦ・梧怙髟ｿ謗･霑・4941 蟄礼ｬｦ縲らｻ捺桷貂・･夲ｼ御ｽ・ｼ壼ｸｦ譚･荳､荳ｪ鬟朱勦・・
 - 蜷取ｮｵ譛崎｣・・雍滄擇郤ｦ譚滓揀驥崎｢ｫ遞驥・ - 讓｡蝙句庄閭ｽ蜿ｪ謚謎ｽ乗怙譏ｾ逵ｼ逧・ｯ搾ｼ梧ｯ泌ｦ・white縲｝hoto縲〉eflection縲〕etter

蟒ｺ隶ｮ荳倶ｸ霓ｮ蜴狗ｼｩ逶ｮ譬・ｼ・
 - B 讓｡蠑乗而蛻ｶ蝨ｨ 3200 蛻ｰ 3800 蟄礼ｬｦ
 - `[SCENE]` 蜥・`[PHOTOGRAPHER]` 蜿ｯ莉･菫晉蕗・御ｽ・ｯ城｡ｹ蟄玲ｮｵ蜀咲洒荳轤ｹ
 - 莠ｺ迚ｩ霄ｫ莉ｽ蜥梧恪陬・ｸｻ扈捺桷荳崎ｦ∝視螟ｪ迢

## 蠖灘燕貂・黒迥ｶ諤・
譁ｰ蠅樊枚莉ｶ・・
 - `fenjue/modes/photographer/plans.py`
 - `fenjue/modes/photographer/templates.py`
 - `fenjue_prompt_mode_launcher.py`
 - `start_fenjue_prompt_mode.bat`

蟾ｲ菫ｮ謾ｹ譁・ｻｶ・・
 - `fenjue/modes/original/plans.py`
 - `art_direction_templates.py`
 - `config/runtime_art_direction.json`

霑吩ｺ帑ｿｮ謾ｹ蛹・性・・
 - 蛻髯､謖・ｮ壽恪陬・ｸ・`hosiery_tea_room`
 - 髯堺ｽ守區濶ｲ / 螂ｶ豐ｹ濶ｲ / 雎｡迚咏區譛崎｣・ｻ倩ｮ､蛟ｾ蜷・ - 髯堺ｽ惹ｺｺ迚ｩ謇区響譚ｯ蟄舌∫悉迺・擶縲∫童蟄千噪讎ら紫
 - 譁ｰ蠅・B 讓｡蠑乗槍蠖ｱ蟶育ｻ捺桷・御ｽ・夊ｿ・眠蜷ｯ蜉ｨ蜈･蜿｣霑帛・
 - B 讓｡蠑丞ｷｲ謾ｹ荳ｺ菴ｿ逕ｨ迢ｬ遶区槍蠖ｱ蟶井ｸ鍋畑 plan 豎・御ｸ榊・螟咲畑蜴滓悽逧・惻譎ｯ / 蜉ｨ菴・/ 譫・崟謚ｽ譬ｷ豎

## B 讓｡蠑丈ｸ鍋畑 Plan 譖ｴ譁ｰ

譁ｰ蠅・`fenjue/modes/photographer/plans.py`・悟宵扈・B 讓｡蠑剰ｰ・畑縲・ 讓｡蠑丞柱蜴・`fenjue/modes/original/plans.py` 逧・歓譬ｷ騾ｻ霎台ｸ榊序縲・
B 讓｡蠑冗鴫蝨ｨ蛻・・荳牙ｱゑｼ・
 - 鞫・ｽｱ蟶亥惻譎ｯ plan・夐葎譯・ｧょｯ溘∽ｽ取惻菴榊燕譎ｯ縲・ｫ俶惻菴咲ｩｺ髣ｴ縲・柄辟ｦ髫皮黄縲∫ｪ苓ｾｹ蜊企・謖｡縲∬｡苓ｧ貞勘郤ｿ縲∵｣壽牛雍溽ｩｺ髣ｴ縲∬ｵｰ蟒企剰ｧ・∝渚蟆・｢守援縲∝､ｩ蜿ｰ螳ｽ譎ｯ
 - 鞫・ｽｱ蟶亥勘菴・plan・夊ｽｬ霄ｫ蜑堺ｸ迸ｬ縲∵ｨｪ遨ｿ逕ｻ髱｢縲∝濠驕ｮ謖｡隗ょｯ溘∬ｾｹ郛伜屓螟ｴ縲∝・譚滉ｸｭ蛛憺｡ｿ縲∝攝蟋ｿ譁懃ｺｿ驥榊ｿ・∵紛逅・､ｴ蜿第・陲門哨縲∵ｳｨ諢丞鴨逡吝惠邇ｯ蠅・㈹
 - 鞫・ｽｱ蟶域桷蝗ｾ plan・夐葎譯・・蜑ｲ縲∽ｽ主燕譎ｯ蜴玖ｿｫ縲・ｫ倩ｧ貞ｺｦ蝨ｰ髱｢蝗ｾ蠖｢縲・柄辟ｦ螻ょ匠隗ょｯ溘∬ｴ溽ｩｺ髣ｴ霎ｹ郛倅ｸｻ菴薙∝渚蟆・｢守援陬∝・縲∵ｶ亥､ｱ轤ｹ陦瑚ｵｰ

B 讓｡蠑丞星蜉ｨ蜷惹ｼ夊ｿｽ蜉鞫・ｽｱ蟶亥惻譎ｯ蛻・ｱｻ騾画叫・・
 - `1`・壽｣壽牛 / 譚ょｿ・/ 鞫・ｽｱ譽・ - `2`・壼ｮ､蜀・/ 蟆剰ｯｴCG / 遨ｺ髣ｴ諢・ - `3`・壽・莠ｮ譌･蟶ｸ / 蠎鈴銅 / 陦怜玄
 - `0`・壼・髫乗惻鞫・ｽｱ蟶亥惻譎ｯ

荵滓髪謖∝多莉､陦檎峩謗･騾画叫・御ｾ句ｦ・`python fenjue_prompt_mode_launcher.py B 2`縲・
菫ｮ豁｣蜷取歓譬ｷ 300 譚｡・・
 - A 讓｡蠑丈ｻ堺ｿ晄戟蜴滓ｨ｡譚ｿ
 - B 讓｡蠑乗ｨ｡譚ｿ蜷搾ｼ啻fenjue_v6_photographer_dedicated_plans`
 - B 讓｡蠑乗ｯ乗擅驛ｽ譛・`[SCENE]` / `[PHOTOGRAPHER]` / `[CHARACTER]` / `[OUTFIT]`
 - B 讓｡蠑剰ｯｯ蟇ｼ鬘ｹ譽譟･・・ 鬘ｹ
 - 謚ｽ譬ｷ髟ｿ蠎ｦ闌・峩・・388 蛻ｰ 4942 蟄礼ｬｦ
 - 蟷ｳ蝮・柄蠎ｦ・・601 蟄礼ｬｦ

## 蟒ｺ隶ｮ荳倶ｸ豁･

1. 蜈育畑 B 讓｡蠑剰ｷ大崟・瑚ｧょｯ滓桷蝗ｾ縲∵恪陬・揀驥阪∽ｺｺ迚ｩ蜉ｨ菴懈弍蜷ｦ豈・A 讓｡蠑乗峩蜒乗槍蠖ｱ蟶亥・蝗ｾ縲・2. 螯よ棡 B 讓｡蠑乗桷蝗ｾ譛画譜菴・署遉ｺ隸崎ｿ・柄・御ｸ倶ｸ霓ｮ謚・B 讓｡蠑丞視郛ｩ蛻ｰ 3200 蛻ｰ 3800 蟄礼ｬｦ縲・3. 螯よ棡 B 讓｡蠑冗ｨｳ螳夲ｼ悟・閠・剔謚・plan 蜴狗ｼｩ謌千畑謌ｷ諠ｳ隕∫噪荳臥ｱｻ蝨ｺ譎ｯ菴鍋ｳｻ縲・
