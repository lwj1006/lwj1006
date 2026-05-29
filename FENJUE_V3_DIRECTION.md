# 焚诀 3.0 develop 方向

更新时间：2026-05-29

当前 develop 是焚诀 3.0 起点，来源是主路径稳定版。上一轮 develop 已归档为：

`D:\workspace\auto-image-create\autoCreateV2`

## 核心定位

焚诀 3.0 是二次元角色传播系统，不再以 cinematic 概念图、AAA key visual、工业空间叙事或写实摄影逻辑为主。

第一目标：

- 停滑
- 点击
- 收藏
- 传播
- 强角色识别
- 强幻想感
- 强情绪价值

## 画面原则

- 角色是世界核心，空间从角色人格中生长出来。
- 情绪优先于现实合理性。
- 手机缩略图优先于细节欣赏。
- 角色脸、眼睛、发型大形、发饰、上半身和专属色彩必须先读到。
- 允许梦境空间、巨型月亮、漂浮 UI、爱心轨道、糖果天空、发光云层、超现实色彩。
- 幻想元素必须服务角色人格，不能随机堆砌。

## 禁止主方向

- western concept art
- UE5 宣传图
- 游戏 loading 图
- 复杂建筑空间
- 写实电影截图
- 角色被空间吞没
- 低气压废墟工业感

## 当前 V3 第一版代码状态

主要文件：

- `art_direction_options.py`
  - 覆写了 V3 active plan pool。
  - 计划池变为人格幻想/传播符号驱动。
  - action 变为 viewer interaction / 情绪关系语言。
- `art_direction_templates.py`
  - prompt 改为 Fenjue 3.0 社交平台二次元插画语气。
  - 强调头部二次元插画师视角，但不仿具体画师。
  - 强调角色世界核心、缩略图、幻想符号、viewer 关系。
- `chatgpt_batch_pyautogui.py`
  - 日志显示 V3 social anime character pipeline。
  - 默认不再复制文件到 `runtime_uploads`。

## 下一步可讨论

- 为每个角色建立更强的专属传播人格包。
- 增加恋爱感 / 偶像感 / 梦境感 / 神性幻想感的比例控制。
- 建立 thumbnail score 或 viral score。
- 针对小红书/Pixiv/头像封面分别做不同 prompt profile。
