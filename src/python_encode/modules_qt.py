import logging
from pathlib import Path
from threading import Thread
from typing import List, Callable, Optional, Set, Union

from PySide6.QtCore import QThread, Signal, QObject, SignalInstance

from python_encode.anime_processor import AnimeProcessor
from python_encode.custom_objects import AnimeFileObject, EncodePresetObject, ProgramInfo

logger = logging.getLogger(__name__)


class AnimeFileObjectWorkerQT(QThread):
    on_progressbar_update = Signal(int)  # argument range should be [0, 100]
    on_progresstitle_update: Signal = Signal(str, int)  # return filename and index
    on_finishing: Signal = Signal()
    on_result_return = Signal(list)
    input_subjects = []
    abort_signal = Signal()
    should_quit_immediately = False
    result: List[AnimeFileObject] = list()
    bytes_read: int = 0
    ffprobe_path: str = 'ffprobe'
    
    def __init__(self, ffprobe: str = 'ffprobe') -> None:
        super().__init__()
        self.ffprobe_path = ffprobe

    def get_abort_signal(self) -> bool:
        return self.should_quit_immediately

    def on_bytes_read(self, byte_size: int, file_size: int) -> int:
        self.bytes_read += byte_size
        return int(self.bytes_read / file_size * 100)

    def run(self):
        logger.info("QThread started, loading video files.")
        self.result = list()
        if not self.input_subjects:
            logger.debug(f"not input_subject == True, input: {self.input_subjects}")
            # self.on_result_return.emit(self.input_subject)
            self.on_finishing.emit()
            return

        for idx, subject in enumerate(self.input_subjects):
            logger.debug(f"Loading: {subject}")
            if self.should_quit_immediately:
                break
            self.bytes_read = 0
            self.on_progresstitle_update.emit(subject, idx)
            subject_file = Path(subject)
            ao = AnimeProcessor.read_anime_file(
                file=subject_file, ffprobe=self.ffprobe_path,
                on_bytes_read_callback=lambda chunk_size: self.on_progressbar_update.emit(
                    self.on_bytes_read(chunk_size, subject_file.stat().st_size)),
                abort_signal=self.get_abort_signal
            )
            logger.debug(f"Result: {ao}")
            self.result.append(ao)
        self.on_finishing.emit()
        self.on_result_return.emit(self.result)

    def exit_now(self) -> None:
        self.should_quit_immediately = True


class AnimeEncodeWorkerQT(QThread):
    __slots__ = (
        '__encode_file_objects',
        '__output_dir',
        '__encode_preset',
        '__ffmpeg',
        '__ffprobe',

        '__selected_video_streams',  # temporarily removed because I'm not good at designing its processing logic
        '__selected_audio_streams',
        '__selected_subtitle_streams',
        '__selected_attachment_streams',

        '__should_quit_immediately',
        '__is_running'
    )

    __on_encode_task_starting: SignalInstance = Signal(str)
    __on_progressbar_update: SignalInstance = Signal(int)  # argument range should be [0, 100]
    __on_progress_label_update: SignalInstance = Signal(str)
    __on_encode_task_finishing: SignalInstance = Signal()
    __return_encoded_files: SignalInstance = Signal(list)

    def __init__(self
                 , encode_file: Union[AnimeFileObject, List[AnimeFileObject]]
                 , output_dir: Path
                 , ffmpeg: ProgramInfo
                 , ffprobe: ProgramInfo
                 , encode_preset: Optional[Union[Path, EncodePresetObject]] = None
                 , selected_streams: Set = ...):
        """
        Setup encode thread.
        :param encode_file: File to be encoded
        :param output_dir: Where encoded file should be saved.
        :param ffmpeg: ProgramInfo of ffmpeg program
        :param ffprobe: ProgramInfo of ffprobe program
        :param encode_preset: How file should be encoded. Use ffmpeg default if not provided.
        :param selected_streams: Which streams in the file should be encoded. "All" if not specified.
        """
        super().__init__()

        self.__encode_file_objects: List[AnimeFileObject] = list()
        if isinstance(encode_file, AnimeFileObject):
            self.__encode_file_objects.append(encode_file)
        elif isinstance(encode_file, List):
            self.__encode_file_objects.extend(encode_file)
        self.__output_dir = output_dir
        if isinstance(encode_preset, EncodePresetObject):
            self.__encode_preset = encode_preset
        else:
            self.__encode_preset = EncodePresetObject(encode_preset)

        self.__ffmpeg = ffmpeg
        self.__ffprobe = ffprobe

        # fixme: make stream selection available when I have the idea

        self.__should_quit_immediately = False
        self.__is_running = False

    def isRunning(self) -> bool:
        return self.__is_running

    def config_signal(self
                      , on_starting_callbacks: List[Callable[[str], None]]
                      , on_progress_percentage_update_callback: Callable[[int], None]
                      , on_progress_text_update_callback: Callable[[str], None]
                      , on_encode_finished: List[Callable[[], None]]
                      , return_encoded_file: Callable[[Path], None]):
        """
        Setup encode thread.
        :param on_starting_callbacks: This function will be called before encoding a file, and filename is passed into it.
        :param return_encoded_file:
        :param on_progress_percentage_update_callback: A callable object taking one integer as parameter. Param value in [0, 100]
        :param on_progress_text_update_callback:
        :param on_encode_finished: A collection of callables taking no parameter which will be called upon completion.
        """
        for starting_callback in on_starting_callbacks:
            self.__on_encode_task_starting.connect(starting_callback)
        self.__on_progressbar_update.connect(on_progress_percentage_update_callback)
        self.__on_progress_label_update.connect(on_progress_text_update_callback)
        for finish_callback in on_encode_finished:
            self.__on_encode_task_finishing.connect(finish_callback)
        self.__return_encoded_files.connect(return_encoded_file)

    def signal_quit(self):
        self.__should_quit_immediately = True

    def handle_integer_progress_update(self, encoded_frames: int, total_frames: int) -> None:
        """
        Calculates percentage from encoded frame count and total frame count.

        Call progress update callback with an integer value ranged from 0 to 100 indicating percentage.
        """
        self.__on_progressbar_update.emit(int(encoded_frames / total_frames * 100))

    def handle_string_progress_update(self, text: str) -> None:
        self.__on_progress_label_update.emit(text)

    def run(self) -> None:
        self.__is_running = True
        output_list: List[Optional[Path]] = list()
        # encode_file_object = self.__encode_file_objects
        for encode_file_object in self.__encode_file_objects:
            self.__on_encode_task_starting.emit(encode_file_object.file_name)
            if self.__should_quit_immediately:
                output_list.append(None)
                continue

            output_file = self.__output_dir / f"{encode_file_object.file.stem}{self.__encode_preset.container_extension}"
            count = 1
            while output_file.exists():
                output_file = self.__output_dir / f"{encode_file_object.file.stem}_{count}{self.__encode_preset.container_extension}"
                count += 1

            # fixme: Keeping all stream from input file is fine for now.
            encoded_file, is_aborted = AnimeProcessor.process_anime_encode(
                output_dir=self.__output_dir,
                source_file_object=encode_file_object,
                encode_preset=self.__encode_preset,
                selected_streams=...,
                ffmpeg_executable=self.__ffmpeg.executable,
                ffprobe_executable=self.__ffprobe.executable,
                encode_progress_callback=self.handle_integer_progress_update,
                abort_signal=lambda: self.__should_quit_immediately
            )

            if encoded_file is None:
                output_list.append(None)
                continue
            output_list.append(output_file)

        self.__return_encoded_files.emit(output_list)
        self.__on_encode_task_finishing.emit()
        self.__is_running = False
