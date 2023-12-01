import sys

from PySide6 import QtWidgets, QtCore
from python_encode.utils_site_package import HelperFunctions
from pathlib import Path


def main():
    tlr = QtCore.QTranslator()
    tl_path = Path(__file__).parent.joinpath("language")
    tlr_loaded = []
    for qm_file in tl_path.glob("*.qm"):
        tlr_loaded.append((qm_file.stem, tlr.load(qm_file.stem, tl_path.__str__(), '_', '.qm')))
    app = QtWidgets.QApplication(sys.argv)
    app.installTranslator(tlr)

    logger = HelperFunctions.setup_logger(log_level='DEBUG', class_name=__name__)

    logger.debug(f"loaded_translations(lang, is_successful)={tlr_loaded}")
    logger.debug(f"tl_path={tl_path}")
    logger.debug(f'__file__={__file__}')

    # window import must be after translation installation, or translation won't work
    from python_encode.ui.controler_main_window import MainWindow
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()
