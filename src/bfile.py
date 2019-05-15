import struct


class Bfile:
    def __init__(self, file):
        self.f = open(file, 'rb')

    def close(self):
        self.f.close()

    def readBytes(self, n):
        return self.f.read(n)

    def readfloat(self):
        bytes = self.readBytes(4)
        return struct.unpack('>f', bytes)[0]

    def readu64(self):
        bytes = self.readBytes(8)
        return int.from_bytes(bytes, 'big', signed=False)

    def readu32(self):
        bytes = self.readBytes(4)
        return int.from_bytes(bytes, 'big', signed=False)

    def readu16(self):
        bytes = self.readBytes(2)
        return int.from_bytes(bytes, 'big', signed=False)

    def readu8(self):
        bytes = self.readBytes(1)
        return int.from_bytes(bytes, 'big', signed=False)

    def readbool(self):
        return self.readu8() != 0

    def readstring(self):
        str = ""
        while True:
            read = self.readBytes(1)
            if read[0] == 0:
                return str
            str += read.decode('utf-8')

