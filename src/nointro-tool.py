from argparse import ArgumentParser
from argparse import FileType

import nointro
import rom

import shutil
import os

parser = ArgumentParser(
    description = "A tool to organize roms no-intro style"
)

parser.add_argument(
    "action",
    nargs = "?",
    const = "status",
    default = "status",
    choices = [
        "status",
        "missing",
        "mispelled",
        "rename",
        "list"
    ]
)

parser.add_argument(
    "--dat-files",
    "-df",
    nargs = "+",
    type = FileType("r"),
    required = True
)


parser.add_argument(
    "--rom-folders",
    "-rf",
    nargs = "+",
    required = True
)

parser.add_argument(
    "--filters",
    "-f",
    default = [],
    action = "append",
    nargs = "+"
)

args = parser.parse_args()

class RomTags(object):
    def __init__(self, rom):
        self.total = rom.name.count("(")
        self.tags = self.__tag_array__(rom.name)

    def __tag_array__(self, name):
        tags = []
        end = 0
        for i in range(self.total):
            start = name.find("(", end)
            end = name.find(")", end + 1)
            tags.extend(self.__strip_tag__(name[start + 1:end].split(",")))
        return tags

    def __strip_tag__(self, tags):
        return [tag.strip() for tag in tags]

    def __str__(self):
        return self.tags.__str__()

def load_nointro(dat_files):
    nointros = []

    for dat_file in dat_files:
        nointros.append(nointro.load(dat_file))

    return nointros

def load_nointro_roms(dat_files):
    nointro_roms = []

    for nointro in load_nointro(dat_files):
        nointro_roms.extend(nointro.roms())

    return nointro_roms

def load_roms(rom_folders):
    roms = []

    for rom_folder in rom_folders:
        roms.extend(rom.load(rom_folder))

    return roms

def load_md5_dict(roms):
    md5_dict = {}

    for rom in roms:
        md5_dict[rom.md5] = rom

    return md5_dict

nointro_roms = load_nointro_roms(args.dat_files)
roms = load_roms(args.rom_folders)

nointro_rom_md5 = load_md5_dict(nointro_roms)
rom_md5 = load_md5_dict(roms)

if args.action == "status":
    print("Loaded {0} no-intro rom file(s)".format(len(nointro_roms)))
    print("Loaded {0} rom file(s)".format(len(roms)))
    print("Missing {0} roms".format(len(nointro_rom_md5.keys() - rom_md5.keys())))

if args.action == "missing":
    for missing_md5 in nointro_rom_md5.keys() - rom_md5.keys():
        print("Missing {0} rom".format(nointro_rom_md5[missing_md5].name))

if args.action == "mispelled":
    for common_md5 in nointro_rom_md5.keys() & rom_md5.keys():
        nointro_rom = nointro_rom_md5[common_md5]
        rom = rom_md5[common_md5]

        if rom.name != nointro_rom.name:
            print("Rom {0} should be named {1}".format(rom.name, nointro_rom.name))

if args.action == "rename":
    for common_md5 in nointro_rom_md5.keys() & rom_md5.keys():
        nointro_rom = nointro_rom_md5[common_md5]
        rom = rom_md5[common_md5]

        if rom.name != nointro_rom.name:
            with open(rom.path) as file:
                base_path = os.path.dirname(file.name)

            src_path = rom.path
            dst_path = os.path.join(base_path, nointro_rom.name)

            print("Moving {0} to {1}".format(src_path, dst_path))
            shutil.move(src_path, dst_path)

def filter_roms(roms, filterss):
    filtered_roms = []

    for rom in roms:
        if should_filter(RomTags(rom).tags, filterss):
            filtered_roms.append(rom)

    return filtered_roms

def should_filter(tags, filterss):
    ret2 = True
    for filters in filterss:
        ret1 = False
        for filter in filters:
            if filter.startswith("!"):
                ret1 |= not tags.__contains__(filter[1:])
            else:
                ret1 |= tags.__contains__(filter)
        ret2 &= ret1
    return ret2

if args.action == "list":
    for rom in filter_roms(roms, args.filters):
        print(rom.name)
