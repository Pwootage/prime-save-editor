import glob
from pathlib import Path

from src.mlvl import Mlvl


class BitFileField:
    def __init__(self, name, offset, bits):
        self.name = name
        self.offset = offset
        self.bits = bits

    def lenStr(self):
        bytes = self.bits // 8
        bits = self.bits % 8
        return f"{self.bits}/{bytes}.{bits}"

    def offsetStr(self):
        bytes = self.offset // 8
        bits = self.offset % 8
        return f"{self.offset}/{hex(bytes)}.{bits} | {self.lenStr()}"


class BitFile:
    def __init__(self, name):
        self.name = name
        self.fields = []
        self.offsetToField = {}
        self.nameToField = {}
        self.len = 0

    def add(self, name, bytes):
        bits = bytes * 8
        offset = self.len
        self.len += bits
        bitfile = BitFileField(name, offset, bits)
        self.fields.append(bitfile)
        self.offsetToField[offset] = bitfile
        self.nameToField[name] = bitfile

    def addb(self, name, bits):
        offset = self.len + bits
        self.len += bits
        bitfile = BitFileField(name, offset, bits)
        self.fields.append(bitfile)
        self.offsetToField[offset] = bitfile
        self.nameToField[name] = bitfile

    def print(self):
        for offset in self.fields:
            print(f"{offset.offsetStr()} - {offset.name}")


def getMlvls(folder):
    mlvls = []

    mlvlFiles = glob.glob(f"{folder}/*.MLVL")
    for mlvlFile in mlvlFiles:
        mlvl = Mlvl(mlvlFile)
        mlvls.append(mlvl)

    mlvls.sort(key=lambda x: x.id)
    return mlvls


def getHints(folder):
    return []


def generatePrimeDataFile(name, folder):
    mlvls = getMlvls(folder)

    f = BitFile(name)
    # File Header
    f.add("crc", 4)
    f.add("comment", 64)
    f.add("bannerTexels", 3072)
    f.add("bannerPalette", 512)
    f.add("iconTexel", 1024)
    f.add("iconPalette", 512)
    # Data Header
    f.add("version", 4)
    for x in range(0, 3):
        f.add(f"savePresent[{x}]", 1)
    # Shared data
    f.add("nesState", 98)
    f.add("unknownShared", 64)
    f.addb("timesFrozenFPS", 2)
    f.addb("timesFrozenMB", 2)
    f.addb("pbAmmoAcquired", 1)
    f.addb("logScanPercent", 7)
    f.addb("fusionLinked", 1)
    f.addb("normalBeat", 1)
    f.addb("hardBeat", 1)
    f.addb("fusionBeat", 1)
    f.addb("allItems", 1)
    f.addb("automapperState", 2)
    for mlvl in mlvls:
        for cineNum, cine in enumerate(mlvl.cines):
            f.addb(f"mlvl[{mlvl.id}].cine[{cineNum}].watched", 1)
            # f.addb(f"mlvl[{mlvl.id}].cine[{cine.name}].watched", 1)

    # Save slot data
    for saveSlot in range(0, 3):
        f.add(f"saveSlot[{saveSlot}].unknownBlob", 128)
        f.add(f"saveSlot[{saveSlot}].timestamp", 4)
        f.addb(f"saveSlot[{saveSlot}].hardMode", 1)
        f.addb(f"saveSlot[{saveSlot}].initPowerupsUsingSpawnpoint", 1)
        f.add(f"saveSlot[{saveSlot}].currentMlvl", 4)
        f.add(f"saveSlot[{saveSlot}].igt", 8)
        # Player State
        f.add(f"saveSlot[{saveSlot}].enabledItemBits", 4)
        f.add(f"saveSlot[{saveSlot}].currentEnergy", 4)
        f.addb(f"saveSlot[{saveSlot}].currentBeam", 3)
        f.addb(f"saveSlot[{saveSlot}].currentSuit", 3)
        f.addb(f"saveSlot[{saveSlot}].powerBeamAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].iceBeamAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].waveBeamAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].plasmaBeamAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].missileAmt/cap", 16)
        f.addb(f"saveSlot[{saveSlot}].scanVisorAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].morphBallBombsAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].powerBombsAmt/cap", 8)
        f.addb(f"saveSlot[{saveSlot}].flamethrowerAm/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].thermalVisorAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].chargeBeamAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].superMissileAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].grappleBeamAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].xrayVisorAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].iceSpreaderAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].spaceJumpBootsAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].morphBallAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].combatVisorAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].boostBallAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].spiderBallAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].powerSuitAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].gravitySuitAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].variaSuitAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].phazonSuitAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].energyTanksAmt/cap", 8)
        f.addb(f"saveSlot[{saveSlot}].unknown1Amt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].unknown2Amt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].wavebusterAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].truthAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].strengthAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].elderAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].wildAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].lifegiverAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].warriorAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].chozoAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].natureAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].sunAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].worldAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].spiritAmt/cap", 2)
        f.addb(f"saveSlot[{saveSlot}].newbornAmt/cap", 2)

        for mlvl in mlvls:
            for scanNum, scan in enumerate(mlvl.scans):
                f.addb(f"saveSlot[{saveSlot}].mlvl[{mlvl.id}].scan[{scanNum}].watched", 1)
                # f.addb(f"mlvl[{mlvl.id}].scan[{scan.name}].watched", 1)

        f.addb(f"saveSlot[{saveSlot}].scanCompletionNumerator", 9)
        f.addb(f"saveSlot[{saveSlot}].scanCompletionDenominator", 9)

        # Game Options
        f.add(f"saveSlot[{saveSlot}].unknownOptionsBlob", 64)
        f.addb(f"saveSlot[{saveSlot}].soundMode", 2)
        f.addb(f"saveSlot[{saveSlot}].screenBrightness", 4)
        f.addb(f"saveSlot[{saveSlot}].screenOffsetX", 6)
        f.addb(f"saveSlot[{saveSlot}].screenOffsetY", 6)
        f.addb(f"saveSlot[{saveSlot}].screenStretch", 5)
        f.addb(f"saveSlot[{saveSlot}].sfxVolume", 7)
        f.addb(f"saveSlot[{saveSlot}].musicVolume", 7)
        f.addb(f"saveSlot[{saveSlot}].hudAlpha", 8)
        f.addb(f"saveSlot[{saveSlot}].helmetAlpha", 8)
        f.addb(f"saveSlot[{saveSlot}].hudLag", 1)
        f.addb(f"saveSlot[{saveSlot}].hints", 1)
        f.addb(f"saveSlot[{saveSlot}].invertY", 1)
        f.addb(f"saveSlot[{saveSlot}].rumble", 1)
        f.addb(f"saveSlot[{saveSlot}].swapBeams", 1)  # The worst option

        # Hint Options
        for hintNum, hint in getHints(folder):
            f.addb(f"saveSlot[{saveSlot}].hints[{hintNum}].state", 2)
            f.add(f"saveSlot[{saveSlot}].hints[{hintNum}].remainingTime", 4)
            # f.addb(f"saveSlot[{saveSlot}].hints[{hint.name}].state", 2)
            # f.add(f"saveSlot[{saveSlot}].hints[{hint.name}].remainingTime", 4)

        # World State
        for mlvl in mlvls:
            f.add(f"saveSlot[{saveSlot}].mlvl[{mlvl.id}].currentAreaID", 4)
            f.add(f"saveSlot[{saveSlot}].mlvl[{mlvl.id}].initialMREAAssetID", 4)
            # Relay Tracker
            for relayNum, relay in enumerate(mlvl.relays):
                f.addb(f"saveSlot[{saveSlot}].mlvl[{mlvl.id}].relay[{relayNum}].active", 1)
                # f.addb(f"mlvl[{mlvl.id}].scan[{relay.name}].watched", 1)

            # Map world info
            for areaNum, area in enumerate(mlvl.areas):
                f.addb(f"saveSlot[{saveSlot}].mlvl[{mlvl.id}].area[{areaNum}].visited", 1)
                # f.addb(f"mlvl[{mlvl.id}].scan[{area.name}].watched", 1)
            for areaNum, area in enumerate(mlvl.areas):
                f.addb(f"saveSlot[{saveSlot}].mlvl[{mlvl.id}].area[{areaNum}].mapped", 1)
                # f.addb(f"mlvl[{mlvl.id}].scan[{area.name}].watched", 1)
            for doorNum, door in enumerate(mlvl.doors):
                f.addb(f"saveSlot[{saveSlot}].mlvl[{mlvl.id}].door[{doorNum}].opened", 1)
                # f.addb(f"mlvl[{mlvl.id}].scan[{door.name}].watched", 1)

            # Layer state
            f.addb(f"saveSlot[{saveSlot}].layerCount", 10)
            for layerNum, layer in enumerate(mlvl.layers):
                f.addb(f"saveSlot[{saveSlot}].layer[{layerNum}|{layer.area.mrea}.MREA-{layer.name}].layerActive", 1)
    return f
