#coding: utf-8
import random, os, sys
from struct import *

class ByteArray:
    def __init__(gift, bytes=b""):
        reload(sys)
        sys.setdefaultencoding("ISO-8859-1")
        if type(bytes) == str:
            try:
                bytes = bytes.encode()
            except Exception as e:
                print(e)
                print("error on encode packet str to bytes")
        gift.bytes = bytes

    def writeByte(gift, value):
        gift.write(pack("!B", int(value) & 0xFF))
        return gift

    def writeShort(gift, value):
        gift.write(pack("!H", int(value) & 0xFFFF))
        return gift
    
    def writeInt(gift, value):
        gift.write(pack("!I", long(value) & 0xFFFFFFFF))
        return gift

    def writeBool(gift, value):
        return gift.writeByte(1 if bool(value) else 0)

    def writeUTF(gift, value):
        value = bytes(value.encode())
        gift.writeShort(len(value))
        gift.write(value)
        return gift

    def writeBytes(gift, value):
        gift.bytes += value
        return gift

    def read(gift, c = 1):
        found = ""
        if gift.getLength() >= c:
            found = gift.bytes[:c]
            gift.bytes = gift.bytes[c:]

        return found

    def write(gift, value):
        gift.bytes += value
        return gift

    def readByte(gift):
        value = 0
        if gift.getLength() >= 1:
            value = unpack("!B", gift.read())[0]
        return value

    def readShort(gift):
        value = 0
        if gift.getLength() >= 2:
            value = unpack("!H", gift.read(2))[0]
        return value

    def readInt(gift):
        value = 0
        if gift.getLength() >= 4:
            value = unpack("!I", gift.read(4))[0]
        return value

    def readUTF(gift):
        value = ""
        if gift.getLength() >= 2:
            value = gift.read(gift.readShort()).decode()
        return value

    def readBool(gift):
        return gift.readByte() > 0

    def readUTFBytes(gift, size):
        value = gift.bytes[:int(size)]
        gift.bytes = gift.bytes[int(size):]
        return value

    def getBytes(gift):
        return gift.bytes

    def toByteArray(gift):
        return gift.getBytes()

    def getLength(gift):
        return len(gift.bytes)

    def bytesAvailable(gift):
        return gift.getLength() > 0


class DailyQuest:
    def __init__(gift, client, server):
        gift.client = client
        gift.server = client.server
        gift.Cursor = client.Cursor

        # List
        gift.missionCheck = []

        # Boolean
        gift.createAccount = False

    def loadDailyQuest(gift, createAccount):
        gift.createAccount = createAccount
        gift.getMissions()
    	gift.activeDailyQuest()
        gift.updateDailyQuest(True)

    def activeDailyQuest(gift):
    	gift.client.sendPacket([144, 5], ByteArray().writeBool(True).toByteArray())

    def getMissions(gift):
        if gift.createAccount:
            ID = 0
            while ID < 3:
                if int(gift.client.dailyQuest[ID]) == 0:
                    mission = gift.randomMission()
                    if mission[0] == int(gift.client.dailyQuest[0]) or int(gift.client.dailyQuest[1]) or int(gift.client.dailyQuest[2]):
                        mission = gift.randomMission()
                    gift.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [int(mission[0]), gift.client.playerID])
                    rs = gift.Cursor.fetchone()
                    if not rs:
                        gift.Cursor.execute("insert into DailyQuest values (%s, %s, %s, %s, '0', %s, '0')", [gift.client.playerID, int(mission[0]), int(mission[1]), int(mission[2]), int(mission[3])])
                    gift.client.dailyQuest[ID] = int(mission[0])
                    gift.client.remainingMissions += 1
                    gift.updateDailyQuest(True)
                ID += 1
            gift.client.dailyQuest[3] = 1
            gift.updateDailyQuest(True)

        gift.Cursor.execute("select MissionID from DailyQuest where UserID = %s", [gift.client.playerID])
        rs = gift.Cursor.fetchall()
        if rs:
            for ms in rs:
                gift.missionCheck.append(int(ms[0]))

        for missionID in gift.missionCheck:
            if gift.checkFinishMission(missionID, gift.client.playerID):
                if int(missionID) in gift.client.dailyQuest:
                    gift.completeMission(missionID, gift.client.playerID)
            gift.missionCheck.remove(missionID)

    def checkFinishMission(gift, missionID, playerID):
        gift.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [missionID, playerID])
        rs = gift.Cursor.fetchone()
        if int(rs[4]) >= int(rs[3]):
            return True
        return False

    def updateDailyQuest(gift, alterDB = False):
        if alterDB:
            gift.client.updateDatabase()
            
        gift.Cursor.execute("select DailyQuest, RemainingMissions from Users where PlayerID = %s", [gift.client.playerID])
        rs = gift.Cursor.fetchone()
        if rs:
            gift.client.remainingMissions = rs[1]
            gift.client.dailyQuest = map(str, filter(None, rs[0].split(","))) if rs[0] != "" else [0, 0, 0, 1]

    def randomMission(gift):
        missionID = random.randint(1, 7)
        id = 0
        while int(gift.client.dailyQuest[id]) == int(missionID):
            missionID = random.randint(1, 7)
            id += 1
        missionType = 0
        reward = random.randint(15, 50)
        collect = random.randint(10, 65)

        if missionID == 2:
            missionType = random.randint(1, 3)

        if missionID == 6:
            collect = 1

        return [missionID, missionType, collect, reward]

    def getMission(gift, missionID, playerID):
    	gift.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [missionID, playerID])
    	rs = gift.Cursor.fetchone()
        if rs:
            if int(rs[6]) == 0:
                return [int(missionID), int(rs[2]), int(rs[3]), int(rs[4]), int(rs[5])]
            else:
                return int(rs[4])

    def changeMission(gift, missionID, playerID):
        mission = gift.randomMission()
        continueChange = False

        while missionID == int(mission[0]):
            mission = gift.randomMission()

        if missionID == int(gift.client.dailyQuest[0]):
            gift.client.dailyQuest[3] = 0
            gift.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [mission[0], playerID])
            rs = gift.Cursor.fetchone()
            if rs:
                if not mission[0] == int(gift.client.dailyQuest[0]) or int(gift.client.dailyQuest[1]) or int(gift.client.dailyQuest[2]):
                    gift.client.dailyQuest[0] = mission[0]
            else:
                if not mission[0] == int(gift.client.dailyQuest[0]) or int(gift.client.dailyQuest[1]) or int(gift.client.dailyQuest[2]):
                    gift.Cursor.execute("insert into DailyQuest values (%s, %s, %s, %s, '0', %s, '0')", [playerID, mission[0], mission[1], mission[2], mission[3]])
                    gift.client.dailyQuest[0] = mission[0]

        elif missionID == int(gift.client.dailyQuest[1]):
            gift.client.dailyQuest[3] = 0
            gift.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [mission[0], playerID])
            rs = gift.Cursor.fetchone()
            if rs:
                if not mission[0] == int(gift.client.dailyQuest[0]) or int(gift.client.dailyQuest[1]) or int(gift.client.dailyQuest[2]):
                    gift.client.dailyQuest[1] = gift.client.dailyQuest[0]
                    gift.client.dailyQuest[0] = mission[0]
            else:
                if not mission[0] == int(gift.client.dailyQuest[0]) or int(gift.client.dailyQuest[1]) or int(gift.client.dailyQuest[2]):
                    gift.Cursor.execute("insert into DailyQuest values (%s, %s, %s, %s, '0', %s, '0')", [playerID, mission[0], mission[1], mission[2], mission[3]])
                    gift.client.dailyQuest[1] = gift.client.dailyQuest[0]
                    gift.client.dailyQuest[0] = mission[0]

        elif missionID == int(gift.client.dailyQuest[2]):
            gift.client.dailyQuest[3] = 0
            gift.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [mission[0], playerID])
            rs = gift.Cursor.fetchone()
            if rs:
                if not mission[0] == int(gift.client.dailyQuest[0]) or int(gift.client.dailyQuest[1]) or int(gift.client.dailyQuest[2]):
                    gift.client.dailyQuest[2] = gift.client.dailyQuest[1]
                    gift.client.dailyQuest[1] = gift.client.dailyQuest[0]
                    gift.client.dailyQuest[0] = mission[0]
            else:
                if not mission[0] == int(gift.client.dailyQuest[0]) or int(gift.client.dailyQuest[1]) or int(gift.client.dailyQuest[2]):
                    gift.Cursor.execute("insert into DailyQuest values (%s, %s, %s, %s, '0', %s, '0')", [playerID, mission[0], mission[1], mission[2], mission[3]])
                    gift.client.dailyQuest[2] = gift.client.dailyQuest[1]
                    gift.client.dailyQuest[1] = gift.client.dailyQuest[0]
                    gift.client.dailyQuest[0] = mission[0]

        gift.updateDailyQuest(True)

    def upMission(gift, missionID, playerID):
        gift.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [missionID, playerID])
        rs = gift.Cursor.fetchone()
        if rs:
            gift.Cursor.execute("update DailyQuest set QntCollected = QntCollected + 1 where MissionID = %s and UserID = %s", [missionID, playerID])
            gift.updateDailyQuest(True)
            gift.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [missionID, playerID])
            rs = gift.Cursor.fetchone()
            if gift.checkFinishMission(int(missionID), playerID):
                gift.completeMission(int(missionID), playerID)
            else:
                gift.client.sendPacket([144, 4], ByteArray().writeShort(missionID).writeByte(0).writeShort(rs[4]).writeShort(rs[3]).writeShort(rs[5]).writeShort(0).toByteArray())

    def completeMission(gift, missionID, playerID):
        gift.Cursor.execute("select * from DailyQuest where Fraise = '1' and UserID = %s", [playerID])
        rs = gift.Cursor.fetchone()
        if rs:
            gift.Cursor.execute("update DailyQuest set QntCollected = QntCollected + 1 where Fraise = '1' and UserID = %s", [playerID])
            gift.client.cheeseCount += int(rs[5])
            gift.client.shopCheeses += int(rs[5])
            #gift.client.addConsumable(random.randint(0, 2350), random.randint(0, 5))
            gift.client.remainingMissions -= 1
            mission = gift.randomMission()
            if missionID == 6:
                mission[2] = 1

            if missionID == int(gift.client.dailyQuest[0]):
                gift.client.dailyQuest[0] = 0
                gift.Cursor.execute("update DailyQuest set QntCollected = 0 and QntToCollect = %s and Reward = %s where MissionID = %s and UserID = %s", [mission[2], mission[3], missionID, playerID])

            elif missionID == int(gift.client.dailyQuest[1]):
                gift.client.dailyQuest[1] = 0
                gift.Cursor.execute("update DailyQuest set QntCollected = 0 and QntToCollect = %s and Reward = %s where MissionID = %s and UserID = %s", [mission[2], mission[3], missionID, playerID])

            elif missionID == int(gift.client.dailyQuest[2]):
                gift.client.dailyQuest[2] = 0
                gift.Cursor.execute("update DailyQuest set QntCollected = 0 and QntToCollect = %s and Reward = %s where MissionID = %s and UserID = %s", [mission[2], mission[3], missionID, playerID])

            gift.updateDailyQuest(True)
            gift.client.sendPacket([144, 4], ByteArray().writeByte(237).writeByte(129).writeByte(0).writeShort(int(rs[4])+1).writeShort(20).writeInt(20).toByteArray())

    def sendDailyQuest(gift):
        p = ByteArray()
        p.writeByte(gift.client.remainingMissions) # Quantidade de missões

        # Missions
        ID = 0
        while ID < 3:
            if int(gift.client.dailyQuest[ID]) != 0:
                mission = gift.getMission(int(gift.client.dailyQuest[ID]), gift.client.playerID)
                p.writeShort(int(mission[0])) # ID da missão
                p.writeByte(int(mission[1])) # Tipo de missão
                p.writeShort(int(mission[3])) # Quantidade coletada
                p.writeShort(int(mission[2])) # Quantidade a coletar
                p.writeShort(int(mission[4])) # Quantidade a receber
                p.writeShort(0)
                p.writeBool(True if bool(int(gift.client.dailyQuest[3])) else False) # Substituir missão
            ID += 1

        # 4
        mission4 = gift.getMission(237129, gift.client.playerID)
        p.writeByte(237)
        p.writeByte(129)
        p.writeByte(0)
        p.writeShort(int(mission4)) # Quantidade coletada
        p.writeShort(20) # Quantidade a coletar
        p.writeInt(20) # Quantidade a receber
        p.writeBool(False) # Substituir missão

        gift.client.sendPacket([144, 3], p.toByteArray())
