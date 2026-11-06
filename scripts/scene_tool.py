#!/usr/bin/env python3
"""Standard-library CLI for local scene work. Never installs software."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def binary(name, override=None):
    if override:
        path = Path(override).expanduser()
        if not path.is_file():
            raise ValueError(f'Executable not found: {override}')
        return str(path.resolve())
    candidates = [shutil.which(name)]
    if name == 'blender':
        candidates += ['/Applications/Blender.app/Contents/MacOS/Blender']
        root = Path(os.environ.get('PROGRAMFILES', 'C:/Program Files')) / 'Blender Foundation'
        if root.exists():
            candidates += [str(p) for p in sorted(root.glob('Blender */blender.exe'), reverse=True)]
    for item in candidates:
        if item and Path(item).is_file():
            return str(Path(item).resolve())
    if override:
        raise ValueError(f'Executable not found: {override}')
    return None


def existing(value):
    p = Path(value).expanduser().resolve()
    if not p.is_file():
        raise ValueError(f'File not found: {p}')
    return str(p)


def execute(command, log=None):
    print(json.dumps({'command': command}, ensure_ascii=False), flush=True)
    if log:
        with open(log, 'w', encoding='utf-8') as stream:
            result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
    else:
        result = subprocess.run(command)
    if result.returncode:
        raise RuntimeError(f'Process exited {result.returncode}; log: {log}')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--blender', help='Blender executable override')
    p.add_argument('--ffmpeg', help='FFmpeg executable override')
    sub = p.add_subparsers(dest='mode', required=True)
    sub.add_parser('probe')
    for mode in ('inspect', 'render', 'run'):
        q = sub.add_parser(mode)
        q.add_argument('--blend', required=mode != 'run')
        q.add_argument('--out', required=True, help='New output directory; existing paths refused')
        q.add_argument('--threads', type=int, default=2)
        if mode == 'run':
            q.add_argument('--script', required=True, help='Task-specific bpy script, already reviewed')
        if mode == 'render':
            q.add_argument('--camera', help='Exact camera name; defaults to active scene camera')
            q.add_argument('--frames', required=True, help='Comma-separated frame numbers or inclusive start:end')
            q.add_argument('--width', type=int, default=640)
            q.add_argument('--height', type=int, default=360)
            q.add_argument('--engine', choices=['current', 'workbench'], default='current')
    q = sub.add_parser('encode')
    q.add_argument('--frames', required=True, help='PNG pattern, e.g. /abs/frames/frame_%%06d.png')
    q.add_argument('--start', type=int, required=True)
    q.add_argument('--fps', type=float, required=True)
    q.add_argument('--output', required=True)
    args = p.parse_args()
    if args.mode == 'probe':
        report = {'python': sys.version.split()[0], 'tools': {}}
        for name in ('blender', 'ffmpeg', 'node'):
            path = binary(name, getattr(args, name, None))
            version = None
            if path:
                flag = '-version' if name == 'ffmpeg' else '--version'
                r = subprocess.run([path, flag], capture_output=True, text=True, timeout=20)
                version = (r.stdout or r.stderr).splitlines()[0] if (r.stdout or r.stderr) else None
            report['tools'][name] = {'path': path, 'version': version}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    if args.mode == 'encode':
        exe = binary('ffmpeg', args.ffmpeg)
        if not exe:
            raise ValueError('FFmpeg missing; install is not performed')
        out = Path(args.output).expanduser().resolve()
        if out.exists() or args.fps <= 0:
            raise ValueError('Output must be new; fps must be positive')
        out.parent.mkdir(parents=True, exist_ok=True)
        execute([exe, '-hide_banner', '-loglevel', 'error', '-n', '-framerate', str(args.fps),
                 '-start_number', str(args.start), '-i', str(Path(args.frames).expanduser().resolve()),
                 '-c:v', 'libx264', '-crf', '20', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2',
                 '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out)])
        return
    exe = binary('blender', args.blender)
    if not exe:
        raise ValueError('Blender missing; install is not performed')
    if args.threads < 1:
        raise ValueError('threads must be positive')
    request = vars(args).copy()
    if args.blend:
        request['blend'] = existing(args.blend)
    if args.mode == 'run':
        request['script'] = existing(args.script)
    if args.mode == 'render':
        if args.width < 1 or args.height < 1:
            raise ValueError('resolution must be positive')
        if ':' in args.frames:
            start, end = map(int, args.frames.split(':'))
            if end < start:
                raise ValueError('end must be >= start')
            frames = list(range(start, end + 1))
        else:
            frames = list(dict.fromkeys(int(x) for x in args.frames.split(',')))
        request['frame_list'] = frames
    out = Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=False)
    request['out'] = str(out)
    path = out / 'request.json'
    path.write_text(json.dumps(request, indent=2), encoding='utf-8')
    command = [exe, '--background', '--factory-startup', '--disable-autoexec', '--threads', str(args.threads)]
    if args.blend:
        command.append(request['blend'])
    command += ['--python-exit-code', '1', '--python', str(HERE / 'blender_job.py'), '--', str(path)]
    execute(command, out / 'blender.log')
    print(json.dumps({'output': str(out), 'report': str(out / 'report.json')}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
