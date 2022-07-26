from datetime import datetime, timedelta
from multiprocessing import pool
import shutil
import subprocess
import sys
import time
from typing import Tuple
import warnings
import ffmpeg

from pathlib import Path
from custom_objects import SSAEncodeProfile, ParameterObject
from utils import extract_names, get_episode_duration, update_filename, verify_crc32, print_msg, get_ff_version
from modules import SleepModule
import argparse


def my_encode_profile_as_custom_object():
    """
    * current encode profile
    Basically SSA's profile but 10bit, ogg audio and soft-subs
    """

    # initialize
    encode_profile = SSAEncodeProfile()

    # assign values
    encode_profile.audio_bitrate = 96
    encode_profile.audio_codec = 'libopus'
    encode_profile.set_video_resolution(720)
    encode_profile.video_profile = 'main10'
    # encode_profile.video_quality = 24.2  # defaut 24.2
    # encode_profile.video_codec = 'libx265' # default libx265
    # encode_profile.preset = 'slow'  # default slow
    encode_profile.attachment_copy = True  #
    encode_profile.subtitle_decoder = None
    encode_profile.video_codec_params.add_params(
        [
            ParameterObject('me', 2),
            ParameterObject('rd', 4),
            ParameterObject('subme', 7),
            ParameterObject('aq-mode', 3),
            ParameterObject('aq-strength', 1),
            ParameterObject('deblock', '1,1'),
            ParameterObject('psy-rd', 1),
            ParameterObject('psy-rdoq', 1),
            ParameterObject('rdoq-level', 2),
            ParameterObject('merange', 57),
            ParameterObject('bframes', 8),
            ParameterObject('b-adapt', 2),
            ParameterObject('limit-sao', 1),
            ParameterObject('no-info', 1)
        ]
    )
    encode_profile.video_codec_params.spliter = ':'
    encode_profile.pix_fmt = 'yuv420p10le'
    encode_profile.vf.add_params(
        [
            ParameterObject('smartblur', '1.5:-0.35:-3.5:0.65:0.25:2.0'),
            ParameterObject(
                'scale', f'-1:{encode_profile.get_video_resolution()}:spline+accurate_rnd+full_chroma_int')
        ]
    )
    encode_profile.vf.spliter = ','
    # color_range
    # color_primaries
    # color_trc
    # colorspace
    return encode_profile


def my_encode_profiles():
    """
    * my previous encode profile based on ssa's (8bit)
    Basically SSA's settings, but ogg audio and softsubs.
    I heard that 'libopus' can achieve the same audio quality with less bitrate. I cannot confirm
    (about the quality part) but my eyes and ears are okay with these settings.
    """

    audio_bitrate = 96  # slider, range from 8 to 320
    audio_codec = 'libopus'  # combobox (with edittext to customize)
    video_resolution = 720  # (specify video height, keep aspect ratio)
    video_codec = 'libx265'  # combobox
    video_quality = 24.2  # slider,  range from 10 to 30
    preset = 'slow'  # combobox, I think

    ffmpeg_arguments = {
        'c:a': audio_codec,
        'c:v': video_codec,
        'b:a': f'{audio_bitrate}k',
        'profile:v': 'main',
        'x265-params': ':'.join(
            ['me=2', 'rd=4', 'subme=7', 'aq-mode=3', f'aq-strength=1', f'deblock=1,1', f'psy-rd=1', f'psy-rdoq=1',
             'rdoq-level=2', 'merange=57', 'bframes=8', 'b-adapt=2', 'limit-sao=1', 'no-info=1']),
        'crf': video_quality,
        'preset': preset,
        'pix_fmt': 'yuv420p',
        'vf': ','.join(['smartblur=1.5:-0.35:-3.5:0.65:0.25:2.0',
                        f'scale=-1:{video_resolution}:spline+accurate_rnd+full_chroma_int']),
        'color_range': 1,
        'color_primaries': 1,
        'color_trc': 1,
        'colorspace': 1,
    }
    return ffmpeg_arguments


def pause_encode(sleep_an_hour: bool = True):
    # encode between 10 am and 5 pm
    ten_am_tmr = (datetime.now() + timedelta(days=1)).replace(hour=10, minute=0, second=0)
    start = timedelta(hours=10)
    end = timedelta(hours=17)
    current = timedelta(hours=datetime.now().hour, minutes=datetime.now().minute)

    if (end - current).total_seconds() < 0:
        print_msg(f"Sleeping until 10 am the next day")
        # (datetime.now()+timedelta(days=1)).replace(hour=10, minute=0, second=0) - datetime.now()
        time.sleep((ten_am_tmr - datetime.now()).total_seconds())
    elif (current - start).total_seconds() < 0:
        print_msg(f"Sleeping until 10 am")
        time.sleep((start - current).total_seconds())
    elif sleep_an_hour:
        print_msg(f"Sleeping for one hour")
        time.sleep(3600)


# # encode during 3 am to 8 am
# end_hour = timedelta(hours=8)
# now = timedelta(hours=datetime.now().hour, minutes=datetime.now().minute,
#                 seconds=datetime.now().second)
# if (end_hour - now).total_seconds() < 0:
#     # using my work pc as test machine to encode during night (3 am ~ 8 am)
#     sleep = timedelta(days=1, hours=3) - now
#     print_msg(f"Sleeping until 3 am next day")
#     time.sleep(sleep.seconds)
#

def main(
        input_folder: Path,
        output_folder: Path,
        encoded_episode_dir: Path,
        naming: str = None,
        ffmpeg_path: str = "ffmpeg",
        ffprobe_path: str = "ffprobe",
        pools: int = None,
        ffmpeg_verbose: bool = False,
        from_cmd: bool = False,
        debug: bool = False,
        watch_input: bool = False,
        no_verify_source: bool = False,
        encode_hour: Tuple[int] = None
):
    print("Encode started")
    if from_cmd:
        # if main() is a direct execution from main.py, then they will have None by default, which need to change
        ffmpeg_path = "ffmpeg" if ffmpeg_path is None else Path(ffmpeg_path).absolute().__str__()
        ffprobe_path = "ffprobe" if ffprobe_path is None else Path(ffprobe_path).absolute().__str__()
    if debug:
        print_msg(f"DEBUG: ffmpeg:[{ffmpeg_path}], ffprobe:[{ffprobe_path}]")
    with get_ff_version(ffmpeg_path) as ffmpeg_ver:
        if ffmpeg_ver is None:
            warnings.warn("ffmpeg not installed, install ffmpeg to continue: https://ffmpeg.org/download.html")
        else:
            print_msg(ffmpeg_ver)
    with get_ff_version(ffprobe_path) as ffprobe_ver:
        if ffprobe_ver is None:
            warnings.warn("ffprobe not installed, install ffmpeg to continue: https://ffmpeg.org/download.html")
        else:
            print_msg(ffprobe_ver)
    if encode_hour is None:
        encode_hour = [None, None]
    if isinstance(encoded_episode_dir, Path):
        # if encoded_episode_dir is a path, then it should be a valid folder
        if not encoded_episode_dir.exists():
            encoded_episode_dir.mkdir(parents=True)
        elif encoded_episode_dir.is_file():
            raise Exception(
                f"Cannot move encoded episode to a file (destination should be a folder): "
                f"{encoded_episode_dir.absolute().__str__()}"
            )
    sleep_module: SleepModule = SleepModule(start_hour=encode_hour[0], end_hour=encode_hour[1])
    input_episodes = input_folder  # folder to watch
    # pause_check_enabled = watch_input
    # output_folder = Path("H:/frd")  # output folder
    while True:
        files_in = []
        try:
            files_in = [input_episodes] if input_episodes.is_file() else list(input_episodes.glob('*'))
        except Exception as ex:
            print_msg(ex.__str__())  # why am i putting a try catch thingy here? what was i thinking?
        if debug:
            print_msg(f"DEBUG: Encode queue: ")
            for item in files_in:
                print(f"\t{item.__str__()}")
        if len(files_in) == 0:
            if watch_input:
                print_msg(f"No file to encode. Sleep for {sleep_module.get_sleep_seconds()} second(s)")
                sleep_module.sleep()
                continue
            else:
                print_msg(f"No file to encode.")
                return
        while len(files_in) > 0:
            if not sleep_module.is_in_encode_period():
                temp = sleep_module.get_sleep_seconds()
                print_msg(f"Not in encode period, encode paused for {temp} second(s)")
                sleep_module.sleep(temp)
                del temp
                print_msg("Continue encode")
            file_in = files_in.pop(0)
            print_msg(f"Preparing {file_in.name}")
            try:
                # make sure file is accessible (like accessing a file on NAS)
                if file_in.is_dir():
                    continue
                if not file_in.exists():
                    warnings.warn(
                        f"Cannot find file: {file_in.name}"
                    )
                    continue
            except OSError as ex:
                print_msg(ex.__str__())
                files_in.clear()
                continue
            source_duration = get_episode_duration(file_in, ffprobe_path)
            if source_duration is None:
                warnings.warn(
                    f"Unable to retrieve video length, source could be broken or ffprobe isn't available. ({file_in.name})"
                )
            episode_info_from_name = extract_names(file_in)
            if no_verify_source:
                print_msg("Source CRC verification skipped by user.")
            elif episode_info_from_name.crc != '':
                print_msg("Verifying CRC32....", end='', flush=True)
                if not verify_crc32(file_in, episode_info_from_name.crc):
                    print("Failed")
                    print_msg(
                        f"CRC mismatch, source could be broken. ({file_in.name})"
                    )
                else:
                    print("OK")
            elif episode_info_from_name.crc == '':
                print_msg(
                    f"Unable to verify source because its CRC checksum isn't found."
                )

            ffmpeg_arguments_obj = my_encode_profile_as_custom_object()
            if pools is not None:
                ffmpeg_arguments_obj.video_codec_params.add_param('pools', pools)
            ffmpeg_arguments_dict = ffmpeg_arguments_obj.as_ffmpeg_python_args()
            output_file = output_folder.joinpath('output.mkv').absolute()
            ffmpeg_stream = ffmpeg.input(file_in.absolute().__str__())
            subtitle_stream = ffmpeg_stream['s?']  # question mark (?) tells ffmpeg to match 0 or more stream,
            attachment_stream = ffmpeg_stream['t?']  # while without '?' it match 1 or more.
            ffmpeg_stream = ffmpeg.output(
                ffmpeg_stream.video, ffmpeg_stream.audio, subtitle_stream, attachment_stream, output_file.__str__(),
                **ffmpeg_arguments_dict
            )
            ffmpeg_stream = ffmpeg.overwrite_output(ffmpeg_stream)
            command = ffmpeg.compile(ffmpeg_stream, ffmpeg_path)
            if debug:
                print_msg("DEBUG: ffmpeg command: " + " ".join(command))
            # subprocess.Popen(command, shell=True, stdout=sys.stdout, stderr=sys.stderr).wait()
            stdout = sys.stdout if ffmpeg_verbose else subprocess.PIPE
            stderr = sys.stderr if ffmpeg_verbose else subprocess.PIPE
            print_msg(f"Start encoding: {file_in.name.__str__()}")
            result = subprocess.run(command, shell=False, stdout=stdout, stderr=stderr)
            if result.returncode != 0:
                warnings.warn(
                    "ffmpeg did not complete encode, check console output or log (run with '--ffmpeg-verbose' argument)"
                )
                continue

            encoded_duration = get_episode_duration(output_file, ffprobe_exec=ffprobe_path)
            if encoded_duration is None or source_duration is None:
                warnings.warn(
                    "Unable to check encoded episode because of the missing source/encoded video length."
                    "You may want to verify the file manually."
                )
            elif abs(encoded_duration - source_duration) > 1:
                warnings.warn(
                    f"Video length mismatch, encoded file could be broken. ({output_file.name}). "
                    f"You may want to verify manually and decide whether to keep the file or not."
                )
            else:
                print_msg("Video length check OK")

            final_filename = update_filename(
                episode_info=episode_info_from_name,
                episode_file=output_file,
                encode_profile=ffmpeg_arguments_obj,
                naming_rule=naming,
                ffprobe_exec=ffprobe_path
            ).name
            print_msg(f"Encoded episode was renamed to {final_filename}")

            # encoded_episode_dir:
            if encoded_episode_dir is None:
                # None -> delete file;
                file_in.unlink(missing_ok=True)
            elif not encoded_episode_dir:
                # False -> do nothing;
                pass
            elif isinstance(encoded_episode_dir, Path):
                # Path() -> move to this folder
                # use shutil to avoid "Invalid cross-device link"
                shutil.move(file_in.absolute().__str__(),
                            encoded_episode_dir.joinpath(file_in.name).absolute().__str__())
                # file_in.replace(encoded_episode_dir.joinpath(file_in.name))
            else:
                ValueError("A wild bug has appeared. Dameda...\n"
                           f"Variable:encoded_episode_dir; Type:{type(encoded_episode_dir)}; "
                           f"Value:{encoded_episode_dir}")
        if not watch_input:
            print_msg("Encode complete")
            return


args = argparse.ArgumentParser()
args.add_argument('-i', '--input', dest='input', type=str,
                  nargs=1, required=False, help='Path to an episode or path to a directory of episodes to encode')
args.add_argument('--watch', dest="watch", action="store_true",
                  required=False, help='Watch input folder')
args.add_argument('--move-encoded', dest="move_encoded", nargs=1, type=str,
                  required=False, help="Move source file to this directory after encode")
args.add_argument('--delete-encoded', dest="delete_encoded", action="store_true",
                  required=False, help='Delete source after encode, overwrites --move-encoded')
args.add_argument('-o', '--output-dir', dest='output', nargs=1, type=str,
                  required=False, help='Save encoded file to this directory')
args.add_argument('--ffmpeg', dest='ffmpeg', nargs=1, type=str,
                  required=False, help='Specify ffmpeg executable location')
args.add_argument('--ffprobe', dest='ffprobe', nargs=1, type=str,
                  required=False, help='Specify ffprobe executable location')
args.add_argument('--naming', dest='naming', nargs=1, type=str,
                  required=False, help='Output naming rule')
args.add_argument('--resolution-height', dest='resolution_height', nargs=1, type=int,
                  required=False, help="Set encode resolution. e.g. 1080 for 1080p encode, 1440 for 2k encode")
args.add_argument('--pools', dest='pools', nargs=1, type=int,
                  required=False, help="Set maximum threads for encoding")
args.add_argument('--do-not-verify-source', dest="no_verify_source", action="store_true",
                  required=False, help='Do not verify source CRC checksum')
args.add_argument('--ffmpeg-verbose', dest="ffmpeg_verbose", action="store_true",
                  required=False, help='Display ffmpeg stdout')
args.add_argument('--schedule-encode-hour', dest="schedule_encode_hour", nargs='+', type=int,
                  required=False, help='Display ffmpeg stdout')
args.add_argument('--debug', dest="debug", action="store_true",
                  required=False, help='Display debug info')
# args.print_help()
args1 = args.parse_args()

if __name__ == "__main__":
    # print_msg(args1.delete_encoded)

    if args1.input is not None:
        input = Path(args1.input[0])
    else:
        raise Exception("must specify an input (-i|--input [file|folder])")

    if args1.output is None:
        raise Exception("must specify an output directory (-o|--output-dir [folder])")

    watch_input = args1.watch

    if args1.delete_encoded:
        move_encoded = None
    elif args1.move_encoded is not None:
        move_encoded = Path(args1.move_encoded[0])
    else:
        if watch_input:
            raise Exception(
                """
                Must specify what to do with an encoded source when watching a folder, 
                otherwise they will be re-encoded upon every program execution, and that shouldn't happen.
                Either move them to a different folder (--move-encoded [path to folder]), 
                or delete them (--delete-encoded)
                """
            )
        move_encoded = False

    pools = None if args1.pools is None else args1.pools[0]
    ffmpeg_path = None if args1.ffmpeg is None else args1.ffmpeg[0]
    ffprobe_path = None if args1.ffprobe is None else args1.ffprobe[0]
    naming = None if args1.naming is None else args1.naming[0]
    encode_hour = None if args1.schedule_encode_hour is None else args1.schedule_encode_hour[0:2]

    # print_msg(args1._get_kwargs())
    main(input_folder=input, output_folder=Path(args1.output[0]),
         encoded_episode_dir=move_encoded, naming=naming,
         ffmpeg_path=ffmpeg_path, ffprobe_path=ffprobe_path,
         pools=pools, ffmpeg_verbose=args1.ffmpeg_verbose,
         debug=args1.debug, from_cmd=True, watch_input=watch_input,
         no_verify_source=args1.no_verify_source,
         encode_hour=encode_hour)
