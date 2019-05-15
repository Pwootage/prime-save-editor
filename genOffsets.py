import fileoffsets

offsets = fileoffsets.generatePrimeDataFile("NTSC", "data/ntsc-0-00-us")

offsets.print()

expectedSize = 0
expectedSize += 4
expectedSize += 64
expectedSize += 3072
expectedSize += 512
expectedSize += 1024
expectedSize += 512
print("Expected before header: ", expectedSize, hex(expectedSize))
expectedSize += 4
expectedSize += 3
print("Expected before shared data: ", expectedSize, hex(expectedSize))
expectedSize += 174
print("Expected before save 1: ", expectedSize, hex(expectedSize))
expectedSize += 940
print("Expected before save 2: ", expectedSize, hex(expectedSize))
expectedSize += 940
print("Expected before save 3: ", expectedSize, hex(expectedSize))
expectedSize += 940
print("Expected size", expectedSize, hex(expectedSize))

# Expected before header:  5188 0x1444
# Expected before shared data:  5195 0x144b
# Expected before save 1:  5369 0x14f9
# Expected before save 2:  6309 0x18a5
# Expected before save 3:  7249 0x1c51
# Expected size 8189 0x1ffd
