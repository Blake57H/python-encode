from importlib.resources import path
import pathlib
from pathlib import Path
import subprocess
import os
import ffmpeg

def main(cmd: str):
    print(cmd)
    # exit(0)
    with subprocess.Popen(cmd) as proc:
        if proc.communicate()[0] is not None:
            print(proc.communicate()[0])
        if proc.communicate()[1] is not None:
            print(proc.communicate()[1])


if __name__ == "__main__":
    ffmpeg_path = r"ffmpeg\bin\ffmpeg"
    input_file = pathlib.Path()
    output_file = pathlib.Path().joinpath()
    cmd = f"{ffmpeg_path} -i \"{input_file}\" -map 0:v -map 0:a -b:a 96k -c:a libopus -c:v libx265 -color_primaries 1 -color_range 1 -color_trc 1 -colorspace 1 -crf 24.2 -map 0:s -map 0:t? -pix_fmt yuv420p -preset slow -profile:v main -vf smartblur=1.5:-0.35:-3.5:0.65:0.25:2.0,scale=1280:720:spline16+accurate_rnd+full_chroma_int -x265-params me=2:rd=4:subme=7:aq-mode=3:aq-strength=1:deblock=1,1:psy-rd=1:psy-rdoq=1:rdoq-level=2:merange=57:bframes=8:b-adapt=2:limit-sao=1:no-info=1 \"{output_file}\" -y"

    # main(ffmpeg_path+" -version")
    main(cmd)
