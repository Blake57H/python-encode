import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Union, Optional, Any, Set, overload, Iterable

import PySide6
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QAbstractItemDelegate
from PySide6.QtCore import QAbstractListModel, QAbstractItemModel

from python_encode.custom_objects import EncodePresetObject
from python_encode.ui.language import EncoderSettingsString
from python_encode.ui.model import Repository, DictReader
from python_encode.ui.model_program_settings import ApplicationSettingsRepository as AppSettingsRepo

logger = logging.getLogger(__name__)


class Defaults:
    CONTAINER = (".mkv", "Matroska (mkv)")
    CODEC = ("copy", "copy")
    PRESET = EncodePresetObject(None)

    # post setup
    PRESET.preset_name = EncoderSettingsString.DEFAULT_PRESET_NAME


class ListModel(QAbstractItemModel):
    """I think I will need a delegate in order to use my custom model, which is 面倒くさい"""
    _list_data: List[Tuple[str, str]] = []  # [ (value, display name), ... ]
    _value_list: List[str] = []
    _display_names: List[str] = []
    _header_data = ("value", "display name")

    def __init__(self, initial_data: Optional[List[Tuple[str, str]]] = ...):
        super().__init__()
        if isinstance(initial_data, List):
            self._list_data.extend(initial_data)
            self._selected_item_index = 0 if len(self._list_data) > 0 else -1

    def rowCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        # logger.debug(f"ListModel: row count = {len(self._list_data)}")
        return len(self._value_list)

    def columnCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return 2

    def data(self,
             index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex],
             role: PySide6.QtCore.Qt.ItemDataRole = PySide6.QtCore.Qt.ItemDataRole.DisplayRole
             ) -> Union[Tuple[str, str], str, None]:
        logger.debug(f"ListModel: indexValid={index.isValid()} row={index.row()}, column={index.column()}, role={role}")
        if not index.isValid():
            return None
        # match role:  # only if python compatibility isn't a concern
        if role == PySide6.QtCore.Qt.ItemDataRole.DisplayRole:
            # return self._list_data[index.row()][1]
            return self._display_names[index.row()]
        if role == PySide6.QtCore.Qt.ItemDataRole.UserRole:
            # return self._list_data[index.row()]
            return self._value_list[index.row()], self._display_names[index.row()]
        # return self._list_data[index.row()][index.column()]
        return "~"

    def headerData(self, section: int, orientation: PySide6.QtCore.Qt.Orientation, role: int = ...) -> Any:
        if role != PySide6.QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == PySide6.QtCore.Qt.Orientation.Horizontal:
            return self._header_data[section]

    def index(self, row: int, column: int, parent: Union[
        PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> PySide6.QtCore.QModelIndex:
        # if self.hasIndex(row, column, parent):
        #     return self.buddy
        return self.createIndex(row, column)

    # def on_item_selected(self, selected_item_index):
    #     logger.debug(f"selected item: ", selected_item_index, self._list_data[selected_item_index])
    #     self._selected_item_index = selected_item_index

    def list_items_data(self, column: int = 0) -> List[str]:
        return [_[column] for _ in self._list_data]

    def load_data(self, in_data: Dict[str, str]):
        self.beginResetModel()

        if not isinstance(in_data, Dict):
            logger.warning(f"Invalid predefined container value, expected {type(Dict)}, got {type(in_data)}")
            return
        parsed_container_list: List[Tuple[str, str]] = list()
        container_names: List[str] = list()
        container_extensions: List[str] = list()
        for item in in_data.items():
            # todo: do I need type checking here?
            parsed_container_list.append((item[0], item[1]))
            container_names.append(item[1])
            container_extensions.append(item[0])

        self._list_data = parsed_container_list
        self._display_names = container_names
        self._value_list = container_extensions
        # self._selected_item_index = 0 if len(self._list_data) > 0 else -1

        self.endResetModel()

    def __getitem__(self, item):
        return self._list_data[item]


class EncoderSettingsRepository(Repository):
    # *  prefer using lists because index can get value *
    _preset_list = [Defaults.PRESET]
    # _container_model: QAbstractItemModel = ListModel([Defaults.CONTAINER])  # [ (file_extension, display name), ... ]
    _container_list: List[Tuple[str, str]] = [Defaults.CONTAINER]
    _video_codecs: List[str] = [Defaults.CODEC[0]]
    _audio_codec_list: List[str] = [Defaults.CODEC[0]]
    _subtitle_codec_list: List[str] = [Defaults.CODEC[0]]
    
    _keep_chapters: bool = True
    _keep_attachments: bool = True
    _enable_hardware_accleration: bool = True

    _selected_preset: EncodePresetObject = Defaults.PRESET
    _selected_container: Tuple[str, str] = Defaults.CONTAINER
    _selected_video_codec: str = Defaults.CODEC
    _selected_audio_codec: str = Defaults.CODEC
    _selected_subtitle_codec: str = Defaults.CODEC

    @staticmethod
    def load_encode_options(option_json_object: Dict = ...):
        if not isinstance(option_json_object, Dict):
            pref_file = AppSettingsRepo.encoder_options_file
            if not pref_file.is_file():
                logger.debug(f"Preference file not found: {pref_file.absolute()}")
                return
            try:
                option_json_object = json.loads(pref_file.read_text())
            except json.JSONDecodeError as ex:
                logger.warning(f"Invalid container and codec list file: {ex}")
                return
            logger.debug(f"Loading container and codec list from file")
        else:
            logger.debug(f"User provided custom pre_defined_dict: {option_json_object}")

        dr = DictReader(option_json_object)
        dr.set_from_val_read(lambda val: EncoderSettingsRepository.read_encode_options_from_json_object(EncoderSettingsRepository._container_list, val), "containers")
        dr.set_from_val_read(lambda val: EncoderSettingsRepository.read_encode_options_from_json_array(EncoderSettingsRepository._video_codecs, set(val)), "video_codecs")
        # # tried to use custom model but no avail sue to incorrect model implementation.
        # dr.read(EncoderSettingsRepository._container_model.load_data, "containers")
        # EncoderSettingsRepository.set_selected_container_extension(
        #     min(0, EncoderSettingsRepository._container_model.rowCount() - 1))
        # logger.debug(
        #     f"Container loaded: items={EncoderSettingsRepository._container_model.list_items_data()}, selected={EncoderSettingsRepository._selected_container}",
        # )

    @staticmethod
    def load_presets():
        EncoderSettingsRepository._preset_list = [Defaults.PRESET]
        EncoderSettingsRepository._preset_list.extend([
            EncodePresetObject(_) for _ in AppSettingsRepo.encode_preset_dir.glob('*') if _.is_dir()
        ])

    @staticmethod
    def read_encode_options_from_json_object(save_dict_to: List, json_object: Dict[str, str]) -> bool:
        # Assumes no duplicate key-value pairs, when using a dict object, This function is intended to load container
        # options from json setting file, but by design it can load other JsonObject-like data.
        if not isinstance(json_object, dict):
            logger.warning(f"Invalid 'json_object' type, expected {type(dict)}, got {type(json_object)}")
            return False
        new_containers = {Defaults.CONTAINER[0]: Defaults.CONTAINER[1]}
        new_containers.update(json_object)
        parsed_container_list: List[Tuple[str, str]] = list()
        for item in new_containers.items():
            # todo: do I need type checking here?
            if not isinstance(item[1], str):
                logger.error(f'Invalid value in "{item}", expected {str}, got {type(item[1])}')
                return False
            parsed_container_list.append((item[0], item[1]))
        # EncoderSettingsRepository._container_model.load_data()
        save_dict_to.clear()
        save_dict_to.extend(parsed_container_list)
        return True

    @staticmethod
    def read_encode_options_from_json_array(save_dict_to: List, json_array: Iterable[str]) -> bool:
        # This function is intended to load codec options from json setting file, but by design it can load other
        # JsonArray-like data.
        if not isinstance(json_array, Iterable):
            logger.warning(f"Invalid predefined container value, expected {Iterable}, got {type(json_array)}")
            return False

        new_codec = {Defaults.CODEC[0]}
        new_codec.update(json_array)

        save_dict_to.clear()
        save_dict_to.extend(sorted(new_codec))
        # I want {"copy"/the default} to be the first codec
        save_dict_to.remove(Defaults.CODEC[0])
        save_dict_to.insert(0, Defaults.CODEC[0])
        logger.debug(save_dict_to)
        logger.debug(EncoderSettingsRepository._video_codecs)
        return True
    
    # @staticmethod
    # def read_preset_settings(preset: EncodePresetObject):
        

    # Preset getter and setter

    @staticmethod
    def get_default_preset() -> EncodePresetObject:
        return Defaults.PRESET

    @staticmethod
    def get_selected_preset() -> EncodePresetObject:
        return EncoderSettingsRepository._selected_preset

    @staticmethod
    def set_selected_preset(selected_idx: int):
        EncoderSettingsRepository._selected_preset = EncoderSettingsRepository._preset_list[selected_idx]

    @staticmethod
    def get_preset_names() -> List[str]:
        return [_.preset_name for _ in EncoderSettingsRepository._preset_list]

    # container getter and setter
    @staticmethod
    def get_container_model() -> QAbstractItemModel:
        if not isinstance(EncoderSettingsRepository._container_model, ListModel):
            EncoderSettingsRepository._container_model = ListModel([Defaults.CONTAINER])
        return EncoderSettingsRepository._container_model

    @staticmethod
    def get_container_names() -> List[str]:
        return [container[1] for container in EncoderSettingsRepository._container_list]

    @staticmethod
    def get_container_index(extension: str) -> int:
        """-1 if not found"""
        ext_lst = [container[0] for container in EncoderSettingsRepository._container_list]
        try:
            return ext_lst.index(extension)
        except ValueError:
            return -1
        
    @staticmethod
    def get_selected_container_name() -> str:
        return EncoderSettingsRepository._selected_container[1]

    @staticmethod
    def set_selected_container(selected_idx: int) -> None:
        EncoderSettingsRepository._selected_container = EncoderSettingsRepository._container_list[selected_idx]
        
    @staticmethod
    def get_default_container() -> Tuple[str, str]:
        return Defaults.CONTAINER

    # @staticmethod
    # def get_selected_container_extension() -> str:
    #     return EncoderSettingsRepository._selected_container[0]
    #
    # @staticmethod
    # def set_selected_container_extension(selected_idx: int) -> None:
    #     if selected_idx < 0:
    #         EncoderSettingsRepository._selected_container = Defaults.CONTAINER
    #         return
    #     EncoderSettingsRepository._selected_container = EncoderSettingsRepository._container_model.index(selected_idx,
    #                                                                                                      0).data(
    #         PySide6.QtCore.Qt.ItemDataRole.UserRole)

    # video codec getter and setter

    @staticmethod
    def get_selected_video_codec() -> str:
        return EncoderSettingsRepository._selected_video_codec

    @staticmethod
    def set_selected_video_codec(selected_idx: int) -> None:
        EncoderSettingsRepository._selected_video_codec = EncoderSettingsRepository._video_codecs[selected_idx]
        logger.debug(f'Selecting video codec: {selected_idx} - {EncoderSettingsRepository._selected_video_codec}')

    @staticmethod
    def get_all_video_codec_names() -> List[str]:
        return EncoderSettingsRepository._video_codecs

    # audio codec getter and setter
    @staticmethod
    def get_selected_audio_codec() -> str:
        return EncoderSettingsRepository._selected_audio_codec

    @staticmethod
    def set_selected_audio_codec(selected_idx: int) -> None:
        EncoderSettingsRepository._selected_audio_codec = EncoderSettingsRepository._audio_codec_list[selected_idx]
        logger.debug(f'Selecting audio codec: {selected_idx} - {EncoderSettingsRepository._selected_audio_codec}')

    # subtitle codec getter and setter
    @staticmethod
    def get_selected_subtitle_codec() -> str:
        return EncoderSettingsRepository._selected_subtitle_codec

    @staticmethod
    def set_selected_subtitle_codec(idx: int) -> None:
        EncoderSettingsRepository._selected_subtitle_codec = EncoderSettingsRepository._subtitle_codec_list[idx]
