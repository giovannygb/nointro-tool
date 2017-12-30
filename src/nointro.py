import xml.etree.ElementTree as ElementTree

def load(dat_file):
    element_tree = ElementTree.parse(dat_file)
    element_root = element_tree.getroot()

    header = element_root.find("header")

    name = header.findtext("name")
    description = header.findtext("description")
    version = header.findtext("version")
    authors = header.findtext("author").split(", ")
    homepage = header.findtext("homepage")
    url = header.findtext("url")

    games = __load_games__(element_root)

    return NoIntro(
        name,
        description,
        version,
        authors,
        homepage,
        url,
        games
    )

class NoIntro(object):
    def __init__(
            self,
            name,
            description,
            version,
            authors,
            homepage,
            url,
            games
        ):
        self.name = name
        self.description = description
        self.version = version
        self.authors = authors
        self.homepage = homepage
        self.url = url
        self.games = games

    def roms(self):
        roms = []

        for game in self.games:
            roms.append(game.rom)

        return roms

class Game(object):
    def __init__(self, name, description, rom):
        self.name = name
        self.description = description
        self.rom = rom

class Rom(object):
    def __init__(self, name, size, crc, md5, sha1):
        self.name = name
        self.size = int(size)
        self.crc = int(crc)
        self.md5 = md5.upper()
        self.sha1 = sha1.upper()

def __load_games__(element_root):
    games = []
    for element_game in element_root.findall("game"):
        games.append(__load_game__(element_game))
    return games

def __load_game__(element_game):
    name = element_game.get("name")
    description = element_game.findtext("description")
    rom = __load_rom__(element_game.find("rom"))

    return Game(
        name,
        description,
        rom
    )

def __load_rom__(element_rom):
    name = element_rom.get("name")
    size = element_rom.get("size")
    crc = element_rom.get("crc")
    md5 = element_rom.get("md5")
    sha1 = element_rom.get("sha1")

    return Rom(
        name,
        size,
        int(crc, 16),
        md5,
        sha1
    )
