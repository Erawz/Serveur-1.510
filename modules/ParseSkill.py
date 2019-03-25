#coding: utf-8

# Modules
from ByteArray import ByteArray
from Identifiers import Identifiers

# Library
from twisted.internet import reactor

class ParseSkill:
    def __init__(gift, player, server):
        gift.client = player
        gift.server = player.server
        gift.rangeArea = 85

    def sendExp(gift, level, exp, nextLevel):
        gift.client.sendPacket(Identifiers.send.Shaman_Exp, ByteArray().writeShort(level - 1).writeInt(exp).writeInt(nextLevel).toByteArray())

    def sendGainExp(gift, amount):
        gift.client.sendPacket(Identifiers.send.Shaman_Gain_Exp, ByteArray().writeInt(amount).toByteArray())

    def sendEarnedExp(gift, xp, numCompleted):
        gift.client.sendPacket(Identifiers.send.Shaman_Earned_Exp, ByteArray().writeShort(xp).writeShort(numCompleted).toByteArray())

    def sendEarnedLevel(gift, playerName, level):
        gift.client.room.sendAll(Identifiers.send.Shaman_Earned_Level, ByteArray().writeUTF(playerName).writeShort(level - 1).toByteArray())
    
    def sendTeleport(gift, type, posX, posY):
        gift.client.room.sendAll(Identifiers.send.Teleport, ByteArray().writeByte(type).writeShort(posX).writeShort(posY).toByteArray())
    
    def sendSkillObject(gift, objectID, posX, posY, angle):
        gift.client.room.sendAll(Identifiers.send.Skill_Object, ByteArray().writeShort(posX).writeShort(posY).writeByte(objectID).writeShort(angle).toByteArray())
    
    def sendShamanSkills(gift, refresh):
        packet = ByteArray().writeByte(len(gift.client.playerSkills))
        for skill in gift.client.playerSkills.items():
            packet.writeByte(skill[0]).writeByte(skill[1])

        packet.writeBoolean(refresh)

        gift.client.sendPacket(Identifiers.send.Shaman_Skills, packet.toByteArray())
    
    def sendEnableSkill(gift, id, count):
        gift.client.sendPacket(Identifiers.send.Enable_Skill, ByteArray().writeUnsignedByte(id).writeUnsignedByte(count).toByteArray())
    
    def sendShamanFly(gift, fly):
        gift.client.room.sendAllOthers(gift.client, Identifiers.send.Shaman_Fly, ByteArray().writeInt(gift.client.playerCode).writeBoolean(fly).toByteArray())
    
    def sendProjectionSkill(gift, posX, posY, dir):
        gift.client.room.sendAllOthers(gift.client, Identifiers.send.Projection_Skill, ByteArray().writeShort(posX).writeShort(posY).writeShort(dir).toByteArray())
    
    def sendConvertSkill(gift, objectID):
        gift.client.room.sendAll(Identifiers.send.Convert_Skill, ByteArray().writeInt(objectID).writeByte(0).toByteArray())
    
    def sendDemolitionSkill(gift, objectID):
        gift.client.room.sendAll(Identifiers.send.Demolition_Skill, ByteArray().writeInt(objectID).toByteArray())
    
    def sendBonfireSkill(gift, px, py, seconds):
        gift.client.room.sendAll(Identifiers.send.Bonfire_Skill, ByteArray().writeShort(px).writeShort(py).writeByte(seconds).toByteArray())
    
    def sendSpiderMouseSkill(gift, px, py):
        gift.client.room.sendAll(Identifiers.send.Spider_Mouse_Skill, ByteArray().writeShort(px).writeShort(py).toByteArray())

    def sendRolloutMouseSkill(gift, playerCode):
        gift.client.room.sendAll(Identifiers.send.Rollout_Mouse_Skill, ByteArray().writeInt(playerCode).toByteArray())

    def sendDecreaseMouseSkill(gift, playerCode):
        gift.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(playerCode).writeShort(70).writeBoolean(True).toByteArray())
    
    def sendLeafMouseSkill(gift, playerCode):
        gift.client.room.sendAll(Identifiers.send.Leaf_Mouse_Skill, ByteArray().writeByte(1).writeInt(playerCode).toByteArray())
    
    def sendIceMouseSkill(gift, playerCode, iced):
        gift.client.room.sendAll(Identifiers.send.Iced_Mouse_Skill, ByteArray().writeInt(playerCode).writeBoolean(iced).toByteArray())

    def sendGravitationalSkill(gift, seconds, velX, velY):
        gift.client.room.sendAll(Identifiers.send.Gravitation_Skill, ByteArray().writeShort(seconds).writeInt(velX).writeInt(velY).toByteArray())
    
    def sendGrapnelSkill(gift, playerCode, px, py):
        gift.client.room.sendAll(Identifiers.send.Grapnel_Mouse_Skill, ByteArray().writeInt(playerCode).writeShort(px).writeShort(py).toByteArray())
    
    def sendEvolutionSkill(gift, playerCode):
        gift.client.room.sendAll(Identifiers.send.Evolution_Skill, ByteArray().writeInt(playerCode).writeByte(100).toByteArray())

    def sendGatmanSkill(gift, playerCode):
        gift.client.room.sendAll(Identifiers.send.Gatman_Skill, ByteArray().writeInt(playerCode).writeByte(1).toByteArray())
    
    def sendRestorativeSkill(gift, objectID, id):
        gift.client.room.sendAll(Identifiers.send.Restorative_Skill, ByteArray().writeInt(objectID).writeInt(id).toByteArray())
    
    def sendRecyclingSkill(gift, id):
        gift.client.room.sendAll(Identifiers.send.Recycling_Skill, ByteArray().writeShort(id).toByteArray())
    
    def sendAntigravitySkill(gift, objectID):
        gift.client.room.sendAll(Identifiers.send.Antigravity_Skill, ByteArray().writeInt(objectID).writeShort(0).toByteArray())
    
    def sendHandymouseSkill(gift, handyMouseByte, objectID):
        gift.client.room.sendAll(Identifiers.send.Handymouse_Skill, ByteArray().writeByte(handyMouseByte).writeInt(objectID).writeByte(gift.client.room.lastHandymouse[1]).writeInt(gift.client.room.lastHandymouse[0]).toByteArray())

    def earnExp(gift, isShaman, exp):
        gainExp = exp * (((3 if gift.client.shamanLevel < 30 else (6 if gift.client.shamanLevel >= 30 and gift.client.shamanLevel < 60 else 10)) if gift.client.shamanType == 0 else (5 if gift.client.shamanLevel < 30 else (10 if gift.client.shamanLevel >= 30 and gift.client.shamanLevel < 60 else 20))) if isShaman else 1)
        gift.client.shamanExp += gainExp
        if gift.client.shamanExp < gift.client.shamanExpNext:
            gift.sendGainExp(gift.client.shamanExp)
            gift.sendExp(gift.client.shamanLevel, gift.client.shamanExp, gift.client.shamanExpNext)
            if isShaman:
                gift.sendEarnedExp(gainExp, exp)
        else:
            if gift.client.shamanLevel < 300:
                gift.client.shamanLevel += 1
                gift.client.shamanExp -= gift.client.shamanExpNext
                if gift.client.shamanExp < 0:
                    gift.client.shamanExp = 0

                gift.client.shamanExpNext += 90

                gift.sendExp(gift.client.shamanLevel, 0, gift.client.shamanExpNext)
                gift.sendGainExp(gift.client.shamanExp)
                if isShaman:
                    gift.sendEarnedExp(gainExp, exp)

                if gift.client.shamanLevel >= 20:
                    gift.sendEarnedLevel(gift.client.playerName, gift.client.shamanLevel)

    def buySkill(gift, skill):
        if gift.client.shamanLevel - 1 > len(gift.client.playerSkills):
            if gift.client.playerSkills.has_key(skill):
                gift.client.playerSkills[skill] += 1
            else:
                gift.client.playerSkills[skill] = 1
            gift.sendShamanSkills(True)

    def redistributeSkills(gift):
        if gift.client.shopCheeses >= gift.client.shamanLevel:
            if len(gift.client.playerSkills) >=  1:
                if gift.client.canRedistributeSkills:
                    gift.client.shopCheeses -= gift.client.shamanLevel
                    gift.client.playerSkills = {}
                    gift.sendShamanSkills(True)
                    gift.client.canRedistributeSkills = False
                    if gift.client.resSkillsTimer != None: gift.client.resSkillsTimer.cancel()
                    gift.client.resSkillsTimer = reactor.callLater(600, setattr, gift, "canRedistributeSkills", True)
                    gift.client.totem = [0, ""]
                else:
                    gift.client.sendPacket(Identifiers.send.Redistribute_Error_Time)
        else:
            gift.client.sendPacket(Identifiers.send.Redistribute_Error_Cheeses)

    def getTimeSkill(gift):
        if gift.client.playerSkills.has_key(0):
            gift.client.room.addTime += gift.client.playerSkills[0] * 5

    def getkills(gift):
        if gift.client.isShaman:
            if gift.client.playerSkills.has_key(4) and not gift.client.room.isDoubleMap:
                gift.client.canShamanRespawn = True

            for skill in [5, 8, 9, 11, 12, 26, 28, 29, 31, 41, 46, 48, 51, 52, 53, 60, 62, 65, 66, 67, 69, 71, 74, 80, 81, 83, 85, 88, 90, 93]:
                if gift.client.playerSkills.has_key(skill) and not (gift.client.room.isSurvivor and skill == 81):
                    gift.sendEnableSkill(skill, gift.client.playerSkills[skill] * 2 if skill in [28, 65, 74] else gift.client.playerSkills[skill])

            for skill in [6, 30, 33, 34, 44, 47, 50, 63, 64, 70, 73, 82, 84, 92]:
                if gift.client.playerSkills.has_key(skill):
                    if skill == 6: gift.client.ambulanceCount = skill
                    gift.sendEnableSkill(skill, 1)

            for skill in [7, 14, 27, 86, 87, 94]:
                if gift.client.playerSkills.has_key(skill):
                    gift.sendEnableSkill(skill, 100)

            for skill in [10, 13]:
                if gift.client.playerSkills.has_key(skill):
                    gift.sendEnableSkill(skill, 3)

            if gift.client.playerSkills.has_key(20):
                count = gift.client.playerSkills[20]            
                gift.sendEnableSkill(20, [114, 118, 120, 122, 126][(5 if count > 5 else count) - 1])

            if gift.client.playerSkills.has_key(21):
                gift.bubblesCount = gift.client.playerSkills[21]

            if gift.client.playerSkills.has_key(22) and not gift.client.room.currentMap in [108, 109]:
                count = gift.client.playerSkills[22]
                gift.sendEnableSkill(22, [25, 30, 35, 40, 45][(5 if count > 5 else count) - 1])

            if gift.client.playerSkills.has_key(23):
                count = gift.client.playerSkills[23]            
                gift.sendEnableSkill(23, [40, 50, 60, 70, 80][(5 if count > 5 else count) - 1])

            if gift.client.playerSkills.has_key(24):
                gift.client.isOpportunist = True

            if gift.client.playerSkills.has_key(32):
                gift.client.iceCount += gift.client.playerSkills[32]

            if gift.client.playerSkills.has_key(40):
                count = gift.client.playerSkills[40]            
                gift.sendEnableSkill(40, [30, 40, 50, 60, 70][(5 if count > 5 else count) - 1])

            if gift.client.playerSkills.has_key(42):
                count = gift.client.playerSkills[42]            
                gift.sendEnableSkill(42, [240, 230, 220, 210, 200][(5 if count > 5 else count) - 1])

            if gift.client.playerSkills.has_key(43):
                count = gift.client.playerSkills[43]            
                gift.sendEnableSkill(43, [240, 230, 220, 210, 200][(5 if count > 5 else count) - 1])

            if gift.client.playerSkills.has_key(45):
                count = gift.client.playerSkills[45]
                gift.sendEnableSkill(45, [110, 120, 130, 140, 150][(5 if count > 5 else count) - 1])

            if gift.client.playerSkills.has_key(49):
                count = gift.client.playerSkills[49]
                gift.sendEnableSkill(49, [80, 70, 60, 50, 40][(5 if count > 5 else count) - 1])

            if gift.client.playerSkills.has_key(54):
                gift.sendEnableSkill(54, 130)

            if gift.client.playerSkills.has_key(72):
                count = gift.client.playerSkills[72]            
                gift.sendEnableSkill(72, [25, 30, 35, 40, 45][(5 if count > 5 else count) - 1])

            if gift.client.playerSkills.has_key(89) and not gift.client.room.isSurvivor:
                count = gift.client.playerSkills[89]            
                gift.sendEnableSkill(49, [56, 52, 48, 44, 40][(5 if count > 5 else count) - 1])
                gift.sendEnableSkill(54, [96, 92, 88, 84, 80][(5 if count > 5 else count) - 1])

            if gift.client.playerSkills.has_key(91):
                gift.client.desintegration = True

    def getPlayerSkills(gift, skills):
        if skills.has_key(1):
            gift.sendEnableSkill(1, [110, 120, 130, 140, 150][(5 if skills[1] > 5 else skills[1]) - 1])

        if skills.has_key(2):
            gift.sendEnableSkill(2, [114, 126, 118, 120, 122][(5 if skills[2] > 5 else skills[2]) - 1])

        if skills.has_key(68):
            gift.sendEnableSkill(68, [96, 92, 88, 84, 80][(5 if skills[68] > 5 else skills[68]) - 1])

    def placeSkill(gift, objectID, code, px, py, angle):
        if code == 36:
            for player in gift.client.room.clients.values():
                if gift.checkQualifiedPlayer(px, py, player):
                    player.sendPacket(Identifiers.send.Can_Transformation, 1)
                    break

        elif code == 37:
            for player in gift.client.room.clients.values():
                if gift.checkQualifiedPlayer(px, py, player):
                    gift.sendTeleport(36, player.posX, player.posY)
                    player.room.movePlayer(player.playerName, gift.client.posX, gift.client.posY, False, 0, 0, True)
                    gift.sendTeleport(37, gift.client.posX, gift.client.posY)
                    break

        elif code == 38:
            for player in gift.client.room.clients.values():
                if player.isDead and not player.hasEnter and not player.isAfk and not player.isShaman and not player.isNewPlayer:
                    if gift.client.ambulanceCount > 0:
                        gift.client.ambulanceCount -= 1
                        gift.client.room.respawnSpecific(player.playerName)
                        player.isDead = False
                        player.hasCheese = False
                        player.room.movePlayer(player.playerName, gift.client.posX, gift.client.posY, False, 0, 0, True)
                        gift.sendTeleport(37, gift.client.posX, gift.client.posY)
                    else:
                        break
            gift.client.room.sendAll(Identifiers.send.Skill, chr(38) + chr(1))

        elif code == 42:
            gift.sendSkillObject(3, px, py, 0)

        elif code == 43:
            gift.sendSkillObject(1, px, py, 0)

        elif code == 47:
            if gift.client.room.numCompleted > 1:
                for player in gift.client.room.clients.values():
                    if player.hasCheese and gift.checkQualifiedPlayer(px, py, player):
                        player.playerWin(0)
                        break

        elif code == 55:
            for player in gift.client.room.clients.values():
                if not player.hasCheese and gift.client.hasCheese and gift.checkQualifiedPlayer(px, py, player):
                    player.sendGiveCheese()
                    gift.client.sendRemoveCheese()
                    gift.client.hasCheese = False
                    break

        elif code == 56:
            gift.sendTeleport(36, gift.client.posX, gift.client.posY)
            gift.client.room.movePlayer(gift.client.playerName, px, py, False, 0, 0, False)
            gift.sendTeleport(37, px, py)

        elif code == 57:
            if gift.client.room.cloudID == -1:
                gift.client.room.cloudID = objectID
            else:
                gift.client.room.removeObject(gift.client.room.cloudID)
                gift.client.room.cloudID = objectID

        elif code == 61:
            if gift.client.room.companionBox == -1:
                gift.client.room.companionBox = objectID
            else:
                gift.client.room.removeObject(gift.client.room.companionBox)
                gift.client.room.companionBox = objectID

        elif code == 70:
            gift.sendSpiderMouseSkill(px, py)

        elif code == 71:
            for player in gift.client.room.clients.values():
                if gift.checkQualifiedPlayer(px, py, player):
                    gift.sendRolloutMouseSkill(player.playerCode)
                    gift.client.room.sendAll(Identifiers.send.Skill, chr(71) + chr(1))
                    break

        elif code == 73:
            for player in gift.client.room.clients.values():
                if gift.checkQualifiedPlayer(px, py, player):
                    gift.sendDecreaseMouseSkill(player.playerCode)
                    break

        elif code == 74:
            for player in gift.client.room.clients.values():
                if gift.checkQualifiedPlayer(px, py, player):
                    gift.sendLeafMouseSkill(player.playerCode)
                    break

        elif code == 75:
            gift.client.room.sendAll(Identifiers.send.Remove_All_Objects_Skill)

        elif code == 76:
            gift.sendSkillObject(5, px, py, angle)

        elif code == 79:
            if not gift.client.room.isSurvivor:
                for client in gift.client.room.clients.values():
                    if gift.checkQualifiedPlayer(px, py, client):
                        gift.sendIceMouseSkill(client.playerCode, True)
                gift.client.room.sendAll(Identifiers.send.Skill, chr(79) + chr(1))
                reactor.callLater(gift.client.playerSkills[82] * 2, lambda: gift.sendIceMouseSkill(client.playerCode, False))

        elif code == 81:
            gift.sendGravitationalSkill(gift.client.playerSkills[63] * 2, 0, 0)

        elif code == 83:
            for player in gift.client.room.clients.values():
                if gift.checkQualifiedPlayer(px, py, player):
                    player.sendPacket(Identifiers.send.Can_Meep, 1)
                    break

        elif code == 84:
            gift.sendGrapnelSkill(gift.client.playerCode, px, py)

        elif code == 86:
            if 86 in gift.client.playerSkills:
                gift.sendBonfireSkill(px, py, gift.client.playerSkills[86] * 4)

        elif code == 92:
            gift.getkills()
            gift.client.room.sendAll(Identifiers.send.Reset_Shaman_Skills)

        elif code == 93:
            for player in gift.client.room.clients.values():
                if gift.checkQualifiedPlayer(px, py, player):
                    gift.sendEvolutionSkill(player.playerCode)
                    break

        elif code == 94:
            gift.sendGatmanSkill(gift.client.playerCode)

    def parseEmoteSkill(gift, emote):
        count = 0
        if emote == 0 and gift.client.playerSkills.has_key(3):
            for player in gift.client.room.clients.values():
                if gift.client.playerSkills[3] >= count and player != gift.client:
                    if player.posX >= gift.client.posX - 400 and player.posX <= gift.client.posX + 400:
                        if player.posY >= gift.client.posY - 300 and player.posY <= gift.client.posY + 300:
                            player.sendPlayerEmote(0, "", False, False)
                            count += 1
                else:
                    break

        elif emote == 4 and gift.client.playerSkills.has_key(61):
            for player in gift.client.room.clients.values():
                if gift.client.playerSkills[61] >= count and player != gift.client:
                    if player.posX >= gift.client.posX - 400 and player.posX <= gift.client.posX + 400:
                        if player.posY >= gift.client.posY - 300 and player.posY <= gift.client.posY + 300:
                            player.sendPlayerEmote(2, "", False, False)
                            count += 1
                else:
                    break

        elif emote == 8 and gift.client.playerSkills.has_key(25):
            for player in gift.client.room.clients.values():
                if gift.client.playerSkills[25] >= count and player != gift.client:
                    if player.posX >= gift.client.posX - 400 and player.posX <= gift.client.posX + 400:
                        if player.posY >= gift.client.posY - 300 and player.posY <= gift.client.posY + 300:
                            player.sendPlayerEmote(3, "", False, False)
                            count += 1
                else:
                    break

    def checkQualifiedPlayer(gift, px, py, player):
        if not player.playerName == gift.client.playerName and not player.isShaman:
            if player.posX >= px - 85 and player.posX <= px + 85:
                if player.posY >= py - 85 and player.posY <= py + 85:
                    return True
        return False

    def getShamanBadge(gift):
        if gift.client.equipedShamanBadge != 0:
            return gift.client.equipedShamanBadge

        badgesCount = [0, 0, 0, 0, 0]

        for skill in gift.client.playerSkills.items():
            if skill[0] > -1 and skill[0] < 14:
                badgesCount[0] += skill[1]
            elif skill[0] > 19 and skill[0] < 35:
                badgesCount[1] += skill[1]
            elif skill[0] > 39 and skill[0] < 55:
                badgesCount[2] += skill[1]
            elif skill[0] > 59 and skill[0] < 75:
                badgesCount[4] += skill[1]
            elif skill[0] > 79 and skill[0] < 95:
                badgesCount[3] += skill[1]

        return -(badgesCount.index(max(badgesCount)))
