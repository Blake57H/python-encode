from __future__ import annotations
import os
from typing import Optional
from PySide6 import QtWidgets, QtGui, QtCore
import python_encode.utils

context = 'utils_qt'

# method wrapper for `QtWidgets.QApplication.translate()` so that I can omit the long `QtWidgets.QApplication.translate`
# update: lupdate does not recognize .tr() texts.
tr = QtWidgets.QApplication.translate


# QtCore.QTranslator.translate


# def tr(context: str|bytes, key: str|bytes, disambiguation: Optional[str|bytes] = None, n: int = -1) -> str:
#     """
#     method wrapper for `QtWidgets.QApplication.translate()`
#     so that I can omit the long ``QtWidgets.QApplication``
#     """
#     return QtWidgets.QApplication.translate(context, key, disambiguation, n)

class General(python_encode.utils.HelperFunctions):
    ...


"""
https://stackoverflow.com/questions/11446478/pyside-pyqt-truncate-text-in-qlabel-based-on-minimumsize
"""


class ElideRightLabel(QtWidgets.QLabel):
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        metrics = QtGui.QFontMetrics(self.font())
        elided = metrics.elidedText(self.text(), QtCore.Qt.ElideRight, self.width())

        painter.drawText(self.rect(), self.alignment(), elided)


class StyleSheets:
    GREEN_CONTENT = "color: green"
    RED_CONTENT = "color: red"


class ShowMessageBox:
    icons = QtWidgets.QMessageBox.Icon
    buttons = QtWidgets.QMessageBox.StandardButton

    @staticmethod
    def show_warning(parent: QtWidgets.QWidget, title: str, text: str,
                     informative_text: Optional[str] = "") -> QtWidgets.QMessageBox.StandardButton:
        msg_box = QtWidgets.QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setInformativeText(informative_text)
        msg_box.setIcon(ShowMessageBox.icons.Warning)
        msg_box.setStandardButtons(ShowMessageBox.buttons.Ok)
        # return QtWidgets.QMessageBox.(
        #     parent=parent,
        #     title=title,
        #     text=text,
        #     informativeText
        # )
        return msg_box.exec()

    @staticmethod
    def show_question(parent: QtWidgets.QWidget, title: str, text: str,
                      informative_text: Optional[str] = "",
                      buttons: ShowMessageBox.buttons = buttons.Ok | buttons.Cancel
                      ) -> QtWidgets.QMessageBox.StandardButton:
        msg_box = QtWidgets.QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setInformativeText(informative_text)
        msg_box.setIcon(ShowMessageBox.icons.Question)
        msg_box.setStandardButtons(buttons)
        return msg_box.exec()

    @staticmethod
    def show_info(parent: QtWidgets.QWidget, title: str, text: str,
                  informative_text: Optional[str] = "") -> QtWidgets.QMessageBox.StandardButton:
        msg_box = QtWidgets.QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setInformativeText(informative_text)
        msg_box.setIcon(ShowMessageBox.icons.Information)
        msg_box.setStandardButtons(ShowMessageBox.buttons.Ok)
        return msg_box.exec()

    @staticmethod
    def show_error(parent: QtWidgets.QWidget, title: str, text: str,
                   informative_text: Optional[str] = "") -> QtWidgets.QMessageBox.StandardButton:
        msg_box = QtWidgets.QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setInformativeText(informative_text)
        msg_box.setIcon(ShowMessageBox.icons.Critical)
        msg_box.setStandardButtons(ShowMessageBox.buttons.Ok)
        return msg_box.exec()


class FileDialogFilter:
    ALL_FILES = f'{tr(context, "All Files")} (*)'
    ANIME = f"{tr(context, 'Most common anime video format')} (*.mkv *.mp4)"
    FFMPEG = f"ffmpeg (ffmpeg ffmpeg.exe)"
    FFPROBE = f"ffprobe (ffprobe ffprobe.exe)"

    @staticmethod
    def compile(*filters: str) -> str:
        """returns qt file dialog filter string"""
        return ";;".join(filters)


if __name__ == "__main__":
    test = 0
    if test == 0:
        # print(FileDialogFilter.compile('a','b','c'))
        app = QtWidgets.QApplication()
        win = QtWidgets.QMainWindow()
        filter = FileDialogFilter.compile(FileDialogFilter.FFMPEG, FileDialogFilter.ALL_FILES)
        print(filter)
        result = QtWidgets.QFileDialog.getOpenFileNames(win, "dialog", filter=filter)
        print(result)
        win.show()
        # print(QtWidgets.QApplication.translate('abcde', 'fghij'))
