import nointro
import rom

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

class RomCleanName(object):
    def __init__(self, rom):
        idx = rom.name.find("(")
        self.name = rom.name[:idx - 1]

    def __str__(self):
        return self.name

def load_nointro_roms(dat_files):
    nointro_roms = []

    for nointro in load_nointro(dat_files):
        nointro_roms.extend(nointro.roms())

    return nointro_roms

def load_nointro(dat_files):
    nointros = []

    for dat_file in dat_files:
        nointros.append(nointro.load(dat_file))

    return nointros

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

def unique_filter(roms):
    unique_names = []
    unique_roms = []
    for rom in roms:
        unique_name = RomCleanName(rom).name
        if unique_name not in unique_names:
            unique_names.append(unique_name)
            unique_roms.append(rom)
    return unique_roms
