from __future__ import annotations

import logging
import sys
from json import JSONDecoder
import re
import subprocess
import time
import zlib
from datetime import datetime, timedelta

from custom_objects import AnimeObject, ExtractedNameObject, ParameterObject, SSAEncodeProfile, TagList, TypeEnum, Tag
# from language import language # utils.py won't import QT stuff
# from utils_qt import tr   # translations will only be available at GUI related method

from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Any
import coloredlogs
import ffmpeg

# lp = language.VariousString
_logger_setup = False

"""
While writing a utility....
I still have trouble understanding python regular expression and I thought writing something on my own
is a good idea....
Basically me reading SSA's code and trying to figure out how it works...
"""


class SleepModule:
    """
    control how program sleeps?
    """
    __slots__ = 'sleep_sec', 'work_hour_start', 'work_hour_end'

    def __init__(self, sleep: int = 3600, start_hour: int | None = None, end_hour: int | None = None):
        """
        1. 'sleep' sets a certain seconds to sleep;
        2. start_hour and end_hour sets to encode between start_hour to end_hour every day.
        if end_hour is equal or smaller than start_hour, then it becomes
        "encode between start_hour to end_hour the next day"

        Parameters
        ----------
        sleep: specify seconds to sleep when calling sleep()
        start_hour:
        end_hour:
        """
        if isinstance(sleep, int):
            self.sleep_sec: int = sleep  # sleep for x seconds, default 3600
        else:
            ValueError(f"parameter 'pause' expect {type(int)}, but got {type(sleep)}")

        if start_hour is None:
            pass
        elif not isinstance(start_hour, int):
            TypeError(f"parameter 'start_hour' expect {type(int)} or {type(None)}, but got {type(start_hour)}")
        elif start_hour > 24 or start_hour < 0:
            ValueError("value of parameter 'start_hour' be between 0 and 24 ")
        self.work_hour_start: int | None = start_hour

        if end_hour is None:
            pass
        elif not isinstance(end_hour, int) and end_hour is not None:
            ValueError(f"parameter 'end_hour' expect {type(int)} or {type(None)}, but got {type(end_hour)}")
        elif end_hour > 24 or end_hour < 0:
            ValueError("value of parameter 'end_hour' be in 0~24 ")
        # elif start_hour >= end_hour:
        #     end_hour += 24
        self.work_hour_end: int | None = end_hour

    def sleep(self, time_override: float = None):
        """
        pause program for 'time_override' seconds, default 1 hour
        """
        time.sleep(self.pause if time_override is None else time_override)

    def pause(self):
        """
        immediately pause program until it reaches the next encode period (time between start_hour and end_hour)
        """
        time.sleep(self.get_total_seconds_to_pause())

    def get_sleep_seconds(self) -> (int):
        return self.sleep_sec

    def get_total_seconds_to_pause(self) -> (float):
        if self.work_hour_start is None:
            ValueError("start_hour must be set to use this function")
        if self.work_hour_end is None:
            ValueError("end_hour must be set to use this function")
        # writing down all possible conditions because I couldn't simplify it in my brain
        start = timedelta(hours=self.work_hour_start)
        current = timedelta(hours=datetime.now().hour, minutes=datetime.now().minute)
        end = timedelta(hours=self.work_hour_end)
        if self.work_hour_start < self.work_hour_end:
            # my terrible English couldn't describe what it is, so I drew a line
            # [0h-----++++++++++++++++----24h]
            # [ pause |    encode    | pause ]
            # or "encode between  'start' to 'end'"
            if (start - current).total_seconds() > 0:
                # before encode period, sleep until reaches it
                return (start - current).total_seconds()
            if (current - end).total_seconds() > 0:
                # after encode period, sleep until the next period
                return (start + timedelta(days=1) - current).total_seconds()
            # in encode period, no need to pause
            return 0
        else:
            # my terrible English couldn't describe what it is, so I drew a line pt2
            # [0h+++++++-------------+++++24h]
            # [ encode |   pause    | encode ]
            # or "encode between  'start' to 'end' the next day"
            if (current - end).total_seconds() > 0 and (start - current).total_seconds() > 0:
                return (start - current).total_seconds()
            # in encode period, no need to pause
            return 0

    def is_in_encode_period(self) -> (bool):
        if self.work_hour_start is None or self.work_hour_end is None:
            # if work hour isn't specified, then assume encode 24/7
            return True
        return self.get_total_seconds_to_pause() == 0


def print_msg(msg: str, flush: bool = False, end='\n'):
    """
    Print with time before the message
    :param msg:
    :param flush:
    :param end:
    :return:
    """
    print(f"[{datetime.now()}] {msg}", flush=flush, end=end)


def is_string_empty(subject: str) -> bool:
    """return `True` if `subject` is None or subject is an empty string"""
    return subject is None or subject == ''


def anime_to_anime_object(file: Path, ffprobe: str = 'ffprobe', 
                          progress_emit: Optional[callable[int]] = ..., 
                          abort_signal: Optional[callable] = ...,
                          debug: bool = False) -> AnimeObject|None:
    """
    Read information from an video file using ffprobe.
    Return `None` if parse failed.
    """
    _logger = logging.getLogger(__name__)

    if not isinstance(file, Path) or not file.exists() or file.is_dir():
        _logger.warning('File "%s" is invalid.', file)
        return None
    if not isinstance(abort_signal, Callable):
        abort_signal = None
    anime = AnimeObject()
    anime.file = file
    anime.video_length = (get_episode_duration(file, ffprobe))
    if None in anime.video_length:
        _logger.warning('Unable to read video length with ffprobe: %s', file)
        return None
    anime.video_resolution = (get_episode_resolution(file, ffprobe))
    if None in anime.video_resolution:
        _logger.warning('Unable to read video resolution with ffprobe: %s', file)
        return None
    anime.file_name = file.name
    anime.file_crc32 = get_episode_crc32(file, report_progress=progress_emit, abort_signal=abort_signal)
    
    episode_info = ExtractedNameObject()
    episode_info.filename = anime.file_name
    title = anime.file.stem

    def read_text(subject: str) -> (Tuple[str, str]):
        content = re.findall(r'^([^\[^\(]*)', title)[0]
        subject = subject[len(content):]
        return subject, content.strip()
    
    def read_brackets(subject: str) -> (Tuple[str, str]):
        content = re.findall(r'^\[([^\]]*)\]', title)[0]
        subject = subject[len(content) + 2:]
        return subject, content

    def read_parenthesis(subject: str) -> (Tuple[str, str]):
        content = re.findall(r'^\(([^\)]*)\)', title)[0]
        subject = subject[len(content) + 2:]
        return subject, content

    while (len(title) > 0):
        is_text = False
        # "content" here is a segment of "title".
        # segment by segment, "title" eventually becomes an empty string.
        if title.startswith('['):
            title, content = read_brackets(title)
        elif title.startswith('('):
            title, content = read_parenthesis(title)
        else:
            title, content = read_text(title)
            is_text = True

        if debug:
            print(("DEBUG: ", title, content))

        if content == "":
            continue

        # assuming first brackets contains group name
        if is_string_empty(episode_info.release_group):
            if not is_text:
                episode_info.release_group = content
                continue
            else:
                # group name may contain underscore (I don't know, it's possible),
                # and for group name I want to leave it as is 
                # and I want to replace underscore with space (I prefer space than underscore)
                #
                # for example, "Selection_Project" -> "Selection Project"
                title = title.replace('_', ' ')
                episode_info.release_group = "UNKNOWN"

        # assuming every single word not enclosed in brackets or parenthesis is episode name
        # otherwise treat it as tag (includes resolution, crc code, and everything else)
        if is_text:
            if not is_string_empty(episode_info.episode_name):
                episode_info.episode_name += " "
            episode_info.episode_name += content
            continue

        # check if tag matches CRC code's patten
        # 8 characters long, contains only 0~9 and a~f
        if len(content) == 8:
            potential_crc = re.findall(r'([0-9|a-f|A-F]*)', content)
            if len(potential_crc) > 0 and potential_crc[0] == content:
                episode_info.crc = content
                continue

        episode_info.other_tags.append(content)
    
    anime.filename_info = episode_info
    return anime
    


def extract_names(title: Path, debug: bool = False) -> ExtractedNameObject:
    """
    Extract episode title and tags (which includes group name, resolution, crc and others).
    Processing logic works for SubsPlease's release. May add logic to process names from 
    other group, but I'd like to take care of my need first.

    Parameters
    ----------
    title: str
        Episode file name (e.g. [SomeGroup] Some Anime - Episode 1 [CRC code].mkv)

    Returns
    -------
    object: ExtractedNameObject
    """

    # names: TagList = TagList()
    episode_info = ExtractedNameObject()
    episode_info.filename = title.name.__str__()

    if title.suffix in [".mp4", ".mkv"]:
        title = title.stem.__str__()
    else:
        title = title.name.__str__()

    title: str = title

    # print(title)

    def read_text(subject: str) -> (Tuple[str, str]):
        content = re.findall(r'^([^\[^\(]*)', title)[0]
        subject = subject[len(content):]
        return subject, content.strip()

    def read_brackets(subject: str) -> (Tuple[str, str]):
        content = re.findall(r'^\[([^\]]*)\]', title)[0]
        subject = subject[len(content) + 2:]
        return subject, content

    def read_parenthesis(subject: str) -> (Tuple[str, str]):
        content = re.findall(r'^\(([^\)]*)\)', title)[0]
        subject = subject[len(content) + 2:]
        return subject, content

    def find_resolution(subject: str) -> (Tuple[(int or None), str]):
        # resolution_regular_expresion = [r'.*(\d+)[p|i|P|I].*', r'.*\d+[x|X](\d+).*']
        resolution_regular_expresions = [r'(\d+)[p|i|P|I]', r'\d+[x|X](\d+)']
        for exp in resolution_regular_expresions:
            potential_resolution = re.search(exp, subject)
            if potential_resolution is None:
                continue
            rest_of_subject = ''
            if subject == potential_resolution.group():
                pass
            elif subject.startswith(potential_resolution.group()):
                rest_of_subject = subject[potential_resolution.end() + 1:]
            elif subject.endswith(potential_resolution.group()):
                rest_of_subject = subject[:potential_resolution.start() - 1]
            else:
                text_before_resolution = subject[:potential_resolution.start()]
                text_after_resolution = subject[potential_resolution.end() + 1:]
                rest_of_subject = text_before_resolution + text_after_resolution

            # if subject != potential_resolution.group():
            #     # if resolution is a part of a brackets content
            #     # (e.g. [1080p.x265] or [AAC-720P] instead of [1080p][x265])
            #     # Then I'd like to extract the resolution and keep the rest
            #     # Usually between resolution and other things there is a character
            #     # and that's what "start()-1" and "end()+1" does in the following code
            #     # in order to get rid of that character
            #     text_before_resolution = subject[0:max(0,potential_resolution.start()-1)]
            #     text_after_resolution = subject[min(len(subject),potential_resolution.end()+1):len(subject)]
            #     rest_of_subject = text_before_resolution + text_after_resolution
            return int(re.findall(exp, subject)[0]), rest_of_subject

            # potential_resolution_tags = re.findall(item, subject)
            # if len(potential_resolution_tags) > 0:
            #     potential_resolution = potential_resolution_tags[0]
            #     others = list()
            #     for item1 in potential_resolution_tags:
            #         # It is very unlikely to match more than one match on resolution patten,
            #         # but who knows...
            #         if potential_resolution != item1:
            #             others.append(item1)
            #         # if item1 in ["480", "540", "720", "1080"]:
            #         #     # Anime are ususally published in those resolutions right?
            #         #     return int(item1)
            #     return potential_resolution, others
        return (None,) * 2

    while (len(title) > 0):
        is_text = False
        # "content" here is a segment of "title".
        # segment by segment, "title" eventually becomes an empty string.
        if title.startswith('['):
            title, content = read_brackets(title)
        elif title.startswith('('):
            title, content = read_parenthesis(title)
        else:
            title, content = read_text(title)
            is_text = True

        if debug:
            print(("DEBUG: ", title, content))

        if content == "":
            continue
        # print(f"title={title}, content={content}")  # debug

        # assuming first brackets contains group name
        if episode_info.release_group == "":
            if not is_text:
                episode_info.release_group = content
                continue
            else:
                # group name may contain underscore (I don't know, it's possible),
                # and for group name I want to leave it as is 
                # and I want to replace underscore with space (I prefer space than underscore)
                #
                # for example, "Selection_Project" -> "Selection Project"
                title = title.replace('_', ' ')
                episode_info.release_group = "UNKNOWN"

        # assuming every single word not enclosed in brackets or parenthesis is episode name
        # otherwise treat it as tag (includes resolution, crc code, and everything else)
        if is_text:
            if len(episode_info.episode_name) > 0:
                episode_info.episode_name += " "
            episode_info.episode_name += content
            continue

        # check if tag matches CRC code's patten
        # 8 characters long, contains only 0~9 and a~f
        if len(content) == 8:
            potential_crc = re.findall(r'([0-9|a-f|A-F]*)', content)
            if len(potential_crc) > 0 and potential_crc[0] == content:
                episode_info.crc = content
                continue

        other_tag_str: str = None
        # check if tag is resolution
        if episode_info.resolution is None:
            episode_info.resolution, other_tag_str = find_resolution(content)
            if debug:
                print(("DEBUG: find resolution", episode_info.resolution, other_tag_str))
            if episode_info.resolution is not None:
                # after resolution is found, is there something I was supposed to do here?
                pass
                # I don't use continue because resolution might only be a part of a tag.
                # If so then rest of the tags should go into other_tags.
            # can add more elif
            else:
                other_tag_str = content
        if other_tag_str is None or other_tag_str == "":
            # nothing left after parsing resolution, continue the loop
            continue
        # if tag did not get parsed by any condition above,
        # treat it as "other tag", like "uncensored", "AVC", "AAC", "WEB-DL", etc...
        # episode_info.other_tags.append(_ for _ in other_tag_str.split(" "))
        episode_info.other_tags.append(other_tag_str)
        other_tag_str = None

    return episode_info


def verify_crc32(file: Path, crc_val: str) -> (bool):
    """
    compute "file" 's crc32 value and compare it against "crc_val"

    Parameters
    ----------
    file: Path
        the file to verify
    crc_val: str
        the crc32 checksum? to compare

    Returns
    -------
    bool: 
        Are crc values match, True or False
    """
    file_crc_val = get_episode_crc32(file)
    return file_crc_val == crc_val


def get_episode_crc32(file: Path, use_alive_bar: bool = True, report_progress: callable[int] = None, abort_signal: callable = None) -> str:
    """
    Calculate CRC32 for an episode, and return the value as string

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
    0 means padding with 0 (left side), 8 means the string length, X means upper case hex value
    %08X is hurting my brain... 
    """
    def execute(bar=None, progress=False):
        with open(file.__str__(), 'rb') as fh:
            hash_val = 0
            # ~ while abort_signal is None or abort_signal() == False
            while not abort_signal or not abort_signal():
                s = fh.read(65536)
                if not s:
                    break
                if bar: bar(len(s))
                if progress: report_progress(int(bar.current/file.stat().st_size*100))
                hash_val = zlib.crc32(s, hash_val)
            # return "%08X" % (hash & 0xFFFFFFFF)
            return format((hash_val & 0xFFFFFFFF), '08X')

    enable_progress_report = isinstance(report_progress, Callable) and file.stat().st_size and use_alive_bar
    if use_alive_bar:
        from alive_progress import alive_bar
        with alive_bar(file.stat().st_size, title="Checking CRC32", force_tty=True) as bar:
            return execute(bar, enable_progress_report)
    return execute()


def update_filename(
        episode_info: ExtractedNameObject,
        episode_file: Path,
        encode_profile: SSAEncodeProfile = None,
        naming_rule: str = None,
        ffprobe_exec: str = "ffprobe",
        update_file=True) -> (Path):
    assert episode_file.exists() and episode_file.is_file(), f"file={episode_file}, exists={episode_file.exists()}, is_file={episode_file.is_file()}"
    crc = get_episode_crc32(episode_file)
    if encode_profile is None:
        resolution = get_episode_resolution(episode_file, ffprobe_exec)[1]
    else:
        resolution = encode_profile.get_video_resolution()
    if naming_rule is None or naming_rule == '':
        filename = episode_file.name
    else:
        filename = naming_rule.replace(
            '{group}', episode_info.release_group
        ).replace(
            '{episode_name}', episode_info.episode_name
        ).replace(
            '{resolution}', str(resolution)
        ).replace(
            '{crc}', crc
        ).replace(
            '{tags}', " ".join(f"[{tag}]" for tag in episode_info.other_tags)
        ).__add__(
            episode_file.suffix
        )
    # filename = f"[src={episode_info.release_group}] {episode_info.episode_name} ({encode_profile._video_resolution}p) [{crc}]{episode_file.suffix}"

    # function will return the updated file path
    if update_file:
        # update the name and return the path pointing to the file
        return episode_file.rename(episode_file.parent.joinpath(filename))
    else:
        # path to the file with new name will be returned, but file's name remain unchanged
        return episode_file.parent.joinpath(filename)


def get_episode_resolution(episode_file: Path, ffprobe_exec="ffprobe") -> (Tuple[int, int] or None):
    width, height = (None,) * 2
    # trying to read resolution from file itself using ffprobe
    if get_ff_version(ffprobe_exec) is None:
        print("ffprobe not installed, install ffmpeg to continue: https://ffmpeg.org/download.html")
        return width, height
    try:
        episode_probe_info: Dict = ffmpeg.probe(episode_file, ffprobe_exec)
        for stream in episode_probe_info.get("streams"):
            res = (stream.get("width"), stream.get("height"))
            if None not in res:
                width, height = res
                break
    except ffmpeg.Error as ex:
        # should I do something here?
        pass
    finally:
        return width, height


def get_episode_duration(episode_file: Path, ffprobe_exec="ffprobe") -> Tuple[float, int]:
    # print(episode_file)
    _logger = logging.getLogger(__name__)
    if get_ff_version(ffprobe_exec, 'ffprobe') is None:
        _logger.error("ffprobe not installed, install ffmpeg to continue: https://ffmpeg.org/download.html")
        return None, None
    source_duration = None
    source_frame_count = None
    try:
        source_info = ffmpeg.probe(episode_file, cmd=ffprobe_exec)
        duration_str = source_info.get("format").get("duration")
        if duration_str is not None:
            source_duration = float(duration_str)
        for stream in source_info.get("streams"):
            if stream.get("codec_type") != 'video': continue
            # remove video duration check, assuming video stream from user's file has correct length
            # if stream.get('duration') != duration_str: continue   
            stream_tags: dict = stream.get('tags')
            for key in stream_tags.keys():
                if not 'NUMBER_OF_FRAMES' in key: continue
                source_frame_count = int(stream_tags.get(key))
                break
            if source_frame_count is not None: break
    except ffmpeg.Error as ex:
        _logger.error(f"Unable to open {episode_file.name} as video")
    except ValueError as ex:
        _logger.error(ex)
    finally:
        # _logger.debug(f"duration: {source_duration}, frames: {source_frame_count}")
        return source_duration, source_frame_count


# ditching the following one
def get_ffmpeg_version(execs: List[str] = None) -> (List[str]):
    """
    I ditched this thing and it should not be used
    """
    if execs is None:
        execs = list(["ffmpeg", "ffprobe"])
    result = list()
    for item in execs:
        sp = subprocess.run([item, "-version"], stdout=subprocess.PIPE)
        if sp.returncode == 0:
            result.append(sp.stdout.decode().split('\r\n')[0])
        else:
            result.append(None)
    return result


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
    logging.info(f'Getting {app_name} version: "{path}"')
    assert isinstance(app_name, str), ValueError('Must specify an app name, either "ffmpeg" or "ffprobe"')
    ver_regexp = r'ff.+? version (\S+) '
    to_return = None
    debug = kwargs.get('debug', False)
    try:
        sp = subprocess.run([path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if sp.returncode == 0:
            to_return = sp.stdout.decode().split('\n')[0].split('\r')[0]
            logging.debug(to_return)
            if to_return.startswith(app_name):
                to_return = re.search(ver_regexp, to_return)
            else:
                to_return = None
        else:
            logging.warning(f'"{path}" returned non-zero exit code ({sp.returncode})')
        if to_return is None: to_return = sp.returncode
    except FileNotFoundError as ex:
        logging.error(f"Cannot find file '{path}': {ex}")
        # to_return = ""
    finally:
        if isinstance(to_return, re.Match): 
            to_return = to_return.groups()[0]
        logging.info(f'Got ffmpeg version: {to_return}')
        return to_return


def read_presets(path: Path) -> (Tuple[SSAEncodeProfile, str]):
    """
    Returns: SSAEncodeProfile, naming (string)
    """
    assert path.exists() and path.is_file(), f"{path} does not exists or is not a file"

    # read encode settings
    json_reader = JSONDecoder()
    presets: str
    with open(path.__str__(), 'r') as stream:
        presets = stream.read()
    presets:dict = json_reader.decode(presets)
    encode_presets:dict = presets.get("encode_settings")
    encode_profile = SSAEncodeProfile()
    encode_profile.hardware_acceleration = encode_presets.get("hardware_acceleration", None)
    encode_profile.attachment_copy = encode_presets.get("attachment_copy", encode_profile.attachment_copy)
    encode_profile.audio_bitrate = encode_presets.get("audio_bitrate", encode_profile.audio_bitrate)
    encode_profile.audio_codec = encode_presets.get("audio_codec", encode_profile.audio_codec)
    encode_profile.color_primaries = encode_presets.get("color_primaries", encode_profile.color_primaries)
    encode_profile.color_range = encode_presets.get("color_range", encode_profile.color_range)
    encode_profile.color_trc = encode_presets.get("color_trc", encode_profile.color_trc)
    encode_profile.colorspace = encode_presets.get("colorspace", encode_profile.colorspace)
    encode_profile.pix_fmt = encode_presets.get("pix_fmt", encode_profile.pix_fmt)
    encode_profile.preset = encode_presets.get("preset", encode_profile.preset)
    encode_profile.set_video_resolution(encode_presets.get("resolution_height", -1), True)
    encode_profile.subtitle_decoder = encode_presets.get("subtitle_decoder", encode_profile.subtitle_decoder)
    encode_profile.vf = SSAEncodeProfile.ParamList()
    vf: Dict = encode_presets.get("vf", None)
    if vf is not None:
        encode_profile.vf.name = vf.get("vf_name", encode_profile.vf.name)
        encode_profile.vf.spliter = vf.get("vf_spliter", encode_profile.vf.spliter)
        vf_list: List[Dict] = vf.get("vf_value", [])
        for _ in vf_list:
            encode_profile.vf.add_param(_.get("param"), _.get("value"))
    encode_profile.video_codec = encode_presets.get("video_codec", encode_profile.video_codec)
    encode_profile.video_codec_params = SSAEncodeProfile.ParamList()
    video_codec_params: Dict = encode_presets.get("video_codec_params", None)
    if video_codec_params is not None:
        encode_profile.video_codec_params.name = video_codec_params.get("video_codec_params_name", encode_profile.vf.name)
        encode_profile.video_codec_params.spliter = video_codec_params.get("video_codec_params_spliter", encode_profile.vf.spliter)
        video_codec_params_value_list: List[Dict] = video_codec_params.get("video_codec_params_value", [])
        for _ in video_codec_params_value_list:
            encode_profile.video_codec_params.add_param(_.get("param"), _.get("value"))
    encode_profile.video_profile = encode_presets.get("video_profile", encode_profile.video_profile)
    encode_profile.video_quality = encode_presets.get("video_quality", encode_profile.video_quality)
    # print(encode_presets, type(encode_presets))

    # read naming
    naming: str = presets.get("naming", None)

    return (encode_profile, naming)


def setup_logger(
        class_name: str = None,
        log_level: str = "INFO",
        log_file: Path = None,
        log_fmt: str = None
) -> logging.Logger | None:
    """
    Setup logger

    TODO: Log file writing still fucking doesn't work.... (𓌻‸𓌻) ᴜɢʜ.

    If `class_name` not given, it won't return a logger object.

    Default log format (if `log_fmt` is None): [%(asctime)s] [%(name)s] [%(levelname)s] %(message)s

    This function should only be called once (e.g., called in `if __name__ == __main__`)
    """
    global _logger_setup
    if _logger_setup:
        logging.warning("Logger setup ran multiple times.")

    if not isinstance(log_fmt, str):
        # log format for `logging` and `coloredlog`
        log_fmt = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'

    if isinstance(log_file, Path):
        if not log_file.parent.exists():
            raise NotADirectoryError(f"Cannot find log directory: {log_file.parent.__str__()}")
        if log_file.exists() and not log_file.is_file():
            raise IOError(f"Found a non-file object with the same name as log file: {log_file.__str__()}")
        logging.basicConfig(filemode='a', filename=log_file, format=log_fmt)

    logging.captureWarnings(True)

    # replace black text from field 'levelname' with white bold text or it blends into terminal's background
    coloredlogs.DEFAULT_FIELD_STYLES['levelname'] = dict(bold=True)
    coloredlogs.install(
        log_level,
        fmt='[%(name)s] [%(levelname)s] %(asctime)s - %(message)s',
        stream=sys.stdout,
    )
    if isinstance(class_name, str):
        return logging.getLogger(class_name)
    return None


# testing
if __name__ == "__main__":
    test = 3
    if test == 3:
        read_presets(Path("presets/my_encode_profile_h265_10bit_720p_opus.json"))
    elif test == 2:
        episode = Path(
            r"E:\torrent\[SubsPlease] Komi-san wa, Comyushou desu. - 01 (1080p) [75117D8F].mkv"
        )
        print(get_episode_duration(episode, 'ffmpeg/bin/ffprobe'))
        probe = ffmpeg.probe(episode.__str__(), 'ffmpeg/bin/ffprobe')
        print(probe.get("format").get('duration'))
    elif test == 1:
        print(get_episode_crc32(Path(
            r"Y:\torrents\[SubsPlease] Shikkakumon no Saikyou Kenja - 09 (1080p) [6D93E561].mkv"
        )))
    elif test == 0:
        print(
            extract_names(
                Path(
                    # r"[SubsPlease] Slow Loop - 07 (1080p) [840BACEC].mkv"
                    # r"[EMBER] S01E07-Assigned to Me (Uncensored) [ED08B372].mkv"
                    # r"[DHR][Kino no Tabi (2017)][02][BIG5][720P][AVC_AAC].mp4"
                    # "[AnimeRG] Triage X - 01 [1080p] [x265] [pseudo].mkv"
                    # "[Erai-raws] Girly Air Force - 02 [1080p][Multiple Subtitle].mkv"
                    # "[Hakata Ramen] Sounan desu ka - 12 (How to Replenish Water).mkv"
                    # "[HorribleSubs] Kanojo ga Flag wo Oraretara - 02 [1080p].mkv"
                    # "(Hi10)_Kanojo_ga_Flag_wo_Oraretara_-_14_(DVD_576p)_(Underwater)_(13F0F765).mkv"
                    # "[HYSUB]Komi-san wa, Komyushou Desu.[03][GB_MP4][1280X720].mp4"
                    # "[zza] Girly Air Force - 01 [1080p.x265].mkv"
                    # "[Pixel] Isekai Shokudou - 02 [720p][BD][HEVC][10 bit][Dual Audio][Opus].mkv"
                    # "Shimoneta to Iu Gainen ga Sonzai Shinai Taikutsu na Sekai 12 [BD Unsensored 1080p][HEVC x265 10bit][Multi-Subs].mkv"
                    # "[H3AsO3] Shuumatsu no Harem - 02 (sub castellà).mp4"
                    # "[x_x] Josee, the Tiger and the Fish. [Movie] [BDRip 1080p x265 Main10 2xFlac 2.0ch+5.1ch].mkv"
                    "Chaos Dragon - Sekiryuu Seneki 5 (English Sub).mkv"
                ), True
            )
        )
