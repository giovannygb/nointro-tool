from argparse import ArgumentParser
from argparse import FileType

import nointro
import rom
import tools

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
        "misspelled",
        "rename",
        "list",
        "copy",
        "mishash"
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
    "--target-dir",
    "-td"
)

parser.add_argument(
    "--filters",
    "-f",
    default = [],
    action = "append",
    nargs = "+"
)

parser.add_argument(
    "--unique",
    action = "store_true"
)

args = parser.parse_args()

nointro_roms = tools.load_nointro_roms(args.dat_files)
roms = tools.load_roms(args.rom_folders)

nointro_roms = tools.filter_roms(nointro_roms, args.filters)

if (args.unique):
    nointro_roms = tools.unique_filter(nointro_roms)

roms = tools.filter_roms(roms, args.filters)

if (args.unique):
    roms = tools.unique_filter(roms)

nointro_rom_md5 = tools.load_md5_dict(nointro_roms)
rom_md5 = tools.load_md5_dict(roms)

if args.action == "status":
    print("Loaded {0} no-intro rom file(s)".format(len(nointro_roms)))
    print("Loaded {0} rom file(s)".format(len(roms)))
    print("Missing {0} roms".format(len(nointro_rom_md5.keys() - rom_md5.keys())))

if args.action == "missing":
    for missing_md5 in nointro_rom_md5.keys() - rom_md5.keys():
        print("Missing {0} rom".format(nointro_rom_md5[missing_md5].name))

if args.action == "misspelled":
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

if args.action == "list":
    for rom in roms:
        print(rom.name)

if args.action == "copy":
    if (args.target_dir != None):
        for rom in roms:
            with open(rom.path) as file:
                base_path = os.path.dirname(file.name)

            src_path = rom.path
            dst_path = os.path.join(args.target_dir, rom.name)
            shutil.copy(src_path, dst_path)

if args.action == "mishash":
    for mishashed_md5 in rom_md5.keys() - nointro_rom_md5.keys():
        rom = rom_md5[mishashed_md5]
        print("Rom {0} should be deleted".format(rom.name))
