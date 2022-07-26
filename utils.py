import re
import subprocess
import time
import zlib
from datetime import datetime

from custom_objects import ExtractedNameObject, SSAEncodeProfile, TagList, TypeEnum, Tag
from pathlib import Path
from typing import Dict, List, Tuple
import binascii
import ffmpeg

"""
While writing a utility....
I still have trouble understanding python regular expression and I thought writing something on my own
is a good idea....
Basically me reading SSA's code and trying to figure out how it works...
"""


def print_msg(msg: str, flush: bool = False, end='\n'):
    """
    Print with time before the message
    :param msg:
    :param flush:
    :param end:
    :return:
    """
    print(f"[{datetime.now()}] {msg}", flush=flush, end=end)


def extract_names(title: Path) -> (ExtractedNameObject):
    """
    Extract episode title and tags (which includes group name, resolution, crc and others).
    Processing logic will be prioritized on SubsPlease. May add logic to process names from 
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
                # and I want to respect that.
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


def get_episode_crc32(file: Path) -> (str):
    """
    Calculate CRC32 for an episode, and return the value as string

    Note
    ----
    It's doing unsigned 32-bit crc according to:
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
    with open(file.__str__(), 'rb') as fh:
        hash_val = 0
        while True:
            s = fh.read(65536)
            if not s:
                break
            hash_val = zlib.crc32(s, hash_val)
        # return "%08X" % (hash & 0xFFFFFFFF)
        return format((hash_val & 0xFFFFFFFF), '08X')


def update_filename(
        episode_info: ExtractedNameObject,
        episode_file: Path,
        encode_profile: SSAEncodeProfile = None,
        naming_rule: str = None,
        ffprobe_exec: str = "ffprobe",
        update_file=True) -> (Path):
    assert episode_file.exists() and episode_file.is_file()
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
    if update_file:
        return episode_file.rename(episode_file.parent.joinpath(filename))
    else:
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


def get_episode_duration(episode_file: Path, ffprobe_exec="ffprobe") -> (float or None):
    if get_ff_version(ffprobe_exec) is None:
        print("ffprobe not installed, install ffmpeg to continue: https://ffmpeg.org/download.html")
        return None
    source_duration = None
    try:
        source_info = ffmpeg.probe(episode_file.__str__(), cmd=ffprobe_exec)
        duration_str = source_info.get("format").get("duration")
        if duration_str is not None:
            source_duration = float(duration_str)
    except ffmpeg.Error as ex:
        print(f"Unable to open {episode_file.name} as video")
    except ValueError as ex:
        print(ex)
    finally:
        return source_duration


# ditching
def get_ffmpeg_version(execs: List[str] = None) -> List[str]:
    """
    I ditched this thing and it should not be used
    """
    if execs is None:
        execs = list(["ffmpeg", "ffprobe"])
    result = list()
    for item in execs:
        sp = subprocess.run(item + " -version", stdout=subprocess.PIPE)
        if sp.returncode == 0:
            result.append(sp.stdout.decode().split('\r\n')[0])
        else:
            result.append(None)
    return result


def get_ff_version(path: str) -> (str | None):
    """
    get ffmpeg component version (to verify its existence before encoding)
    :param path: ffmpeg/ffprobe/... executable
    :return: version string, or None if not found
    """
    sp = subprocess.run(path + " -version", stdout=subprocess.PIPE)
    if sp.returncode == 0:
        return sp.stdout.decode().split('\r\n')[0]
    else:
        return None


# testing
if __name__ == "__main__":
    test = 2
    if test == 2:
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
                    "[Pixel] Isekai Shokudou - 02 [720p][BD][HEVC][10 bit][Dual Audio][Opus].mkv"
                    # "Shimoneta to Iu Gainen ga Sonzai Shinai Taikutsu na Sekai 12 [BD Unsensored 1080p][HEVC x265 10bit][Multi-Subs].mkv"
                    # "[H3AsO3] Shuumatsu no Harem - 02 (sub castellà).mp4"
                    # "[x_x] Josee, the Tiger and the Fish. [Movie] [BDRip 1080p x265 Main10 2xFlac 2.0ch+5.1ch].mkv"
                )
            )
        )
