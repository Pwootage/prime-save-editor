import retroCRC
import bitstream
from bitstream import BitStream
from numpy import *
import struct


FILE_LEN = 90176

out = bytearray()

with open("01-GALE-SuperSmashBros0110290334.gci", "rb") as f:
    out += bytearray(f.read(FILE_LEN))

# out = bytearray(b"\xff" * (FILE_LEN - 4))

print("Bytes: {}".format(len(out)))

out = out[64:]
# out += bytearray([0xFF, 0xFF, 0xFF, 0xFF])


print("Bytes: {}".format(len(out)))

# xorstream it
# key = [0xB3, 0xC6, 0xC2, 0x1D]
# for i in range(0, len(out)):
#     out[i] = out[i] ^ key[i % 4]

# Make file B I G

# for i in range(0, 39):
#     out += bytearray([0xFF] * 8192 * 16)

# print("Bytes: {}".format(len(out)))

crc = retroCRC.crc_bytes(retroCRC.DEFAULT_CRC, out)
crc = crc ^ 0xFFFFFFFF
print("CRC: {}".format(hex(crc)))

# out = bytearray([
#     (crc >> 24) & 0xFF,
#     (crc >> 16) & 0xFF,
#     (crc >> 8) & 0xFF,
#     (crc >> 0) & 0xFF
# ]) + out
#
# print("Bytes: {}".format(len(out)))
#
# len_before_prefix = len(out)a
#
# PREFIX = bytearray()
#
# with open("fileprefix.bin", "rb") as f:
#     PREFIX += bytearray(f.read(64))
#
# out = PREFIX + out
#
# # 25174016 / 8192 = 3073 = 0xC01
#
# len_in_blocks = int(ceil(len_before_prefix / 8192))
#
# out[0x38] = (len_in_blocks >> 8) & 0xFF
# out[0x39] = (len_in_blocks >> 0) & 0xFF
#
# print(hex(out[0x38]))
# print(hex(out[0x39]))
#
# print("Bytes: {}".format(len(out)))
#
with open("test.bin", "wb") as f:
    f.write(out)
    f.flush()
