"""
Deprecation for "main_deprecating.py" file is planned because code refactor broke some process logics.
"""

# from modules import SleepModule
import argparse
import logging
from pathlib import Path
from typing import Sized, Optional

from python_encode.anime_processor import AnimeProcessor
from python_encode.utils_site_package import HelperFunctions
from python_encode.custom_objects import EncodePresetObject

logger = logging.getLogger(__name__)


def run_in_cli(
        input_file_or_folder: Path,
        output_folder: Path,
        encoded_episode_dir: Optional[Path] = ...,
        presets: Path = None,
        ffmpeg_path: str = "ffmpeg",
        ffprobe_path: str = "ffprobe",
        ffmpeg_verbose: bool = False,
        watch_input: bool = False,
        no_verify_source: bool = False,
):
    input_files = [input_file_or_folder] if input_file_or_folder.is_file() else list(input_file_or_folder.glob('*.*'))

    encode_preset = EncodePresetObject(preset_dir=presets)
    logger.info(f"Using presets: {encode_preset.preset_name}")
    logger.debug("Input list:\n\t"+"\n\t".join([_.name for _ in input_files]))

    failed_encodes: list[Path] = list()
    for input_file in input_files:
        logger.info(f"Processing {input_file.name}")
        encoded_file, aborted = AnimeProcessor.do_encode_task(
            source_file=input_file, output_dir=output_folder,
            encode_preset=encode_preset, ffmpeg_executable=ffmpeg_path, ffprobe_executable=ffprobe_path,
            show_ffmpeg_stdout=ffmpeg_verbose
        )
        if aborted:
            return
        if encoded_file is None:
            logger.warning(f'Encode failed for file "{input_file}"')
            failed_encodes.append(input_file)
            continue
        logger.info(f"Encode complete >> {encoded_file.name}")
    logger.info("Process completed. ")
    if not HelperFunctions.is_subject_empty(failed_encodes):
        failed_encodes_str = "\n\t".join([_.__str__() for _ in failed_encodes])
        logger.info(f"The following file(s) did not encode:\n\t{failed_encodes_str}")


def get_cmd_argument(argument: any, default: any = None, argument_size: int = 1):
    """return the first cmd argument if presents"""
    if argument_size > 1:
        return default if argument is None else argument[0:argument_size]
    if isinstance(argument, Sized):
        return default if argument is None else argument[0]
    return default if argument is None else argument

def main():
    args = argparse.ArgumentParser()
    args.add_argument('-i', '--input', dest='input', type=str,
                      nargs=1, required=False,
                      help='Path to an episode or path to a directory of video files to encode')
    args.add_argument('-o', '--output-dir', dest='output', nargs=1, type=str,
                      required=False, help='Save encoded file to this directory')
    args.add_argument('--presets', dest='presets', nargs=1, type=str,
                      required=False, help='A directory containing encode presets for encoding')
    args.add_argument('--ffmpeg', dest='ffmpeg', nargs=1, type=str,
                      required=False, help='Specify ffmpeg executable location')
    args.add_argument('--ffprobe', dest='ffprobe', nargs=1, type=str,
                      required=False, help='Specify ffprobe executable location')
    args.add_argument('--do-not-verify-source', dest="no_verify_source", action="store_true",
                      required=False, help='Do not verify source CRC checksum')
    args.add_argument('--ffmpeg-verbose', dest="ffmpeg_verbose", action="store_true",
                      required=False, help='Display ffmpeg stdout')
    args.add_argument('--debug', dest="debug", action="store_true",
                      required=False, help='Display debug info')
    # args.print_help()

    args1 = args.parse_args()
    if args1.input is None:
        raise Exception("must specify an input (-i|--input [file|folder])")
    input = Path(args1.input[0])

    if args1.output is None:
        raise Exception("must specify an output directory (-o|--output-dir [folder])")

    ffmpeg_path = get_cmd_argument(args1.ffmpeg, "ffmpeg")
    ffprobe_path = get_cmd_argument(args1.ffprobe, "ffprobe")
    # encode_hour = get_cmd_argument(args1.schedule_encode_hour, argument_size=2)

    presets_dir = get_cmd_argument(args1.presets, "")
    global logger
    logger = HelperFunctions.setup_logger(__name__, log_level="DEBUG" if get_cmd_argument(args1.debug, False) else "INFO")

    run_in_cli(input_file_or_folder=input, output_folder=Path(get_cmd_argument(args1.output, "")),
               presets=Path(presets_dir),
               ffmpeg_path=ffmpeg_path, ffprobe_path=ffprobe_path,
               ffmpeg_verbose=args1.ffmpeg_verbose,
               no_verify_source=args1.no_verify_source)


if __name__ == "__main__":
    main()
