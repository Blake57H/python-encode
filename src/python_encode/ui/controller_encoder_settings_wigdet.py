import logging
from typing import List, Dict

import PySide6
from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import QWidget

from python_encode.custom_objects import EncodePresetObject
from python_encode.ui.language import EncoderSettingsString as lp
from python_encode.ui.model import DictReader
from python_encode.ui.model_encoder_settings import EncoderSettingsRepository as EncodeRepos
from python_encode.ui.ui_encoder_settings_widget import Ui_Form_EncoderSettings
from python_encode.utils import HelperFunctions
from python_encode.utils_qt import ShowMessageBox

logger = logging.getLogger(__name__)


def reload_combox_items(combox: PySide6.QtWidgets.QComboBox, items: List[str]):
    if len(items) == 0:
        logger.warning("Reload combobox with empty list is not allowed.")
        return
    combox.clear()
    combox.addItems(items)
    combox.setCurrentIndex(0)


class EncoderSettingsWidget(QWidget, Ui_Form_EncoderSettings):

    # _preset_list_1 = QAbstractListModel(_preset_list)
    @property
    def selected_preset(self) -> EncodePresetObject:
        return EncodeRepos.get_selected_preset()

    def on_preset_index_changed(self, index):
        try:
            EncodeRepos.set_selected_preset(index)
            # self._selected_preset = self._preset_list[index]
            self.upon_selected_preset_changed()
            logger.debug(f"Selected preset index: {index}, {EncodeRepos.get_selected_preset().preset_name}")
        except IndexError:
            err_txt = lp.MSG_USE_DEFAULT_PRESET
            informative = f"Out of index error occurred while selecting preset, index={index}, len(presets)={len(EncodeRepos.get_preset_names())}"
            logger.error(informative)
            logger.warning(err_txt)
            logger.debug(f"combo box text={self.comboBox_PresetList.currentText()}; index={index}")
            ShowMessageBox.show_error(self, lp.ERROR, err_txt, informative)
            EncodeRepos.load_presets()

    def _reset_labels(self):
        self.label_presetModifiedMark.setVisible(False)


    def update_preset_groupbox(self, selected_preset: EncodePresetObject):
        self.label_presetDisplayName.setText(selected_preset.preset_name)

    def update_miscellaneous_section(self, selected_preset: EncodePresetObject):
        option: DictReader = DictReader(selected_preset.stream_params)
        option.set_from_val_read(lambda val: self.checkBox_enableHwaccel.setChecked(val != ''), 'input', 'hwaccel', defaults='')
        option.set_from_val_read(self.checkBox_keepChapters.setChecked, 'other', 'keep_chapters', defaults=True)
        option.set_from_val_read(self.checkBox_keepChapters.setChecked, 'other', 'keep_attachments', defaults=True)
        
        # fixme: if user wrote a 
        container_extension = option.read("other", "container", defaults=EncodeRepos.get_default_container()[0])
        index = EncodeRepos.get_container_index(container_extension)
        if index == -1:
            self.comboBox_containerSelection.setEditText(container_extension)
            return
        self.comboBox_containerSelection.setCurrentIndex(index)  # this should trigger the currentIndexChanged action

    def upon_selected_preset_changed(self):
        # logger.debug("upon_selected_preset_changed: Updating GUI")
        self.update_preset_groupbox(EncodeRepos.get_selected_preset())
        self.update_miscellaneous_section(EncodeRepos.get_selected_preset())
        self.label_presetModifiedMark.setVisible(False)

    def upon_preset_modified(self, *args, **kwargs):
        self.label_presetModifiedMark.setVisible(True)
        # todo: change ffmpeg command preview

    def preset_modified_signal_connector(self, *signal_instances: PySide6.QtCore.SignalInstance):
        for instance in signal_instances:
            instance.connect(self.upon_preset_modified)
            
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        EncodeRepos.load_encode_options()
        EncodeRepos.load_presets()

        # setting up default values
        reload_combox_items(self.comboBox_PresetList, EncodeRepos.get_preset_names())
        self.comboBox_PresetList.currentIndexChanged.connect(self.on_preset_index_changed)

        reload_combox_items(self.comboBox_containerSelection, EncodeRepos.get_container_names())
        self.comboBox_containerSelection.currentIndexChanged.connect(EncodeRepos.set_selected_container)

        reload_combox_items(self.comboBox_videoCodec, EncodeRepos.get_all_video_codec_names())
        self.comboBox_videoCodec.currentIndexChanged.connect(EncodeRepos.set_selected_video_codec)

        self.preset_modified_signal_connector(
            self.comboBox_containerSelection.currentIndexChanged,
            self.comboBox_containerSelection.editTextChanged,
            self.comboBox_videoCodec.currentIndexChanged
        )

        self._reset_labels()
        
        # todo: Disabled until complete programming
        self.groupBox_basic.setEnabled(False)
        self.groupBox_moreParams.setEnabled(False)
