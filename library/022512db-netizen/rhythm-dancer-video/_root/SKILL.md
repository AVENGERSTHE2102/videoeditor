---
name: rhythm-dancer-video
description: 把一张角色定妆照做成“绿幕舞蹈 + 节拍可视化舞台”的网页和可发布 MP4（Claudia Explains / Rhythm Girl 那类帖子的做法）：图生视频模型（默认 muse2api，可换 Kling/Wan/Veo/Seedance 等任意支持首帧的模型）生成绿幕首帧和链式连续舞蹈，WebGL 实时抠像，Web Audio 合成欧几里得节奏鼓组，表盘/灯光/镜头踩鼓点，Playwright 逐帧导出。用于“复刻那个跳舞+节奏表盘的视频”“让某个角色在舞台上跟鼓点跳舞”“换角色/换节奏/重新导出”。不用于纯代码画人物动画，也不用于普通短剧镜头生产。
---

# Rhythm Dancer Video

核心思路：**舞蹈交给视频模型，代码只做它擅长的**（抠像、节拍、HUD、灯光、镜头、导出）。不要尝试用 SVG/骨骼手写舞蹈，也不要为了卡点去变速/倒放舞蹈——那样会一顿一顿（已验证失败）。舞蹈原速连续播放，鼓点驱动的是灯光、表盘、光环、镜头和人物光晕。

## 视频模型：不绑定 Muse

流程对模型只有这几条要求，满足就能替换：

1. **图生视频且首帧可控**：能以给定图片作为第一帧（first frame / image-to-video）。只支持“参考图风格”而不锁首帧的模型做不了链式接缝。
2. **单段 ≥5 秒、全身入镜、静止机位**，并能保持纯绿背景（提示词里写明；生成后抽帧检查）。
3. **角色一致性**：多段之间人物不走样。弱的模型要在每段提示词里重复外观描述（`--look` 已自动做）。
4. 能拿到 mp4 文件。

不要求模型懂节拍：舞蹈本来就不踩点，鼓点由页面负责。

- 默认后端是 muse2api（`muse_client.py`）。
- 换模型：`chain_dance.py --generator '命令模板'`，每段调用一次，占位符 `{first}` 首帧图、`{prompt_file}` 提示词文件、`{out}` 输出 mp4、`{seconds}`、`{ratio}`；命令写出 `{out}` 并返回 0 即可。为新模型写个小包装脚本即可，其余步骤（拼接、抠像、导出）不变。
- 绿幕首帧同理：任何图生图/编辑模型都行（如 `image-gen` skill），只要产出全身、纯绿背景、同一角色的图；`make_greenscreen.py` 只是 Muse 版本。
- 已知差异：各模型对“纯绿背景”的服从度不同，背景出现渐变/地面阴影时调高抠像阈值（见 pitfalls）；部分模型单段只有 5 秒，段数相应翻倍。

## 付费与确认边界

- 每张绿幕首帧 1 次生图，每段新 clip 1 次生视频（Muse 用账号免费周额度；其他模型可能按次扣费）。**生成前告诉用户要生成几次并取得确认**；已有的 clip 会被复用，失败后重跑不会重复生成。
- 角色若有授权限制（例如非商用、需署名），交付时提醒。
- 任何后端的密钥都只从环境变量或本地 `.env` 读取（Muse：`MUSE2API_KEY` / `MUSE2API_ENV`），不得打印、写入代码、提示词文件或回复。

## 环境

- muse2api（默认后端）：`MUSE2API_BASE`，需自行部署 muse2api 并设置该变量。用前先 `GET /v1/models` 确认鉴权通。
- 本机需要 `ffmpeg`、Python3 + `opencv-python` + `numpy`、Node + `playwright` 包（浏览器优先用 `~/Library/Caches/ms-playwright` 里已有的 Chromium，不需要 `playwright install`）。
- 脚本都在 `scripts/`，用 `python3 <skill>/scripts/xxx.py` 调用（`muse_client.py` 与它们同目录，自动导入）。

## 流程

1. **建舞台目录**：`python3 scripts/new_stage.py OUT_DIR` 复制 `assets/stage/index.html` 和一份 `stage.json`。改 `stage.json` 的标题、BPM、段落（欧几里得节奏与字幕）、素材文件名。字段说明见 [references/stage-config.md](references/stage-config.md)。
2. **绿幕首帧**（1 次生图）：`python3 scripts/make_greenscreen.py 定妆照 OUT_DIR/poster.png --look "英文外观描述"`。必须看图确认：人物一致、全身含脚、背景纯绿、手不交叉（便于起舞）。
3. **链式舞蹈**（N 次生视频）：`python3 scripts/chain_dance.py OUT_DIR/poster.png OUT_DIR/clips --look "同上" --move "第1段编舞" --move "第2段" ... [--generator ...]`。段数 ≈ 循环时长 / 10 秒（默认 5 段×4 小节×120BPM = 40 秒 → 4 段）。编舞按段落情绪写：起舞 → 加速 → 高潮转圈 → 收尾定格。每段生成后抽帧检查人物是否走样。
4. **拼接**：`python3 scripts/join_clips.py OUT_DIR/clips/clips.json OUT_DIR/dancer.mp4 --length <循环秒数>`。会报告每个接缝与正常帧差的比值，标 `visible jump` 的需要重生成那一段。
5. **预览**：在 OUT_DIR 起 `python3 -m http.server`，浏览器打开 `index.html`（不能 file://，WebGL 读视频会被跨域拦截）。`?autoplay` 自动播放，空格暂停。
6. **导出**：`node scripts/render.mjs OUT_DIR OUT.mp4 [--secs N] [--size 1920x1080]`（首次在 `scripts/` 里 `npm i` 安装 playwright）。先 `--secs 6` 试渲染并抽帧看，再导全长。约 10–15 帧/秒。
7. **交付**：说明已验证项（抽帧、接缝数值、音量）与未验证项（是否完整看/听过）。


## 工作流变体：Video-First & 原生音视频联动（推荐）

如果图生视频模型自身具备生成音轨或原声语音能力（例如 Google Veo 3.1 R2V 系列）：

1. **先出片后造台**：不预设死板的节拍和舞台模板，先让模型根据角色参考图与舞种提示词自由生成一段连贯生动的绿幕舞蹈（含原生音轨）。
2. **提取原声音效与动作事件**：
   - 使用 `ffmpeg` 提取视频原生音轨；
   - 通过频谱分析提取低频打击点（底鼓）、高频清脆节拍（军鼓/镲片）与中频人声发声点（如萌点台词）；
   - 生成对应的 `cues.json`。
3. **因舞定台**：
   - 提取角色身上的专属视觉符号（例如角色配饰、发色对应的粒子与霓虹辉光）；
   - 在独立舞台模板中配置粒子系统、光柱角度与地面接触波纹，使其完全由原生音轨的声学事件触发联动；
4. **渲染合成**：使用 `render.mjs` 输出 1080p 高清成片。


## 配乐（推荐）

- `python3 scripts/detect_tempo.py STAGE/dancer.mp4 STAGE/tempo.json`：从角色动作估出 BPM 和第一拍位置。
- `python3 scripts/compose_song.py STAGE`：在固定拍网格上作一首完整曲子（鼓、贝斯、和弦、琶音、主旋律、加花），同时写 `cues.json` 驱动舞台。
- 不要把鼓点直接放在动作峰值上：间隔不稳，听起来像噪声（已验证失败）。
- 视频模型自带音轨可直接用，也可去掉后用上面的作曲替换；片尾若有突然推镜，拼接前先剪掉。

## 常见坑（Muse 专有，遇到时读 references/pitfalls.md）

- 视频首帧走 multipart 时曾生成了完全不同的角色；`muse_client.video()` 已固定用 JSON `reference_image`。
- “模型只返回文本”可重试；“muse.ai 页面加载超时”连续出现时重试无用，需要重启服务器上的 muse2api。
- 详细排障、调参与已知限制见 [references/pitfalls.md](references/pitfalls.md)。
