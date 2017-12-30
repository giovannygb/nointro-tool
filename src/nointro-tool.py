from argparse import ArgumentParser
from argparse import FileType

from nointro import load

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
    "--dat-file",
    "-df",
    type = FileType("r"),
    required = True
)

args = parser.parse_args()

nointro = load(args.dat_file)

if args.action == "status":
    print("Loaded {0} games from dat file {1}".format(
        len(nointro.games),
        nointro.name
    ))
