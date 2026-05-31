# Fenjue 3.0 本轮生成 Review：星见雅 / 丹未按提示词生成问题

## 0. 结论

本轮问题不是单纯“模型不听话”，而是 pipeline 里存在一个明显的控制权错位：**当前批量逻辑先抽一个全局服装 / 企划 theme，然后把同一个 theme 套给所有角色**。这会绕开角色自己的 `CHARACTER_PLAN_WEIGHTS`、`preferred_hooks` 和角色人格偏向，导致星见雅、丹被迫进入不适合自己的场景 / 服装 / 情绪模板。

所以星见雅和丹出现偏离，核心原因是：

1. **角色企划选择被全局 theme 接管**，角色权重没有真正主导画面。
2. **Identity Lock 仍然偏“描述型”，不是“强制 token 型”**，关键识别点没有形成不可替代的硬锚点。
3. **V3 社交传播模板的共性太强**，容易把所有角色拉成“好看的二次元社交图”，削弱星见雅的剑客压迫感和丹的透明未来感。
4. **星见雅 / 丹的核心识别物被写成 optional**，一旦场景和服装更强，模型会优先执行更有画面诱惑力的泛化元素。

---

## 1. 本轮代码层面的主要问题

### 1.1 当前批量逻辑使用“全局 theme 批次”

新版本 `chatgpt_batch_pyautogui.py` 的逻辑是：

```python
while run_number <= total_runs and not stop_requested:
    theme = choose_unused_clothing_theme(used_clothing_themes)
    theme_total_runs = len(CHARACTER_SEQUENCE) * RUNS_PER_CHARACTER_PER_THEME

    for character_repeat in range(1, RUNS_PER_CHARACTER_PER_THEME + 1):
        for character_name in CHARACTER_SEQUENCE:
            reference_files = reference_files_for_character(character_name)
            art_plan = choose_art_plan_for_outfit(theme)
            action_style = choose_action_style(character_name, recent_visual_tags)
            propagation_profile = propagation_profile_for(character_name)
            prompt = prompt_for_art_direction(character_name, art_plan, action_style)
```

这段的实际效果是：

- 先抽一个 `theme`。
- 再让南宫、爱芮、千夏、丹、星见雅、仪玄全部使用这个 theme。
- `art_plan = choose_art_plan_for_outfit(theme)` 只按服装主题反查 plan。
- 角色只影响 `reference_files`、`action_style`、`propagation_profile`。
- **角色并没有主导 art_plan。**

这会直接造成：

| 角色 | 应该由谁主导 | 实际主导 |
|---|---|---|
| 星见雅 | 剑客、黑兽耳、长直发、压迫感、刀线、月 / 仪式 / 冷感 | 当前全局 theme |
| 丹 | 浅粉短发、透明感、安静、未来感、轻漂浮 / 留白 | 当前全局 theme |

这也是为什么你会感觉“星见雅、丹明显没有按照提示词生成”。提示词里虽然写了角色，但前面的画面企划和服装主题已经把模型带偏了。

---

## 2. 当前上传图片的可见问题

我当前能直接看到的一张生成图：

- 画面完成度高。
- 构图、光影、细节密度都强。
- 但角色识别明显是黑粉双马尾、猫发夹、科技光环、小机械翅膀方向。
- 这更接近南宫 / 爱芮系的视觉语言。
- 如果这张本应是星见雅或丹，那就是严重失败。

问题不在画面质量，而在**角色身份没有被当前 prompt 系统锁住**。

这张图说明当前系统很擅长生成：

```text
高完成度二次元社交传播图
赛博偶像 / 黑粉少女 / 机能服 / 大腿近景 / 黄昏城市
```

但它没有稳定执行：

```text
角色专属身份 > 本轮主题 > 服装变化 > 场景传播符号
```

目前更像是：

```text
本轮主题 / 好看的社交图风格 > 角色身份
```

---

## 3. 星见雅为什么容易跑偏

### 3.1 星见雅的识别点被写得偏“可选”

当前 `CHARACTER_LOCKS` 中星见雅写法大意是：

```text
黑色长直发、齐刘海、黑色兽耳、红色眼瞳。
武士风格的绳结、挂饰、红色刀线或武器意象可以作为可选识别元素。
不要求每张都出现实体武器。
```

这里的问题是：

- 黑色兽耳很重要，但如果画面复杂，可能被头饰 / 光环替代。
- 太刀 / 红色刀线被写成 optional，模型容易省略。
- 一旦省略刀线，星见雅就会退化成“黑长直兽耳少女”。
- 如果又叠上社交传播模板，就会继续退化成“黑发漂亮女生”。

### 3.2 星见雅不适合太多“恋爱 / 可爱 / 近景互动”模板

当前星见雅仍然存在一些容易软化她的 plan：

- `planetarium_soft_date`
- `rainy_clear_umbrella_date`
- `neon_call_night`
- `pajama_game_party` 低权重但仍可能被 theme 批次间接带入

这些不是完全不能用，但在 identity 还没稳之前，会把星见雅拉向：

```text
冷感约会少女 / 夜景通话少女 / 黑发社交图
```

而不是：

```text
凛然剑客 / 黑兽耳 / 红瞳 / 刀线 / 压迫感
```

### 3.3 建议改成“星见雅三锚点强制”

星见雅每张至少必须成立：

```text
黑色长直发 + 黑色兽耳 + 红色眼瞳
```

并且再强制一个剑客锚点：

```text
红色刀线 / 太刀柄 / 刀鞘 / 绳结挂饰 / 月下刀影
```

不要把这些全部写成“可选”。可选只适合外围符号，不适合身份锚点。

---

## 4. 丹为什么容易跑偏

### 4.1 丹的身份锚点太柔，容易被主题吃掉

丹当前锁定是：

```text
浅粉色短发，空气感厚刘海，不对称刘海，两侧包脸短发，发尾外翻；
柔软羽毛感短层次发型，浅粉色头发渐变，粉紫色眼睛。
银白细头环、蓝银色星形发卡、耳侧轻机械模块只是小识别点。
气质安静温柔、略淡漠、未来感与透明感。
```

这个描述方向是对的，但执行上有两个弱点：

1. 丹没有像南宫那样有“黑粉双马尾 + 猫发夹 + 光环 + 机械翅膀”这种强视觉符号。
2. 丹的银白头环、星形发卡、耳侧机械模块被写成“小识别点”，模型很容易丢。

于是丹会被当前 theme 拉成：

```text
普通粉发少女 / 圣女风少女 / 柔光短发女孩 / 透明系泛用角色
```

### 4.2 丹需要“轻未来识别件”强制出现

丹每张至少必须成立：

```text
浅粉短发 + 不对称厚刘海 + 粉紫眼睛
```

并且必须有一个未来识别件：

```text
银白细头环 / 蓝银星形发卡 / 耳侧轻机械模块 / 透明蓝银小光片
```

否则她会太容易被其他粉发角色吞掉。

---

## 5. Prompt 模板问题

### 5.1 Identity Lock 位置对，但语气不够硬

当前模板有 `Identity Lock`，这是正确方向。但这一句会削弱角色：

```text
角色识别只锁头发轮廓、发色、发饰、眼睛和脸部气质；服装主色由本次视觉企划决定，不被角色默认配色支配。
```

问题是：

- 对南宫、爱芮这类强发型角色影响较小。
- 对丹、星见雅这类依赖气质和局部符号的角色影响很大。
- “服装主色由视觉企划决定”会让模型优先执行 theme 的色彩和衣装，而不是角色身份。

建议改成：

```text
角色身份优先级高于服装主题、场景主题和视觉企划。
服装可以变化，但不能改变角色的头发轮廓、发色、发饰、眼睛、核心符号和人格气质。
```

### 5.2 V3 社交模板的泛化力量太强

当前模板强调：

```text
停滑、点击、收藏和传播
角色人格、幻想感、情绪价值和缩略图识别
恋爱感、安全亲密感、被角色选中的感觉
```

这对爱芮、南宫、千夏有效，但对星见雅、丹需要降权。

星见雅的传播不是“恋爱亲密”，而是：

```text
凛然、压迫、被凝视、刀线、冷感距离、强者存在感
```

丹的传播不是“营业互动”，而是：

```text
安静、透明、漂浮、未来感、距离感、轻微神性、被治愈
```

所以建议 `Official Personality Translation` 里增加一个字段：

```python
"viewer_distance": "close / medium / distant / ritual"
```

然后在模板里控制互动方式：

- 爱芮：close / idol interaction
- 南宫：medium-close / teasing control
- 千夏：medium / shy companion
- 丹：medium-distant / quiet healing
- 星见雅：distant / pressure gaze
- 仪玄：ritual / mature mystery

---

## 6. 代码结构建议

### 6.1 不要用全局 theme 强行跑全角色

当前逻辑：

```python
theme = choose_unused_clothing_theme(used_clothing_themes)
for character_name in CHARACTER_SEQUENCE:
    art_plan = choose_art_plan_for_outfit(theme)
```

建议改成：

```python
for character_name in CHARACTER_SEQUENCE:
    art_plan, action_style = choose_plan_and_action(character_name, recent_visual_tags)
    theme = art_plan["outfit_direction"]
```

如果你想保留“服装主题不重复”，也应该改成每个角色一套 usage：

```python
used_clothing_themes_by_character = {
    "丹": set(),
    "星见雅": set(),
    ...
}
```

不要让一个主题同时支配六个角色。

### 6.2 `choose_art_plan_for_outfit` 应该降级为 fallback

现在它是主路径。建议只在你明确指定某个衣装主题时使用：

```python
if forced_theme:
    art_plan = choose_art_plan_for_outfit_for_character(character_name, forced_theme)
else:
    art_plan, action_style = choose_plan_and_action(character_name, recent_visual_tags)
```

更稳的版本：

```python
def choose_art_plan_for_outfit_for_character(character_name: str, outfit_direction: str, recent_tags=None) -> dict:
    character = _primary_character(character_name)
    weights_by_name = CHARACTER_PLAN_WEIGHTS.get(character, CHARACTER_PLAN_WEIGHTS["丹"])
    profile = propagation_profile_for(character)

    candidates = [
        plan for plan in ART_DIRECTION_PLANS
        if plan["outfit_direction"] == outfit_direction
        and weights_by_name.get(plan["name"], 0) > 0
    ]

    if not candidates:
        return choose_art_plan(character_name, recent_tags)

    weights = [
        _profile_adjusted_weight(
            plan["name"],
            weights_by_name.get(plan["name"], 1),
            profile.get("preferred_hooks", set()),
        )
        for plan in candidates
    ]
    return _weighted_choice(candidates, weights)
```

### 6.3 给星见雅 / 丹加 hard gate

建议新增：

```python
CHARACTER_REQUIRED_IDENTITY_TOKENS = {
    "丹": [
        "浅粉色短发",
        "不对称空气感厚刘海",
        "粉紫色眼睛",
        "银白细头环或蓝银星形发卡或耳侧轻机械模块",
    ],
    "星见雅": [
        "黑色长直发",
        "厚重整齐齐刘海",
        "黑色兽耳",
        "锐利红色眼瞳",
        "红色刀线或太刀柄或刀鞘或武士绳结",
    ],
}
```

模板里单独输出：

```text
【Non-negotiable Identity Tokens】
本角色必须同时满足以下识别 token：...
这些 token 的优先级高于服装主题、场景主题、背景符号和构图企划。
```

### 6.4 增加角色专属禁用 plan / 降权 plan

建议短期先加：

```python
CHARACTER_FORBIDDEN_PLANS = {
    "星见雅": {
        "pajama_game_party",
        "bakery_morning_window",
        "blooming_flower_cart",
        "seaside_date_kiosk",
        "laundry_sun_room",
    },
    "丹": {
        "arcade_prize_date",
        "theme_park_twilight",
        "idol_practice_mirror_clean",
        "neon_call_night",
    },
}
```

星见雅不是不能约会，但第一阶段先稳身份，不要让软场景污染她。丹也不是不能日常，但第一阶段先稳“透明未来感”，不要被高色块娱乐场景吞掉。

---

## 7. 推荐修改优先级

### P0：立刻改

1. 批量主循环改回“每个角色自己选 art_plan”。
2. `choose_art_plan_for_outfit(theme)` 不再作为默认主路径。
3. 星见雅、丹加入 `Non-negotiable Identity Tokens`。
4. 星见雅的刀线 / 太刀柄 / 刀鞘 / 武士绳结从 optional 提升到“至少一个必须出现”。
5. 丹的银白细头环 / 蓝银星形发卡 / 耳侧轻机械模块从小识别点提升到“至少一个必须出现”。

### P1：下一轮优化

1. `preferred_hooks` 改成更强的 gate，不只是加权。
2. 增加 `viewer_distance`，按角色控制互动距离。
3. 每个角色单独维护服装主题冷却，不要全局共享。
4. prompt log 里打印完整 prompt，方便回查。
5. feedback log 增加人工评分字段：
   - identity_score
   - plan_score
   - outfit_score
   - thumbnail_score
   - reject_reason

### P2：长期优化

1. 做角色专属 prompt mini-template。
2. 对星见雅、丹单独建立“身份稳定测试集”。
3. 每次只跑 6 张身份测试图，稳定后再放回全自动批量。

---

## 8. 下一轮测试建议

下一轮不要直接跑 99 或 999。

建议先跑：

```text
星见雅 4 张
丹 4 张
```

测试目标不是画面质量，而是：

```text
角色身份是否一眼成立
```

评分标准：

| 分数 | 标准 |
|---|---|
| 3 | 一眼就是该角色，发型 / 眼睛 / 核心符号都成立 |
| 2 | 基本像，但少一个关键符号 |
| 1 | 只有部分元素像，整体像泛用角色 |
| 0 | 完全跑偏 |

先把星见雅、丹稳定到平均 2.5 分以上，再恢复全角色批量。

---

## 9. 最终判断

这轮最大问题不是图不好看，而是系统的控制权顺序错了。

当前实际顺序接近：

```text
全局服装 theme → art_plan → 社交传播模板 → 角色 identity
```

应该改成：

```text
角色 identity hard lock → 角色人格传播 → 角色允许的 art_plan → 服装变化 → 场景符号
```

星见雅和丹的问题会在这个顺序修正后明显改善。
