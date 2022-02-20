import os
import re
import time
import random
import base64
import shutil
from pathlib import Path
from typing import List, Tuple

"""
While writing a utility....
I still have trouble understanding python regular expression and I thought writing something on my own
is a good idea....
Basically me reading SSA's code and trying to figure out how it works...
"""

def extract_names(title: Path) -> Tuple[str, str]:
    """
    Extract episode title and tags (which includs group name, resolution, crc and others)

    Parameters
    ----------
    title: str
        Episode file name (e.g. [SomeGroup] Some Anime - Episode 1 [CRC code].mkv)
    
    Returns
    -------
    group name: str
    episode title: str
    """

    if title.suffix in [".mp4", ".mkv"]:
        title = title.stem
    else:
        title = title.name
    
    bracket_tags: List[str] = re.findall(r'\[([^\]]*)\]', title)
    parenthesis_tags: List[str] = re.findall(r'\(([^\)*])\)', title)
    
    print(bracket_tags)
    print(parenthesis_tags)


extract_names(Path(r"Y:\torrents\[Erai-raws] Girly Air Force - 01 ~ 12 [1080p][Multiple Subtitle]\[Erai-raws] Girly Air Force - 01 [1080p][Multiple Subtitle].mkv"))
