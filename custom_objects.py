import enum
from typing import Any, Iterable, List, Dict, Tuple, overload


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

    def to_param(self):
        pass


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
        self.filename: str = ""
        # basic info, I think
        self.release_group: str = ""
        self.episode_name: str = ""
        self.resolution: int = None
        self.crc: str = ""
        # some other known info
        # Bluray, Uncensored, ...
        self.known_tags: List[str] = list()
        # info not recognized
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
                     'b:a': f'{self.audio_bitrate}k',
                     'profile:v': self.video_profile,
                     self.video_codec_params.name: self.video_codec_params.as_string_params(),
                     'crf': self.video_quality,
                     'preset': self.preset,
                     'pix_fmt': self.pix_fmt,
                     self.vf.name: self.vf.as_string_params(),
                     'color_range': self.color_range,
                     'color_primaries': self.color_primaries,
                     'color_trc': self.color_trc,
                     'colorspace': self.colorspace}
        # todo: subtitle decoder for MP4 container
        return to_return

    def set_video_resolution(self, resolution: int):
        self._video_resolution = resolution
        self.vf.add_param(
            'scale', f'-1:{resolution}:spline+accurate_rnd+full_chroma_int'
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


if __name__ == "__main__":
    print(SSAEncodeProfile().as_ffmpeg_python_args())
