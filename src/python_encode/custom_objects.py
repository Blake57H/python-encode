""" I believe refactor is required... (utils and custom_object are a mess) (better than when it started but still a mess) """

import enum
import json
import logging
import warnings
from pathlib import Path
from typing import Any, Iterable, List, Dict, Tuple, Optional, Union, Set

logger = logging.getLogger(__name__)


class TypeEnum(enum.Enum):
    GROUP = "group"
    EPISODE_NAME = "episode_name"
    RESOLUTION = "resolution"
    CRC = "crc"
    OTHER = "other"


class ParameterObject:
    __slots__ = "param", "value"

    def __init__(self, param, value) -> (None):
        self.param: str = param
        self.value: str = str(value)

    def to_param(self) -> None:
        """Not implemented, DO NOT USE"""
        pass


class EncodePresetObject:
    __slots__ = (
        'preset_dir',
        'preset_name',
        'stream_params',
        'extra_options',
        'naming',
        'tag_divider',
        'container_extension'
    )

    def __init__(self, preset_dir: Optional[Path] = ...):
        self.preset_dir: Optional[Path] = preset_dir
        self.preset_name: str = "FFMPEG DEFAULT"
        self.naming: str = ""
        self.tag_divider: str = " "
        self.stream_params: Dict[str, Union[str, int, float]] = dict()
        self.extra_options: list = list()
        self.container_extension = '.mkv'  # fixme: should this setting be here?
        # self.keep_chapters = True
        # self.keep_attachments = True
        # self.use_hardware_accleration = True

        if not isinstance(preset_dir, Path):
            logger.debug(f"Creating empty preset from non-Path object: {type(preset_dir)}")
            return

        # fixme: until I think of a better place for these configs
        naming_file = preset_dir / "naming.txt"
        if naming_file.is_file():
            self.naming = naming_file.read_text().strip()

        tag_divider_file = preset_dir / "tag_divider.txt"
        if tag_divider_file.is_file():
            self.tag_divider = tag_divider_file.read_text().strip()

        stream_specific_option_file = preset_dir / "basic.json"
        if stream_specific_option_file.is_file():
            self.stream_params = json.loads(stream_specific_option_file.read_bytes())
            self.preset_name = self.stream_params.get("preset_name", self.preset_name)

        extra_option_file = preset_dir / "extra_param.txt"
        if extra_option_file.is_file():
            reading_text = False
            arg_buffer = []
            for arg in extra_option_file.read_text().strip().split():
                if arg.startswith('"'):
                    reading_text = True
                    arg_buffer.clear()
                if reading_text:
                    arg_buffer.append(arg.strip('"'))
                else:
                    self.extra_options.append(arg)
                if arg.endswith('"'):
                    reading_text = False
                    self.extra_options.append(' '.join(arg_buffer))
                    arg_buffer.clear()

        logger.debug(self.__str__())

    def __str__(self):
        return f"""EncodePresetObject:
preset_dir={self.preset_dir.absolute() if isinstance(self.preset_dir, Path) else 'Empty'}, is_dir={self.preset_dir.is_dir() if isinstance(self.preset_dir, Path) else False}
preset_name={self.preset_name}
naming={self.naming}
tag_divider={self.tag_divider}
stream_params={self.stream_params}
extra_options={self.extra_options}
container_extension={self.container_extension}
        """


class AnimeFileObject:
    """ Trying to combine 'AnimeObject' and 'ExtractedNameObject' """

    __slots__ = (
        'file',
        'file_name',

        'video_stream_indexes',
        'audio_stream_indexes',
        'subtitle_stream_indexes',
        'attachment_stream_indexes',
        'chapters',
        'video_resolution',
        'video_length_seconds',
        'video_frame_count',

        'release_group',
        'episode_name',
        'episodes',
        'crc32',

        'omittable_tags',
        'non_omittable_tags'
    )

    def __init__(self) -> None:
        # file bytes related
        self.file: Optional[Path] = None
        self.file_name: Optional[str] = None

        # basically ffprobe
        self.video_stream_indexes: set[int] = set()
        self.audio_stream_indexes: set[int] = set()
        self.subtitle_stream_indexes: set[int] = set()
        self.attachment_stream_indexes: set[int] = set()
        self.chapters: list[
            tuple[str, str, str]] = list()  # chapter list of start time (in second), end time (in second), title
        self.video_resolution: Tuple[Optional[str], Optional[str]] = (None, None)  # width by height, in pixel, numeric
        self.video_length_seconds: Optional[float] = None  # I wonder if floating point precision is an issue
        self.video_frame_count: Optional[int] = None

        # file name related
        self.release_group: Optional[str] = None
        self.episode_name: Optional[str] = None
        self.episodes: Optional[str] = None  # it's a placeholder.
        self.crc32: Tuple[Optional[str], Optional[str]] = (None, None)  # (file bytes, filename label)

        # fixme: if there are better namings
        self.omittable_tags: set[str] = set()  # tags that should be updated, like resolution, codec and checksum
        # tags that should not be modified, like video source such as "BD" and "WEB-DL"
        self.non_omittable_tags: set[str] = set()

    def __eq__(self, other) -> bool:
        return isinstance(other, AnimeFileObject) \
            and (
                    (self.file is None and other.file is None) or
                    (self.file is Path and other.file is Path and self.file.samefile(other.file))
            ) and self.file_name == other.file_name \
            and len(list(set(self.chapters).difference(set(other.chapters)))) == 0 \
            and self.crc32 == other.crc32 \
            and self.video_resolution == other.video_resolution \
            and self.video_length_seconds == other.video_length_seconds \
            and self.video_frame_count == other.video_frame_count \
            and self.release_group == other.release_group \
            and self.episode_name == other.episode_name \
            and self.omittable_tags.__eq__(other.omittable_tags) \
            and self.non_omittable_tags.__eq__(other.non_omittable_tags)

    def __str__(self) -> str:
        return \
            f"""
File Info:
    Full Path: {self.file}
    Name: {self.file_name}
    Chapters: {[chapter[2] for chapter in self.chapters]}
    CRC (calculated, filename): {self.crc32}
    Resolution: {'Unknown' if None in self.video_resolution else 'x'.join(self.video_resolution)}
    Length: {self.video_length_seconds} seconds, {self.video_frame_count} frames
    Group: {self.release_group}
    Episode Name: {self.episode_name}
    Episode (unavailable for now): {self.episodes}
    Omittable Tags: {[item for item in self.omittable_tags]}
    Non Omittable Tags: {[item for item in self.non_omittable_tags]}  
"""

    def get_all_stream_indexes(self) -> Set:
        return set().union(self.video_stream_indexes, self.audio_stream_indexes, self.subtitle_stream_indexes, self.attachment_stream_indexes)


class AnimeObject:
    """ abandoned and may remove in the future """
    __slots__ = (
        'file',
        'file_crc32',
        'video_resolution',
        'video_length',
        'release_group',
        'episode_name',
        'filename_info'
    )

    def __init__(self) -> None:
        warnings.warn(f"Class {self.__class__} deprecating or deprecated", DeprecationWarning)
        self.file: Path = None
        self.file_crc32: str = None
        self.video_resolution: Tuple[str, str] = (None, None)
        # video_length: [seconds, frames]. As long as I don't do division float percision isn't a concern? 
        self.video_length: Tuple[float, int] = (None, None)
        self.filename_info: ExtractedNameObject = None

    def __str__(self) -> str:
        return f"File Info: \n" \
               f"\tFull Path: {self.file.absolute().__str__()}\n" \
               f"\tName: {self.file.name}\n" \
               f"\tFile CRC: {self.file_crc32}\n" \
               f"\tResolution: {'x'.join(map(str, self.video_resolution))} \n" \
               f"\tLength: {self.video_length[0]} seconds, {self.video_length[1]} frames \n" \
               f"{self.filename_info}"


class ExtractedNameObject:
    __slots__ = (
        'filename',
        'release_group',
        'episode_name',
        'resolution',
        'crc',
        'known_tags',
        'other_tags'
    )

    def __init__(self) -> (None):
        warnings.warn(f"Class {self.__class__} deprecating or deprecated", DeprecationWarning)
        self.filename: str = ""
        # basic info, I think
        self.release_group: str = ""
        self.episode_name: str = ""
        self.resolution: int = None
        self.crc: str = ""
        # some other known info
        # Bluray, Uncensored, ... (why don't I merge known tags and other tags?)
        self.known_tags: List[str] = list()
        # other info that I don't ususlly see...
        self.other_tags: List[str] = list()

    def is_ready(self) -> (bool):
        return self.filename != ""

    def __str__(self) -> (str):
        return f"\nExtracted Name: \n" \
               f"\tGroup: {self.release_group}\n" \
               f"\tName: {self.episode_name}\n" \
               f"\tCRC: {self.crc}\n" \
               f"\tResolution: {self.resolution} \n" \
               f"\tOther Tags: {[item for item in self.other_tags]} \n" \
               f"\tOriginal filename: {self.filename}"


class ParamItem(ParameterObject):
    def to_param(self, symbol='=') -> (str):
        return f"{self.param}{symbol}{self.value}"


class SSAEncodeProfile:
    """
    A class to put all encode parameters.
    I may consider switching to ffmpeg's encode profile file (But I don't know how that works as of this writing)

    update:
    I'm now switching to json files to store preset.
    """

    class ParamList:
        """
        For video codec parameters
        (Maybe audio codec as well, haven't tried yet)
        """

        _params: List[ParamItem]
        _params_length = 0
        _hash_map: Dict
        name = None
        spliter = ''

        def __init__(self):
            self._params = list()
            self._hash_map = {}

        def add_param(self, param: str, value: Any) -> (None):
            index = self._hash_map.get(param)
            if index is None:
                index = self._params_length
                self._params.append(ParamItem(param, value))
                self._hash_map[param] = index
                self._params_length += 1
            else:
                self._params[index].value = str(value)

        def add_params(self, param_list: Iterable[ParameterObject]):
            for item in param_list:
                self.add_param(item.param, item.value)

        def remove_param(self, param: str) -> (None):
            index = self._hash_map.pop(param, None)
            if index is None:
                return
            self._params.pop(index)
            self._params_length -= 1

        def as_array_params(self) -> (List[str]):
            if self._params_length == 0:
                return []
            else:
                return [item.to_param() for item in self._params]

        def as_string_params(self) -> (str):
            if self._params_length == 0:
                return ''
            else:
                return self.spliter.join([item.to_param() for item in self._params])

    # use ssa's 1080p profile as default
    # todo: Note written in July 2022:
    # todo: I just learned what __slot__ can do, and I don't know if I should use it here
    # todo: maybe I will put these variables in __init__ then declare a __slot__?
    audio_bitrate = 192  # slider, range from 8 to 320
    audio_codec = 'aac'  # combobox with edittext
    _video_resolution = 1080  # I don't know, combobox?
    video_codec = 'libx265'  # combobox with edittext
    video_quality = 24.2  # slider,  range from 10 to 30
    video_profile = 'main'
    preset = 'slow'  # combobox
    hardware_acceleration = 'auto'
    # I've been copying subtitle and font when doing encode with MKV container
    attachment_copy = False

    # todo check ffmpeg for a proper subtitle decoder
    # Required to do MP4 encode because it needs hard-subs. I prefer MKV for soft-subs so I won't need it.
    # None = ignore subtitle track; '' = copy track; 'xxx' = specify a subtitle decoder
    subtitle_decoder = None

    # todo: there's more option in ssa's task.py
    video_codec_params: ParamList = ParamList()
    video_codec_params.add_params(
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
    video_codec_params.spliter = ':'
    video_codec_params.name = 'x265-params'

    pix_fmt = 'yuv420p'

    vf: ParamList = ParamList()
    vf.add_params(
        [
            ParameterObject('smartblur', '1.5:-0.35:-3.5:0.65:0.25:2.0'),
            ParameterObject(
                'scale', f'-1:{_video_resolution}:spline+accurate_rnd+full_chroma_int')
        ]
    )
    vf.spliter = ','
    vf.name = 'vf'

    color_range = 1
    color_primaries = 1
    color_trc = 1
    colorspace = 1

    def as_ffmpeg_python_args(self) -> (Dict):
        to_return = {'c:a': self.audio_codec,
                     'c:v': self.video_codec,
                     'c:s': self.subtitle_decoder,
                     'b:a': f'{self.audio_bitrate}k',
                     'profile:v': self.video_profile,
                     #  self.video_codec_params.name: self.video_codec_params.as_string_params(),
                     'crf': self.video_quality,
                     'preset': self.preset,
                     'pix_fmt': self.pix_fmt,
                     self.vf.name: self.vf.as_string_params(),
                     'color_range': self.color_range,
                     'color_primaries': self.color_primaries,
                     'color_trc': self.color_trc,
                     'colorspace': self.colorspace,
                     #  'hwaccel': self.hardware_accleration
                     }
        # todo: subtitle decoder for MP4 container
        if self.video_codec_params.name is not None and self.video_codec_params._params_length > 0:
            to_return[self.video_codec_params.name] = self.video_codec_params.as_string_params()
        return to_return

    def set_video_resolution(self, resolution: int, resolution_only: bool = False):
        self._video_resolution = resolution
        if resolution_only:
            self.vf.add_param(
                'scale', f'-1:{resolution}:spline+accurate_rnd+full_chroma_int'
            )
        else:
            self.vf.add_param(
                'scale', f'-1:{resolution}'
            )

    def get_video_resolution(self):
        return self._video_resolution


class Tag:
    """
    todo: what is this for?
    I forgot....
    """
    __slots__ = (
        "value",
        "type_enum"
    )

    def __init__(self, value: str, type_enum: TypeEnum) -> (None):
        self.value = value
        self.type_enum = type_enum

    def get_value(self) -> (str):
        return self.value

    def get_type(self) -> (TypeEnum):
        return self.type_enum

    def __str__(self) -> (str):
        return f"value={self.get_value()}, type={self.get_type()}"


class TagList:
    """
    An object for all unknown tags
    todo: kinda forgot why I create this class in the first place
    """

    __slots__ = "tags", "tag_type_map"

    def __init__(self) -> (None):
        self.tags: List[Tag] = list()
        self.tag_type_map: Dict = {}

    def put_tag(self, subject: Tag) -> (None):
        self.tags.append(subject)
        self.tag_type_map[subject.get_type()] = self.tags.__sizeof__()

    def get_tag(self, index: int) -> (None or Tag):
        if index is None or index >= self.__sizeof__():
            return None
        return self.tags[index]

    def get_tag_index_by_type(self, tag: TypeEnum) -> (int or None):
        """
        Will be used to get indexes of title and episode name 
        """
        return self.tag_type_map.get(tag)

    def is_ready(self) -> (bool):
        # todo: probably deprecated?
        return self.get_tag_index_by_type(TypeEnum.GROUP) is not None and \
            self.get_tag_index_by_type(TypeEnum.EPISODE_NAME) is not None

    def get_size(self) -> (int):
        return len(self.tags)

    def __str__(self) -> (str):
        to_return = ""
        for item in self.tags:
            to_return += f"value={item.get_value()}, type={item.get_type()};\n"
        return to_return


class EncodeListAbstract:
    NAME_DICT = {}

    def get_names(self):
        return [_ for _ in self.NAME_DICT.keys()]
    
    @property
    def values(self) -> List[str]:
        return [_ for _ in self.NAME_DICT.values()]


class EncodeContainerList(EncodeListAbstract):
    NAME_DICT = {
        'Matroska (mkv)': '.mkv'
    }


class EncodeVideoCodecList(EncodeListAbstract):
    NAME_DICT = {
        'Copy': 'copy',
        'HEVC (x265)': 'libx265'
    }


class EncoderAudioCodecList(EncodeListAbstract):
    NAME_DICT = {
        'Copy': 'copy',
        'Opus': 'libopus'
    }


class ProgramInfo:
    __slots__ = (
        '__program_name__',
        '__ready__',
        '__program_exec__',
        '__default_program_exec__'
    )

    @staticmethod
    def new(program: str):
        return ProgramInfo(program, program, program)
        # if not isinstance(program, str):
        #     raise TypeError(f"expect str, got {type(program)}")
        # self.__program_name__ = program
        # self.__program_exec__ = program
        # self.__default_program_exec__ = program

    def __init__(self, program_name: str, program_exec: str, default_exec: str):
        self.__program_name__ = program_name
        self.__ready__ = False
        if not isinstance(program_exec, str):
            raise TypeError(f"expect str, got {type(program_exec)}")
        self.__program_exec__ = program_exec
        self.__default_program_exec__ = default_exec
        
    def set_ready(self, is_ready: bool):
        self.__ready__ = is_ready

    @property
    def is_ready(self) -> bool:
        return self.__ready__

    @property
    def default_exec(self) -> str:
        return self.__default_program_exec__
    
    @property
    def executable(self) -> str:
        return self.__program_exec__

    @executable.setter
    def executable(self, program_exec: str):
        if not isinstance(program_exec, str):
            raise TypeError(f"expect str, got {type(program_exec)}")
        self.__program_exec__ = program_exec

    def set_executable(self, program_exec: str):
        self.executable = program_exec
        
    @property
    def program_name(self) -> str:
        return self.__program_name__


if __name__ == "__main__":
    # print(SSAEncodeProfile().as_ffmpeg_python_args())
    print(EncodeContainerList.NAME_DICT.keys())
