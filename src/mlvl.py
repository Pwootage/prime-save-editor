from pathlib import Path

from src.bfile import Bfile


class Mlvl:
    def __init__(self, file):
        self.id = Path(file).stem
        self.cines = []
        self.scans = []
        self.relays = []
        self.doors = []
        self.areas = []
        self.layers = []
        self.audioGroups = []
        self.layerCount = 0
        self.readFromFile(file)

    def readFromFile(self, file):
        f = Bfile(file)

        magic = f.readu32()
        assert (magic == 0xDEAFBABE)

        version = f.readu32()
        assert (version == 0x11)

        self.worldName = f.readu32()
        self.savwID = f.readu32()
        self.skybox = f.readu32()  # Default skybox CMDL
        relayCount = f.readu32()
        for i in range(0, relayCount):
            sender = f.readu32()
            recipient = f.readu32()
            message = f.readu16()
            active = f.readbool()
            relay = MemoryRelay(
                sender=sender,
                recipient=recipient,
                message=message,
                active=active
            )
            self.relays.append(relay)

        areaCount = f.readu32()
        assert (f.readu32() == 1)  # Unknown

        for _ in range(0, areaCount):
            areaName = f.readu32()
            transform = [f.readfloat() for _ in range(0, 12)]
            bb = [f.readfloat() for _ in range(0, 6)]
            mrea = f.readu32()
            internalID = f.readu32()
            attachedCount = f.readu32()
            attachedRooms = [f.readu16() for _ in range(0, attachedCount)]
            depCount = f.readu32()
            deps = [(f.readu32(), f.readu32()) for _ in range(0, depCount)]
            dep2Count = f.readu32()
            deps2 = [(f.readu32(), f.readu32()) for _ in range(0, dep2Count)]
            depOffsetCount = f.readu32()
            depOffsets = [f.readu32() for _ in range(0, depOffsetCount)]
            dockCount = f.readu32()
            docks = []
            for _ in range(0, dockCount):
                connectingCount = f.readu32()
                connectingDocks = [
                    ConnectingDock(areaIndex=f.readu32(), dockIndex=f.readu32())
                    for _ in range(0, connectingCount)
                ]
                dockCoordinateCount = f.readu32()
                dockCoordinates = [(f.readfloat(), f.readfloat(), f.readfloat()) for _ in range(0, dockCoordinateCount)]
                dock = Dock(
                    connectingDocks=connectingDocks,
                    dockCoordinates=dockCoordinates
                )
                docks.append(dock)

            area = Area(
                name=areaName,
                transform=transform,
                bb=bb,
                mrea=mrea,
                internalID=internalID,
                attachedRooms=attachedRooms,
                deps=deps,
                deps2=deps2,
                depOffsets=depOffsets,
                docks=docks,
                layerCount=0  # Don't know this yet
            )
            self.areas.append(area)

        self.mapw = f.readu32()
        assert (f.readu8() == 0)  # Unknown, presumably same as SCLY
        self.scriptInstanceCount = f.readu32()

        audioGroupCount = f.readu32()
        self.audioGroups = [(f.readu32(), f.readu32()) for _ in range(0, audioGroupCount)]
        assert (f.readu8() == 0)  # Empty string
        assert (f.readu32() == areaCount)
        for areaID in range(0, areaCount):
            # Area layer flags
            layerCount = f.readu32()
            layerFlags = f.readu64()
            self.areas[areaID].layerCount = layerCount
            for i in range(0, layerCount):
                active = ((layerFlags >> i) & 1) != 0
                self.layers.append(Layer(active=active))

        layerNameCount = f.readu32()
        layerNames = [f.readstring() for _ in range(0, layerNameCount)]

        assert (f.readu32() == areaCount)

        cLayerCount = 0
        for areaID in range(0, areaCount):
            offset = f.readu32()
            for layerNum in range(0, self.areas[areaID].layerCount):
                self.layers[cLayerCount].__dict__['name'] = layerNames[offset]
                self.layers[cLayerCount].__dict__['area'] = area
                cLayerCount += 1

        f.close()
        pass


class MemoryRelay:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Area:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Dock:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ConnectingDock:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Layer:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
