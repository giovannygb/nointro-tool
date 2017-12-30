import glob
import os
import zlib
import hashlib

def load(path):
    filePaths = glob.glob(path + "/**")
    roms = []

    for filePath in filePaths:
        if os.path.isfile(filePath):
            roms.append(Rom(filePath))
    return roms

class Rom(object):
    def __init__(self, path):
        self.path = path
        self.size = int(os.stat(path).st_size)
        self.md5 = __load_md5__(path).upper()
        self.sha1 = __load_sha1__(path).upper()
        with open(path, "rb") as file:
            self.name = os.path.basename(file.name)
            self.crc = int(zlib.crc32(file.read()))

def __load_md5__(path):
    return __load_hash__(path, hashlib.md5())

def __load_hash__(path, hash):
    with open(path, "rb") as file:
        hash.update(file.read())

    return hash.hexdigest()

def __load_sha1__(path):
    return __load_hash__(path, hashlib.sha1())
