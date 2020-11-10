import struct

# Reading Functions
def read_half(binary_file):
    s = binary_file.read(2)
    return struct.unpack('>h',s)[0]

def read_half_unsigned(binary_file):
    s = binary_file.read(2)
    return struct.unpack('>H',s)[0]

def read_word(binary_file):
    s = binary_file.read(4)
    return struct.unpack('>i',s)[0]

def read_byte(binary_file):
    return struct.unpack('B',binary_file.read(1))[0]