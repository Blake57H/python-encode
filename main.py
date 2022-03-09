from importlib.resources import path
import pathlib
from pathlib import Path
import subprocess
import os
import ffmpeg

def my_encode_profiles():
    """
    Basically SSA's settings, but softsubs.
    I heard that 'libopus' can achieve the same audio quality with less bitrate. I cannot confirm but my
    eyes and ears are okay with these settings.
    """
    ffmpeg_arguments = {
        'c:a': 'libopus',
        'c:v': 'libx265',
        'b:a': '96k',
        'profile:v': 'main',
        'x265-params': ':'.join(['me=2', 'rd=4', 'subme=7', 'aq-mode=3', f'aq-strength=1', f'deblock=1,1', f'psy-rd=1', f'psy-rdoq=1', 'rdoq-level=2', 'merange=57', 'bframes=8', 'b-adapt=2', 'limit-sao=1', 'no-info=1']),
        'crf': 24.2,
        'preset': 'slow',
        'pix_fmt': 'yuv420p',
        'vf': ','.join(['smartblur=1.5:-0.35:-3.5:0.65:0.25:2.0', 'scale=1280:720:spline+accurate_rnd+full_chroma_int']),
        'color_range': 1,
        'color_primaries': 1,
        'color_trc':  1,
        'colorspace': 1,
    }
    return ffmpeg_arguments


def main():
    ffmpeg_path = r"ffmpeg\bin\ffmpeg"
    input_file = pathlib.Path()  # folder to watch
    output_file = pathlib.Path()  # output folder


if __name__ == "__main__":
    # main(ffmpeg_path+" -version")
    main()
