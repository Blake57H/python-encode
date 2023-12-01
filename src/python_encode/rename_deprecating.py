# I encoded some episodes using Handbrake and I would like to automate the rename procedure

import argparse
import os
from typing import List
from src.python_encode import utils_deprecating
from pathlib import Path

class Rename:
    def __init__(self, input: Path, naming: str, release_group:str = None, 
                tags:List[str]=[], debug: bool = False) -> (None):
        if not input.exists():
            FileNotFoundError(f"{input} not found")
        self.input = input
        self.naming = "[src={group}] {episode_name} ({resolution}p) [{crc}]" if naming in [None, ''] else naming
        self.release_group = release_group if release_group not in ['', None] else None
        self.tags = tags if tags is not None else []
        self.debug = True if debug is True else False
        if debug:
            print("\n\t".join(["DEBUG:", self.input.__str__(), self.naming.__str__(), self.release_group.__str__()]))
            print(f"naming in None: {naming in [None, '']}")

    __slots__ = "input", "naming", "debug", "release_group", "tags"

    def rename(self):
        # assuming 'input' is either file or folder
        input_files = [_ for _ in self.input.glob('*')] if self.input.is_dir() else [self.input]
        if self.debug:
            print(f"DEBUG: {self.input.is_dir()}, {self.input.exists()}, {self.input}")
            print(f"DEBUG: Files:\n\t"+"\n\t".join([_.__str__() for _ in input_files]))
        for input_file in input_files:
            if input_file.is_dir():
                # ignore folder grabbed by `glob` when `input` is a folder
                continue
            # from here input_file is assumed a video file
            extracted_tags = utils_deprecating.extract_names(input_file)
            # in case handbrake or another program carried over incorrect resolution in file name
            extracted_tags.resolution = None
            if self.release_group is not None:
                extracted_tags.release_group = self.release_group
            if len(self.tags) > 0:
                extracted_tags.other_tags = self.tags
            if self.debug:
                print(extracted_tags.__str__()+"\n")
            orig_name = input_file.name
            updated_name = utils_deprecating.update_filename(
                episode_info=extracted_tags, 
                episode_file=input_file, 
                naming_rule=self.naming, 
                update_file=not self.debug
                ).name
            print(f"{orig_name}\n\t--> {updated_name}")

args = argparse.ArgumentParser()
args.add_argument('-i', '--input', dest='input', type=str,
                  nargs=1, required=False, help='Path to an episode or path to a directory of episodes to encode')
args.add_argument('--ffprobe', dest='ffprobe', nargs=1, type=str,
                  required=False, help='Specify ffprobe executable location')
args.add_argument('--naming', dest='naming', nargs=1, type=str,
                  required=False, help='Output naming rule')
args.add_argument('--group', dest="group", nargs=1, type=str,
                  required=False, help='Set release group')                  
args.add_argument('--tags', dest="tags", nargs='+', type=str,
                  required=False, help='Customized your tags')                  
args.add_argument('--debug', dest="debug", action="store_true",
                  required=False, help='Display debug info')
# args.print_help()
args1 = args.parse_args()

if __name__ == "__main__":
    # print_msg(args1.delete_encoded)

    if args1.input is not None:
        input_file = Path(args1.input[0])
    else:
        raise Exception("must specify an input (-i|--input [file|folder])")
    
    # current_path = os.getcwd()
    expected_current_path = Path(__file__).parent.absolute().__str__()
    os.chdir(expected_current_path)

    ffprobe_path = None if args1.ffprobe is None else args1.ffprobe[0]
    naming = None if args1.naming is None else args1.naming[0]
    release_group = None if args1.group is None else args1.group[0]
    tags = [] if args1.tags is None else args1.tags

    # print_msg(args1._get_kwargs())
    Rename(input=input_file, naming=naming, release_group=release_group, tags=tags, debug=args1.debug).rename()
    # d:/Download/Dtaa/Coding/python-encode/venv310/Scripts/python.exe d:/Download/Dtaa/Coding/python-encode/rename.py -i E:\torrent\encode\rename --group kmplx --tags "Dual Audio" --naming "[src={group}] In Another World With My Smartphone - {episode_name} ({resolution}p) {tags} [{crc}]" --debug
    # python rename.py -i "Y:\torrents\_encode\encoded\[jibaketa]Spy x Family - 01 (BD 1920x1080 x264 AACx2 SRT MUSE CHT).mkv"
    # "C:\Users\tingt\CodingNShares\Coding\python-encode\rename.py" -i "{destination}"
    input("Press ENTER to continue...")