from __future__ import annotations
import logging
from pathlib import Path
from threading import Thread

import time
from datetime import datetime, timedelta
from typing import Callable, Any

from custom_objects import AnimeObject
from utils_deprecating import anime_to_anime_object


class SleepModule:
    """
    control how program sleeps?
    """
    __slots__ = 'sleep_sec', 'work_hour_start', 'work_hour_end'

    def __init__(self, sleep: int = 3600, start_hour: int | None = None, end_hour: int | None = None):
        """
        1. 'sleep' sets a certain seconds to sleep;
        2. start_hour and end_hour sets to encode between start_hour to end_hour every day.
        if end_hour is equal or smaller than start_hour, then it becomes
        "encode between start_hour to end_hour the next day"

        Parameters
        ----------
        sleep: specify seconds to sleep when calling sleep()
        start_hour:
        end_hour:
        """
        if isinstance(sleep, int):
            self.sleep_sec: int = sleep  # sleep for x seconds, default 3600
        else:
            ValueError(f"parameter 'pause' expect {type(int)}, but got {type(sleep)}")

        if start_hour is None:
            pass
        elif not isinstance(start_hour, int):
            TypeError(f"parameter 'start_hour' expect {type(int)} or {type(None)}, but got {type(start_hour)}")
        elif start_hour > 24 or start_hour < 0:
            ValueError("value of parameter 'start_hour' be between 0 and 24 ")
        self.work_hour_start: int | None = start_hour

        if end_hour is None:
            pass
        elif not isinstance(end_hour, int) and end_hour is not None:
            ValueError(f"parameter 'end_hour' expect {type(int)} or {type(None)}, but got {type(end_hour)}")
        elif end_hour > 24 or end_hour < 0:
            ValueError("value of parameter 'end_hour' be in 0~24 ")
        # elif start_hour >= end_hour:
        #     end_hour += 24
        self.work_hour_end: int | None = end_hour

    def sleep(self, time_override: float = None):
        """
        pause program for 'time_override' seconds, default 1 hour
        """
        time.sleep(self.pause if time_override is None else time_override)

    def pause(self):
        """
        immediately pause program until it reaches the next encode period (time between start_hour and end_hour)
        """
        time.sleep(self.get_total_seconds_to_pause())

    def get_sleep_seconds(self) -> (int):
        return self.sleep_sec

    def get_total_seconds_to_pause(self) -> (float):
        if self.work_hour_start is None:
            ValueError("start_hour must be set to use this function")
        if self.work_hour_end is None:
            ValueError("end_hour must be set to use this function")
        # writing down all possible conditions because I couldn't simplify it in my brain
        start = timedelta(hours=self.work_hour_start)
        current = timedelta(hours=datetime.now().hour, minutes=datetime.now().minute)
        end = timedelta(hours=self.work_hour_end)
        if self.work_hour_start < self.work_hour_end:
            # my terrible English couldn't describe what it is, so I drew a line
            # [0h-----++++++++++++++++----24h]
            # [ pause |    encode    | pause ]
            # or "encode between  'start' to 'end'"
            if (start - current).total_seconds() > 0:
                # before encode period, sleep until reaches it
                return (start - current).total_seconds()
            if (current - end).total_seconds() > 0:
                # after encode period, sleep until the next period
                return (start + timedelta(days=1) - current).total_seconds()
            # in encode period, no need to pause
            return 0
        else:
            # my terrible English couldn't describe what it is, so I drew a line pt2
            # [0h+++++++-------------+++++24h]
            # [ encode |   pause    | encode ]
            # or "encode between  'start' to 'end' the next day"
            if (current - end).total_seconds() > 0 and (start - current).total_seconds() > 0:
                return (start - current).total_seconds()
            # in encode period, no need to pause
            return 0

    def is_in_encode_period(self) -> (bool):
        if self.work_hour_start is None or self.work_hour_end is None:
            # if work hour isn't specified, then assume encode 24/7
            return True
        return self.get_total_seconds_to_pause() == 0


class AnimeObjectWorker_deprecating(Thread, DeprecationWarning):
    on_progressbar_update: Callable[[int], None] = None
    on_progresstitle_update: Callable[[str, int], None] = None
    on_finished: list[Callable[[], Any]] = []
    on_result_return: Callable[[list[AnimeObject]], None] = None
    input_subject: list[str] = None
    abort_signal: Callable = None
    exit_now_request = False
    result: list[AnimeObject] = list()
    _logger = logging.getLogger(__name__)

    def run(self) -> None:
        self._logger.info("Thread started, loading source videos.")
        self.result = list()
        if not self.input_subject:
            self._logger.debug(f"not input_subject == True, input: {self.input_subject}")
            self._on_finished()
            return
        
        for idx, subject in enumerate(self.input_subject):
            if self.exit_now_request: 
                break
            self.on_progresstitle_update(subject, idx)
            ao = anime_to_anime_object(Path(subject), progress_emit=self.on_progressbar_update, abort_signal=lambda: self.exit_now_request)
            self._logger.debug(f'{idx}, {subject}')
            self.result.append(ao)
        self.on_result_return(self.result)
        self._on_finished()

    def exit_now(self) -> None:
        self.exit_now_request = True

    def _on_finished(self):
        self._logger.info(f"Thread finishing. Got {len(self.result)} input(s).")
        for function in self.on_finished:
            function()


