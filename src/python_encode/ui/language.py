from PySide6.QtCore import QCoreApplication


class VariousString:
    # ctx = "VariousString"
    # ctt = "ctt"
    # TEST = QCoreApplication.translate("VariousString", "test")
    # TEST1 = QCoreApplication.translate("VariousString", "TEST1")
    # TEST2 = QCoreApplication.translate("VariousString", ctt)
    ERROR = QCoreApplication.translate("VariousString", "Error", None)
    READY = QCoreApplication.translate("VariousString", 'Ready', None)
    INFO = QCoreApplication.translate("VariousString", 'Info', None)
    EMPTY = ''
    FFMPEG = 'ffmpeg'
    FFPROBE = 'ffprobe'

    """Dialogs"""
    FORM_TITLE_CANCEL_TASK = 'Cancel task'
    FORM_TEXT_CANCEL_TASK = 'Task is in progress! Are you sure you want to quit?'
    LABEL_READING_FILE = QCoreApplication.translate("VariousString", "Opening", None)
    TITLE_FFPROBE_READ_FAIL = 'Cannot open file(s)'
    HINT_FFPROBE_READ_FAIL = "The following file(s) cannot be opened:"

    # exception messages
    MSG_SUBPROCESS_ERROR = QCoreApplication.translate("VariousString", 'Process "{0}" error: {1}')


class MainWindowString(VariousString):
    DEBUG_LONG_TEXT = 'Open a file to continue... / LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG / [group] Title - 01 [CRC32]'

    MSG_INFO_NO_INPUT = QCoreApplication.translate('MainWindowString', 'No file to encode.')
    HINT_ENCODING_FILE = QCoreApplication.translate("MainWindowString", "Encoding {}")
    HINT_ENCODE_COMPLETED = QCoreApplication.translate("MainWindowString", 'Encode Completed')
    OPEN_SOURCE = QCoreApplication.translate("MainWindowString", 'Open Source')
    HINT_OPEN_SOURCE = QCoreApplication.translate("MainWindowString", 'Open a file to continue...')
    HINT_MULTIPLE_INPUTS = QCoreApplication.translate("MainWindowString", 'and {} more')

    BUTTON_START_ENCODE = QCoreApplication.translate("MainWindowString", "Start Encode")
    BUTTON_STOP_ENCODE = QCoreApplication.translate("MainWindowString", "Stop Encode")


class SourceInfoWidgetString(VariousString):
    LABEL_STREAM_DESCRIPTION = QCoreApplication.translate("VariousString", "{0} audio tracks, {1} subtitle tracks, {2} attachments")
    LABEL_CRC_FROM_FILE_TITLE = QCoreApplication.translate("VariousString", "File")
    LABEL_CRC_FROM_FILENAME_TITLE = QCoreApplication.translate("VariousString", "Filename")
    LABEL_CRC_MATCH = "Match"
    LABEL_CRC_NOT_PRESENT = "Not Present"
    LABEL_CRC_NOT_MATCH = "Not Match"
    LABEL_VIDEO_LENGTH_SECONDS = "{} second(s)"
    LABEL_VIDEO_LENGTH_FRAMES = "{} frame(s)"


class AppSettingsWidgetString(VariousString):
    """app settings widget/tab"""
    # template: QCoreApplication.translate('AppSettingsWidgetString', )
    # MESSAGE_FF_VER_UNRECOGNIZABLE = "ERROR {1} - Unrezognizab"
    TITLE_SELECT_OUTPUT_DIR = QCoreApplication.translate("AppSettingsWidgetString", 'Select output directory')
    LABEL_FF_PATH_NOT_FOUND = 'ERROR - Cannot open file "{0}"'
    LABEL_FF_VERSION_ERROR = 'ERROR {1} - Unable to get version from "{0}" - {2}'
    LABEL_FF_VERSION_DISPLAY = 'OK - Version "{0}" from "{1}"'
    MESSAGE_BOX_FF_FOUND = QCoreApplication.translate('AppSettingsWidgetString', '{0} found')  # 'ffmpeg' or 'ffprobe'
    MESSAGE_BOX_FF_NOT_FOUND = QCoreApplication.translate('AppSettingsWidgetString',
                                                          '{0} not found')  # 'ffmpeg' or 'ffprobe'
    MESSAGE_BOX_INVALID_DIR = QCoreApplication.translate('AppSettingsWidgetString', 'Invalid directory "{0}"')
    TITLE_OPEN_FF = QCoreApplication.translate('AppSettingsWidgetString', "Set {} executable")


class EncoderSettingsString(VariousString):
    """encoder settings widget/tab"""
    MSG_USE_DEFAULT_PRESET = QCoreApplication.translate('EncoderSettingsString',
                                                        'Error while selecting preset. Using default preset instead.')
    DEFAULT_PRESET_NAME = QCoreApplication.translate('EncoderSettingsString', 'No Preset (use ffmpeg default)')
    MSG_PRESET_NOT_FOUND = QCoreApplication.translate('EncoderSettingsString', 'Preset {} not found')
