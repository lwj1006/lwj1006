# Fenjue 3.0 新版代码 Review：新人物 / 3人轮次 / JSON 管理 / 提示词建议

## 0. 结论

这版代码的主方向是对的：

- 已经从“随机角色 + 随机主题”升级成了 **角色轮次驱动**。
- `CHARACTER_SEQUENCE` 已包含 9 个角色：南宫、爱芮、千夏、丹、星见雅、仪玄、叶瞬光、席德、橘福福。
- `CHARACTERS_PER_BATCH = 3`，每一批抽 3 个未出现角色。
- 一轮 9 个角色跑完后，通过 `used_character_batches.json` 清空并重新开始。
- 每个角色自己的服装主题使用历史通过 `used_character_clothing_themes.json` 管理，避免同一角色短期内重复同一服装主题。
- 新追加的 3 个角色已经进入：
  - `NEW_CHARACTER_PROPAGATION_PROFILES`
  - `NEW_CHARACTER_OUTFIT_VARIATIONS`
  - `NEW_CHARACTER_PLAN_WEIGHTS`
  - `CHARACTER_REQUIRED_IDENTITY_TOKENS`
  - `CHARACTER_FORBIDDEN_PLANS`
  - `CHARACTER_VIEWER_DISTANCE`
  - `CHARACTER_LOCKS`

但是目前还存在 4 个需要优先修的点：

1. **新角色没有独立 `CHARACTER_ACTION_WEIGHTS`**，会 fallback 到“丹”的动作逻辑。
2. **部分新角色的主题权重和 forbidden tag 冲突**，有些写了权重但实际永远抽不到。
3. **当前保证的是“每批 3 个角色不重复”，不是“每批 3 个角色主题也不重复”**。
4. **提示词内容偏强，但有些角色的主题池会把官方人格拉偏**，尤其是橘福福和席德。

---

## 1. 当前规则 Review

### 1.1 角色轮次逻辑

当前主流程：

```python
CHARACTER_SEQUENCE = ["南宫", "爱芮", "千夏", "丹", "星见雅", "仪玄", "叶瞬光", "席德", "橘福福"]
CHARACTERS_PER_BATCH = 3
USED_CHARACTER_BATCH_FILE = PROJECT_DIR / "config" / "used_character_batches.json"
```

实际逻辑：

```python
def choose_character_batch(used_characters: list[str]) -> list[str]:
    valid_used = [name for name in used_characters if name in CHARACTER_SEQUENCE]
    used_characters[:] = valid_used

    available = [name for name in CHARACTER_SEQUENCE if name not in used_characters]
    if not available:
        used_characters.clear()
        save_used_character_batch(used_characters)
        available = CHARACTER_SEQUENCE[:]

    batch_size = min(CHARACTERS_PER_BATCH, len(available))
    selected = random.sample(available, k=batch_size)
    return selected
```

判断：**逻辑成立。**

效果是：

- 第 1 批：从 9 人里抽 3 人。
- 第 2 批：从剩下 6 人里抽 3 人。
- 第 3 批：从剩下 3 人里抽 3 人。
- 第 4 批：9 人全部用完，清空 JSON，重新开始新一轮。

这符合“每批角色不重复，一轮角色完成后重新开始新一轮”。

### 1.2 服装主题 JSON 管理

当前逻辑：

```python
USED_CHARACTER_CLOTHING_THEMES_FILE = PROJECT_DIR / "config" / "used_character_clothing_themes.json"
```

每个角色单独记录用过的服装主题：

```python
def choose_character_plan_and_action(character_name, recent_visual_tags, used_by_character):
    used_themes = used_by_character.setdefault(character_name, [])
    valid_used = [theme for theme in used_themes if theme in CLOTHING_THEMES]
    used_by_character[character_name] = valid_used
    used_set = set(valid_used)

    if len(used_set) >= len(CLOTHING_THEMES):
        used_by_character[character_name] = []
        used_set = set()
        save_used_character_clothing_themes(used_by_character)

    for _ in range(24):
        art_plan, action_style = choose_plan_and_action(character_name, recent_visual_tags)
        if art_plan["outfit_direction"] not in used_set:
            return art_plan, action_style
```

判断：**这个设计比全局服装去重更合理。**

原因：

- 南宫、爱芮、千夏、丹、星见雅、仪玄、叶瞬光、席德、橘福福的服装适配方向不同。
- 全局主题去重会导致一个角色被迫吃不适合自己的主题。
- 现在按角色记录主题历史，可以保证“同一角色不要一直重复同一套衣服”。

但它目前不能保证：**同一批 3 个角色之间的主题不重复。**

例如一批里可能出现：

- 叶瞬光：modern_guofeng_character_poster
- 橘福福：modern_guofeng_character_poster
- 仪玄：modern_guofeng_character_poster

这在代码上是允许的，因为去重是 `per-character`，不是 `per-batch`。

如果你说的“每个主题不重复角色3人”是指 **同一批 3 人不要使用同一个服装/主题方向**，需要追加一个 batch-level theme block。

---

## 2. 新人物接入 Review

## 2.1 叶瞬光

当前定位：

- 云岿山温柔师姐型执剑少女
- 温柔、可靠、保护者、清亮剑意
- 需要云岿山、剑、剑光、剑穗、符纹、山风或云气锚点

这个方向是成立的。她的传播人格比“冷酷剑客”更有差异化，适合做“温柔保护感 + 剑意”的二次元社交图。

当前问题：

```python
NEW_CHARACTER_PLAN_WEIGHTS["叶瞬光"] = {
    "modern_guofeng_character_poster": 10,
    "rainy_clear_umbrella_date": 6,
    "storybook_castle_balcony": 5,
    "dream_mist_portrait": 7,
    "ritual_star_idol": 6,
    "train_window_weekend": 4,
    "planetarium_soft_date": 3,
    "fairy_tale_bookshop": 2,
}
```

问题不大，但后半部分偏“约会 / 童话 / 日常”，如果抽多了会削弱云岿山和执剑身份。

建议：

- 保留 `modern_guofeng_character_poster`、`dream_mist_portrait`、`ritual_star_idol`。
- `rainy_clear_umbrella_date` 可以保留，但提示词里要改成“雨中护送 / 剑伞 / 山门雨气”，不要变成普通约会。
- `storybook_castle_balcony` 建议降低或替换，因为西式城堡容易误读成西幻公主。
- `planetarium_soft_date` 建议降低，因为星空约会容易把她拉成普通柔美少女。

推荐权重：

```python
NEW_CHARACTER_PLAN_WEIGHTS["叶瞬光"] = {
    "modern_guofeng_character_poster": 12,
    "dream_mist_portrait": 9,
    "ritual_star_idol": 7,
    "rainy_clear_umbrella_date": 4,
    "train_window_weekend": 2,
    "storybook_castle_balcony": 1,
    "planetarium_soft_date": 1,
    "fairy_tale_bookshop": 1,
}
```

建议追加动作权重：

```python
CHARACTER_ACTION_WEIGHTS.update({
    "叶瞬光": {
        "dreamy_side_glance": 7,
        "direct_eye_contact": 5,
        "symbolic_center_pose": 6,
        "floating_daydream_pose": 2,
        "near_camera_whisper": 0,
        "earpiece_call_gaze": 0,
        "idol_business_smile": 0,
    },
})
```

提示词建议追加：

```text
叶瞬光的剑意必须是“护人”而不是“杀人”。
画面可以出现剑光、剑穗、山门、竹影、云气、雨中回身，但不要把她画成冷酷刺客、西式骑士、公主或普通校园少女。
如果使用约会类主题，请转译为“师姐护送 viewer 经过山门/雨巷/石阶”，而不是甜蜜恋爱营业。
```

---

## 2.2 席德

当前定位：

- S级电属性强攻代理人
- 天真危险的机械改造少女
- 机械、改造、老席德、电弧、花朵反差

这个方向很好，传播钩子很强：**天真表情 + 危险机械 + 电光 + 花朵反差**。

当前最大问题：主题权重和 forbidden tags 冲突。

当前权重里有：

```python
"pixel_cloud_savepoint": 6,
"pajama_game_party": 3,
```

但当前 forbidden tags：

```python
"席德": {"soft_emotion", "flower", "warm_light"}
```

而：

- `pixel_cloud_savepoint` 带 `soft_emotion`
- `pajama_game_party` 带 `soft_emotion`

所以这两个主题虽然写了权重，实际会被 `_allowed_plan_for_character()` 过滤掉。

建议二选一。

### 方案 A：删除无效权重

```python
NEW_CHARACTER_PLAN_WEIGHTS["席德"] = {
    "game_ui_battle_select": 10,
    "neon_call_night": 7,
    "gacha_capsule_corner": 6,
    "arcade_prize_date": 5,
    "ultra_minimal_character_poster": 4,
}
```

### 方案 B：保留 savepoint，但让它席德化

如果你喜欢 `pixel_cloud_savepoint`，可以不要禁掉所有 `soft_emotion`，改成只禁具体不适合的 plan。

```python
CHARACTER_FORBIDDEN_TAGS.update({
    "席德": {"warm_light"},
})
```

然后在席德提示词里把 savepoint 转译成：

```text
如果使用 savepoint / game UI 类主题，必须表现为机械维修存档点、蓝紫电弧充电桩、老席德机械影子，而不是柔软云朵梦境。
```

更推荐方案 A。因为席德的核心是机械电光，不适合太软。

建议追加动作权重：

```python
CHARACTER_ACTION_WEIGHTS.update({
    "席德": {
        "direct_eye_contact": 6,
        "symbolic_center_pose": 7,
        "earpiece_call_gaze": 3,
        "dreamy_side_glance": 2,
        "floating_daydream_pose": 1,
        "near_camera_whisper": 0,
        "idol_business_smile": 0,
    },
})
```

提示词建议追加：

```text
席德的可爱必须来自“天真地展示危险改造”，不是普通卖萌。
蓝紫电弧、电路纹、机械零件、机库光、老席德大型机械痕迹至少要成为一个清楚视觉锚点。
花朵只能作为机械反差点缀，不要让画面变成普通花园少女。
不要普通军服少女、纯冷酷机器人、普通机甲驾驶员或无机械元素的电系少女。
```

---

## 2.3 橘福福

当前定位：

- 云岿山虎系元气师姐
- 火属性击破
- 虎虎生风、猛虎伏魔、热情能打

这个方向非常适合传播，但现在主题池有一部分会把她拉成普通可爱日常角色。

当前权重：

```python
NEW_CHARACTER_PLAN_WEIGHTS["橘福福"] = {
    "modern_guofeng_character_poster": 8,
    "rpg_town_square_festival": 8,
    "fantasy_cooking_class": 6,
    "theme_park_twilight": 5,
    "game_ui_battle_select": 5,
    "idol_practice_mirror_clean": 4,
    "bakery_morning_window": 4,
}
```

风险点：

- `bakery_morning_window` 会把她拉成普通面包店约会。
- `theme_park_twilight` 会把她拉成普通元气约会少女。
- `idol_practice_mirror_clean` 会把她拉成偶像练习生。
- 如果虎、火、云岿山锚点不强，会误读成普通猫娘。

建议：

```python
NEW_CHARACTER_PLAN_WEIGHTS["橘福福"] = {
    "modern_guofeng_character_poster": 10,
    "rpg_town_square_festival": 9,
    "game_ui_battle_select": 6,
    "fantasy_cooking_class": 4,
    "theme_park_twilight": 2,
    "idol_practice_mirror_clean": 1,
    "bakery_morning_window": 0,
}
```

或者直接加入 forbidden plan：

```python
CHARACTER_FORBIDDEN_PLANS.update({
    "橘福福": {
        "planetarium_soft_date",
        "fairy_tale_bookshop",
        "laundry_sun_room",
        "aquarium_blue_date",
        "bakery_morning_window",
    },
})
```

建议追加动作权重：

```python
CHARACTER_ACTION_WEIGHTS.update({
    "橘福福": {
        "direct_eye_contact": 6,
        "symbolic_center_pose": 6,
        "idol_business_smile": 4,
        "dreamy_side_glance": 2,
        "floating_daydream_pose": 1,
        "near_camera_whisper": 0,
        "earpiece_call_gaze": 0,
    },
})
```

提示词建议追加：

```text
橘福福的元气必须带“能打”和“伏魔”气质，不是普通猫娘卖萌。
虎纹火焰、虎系轮廓、虎威装置、伏魔符纸、云岿山石阶或练武场风线至少出现一个强锚点。
如果使用日常/料理/庙会主题，请转译成“虎系师姐招呼 viewer 后马上出发伏魔”的行动感，而不是普通甜美约会。
```

---

## 3. 必须优先修改的问题

## 3.1 新角色没有独立动作权重

当前 `CHARACTER_ACTION_WEIGHTS` 没有：

- 叶瞬光
- 席德
- 橘福福

因此 `choose_action_style()` 会 fallback 到 `CHARACTER_ACTION_WEIGHTS["丹"]`。

这会导致：

- 叶瞬光还算能接受，因为她和丹一样偏安静。
- 席德会不够“机械展示 / 危险说明”。
- 橘福福会不够“虎系行动 / 元气召唤”。

建议立刻追加：

```python
CHARACTER_ACTION_WEIGHTS.update({
    "叶瞬光": {
        "dreamy_side_glance": 7,
        "direct_eye_contact": 5,
        "symbolic_center_pose": 6,
        "floating_daydream_pose": 2,
        "near_camera_whisper": 0,
        "earpiece_call_gaze": 0,
        "idol_business_smile": 0,
    },
    "席德": {
        "direct_eye_contact": 6,
        "symbolic_center_pose": 7,
        "earpiece_call_gaze": 3,
        "dreamy_side_glance": 2,
        "floating_daydream_pose": 1,
        "near_camera_whisper": 0,
        "idol_business_smile": 0,
    },
    "橘福福": {
        "direct_eye_contact": 6,
        "symbolic_center_pose": 6,
        "idol_business_smile": 4,
        "dreamy_side_glance": 2,
        "floating_daydream_pose": 1,
        "near_camera_whisper": 0,
        "earpiece_call_gaze": 0,
    },
})
```

---

## 3.2 席德存在“写了权重但实际抽不到”的主题

当前 `席德` 权重中：

```python
"pixel_cloud_savepoint": 6,
"pajama_game_party": 3,
```

但 forbidden tags 禁了：

```python
"soft_emotion"
```

这两个 plan 都会被过滤。

建议删除这两个权重，或者修改 forbidden tags。

我建议删除，因为席德更适合机械、电弧、UI、机库、改造、危险玩具。

---

## 3.3 橘福福需要防止变成普通猫娘 / 普通约会少女

建议增加：

```python
CHARACTER_FORBIDDEN_PLANS.update({
    "橘福福": {
        "planetarium_soft_date",
        "fairy_tale_bookshop",
        "laundry_sun_room",
        "aquarium_blue_date",
        "bakery_morning_window",
    },
})
```

并降低：

```python
"theme_park_twilight": 2,
"idol_practice_mirror_clean": 1,
```

不要直接禁 `warm_light`，因为火属性角色本来就需要暖光。关键是禁“无虎无火无武修”的软日常。

---

## 3.4 每批 3 人内主题仍可能重复

如果你希望“一批 3 人主题也不重复”，建议改 `choose_character_plan_and_action()`。

### 建议改法

新增参数：

```python
def choose_character_plan_and_action(
    character_name: str,
    recent_visual_tags: list[str],
    used_by_character: dict[str, list[str]],
    batch_used_themes: set[str] | None = None,
) -> tuple[dict, dict]:
    batch_used_themes = batch_used_themes or set()
```

判断时同时避开角色历史和本批主题：

```python
if art_plan["outfit_direction"] not in used_set and art_plan["outfit_direction"] not in batch_used_themes:
    return art_plan, action_style
```

主循环里加入：

```python
while run_number <= total_runs and not stop_requested:
    selected_characters = choose_character_batch(used_character_batch)
    batch_completed_characters: list[str] = []
    batch_used_themes: set[str] = set()

    for character_name in selected_characters:
        art_plan, action_style = choose_character_plan_and_action(
            character_name,
            recent_visual_tags,
            used_by_character,
            batch_used_themes,
        )
        theme = art_plan["outfit_direction"]
        batch_used_themes.add(theme)
```

这样才是：

- 同一角色：长期不重复服装主题。
- 同一批 3 人：不会撞同一服装主题。
- 一轮角色结束：角色循环重新开始。

---

## 4. 提示词结构 Review

当前提示词结构：

```python
_visual_direction(selected_plan)
_official_personality_translation(character_name)
_performance(character_name, selected_plan, selected_action)
_anatomy_control()
_fashion(character_name, selected_plan)
_identity_lock(character_name)
_rendering(selected_plan)
_negative()
```

判断：**结构是对的。**

尤其是：

- 先给传播企划。
- 再给官方人格转译。
- 再给动作语言。
- 再给手脚控制。
- 再给服装。
- 再给身份锁。
- 最后给渲染层和负面项。

这里有一个小问题：

`_identity_lock()` 放在 `_fashion()` 后面是可以的，但如果模型对服装主题吸收太强，有时会先把角色变装成主题角色，再回头弱化身份锁。

建议顺序改成：

```python
_visual_direction(selected_plan)
_official_personality_translation(character_name)
_identity_lock(character_name)
_performance(character_name, selected_plan, selected_action)
_anatomy_control()
_fashion(character_name, selected_plan)
_rendering(selected_plan)
_negative()
```

理由：

- 官方人格之后马上锁身份。
- 再允许动作和服装变化。
- 这样新角色不容易被主题吞掉。

---

## 5. 推荐最终补丁片段

下面是我建议你优先追加到 `art_direction_options.py` 末尾的补丁。

```python
# ---------------------------------------------------------------------------
# New character action weights + stricter theme safety gates
# ---------------------------------------------------------------------------

CHARACTER_ACTION_WEIGHTS.update({
    "叶瞬光": {
        "dreamy_side_glance": 7,
        "direct_eye_contact": 5,
        "symbolic_center_pose": 6,
        "floating_daydream_pose": 2,
        "near_camera_whisper": 0,
        "earpiece_call_gaze": 0,
        "idol_business_smile": 0,
    },
    "席德": {
        "direct_eye_contact": 6,
        "symbolic_center_pose": 7,
        "earpiece_call_gaze": 3,
        "dreamy_side_glance": 2,
        "floating_daydream_pose": 1,
        "near_camera_whisper": 0,
        "idol_business_smile": 0,
    },
    "橘福福": {
        "direct_eye_contact": 6,
        "symbolic_center_pose": 6,
        "idol_business_smile": 4,
        "dreamy_side_glance": 2,
        "floating_daydream_pose": 1,
        "near_camera_whisper": 0,
        "earpiece_call_gaze": 0,
    },
})

NEW_CHARACTER_PLAN_WEIGHTS.update({
    "叶瞬光": {
        "modern_guofeng_character_poster": 12,
        "dream_mist_portrait": 9,
        "ritual_star_idol": 7,
        "rainy_clear_umbrella_date": 4,
        "train_window_weekend": 2,
        "storybook_castle_balcony": 1,
        "planetarium_soft_date": 1,
        "fairy_tale_bookshop": 1,
    },
    "席德": {
        "game_ui_battle_select": 10,
        "neon_call_night": 7,
        "gacha_capsule_corner": 6,
        "arcade_prize_date": 5,
        "ultra_minimal_character_poster": 4,
    },
    "橘福福": {
        "modern_guofeng_character_poster": 10,
        "rpg_town_square_festival": 9,
        "game_ui_battle_select": 6,
        "fantasy_cooking_class": 4,
        "theme_park_twilight": 2,
        "idol_practice_mirror_clean": 1,
        "bakery_morning_window": 0,
    },
})

for character_name, plan_weights in NEW_CHARACTER_PLAN_WEIGHTS.items():
    CHARACTER_PLAN_WEIGHTS.setdefault(character_name, {}).update(plan_weights)

CHARACTER_FORBIDDEN_PLANS.update({
    "橘福福": {
        "planetarium_soft_date",
        "fairy_tale_bookshop",
        "laundry_sun_room",
        "aquarium_blue_date",
        "bakery_morning_window",
    },
})
```

---

## 6. 推荐最终提示词追加文案

可以追加到 `CHARACTER_LOCKS` 或 `NEW_CHARACTER_PROPAGATION_PROFILES` 对应字段里。

### 叶瞬光

```text
叶瞬光的剑意必须是“护人”而不是“杀人”。画面可以出现剑光、剑穗、山门、竹影、云气、雨中回身，但不要把她画成冷酷刺客、西式骑士、公主或普通校园少女。如果使用约会类主题，请转译为“师姐护送 viewer 经过山门/雨巷/石阶”，而不是甜蜜恋爱营业。
```

### 席德

```text
席德的可爱必须来自“天真地展示危险改造”，不是普通卖萌。蓝紫电弧、电路纹、机械零件、机库光、老席德大型机械痕迹至少要成为一个清楚视觉锚点。花朵只能作为机械反差点缀，不要让画面变成普通花园少女。不要普通军服少女、纯冷酷机器人、普通机甲驾驶员或无机械元素的电系少女。
```

### 橘福福

```text
橘福福的元气必须带“能打”和“伏魔”气质，不是普通猫娘卖萌。虎纹火焰、虎系轮廓、虎威装置、伏魔符纸、云岿山石阶或练武场风线至少出现一个强锚点。如果使用日常/料理/庙会主题，请转译成“虎系师姐招呼 viewer 后马上出发伏魔”的行动感，而不是普通甜美约会。
```

---

## 7. 最终判断

这版代码已经完成了结构升级：

- 角色轮次：成立。
- JSON 管理：成立。
- 新人物人格系统：基本成立。
- 单人优先 pipeline：成立。
- 身份锚点：成立。
- 社交传播提示词：成立。

真正需要改的是：

1. 给新 3 人补独立 `CHARACTER_ACTION_WEIGHTS`。
2. 修掉席德“权重存在但被 forbidden tag 过滤”的无效配置。
3. 收紧橘福福软日常主题，避免普通猫娘化。
4. 如果你要严格做到“一批 3 人主题也不重复”，加 `batch_used_themes`。
5. 把 `_identity_lock()` 提前到 `_official_personality_translation()` 后面，减少主题吞角色的问题。

优先级：

```text
P0：新角色 action weights
P0：席德权重 / forbidden tag 冲突
P1：橘福福主题池收紧
P1：batch_used_themes 防同批主题重复
P2：prompt_for_art_direction 顺序调整
P2：清理 art_direction_options.py 里多次 redefine 的 choose_art_plan，降低维护成本
```
