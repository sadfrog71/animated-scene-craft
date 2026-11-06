# Animated Scene Craft — 3D Scene & Game Animation Agent Skill

[中文说明](README.zh-CN.md) · [Skill instructions](SKILL.md) · [MIT License](LICENSE)

An open-source **Codex agent skill for 3D scene creation, game animation, Blender workflows, and real-time animation integration**. It guides an AI coding agent from scene purpose and visual composition through motion design, editable assets, export checks, and actual playback review.

Use it to build or refine interactive environments, character and creature animation, animated props, architectural scenes, product presentations, or offline animation. The workflow is engine-agnostic; bundled execution helpers target Blender and FFmpeg. The skill instructions are currently written in Chinese; this README provides an English overview and usage examples.

## Visual approval and completion checks

For a new scene or a major art-direction change, the skill first generates actual ImageGen concept images, reviews them, and presents a recommended version for user confirmation before detailed or bulk production. Existing approved targets are reused. Explicit greybox-only tasks, technical prototypes, or requests to skip concepts keep their stated scope; silence is not approval.

Production compares three sources: the approved visual target, the previous actual render (when available), and the current actual render. Comparable viewpoints and game states make differences actionable. ImageGen paintovers may suggest improvements, but do not count as implementation evidence or silently replace the approved target.

Checks occur at greybox, representative integrated scene, and whole-delivery stages. Content, spatial composition, art finish, motion/interaction, and runtime fidelity receive separate PASS / PARTIAL / FAIL / BLOCKED conclusions with evidence. There is no invented overall completion percentage. See [visual completion workflow](references/visual-completion.md).

## What it improves

- **Intentional scenes:** derive composition, spatial relationships, close-up detail, and interaction reachability from what a viewer or player will do.
- **Motion with causes:** account for pivots, support, contact, direction, amplitude, timing, phase, and secondary motion instead of applying the same oscillation everywhere.
- **Gameplay-aware animation:** separate behavior, world movement, body pose, and visual feedback; define clip transitions, interruptions, and event timing without forcing a complex state machine on a simple loop.
- **Reproducible assets:** connect editable source files, export settings, post-processing, and runtime assets so a later export retains approved fixes.
- **Playback-based review:** inspect full actions or loops at normal speed, exercise real inputs, and distinguish a successful render from a visually convincing or playable result.
- **Measured optimization:** profile the target device before changing geometry, animation, shaders, or rendering architecture.

## When to use it

| Request | How the skill helps |
| --- | --- |
| Build an animated environment | Establish visual priorities, spatial coherence, object detail, and environmental motion |
| Improve character or creature movement | Coordinate locomotion, body deformation, transitions, and contact points |
| Animate interactive props or mechanisms | Connect input, state, motion, interruption, and completion feedback |
| Bring Blender animation into a game | Check the target format and loader, preserve pivots and clips, compare source and runtime playback |
| Produce an offline animation | Create editable source, render continuous frames, and review the encoded result |
| Build a playable game | Coordinate scene and animation work with available gameplay, input, collision, and QA skills |

This is a skill package, **not a game engine, asset library, autonomous game generator, or Blender MCP server**. It does not provide a universal asset exporter or automated aesthetic scoring. A still image, a successful build, and a working game are treated as different levels of evidence.

## Install in Codex

Requirements: Git for cloning; a Codex installation that loads local skills. Check that the destination does not already contain another copy before cloning.

```bash
git clone https://github.com/sadfrog71/animated-scene-craft.git ~/.codex/skills/animated-scene-craft
```

If your Codex installation uses a custom skill directory, clone into that directory instead. Start a new chat and check that `animated-scene-craft` is available. No MCP server, paid model-generation service, or additional engine is required by the package itself.

Already installed a local copy? Back up or compare your local changes before replacing it with this repository. For a Git-based installation, update with `git pull --ff-only` from its directory after reviewing local changes.

Other agent hosts may be able to read `SKILL.md`, but host-specific discovery, tool access, and automatic invocation have not been verified.

## Usage examples

### A first playable slice

> Use $animated-scene-craft to build a small browser game where a robot explores a room and pushes crates to open a passage. Use a stylized look, support desktop controls, and deliver one playable level. The existing project is at [path]. Reuse its engine and verify actual input and animation playback.

### Refine an existing character

> Use $animated-scene-craft to improve walking, turning, and landing in [project path]. Keep the existing art direction and gameplay. Check transitions, foot contact, interruptions, and actual playback before changing unrelated systems.

### Export an animated asset

> Use $animated-scene-craft with the attached Blender project to create idle, walk, and jump clips for my Godot game. Deliver editable source and runtime assets, and verify the imported motion in the target project.

### An animated product presentation

> Use $animated-scene-craft to create a short animation of this product opening and closing. Preserve the supplied model, emphasize joints and material detail, and deliver an editable Blender file plus a normal-speed preview.

Give the agent the project or source assets, intended activity, visual references, target device, and desired delivery stage. If you want a proposal only, say “design first; do not implement.” Missing implementation details can be resolved from the existing project.

## Workflow and delivery

1. Inspect available assets, the existing project, tools, target device, and authorized scope.
2. Generate and confirm visual targets when needed; establish observable visual priorities and motion/interaction needs.
3. Check the greybox, then finish a representative integrated scene or interaction before expanding content.
4. Verify source-to-runtime compatibility and any required export transformations.
5. Compare approved targets and actual renders; review normal-speed playback and player interactions on the target surface.
6. Deliver editable source or runnable output, necessary resource/version information, and clearly stated verification limits.

Deliverables depend on the request: `.blend` source, scene scripts, runtime assets, a runnable game or page, rendered frames, or a preview video. These are produced during a task; the repository does not include demonstration assets or a finished game.

## Included tools and requirements

| Resource | Purpose | Requirement |
| --- | --- | --- |
| `scripts/scene_tool.py probe` | Discover Blender, FFmpeg, and Node executables | Python 3 |
| `inspect` | Read scene cameras, object counts, timing, and selected missing dependencies | Blender |
| `run` | Execute a task-specific production script and save a separate project | Blender |
| `render` | Render selected frames or a continuous sequence | Blender |
| `encode` | Encode continuous frames as an H.264 preview | FFmpeg |

```bash
python3 scripts/scene_tool.py --help
python3 scripts/scene_tool.py probe
```

See [execution examples](references/execution.md) for full commands and output constraints. Python helpers use the standard library; Blender jobs run in Blender's Python environment. The helpers do not install software. Run only reviewed local production scripts: the runner is not a sandbox. Complex caches, all geometry defects, and visual quality are outside the `inspect` command's checks.

## Optional skill integrations

The execution guide routes to specialized skills only when installed and relevant: `scenario-blender-expert`, `environment-artist`, `set-dressing`, `imagegen`, `threejs-interaction`, `threejs-gameplay-systems`, `build-mobile-threejs-games`, and `threejs-qa-release`, among others.

Those packages are **not bundled or automatically installed**. Their availability and licenses are independent of this repository. Missing specialists should be reported and available project tools reused. Existing Unity, Unreal, Godot, native, or web projects keep their own toolchain; this skill does not require migration to Three.js.

## Repository map

- [SKILL.md](SKILL.md): core scene and animation decisions; Codex entry point.
- [references/execution.md](references/execution.md): tool selection and Blender/FFmpeg commands.
- [references/visual-completion.md](references/visual-completion.md): ImageGen concept approval, comparable evidence, stage checks, and completion criteria.
- [references/realtime-animation.md](references/realtime-animation.md): behavior/motion ownership, animation clips, reproducible exports, timing, performance, and playtesting.
- `scripts/scene_tool.py` and `scripts/blender_job.py`: execution helpers.
- `agents/openai.yaml`: Codex UI metadata and invocation configuration.

## Validation and contributions

Metadata and reference checks do not establish successful rendering or game performance. Validate changes at the appropriate level: CLI help and syntax for scripts, a representative Blender asset for export changes, and real gameplay for interaction changes. Include tool versions, expected versus observed behavior, and a small reproducible example when reporting a problem. Do not upload private projects, credentials, or assets without redistribution rights.

Contributions that improve reusable decisions, reproducibility, or observable verification are welcome. Keep project-specific conventions out of general instructions and avoid adding dependencies without a demonstrated need.

## License

[MIT](LICENSE) applies to this repository's instructions and helper code. Blender, FFmpeg, engines, external skills, models, textures, and other inputs retain their own licenses. This license does not grant rights to third-party assets.
