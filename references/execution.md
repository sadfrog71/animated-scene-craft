# 软件、技能与执行路线

开始时定位本技能目录为 `SKILL_DIR`。以下 shell 示例中的项目和输出路径需替换为真实绝对路径；含空格的路径必须引用。不依赖某个用户目录。Python 脚本仅使用标准库；`blender_job.py` 由 Blender 内置 Python 执行。

## 1. 先检查再选工具

需要 Blender 制作或视频编码时再运行环境检查；仅修改现有引擎代码时，直接检查该工程。

```bash
python3 "$SKILL_DIR/scripts/scene_tool.py" probe
```

输出 Blender、FFmpeg、Node 的可执行路径与版本；缺失为 null，不自动安装。版本仅用于选择兼容 API，不代表性能已验证。可在子命令前传 `--blender "/path/to/blender"` 或 `--ffmpeg "/path/to/ffmpeg"`。

按实际交付选择一条主路线，辅助技能按需读取，不把表中技能全部加载。名称以当前可用技能清单为准；缺失时说明缺口，用已有工具完成可行部分，不自动安装。

| 路线 | 工具与技能调用 | 具体产物 |
| --- | --- | --- |
| 概念与风格 | 多视角时用 `game-scene-visual-exploration`；生成或修改栅格图时用 `imagegen` 与实际图像工具 | 参考图、提示词、空间约束；不是模型 |
| 三维场景和离线动画 | 先读 `scenario-blender-expert`，核对当前 Blender 版本与相关 API；环境构建按需读 `environment-artist`，布置关键物件按需读 `set-dressing` | 场景制作脚本、可编辑 .blend、镜头与动画 |
| 程序化或贴图专项 | 只有任务需要时读 `scenario-blender-geometry-nodes` 或 `scenario-blender-uv-baking` | 共享几何、材质、UV 或烘焙结果 |
| 网页实时场景 | 在已有 Three.js 工程里接入；有拾取、镜头或触控需求时读 `threejs-interaction`；定向视觉提升可用 `threejs-aaa-graphics-builder` | 可运行页面、资源及实际交互证据 |
| 可玩 Three.js 游戏 | 核心玩法、关卡、碰撞按需用 `threejs-gameplay-systems`；移动端整体制作可用 `build-mobile-threejs-games`；完成后用 `threejs-qa-release` 验证实际玩法 | 输入、规则、动作反馈与结束/重试或持续状态构成可玩流程；复用现有工程，不重复搭架子 |
| 固定视角图层动画 | 先明确它与三维的差异；图像工具生成底图，现有渲染器实现遮罩、局部运动与宿主控制 | 底图、遮罩、参数及运行页面；不是自由视角模型 |
| 引擎或原生应用 | 沿项目现有 Unity、Unreal、Godot 或原生工程与资源管线；查其实际版本和本地指南 | 引擎资源或宿主集成，不因本技能改换平台 |

工具选择依据当前工程、编辑需求、资产适配和目标设备，不依据插件数量。MCP、脚本或编辑器操作都是执行通道，不能代替质量验收。生成式 3D 资产先检查轮廓、拓扑、绑定适配、尺度与使用许可；只为具体资产缺口引入，不承诺生成后即可用于游戏。

`threejs-qa-release` 只在相应游戏验证/发布任务需要时使用，不为了查看一个场景自动启动发布流程。概念图和材质参考不能代替实际模型渲染。

## 2. 检查已有 Blender 场景

```bash
python3 "$SKILL_DIR/scripts/scene_tool.py" inspect \
  --blend "/project/source.blend" --out "/project/evidence/inspect-v001"
```

读取场景相机、对象数量、时间范围、帧率、引擎、尺寸、缺失的普通外部图片与链接库，输出 `report.json`。不修改或保存源工程。不包括 UDIM/图像序列、字体、模拟缓存和全部几何问题，不能称为完整资产审计。

需要网格结构检查时复用 `scenario-blender-expert/scripts/bx_audit.py`，按该脚本实际接口指定重点对象；需要轮廓、多视角模型检查或已有 playblast 能力时复用 `bx_review.py`。不要把角色拓扑阈值套在建筑、植物或有意开放的曲面上。

## 3. 编写本场景制作脚本并执行

制作脚本是任务成果的一部分，不由通用入口凭空生成。依据 SKILL.md 的制作判断，用 `bpy` 实现：

1. 识别现有对象、集合、材质、相机与动画，建立本次改动的命名范围；新场景建立基础尺度、主体与机位。
2. 先做主要形体、空间与接触关系，渲染确认后再做关键物件、材质和细节。局部优化不重建无关对象。
3. 对需运动的对象设置合理原点、父子关系、约束和驱动；按运动来源选择关键帧、骨骼、节点、着色器或模拟，静态对象不误加动画。
4. 在任务脚本中明确相机、帧率、时间范围、渲染器与必要灯光；不依赖启动文件中的默认立方体或灯光。
5. 读取当前 API 文档或所用技能的版本说明。遇到接口错误先核对版本，不连续猜测参数。脚本不覆盖输入文件、不写无关目录。

```bash
python3 "$SKILL_DIR/scripts/scene_tool.py" run \
  --blend "/project/source.blend" \
  --script "/project/scripts/refine_scene.py" \
  --out "/project/versions/v002"
```

从零创建时省略 `--blend`，工作进程从空场景开始。脚本可用注入的 `SCENE_OUTPUT_DIR` 保存本轮辅助产物。执行成功后入口另存 `scene.blend` 并生成报告。

该入口运行已审阅的本地 Python，不是代码沙箱；`--disable-autoexec` 只禁用工程加载时自动脚本，不阻止显式任务脚本自行写文件。不要对不可信脚本直接执行。

输出目录必须不存在，避免覆盖历史。失败时保留请求和日志，查看 `blender.log`，查明原因后用新的版本目录重试；不把失败输出当成可用成品。默认两个 CPU 线程，不宣称限制内存或 GPU；大型工程先用局部场景和低分辨率试跑，沿用项目已有资源预算工具。本入口每次运行一个 Blender 进程，调用方不要并行启动多个重任务。

## 4. 渲染可比较的静帧与动画

选取 inspect 中实际存在的相机名称。脚本保持工程材质与灯光，覆盖本次输出分辨率；不保存这些预览设置到源文件。

```bash
python3 "$SKILL_DIR/scripts/scene_tool.py" render \
  --blend "/project/versions/v002/scene.blend" --camera "Camera_Main" \
  --frames "1,24,48" --width 960 --height 540 \
  --out "/project/evidence/stills-v002"
```

`--frames "1:48"` 表示逐帧渲染闭区间；逗号列表用于抽帧。`--engine workbench` 用于几何、构图和基本运动检查，不能证明最终材质、透明、烟雾或光照效果；默认 `current` 使用工程引擎。

```bash
python3 "$SKILL_DIR/scripts/scene_tool.py" render \
  --blend "/project/versions/v002/scene.blend" --camera "Camera_Main" \
  --frames "1:48" --width 640 --height 360 \
  --out "/project/evidence/motion-v002"
python3 "$SKILL_DIR/scripts/scene_tool.py" encode \
  --frames "/project/evidence/motion-v002/frames/frame_%06d.png" \
  --start 1 --fps 24 --output "/project/evidence/motion-v002.mp4"
```

示例 24 fps 必须换成场景报告中的真实帧率，含小数帧率；不能通过加快播放掩盖运动过小。编码仅接受连续帧序列，不能把稀疏抽帧伪装成正常速度动画。动态模拟应先在制作流程中正确缓存/烘焙；从中间帧启动或跳帧不保证模拟正确。入口不会自动烘焙或改变模拟。

FFmpeg 输出 H.264 MP4，不覆盖既有文件；奇数宽高只在右/下边补齐到偶数。输出不自动附加音轨。需要声音时沿用户要求和现有音频流程处理。

## 5. 实时制作与验证

复用工程现有启动、构建和资源导入方式，不新造第二套应用。涉及动作制作、导出或游戏接入时，按 [实时动画制作与接入](realtime-animation.md) 核对职责与兼容性；工具脚本的 inspect 不覆盖这些检查。将已确认模型或底图导入后：

- 为动画设置明确的时间推进与暂停状态；按真实对象挂点与空间关系实现动态。
- 界面文字、操作、业务数据与场景分层，宿主控制可见性、暂停、减少动态和音频；不要在场景内复制账号或业务体系。
- 用当前可用浏览器工具打开实际运行入口，检查加载、镜头、目标尺寸与交互，保存截图及正常速度实播。静态截图只能证明对应画面。
- 原生或其他引擎场景到对应设备验证，不用网页上的成功替代。无目标设备时记录验证缺口，交付可复现入口。

不存在能通用于所有引擎的可靠“自动审美验收”脚本。自动检查负责资源和运行状态；主动查看静帧、实播片段和真实使用流程，才是本技能要求的效果验收。
