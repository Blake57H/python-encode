import json
import logging
import re
import signal
import subprocess
from pathlib import Path
from typing import Optional, Callable, Dict, List, Union, Set, Tuple

import alive_progress

from python_encode.custom_objects import AnimeFileObject, EncodePresetObject
from python_encode.ui.model_encoder_settings import Defaults
from python_encode.utils_site_package import ProbeResultKeys, HelperFunctions, Constants


class AnimeProcessor:
    logger = logging.getLogger(__name__)
    ffmpeg = 'ffmpeg'
    ffprobe = 'ffprobe'
    brackets = {'(': ')', '[': ']'}
    ignoring_left_brackets = set()
    tag_content_spliter = None

    @staticmethod
    def probe_file(file: Path, ffprobe_path: str = ffprobe) -> dict:
        # eqvalant cmd: ffprobe {file} -show_format -show_streams -show_chapters -print_format json >> probe.json
        probe_result = subprocess.run([
            ffprobe_path,
            file.absolute().__str__(),
            "-show_format",
            "-show_streams",
            "-show_chapters",
            "-print_format", "json"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if probe_result.returncode != 0:
            raise subprocess.SubprocessError(
                str.format('Process "{0}" error: {1}', ffprobe_path, probe_result.stderr.splitlines()[-1].decode()))
        return json.loads(probe_result.stdout)

    @staticmethod
    def process_tag(anime_object: AnimeFileObject, tag_content: str,
                    known_omittable_tags: Optional[Set[str]] = None) -> None:
        """Check tag content and write it to the corresponding anime object property"""

        # known_tag list
        for known_omittable_tag in known_omittable_tags:
            if tag_content.upper() == known_omittable_tag:
                anime_object.omittable_tags.add(tag_content)
                AnimeProcessor.logger.debug(f"known tag: {tag_content}")
                return

        # crc32
        if len(tag_content) == 8:
            potential_crc = re.match(r'([0-9|a-f]*)', tag_content, re.IGNORECASE)
            if potential_crc is not None and potential_crc.group() == tag_content:
                anime_object.crc32 = (anime_object.crc32[0], tag_content)
                AnimeProcessor.logger.debug(f"crc32: {tag_content}")
                return

        # resolution
        for exp in [r'(\d+)[p|i|P|I]', r'\d+[x|X](\d+)']:
            if re.search(exp, tag_content) is not None:
                anime_object.omittable_tags.add(tag_content)
                AnimeProcessor.logger.debug(f"resolution: {tag_content}")
                return

        # a tag that is not known or should not omit
        anime_object.non_omittable_tags.add(tag_content)

    @staticmethod
    def read_anime_file_probe_result(anime: AnimeFileObject, probe_result: dict) -> None:
        """
        Read ffprobe result and write available indo to AnimeFileObject which includes:
            - video length (seconds and frame count)
            - resolution
            - all streams' index and type except attachments

        :param anime: AnimeFileObject
        :param probe_result: ffprobe json output
        :return: None
        """
        if not isinstance(anime.file, Path) or not anime.file.exists() or anime.file.is_dir():
            raise RuntimeError('File "%s" is invalid.', anime.file)

        streams: list[dict] = probe_result.get("streams", list())
        st = ProbeResultKeys.StreamTypes

        # chapters: list[dict] = probe_result.get("chapters", list())
        for chapter in probe_result.get("chapters", list()):
            anime.chapters.append((
                chapter.get('start_time', None),
                chapter.get('end_time', None),
                chapter.get('tags', dict()).get('title', None)
            ))

        # try to get video length (duration)
        duration_str = probe_result.get("format", dict()).get("duration", None)
        if duration_str is not None:
            anime.video_length_seconds = float(duration_str)

        # noting down all stream types (except attachments)
        for idx, stream in enumerate(streams):
            stream_type = stream["codec_type"]
            if stream_type == st.VIDEO:
                anime.video_stream_indexes.add(idx)
                continue
            if stream_type == st.AUDIO:
                anime.audio_stream_indexes.add(idx)
                continue
            if stream_type == st.SUBTITLE:
                anime.subtitle_stream_indexes.add(idx)
                continue
            if stream_type == st.ATTACHMENT:
                anime.attachment_stream_indexes.add(idx)
                continue

        # try get resolution, frame count and video length from first video stream
        if not HelperFunctions.is_subject_empty(anime.video_stream_indexes):
            first_video_stream = streams[list(anime.video_stream_indexes)[0]]
            # resolution
            anime.video_resolution = (
                first_video_stream.get('width', None).__str__(),
                first_video_stream.get('height', None).__str__()
            )
            # show warning if resolution is not found
            if None in anime.video_resolution:
                AnimeProcessor.logger.warning('Unable to read video resolution with ffprobe: %s', anime.file)
            # frame count / duration (if previous attempt failed)
            stream_tags: dict = first_video_stream.get('tags')
            for key in stream_tags.keys():
                if 'NUMBER_OF_FRAMES' in key:
                    anime.video_frame_count = int(stream_tags.get(key))
                if anime.video_length_seconds is None and 'DURATION' in key:
                    hour, minute, second = stream_tags.get(key).split(':')
                    anime.video_length_seconds = float(hour) * 3600 + float(minute) * 60 + float(second)
            # show warning if video length is not found
            if anime.video_length_seconds is None:
                AnimeProcessor.logger.warning('Unable to read video length with ffprobe: %s', anime.file)

    @staticmethod
    def read_anime_file_crc32(anime: AnimeFileObject, on_bytes_read: Optional[Callable[[int], None]] = ...,
                              abort_signal: Optional[Callable[[None], bool]] = ..., ) -> None:
        """
        Use zlib to calculate video file's crc32.
        And use alive_progress without "with/as" context: https://github.com/rsalmei/alive-progress/issues/3
        :param anime:
        :param progress_emit:
        :param abort_signal:
        :return:
        """
        progress_emit: Callable[[int], None]
        if not isinstance(anime.file, Path) or not anime.file.exists() or anime.file.is_dir():
            raise RuntimeError('File "%s" is invalid.', anime.file)
        bar = alive_progress.alive_bar(anime.file.stat().st_size, title="Calculating CRC32", theme='classic', scale=2)
        if not isinstance(on_bytes_read, Callable):
            progress_emit = bar.__enter__()
        else:
            progress_emit = on_bytes_read
        anime.crc32 = (
            HelperFunctions.get_file_crc32(anime.file, on_file_chunk_read=progress_emit, abort_signal=abort_signal),
            None)
        if not isinstance(on_bytes_read, Callable):
            bar.__exit__(None, None, None)

    # @staticmethod
    # def read_anime_file_crc32_str(anime: Path, on_bytes_read: Optional[Callable[[int], None]] = ...,
    #                               abort_signal: Optional[Callable[[None], bool]] = ..., ) -> str:
    #     progress_emit = lambda: ...
    #     if not isinstance(anime, Path) or not anime.exists() or anime.is_dir():
    #         raise RuntimeError('File "%s" is invalid.', anime)
    #     bar = alive_progress.alive_bar(anime.stat().st_size, title="Calculating CRC32", theme='classic', unit=2)
    #     if not isinstance(on_bytes_read, Callable):
    #         progress_emit = bar.__enter__()
    #     else:
    #         progress_emit = on_bytes_read
    #     crc32 = Utils.get_episode_crc32(anime, on_file_chunk_read=progress_emit, abort_signal=abort_signal)
    #     if not isinstance(on_bytes_read, Callable):
    #         bar.__exit__()
    #     return crc32

    @staticmethod
    def read_anime_file_name(anime: AnimeFileObject,
                             brackets: Dict[str, str] = ...,
                             ignoring_left_brackets: Set[str] = ...,
                             multiple_content_spliter: Optional[str] = None,
                             ) -> None:
        """Parse filename and extract info like episode name and release group"""
        if not isinstance(anime.file, Path) or not anime.file.exists() or anime.file.is_dir():
            raise RuntimeError('File "%s" is invalid.', anime.file)
        if not isinstance(brackets, Dict):
            brackets = AnimeProcessor.brackets
        if isinstance(ignoring_left_brackets, List):
            for left_bracket in ignoring_left_brackets:
                brackets.pop(left_bracket, None)

        anime.episode_name = ""  # initialize episode name
        title = anime.file.stem
        left_brackets = tuple(brackets.keys())

        # I can assume filename length > 0 right?
        right_bracket = brackets.get(title[0], None)
        # Finding release group
        if right_bracket is not None:
            right_bracket_position = title.find(right_bracket)
            anime.release_group = title[1:right_bracket_position]
            title = title[right_bracket_position + 1:].strip()
        else:
            anime.release_group = None
        title = title.replace('_', ' ')

        while len(title) > 0:
            # treat text wrapped in brackets tags
            if title.startswith(left_brackets):
                right_bracket_position = title.find(brackets.get(title[0]))
                if right_bracket_position == -1:
                    right_bracket_position = len(title)
                tag_content = title[1:right_bracket_position]
                if multiple_content_spliter is not None:
                    for tag_content_part in tag_content.split(multiple_content_spliter):
                        AnimeProcessor.process_tag(anime, tag_content_part,
                                                   known_omittable_tags=Constants.KNOWN_OMITTABLE_TAGS)
                else:
                    AnimeProcessor.process_tag(anime_object=anime, tag_content=tag_content,
                                               known_omittable_tags=Constants.KNOWN_OMITTABLE_TAGS)
                title = title[right_bracket_position + 1:].strip()  # no index out of range error
                AnimeProcessor.logger.debug(str.format("title='{}', tag_content='{}'", title, tag_content))
                continue

            # not starting with brackets, treating the following texts as text
            left_pointer = 0
            while left_pointer < len(title) and title[left_pointer] not in left_brackets:
                left_pointer += 1  # move pointer until reaching
            if not HelperFunctions.is_string_empty(anime.episode_name):
                anime.episode_name += " "
            anime.episode_name += title[:left_pointer].strip()
            title = title[left_pointer:]
            AnimeProcessor.logger.debug(str.format("title='{}', episode_name='{}'", title, anime.episode_name))
            continue

    @staticmethod
    def read_anime_file(file: Path,
                        ffprobe: str = ffprobe,
                        on_bytes_read_callback: Optional[Callable[[int], None]] = ...,
                        abort_signal: Optional[Callable[[], bool]] = ...,
                        brackets: Dict[str, str] = ...,
                        ignoring_left_brackets: Set[str] = ...,
                        skip_crc32: bool = False,
                        tag_content_spliter: Optional[str] = None) -> Optional[AnimeFileObject]:
        """
        Read information from a video file using ffprobe.
        This function calls all other "read_anime_file_XXX" function


        :param file:
        :param ffprobe:
        :param existing_anime_file_object:
        :param on_bytes_read_callback: A callback function for progress report, has one integer argument and its range is [0, 100]
        :param abort_signal: A callable that returns a boolean. If returned boolean is True, then thread should terminate/abort.
        :param brackets: Dictionary containing bracket pairs for tag recognition. Defaults are () and [].
        :param ignoring_left_brackets: Ignore a specific set of bracket presented in "brackets" argument.
        :param tag_content_spliter:  Pass a spliter to deal with some releases that put multiple tags in one brackets.
        :param skip_crc32:
        :return Return `None` if parse failed.
        """

        if not isinstance(file, Path) or not file.exists() or file.is_dir():
            AnimeProcessor.logger.error('File "%s" is invalid.', file)
            raise FileNotFoundError(f'File "{file.__str__()}" is invalid.')
        if not isinstance(abort_signal, Callable):
            AnimeProcessor.logger.debug(f"type(abort_signal)={type(abort_signal)}!=Callable")
            abort_signal = None
        if not isinstance(brackets, Dict):
            brackets = AnimeProcessor.brackets
        if isinstance(ignoring_left_brackets, Set):
            for left_bracket in ignoring_left_brackets:
                brackets.pop(left_bracket, None)
        if tag_content_spliter is not None:
            tag_content_spliter = tag_content_spliter.replace('_', " ")

        # begin with creating an object
        try:
            anime = AnimeFileObject()
            anime.file = file
            anime.file_name = file.name

            probe_result = AnimeProcessor.probe_file(file=file, ffprobe_path=ffprobe)
            AnimeProcessor.read_anime_file_probe_result(anime, probe_result)

            if not skip_crc32:
                AnimeProcessor.read_anime_file_crc32(anime, on_bytes_read_callback, abort_signal)

            AnimeProcessor.read_anime_file_name(anime=anime, brackets=brackets,
                                                multiple_content_spliter=tag_content_spliter)
            return anime
        except subprocess.SubprocessError:
            return None

    @staticmethod
    def compile_encode_param(anime_file: AnimeFileObject,
                             output_file_path: Path,
                             encode_preset_object: Optional[EncodePresetObject],
                             select_video_streams: Set[Union[int, str]] = ...,
                             select_audio_streams: Set[Union[int, str]] = ...,
                             select_subtitle_streams: Set[Union[int, str]] = ...,
                             select_attachment_streams: Set[Union[int, str]] = ...,
                             ffmpeg: str = ffmpeg,
                             ignore_warning: bool = False
                             ) -> List[str]:
        """
        
        :param anime_file: Source file's AnimeFileObject
        :param output_file_path: Path object pointing to the encoded file
        :param encode_preset_object: An EncodePresetObject for setting encode parameters
        :param select_video_streams: Specify video stream(s) to encode
        :param select_audio_streams: Specify audio stream(s) to encode
        :param select_subtitle_streams: Specify subtitle stream(s) to encode
        :param select_attachment_streams: Specify attachment stream(s) to encode
        :param ffmpeg: Specify ffmpeg executable
        :param ignore_warning:
        :return:
        """
        command_args = [ffmpeg]
        if not isinstance(encode_preset_object, EncodePresetObject):
            encode_preset_object = EncodePresetObject()
        AnimeProcessor.logger.debug(encode_preset_object)
        # naming_file = encode_preset_dir / "naming.txt"
        st = ProbeResultKeys.StreamTypes

        stream_specific_option: Dict = encode_preset_object.stream_params
        extra_options: list[str] = encode_preset_object.extra_options

        if not ignore_warning and len(stream_specific_option) == 0:
            AnimeProcessor.logger.debug(stream_specific_option)
            AnimeProcessor.logger.warning("Encode preset not found, using ffmpeg default settings.")

        # naming = naming_file.read_text() if naming_file.is_file() else None

        input_option = stream_specific_option.get('input', dict())
        for key, val in input_option.items():
            command_args.extend([f"-{key}", val])

        # fixme: the followings will cause problems if not using mkv container
        # fixme: If all stream is selected, command arg should be shortened. For now iterating all streams works.

        command_args.extend(["-i", anime_file.file.absolute().__str__()])
        # selected_streams = set.union()

        stream_counter = 0
        if select_video_streams is Ellipsis:
            select_video_streams = anime_file.video_stream_indexes
        for stream_idx in select_video_streams:
            command_args.extend(['-map', f'0:{stream_idx}'])
            for key, val in stream_specific_option.get(st.VIDEO, dict()).items():
                if val is None:
                    continue
                command_args.extend([f'-{key}:{stream_counter}', val])
            stream_counter += 1

        if select_audio_streams is Ellipsis:
            select_audio_streams = anime_file.audio_stream_indexes
        for stream_idx in select_audio_streams:
            command_args.extend(['-map', f'0:{stream_idx}'])
            for key, val in stream_specific_option.get(st.AUDIO, dict()).items():
                if val is None:
                    continue
                command_args.extend([f'-{key}:{stream_counter}', val])
            stream_counter += 1

        if select_subtitle_streams is Ellipsis:
            select_subtitle_streams = anime_file.subtitle_stream_indexes
        for stream_idx in select_subtitle_streams:
            command_args.extend(['-map', f'0:{stream_idx}'])
            for key, val in stream_specific_option.get(st.SUBTITLE, dict()).items():
                if val is None:
                    continue
                command_args.extend([f'-{key}:{stream_counter}', val])
            stream_counter += 1

        if len(list(anime_file.attachment_stream_indexes)) == 0:
            pass
        elif len(select_attachment_streams.difference(anime_file.attachment_stream_indexes)) > 0:
            for stream_idx in select_attachment_streams:
                command_args.extend(['-map', f'0:{stream_idx}'])
            command_args.extend(['-c:t', 'copy'])
        elif (len(list(anime_file.attachment_stream_indexes)) > 0 and
              stream_specific_option.get('keep_attachments', True)):
            command_args.extend(['-map', '0:t', '-c:t', 'copy'])

        if not stream_specific_option.get('keep_chapters', True):
            command_args.extend(['-map_chapters', '-1'])
        command_args.extend(extra_options)

        command_args.extend([output_file_path.absolute().__str__(), '-y'])
        debug_args = [_ if ' ' not in _ else f'"{_}"' for _ in command_args]
        AnimeProcessor.logger.debug(f"Encode param: {' '.join(debug_args)}")

        return command_args

    @staticmethod
    def calling_subprocess_encode(
            anime_src_info: AnimeFileObject,
            subprocess_args: List[str],
            progress_update_callback_integer: Callable[[int, int], None] = Ellipsis,
            progress_update_callback_string: Callable[[str], None] = Ellipsis,
            abort_signal: Callable[[], bool] = Ellipsis,
            show_ffmpeg_stdout: bool = False,
    ) -> Tuple[Optional[int], str]:
        """
        todo: lambdas used here are hurting future me (why the fuck did I use 2 parameters?)

        :param anime_src_info:
        :param subprocess_args:
        :param progress_update_callback_integer: A function taking two integer arguments. First one is encoded_frame_count, second one is total_frame_count
        :param progress_update_callback_string: FFmpeg's progress stdout will be passed into this function.
        :param abort_signal: A function returns a boolean, which indicates if the process should terminate.
        :param show_ffmpeg_stdout: Print ffmpeg console output (replaces the default progress bar)
        :return: return code, return message
        """
        bar = alive_progress.alive_bar(anime_src_info.video_frame_count, title="Encoding", unit="frames",
                                       theme='classic')
        on_frame_encoded = progress_update_callback_integer
        on_string_progress_returned = progress_update_callback_string
        progress_bar_enabled = not show_ffmpeg_stdout  # for the sake of readability

        get_current_frame_expression = re.compile(r'frame= *(\d+)')

        if not isinstance(progress_update_callback_string, Callable) or show_ffmpeg_stdout:
            on_string_progress_returned = lambda progress_str: ...
        if not isinstance(progress_update_callback_integer, Callable):
            if show_ffmpeg_stdout:
                on_frame_encoded = lambda encoded_frame_count, total_frame_count: ...
            else:
                update_progress = bar.__enter__()
                update_progress(-1)
                on_frame_encoded = lambda encoded_frame_count, total_frame_count: update_progress(
                    encoded_frame_count - update_progress.current)
        proc = None
        last_stdout = list()
        if not isinstance(abort_signal, Callable):
            abort_signal = lambda: False
        try:
            with subprocess.Popen(args=subprocess_args, shell=False, stderr=subprocess.STDOUT, stdout=subprocess.PIPE,
                                  universal_newlines=True) as proc:
                while proc.poll() is None:
                    stdout = proc.stdout.readline()
                    if show_ffmpeg_stdout:
                        print(stdout, end='')
                    stdout = stdout.strip()
                    if stdout != '':
                        last_stdout.append(stdout)
                    frame = get_current_frame_expression.match(stdout)
                    if frame is not None:
                        on_frame_encoded(int(frame.groups()[0]), anime_src_info.video_frame_count)
                        on_string_progress_returned(stdout)
                    if abort_signal():
                        AnimeProcessor.logger.info("Abort signal received. Shutting down ffmpeg...")
                        proc.terminate()
                        return None, "Aborted"
            if not isinstance(progress_update_callback_integer, Callable) and progress_bar_enabled:
                bar.__exit__(None, None, None)
            AnimeProcessor.logger.debug("encode complete")
        except KeyboardInterrupt:
            # I need printing outside alive progress
            if not isinstance(progress_update_callback_integer, Callable) and progress_bar_enabled:
                bar.__exit__(None, None, None)
            AnimeProcessor.logger.info("User pressed Ctrl+C.")
            if isinstance(proc, subprocess.Popen):
                proc.send_signal(signal.SIGTERM)
                AnimeProcessor.logger.info("Shutting down ffmpeg...")
            while proc.poll() is None:
                pass
            return None, "User pressed Ctrl+C."
        except Exception as ex:
            # in case my code went wrong...
            if not isinstance(progress_update_callback_integer, Callable) and progress_bar_enabled:
                bar.__exit__(None, None, None)
            AnimeProcessor.logger.error(f"Application error: {ex.__str__()}")
            if isinstance(proc, subprocess.Popen):
                proc.send_signal(signal.SIGTERM)
                AnimeProcessor.logger.info("Shutting down ffmpeg...")
            return None, f"Application error: {ex.__str__()}"

        if proc is None:
            return None, "Subprocess not created"
        if proc.returncode == 0:
            return proc.returncode, ""
        last_stdout = last_stdout[-10:]
        last_stdout.insert(0, "Last 10 output: ")
        return proc.returncode, "\n".join(last_stdout)

    @staticmethod
    def build_rename_keyword_replacement(
            source_anime_object: AnimeFileObject, encoded_anime_file: Path,
            encoded_anime_object: Optional[AnimeFileObject] = ..., ffprobe: str = ffprobe,
            encode_preset_object: Optional[EncodePresetObject] = None,
            on_byte_read_callback: Optional[Callable[[int], None]] = ...
    ) -> Dict[str, Union[str, int]]:
        assert isinstance(source_anime_object,
                          AnimeFileObject), f"Invalid input source_anime_object: expect {type(AnimeFileObject)}, got {type(source_anime_object)}"

        if not isinstance(encode_preset_object, EncodePresetObject):
            encode_preset_object = EncodePresetObject()
        if not isinstance(encoded_anime_object, AnimeFileObject):
            encoded_anime_object = AnimeFileObject()
        if encoded_anime_object.file is None:
            encoded_anime_object.file = encoded_anime_file
        elif not encoded_anime_object.file.samefile(encoded_anime_file):
            AnimeProcessor.logger.warning(
                f'Input inconsistency: encoded_anime_object({encoded_anime_file}) != encoded_anime_object.file({encoded_anime_object.file}). "encode_anime_object.file" will be used.'
            )

        AnimeProcessor.read_anime_file_probe_result(
            encoded_anime_object, AnimeProcessor.probe_file(encoded_anime_object.file, ffprobe)
        )

        kw_replace_dict = {
            "{release_group}": source_anime_object.release_group,
            "{episode_name}": source_anime_object.episode_name,
            "{resolution_width}": encoded_anime_object.video_resolution[0],
            "{resolution_height}": encoded_anime_object.video_resolution[1],
            "{tags}": encode_preset_object.tag_divider.join(source_anime_object.non_omittable_tags),
        }

        for k, v in kw_replace_dict.items():
            if v is None:
                kw_replace_dict[k] = ""

        if "{crc32}" in encode_preset_object.naming:
            AnimeProcessor.read_anime_file_crc32(encoded_anime_object, on_byte_read_callback)
            kw_replace_dict["{crc32}"] = encoded_anime_object.crc32[0]

        return kw_replace_dict

    @staticmethod
    def rename_encoded_file(naming_template: str, encoded_file: Path, keyword_replacement: dict = None,
                            update_file: bool = True) -> Path:
        """
        Rename encoded file with a naming template. Returns "encoded_file" if naming template is empty.
        :param naming_template:
        :param encoded_file:
        :param keyword_replacement:
        :param update_file:
        :return:
        """
        assert encoded_file.exists() and encoded_file.is_file(), f"file={encoded_file}, exists={encoded_file.exists()}, is_file={encoded_file.is_file()}"
        if keyword_replacement is None:
            keyword_replacement = dict()
        if HelperFunctions.is_subject_empty(naming_template):
            return encoded_file

        filename = naming_template
        for replacement in keyword_replacement.items():
            filename = filename.replace(replacement[0], replacement[1])
        filename += encoded_file.suffix

        # This function returns the updated file path
        if update_file:
            # update the name and return the path pointing to the file
            return encoded_file.rename(encoded_file.parent.joinpath(filename))
        else:
            # Creates a new Path pointing to the non-exist renamed file.
            # No file is actually renamed.
            return encoded_file.parent.joinpath(filename)

    @staticmethod
    def process_anime_encode(
            output_dir: Path,
            source_file_object: AnimeFileObject,
            # output_file_extension: str = Defaults.CONTAINER[0],
            encode_preset: Optional[EncodePresetObject] = ...,
            selected_streams: Optional[Set[int]] = ...,
            ffmpeg_executable: str = ffmpeg,
            ffprobe_executable: str = ffprobe,
            encode_progress_callback: Optional[Callable[[int, int], None]] = ...,  # why am I compliating myself...
            show_ffmpeg_stdout: bool = False,
            abort_signal: Optional[Callable[[], bool]] = ...,
    ) -> Tuple[Optional[Path], bool]:
        """

        :param output_dir:
        :param source_file_object:
        # :param output_file_extension:
        :param encode_preset:
        :param selected_streams:
        :param ffmpeg_executable:
        :param ffprobe_executable:
        :param encode_progress_callback:
        :param show_ffmpeg_stdout:
        :param abort_signal:
        :return: Path object of encoded file if encode successful, and an is_aborted mark
        """
        if not isinstance(selected_streams, Set):
            selected_streams = source_file_object.get_all_stream_indexes()
        if not isinstance(output_dir, Path) or not Path(source_file_object.file.root).exists():
            raise NotADirectoryError('Output directory "%s" is invalid.', output_dir)
        output_file_extension: Optional[str] = encode_preset.stream_params.get("container", None)
        if not isinstance(output_file_extension, str):
            output_file_extension = Defaults.CONTAINER[0]
        # fixme: Should I move all miscellaneous options like naming and container and tag divider into a Json file?
        num = 1
        output_file = output_dir / f"{source_file_object.file.stem}_{num}{output_file_extension}"
        while output_file.exists():
            num += 1
            output_file = output_dir / f"{source_file_object.file.stem}_{num}{output_file_extension}"

        encode_command_args = AnimeProcessor.compile_encode_param(
            anime_file=source_file_object, output_file_path=output_file, encode_preset_object=encode_preset,
            select_video_streams=source_file_object.video_stream_indexes.intersection(selected_streams),
            select_audio_streams=source_file_object.audio_stream_indexes.intersection(selected_streams),
            select_subtitle_streams=source_file_object.subtitle_stream_indexes.intersection(selected_streams),
            select_attachment_streams=source_file_object.attachment_stream_indexes.intersection(selected_streams),
            ffmpeg=ffmpeg_executable
        )

        returned_code, error_text = AnimeProcessor.calling_subprocess_encode(
            anime_src_info=source_file_object, subprocess_args=encode_command_args,
            progress_update_callback_integer=encode_progress_callback, abort_signal=abort_signal,
            show_ffmpeg_stdout=show_ffmpeg_stdout
        )
        if returned_code is None:
            AnimeProcessor.logger.info(f"Encode canceled: {error_text}")
            return None, True
        if returned_code != 0:
            AnimeProcessor.logger.error(f"Encode process returned non-zero exit code ({returned_code}): {error_text}")
            return None, False

        encoded_file_object = AnimeFileObject()
        naming_kw_replacement = AnimeProcessor.build_rename_keyword_replacement(
            source_anime_object=source_file_object, encoded_anime_file=output_file,
            encoded_anime_object=encoded_file_object, ffprobe=ffprobe_executable, encode_preset_object=encode_preset,
        )

        output_file = AnimeProcessor.rename_encoded_file(
            naming_template=encode_preset.naming, encoded_file=output_file, keyword_replacement=naming_kw_replacement
        )
        return output_file, False

    @staticmethod
    def do_encode_task(
            source_file: Path,
            output_dir: Path,
            encode_preset: Optional[EncodePresetObject] = ...,
            selected_streams: Optional[Set[int]] = ...,
            ffmpeg_executable: str = ffmpeg,
            ffprobe_executable: str = ffprobe,
            file_read_progress_callback: Optional[Callable[[int], None]] = ...,
            encode_progress_callback: Optional[Callable[[int, int], None]] = ...,  # why am I compliating myself...
            show_ffmpeg_stdout: bool = False,
            abort_signal: Optional[Callable[[], bool]] = ...,
            brackets: Dict[str, str] = ...,
            ignoring_left_brackets: Set[str] = ...,
            tag_content_spliter: Optional[str] = None
    ) -> Tuple[Optional[Path], bool]:
        if not isinstance(source_file, Path) or not source_file.is_file():
            raise FileNotFoundError('File "%s" is invalid.', source_file)

        source_file_object = AnimeProcessor.read_anime_file(
            file=source_file, ffprobe=ffprobe_executable, on_bytes_read_callback=file_read_progress_callback,
            abort_signal=abort_signal, brackets=brackets, ignoring_left_brackets=ignoring_left_brackets,
            tag_content_spliter=tag_content_spliter
        )

        encoded_file, is_aborted = AnimeProcessor.process_anime_encode(
            output_dir, source_file_object, encode_preset, selected_streams, ffmpeg_executable,
            ffprobe_executable, encode_progress_callback, show_ffmpeg_stdout, abort_signal
        )

        return encoded_file, is_aborted
