# 焚诀提示词模式复查 Feedback

日期：2026-06-08

## 结论

新加入的 A/B 入口整体可用。A 模式保持原先稳定模板，B 模式会在运行时切换到新的「场景 / 摄影师 / 人物 / 服装」四块摄影师模板，没有直接改动原启动入口。

目前建议：可以继续保留 B 模式作为实验入口，但不要急着把它替换成默认生产模板。B 模式结构是对的，已修正第一轮发现的主要误导措辞；剩余主要观察点是提示词长度偏长，跑图后需要看服装权重和构图权重是否被稀释。

## 已自测项目

1. 新文件语法检查通过：
   - `photographer_prompt_templates.py`
   - `fenjue_prompt_mode_launcher.py`

2. A/B 入口逻辑检查通过：
   - A 模式：保持 `chatgpt_batch_pyautogui` 原始 `prompt_for_art_direction`
   - B 模式：运行时 monkeypatch 到 `photographer_prompt_templates.prompt_for_art_direction`
   - 原 `start_fenjue_v3.bat` 没有被改动

3. B 模式抽样 200 条提示词：
   - 覆盖 24 个 plan
   - 每条都包含且只包含一次：
     - `[SCENE]`
     - `[PHOTOGRAPHER]`
     - `[CHARACTER]`
     - `[OUTFIT]`
   - 修正后抽样长度范围：4279 到 4941 字符
   - 修正后平均长度：4579 字符
   - 修正后误导项检查：0 项

4. 服装删除清单复查通过：
   - 目标服装名已从当前代码中移除
   - `hosiery_tea_room` 也已移除

5. 杯子/手部风险复查：
   - 没再发现明显正向鼓励“手拿杯子 / 放下杯子 / 拿玻璃杯 / 拿瓶子”的描述
   - 当前模板有明确负面约束：不要让手拿杯子、马克杯、饮用玻璃杯、瓶子、饮料容器

## 已修正风险点

### 1. `photograph-like anime key visual` 可能误导成写实

B 模式开头现在有一句：

```text
Create one coherent photograph-like anime key visual with one character.
```

问题是用户想要的是“像摄影师一样组织画面”，不是让图像变成真人摄影或半写实摄影。`photograph-like` 可能被其他模型理解为 photorealistic / realistic photo。

已改成：

```text
Create one coherent photographer-composed anime key visual with one character, not photorealistic.
```

### 2. 反射类场景有“额外人物”误判风险

当前 plan 里有 mirror / reflection / acrylic / glass 等元素。模板负面词也写了 `Avoid: extra people`。

这不是严格矛盾，但模型可能把“镜中反射”画成第二个人，尤其是：
 - `trend_mirror_studio`
 - `greenhouse_terrace_reflection`
 - `transparent_acrylic_display_wall`
 - `mirror_fragment_corner`

已在反射相关场景中补一句：

```text
Reflections may show abstract fragments or partial echoes only, never a second character or duplicate person.
```

### 3. 海报字块和“禁止文字”存在轻微冲突

`graphic_poster_studio` 这类 plan 会出现：

```text
large unreadable letter blocks
decorative non-readable letters
```

但负面约束里同时有：

```text
text, watermark
```

用户之前喜欢 Ellen Joe 那张海报感，但图像模型容易把“letter blocks”理解成真实英文、角色名、Logo 或品牌字。

已在海报 / 字块相关场景中补一句：

```text
Typography-like shapes must be abstract graphic blocks with no readable words, letters, logos, or brand text.
```

### 4. “手保持 empty”不应误伤自然动作

原约束：

```text
Hands stay simple, empty, and anatomically readable.
```

这里的 empty 本意是“不拿物体”，不是“不允许手碰头发 / 扶栏 / 放在桌面”。为了避免模型把手画得僵硬，已改成：

```text
Hands stay simple, empty of objects, and anatomically readable.
```

## 剩余观察点

### 1. 提示词整体偏长

B 模式修正后平均约 4579 字符，最长接近 4941 字符。结构清楚，但会带来两个风险：

 - 后段服装或负面约束权重被稀释
 - 模型可能只抓住最显眼的词，比如 white、photo、reflection、letter

建议下一轮压缩目标：

 - B 模式控制在 3200 到 3800 字符
 - `[SCENE]` 和 `[PHOTOGRAPHER]` 可以保留，但每项字段再短一点
 - 人物身份和服装主结构不要压太狠

## 当前清单状态

新增文件：

 - `photographer_prompt_plans.py`
 - `photographer_prompt_templates.py`
 - `fenjue_prompt_mode_launcher.py`
 - `start_fenjue_prompt_mode.bat`

已修改文件：

 - `art_direction_options.py`
 - `art_direction_templates.py`
 - `config/runtime_art_direction.json`

这些修改包含：

 - 删除指定服装与 `hosiery_tea_room`
 - 降低白色 / 奶油色 / 象牙白服装默认倾向
 - 降低人物手拿杯子、玻璃杯、瓶子的概率
 - 新增 B 模式摄影师结构，但通过新启动入口进入
 - B 模式已改为使用独立摄影师专用 plan 池，不再复用原本的场景 / 动作 / 构图抽样池

## B 模式专用 Plan 更新

新增 `photographer_prompt_plans.py`，只给 B 模式调用。A 模式和原 `art_direction_options.py` 的抽样逻辑不变。

B 模式现在分成三层：

 - 摄影师场景 plan：门框观察、低机位前景、高机位空间、长焦隔物、窗边半遮挡、街角动线、棚拍负空间、走廊透视、反射碎片、天台宽景
 - 摄影师动作 plan：转身前一瞬、横穿画面、半遮挡观察、边缘回头、光束中停顿、坐姿斜线重心、整理头发或袖口、注意力留在环境里
 - 摄影师构图 plan：门框切割、低前景压迫、高角度地面图形、长焦层叠观察、负空间边缘主体、反射碎片裁切、消失点行走

B 模式启动后会追加摄影师场景分类选择：

 - `1`：棚拍 / 杂志 / 摄影棚
 - `2`：室内 / 小说CG / 空间感
 - `3`：明亮日常 / 店铺 / 街区
 - `0`：全随机摄影师场景

也支持命令行直接选择，例如 `python fenjue_prompt_mode_launcher.py B 2`。

修正后抽样 300 条：

 - A 模式仍保持原模板
 - B 模式模板名：`fenjue_v6_photographer_dedicated_plans`
 - B 模式每条都有 `[SCENE]` / `[PHOTOGRAPHER]` / `[CHARACTER]` / `[OUTFIT]`
 - B 模式误导项检查：0 项
 - 抽样长度范围：4388 到 4942 字符
 - 平均长度：4601 字符

## 建议下一步

1. 先用 B 模式跑图，观察构图、服装权重、人物动作是否比 A 模式更像摄影师出图。
2. 如果 B 模式构图有效但提示词过长，下一轮把 B 模式压缩到 3200 到 3800 字符。
3. 如果 B 模式稳定，再考虑把 plan 压缩成用户想要的三类场景体系。
