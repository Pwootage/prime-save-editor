import retroCRC
import bitstream
from bitstream import BitStream
from numpy import *


FILE_LEN = 8192

out = bytearray()

with open("01-GM8E-MetroidPrime A.orig.gci", "rb") as f:
    out += bytearray(f.read(8192 + 64))

# out = bytearray(b"\xff" * (FILE_LEN - 4))

print("Bytes: {}".format(len(out)))

out = out[68:]


print("Bytes: {}".format(len(out)))


# Make file B I G

for i in range(0, 39):
    out += bytearray([0xFF] * 8192 * 16)

print("Bytes: {}".format(len(out)))

crc = retroCRC.crc_bytes(retroCRC.DEFAULT_CRC, out)
print("CRC: {}".format(hex(crc)))

out = bytearray([
    (crc >> 24) & 0xFF,
    (crc >> 16) & 0xFF,
    (crc >> 8) & 0xFF,
    (crc >> 0) & 0xFF
]) + out

print("Bytes: {}".format(len(out)))

len_before_prefix = len(out)

PREFIX = bytearray()

with open("fileprefix.bin", "rb") as f:
    PREFIX += bytearray(f.read(64))

out = PREFIX + out

# 25174016 / 8192 = 3073 = 0xC01

len_in_blocks = int(ceil(len_before_prefix / 8192))

out[0x38] = (len_in_blocks >> 8) & 0xFF
out[0x39] = (len_in_blocks >> 0) & 0xFF

print(hex(out[0x38]))
print(hex(out[0x39]))

print("Bytes: {}".format(len(out)))

with open("01-GM8E-MetroidPrime A.gci", "wb") as f:
    f.write(out)
    f.flush()
