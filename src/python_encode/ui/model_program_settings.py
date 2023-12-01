import json
import logging
from pathlib import Path
from typing import Optional, Dict, TypeVar

from python_encode.custom_objects import ProgramInfo, EncodePresetObject
from python_encode.ui.model import DictReader, GenericObject

logger = logging.getLogger(__name__)


class ApplicationSettingsRepository:
    ffmpeg = ProgramInfo.new("ffmpeg")
    ffprobe = ProgramInfo.new('ffprobe')

    # fixme: use config file to locate preset directory
    encode_preset_dir = Path("presets")
    encoder_options_file = encode_preset_dir / 'container_and_codecs.json'
    # encode_preset_list = [EncodePresetObject(_) for _ in Path('presets').glob('*') if _.is_dir()]

    preferred_preset: Optional[EncodePresetObject] = None
    preferred_output_dir: GenericObject[Path] = GenericObject()
    current_output_dir: GenericObject[Path] = GenericObject(Path(""))  # future me: why GenericObject class?

    @staticmethod
    def load_from_preference(pref_dict: Dict = ...):
        logger.info("Loading preferences...")
        if not isinstance(pref_dict, Dict):
            pref_file = Path("") / 'preference.json'
            if not pref_file.is_file():
                logger.debug(f"Preference file not found: {pref_file.absolute()}")
                return
            try:
                pref_dict = json.loads(pref_file.read_text())
            except json.JSONDecodeError as ex:
                logger.warning(f"Invalid preference file: {ex}")
                return
            logger.debug(f"Loading settings from pref file {pref_file.absolute()}")
        else:
            logger.debug(f"User provided custom pref_dict: {pref_dict}")

        dr = DictReader(pref_dict)
        dr.set_from_val_read(ApplicationSettingsRepository.ffmpeg.set_executable, 'ffmpeg')
        dr.set_from_val_read(ApplicationSettingsRepository.ffprobe.set_executable, 'ffprobe')
        dr.set_from_val_read(lambda path: ApplicationSettingsRepository.preferred_output_dir.set(Path(path)), 'output_dir')


ApplicationSettingsRepository.load_from_preference()
