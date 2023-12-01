"""
何するんだよ私…
Try not to import non-buildin library plz...
"""

from __future__ import annotations
from datetime import datetime
import json
import logging
import re
from pathlib import Path
import subprocess
from subprocess import CompletedProcess
import sys
from typing import Callable, Optional, Dict, List, Sized, Iterable, Any, Generic, Text, TextIO, AnyStr
import zlib
from argparse import ArgumentParser

logger = logging.getLogger(__name__)


class ProbeResultKeys:
    class StreamTypes:
        """ ffprobe result? """
        VIDEO = 'video'
        AUDIO = 'audio'
        SUBTITLE = 'subtitle'
        ATTACHMENT = 'attachment'


class Constants:
    """ class object is a temporary solution, I probably should use a txt file or something simular """
    # todo: use text file / config instead of hard coding
    KNOWN_NON_OMITTABLE_TAGS = {'BD', 'WEB-DL'}  # it should be case-insensitive (default to upper case)
    KNOWN_OMITTABLE_TAGS = {'HEVC', 'AAC', 'OPUS'}
    LOGGER_SETUP = False


class HelperFunctions:
    @staticmethod
    def print_msg(msg: str, flush: bool = False, end: str = '\n'):
        """
        I have replaced this function with `coloredlogs`.
        However, if `coloredlogs` is too much, this is still available...

        Print message with time in front.
        :param msg:
        :param flush:
        :param end:
        :return:
        """
        print(f"[{datetime.now()}] [{__name__}] {msg}", flush=flush, end=end)

    @staticmethod
    def subprocess_run(args: list[str], stdout=subprocess.PIPE, stderr=subprocess.PIPE) -> CompletedProcess[bytes]:
        return subprocess.run(args=args, stdout=stdout, stderr=stderr)

    @staticmethod
    def get_file_crc32(file: Path, on_file_chunk_read: Optional[Callable[[int], None]] = None,
                       abort_signal: Optional[Callable[[], None]] = None) -> str:
        """
        Calculate CRC32 for an episode, and return the value as string

        :param on_file_chunk_read: (Chunk size): Callback upon reading x bytes of data
        :param abort_signal: A function that reads if abort signal is received. Useful when using alive_progress bar.

        Note
        ----
        It's doing unsigned 32-bit crc according to
        https://stackoverflow.com/questions/30092226/how-to-calculate-crc32-with-python-to-match-online-results
        and
        https://docs.python.org/3/library/binascii.html#binascii.crc32
        and
        https://stackoverflow.com/questions/1742866/compute-crc-of-file-in-python

        More Notes
        ----------
        0 means padding with zero (left side), 8 means the string length, X means upper case hex value.

        %08X is hurting my brain...
        """

        enable_progress_report = isinstance(on_file_chunk_read, Callable)  # and use_alive_bar
        logger.debug(f"enable_progress_report={enable_progress_report}; ")
        if not enable_progress_report:
            on_file_chunk_read_cb = lambda chunk_size: logger.debug(f"Sending size {chunk_size}")
        else:
            on_file_chunk_read_cb = lambda chunk_size: {
                # logger.debug(f"Sending size {chunk_size}"),
                on_file_chunk_read(chunk_size)
            }
        if not isinstance(abort_signal, Callable):
            abort_signal = lambda: False
        with open(file.__str__(), 'rb') as fh:
            hash_val = 0
            # ~ while abort_signal is None or abort_signal() == False
            while not abort_signal():
                s = fh.read(65536)
                if not s:
                    break
                on_file_chunk_read_cb(len(s))
                hash_val = zlib.crc32(s, hash_val)
            # return "%08X" % (hash & 0xFFFFFFFF)
            return format((hash_val & 0xFFFFFFFF), '08X')

    @staticmethod
    def is_string_empty(subject: str, whitespace_is_empty: bool = True) -> bool:
        return subject is None or (whitespace_is_empty and len(subject.strip()) == 0)

    @staticmethod
    def is_subject_empty(subject: Any) -> bool:
        """return `True` if `subject` is `None` or `len()==0`"""
        if subject is None:
            return True
        if isinstance(subject, Sized) and len(subject) == 0:
            return True
        if isinstance(subject, str):
            return HelperFunctions.is_string_empty(subject=subject)
        return False

    @staticmethod
    def update_filename(
            episode_file: Path,
            naming_template: str = None,
            naming_keyword_replacement: dict[str, str] = None,
            update_file=True) -> Path:
        assert episode_file.exists() and episode_file.is_file(), f"file={episode_file}, exists={episode_file.exists()}, is_file={episode_file.is_file()}"
        if HelperFunctions.is_subject_empty(naming_template):
            filename = episode_file.name
        else:
            filename = naming_template
            for replacement in naming_keyword_replacement.items():
                filename.replace(replacement[0], replacement[1])
            filename += episode_file.suffix
        # filename = f"[src={episode_info.release_group}] {episode_info.episode_name} ({encode_profile._video_resolution}p) [{crc}]{episode_file.suffix}"

        # function will return the updated file path
        if update_file:
            # update the name and return the path pointing to the file
            return episode_file.rename(episode_file.parent.joinpath(filename))
        else:
            # path to the file with new name will be returned, but file's name remains unchanged
            return episode_file.parent.joinpath(filename)

    @staticmethod
    def get_ff_version(path: str, app_name: str = ..., **kwargs) -> (str | int | None):
        """
        get ffmpeg component version (to verify its existence before encoding)

        Param
        -----
            path: ffmpeg/ffprobe/... executable
            app_name: 'ffmpeg'|'ffprobe'
        
        Returns
        -------
            version string as `str`,
            or `None` if program not found (FileNotExistError),
            or return code as `int` if program exists but did not exit correctly or program version not found (regular expression did not match)
        """
        logger.info(f'Getting {app_name} version: "{path}"')
        assert isinstance(app_name, str), ValueError('Must specify an app name, either "ffmpeg" or "ffprobe"')
        ver_regexp = r'ff.+? version (\S+) '
        to_return = None
        debug = kwargs.get('debug', False)
        try:
            sp = subprocess.run([path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                creationflags=subprocess.DETACHED_PROCESS)
            if sp.returncode == 0:
                to_return = sp.stdout.decode().split('\n')[0].split('\r')[0]
                logger.debug(to_return)
                if to_return.startswith(app_name):
                    to_return = re.search(ver_regexp, to_return)
                else:
                    to_return = None
            else:
                logger.warning(f'"{path}" returned non-zero exit code ({sp.returncode})')
            if to_return is None: to_return = sp.returncode
        except FileNotFoundError as ex:
            logger.error(f"Cannot find file '{path}': {ex}")
            # to_return = ""
        finally:
            if isinstance(to_return, re.Match):
                to_return = to_return.groups()[0]
            logger.info(f'Got ffmpeg version: {to_return}')
            return to_return

    @staticmethod
    def get_value_from_nested_dict(*keys, dict_obj: Dict, default: Any = None) -> Any:
        current_dict = dict_obj
        for key in keys:
            current_dict = current_dict.get(key, default)
            if isinstance(current_dict, Dict):
                continue
            break  # if keys exhausted or got a non-dict object, break loop and return the current object
        return current_dict


if __name__ == '__main__':
    tool_name = ['lupdate', 'a']
    usage = \
        f"""
python3 -m python_encode.utils [tool name]
Anvaiable tools: {tool_name}
"""

    parser = ArgumentParser(prog=f"python_encode dev tool", usage=usage,
                            description="Helps me with some repetitive tasks.")
    parser.add_argument("tool", type=str, nargs='+', choices=tool_name,
                        help='Use "lupupdate" to create language file for .ui files and language.py in this package')
    args = parser.parse_args()

    script_path = Path(sys.executable).parent
    if sys.platform == 'linux':
        print("Linux is not supported yet")
        exit(-1)
    elif sys.platform == 'darwin':
        print("MacOS is not supported yet")
        exit(-1)
    elif sys.platform == 'win32':
        script_path = script_path / "Scripts"

    if 'lupdate' in args.tool:
        cmd = [script_path.joinpath("pyside6-lupdate").__str__()]
        cmd.append(Path(__file__).parent.joinpath("language", "language.py").__str__())
        cmd.extend(map(str, Path(__file__).parent.joinpath("ui").glob("*.ui")))
        cmd.extend(['-ts', Path(__file__).parent.joinpath("language", "language.ts").__str__()])
        cmd.extend(['-source-language'])
        str_cmd = " ".join([_ if " " not in _ else f'"{_}"' for _ in cmd])
        print(f"Running lupdate << {str_cmd}")
        subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
    if 'a' in args.tool:
        print('a')
