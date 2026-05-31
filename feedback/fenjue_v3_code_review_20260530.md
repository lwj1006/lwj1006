# Fenjue 3.0 新代码 Review - 2026-05-30

## 结论

这轮修改方向是对的，核心问题已经从“全局 theme 套所有角色”改成了“角色先决定企划，再落到服装与场景”。  
丹 / 星见雅跑偏的问题也有了有效的第一层防线：硬身份 token、禁用 plan、viewer distance、每角色服装主题历史都已经进入主流程。

当前版本可以进入小批量实跑，但建议先跑 12～24 张，不要直接开 999。重点看丹和星见雅是否还会被“约会 / 偶像 / 糖果 / 童话”语义软化。

---

## 已解决的问题

### 1. 批量逻辑已回到角色主导

现在主循环不再先抽一个全局 theme 给所有角色复用，而是在每个角色回合调用：

```python
art_plan, action_style = choose_character_plan_and_action(
    character_name,
    recent_visual_tags,
    used_by_character,
)
```

这点是关键修复。  
以前的问题是：theme 先行，角色只能被动套衣服；现在变成角色先行，服装只是 art_plan 的结果。

### 2. 丹 / 星见雅身份锚点已经加到 prompt 高优先级区

丹新增的硬 token：

- 浅粉色短发
- 不对称空气感厚刘海
- 粉紫色眼睛
- 未来识别件至少一个

星见雅新增的硬 token：

- 黑色长直发
- 厚重整齐齐刘海
- 黑色兽耳
- 红色眼瞳
- 剑客锚点至少一个

并且 prompt 中写明这些 token 高于服装、场景、背景符号和构图企划。  
这比单纯写在角色描述里有效，因为它明确了优先级。

### 3. 禁用 plan 已进入 choose_art_plan

`_allowed_plan_for_character()` 已经被接入 `choose_art_plan()` 的候选过滤。  
这意味着丹 / 星见雅不会只是在权重上降低，而是直接排除某些明显不合适的 plan。

这对星见雅尤其重要，因为她一旦抽到 theme park、bakery、laundry、seaside date 这类软场景，很容易被模型画成普通约会少女。

### 4. viewer distance 是对症修复

丹被定义为：

```text
medium-distant / quiet healing
```

星见雅被定义为：

```text
distant / pressure gaze
```

这个设计合理。  
丹不应该贴脸强营业，星见雅也不应该被处理成亲密约会感角色。viewer distance 能约束“镜头关系”，这比只改服装更有效。

### 5. 每角色服装主题历史已做出来

`used_character_clothing_themes.json` 这条线是必要的。  
它解决的不是“全局重复”，而是“同一个角色连续抽到同类 outfit_direction”的问题。

当前实现里：

- 按角色读取历史
- 过滤已用 theme
- 找不到未用 theme 时最多尝试 24 次
- 标记时按角色写入历史

整体逻辑成立。

---

## 仍然存在的风险

### 风险 1：`CHARACTER_PLAN_WEIGHT_FLOOR = 1` 会让未显式配置的新 plan 默认可抽

这是当前最大隐患。

因为你现在场景池不断追加，新 plan 只要没有写进某个角色的权重表，默认仍然会以 1 的权重进入候选。  
这对千夏、南宫、爱芮问题不大，但对丹 / 星见雅这种容易跑偏的角色风险更高。

建议后续把丹 / 星见雅改成更严格的 whitelist 模式：

```python
STRICT_PLAN_CHARACTERS = {"丹", "星见雅", "仪玄"}
```

对这些角色，未写入权重表的 plan 默认权重应为 0，而不是 1。

### 风险 2：profile preferred_hooks 仍可能把某些软场景重新加权

`_profile_adjusted_weight()` 会对 preferred_hooks 加 5。  
如果某个角色 profile 里还保留了偏软、偏约会、偏偶像的 hook，就可能把不够合适的 plan 拉高。

尤其要检查：

- 星见雅是否还保留 `heart_signal_closeup`
- 星见雅是否还保留 `moon_confession_fantasy`
- 丹是否还保留过多 date / confession / closeup 类 hook

这些不一定要删，但应该只保留少量，并且配合 viewer distance 把它们转译成“冷感、距离、克制”。

### 风险 3：禁用 plan 只挡了 plan name，挡不住语义近亲

例如你禁用了 `theme_park_twilight`，但如果之后新增：

- `festival_date_evening`
- `cute_prize_corner`
- `romantic_cafe_window`
- `soft_couple_walk`

这些不会自动被禁用。  
后续最好增加 `PLAN_TAGS` 层面的禁用，比如：

```python
CHARACTER_FORBIDDEN_TAGS = {
    "星见雅": {"cute_date", "soft_romance", "idol_business", "theme_park"},
    "丹": {"idol_business", "loud_stage", "gacha_cute", "strong_flirt"},
}
```

这样比只按 plan name 更稳。

### 风险 4：每角色服装去重是“抽样尝试”，不是严格求解

`choose_character_plan_and_action()` 最多尝试 24 次找未用 outfit_direction。  
如果候选池被 recent tags / forbidden plans / 权重压缩得很小，有可能 fallback 到已用 theme。

这不是 bug，但要知道它是软约束。  
如果你想强约束，就要先构建候选池，再从未用集合里抽，而不是随机重试。

### 风险 5：旧的全局 clothing theme 函数还在文件里

`load_used_clothing_themes()`、`choose_unused_clothing_theme()`、`mark_clothing_theme_used()` 仍然保留。  
目前主流程已经改用 `used_by_character`，所以不影响运行。  
但以后继续迭代时容易误用旧函数。

建议加注释：

```python
# Legacy global clothing cycle. Kept for compatibility; production uses per-character cycle.
```

---

## 建议下一步修改

### 必改 1：给丹 / 星见雅加 strict plan whitelist

建议新增：

```python
STRICT_PLAN_CHARACTERS = {"丹", "星见雅", "仪玄"}

def _default_plan_weight_for(character: str) -> int:
    return 0 if character in STRICT_PLAN_CHARACTERS else CHARACTER_PLAN_WEIGHT_FLOOR
```

然后在 `choose_art_plan()` 中：

```python
default_weight = _default_plan_weight_for(character)
weight = weights_by_name.get(plan_name, default_weight)
```

这样新加场景不会自动污染丹 / 星见雅。

### 必改 2：加 forbidden tags

在 plan name 禁用之外，再加 tag 禁用：

```python
CHARACTER_FORBIDDEN_TAGS = {
    "丹": {"idol", "performance", "strong_flirt", "gacha", "theme_park"},
    "星见雅": {"cute", "soft_date", "idol", "domestic_daily", "theme_park"},
}
```

然后 `_allowed_plan_for_character()` 同时判断 plan name 和 tags。

### 建议改 3：prompt log 里追加 identity tokens 和 viewer distance

现在 prompt 里有，但 log 结构里最好也显式写出来，方便回看失败原因：

```json
"required_identity_tokens": [...],
"viewer_distance": "..."
```

这样你后面 review 图片时可以直接看：是 prompt 没带，还是模型没遵守。

### 建议改 4：小批量验证顺序

先不要直接跑 999。建议：

```bash
python chatgpt_batch_pyautogui.py --runs 12 --review-url
```

看 2 轮完整角色循环。  
如果丹和星见雅都稳定，再跑：

```bash
python chatgpt_batch_pyautogui.py --runs 24 --review-url
```

通过后再夜跑。

---

## 当前版本总体评分

| 项目 | 评分 | 说明 |
|---|---:|---|
| 角色主导逻辑 | 9/10 | 已从全局 theme 改成角色先行 |
| 丹身份防跑偏 | 8/10 | 硬 token 有效，但还需 strict whitelist |
| 星见雅身份防跑偏 | 8/10 | 兽耳 + 红瞳 + 剑客锚点有效，但软恋爱场景仍需防语义近亲 |
| 服装主题去重 | 7/10 | 每角色历史成立，但 24 次 fallback 是软约束 |
| 可维护性 | 7/10 | 旧全局 theme 函数仍保留，后续需标注 legacy |
| 实跑安全性 | 8/10 | 可以小批量跑，不建议直接 999 |

---

## 最终判断

这版是有效修复。  
它已经解决了上一轮最核心的结构性错误：不是“所有角色共享一个场景服装主题”，而是“每个角色按自己的人格、身份、viewer distance 和禁用规则进入不同企划”。

但如果目标是稳定生产丹 / 星见雅，下一刀应切在：

1. 丹 / 星见雅 strict whitelist
2. forbidden tags
3. prompt log 显式记录 identity tokens / viewer distance

这样才能防止未来新增场景时再次把她们带偏。
