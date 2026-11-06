"""Blender worker. Invoke through scene_tool.py, not system Python."""
import json
from pathlib import Path
import runpy
import sys
import bpy

request = json.loads(Path(sys.argv[sys.argv.index('--') + 1]).read_text())
out = Path(request['out'])
mode = request['mode']
if mode == 'run':
    if not request.get('blend'):
        bpy.ops.wm.read_factory_settings(use_empty=True)
    # A task script may use SCENE_OUTPUT_DIR; it must not overwrite its source.
    runpy.run_path(request['script'], init_globals={'SCENE_OUTPUT_DIR': str(out)}, run_name='__main__')
    bpy.ops.wm.save_as_mainfile(filepath=str(out / 'scene.blend'), copy=True)

scene = bpy.context.scene
report = {
    'blender_version': bpy.app.version_string,
    'source': request.get('blend'),
    'scene': scene.name,
    'objects': len(scene.objects),
    'cameras': [obj.name for obj in scene.objects if obj.type == 'CAMERA'],
    'active_camera': scene.camera.name if scene.camera else None,
    'frame_range': [scene.frame_start, scene.frame_end],
    'fps': scene.render.fps / scene.render.fps_base,
    'resolution': [scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage],
    'engine': scene.render.engine,
    'missing_external_images': [],
    'missing_libraries': [],
    'scope': 'Inventory only; not geometry, simulation-cache or visual acceptance',
}
for im in bpy.data.images:
    if im.source == 'FILE' and im.filepath and not im.packed_file:
        path = Path(bpy.path.abspath(im.filepath, library=im.library))
        if not path.is_file():
            report['missing_external_images'].append({'name': im.name, 'path': str(path)})
for lib in bpy.data.libraries:
    path = Path(bpy.path.abspath(lib.filepath))
    if not path.is_file():
        report['missing_libraries'].append(str(path))
if mode == 'render':
    name = request.get('camera')
    if name:
        camera = scene.objects.get(name)
        if camera is None or camera.type != 'CAMERA':
            raise ValueError(f'Camera not found in active scene: {name}')
        scene.camera = camera
    if scene.camera is None:
        raise ValueError('No active camera; specify --camera from inspect output')
    if request['engine'] == 'workbench':
        scene.render.engine = 'BLENDER_WORKBENCH'
    scene.render.resolution_x = request['width']
    scene.render.resolution_y = request['height']
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.use_file_extension = True
    frames_dir = out / 'frames'
    frames_dir.mkdir()
    files = []
    for frame in request['frame_list']:
        scene.frame_set(frame)
        target = frames_dir / f'frame_{frame:06d}.png'
        scene.render.filepath = str(target)
        bpy.ops.render.render(write_still=True)
        if not target.is_file():
            raise RuntimeError(f'Render missing: {target}')
        files.append(str(target))
    report['render'] = {'camera': scene.camera.name, 'engine': scene.render.engine,
                        'size': [request['width'], request['height']], 'frames': files,
                        'note': 'Workbench is geometry preview, not final material or lighting proof'}
report['output_blend'] = str(out / 'scene.blend') if mode == 'run' else None
(out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('SCENE_JOB ' + json.dumps({'mode': mode, 'report': str(out / 'report.json')}))
