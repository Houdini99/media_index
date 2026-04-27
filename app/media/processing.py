"""File-type detection, hashing, and thumbnail generation.

Pure I/O helpers — no Flask, no SQL.
"""
import hashlib
from PIL import Image, ImageSequence
from moviepy import VideoFileClip

from ..config import Config


def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    return ext in (Config.ALLOWED_IMAGE_EXT | Config.ALLOWED_GIF_EXT | Config.ALLOWED_VIDEO_EXT)


def file_type(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext in Config.ALLOWED_IMAGE_EXT:
        return "image"
    if ext in Config.ALLOWED_GIF_EXT:
        return "gif"
    if ext in Config.ALLOWED_VIDEO_EXT:
        return "video"
    return "unknown"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def gen_image_thumb(src, dst):
    try:
        img = Image.open(src)
        if img.format == 'GIF':
            frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
            frame = frames[0]
            frame.thumbnail(Config.THUMB_SIZE)
            frame.save(dst, format='PNG')
        else:
            img.thumbnail(Config.THUMB_SIZE)
            img.save(dst, format='PNG')
        return dst
    except Exception:
        return gen_placeholder_thumb(dst)


def gen_video_thumb(src, dst):
    clip = None
    try:
        clip = VideoFileClip(src)
        dur = clip.duration
        for t in (2, dur / 2, 1, dur / 3):
            if 0 <= t <= dur:
                try:
                    frame = clip.get_frame(t)
                    img = Image.fromarray(frame)
                    img.thumbnail(Config.THUMB_SIZE)
                    img.save(dst, format='PNG')
                    break
                except Exception:
                    continue
        else:
            frame = clip.get_frame(min(0.1, dur))
            img = Image.fromarray(frame)
            img.thumbnail(Config.THUMB_SIZE)
            img.save(dst, format='PNG')
        return dst
    except Exception:
        return gen_placeholder_thumb(dst)
    finally:
        if clip:
            try:
                clip.reader.close()
            except Exception:
                pass
            if hasattr(clip, 'audio') and clip.audio:
                try:
                    clip.audio.reader.close_proc()
                except Exception:
                    pass


def gen_placeholder_thumb(dst):
    img = Image.new('RGB', Config.THUMB_SIZE, (32, 48, 32))
    img.save(dst, format='PNG')
    return dst
