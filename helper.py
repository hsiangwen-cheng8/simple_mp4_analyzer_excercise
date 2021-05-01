import struct

def ReadUI32(fp):
    return struct.unpack('>I', fp.read(4))[0]

def ReadUI32ToString(fp):
    return fp.read(4).decode("utf-8")

def ReadUI64(fp):
    return struct.unpack('>I', fp.read(8))[0]

def Read32HexAsString(fp):
    return '0x' +fp.read(4).hex()

def Read16HexAsString(fp):
    return '0x' +fp.read(2).hex()

def ReadI16(fp):
    return struct.unpack('>h', fp.read(2))[0]

def ReadI32(fp):
    return struct.unpack('>h', fp.read(4))[0]

def ReadUI16x16(fp):
    f = struct.unpack('>2H', fp.read(4))[0]
    return f