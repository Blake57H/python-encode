import enum
from typing import List, Dict, Type


class TypeEnum(enum.Enum):
    GROUP = "group"
    EPISODE_NAME = "episode_name"
    RESOLUTION = "resolution"
    CRC = "crc"
    OTHER = "other"


class ExtractedNameObject:
    def __init__(self) -> (None):
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
        return self.episode_name!=""

    def __str__(self) -> (str):
        return f"Extracted Name: \n" \
                f"\tGroup: {self.release_group}\n" \
                f"\tName: {self.episode_name}\n" \
                f"\tCRC: {self.crc}\n" \
                f"\tResolution: {self.resolution} \n" \
                f"\tOther Tags: {[item for item in self.other_tags]}"            

class Tag:
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
    def __init__(self) -> (None):
        self.tags: List[Tag] = list()
        self.tag_type_map: Dict = {}

    def put_tag(self, subject: Tag) -> (None):
        self.tags.append(subject)
        self.tag_type_map[subject.get_type()] = self.tags.__sizeof__()

    def get_tag(self, index: int) -> (None | Tag):
        if index is None or index >= self.__sizeof__():
            return None
        return self.tags[index]

    def get_tag_index_by_type(self, tag: TypeEnum) -> (int | None):
        """
        Will be used to get indexes of title and episode name 
        """
        return self.tag_type_map.get(tag)

    def is_ready(self) -> (bool):
        return self.get_tag_index_by_type(TypeEnum.GROUP) is not None and self.get_tag_index_by_type(TypeEnum.EPISODE_NAME) is not None

    def get_size(self) -> (int):
        return len(self.tags)

    def __str__(self) -> (str):
        to_return = ""
        for item in self.tags:
            to_return += f"value={item.get_value()}, type={item.get_type()};\n"
        return to_return

