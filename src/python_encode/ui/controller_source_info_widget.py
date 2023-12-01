import logging
from python_encode.custom_objects import AnimeFileObject
from python_encode.ui.ui_source_info_widget import Ui_source_info_widget
from PySide6.QtWidgets import QWidget
from python_encode.ui.language import SourceInfoWidgetString as lp
from python_encode.utils import HelperFunctions

from typing import List


class SourceInfoWidget(QWidget, Ui_source_info_widget):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.anime_object_list: list[AnimeFileObject] = list()
        self.logger = logging.getLogger(__name__)
        self.cxt = __name__
        self.reset_content()

        """listeners"""
        self.comboBox_inputSourcesList.currentIndexChanged.connect(self.on_combox_item_changed)

    def reset_content(self):
        self.anime_object_list.clear()
        self.comboBox_inputSourcesList.clear()
        self.label_fullPathContent.setText('')
        self.label_animeNameContent.setText('')
        self.label_groupContent.setText('')
        self.label_CRC32FileC.setText('')
        self.label_CRC32FileT.setVisible(False)
        self.label_CRC32NameC.setText('')
        self.label_CRC32NameT.setVisible(False)
        self.label_CRC32CheckResult.setText('')
        self.label_videoLengthC.setText('')
        self.label_resolutionC.setText('')
        self.label_tagC.setText('')
        self.label_ChaptersContent.setText('')
        self.label_StreamsC.setText('')

    def show_content(self, anime_objects: List[AnimeFileObject]) -> None:
        self.reset_content()
        self.anime_object_list.extend(anime_objects)
        self.comboBox_inputSourcesList.addItems([_.file_name for _ in anime_objects])

    def on_combox_item_changed(self, index: int):
        if index == -1: return
        if index >= self.anime_object_list.__len__():
            self.logger.warning("index error: selected %d, list size %d", index, len(self.anime_object_list))
        anime_object: AnimeFileObject = self.anime_object_list[index]
        self.logger.debug(f'combobox item changed{anime_object}')
        self.label_fullPathContent.setText(anime_object.file.__str__())
        self.label_animeNameContent.setText(anime_object.episode_name)
        self.label_groupContent.setText(anime_object.release_group)
        self.label_CRC32FileT.setVisible(True)
        self.label_CRC32FileC.setText(anime_object.crc32[0])
        name_crc32 = anime_object.crc32[1]
        if HelperFunctions.is_string_empty(name_crc32):
            name_crc32 = lp.LABEL_CRC_NOT_PRESENT
            crc32_match = ''
        else:
            crc32_match = lp.LABEL_CRC_MATCH if name_crc32 == anime_object.crc32[0] else lp.LABEL_CRC_NOT_MATCH
        self.label_CRC32NameC.setText(name_crc32)
        self.label_CRC32NameT.setVisible(True)
        self.label_CRC32CheckResult.setText(crc32_match)
        video_length = f"{str.format(lp.LABEL_VIDEO_LENGTH_SECONDS, int(anime_object.video_length_seconds))} ({str.format(lp.LABEL_VIDEO_LENGTH_FRAMES, anime_object.video_frame_count)})"
        self.label_videoLengthC.setText(video_length)
        self.label_resolutionC.setText('x'.join(map(str, anime_object.video_resolution)))
        self.label_tagC.setText(', '.join(anime_object.non_omittable_tags))
        self.label_ChaptersContent.setText(', '.join(map(lambda subject: subject[2], anime_object.chapters)))
        self.label_StreamsC.setText(lp.LABEL_STREAM_DESCRIPTION.format(len(anime_object.audio_stream_indexes), len(anime_object.subtitle_stream_indexes), len(anime_object.attachment_stream_indexes)))
