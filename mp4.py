import os
import logging
import struct
from helper import *
import sys
from datetime import date, datetime, time, timedelta
import pytz


class MP4File:
    def __init__(self, fname):
        with open(fname, "rb") as fp:
            self.fsize = os.path.getsize(fname)
            logging.getLogger('mp4').info('The file size is: %d', self.fsize)
            box_maker = BoxMaker(0)
            self.boxes = {}
            eof = False
            # Assume that ftyp for iso is always at the front.
            # Hence if the first box return is not ftyp, exit()
            found_ftyp = False
            while not eof:
                if len(fp.read(4)) != 4:
                    eof = True
                    break
                else:
                    fp.seek(-4, 1)
                box = box_maker.createBoxFromStream(fp)
                if not found_ftyp:
                    if box.boxType != 'ftyp':
                        logging.getLogger('mp4').error('This MP4 file is not iso standard or a format that is not supported. FTYP box must be the first box')
                        raise Exception(
                            "This MP4 file is not iso standard or a format that is not supported. FTYP box must be the first box")
                    else:
                        found_ftyp = True
                self.boxes[box.boxType] = box
            print('.......High Over View of the Structure.......')
            for box in self.boxes:
                self.boxes[box].print_info()


class BoxMaker:
    def __init__(self, level):
        # Any box that is not in this list will only read the type and size
        # TODO: Need to check for fullbox or box 
        self.supported_box = ['ftyp', 'mdat', 'moov',
                              'mvhd', 'trak', 'tkhd', 'udta', 'tsel']
        self.level = level

    def createBoxFromStream(self, fp):
        starting_fp = fp.tell()
        size = ReadUI32(fp)

        boxType = ReadUI32ToString(fp)

        largesize = None
        # handle special size values
        if size == 1:
            logging.getLogger('mp4').error('size == 1 is not supported... exiting')
            raise Exception(
                            "Box with size == 1 is not supported... exiting")
            # Box is large 64-bit size
            # largesize = ReadUI64(fp)
            # TODO: Need proper implementation
            # logging.getLogger('mp4').debug('Size is 1, largesize is: %d', largesize)
        if boxType == 'uuid':
            # TODO: Need proper implementation
            logging.getLogger('mp4').error('uuid is not supported... exiting')
            raise Exception(
                            "uuid is not supported... exiting")
        return self.chooseBox(fp, size, boxType, starting_fp, self.level, largesize)

    def chooseBox(self, fp, size, boxType, starting_fp, level, largesize=None):
        if boxType in self.supported_box:
            box_class = getattr(sys.modules[__name__], boxType+'Box')
            if box_class:
                logging.getLogger('mp4').info(
                    'Type %s: Known tpye box will be created', boxType)
                return box_class(fp, size, boxType, starting_fp, level, largesize)
        else:
            logging.getLogger('mp4').warning(
                'Type %s with size %d: This box type is not supported. Limited Information Only', boxType, size)
            if size >= 8:
                fp.seek(starting_fp+size)
                logging.getLogger('mp4').debug('The finshed point of the %s is: %d',
                              boxType, starting_fp+size)
                return Box(size, boxType, starting_fp, level)
            return None


class Box:
    def __init__(self, size, boxType, starting_fp, level, largesize=None):
        self.boxType = boxType
        self.size = size
        self.starting_fp = starting_fp
        self.level = level
        logging.getLogger('mp4').debug('Type of Box: %s', boxType)
        logging.getLogger('mp4').debug('Size of Box: %u', size)
        logging.getLogger('mp4').debug('The starting point of the fp is %d', starting_fp)
        self.largesize = largesize
        self.box_info = {}
        self.child_boxes = {}
        if self.largesize == None:
            logging.getLogger('mp4').debug(
                'This is a normal box where largesize is not defined')
        else:
            logging.getLogger('mp4').debug('largesize: %d', largesize)

    def pretty_print(self, message):
        ladder = "|"
        bridge = "..."
        cloud = "   "
        print(cloud*self.level+ladder+bridge*self.level+message)

    def print_info(self):
        self.pretty_print('Name of the box: ' + self.boxType)
        # self.pretty_print('Size of the box: '+ str(self.size))

class FullBox(Box):
    def __init__(self, fp, size, boxType, starting_fp, level, largesize):
        super().__init__(size, boxType, starting_fp, level, largesize)
        bytes_read = ReadUI32(fp)
        self.box_info['version'] = bytes_read // 16777216
        self.box_info['flags'] = "{0:#08x}".format(bytes_read % 16777216)
        logging.getLogger('mp4').debug('version: %s', self.box_info['version'])
        logging.getLogger('mp4').debug('flags: %s', self.box_info['flags'])

    def print_info(self):
        super().print_info()
        # print('version: ', self.box_info['version'])
        # print('flags: ', self.box_info['flags'])

# aligned(8) class FileTypeBox
#  extends Box(‘ftyp’) {
#  unsigned int(32) major_brand;
#  unsigned int(32) minor_version;
#  unsigned int(32) compatible_brands[]; // to end of the box
# }


class ftypBox(Box):
    def __init__(self, fp, size, boxType, starting_fp, level, largesize):
        super().__init__(size, boxType, starting_fp, level, largesize)
        self.box_info['major_brand'] = ReadUI32ToString(fp)
        logging.getLogger('mp4').debug('major_brand: %s', self.box_info['major_brand'])
        self.box_info['minor_version'] = "{0:#010x}".format(ReadUI32(fp))
        logging.getLogger('mp4').debug('minor_version: %s', self.box_info['minor_version'])
        # Prepare to loop
        size -= 16
        self.box_info['compatible_brands'] = []
        while size >= 4:
            self.box_info['compatible_brands'].append(ReadUI32ToString(fp))
            size -= 4

        logging.getLogger('mp4').debug('compatible_brands: %s',
                      self.box_info['compatible_brands'])

    def print_info(self):
        super().print_info()
        # print('Info of the box: ', self.box_info)

# mdat


class mdatBox(Box):
    def __init__(self, fp, size, boxType, starting_fp, level, largesize):
        super().__init__(size, boxType, starting_fp, level, largesize)
        fp.seek(starting_fp+self.size)

    def print_info(self):
        super().print_info()

# aligned(8) class MovieBox extends Box(‘moov’){
# }


class moovBox(Box):
    def __init__(self, fp, size, boxType, starting_fp, level, largesize):
        super().__init__(size, boxType, starting_fp, level, largesize)
        box_maker = BoxMaker(1)
        self.trak_counter = 0
        while size - 8 > 7:
            box = box_maker.createBoxFromStream(fp)
            if box.boxType != 'trak':
                self.child_boxes[box.boxType] = box
            else:
                self.child_boxes[box.boxType+str(self.trak_counter)] = box
                self.trak_counter += 1
            size -= box.size
        fp.seek(starting_fp+self.size)

    def print_info(self):
        super().print_info()
        for child_box in self.child_boxes:
            self.child_boxes[child_box].print_info()

# aligned(8) class MovieHeaderBox extends FullBox(‘mvhd’, version, 0) {
#  if (version==1) {
#  unsigned int(64) creation_time;
#  unsigned int(64) modification_time;
#  unsigned int(32) timescale;
#  unsigned int(64) duration;
#  } else { // version==0
#  unsigned int(32) creation_time;
#  unsigned int(32) modification_time;
#  unsigned int(32) timescale;
#  unsigned int(32) duration;
#  }
#  template int(32) rate = 0x00010000; // typically 1.0
#  template int(16) volume = 0x0100; // typically, full volume
#  const bit(16) reserved = 0;
#  const unsigned int(32)[2] reserved = 0;
#  template int(32)[9] matrix =
#  { 0x00010000,0,0,0,0x00010000,0,0,0,0x40000000 };
#  // Unity matrix
#  bit(32)[6] pre_defined = 0;
#  unsigned int(32) next_track_ID;
# }


class mvhdBox(FullBox):
    def __init__(self, fp, size, boxType, starting_fp, level, largesize):
        super().__init__(fp, size, boxType, starting_fp, level, largesize)
        base_date = datetime(1904, 1, 1, 0, 0, 0, tzinfo=pytz.timezone("UTC"))
        if self.box_info['version'] == 0:
            self.box_info['creation_time'] = base_date + \
                timedelta(seconds=ReadUI32(fp))
            self.box_info['modification_time'] = base_date + \
                timedelta(seconds=ReadUI32(fp))
            self.box_info['timescale'] = ReadUI32(fp)
            self.box_info['duration'] = ReadUI32(fp)
        else:
            self.box_info['creation_time'] = base_date + \
                timedelta(seconds=ReadUI64(fp))
            self.box_info['modification_time'] = base_date + \
                timedelta(seconds=ReadUI64(fp))
            self.box_info['timescale'] = ReadUI32(fp)
            self.box_info['duration'] = ReadUI64(fp)
        self.box_info['rate'] = Read32HexAsString(fp)
        self.box_info['volume'] = Read16HexAsString(fp)
        self.box_info['reserved'] = fp.read(2).hex()
        self.box_info['reserved_array'] = []
        self.box_info['reserved_array'].append(ReadUI32(fp))
        self.box_info['reserved_array'].append(ReadUI32(fp))
        self.box_info['matrix'] = []
        for i in range(9):
            self.box_info['matrix'].append(Read32HexAsString(fp))
        self.box_info['pre_defined'] = []
        for j in range(6):
            self.box_info['pre_defined'].append(Read32HexAsString(fp))
        self.box_info['next_track_ID'] = ReadUI32(fp)
        fp.seek(starting_fp+self.size)
        logging.getLogger('mp4').debug('The finshed point of the mvhd is: %d', starting_fp+size)

    def print_info(self):
        super().print_info()
        # print(self.box_info)

# aligned(8) class TrackBox extends Box(‘trak’) {
# }


class trakBox(Box):
    def __init__(self, fp, size, boxType, starting_fp, level, largesize):
        super().__init__(size, boxType, starting_fp, level, largesize)
        box_maker = BoxMaker(level+1)
        while size - 8 > 7:
            box = box_maker.createBoxFromStream(fp)
            self.child_boxes[box.boxType] = box
            size -= box.size
        fp.seek(starting_fp+self.size)

        logging.getLogger('mp4').debug('The finshed point of the trak is: %d',
                      starting_fp+self.size)

    def print_info(self):
        super().print_info()
        for child_box in self.child_boxes:
            self.child_boxes[child_box].print_info()
# aligned(8) class TrackHeaderBox
#  extends FullBox(‘tkhd’, version, flags){
#  if (version==1) {
#  unsigned int(64) creation_time;
#  unsigned int(64) modification_time;
#  unsigned int(32) track_ID;
#  const unsigned int(32) reserved = 0;
#  unsigned int(64) duration;
#  } else { // version==0
#  unsigned int(32) creation_time;
#  unsigned int(32) modification_time;
#  unsigned int(32) track_ID;
#  const unsigned int(32) reserved = 0;
#  unsigned int(32) duration;
#  }
#  const unsigned int(32)[2] reserved = 0;
#  template int(16) layer = 0;
#  template int(16) alternate_group = 0;
#  template int(16) volume = {if track_is_audio 0x0100 else 0};
#  const unsigned int(16) reserved = 0;
#  template int(32)[9] matrix=
#  { 0x00010000,0,0,0,0x00010000,0,0,0,0x40000000 };
#  // unity matrix
#  unsigned int(32) width;
#  unsigned int(32) height;
# }


class tkhdBox(FullBox):
    def __init__(self, fp, size, boxType, starting_fp, level, largesize):
        super().__init__(fp, size, boxType, starting_fp, level, largesize)
        base_date = datetime(1904, 1, 1, 0, 0, 0, tzinfo=pytz.timezone("UTC"))
        if self.box_info['version'] == 0:
            self.box_info['creation_time'] = base_date + \
                timedelta(seconds=ReadUI32(fp))
            self.box_info['modification_time'] = base_date + \
                timedelta(seconds=ReadUI32(fp))
            self.box_info['track_ID'] = ReadUI32(fp)
            self.box_info['reserved'] = ReadUI32(fp)
            self.box_info['duration'] = ReadUI32(fp)
        else:
            self.box_info['creation_time'] = base_date + \
                timedelta(seconds=ReadUI64(fp))
            self.box_info['modification_time'] = base_date + \
                timedelta(seconds=ReadUI64(fp))
            self.box_info['track_ID'] = ReadUI32(fp)
            self.box_info['reserved'] = ReadUI32(fp)
            self.box_info['duration'] = ReadUI64(fp)
        self.box_info['reserved_array'] = []
        self.box_info['reserved_array'].append(ReadUI32(fp))
        self.box_info['reserved_array'].append(ReadUI32(fp))
        self.box_info['layer'] = ReadI16(fp)
        self.box_info['alternate_group'] = ReadI16(fp)
        self.box_info['volume'] = ReadI16(fp)
        # unsigned int(16) reserved,
        fp.read(2)
        self.box_info['matrix'] = []
        for i in range(9):
            self.box_info['matrix'].append(Read32HexAsString(fp))
        self.box_info['width'] = ReadUI16x16(fp)
        self.box_info['height'] = ReadUI16x16(fp)
        fp.seek(starting_fp+self.size)
        logging.getLogger('mp4').info(self.box_info)
        logging.getLogger('mp4').debug('The finshed point of the mvhd is: %d', starting_fp+size)

    def print_info(self):
        super().print_info()
        # print(self.box_info)

# aligned(8) class UserDataBox extends Box(‘udta’) {
# }


class udtaBox(Box):
    def __init__(self, fp, size, boxType, starting_fp, level, largesize):
        super().__init__(size, boxType, starting_fp, level, largesize)
        box_maker = BoxMaker(level+1)
        while size - 8 > 7:
            box = box_maker.createBoxFromStream(fp)
            self.child_boxes[box.boxType] = box
            size -= box.size
        fp.seek(starting_fp+self.size)
        fp.seek(starting_fp+self.size)
        logging.getLogger('mp4').debug('The finshed point of the %s is: %d',
                      boxType, starting_fp+size)

    def print_info(self):
        super().print_info()
        for child_box in self.child_boxes:
            self.child_boxes[child_box].print_info()
# aligned(8) class TrackSelectionBox
#  extends FullBox(‘tsel’, version = 0, 0) {
#  template int(32) switch_group = 0;
#  unsigned int(32) attribute_list[]; // to end of the box
# }


class tselBox(FullBox):
    def __init__(self, fp, size, boxType, starting_fp, level, largesize):
        super().__init__(fp, size, boxType, starting_fp, level, largesize)
        self.box_info['switch_group'] = ReadI32(fp)
        self.box_info['attribute_list'] = []
        while fp < starting_fp+self.size:
            self.box_info['attribute_list'].append(ReadUI32ToString(fp))
        fp.seek(starting_fp+self.size)
        logging.getLogger('mp4').debug('The finshed point of the %s is: %d',
                      boxType, starting_fp+size)
