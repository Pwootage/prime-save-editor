import retroCRC
import bitstream
from bitstream import BitStream
from numpy import *


FILE_LEN = 8192

out = BitStream()

out.write(b"\xFF" * 64, bytes)  # file comment
out.write(b"\xFF" * 3072, bytes)  # C8-encoded banner texel indicies (96x32)
out.write(b"\xFF" * 512, bytes)  # RGB5A3-encoded banner palette colors
out.write(b"\xFF" * 1024, bytes)  # C8-encoded icon texel indicies (32x32)
out.write(b"\xFF" * 512, bytes)  # RGB5A3-encoded icon palette colors
out.write(b"\xFF" * 4, bytes)  # version
out.write(b"\xFF" * 3, bytes)  # save present
out.write(b"\xFF" * 98, bytes)  # NES state
out.write(b"\xFF" * 64, bytes)  # Unknown blob
out.write([True] * 2, bool) #

out.write([True] * 2, bool) # 2b: times frozen in FPS (for three-time HUD memo)
out.write([True] * 2, bool) # 2b: times frozen in morph ball (for three-time HUD memo)
out.write([True] * 1, bool) # 1b: power bomb ammunition acquired (for one-time HUD memo)
out.write([True] * 7, bool) # 7b: log scan percent
out.write([True] * 1, bool) # 1b: metroid fusion linked
out.write([True] * 1, bool) # 1b: normal mode beat
out.write([True] * 1, bool) # 1b: hard mode beat
out.write([True] * 1, bool) # 1b: metroid fusion beat
out.write([True] * 1, bool) # 1b: all items collected
out.write([True] * 2, bool) # 2b: auto mapper key state
# for each MLVL sorted by MLVL asset ID:
#     for each cinematic entity in MLVL's SAVW:
#         1b: cinematic viewed



print("Bytes: {}".format(len(out) / 8))

for i in range(0, (FILE_LEN - 4) * 8 - len(out)):
    out.write(False, bool)

print("Bytes: {}".format(len(out) / 8))

out = out.read(bytes, FILE_LEN - 4)

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
