import re
import time
from custom_objects import ExtractedNameObject, SSAEncodeProfile, TagList, TypeEnum, Tag
from pathlib import Path
from typing import List, Tuple
import binascii

"""
While writing a utility....
I still have trouble understanding python regular expression and I thought writing something on my own
is a good idea....
Basically me reading SSA's code and trying to figure out how it works...
"""


def extract_names(title: Path) -> (ExtractedNameObject):
    """
    Extract episode title and tags (which includs group name, resolution, crc and others).
    Processing logic will be prioritized on SubsPlease. May add logic to process names from 
    other group but I'd like to take care of my need first.

    Parameters
    ----------
    title: str
        Episode file name (e.g. [SomeGroup] Some Anime - Episode 1 [CRC code].mkv)

    Returns
    -------
    object: ExtractedNameObject
    """

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
        subject = subject[len(content)+2:]
        return subject, content

    def read_parenthesis(subject: str) -> (Tuple[str, str]):
        content = re.findall(r'^\(([^\)]*)\)', title)[0]
        subject = subject[len(content)+2:]
        return subject, content

    def find_resolution(subject: str) -> (Tuple[(int or None), str]):
        # resolution_regular_expresion = [r'.*(\d+)[p|i|P|I].*', r'.*\d+[x|X](\d+).*']
        resolution_regular_expresion = [r'(\d+)[p|i|P|I]', r'\d+[x|X](\d+)']
        for item in resolution_regular_expresion:
            potential_resolution = re.search(item, subject)
            if potential_resolution is None:
                continue
            rest_of_subject = ''
            if subject == potential_resolution.group():
                pass
            elif subject.startswith(potential_resolution.group()):
                rest_of_subject = subject[potential_resolution.end()+1:]
            elif subject.endswith(potential_resolution.group()):
                rest_of_subject = subject[:potential_resolution.start()-1]
            else:
                text_before_resolution = subject[:potential_resolution.start()]
                text_after_resolution = subject[potential_resolution.end()+1:]
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
            return int(re.findall(item, subject)[0]), rest_of_subject

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
        return (None,)*2

    # names: TagList = TagList()
    episode_info = ExtractedNameObject()

    while(len(title) > 0):
        is_text = False
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
        # first text read (in brackets or not) will be treated
        if episode_info.release_group == "":
            if not is_text:
                episode_info.release_group = content
                continue
            else:
                title = title.replace('_', ' ')
                episode_info.release_group = "UNKNOWN"
        # assuming every single word not enclosed in brackets or parenthesis is episode name
        if is_text:
            if len(episode_info.episode_name) > 0:
                episode_info.episode_name += " "
            episode_info.episode_name += content
            continue
        # check if text matches CRC code's patten
        if len(content) == 8:
            potential_crc = re.findall(r'([0-9|a-f|A-F]*)', content)
            if len(potential_crc) > 0 and potential_crc[0] == content:
                episode_info.crc = content
                continue
        # check if text is resolution
        if episode_info.resolution is None:
            episode_info.resolution, item = find_resolution(content)
            if item is not None:
                episode_info.other_tags.append(item)
            if episode_info.resolution is not None:
                continue
        # otherwise treat it as other tag, like "uncensored", "AVC AAC", "WEB-DL" etc...
        episode_info.other_tags.append(content)


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
    file_crc_val = calculate_crc32(file)
    return file_crc_val == crc_val


def calculate_crc32(file: Path) -> (str):
    """
    Calculate CRC32 for an episode, and return the value as string

    Note
    ----
    It's doing unsigned 32-bit crc according to:
    https://stackoverflow.com/questions/30092226/how-to-calculate-crc32-with-python-to-match-online-results
    and
    https://docs.python.org/3/library/binascii.html#binascii.crc32
    """
    # make sure it's unsigned
    crc32_value = (binascii.crc32(file.read_bytes()) & 0xFFFFFFFF)
    crc32_hex = hex(crc32_value)
    crc32_str = crc32_hex[2:]
    zeros = 8 - len(crc32_str)
    crc32_str = '0'*zeros + crc32_str
    return crc32_str.upper()


def update_filename(episode_info: ExtractedNameObject, episode_file: Path, encode_profile: SSAEncodeProfile) -> (Path):
    assert episode_file.exists() and episode_file.is_file()
    crc = calculate_crc32(episode_file)
    filename = f"[src={episode_info.release_group}] {episode_info.episode_name} ({encode_profile._video_resolution}) [{crc}]{episode_file.suffix}"
    episode_file = episode_file.rename(filename)
    return episode_file



# testing
if __name__ == "__main__":
    test = 1
    if test == 1:
        calculate_crc32(
            r"Y:\torrents\[SubsPlease] Shikkakumon no Saikyou Kenja - 09 (1080p) [6D93E561].mkv"
        )
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
                    "[x_x] Josee, the Tiger and the Fish. [Movie] [BDRip 1080p x265 Main10 2xFlac 2.0ch+5.1ch].mkv"
                )
            )
        )
