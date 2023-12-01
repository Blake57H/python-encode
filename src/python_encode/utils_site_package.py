from __future__ import annotations

import json
import logging
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional, Callable, Dict, List

import coloredlogs

from python_encode.utils import Constants, ProbeResultKeys

import python_encode.utils

from python_encode.custom_objects import AnimeFileObject

# from python_encode.language.language import VariousString as lp


class HelperFunctions(python_encode.utils.HelperFunctions):
    @staticmethod
    def setup_logger(
            class_name: str = None,
            log_level: str = "INFO",
            log_file: Path = None,
            log_fmt: str = None
    ) -> logging.Logger | None:
        """
        Setup logger

        TODO: Log file writing still fucking doesn't work.... (𓌻‸𓌻) ᴜɢʜ.

        If `class_name` not given, it won't return a logger object.

        Default log format (if `log_fmt` is None): [%(asctime)s] [%(name)s] [%(levelname)s] %(message)s

        This function should only be called once (e.g., called in `if __name__ == __main__`)
        """
        if Constants.LOGGER_SETUP:
            logging.warning("Logger setup ran multiple times.")

        if not isinstance(log_fmt, str):
            # log format for `logging` and `coloredlog`
            log_fmt = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'

        if isinstance(log_file, Path):
            if not log_file.parent.exists():
                raise NotADirectoryError(f"Cannot find log directory: {log_file.parent.__str__()}")
            if log_file.exists() and not log_file.is_file():
                raise IOError(f"Found a non-file object with the same name as log file: {log_file.__str__()}")
            logging.basicConfig(filemode='a', filename=log_file, format=log_fmt)

        logging.captureWarnings(True)

        # replace black text from field 'levelname' with white bold text or it blends into terminal's background
        coloredlogs.DEFAULT_FIELD_STYLES['levelname'] = dict(bold=True)
        coloredlogs.install(
            log_level,
            fmt='[%(name)s] [%(levelname)s] %(asctime)s - %(message)s',
            stream=sys.stdout,
        )
        Constants.LOGGER_SETUP = True
        if isinstance(class_name, str):
            return logging.getLogger(class_name)
        return None