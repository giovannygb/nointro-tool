from argparse import ArgumentParser
from argparse import FileType

import nointro
import rom

parser = ArgumentParser(
    description = "A tool to organize roms no-intro style"
)

parser.add_argument(
    "action",
    nargs = "?",
    const = "status",
    default = "status",
    choices = ["status"]
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

args = parser.parse_args()

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

nointro_roms = load_nointro_roms(args.dat_files)
roms = load_roms(args.rom_folders)

if args.action == "status":
    print("Loaded {0} no-intro rom file(s)".format(len(nointro_roms)))
    print("Loaded {0} rom file(s)".format(len(roms)))
