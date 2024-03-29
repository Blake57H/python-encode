import logging
import re
import subprocess
from pathlib import Path
from typing import Optional, Union, Tuple

from PySide6.QtWidgets import QWidget, QLineEdit, QLabel, QFileDialog

from python_encode.ui.language import AppSettingsWidgetString as lp
from python_encode.ui.model_program_settings import ApplicationSettingsRepository as Repos, ProgramInfo
from python_encode.ui.ui_app_settings_widget import Ui_Form
from python_encode.utils_qt import StyleSheets, FileDialogFilter as fdf, General, ShowMessageBox

logger = logging.getLogger(__name__)


def set_qlabel_text(label: QLabel, text: str, style: str = '') -> None:
    """get ffmpeg app version and update GUI"""
    label.setText(text)
    if isinstance(style, str):
        label.setStyleSheet(style)


class AppSettingsWidget(QWidget, Ui_Form):

    # app settings getter
    @staticmethod
    def get_ffmpeg_program_info() -> ProgramInfo:
        return Repos.ffmpeg

    @staticmethod
    def get_ffprobe_program_info() -> ProgramInfo:
        return Repos.ffprobe

    @staticmethod
    def get_output_directory() -> Path:
        return Repos.current_output_dir.get()
    
    @staticmethod
    def is_ready(widget: QWidget, display_error_message_box: bool = False) -> bool:
        is_ready_ = AppSettingsWidget.is_file_reading_ready(widget, display_error_message_box)
        return is_ready_ and AppSettingsWidget.is_file_encode_ready(widget, display_error_message_box)            
    
    @staticmethod
    def is_file_reading_ready(widget: QWidget, display_error_message_box: bool = False) -> bool:
        is_ready_ = True
        if not Repos.ffprobe.is_ready:
            if display_error_message_box:
                ShowMessageBox.show_error(widget, lp.ERROR, str.format(lp.MESSAGE_BOX_FF_NOT_FOUND, 'ffprobe'))
            is_ready_ = False
        return  is_ready_   
    
    @staticmethod
    def is_file_encode_ready(widget: QWidget, display_error_message_box: bool = False) -> bool:
        is_ready_ = True
        if not Repos.ffmpeg.is_ready:
            if display_error_message_box:
                ShowMessageBox.show_error(widget, lp.ERROR, str.format(lp.MESSAGE_BOX_FF_NOT_FOUND, 'ffmpeg'))
            is_ready_ = False
        if Repos.current_output_dir.get() is None or not Repos.current_output_dir.get().is_dir():
            logger.debug(Repos.current_output_dir.get())
            if display_error_message_box:
                ShowMessageBox.show_error(widget, lp.ERROR, str.format(lp.MESSAGE_BOX_INVALID_DIR, Repos.current_output_dir.get()))
            is_ready_ = False            
        return is_ready_

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        # self.ffmpeg = [lp.FFMPEG, False, 'ffmpeg'] # config list - (app_name (don't change), is_ready, executable_path)
        # self.ffprobe = [lp.FFPROBE, False, 'ffprobe'] # same as above
        # self.ffmpeg_ready = False
        # self.ffprobe_ready = False

        """signal and slots"""
        self.toolButton_findFfmpeg.clicked.connect(lambda: self._on_select_ffmpeg_location(
            self.lineEdit_ffmpegC, self.label_ffmpegC, Repos.ffmpeg,
            str.format(lp.TITLE_OPEN_FF, lp.FFMPEG),
            fdf.compile(fdf.FFMPEG, fdf.ALL_FILES)
        ))
        self.toolButton_findFfprobe.clicked.connect(lambda: self._on_select_ffmpeg_location(
            self.lineEdit_ffprobeC, self.label_ffprobeC, Repos.ffprobe,
            str.format(lp.TITLE_OPEN_FF, lp.FFPROBE),
            fdf.compile(fdf.FFPROBE, fdf.ALL_FILES)
        ))
        self.pushButton_verifyFfmpeg.clicked.connect(lambda: {
            self._on_verify_ffmpeg_button_clicked(
                self.lineEdit_ffmpegC, self.label_ffmpegC, Repos.ffmpeg
            ),

        })
        self.pushButton_verifyFfprobe.clicked.connect(lambda: {
            self._on_verify_ffmpeg_button_clicked(
                self.lineEdit_ffprobeC, self.label_ffprobeC, Repos.ffprobe
            )
        })
        self.reset_labels()

    @staticmethod
    def _get_ffmpeg_version(path: str, app_name: str = '\b', **kwargs) -> Tuple[Optional[int], str]:
        """
        Get ffmpeg component version (to verify its existence before encoding)

        Param
        -----
            path: ffmpeg/ffprobe/... executable
            app_name: 'ffmpeg'|'ffprobe'

        Returns
        -------
            version string as `str`,
            or `None` if program not found (FileNotExistError),
            or return code as `int` if program exists but did not exit correctly or the program version not found (regular expression did not match)
        """
        logger.info(f'Getting {app_name} version: "{path}"')
        # assert isinstance(app_name, str), ValueError('Must specify an app name, either "ffmpeg" or "ffprobe".')
        ver_regexp = r'ff.+? version (\S+) '
        return_code = None
        return_msg: str
        # debug = kwargs.get('debug', False)
        try:
            sp: subprocess.CompletedProcess[str] = subprocess.run([path, "-version"], stdout=subprocess.PIPE,
                                                                  stderr=subprocess.STDOUT, universal_newlines=True)
            return_code = sp.returncode

            # program returned non-zero exit code, and version string fetched
            if sp.returncode != 0:
                logger.warning(f'"{path}" returned non-zero exit code ({sp.returncode})')
                return_msg = sp.stdout
                return return_code, return_msg

            return_msg = sp.stdout.split('\n')[0].split('\r')[0]  # stdout string, first line

            # program returned 0, and version string fetched
            if return_msg.startswith(app_name):
                version_str = re.search(ver_regexp, return_msg)
                if version_str is not None:
                    logger.debug(version_str)
                    return_msg = version_str.groups()[0]
                    logger.info(f'Got {app_name} version: {return_msg}')
                    return return_code, return_msg

            # program returned 0, but version string is unrecognizable
            logger.warning(f'Unrecognizable version for "{app_name}": "{return_msg}"')
            return return_code, return_msg

        except FileNotFoundError as ex:
            return_msg = f"Cannot find file '{path}': {ex}"
            logger.warning(return_msg)
            return return_code, return_msg
        except OSError as ex:
            return_msg = f"Can't execute '{path}': {ex}"
            logger.warning(return_msg)
            return return_code, return_msg
        except Exception as ex:
            return_msg = f"Unexpected error {type(ex)} at '{path}': {ex}"
            logger.error(return_msg)
            return return_code, return_msg
        # finally:
        #     return return_code, return_msg

    def _dialogue_open_file(self, title: str, file_filter: str) -> Optional[str]:
        """Open file select dialogue and retrieve user selected ffmpeg/ffprobe path"""
        result = QFileDialog.getOpenFileName(self, title, filter=file_filter, options=QFileDialog.Option(QFileDialog.Option.DontResolveSymlinks))[0]
        logger.debug(f"open file dialog, ffmpeg: '{result}'")
        if result == '': return None
        return result

    def _dialogue_open_folder(self, title: str) -> Optional[str]:
        result = QFileDialog.getExistingDirectory(self, caption=title)
        logger.debug(f"select directory: {result}")
        if result == '':
            return None
        return result

    def _on_select_output_directory(self):
        result = self._dialogue_open_folder(lp.TITLE_SELECT_OUTPUT_DIR)
        if result is None:
            return
        self.lineEdit_saveDirectory.setText(result)
        Repos.current_output_dir.set(Path(result))

    def _on_select_ffmpeg_location(self, line_edit: QLineEdit, label: QLabel, program_info: ProgramInfo, title: str,
                                   file_filter: str) -> None:
        """Debug function"""
        result = self._dialogue_open_file(title, file_filter)
        if result is None: return
        line_edit.setText(result)
        self._on_verify_ffmpeg_button_clicked(line_edit, label, program_info)

    def _on_verify_ffmpeg_button_clicked(self, line_edit: QLineEdit, label: QLabel, program: ProgramInfo,
                                         display_message_box: bool = True) -> None:
        logger.debug(f"_on_verify_button_clicked: program name: {program.executable}")

        path = line_edit.text().strip()
        if General.is_string_empty(path):
            path = program.default_exec
        program.executable = path
        code, msg = AppSettingsWidget._get_ffmpeg_version(program.executable, program.program_name)
        logger.debug(f"code={code}, message={msg}")
        if isinstance(msg, str) and code == 0:
            label.setText(str.format(lp.LABEL_FF_VERSION_DISPLAY, msg, path))
            label.setStyleSheet('')
            program.set_ready(True)
            if display_message_box:
                ShowMessageBox.show_info(self,
                                         str.format(lp.MESSAGE_BOX_FF_FOUND, program.program_name),
                                         str.format(lp.LABEL_FF_VERSION_DISPLAY, msg, path))
            return

        if code is None:
            txt = str.format(lp.LABEL_FF_PATH_NOT_FOUND, msg)
        elif isinstance(code, int):
            txt = str.format(lp.LABEL_FF_VERSION_ERROR, path, code, msg)
        else:
            err = f"Unexpected code type: {type(code)}"
            logger.error(err)
            raise RuntimeError(err)
        set_qlabel_text(label, txt, StyleSheets.RED_CONTENT)
        program.set_ready(False)
        if display_message_box:
            ShowMessageBox.show_error(self, str.format(lp.MESSAGE_BOX_FF_NOT_FOUND, program.program_name), txt)
        return

    def reset_labels(self):
        if Repos.ffmpeg.executable != Repos.ffmpeg.default_exec:
            self.lineEdit_ffmpegC.setText(Repos.ffmpeg.executable)
        if Repos.ffprobe.executable != Repos.ffprobe.default_exec:
            self.lineEdit_ffprobeC.setText(Repos.ffprobe.executable)
        self._on_verify_ffmpeg_button_clicked(self.lineEdit_ffmpegC, self.label_ffmpegC, Repos.ffmpeg, False)
        self._on_verify_ffmpeg_button_clicked(self.lineEdit_ffprobeC, self.label_ffprobeC, Repos.ffprobe, False)
        output_dir = Repos.preferred_output_dir.get()
        if output_dir is None:
            output_dir = Repos.current_output_dir.get()
        else:
            Repos.current_output_dir.set(output_dir)
        self.lineEdit_saveDirectory.setText(output_dir.absolute().__str__())
