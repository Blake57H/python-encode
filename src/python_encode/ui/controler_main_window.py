from __future__ import annotations

import logging
from pathlib import Path
from threading import Thread
from typing import List, Optional

from PySide6.QtCore import QThread, Qt, Signal, SignalInstance
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow, QFormLayout, QFileDialog

from python_encode.custom_objects import AnimeFileObject, EncodeContainerList
from python_encode.modules_qt import AnimeFileObjectWorkerQT, AnimeEncodeWorkerQT
from python_encode.ui.controller_app_settings_widget import AppSettingsWidget
from python_encode.ui.controller_encoder_settings_wigdet import EncoderSettingsWidget
from python_encode.ui.controller_source_info_widget import SourceInfoWidget
from python_encode.ui.controller_source_loading_dialog import LoadDialog
from python_encode.ui.language import MainWindowString as Lp  # lp = language pack
from python_encode.ui.ui_main_window import Ui_MainWindow
from python_encode.utils_qt import FileDialogFilter as fdf, ShowMessageBox  # , tr

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, Ui_MainWindow):

    input_files_selected_signal: SignalInstance = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.read_file_thread = None
        self.encode_thread = None
        self.master_encode_thread: Thread = Thread()

        """signal and slot"""
        # self.onSelectSourceTriggered = self.open_source_file
        self.setupUi(self)
        self.input_files_selected_signal.connect(self.read_source_file)

        """class variable"""
        self.input_source_anime_objects: List[AnimeFileObject] = list()  # valid sources
        self.input_source_paths: List[str] = list()  # user inputs
        self._load_video_progress_dialog = LoadDialog()
        self.read_file_worker = AnimeFileObjectWorkerQT()
        self.encode_worker: AnimeEncodeWorkerQT = ...

        """UI element"""
        self.info_widget_controller = SourceInfoWidget()
        info_widget = QFormLayout()
        info_widget.setContentsMargins(0,0,0,0)
        info_widget.addWidget(self.info_widget_controller)
        self.widget_tabWidgetPageInputList.setLayout(info_widget)

        self.app_setting_widget_controller = AppSettingsWidget()
        app_setting_widget = QFormLayout()
        app_setting_widget.setContentsMargins(0,0,0,0)
        app_setting_widget.addWidget(self.app_setting_widget_controller)
        self.tab_appSettings.setLayout(app_setting_widget)

        self.encode_settings_widget_controller = EncoderSettingsWidget()
        encoder_setting_widget = QFormLayout()
        encoder_setting_widget.setContentsMargins(0,0,0,0)
        encoder_setting_widget.addWidget(self.encode_settings_widget_controller)
        self.tab_encoderSettings.setLayout(encoder_setting_widget)

        self.tabWidget.setCurrentIndex(0)
        self.reset_labels()

        """debug"""
        self.toolButton.clicked.connect(self.displayOverlay)

    def reset_labels(self):
        # fixme: I tried make long text label ends with ellipses, and I gave up
        # self.label_sourceFilenameC = ElideRightLabel()
        # self.label_sourceFilenameC.setText(language_pack.DEBUG_LONG_TEXT)
        logger.info(Lp.HINT_OPEN_SOURCE)
        self.label_sourceFilenameC.setText(Lp.HINT_OPEN_SOURCE)
        self.label_multipleInputCounter.setText('')
        self.widget_progressContainer.setVisible(False)
        self.label_statusTextGlobal.setText(Lp.READY)
        self.pushButton_startStopEncode.setText(Lp.BUTTON_START_ENCODE)

    def on_loading_anime(self, ao_list: list[AnimeFileObject], input_list: Optional[list[str]] = None) -> None:
        """
        Update input list labels in main window and input info widget

        ao_list: A list of 'AnimeObject's

        input_list: A list of input filepath
        """
        logger.debug(f'AnimeFileObject list: {ao_list}')
        logger.debug(f'Path list: {input_list}')
        if input_list is None:
            input_list = self.input_source_paths
        if self.read_file_worker.should_quit_immediately:
            logger.debug("Ignore UI update because user canceled video import")
            return 
        self.input_source_anime_objects = list()
        error_list = list()
        for idx, obj in enumerate(ao_list):
            if obj is not None:
                self.input_source_anime_objects.append(obj)
            else:
                error_list.append(input_list[idx])
        logger.debug(f"Valid source: {[_.file_name for _ in self.input_source_anime_objects]}")
        logger.debug(F"Invalid source: {error_list}")
        valid_source_len = len(self.input_source_anime_objects)
        if len(error_list) > 0:
            ShowMessageBox.show_warning(
                parent=self,
                # title=QCoreApplication.translate('MainWindow', 'Cannot open file(s)', n=len(error_list)),
                title=Lp.TITLE_FFPROBE_READ_FAIL,
                text=Lp.HINT_FFPROBE_READ_FAIL,
                informative_text='\n'.join(error_list)
            )
        if valid_source_len == 0: return
        if valid_source_len == 1: 
            self.label_multipleInputCounter.setText('')
        if valid_source_len > 1: 
            self.label_multipleInputCounter.setText(
                str.format(Lp.HINT_MULTIPLE_INPUTS, valid_source_len - 1)
            )
        self.label_sourceFilenameC.setText(self.input_source_anime_objects[0].file_name)
        self.info_widget_controller.show_content(self.input_source_anime_objects)

    def displayOverlay(self):
        """debug"""
        _ = LoadDialog()
        print("ready to show dialog")
        _.show()
        print("show called, starting thread")
        result = _.forced_close
        print("clicked", result)

    def read_source_button_clicked(self):
        """ upon "open source" button clicked, open a file open dialogue """
        title = Lp.OPEN_SOURCE
        file_dialogue_filter = fdf.compile(fdf.ANIME, fdf.ALL_FILES)
        result: tuple[list[str], str] = QFileDialog.getOpenFileNames(self, title, filter=file_dialogue_filter)
        logger.debug(f"selected files: {result}")
        result_len = len(result[0])
        self.input_source_paths = result[0]
        if result_len == 0:
            return
        self.input_files_selected_signal.emit()

    def read_source_file(self):
        input_source_size = len(self.input_source_paths)
        if input_source_size == 0:
            ShowMessageBox.show_error(parent=self, title=Lp.ERROR, text=Lp.MSG_INFO_NO_INPUT)
            return
        if not AppSettingsWidget.is_ready(widget=self, display_error_message_box=True):
            return

        self._load_video_progress_dialog = LoadDialog()
        self.read_file_thread = QThread()
        self.read_file_worker = AnimeFileObjectWorkerQT(ffprobe=AppSettingsWidget.get_ffprobe_program_info().executable)
        self.read_file_worker.moveToThread(self.read_file_thread)

        self.read_file_thread.started.connect(self.read_file_worker.run)
        self.read_file_thread.finished.connect(self.read_file_thread.deleteLater)
        self.read_file_worker.input_subjects = self.input_source_paths
        self.read_file_worker.on_finishing.connect(self.read_file_thread.quit)
        self.read_file_worker.on_finishing.connect(self.read_file_worker.deleteLater)
        self.read_file_worker.on_finishing.connect(lambda: self.tabWidgetPageInputList.setEnabled(True))
        self.read_file_worker.on_finishing.connect(self._load_video_progress_dialog.close_dialog)
        self.read_file_worker.on_result_return.connect(self.on_loading_anime)
        self.read_file_worker.on_progresstitle_update.connect(lambda a, b: self._load_video_progress_dialog.set_label_text(a, b + 1, input_source_size))
        self.read_file_worker.on_progressbar_update.connect(self._load_video_progress_dialog.set_progress)
        self._load_video_progress_dialog.on_user_closing_action = self.read_file_worker.exit_now

        self._load_video_progress_dialog.show()
        self.tabWidgetPageInputList.setEnabled(False)
        self.read_file_thread.start()

    def start_encode_process(self, anime_objects: List[AnimeFileObject]):
        self.encode_thread = QThread()
        self.encode_worker = AnimeEncodeWorkerQT(
            encode_file=anime_objects,
            output_dir=self.app_setting_widget_controller.get_output_directory(),
            ffmpeg=self.app_setting_widget_controller.get_ffmpeg_program_info(),
            ffprobe=self.app_setting_widget_controller.get_ffprobe_program_info(),
            encode_preset=self.encode_settings_widget_controller.selected_preset,
            selected_streams=...    # todo: add stream selection in encode settings
        )
        self.encode_worker.config_signal(
            on_starting_callbacks=[
                lambda args: self.progressBar_statusGlobal.setValue(0),
                lambda args: self.label_progressTextForFFMPEG.setText(''),
                lambda arg: self.label_statusTextGlobal.setText(str.format(Lp.HINT_ENCODING_FILE, arg)),
                lambda arg: self.widget_progressContainer.setVisible(True),
                lambda arg: self.pushButton_startStopEncode.setText(Lp.BUTTON_STOP_ENCODE)
            ],
            on_progress_percentage_update_callback=self.progressBar_statusGlobal.setValue,
            on_progress_text_update_callback=self.label_progressTextForFFMPEG.setText,
            on_encode_finished=[
                self.encode_thread.quit,
                self.encode_worker.deleteLater,
                lambda : self.label_statusTextGlobal.setText(Lp.HINT_ENCODE_COMPLETED),
                lambda : self.widget_progressContainer.setVisible(False),
                lambda : self.pushButton_startStopEncode.setText(Lp.BUTTON_START_ENCODE)
            ],
            return_encoded_file=lambda file_list: ...
        )
        self.encode_worker.moveToThread(self.encode_thread)

        self.encode_thread.finished.connect(self.encode_thread.deleteLater)
        self.encode_thread.started.connect(self.encode_worker.run)
        self.encode_thread.start(QThread.Priority.LowPriority)

    def encode_button_clicked(self):
        logger.debug("start / stop button clicked")
        logger.debug(f"encode_worker initialized: {isinstance(self.encode_worker, AnimeEncodeWorkerQT)}")
        logger.debug(f"encode_worker is running: {isinstance(self.encode_worker, AnimeEncodeWorkerQT) and self.encode_worker.isRunning()}")
        if isinstance(self.encode_worker, AnimeEncodeWorkerQT) and self.encode_worker.isRunning():
            should_stop = self.handle_user_cancelling_encode()
            if should_stop:
                self.encode_worker.signal_quit()
            return

        if len(self.input_source_anime_objects) == 0:
            ShowMessageBox.show_info(self, Lp.INFO, Lp.MSG_INFO_NO_INPUT)
            return

        self.start_encode_process(self.input_source_anime_objects)

    def handle_user_cancelling_encode(self) -> bool:
        """Shows a message box asking for confirmation, and returns boolean indicating if encode should stop"""
        answer = ShowMessageBox.show_question(
            self,
            title=Lp.FORM_TITLE_CANCEL_TASK,
            text=Lp.FORM_TEXT_CANCEL_TASK,
            buttons=ShowMessageBox.buttons.Yes | ShowMessageBox.buttons.No
        )
        # logger.debug(f"close confirm dialog: {answer} ")
        return answer == ShowMessageBox.buttons.Yes

    def closeEvent(self, event: QCloseEvent) -> None:
        logger.debug(f"User closing main window. Encode worker is initialized and running = {isinstance(self.encode_worker, AnimeEncodeWorkerQT) and self.encode_worker.isRunning()}")
        if isinstance(self.encode_worker, type(...)) or not self.encode_worker.isRunning():
            event.accept()
            return
        if self.handle_user_cancelling_encode():
            self.encode_worker.signal_quit()
            logger.debug("User closing windows, and encode stop signal is sent.")
            while self.encode_worker.isRunning():
                pass  # blocks until encode process completes
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        """ unnecessary in this case, kept for testing/debugging purpose """
        # logger.debug(f"File drag started, hasUrls={event.mimeData().hasUrls()}")
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """ unnecessary in this case, kept for testing/debugging purpose (cli is blowing up) """
        # logger.debug(f"File drag moving, hasUrls={event.mimeData().hasUrls()}")
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        logger.debug(f"File dropped, hasUrls={event.mimeData().hasUrls()}, mimeData.urls={event.mimeData().urls()}")
        
        if not event.mimeData().hasUrls():
            event.ignore()
            return
        logger.debug(f"mimeData.urls[0]={event.mimeData().urls()[0].toLocalFile()}")
        event.setDropAction(Qt.CopyAction)
        event.accept()
        
        url_list = list()
        # valid_suffix = EncodeContainerList().values  # file checking is handled by ffprobe parse result, no need to check extension here.
        # for url in event.mimeData().urls():
        #     url_list.append(url.toLocalFile())
        self.input_source_paths.clear()
        self.input_source_paths.extend([_.toLocalFile() for _ in event.mimeData().urls()])
        logger.debug(f"dropped urls: {self.input_source_paths}")
        self.input_files_selected_signal.emit()

