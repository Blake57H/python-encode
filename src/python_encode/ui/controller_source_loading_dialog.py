import logging
from typing import Callable

from PySide6 import QtGui
from PySide6.QtWidgets import QDialog, QMessageBox, QApplication
from python_encode.ui.ui_source_loading_overlay import Ui_SourceLoadingForm
from python_encode.ui.language import VariousString as lp
from python_encode.utils_qt import tr


logger = logging.getLogger(__name__)


class LoadDialog(Ui_SourceLoadingForm, QDialog):
    """
    loading screen for opening video files
    """
    def __init__(self, close_action: Callable = None) -> None:
        super().__init__()
        self.setupUi(self)
        self.closeEvent = self.on_closing
        # self.close = self.close_dialog
        self.forced_close = False
        self.setModal(True)
        # self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        # self.pushButton = QPushButton()
        self.pushButton_cancel.clicked.connect(self.close)
        self.ctx = __name__
        self.on_user_closing_action: Callable = close_action
        self.reset_labels()
        # QtCore.QTimer.singleShot(5 * 1000, self.close_dialog) # For simulate test direct close 

    def on_closing(self, event: QtGui.QCloseEvent):
        """
        https://stackoverflow.com/questions/25882595/closing-pyqt-messagebox-with-closeevent-of-the-parent-window
        """
        # print(self.direct_close)
        if self.forced_close:
            event.accept()
            return
        answer = QMessageBox.question(
            self,
            lp.FORM_TITLE_CANCEL_TASK,
            lp.FORM_TEXT_CANCEL_TASK,
            QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No)
        # logger.debug(f"close confirm dialog: {answer} ")
        if answer == QMessageBox.StandardButton.Yes or self.forced_close:
            if self.on_user_closing_action: 
                logger.debug("User canceled video import")
                self.on_user_closing_action()
            event.accept()
        else:
            event.ignore()

    def close_dialog(self):
        for childQWidget in self.findChildren(QMessageBox):
            childQWidget.close()
        self.forced_close = True
        return QDialog.close(self)
    
    def reset_labels(self) -> None:
        self.label_currentItem.setText("")
        self.progressBar_currentItem.setValue(0)

    def set_label_text(self, filename: str, current_index: int, total: int) -> None:
        self.label_currentItem.setText(f"{lp.LABEL_READING_FILE} {filename} ({current_index}/{total})")

    def set_progress(self, progress: int):
        """Expect an int value betweem 0 and 100 (inclusive)"""
        # logger.debug(f"received progress: {progress}")
        self.progressBar_currentItem.setValue(progress)
    

    

if __name__ == "__main__":
    import sys
    logging.basicConfig(level='DEBUG')
    app = QApplication(sys.argv)

    # # setup_logger(log_level='DEBUG')

    window = LoadDialog()
    # window.setCentralWidget()
    window.show()

    print(app.exec())