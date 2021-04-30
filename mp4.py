import os
import logging
import struct
import binascii


class MP4File:
    def __init__(self, fname):
        with open(fname, "rb") as fp:
            fsize = os.path.getsize(fname)
            logging.info('The file size is: %d', fsize)
            FTYP = False
            FileTypeBox(fp, struct.unpack('>I', fp.read(4))[0])


class Box:
    def __init__(self, fp, size = None, boxType = None):
        if size == None:
            self.size = struct.unpack('>I', fp.read(4))[0]
        else:
            self.size = size
        logging.debug('Size of Box: %u', self.size)
        if boxType == None:
            self.type = fp.read(4).decode('utf-8')
        else:
            self.type = boxType
        logging.debug('Type of Box: %s', self.type)
        if self.size == 1:
            self.largesize = struct.unpack('>Q', fp.read(8))[0]
            logging.debug('Size is 1: %d', self.largesize)
        if self.type == 'uuid':
            logging.warning(
                'A special type uuid is found, no idea what to do yet.')
            # self.uuid = binascii.b2a_hex(
            #     fp.read(16)).decode('utf-8', errors="ignore")


class FullBox(Box):
    def __init__(self, fp):
        bytes_read = fp.read(4)
        self.version = struct.unpack('>I', fp.read(1))[0]
        self.flags = struct.unpack('>B', fp.read(3))[0]

class FileTypeBox(Box):
    def __init__(self, fp, size):
        super().__init__(fp, size, 'ftyp')
        # self.major_brand = fp.read(4)
        # unsigned int(32) major_brand;
        # unsigned int(32) minor_version;
        # unsigned int(32) compatible_brands[]