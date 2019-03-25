#coding: utf-8
#İmp - Gifted
import re, json, random, urllib, traceback, time as _time, struct

# Modules
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

# Library
from collections import deque
from twisted.internet import reactor

class ParsePackets:
    def __init__(gift, player, server):
        gift.client = player
        gift.server = player.server
        gift.Cursor = player.Cursor

    def parsePacket(gift, packetID, C, CC, packet):
        if C == Identifiers.recv.Old_Protocol.C:
            if CC == Identifiers.recv.Old_Protocol.Old_Protocol:
                data = packet.readUTF()
                gift.client.parsePackets.parsePacketUTF(data)
                return

        elif C == Identifiers.recv.Sync.C:
            if CC == Identifiers.recv.Sync.Object_Sync:
                roundCode = packet.readInt()
                if roundCode == gift.client.room.lastRoundCode:
                    packet2 = ByteArray()
                    while packet.bytesAvailable():
                        objectID = packet.readShort()
                        objectCode = packet.readShort()
                        if objectCode == -1:
                            packet2.writeShort(objectID)
                            packet2.writeShort(-1)
                        else:
                            posX = packet.readShort()
                            posY = packet.readShort()
                            velX = packet.readShort()
                            velY = packet.readShort()
                            rotation = packet.readShort()
                            rotationSpeed = packet.readShort()
                            ghost = packet.readBoolean()
                            stationary = packet.readBoolean()
                            packet2.writeShort(objectID).writeShort(objectCode).writeShort(posX).writeShort(posY).writeShort(velX).writeShort(velY).writeShort(rotation).writeShort(rotationSpeed).writeBoolean(ghost).writeBoolean(stationary).writeBoolean(gift.client.room.getAliveCount() > 1)
                    gift.client.room.sendAllOthers(gift.client, Identifiers.send.Sync, packet2.toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Mouse_Movement:
                roundCode, droiteEnCours, gaucheEnCours, px, py, vx, vy, jump, jump_img, portal, isAngle = packet.readInt(), packet.readBoolean(), packet.readBoolean(), packet.readUnsignedInt(), packet.readUnsignedInt(), packet.readUnsignedShort(), packet.readUnsignedShort(), packet.readBoolean(), packet.readByte(), packet.readByte(), packet.bytesAvailable(),
                angle = packet.readUnsignedShort() if isAngle else -1
                vel_angle = packet.readUnsignedShort() if isAngle else -1
                loc_1 = packet.readBoolean() if isAngle else False

                if roundCode == gift.client.room.lastRoundCode:
                    if droiteEnCours or gaucheEnCours:
                        gift.client.isMovingRight = droiteEnCours
                        gift.client.isMovingLeft = gaucheEnCours

                        if gift.client.isAfk:
                            gift.client.isAfk = False

                    gift.client.posX = px * 800 / 2700
                    gift.client.posY = py * 800 / 2700
                    gift.client.velX = vx
                    gift.client.velY = vy
                    gift.client.isJumping = jump
                
                    packet2 = ByteArray().writeInt(gift.client.playerCode).writeInt(roundCode).writeBoolean(droiteEnCours).writeBoolean(gaucheEnCours).writeUnsignedInt(px).writeUnsignedInt(py).writeUnsignedShort(vx).writeUnsignedShort(vy).writeBoolean(jump).writeByte(jump_img).writeByte(portal)
                    if isAngle:
                        packet2.writeUnsignedShort(angle).writeUnsignedShort(vel_angle).writeBoolean(loc_1)
                    gift.client.room.sendAllOthers(gift.client, Identifiers.send.Player_Movement, packet2.toByteArray())
                return
            
            elif CC == Identifiers.recv.Sync.Mort:
                roundCode, loc_1 = packet.readInt(), packet.readByte()
                if roundCode == gift.client.room.lastRoundCode:
                    gift.client.isDead = True
                    if not gift.client.room.noAutoScore: gift.client.playerScore += 1
                    gift.client.sendPlayerDied()

                    if gift.client.room.getPlayerCountUnique() >= gift.server.needToFirst:
                        if gift.client.room.isSurvivor:
                            for playerCode, client in gift.client.room.clients.items():
                                if client.isShaman:
                                    client.survivorDeath += 1

                                    if client.survivorDeath == 4:
                                        id = 2260
                                        if not id in client.playerConsumables:
                                            client.playerConsumables[id] = 1
                                        else:
                                            count = client.playerConsumables[id] + 1
                                            client.playerConsumables[id] = count
                                        client.sendAnimZeldaInventory(4, id, 1)
                                        client.survivorDeath = 0

                    if not gift.client.room.currentShamanName == "":
                        player = gift.client.room.clients.get(gift.client.room.currentShamanName)

                        if player != None and not gift.client.room.noShamanSkills:
                            if player.bubblesCount > 0:
                                if gift.client.room.getAliveCount() != 1:
                                    player.bubblesCount -= 1
                                    gift.client.sendPlaceObject(gift.client.room.objectID + 2, 59, gift.client.posX, 450, 0, 0, 0, True, True)

                            if player.desintegration:
                                gift.client.parseSkill.sendSkillObject(6, gift.client.posX, 395, 0)
                    gift.client.room.checkChangeMap()
                return

            elif CC == Identifiers.recv.Sync.Player_Position:
                direction = packet.readBoolean()
                gift.client.room.sendAll(Identifiers.send.Player_Position, ByteArray().writeInt(gift.client.playerCode).writeBoolean(direction).toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Shaman_Position:
                direction = packet.readBoolean()
                gift.client.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(gift.client.playerCode).writeBoolean(direction).toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Crouch:
                crouch = packet.readByte()
                gift.client.room.sendAll(Identifiers.send.Crouch, ByteArray().writeInt(gift.client.playerCode).writeByte(crouch).writeByte(0).toByteArray())
                return

        elif C == Identifiers.recv.Room.C:
            if CC == Identifiers.recv.Room.Map_26:
                if gift.client.room.currentMap == 26:
                    posX, posY, width, height = packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort()

                    bodyDef = {}
                    bodyDef["type"] = 12
                    bodyDef["width"] = width
                    bodyDef["height"] = height
                    gift.client.room.addPhysicObject(0, posX, posY, bodyDef)
                return

            elif CC == Identifiers.recv.Room.Shaman_Message:
                type, x, y = packet.readByte(), packet.readShort(), packet.readShort()
                gift.client.room.sendAll(Identifiers.send.Shaman_Message, ByteArray().writeByte(type).writeShort(x).writeShort(y).toByteArray())
                return

            elif CC == Identifiers.recv.Room.Convert_Skill:
                objectID = packet.readInt()
                gift.client.parseSkill.sendConvertSkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Demolition_Skill:
                objectID = packet.readInt()
                gift.client.parseSkill.sendDemolitionSkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Projection_Skill:
                posX, posY, dir = packet.readShort(), packet.readShort(), packet.readShort()
                gift.client.parseSkill.sendProjectionSkill(posX, posY, dir)
                return

            elif CC == Identifiers.recv.Room.Enter_Hole:
                holeType, roundCode, monde, distance, holeX, holeY = packet.readByte(), packet.readInt(), packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort()
                if roundCode == gift.client.room.lastRoundCode and (gift.client.room.currentMap == -1 or monde == gift.client.room.currentMap or gift.client.room.EMapCode != 0):
                    gift.client.playerWin(holeType, distance)
                return

            elif CC == Identifiers.recv.Room.Get_Cheese:
                roundCode, cheeseX, cheeseY, distance = packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort()
                if roundCode == gift.client.room.lastRoundCode:
                    gift.client.sendGiveCheese(distance)
                return

            elif CC == Identifiers.recv.Room.Place_Object:
                if not gift.client.isShaman:
                    return

                roundCode, objectID, code, px, py, angle, vx, vy, dur, origin = packet.readByte(), packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readByte(), packet.readByte(), packet.readBoolean(), packet.readBoolean()
                if gift.client.room.isTotemEditor:
                    if gift.client.tempTotem[0] < 20:
                        gift.client.tempTotem[0] = int(gift.client.tempTotem[0]) + 1
                        gift.client.sendTotemItemCount(gift.client.tempTotem[0])
                        gift.client.tempTotem[1] += "#2#" + chr(1).join(map(str, [code, px, py, angle, vx, vy, dur]))
                else:
                    if code == 44:
                        if not gift.client.useTotem:
                            gift.client.sendTotem(gift.client.totem[1], px, py, gift.client.playerCode)
                            gift.client.useTotem = True

                    gift.client.sendPlaceObject(objectID, code, px, py, angle, vx, vy, dur, False)
                    gift.client.parseSkill.placeSkill(objectID, code, px, py, angle)
                return

            elif CC == Identifiers.recv.Room.Ice_Cube:
                playerCode, px, py = packet.readInt(), packet.readShort(), packet.readShort()
                if gift.client.isShaman and not gift.client.isDead and not gift.client.room.isSurvivor and gift.client.room.numCompleted > 1:
                    if gift.client.iceCount != 0 and playerCode != gift.client.playerCode:
                        for player in gift.client.room.clients.values():
                            if player.playerCode == playerCode and not player.isShaman:
                                player.isDead = True
                                if not gift.client.room.noAutoScore: gift.client.playerScore += 1
                                player.sendPlayerDied()
                                gift.client.sendPlaceObject(gift.client.room.objectID + 2, 54, px, py, 0, 0, 0, True, True)
                                gift.client.iceCount -= 1
                                gift.client.room.checkChangeMap()
                return

            elif CC == Identifiers.recv.Room.Bridge_Break:
                if gift.client.room.currentMap in [6, 10, 110, 116]:
                    bridgeCode = packet.readShort()
                    gift.client.room.sendAllOthers(gift.client, Identifiers.send.Bridge_Break, ByteArray().writeShort(bridgeCode).toByteArray())
                return

            elif CC == Identifiers.recv.Room.Defilante_Points:
                gift.client.defilantePoints += 1
                return

            elif CC == Identifiers.recv.Room.Restorative_Skill:
                objectID, id = packet.readInt(), packet.readInt()
                gift.client.parseSkill.sendRestorativeSkill(objectID, id)
                return

            elif CC == Identifiers.recv.Room.Recycling_Skill:
                id = packet.readShort()
                gift.client.parseSkill.sendRecyclingSkill(id)
                return

            elif CC == Identifiers.recv.Room.Gravitational_Skill:
                velX, velY = packet.readShort(), packet.readShort()
                gift.client.parseSkill.sendGravitationalSkill(0, velX, velY)
                return

            elif CC == Identifiers.recv.Room.Antigravity_Skill:
                objectID = packet.readInt()
                gift.client.parseSkill.sendAntigravitySkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Handymouse_Skill:
                handyMouseByte, objectID = packet.readByte(), packet.readInt()
                if gift.client.room.lastHandymouse[0] == -1:
                    gift.client.room.lastHandymouse = [objectID, handyMouseByte]
                else:
                    gift.client.parseSkill.sendHandymouseSkill(handyMouseByte, objectID)
                    gift.client.room.sendAll(Identifiers.send.Skill, chr(77) + chr(1))
                    gift.client.room.lastHandymouse = [-1, -1]
                return

            elif CC == Identifiers.recv.Room.Enter_Room:
                community, roomName, isSalonAuto = packet.readByte(), packet.readUTF(), packet.readBoolean()
                if isSalonAuto or roomName == "":
                    gift.client.startBulle(gift.server.recommendRoom(gift.client.langue))
                elif not roomName == gift.client.roomName or not gift.client.room.isEditor or not len(roomName) > 64 or not gift.client.roomName == "%s-%s" %(gift.client.langue, roomName):
                    if gift.client.privLevel < 8: roomName = gift.server.checkRoom(roomName, gift.client.langue)
                    roomEnter = gift.server.rooms.get(roomName if roomName.startswith("*") else ("%s-%s" %(gift.client.langue, roomName)))
                    if roomEnter == None or gift.client.privLevel >= 7:
                        gift.client.startBulle(roomName)
                    else:
                        if not roomEnter.roomPassword == "":
                            gift.client.sendPacket(Identifiers.send.Room_Password, ByteArray().writeUTF(roomName).toByteArray())
                        else:
                            gift.client.startBulle(roomName)
                return

            elif CC == Identifiers.recv.Room.Room_Password:
                roomPass, roomName = packet.readUTF(), packet.readUTF()
                roomEnter = gift.server.rooms.get(roomName if roomName.startswith("*") else ("%s-%s" %(gift.client.langue, roomName)))
                if roomEnter == None or gift.client.privLevel >= 7:
                    gift.client.startBulle(roomName)
                else:
                    if not roomEnter.roomPassword == roomPass:
                        gift.client.sendPacket(Identifiers.send.Room_Password, ByteArray().writeUTF(roomName).toByteArray())
                    else:
                        gift.client.startBulle(roomName)
                return

            elif CC == Identifiers.recv.Room.Send_Music:
                url = packet.readUTF()
                id = Utils.getYoutubeID(url)
                if (id == None):
                    gift.client.sendLangueMessage("", "$ModeMusic_ErreurVideo")
                else:
                    myUrl = urllib.urlopen("https://www.googleapis.com/youtube/v3/videos?id=" + id + "&key=AIzaSyDQ7jD1wcD5A_GeV4NfZqWJswtLplPDr74&part=snippet,contentDetails")
                    data = json.loads(myUrl.read())
                    if data["pageInfo"]["totalResults"] == 0:
                        gift.client.sendLangueMessage("", "$ModeMusic_ErreurVideo")
                    else:
                        duration = Utils.Duration(data["items"][0]["contentDetails"]["duration"])
                        duration = 300 if duration > 300 else duration
                        title = data["items"][0]["snippet"]["title"]
                        if (filter(lambda music: music["By"] == (gift.client.playerName), gift.client.room.musicVideos)):
                            gift.client.sendLangueMessage("", "$ModeMusic_VideoEnAttente")
                        elif (filter(lambda music: music["Title"] == (title), gift.client.room.musicVideos)):
                            gift.client.sendLangueMessage("", "$DejaPlaylist");
                        else:
                            gift.client.sendLangueMessage("", "$ModeMusic_AjoutVideo", str(len(gift.client.room.musicVideos) + 1))
                            values = {}
                            values["By"] = gift.client.playerName
                            values["Title"] = title
                            values["Duration"] = str(duration)
                            values["VideoID"] = id
                            gift.client.room.musicVideos.append(values)
                            if (len(gift.client.room.musicVideos) == 1):
                                gift.client.sendMusicVideo(True)
                                gift.client.room.isPlayingMusic = True
                                gift.client.room.musicSkipVotes = 0

                    return

            elif CC == Identifiers.recv.Room.Send_PlayList:
                packet = ByteArray().writeShort(len(gift.client.room.musicVideos))
                for music in gift.client.room.musicVideos:
                    packet.writeUTF(music["Title"]).writeUTF(music["By"])
                gift.client.sendPacket(Identifiers.send.Music_PlayList, packet.toByteArray())
                return

            elif CC == Identifiers.recv.Room.Music_Time:
                time = packet.readInt()
                if len(gift.client.room.musicVideos) > 0:
                    gift.client.room.musicTime = time
                    duration = gift.client.room.musicVideos[0]["Duration"]
                    if time >= int(duration) - 5 and gift.client.room.canChangeMusic:
                        gift.client.room.canChangeMusic = False
                        del gift.client.room.musicVideos[0]
                        gift.client.room.musicTime = 1
                        if len(gift.client.room.musicVideos) >= 1:
                            gift.client.sendMusicVideo(True)
                        else:
                            gift.client.room.isPlayingMusic = False
                            gift.client.room.musicTime = 0
                return
            
        elif C == Identifiers.recv.Others.C:
            if CC == Identifiers.recv.Others.Daily_Quest_Open:
                gift.client.DailyQuest.sendDailyQuest()
                return

            elif CC == Identifiers.recv.Others.Daily_Quest_Change:
                missionID = packet.readShort()
                gift.client.DailyQuest.changeMission(int(missionID), int(gift.client.playerID))
                gift.client.DailyQuest.sendDailyQuest()
                return
            

        elif C == Identifiers.recv.Chat.C:
            if CC == Identifiers.recv.Chat.Chat_Message:
                #packet = gift.descriptPacket(packetID, packet)
                message = packet.readUTF().replace("&amp;#", "&#").replace("<", "&lt;")
                message = message.replace("|", "").replace("  ", "").replace("&nbsp;", "").replace("\n", "").replace("<br>", "").replace("<br/>", "").replace("</br>", "")
##                if gift.client.cheeseCount > 3:
                if message in ["\n"] or message in ["\r"] or message in ["\x02"] or message in ["<BR>"]:
                    if message in ["\n", "\r"]:
                        gift.client.sendServerMessageAdmin("[<V>BOT</V>][<font color='#CBF722'>%s</J>][<V>%s</V>] suspicious bot players." %(gift.client.ipAddress, gift.client.playerName))
                    gift.client.transport.loseConnection()
                if gift.client.privLevel not in [11, 10, 9, 8, 7, 6, 5, 2]:
                    if "micee" in message or "mice" in message or "mi ce" in message or "m i c e" in message or "m ice" in message or "mic e" in message or "mice" in message:
##                        gift.client.sendMessage("[<V>BOT</V>] Ooops <font color='#CBF722'>%s</J>, Dikkatli olmalısın! <R>Bu paylaştığınız url size aitse cezalandırılacaksınız. " %(gift.client.playerName))
                        gift.client.sendServerMessageAdmin("[<V>CM</V>][<J>%s</J>][<V>%s</V>] Suspicious actress typed: [<R>%s</R>]" %(gift.client.ipAddress, gift.client.playerName, message))
                        message = ""
                    if message == gift.client.lastMessage and gift.client.privLevel < 6:
                        message = ""
                if gift.client.isGuest:
                    gift.client.sendLangueMessage("", "$Créer_Compte_Parler")
                elif not message == "" and len(message) < 256:
                    if gift.client.isMute:
                        muteInfo = gift.server.getModMuteInfo(gift.client.playerName)
                        timeCalc = Utils.getHoursDiff(muteInfo[1])          
                        if timeCalc <= 0:
                            gift.client.isMute = False
                            gift.server.removeModMute(gift.client.playerName)
                            gift.client.room.sendAllChat(gift.client.playerCode, gift.client.playerName, message, gift.client.langueID, gift.server.checkMessage(gift.client, message))
                        else:
                            gift.client.sendModMute(gift.client.playerName, timeCalc, muteInfo[0], True)
                            return
                    else:
                        if gift.client.room.isUtility == True:
                            gift.client.Utility.isCommand = False
                            if message.startswith("!"):
                                gift.client.Utility.sentCommand(message)
                            if gift.client.Utility.isCommand == True:
                                message = ""    
                        if not gift.client.chatdisabled:
                            if not message == gift.client.lastMessage:
                                gift.client.lastMessage = message
                                gift.client.room.sendAllChat(gift.client.playerCode, gift.client.playerName, message, gift.client.langueID, gift.server.checkMessage(gift.client, message))
                                reactor.callLater(0.9, gift.client.chatEnable)
                                gift.client.chatdisabled = True
                            else:
                                gift.client.sendLangueMessage("", "$Message_Identique")
                        else:
                            gift.client.sendLangueMessage("", "$Doucement")  

                    if not gift.server.chatMessages.has_key(gift.client.playerName):
                        messages = deque([], 60)
                        messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                        gift.server.chatMessages[gift.client.playerName] = messages
                    else:
                        gift.server.chatMessages[gift.client.playerName].append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                return
##                else:
##                    gift.client.sendMessage("<ROSE>You need 3 cheeses to speak.")

            elif CC == Identifiers.recv.Chat.Staff_Chat:
                type, message = packet.readByte(), packet.readUTF()
                if gift.client.privLevel >= (3 if type == 8 else 4 if type == 9 else 5 if type == 2 or type == 5 else 6 if type == 7 or type == 6 else 7 if type == 0 or type == 4 or type == 3 else 8 if type == 1 else 10):
                    gift.client.sendAllModerationChat(type, message)
                return
 
                
            
##            elif CC == Identifiers.recv.Chat.Staff_Chat:
##                type, message = packet.readByte(), packet.readUTF()
##                if gift.client.privLevel >= (6 if type == 6 else 7 if type == 0 or type == 4 or type == 3 else 8 if type == 1 else 10):
##                    gift.client.sendAllModerationChat(type, mesage)
##                if gift.client.privLevel == (3 if type == 8 else 4 if type == 9 else 6 if type == 7 else 5 if type == 2 or type == 5 else 10 or 11):
##                    gift.client.sendAllModerationChat(type, message)
##                return

            elif CC == Identifiers.recv.Chat.Commands:
                #packet = gift.descriptPacket(packetID, packet)
                command = packet.readUTF()
                try:
                    if _time.time() - gift.client.CMDTime > 1:
                        gift.client.parseCommands.parseCommand(command)
                        gift.client.parseCodeCmd.parseCommandCode(command)
                        #if gift.client.playerName == "Loveditoi":
                            #gift.client.sendLuaMessageAdmin("<BL>~ <VP>[<FC>COMMAND<VP>] <BV>%s <R>typed <BL>/<J>%s" %(gift.client.playerName, command))
                        gift.client.CMDTime = _time.time()
                except Exception as e:
                    with open("./include/MErros.log", "a") as f:
                        traceback.print_exc(file=f)
                        f.write("\n")
                return

        elif C == Identifiers.recv.Player.C:
            if CC == Identifiers.recv.Player.Emote:
                emoteID, playerCode = packet.readByte(), packet.readInt()
                flag = packet.readUTF() if emoteID == 10 else ""
                gift.client.sendPlayerEmote(emoteID, flag, True, False)
                if playerCode != -1:
                    if emoteID == 14:
                        gift.client.sendPlayerEmote(14, flag, False, False)
                        gift.client.sendPlayerEmote(15, flag, False, False)
                        player = filter(lambda p: p.playerCode == playerCode, gift.server.players.values())[0]
                        if player != None:
                            player.sendPlayerEmote(14, flag, False, False)
                            player.sendPlayerEmote(15, flag, False, False)

                    elif emoteID == 18:
                        gift.client.sendPlayerEmote(18, flag, False, False)
                        gift.client.sendPlayerEmote(19, flag, False, False)
                        player = filter(lambda p: p.playerCode == playerCode, gift.server.players.values())[0]
                        if player != None:
                            player.sendPlayerEmote(17, flag, False, False)
                            player.sendPlayerEmote(19, flag, False, False)

                    elif emoteID == 22:
                        gift.client.sendPlayerEmote(22, flag, False, False)
                        gift.client.sendPlayerEmote(23, flag, False, False)
                        player = filter(lambda p: p.playerCode == playerCode, gift.server.players.values())[0]
                        if player != None:
                            player.sendPlayerEmote(22, flag, False, False)
                            player.sendPlayerEmote(23, flag, False, False)

                    elif emoteID == 26:
                        gift.client.sendPlayerEmote(26, flag, False, False)
                        gift.client.sendPlayerEmote(27, flag, False, False)
                        player = filter(lambda p: p.playerCode == playerCode, gift.server.players.values())[0]
                        if player != None:
                            player.sendPlayerEmote(26, flag, False, False)
                            player.sendPlayerEmote(27, flag, False, False)
                            gift.client.room.sendAll(Identifiers.send.Joquempo, ByteArray().writeInt(gift.client.playerCode).writeByte(random.randint(0, 2)).writeInt(player.playerCode).writeByte(random.randint(0, 2)).toByteArray())

                if gift.client.isShaman:
                    gift.client.parseSkill.parseEmoteSkill(emoteID)
                return
                    
            elif CC == Identifiers.recv.Player.Langue:
                gift.client.langueID = packet.readByte()
                langue = Utils.getTFMLangues(gift.client.langueID)
                gift.client.langue = langue
                return

            elif CC == Identifiers.recv.Player.Emotions:
                emotion = packet.readByte()
                gift.client.sendEmotion(emotion)
                return

            elif CC == Identifiers.recv.Player.Shaman_Fly:
                fly = packet.readBoolean()
                gift.client.parseSkill.sendShamanFly(fly)
                return

            elif CC == Identifiers.recv.Player.Shop_List:
                gift.client.parseShop.sendShopList()
                return

            elif CC == Identifiers.recv.Player.Buy_Skill:
                skill = packet.readByte()
                gift.client.parseSkill.buySkill(skill)
                return

            elif CC == Identifiers.recv.Player.Redistribute:
                gift.client.parseSkill.redistributeSkills()
                return

            elif CC == Identifiers.recv.Player.Report:
                playerName, type, comments = packet.readUTF(), packet.readByte(), packet.readUTF()
                gift.client.modoPwet.makeReport(playerName, type, comments)
                return

            elif CC == Identifiers.recv.Player.Ping:
                if (_time.time() - gift.client.PInfo[1]) >= 5:
                    gift.client.PInfo[1] = _time.time()
                    gift.client.sendPacket(Identifiers.send.Ping, gift.client.PInfo[0])
                    gift.client.PInfo[0] += 1
                    if gift.client.PInfo[0] == 31:
                        gift.client.PInfo[0] = 0
                return

            
            
            elif CC == Identifiers.recv.Player.Meep:
                posX, posY = packet.readShort(), packet.readShort()
                gift.client.room.sendAll(Identifiers.send.Meep_IMG, ByteArray().writeInt(gift.client.playerCode).toByteArray())
                gift.client.room.sendAll(Identifiers.send.Meep, ByteArray().writeInt(gift.client.playerCode).writeShort(posX).writeShort(posY).writeInt(10 if gift.client.isShaman else 5).toByteArray())
                return

            elif CC == Identifiers.recv.Player.Bolos:
                #print repr(packet.toByteArray())
                sla, sla2, id, type = packet.readByte(), packet.readByte(), packet.readByte(), packet.readByte()
                #print("ID: "+str(id)+ ", ID da aventura: "+str(sla2)+ ", Sla: "+str(sla))
                #.client.winEventMap()
                if not gift.client.hasBolo:
                    p = ByteArray()
                    p.writeByte(52)
                    p.writeByte(1)
                    p.writeByte(2)
                    p.writeUTF(str(gift.client.playerCode))
                    p.writeUTF(str(id))
                    gift.client.room.sendAll([16, 10], p.toByteArray())
                    gift.client.room.sendAll([100, 101], ByteArray().writeByte(2).writeInt(gift.client.playerCode).writeUTF("x_transformice/x_aventure/x_recoltables/x_"+str((1 if id == 1 else 0))+".png").writeInt(-1900574).writeByte(0).writeShort(100).writeShort(0).toByteArray())
                    gift.client.sendPacket([100, 101], "\x01\x01")
                    #gift.client.room.sendAll([5, 53], ByteArray().writeByte(type).writeShort(id).toByteArray())
                    #gift.client.room.sendAll([100, 101], ByteArray().writeByte(2).writeInt(gift.client.playerCode).writeUTF("x_transformice/x_aventure/x_recoltables/x_"+1 if gift.server.adventureID == 52 else 0+".png").writeInt(-1900574).writeByte(0).writeShort(100).writeShort(0).toByteArray())
                    #gift.client.sendPacket([100, 101], "\x01\x00")
                    gift.client.hasBolo = True
                    if not gift.client.isGuest:
                        if id == 1:
                            gift.client.giftGet = True
                return

            elif CC == Identifiers.recv.Player.Vampire:
                if gift.client.room.isSurvivor:
                    gift.client.sendVampireMode(True)
                return

        elif CC == Identifiers.recv.Player.Calendar:
                pass
                return

        elif C == Identifiers.recv.Buy_Fraises.C:
            if CC == Identifiers.recv.Buy_Fraises.Buy_Fraises:
                return

        elif C == Identifiers.recv.Tribe.C:
            if CC == Identifiers.recv.Tribe.Tribe_House:
                if not gift.client.tribeName == "":
                    gift.client.startBulle("*\x03%s" %(gift.client.tribeName))
                return

            elif CC == Identifiers.recv.Tribe.Tribe_Invite:
                playerName = packet.readUTF()
                player = gift.server.players.get(playerName)
                if player != None and player.tribeName in gift.client.invitedTribeHouses:
                    if gift.server.rooms.get("*%s%s" %(chr(3), player.tribeName)) != None:
                        if gift.client.room.roomName != "*%s%s" %(chr(3), player.tribeName):
                            gift.client.startBulle("*%s%s" %(chr(3), player.tribeName))
                    else:
                        player.sendLangueMessage("", "$InvTribu_MaisonVide")
                return

            elif CC == Identifiers.recv.Tribe.Bot_Bolo:
                pass
                return

        elif C == Identifiers.recv.Shop.C:
            if CC == Identifiers.recv.Shop.Equip_Clothe:
                gift.client.parseShop.equipClothe(packet)
                return

            elif CC == Identifiers.recv.Shop.Save_Clothe:
                gift.client.parseShop.saveClothe(packet)
                return
            
            elif CC == Identifiers.recv.Shop.Info:
                gift.client.parseShop.sendShopInfo()
                return

            elif CC == Identifiers.recv.Shop.Equip_Item:
                gift.client.parseShop.equipItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Item:
                gift.client.parseShop.buyItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Custom:
                gift.client.parseShop.customItemBuy(packet)
                return

            elif CC == Identifiers.recv.Shop.Custom_Item:
                gift.client.parseShop.customItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Clothe:
                gift.client.parseShop.buyClothe(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Visu_Done:
                p = ByteArray(packet.toByteArray())
                visuID = p.readShort()
                lookBuy = p.readUTF()
                look = gift.server.newVisuList[visuID].split(";")
                look[0] = int(look[0])
                count = 0
                if gift.client.shopFraises >= gift.client.priceDoneVisu:
                    for visual in look[1].split(","):
                        if not visual == "0":
                            item, customID = visual.split("_", 1) if "_" in visual else [visual, ""]
                            item = int(item)
                            itemID = gift.client.getFullItemID(count, item)
                            itemInfo = gift.client.getItemInfo(count, item)
                            if len(gift.client.shopItems) == 1:
                                if not gift.client.parseShop.checkInShop(itemID):
                                    gift.client.shopItems += str(itemID)+"_" if gift.client.shopItems == "" else "," + str(itemID)+"_"
                                    if not itemID in gift.client.custom:
                                        gift.client.custom.append(itemID)
                                    else:
                                        if not str(itemID) in gift.client.custom:
                                            gift.client.custom.append(str(itemID))
                            else:
                                if not gift.client.parseShop.checkInShop(str(itemID)):
                                    gift.client.shopItems += str(itemID)+"_" if gift.client.shopItems == "" else "," + str(itemID)+"_"
                                    if not itemID in gift.client.custom:
                                        gift.client.custom.append(itemID)
                                    else:
                                        if not str(itemID) in gift.client.custom:
                                            gift.client.custom.append(str(itemID))
                        count += 1
                        
                    gift.client.clothes.append("%02d/%s/%s/%s" %(len(gift.client.clothes), lookBuy, "78583a", "fade55" if gift.client.shamanSaves >= 1000 else "95d9d6"))
                    furID = gift.client.getFullItemID(22, look[0])
                    gift.client.shopItems += str(furID) if gift.client.shopItems == "" else "," + str(furID)
                    gift.client.shopFraises -= gift.client.priceDoneVisu
                    gift.client.visuDone.append(lookBuy)
                else:
                    gift.sendMessage("<Vous n'avez pas assez de fraises.")
                gift.client.parseShop.sendShopList(False)

            elif CC == Identifiers.recv.Shop.Buy_Shaman_Item:
                gift.client.parseShop.buyShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Equip_Shaman_Item:
                gift.client.parseShop.equipShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Shaman_Custom:
                gift.client.parseShop.customShamanItemBuy(packet)
                return

            elif CC == Identifiers.recv.Shop.Custom_Shaman_Item:
                gift.client.parseShop.customShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Send_Gift:
                gift.client.parseShop.sendGift(packet)
                return

            elif CC == Identifiers.recv.Shop.Gift_Result:
                gift.client.parseShop.giftResult(packet)
                return

        elif C == Identifiers.recv.Modopwet.C:
            if CC == Identifiers.recv.Modopwet.Modopwet:
                if gift.client.privLevel >= 7:
                    isOpen = packet.readBoolean()
                    # if isOpen:
                        # gift.client.modoPwet.openModoPwet(True)
                        # change_langue bolumunde acılıyor.
                        
                    gift.client.isModoPwet = isOpen    
                return

            elif CC == Identifiers.recv.Modopwet.Delete_Report:
                if gift.client.privLevel >= 7:
                    playerName, closeType = packet.readUTF(), packet.readByte()
                    gift.client.modoPwet.deleteReport(playerName,int(closeType))
                return

            elif CC == Identifiers.recv.Modopwet.Watch:
                if gift.client.privLevel >= 7:
                    playerName = packet.readUTF()
                    if not gift.client.playerName == playerName:
                        roomName = gift.server.players[playerName].roomName if gift.server.players.has_key(playerName) else ""
                        if not roomName == "" and not roomName == gift.client.roomName and not "[Editeur]" in roomName and not "[Totem]" in roomName:
                            gift.client.startBulle(roomName)
                return

            elif CC == Identifiers.recv.Modopwet.Ban_Hack:
                if gift.client.privLevel >= 7:
                    playerName, iban = packet.readUTF(), packet.readBoolean()
                    gift.client.modoPwet.banHack(playerName,iban)
                return

            elif CC == Identifiers.recv.Modopwet.Change_Langue:
                if gift.client.privLevel >= 7:
                    langue,modopwetOnlyPlayerReports,sortBy = packet.readUTF(),packet.readBoolean(),packet.readBoolean()
                    gift.client.modoPwetLangue = langue.upper()
                    gift.client.modoPwet.openModoPwet(gift.client.isModoPwet,modopwetOnlyPlayerReports,sortBy)
                return
                
            elif CC == Identifiers.recv.Modopwet.Modopwet_Notifications:
                if gift.client.privLevel >= 7:
                    isTrue = packet.readBoolean()
                    gift.client.isModoPwetNotifications = isTrue  
                return    
                
            elif CC == Identifiers.recv.Modopwet.Chat_Log:
                if gift.client.privLevel >= 7:
                    playerName = packet.readUTF()
                    gift.client.modoPwet.openChatLog(playerName)
                return


        elif C == Identifiers.recv.Login.C:
            if CC == Identifiers.recv.Login.Create_Account:
                #packet = gift.descriptPacket(packetID, packet)
                playerName, password, email, captcha, url, test = Utils.parsePlayerName(packet.readUTF()), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readUTF()
            
                if gift.client.checkTimeAccount():
                    
                    canLogin = False
                    for urlCheck in gift.server.serverURL:
                        if url.startswith(urlCheck):
                            canLogin = True
                            break

                    if not canLogin:
                        gift.server.sendStaffMessage(7, "[<V>URL</V>][<J>%s</J>][<V>%s</V>][<R>%s</R>] Invalid login url." %(gift.client.ipAddress, playerName, url))
                        gift.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Accéder au site: %s" %(gift.server.serverURL[0])])
                        gift.client.transport.loseConnection()
                        return


                    elif gift.server.checkExistingUser(playerName):
                        gift.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(3).writeUTF(playerName).writeUTF("").toByteArray())
                    elif not re.match("^(?=^(?:(?!.*_$).)*$)(?=^(?:(?!_{2,}).)*$)[A-Za-z][A-Za-z0-9_]{2,11}$", playerName):
                        gift.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(5).writeUTF("").writeUTF("").toByteArray())
                    elif not gift.client.currentCaptcha == captcha:
                        gift.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(7).writeUTF("").writeUTF("").toByteArray())
                    else:
                        #tag = "0000"
                        #while gift.server.checkExistingUser(playerName + "#" + tag):
                            #tag = "".join([str(random.choice(range(9))) for x in range(4)])
                        #playerName += "#" + tag
                        gift.client.sendAccountTime()
                        gift.server.lastPlayerID += 1
                        gift.Cursor.execute("insert into users values (%s, %s, %s, 1, 0, 10000, 15000, 5000, %s, %s, 20000, 10000, 10000, 5000, 0, '', '', '', '1;0,0,0,0,0,0,0,0,0,0,0', '0,0,0,0,0,0,0,0,0,0', '78583a', '95d9d6', %s, '{}', '', '', '', '', '', '', '', '', 0, 100, 0, 100, '', 0, '', '', 0, 0, '', 0, 0, 0, '', '', '0,0,0,0', '0,0,0,0', '23:10;2252:5;2256:5;2349:5;2379:5', '23', 0, 0, '', 0, 0, 0, '', '', '', 0, 0, '2,8,0,0,0,189,133,0,0', 0, %s, '0#0#0#0#0#0', '', '', '', '24:0', 0, 'xx', '0.jpg', 1, '', 0, 0, 0, '', 0, 1, %s, '', 1, '', 0, 0, 'Little Mouse', 0,0)", [playerName, password, gift.server.lastPlayerID, gift.server.initialCheeses, gift.server.initialFraises, Utils.getTime(), gift.client.langue, email])
                        gift.Cursor.execute("insert into DailyQuest values (%s, '237129', '0', '20', '0', '20', '1')", [gift.server.lastPlayerID])
                        gift.client.loginPlayer(playerName, password, "\x03[Tutorial] %s" %(playerName))
                        gift.client.sendNewConsumable(23, 10)
                        gift.client.sendNewConsumable(2252, 5)
                        gift.client.sendNewConsumable(2256, 5)
                        gift.client.sendNewConsumable(2349, 5)
                        gift.client.sendNewConsumable(2379, 5)
                        gift.client.sendServerMessageAdmin("• [<J>%s</J>] [<J>%s</J>] <V>%s</V> vient de créé un compte." %(gift.client.langue, gift.client.ipAddress, playerName))
                        gift.server.updateConfig()
                        if "?id=" in url:
                            link = url.split("?id=")
                            gift.Cursor.execute("select IP from loginlog where Username = %s", [gift.server.getPlayerName(int(link[1]))])
                            ipPlayer = gift.Cursor.fetchone()[0]
                            gift.Cursor.execute("select Password from users where Password = %s", [password])
                            passProtection = gift.Cursor.fetchone()[0]
                            if ipPlayer is None and passProtection is None:
                                player = gift.server.players.get(gift.server.getPlayerName(int(link[1])))
                                if player != None:
                                    player.cheeseCount += 10
                                    player.firstCount += 10
                                    player.shopCheeses += 2000
                                    player.shopFraises += 2000
                                    player.nowCoins += 15
                                    player.sendMessage("<CH>Félicitations! ", True)
                                else:
                                    gift.Cursor.execute("update users set CheeseCount = CheeseCount + 10, FirstCount = FirstCount + 10, ShopCheeses = ShopCheeses + 2000, ShopFraises = ShopFraises + 2000, Coins = Coins + 15 where Username = %s", [gift.server.getPlayerName(int(link[1]))])
                    return
                else:
                    gift.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(5).writeByte(0).writeByte(0).writeUTF(playerName).toByteArray())


            elif CC == Identifiers.recv.Login.Login:
                #packet = gift.descriptPacket(packetID, packet)
                playerName, password, url, startRoom, resultKey, byte = Utils.parsePlayerName(packet.readUTF()), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readInt(), packet.readByte()
                #authKey = gift.client.authKey
                #print(url)

                if not len(gift.client.playerName) == 0:
                    gift.server.sendStaffMessage(7, "[<V>ANTI-BOT</V>][<J>%s</J>][<V>%s</V>] a essayé de se connecter avec plusieurs comptes." %(gift.client.ipAddress, gift.client.playerName))
                    gift.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "A essayé de se connecter avec plusieurs comptes."])
                    gift.client.transport.loseConnection()
                    return
                elif playerName == "" and not password == "":
                    gift.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF(playerName).writeUTF("").toByteArray())
                else:
                    gift.client.loginPlayer(playerName, password, startRoom)
                #else:
                #gift.server.sendStaffMessage(7, "[<V>ANTI-BOT</V>][<J>%s</J>][<V>%s</V>] Invalid login auth key." %(gift.client.ipAddress, playerName))
                #gift.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Invalid login auth key."])
                #gift.client.transport.loseConnection()
                    return

            elif CC == Identifiers.recv.Login.Player_FPS:
                return

            elif CC == Identifiers.recv.Login.Captcha:
                if _time.time() - gift.client.CAPTime > 2:
                    gift.client.currentCaptcha, px, ly, lines = gift.server.buildCaptchaCode()
                    packet = ByteArray().writeShort(px).writeShort(ly).writeShort((px * ly))
                    for line in lines:
                        packet.writeBytes("\x00" * 4)
                        for value in line.split(","):
                            packet.writeUnsignedByte(value).writeBytes("\x00" * 3)
                        packet.writeBytes("\x00" * 4)
                    packet.writeBytes("\x00" * (((px * ly) - (packet.getLength() - 6) / 4) * 4))
                    gift.client.sendPacket(Identifiers.send.Captcha, packet.toByteArray())
                    gift.client.CAPTime = _time.time()
                return

            elif CC == Identifiers.recv.Login.Dummy:
                if gift.client.awakeTimer.getTime() - _time.time() < 110.0:
                    gift.client.awakeTimer.reset(120)
                return

            elif CC == Identifiers.recv.Login.Player_Info:
                return
            elif CC == Identifiers.recv.Login.Player_Info2:
                return

            elif CC == Identifiers.recv.Login.Temps_Client:
                return

            elif CC == Identifiers.recv.Login.Rooms_List:
                mode = packet.readByte()
                gift.client.lastGameMode = mode
                gift.client.sendGameMode(mode)
                return

            elif CC == Identifiers.recv.Login.Undefined:
                return

        elif C == Identifiers.recv.Transformation.C:
            if CC == Identifiers.recv.Transformation.Transformation_Object:
                objectID = packet.readShort()
                if not gift.client.isDead and gift.client.room.currentMap in range(200, 211):
                    gift.client.room.sendAll(Identifiers.send.Transformation, ByteArray().writeInt(gift.client.playerCode).writeShort(objectID).toByteArray())
                return

        elif C == Identifiers.recv.Informations.C:
            if CC == Identifiers.recv.Informations.Game_Log:
                errorC, errorCC, oldC, oldCC, error = packet.readByte(), packet.readByte(), packet.readUnsignedByte(), packet.readUnsignedByte(), packet.readUTF()
                if gift.server.isDebug:
                    if errorC == 1 and errorCC == 1:
                        print "[%s] [%s][OLD] GameLog Error - C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), gift.client.playerName, oldC, oldCC, error)
                    elif errorC == 60 and errorCC == 1:
                        if oldC == Identifiers.tribulle.send.ET_SignaleDepartMembre or oldC == Identifiers.tribulle.send.ET_SignaleExclusion: return
                        print "[%s] [%s][TRIBULLE] GameLog Error - Code: %s error: %s" %(_time.strftime("%H:%M:%S"), gift.client.playerName, oldC, error)
                    else:
                        print "[%s] [%s] GameLog Error - C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), gift.client.playerName, errorC, errorCC, error)
                return

            elif CC == Identifiers.recv.Informations.Player_Ping:
                try:
                    VC = (ord(packet.toByteArray()) + 1)
                    if gift.client.PInfo[0] == VC:
                        gift.client.PInfo[2] = int((_time.time() - gift.client.PInfo[1]) * 1000)
                except: pass
                return


            elif CC == Identifiers.recv.Informations.Change_Shaman_Type:
                type = packet.readByte()
                gift.client.shamanType = type
                gift.client.sendShamanType(type, (gift.client.shamanSaves >= 100 and gift.client.hardModeSaves >= 150))
                return

            elif CC == Identifiers.recv.Informations.Letter:
                playerName = Utils.parsePlayerName(packet.readUTF())[:-5]
                type = packet.readByte()
                letter = packet.readUTFBytes(packet.getLength())
                idler = {0:29,1:30,2:2241,3:2330,4:2351}
                
                if gift.server.checkExistingUser(playerName):
                    id = idler[type]
                    count = gift.client.playerConsumables[id]
                    if count > 0:
                        count -= 1
                        gift.client.playerConsumables[id] -= 1
                        if count == 0:
                            del gift.client.playerConsumables[id]
                            if gift.client.equipedConsumables:
                                for id in gift.client.equipedConsumables:
                                    if not id:
                                        gift.client.equipedConsumables.remove(id)
                                None
                                if id in gift.client.equipedConsumables:
                                    gift.client.equipedConsumables.remove(id)

                    gift.client.updateInventoryConsumable(id, count)
                    gift.client.useInventoryConsumable(id)
                    
                    player = gift.server.players.get(playerName)
                    if (player != None): 
                        p = ByteArray()
                        p.writeUTF(gift.client.playerName)
                        p.writeUTF(gift.client.playerLook)
                        p.writeByte(type)
                        p.writeBytes(letter)
                        player.sendPacket(Identifiers.send.Letter, p.toByteArray())
                        gift.client.sendLangueMessage("", "$MessageEnvoye")
                    else:
                        gift.client.sendLangueMessage("", "$Joueur_Existe_Pas")
                else: 
                    gift.client.sendLangueMessage("", "$Joueur_Existe_Pas")
                
                return

            elif CC == Identifiers.recv.Informations.Letter:
                return

            elif CC == Identifiers.recv.Informations.Send_Gift:
                gift.client.sendPacket(Identifiers.send.Send_Gift, 1)
                return

            elif CC == Identifiers.recv.Informations.Computer_Info:
                return

            elif CC == Identifiers.recv.Informations.Change_Shaman_Color:
                color = packet.readInt()
                gift.client.shamanColor = "%06X" %(0xFFFFFF & color)
                return

            elif CC == Identifiers.recv.Informations.Request_Info:
                gift.client.sendPacket(Identifiers.send.Request_Info, ByteArray().writeUTF("http://195.154.124.74/outils/info.php").toByteArray())
                return       

        elif C == Identifiers.recv.Lua.C:
            if CC == Identifiers.recv.Lua.Lua_Script:
                byte, script = packet.readByte(), packet.readUTF()
                if gift.client.privLevel == 15 and gift.client.isLuaAdmin:
                    gift.client.runLuaAdminScript(script)
                return

            elif CC == Identifiers.recv.Lua.Key_Board:
                key, down, posX, posY = packet.readShort(), packet.readBoolean(), packet.readShort(), packet.readShort()

                
                if gift.client.isFFA and key == 40:
                    if gift.client.canSpawnCN == True:
                        if gift.client.isMovingRight == True and gift.client.isMovingLeft == False:
                            reactor.callLater(0.2, gift.client.Utility.spawnObj, 17, posX - 10, posY +15, 90)
                        if gift.client.isMovingRight == False and gift.client.isMovingLeft == True:
                            reactor.callLater(0.2, gift.client.Utility.spawnObj, 17, posX + 10, posY +25, 270)
                        reactor.callLater(2.5, gift.client.Utility.removeObj)
                        gift.client.canSpawnCN = False
                        reactor.callLater(1.3, gift.client.enableSpawnCN)

                elif gift.client.room.mapCode == 923:  ## Test pour prochain évent
					if gift.client.posX >= 464 and gift.client.posX <= 154 and gift.client.posY >= 354 and gift.client.posY <= 356:
						if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, gift.client.sendFishingCount)
			##		elif gift.client.posX >= 962 and gift.client.posX <= 1049 and gift.client.posY >= 274 and gift.client.posY <= 276:
					##	if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, gift.client.sendFishingCount)
			##		elif gift.client.posX >= 1615 and gift.client.posX <= 1705 and gift.client.posY >= 246 and gift.client.posY <= 247:
					##	if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, gift.client.sendFishingCount)
			##		elif gift.client.posX >= 277 and gift.client.posX <= 347 and gift.client.posY == 193:
					##	if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, gift.client.sendFishingCount)
			##		elif gift.client.posX >= 1752 and gift.client.posX <= 2060 and gift.client.posY >= 355 and gift.client.posY <= 363:
					##	if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(8, gift.client.sendFishingCount)        

                elif gift.client.room.mapCode == 20001:
					if gift.client.posX >= 789 and gift.client.posX <= 911 and gift.client.posY >= 354 and gift.client.posY <= 356:
						if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, gift.client.sendFishingCount)
					elif gift.client.posX >= 962 and gift.client.posX <= 1049 and gift.client.posY >= 274 and gift.client.posY <= 276:
						if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, gift.client.sendFishingCount)
					elif gift.client.posX >= 1615 and gift.client.posX <= 1705 and gift.client.posY >= 246 and gift.client.posY <= 247:
						if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, gift.client.sendFishingCount)
					elif gift.client.posX >= 277 and gift.client.posX <= 347 and gift.client.posY == 193:
						if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, gift.client.sendFishingCount)
					elif gift.client.posX >= 1752 and gift.client.posX <= 2060 and gift.client.posY >= 355 and gift.client.posY <= 363:
						if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(8, gift.client.sendFishingCount)                    

		elif gift.client.room.mapCode == 20002:
                    if gift.client.posX >= 638 and gift.client.posX <= 721 and gift.client.posY >= 43 and gift.client.posY <= 53:
						if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, gift.client.sendFishingCount)
                    elif gift.client.posX >= 647 and gift.client.posX <= 734 and gift.client.posY >= 336 and gift.client.posY <= 338:
						if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, gift.client.sendFishingCount)
                    elif gift.client.posX >= 300 and gift.client.posX <= 738 and gift.client.posY >= 293 and gift.client.posY <= 335:
						if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, gift.client.sendFishingCount)
                    elif gift.client.posX >= 200 and gift.client.posX <= 256 and gift.client.posY >= 182 and gift.client.posY <= 186:
						if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, gift.client.sendFishingCount)
                    elif gift.client.posX >= 41 and gift.client.posX <= 129 and gift.client.posY >= 331 and gift.client.posY <= 353:
						if gift.client.isEvent and key == 32:
							gift.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(8, gift.client.sendFishingCount)                
                        
                if gift.client.isSpeed and key == 32:
                    gift.client.room.movePlayer(gift.client.playerName, 0, 0, True, 50 if gift.client.isMovingRight else -50, 0, True)
                if gift.client.room.isFlyGame and key == 32:
                    if gift.client.flypoints >= 1:
                        gift.client.room.movePlayer(gift.client.playerName, 0, 0, True, 0, -50, True)
                        gift.client.flypoints -= 1
                if gift.client.isFly and key == 32:
                    gift.client.room.movePlayer(gift.client.playerName, 0, 0, True, 0, -50, True) 

                if gift.client.room.isDeathmatch and key == 3:
                    if gift.client.room.canCannon:
                        if not gift.client.canCN:
                            gift.client.room.objectID += 1
                            idCannon = {15: "149aeaa271c.png", 16: "149af112d8f.png", 17: "149af12c2d6.png", 18: "149af130a30.png", 19: "149af0fdbf7.png", 20: "149af0ef041.png", 21: "149af13e210.png", 22: "149af129a4c.png", 23: "149aeaa06d1.png"}
                            #idCannon = "149aeaa271c.png" if gift.client.deathStats[4] == 15 else "149af112d8f.png" if gift.client.deathStats[4] == 16 else "149af12c2d6.png"
                            if gift.client.isMovingRight:
                                x = int(gift.client.posX+gift.client.deathStats[0]) if gift.client.deathStats[0] < 0 else int(gift.client.posX+gift.client.deathStats[0])
                                y = int(gift.client.posY+gift.client.deathStats[1]) if gift.client.deathStats[1] < 0 else int(gift.client.posY+gift.client.deathStats[1])
                                gift.client.sendPlaceObject(gift.client.room.objectID, 17, x, y, 90, 0, 0, True, True)
                                if gift.client.deathStats[4] in [15, 16, 17, 18, 19, 20, 21, 22, 23]:
                                    if not gift.client.deathStats[3] == 1:
                                        gift.client.room.sendAll([29, 19], ByteArray().writeInt(gift.client.playerCode).writeUTF(idCannon[gift.client.deathStats[4]]).writeByte(1).writeInt(gift.client.room.objectID).toByteArray()+"\xff\xf0\xff\xf0")
                            else:
                                x = int(gift.client.posX-gift.client.deathStats[0]) if gift.client.deathStats[0] < 0 else int(gift.client.posX-gift.client.deathStats[0])
                                y = int(gift.client.posY+gift.client.deathStats[1]) if gift.client.deathStats[1] < 0 else int(gift.client.posY+gift.client.deathStats[1])
                                gift.client.sendPlaceObject(gift.client.room.objectID, 17, x, y, -90, 0, 0, True, True)
                                if gift.client.deathStats[4] in [15, 16, 17, 18, 19, 20, 21, 22, 23]:
                                    if not gift.client.deathStats[3] == 1:
                                        gift.client.room.sendAll([29, 19], ByteArray().writeInt(gift.client.playerCode).writeUTF(idCannon[gift.client.deathStats[4]]).writeByte(1).writeInt(gift.client.room.objectID).toByteArray()+"\xff\xf0\xff\xf0")
                            gift.client.canCN = True       
                            gift.canCCN = reactor.callLater(0.8, gift.client.cnTrueOrFalse)        
                if gift.client.room.isDeathmatch and key == 79:
                    gift.client.sendDeathInventory()
                if gift.client.room.isDeathmatch and key == 80:
                    gift.client.sendDeathProfile()
                    
                if gift.client.room.isFFARace and key == 3:
                    if gift.client.canCannon:
                        itemID = random.randint(100, 999)
                        if gift.client.isMovingRight:
                            reactor.callLater(0.2, lambda: gift.client.room.sendAll(Identifiers.send.Spawn_Object, ByteArray().writeInt(itemID).writeShort(17).writeShort(posX + -5).writeShort(posY + 15).writeShort(90).writeShort(0).writeByte(1).writeByte(0).toByteArray()))
                        else:
                            reactor.callLater(0.2, lambda: gift.client.room.sendAll(Identifiers.send.Spawn_Object, ByteArray().writeInt(itemID).writeShort(17).writeShort(posX - -5).writeShort(posY + 15).writeShort(-90).writeShort(0).writeByte(1).writeByte(0).toByteArray()))
                        reactor.callLater(2.5, lambda: gift.client.sendPacket(Identifiers.send.Remove_Object, ByteArray().writeInt(itemID).writeBoolean(True).toByteArray()))
                        gift.client.canCannon = False
                        reactor.callLater(1.3, setattr, gift.client, "canCannon", True)
                return
            
            elif CC == Identifiers.recv.Lua.Mouse_Click:
                posX, posY = packet.readShort(), packet.readShort()
                if gift.client.isTeleport:
                    gift.client.room.movePlayer(gift.client.playerName, posX, posY, False, 0, 0, False)

                elif gift.client.isExplosion:
                    gift.client.Utility.explosionPlayer(posX, posY)
                return

            elif CC == Identifiers.recv.Lua.Popup_Answer:
                popupID, answer = packet.readInt(), packet.readUTF()
                return

            elif CC == Identifiers.recv.Lua.Text_Area_Callback:
                textAreaID, event = packet.readInt(), packet.readUTF()
                ## Gifted Menu System ##
                if event == "showButtons":
                    gift.client.showButtons = not gift.client.showButtons
                    gift.client.sendMenu()

                ## FFA RACE ##
                if event.startswith("ffarace"):
                    if event == "ffarace:close":
                        gift.client.config.closeFFARaceInformation()

                    # Pages
                    elif event == "ffarace:newHelp0":
                        gift.client.config.FFARaceHelp(0)
                    elif event == "ffarace:newHelp1":
                        gift.client.config.FFARaceHelp(1)
                    elif event == "ffarace:newHelp2":
                        gift.client.config.FFARaceHelp(2)
                    elif event == "ffarace:newHelp3":
                        gift.client.config.FFARaceHelp(3)
                    elif event == "ffarace:newHelp4":
                        gift.client.config.FFARaceHelp(4)

                    # Thread
                    elif event == "ffarace:thread2":
                        gift.client.sendLangueMessage("", "<V>[#]</V> http://atelier801.com/topic?f=366697&t=773684")
                    elif event == "ffarace:thread3":
                        gift.client.sendLangueMessage("", "<V>[#]</V> http://atelier801.com/topic?f=366697&t=773978")
                ## END FFA RACE ##

                ## Configurations ##
                if event.startswith("config"):
                    if event == "config:open":
                        gift.client.config.open()
                    elif event == "config:colormouse":
                        gift.client.parseCommands.parseCommand("cor")
                    elif event == "config:close":
                        gift.client.config.close()
                    elif event == "config:close2":
                        gift.client.config.close2()
                    elif event == "config:closeoption":
                        gift.client.config.closeoption()
                    elif event == "config:colornick":
                        if gift.client.privLevel >= 2:
                            gift.client.config.options(1, "<a href='event:config:colornickchat'>Cor do nick no chat</a>", "<a href='event:config:colornickmap'>Cor do nick no mapa</a>")
                    elif event == "config:colornickmap":
                        gift.client.config.closeoption()
                        gift.client.room.showColorPicker(10000, gift.client.Username, 0xc2c2da if gift.client.nameColorMap == "" else int(gift.client.nameColorMap, 16), "Select a color for your name.")
                    elif event == "config:colornickchat":
                        gift.client.config.closeoption()
                        gift.client.room.showColorPicker(10002, gift.client.Username, 0xc2c2da if gift.client.nameColorChat == "" else int(gift.client.nameColorChat, 16), "Select a color for your name in chat.")

                    ## Rádio System ##
                    elif event == "config:music":
                        gift.client.config.options(2, "<a href='event:config:music:funk'>Funk</a>", "<a href='event:config:music:eletronica'>Eletrônica</a>", "<a href='event:config:music:sertaneja'>Sertaneja</a>", "<a href='event:config:music:rap'>Rap</a>", "<a href='event:config:music:off'>Desligar</a>")
                    elif event == "config:music:funk":
                        gift.client.config.closeoption()
                        gift.client.sendPacket(Identifiers.old.send.Music, ["http://216.245.204.229:8054/live"])
                        gift.client.musicNameLink = ""
                        gift.client.musicOn = 1
                        gift.client.sendLangueMessage("", "<PT>[•]<N> Rádio Funk ligada.")
                        gift.client.musicName = 0
                        gift.client.config.musicName(0)
                    elif event == "config:music:eletronica":
                        gift.client.config.closeoption()
                        gift.client.sendPacket(Identifiers.old.send.Music, ["http://live.hunter.fm:82/fresh"])
                        gift.client.musicNameLink = ""
                        gift.client.musicOn = 1
                        gift.client.sendLangueMessage("", "<PT>[•]<N> Rádio Eletrônica ligada.")
                        gift.client.musicName = 0
                        gift.client.config.musicName(0)
                    elif event == "config:music:sertaneja":
                        gift.client.config.closeoption()
                        gift.client.sendPacket(Identifiers.old.send.Music, ["http://live.hunter.fm/country"])
                        gift.client.musicNameLink = "sertaneja"
                        gift.client.musicOn = 1
                        gift.client.sendLangueMessage("", "<PT>[•]<N> Rádio Sertaneja ligada.")
                        gift.client.musicName = 0
                        gift.client.config.musicName(0)
                    elif event == "config:music:rap":
                        gift.client.config.closeoption()
                        gift.client.sendPacket(Identifiers.old.send.Music, ["http://streaming01.hstbr.net:8198/live?1501335186500"])
                        gift.client.musicNameLink = ""
                        gift.client.musicOn = 1
                        gift.client.sendLangueMessage("", "<PT>[•]<N> Rádio RAP ligada.")
                        gift.client.musicName = 0
                        gift.client.config.musicName(0)
                    elif event == "config:music:pop":
                        gift.client.config.closeoption()
                        gift.client.sendPacket(Identifiers.old.send.Music, ["http://audio3.cmaudioevideo.com:8050/stream"])
                        gift.client.musicNameLink = ""
                        gift.client.musicOn = 1
                        gift.client.sendLangueMessage("", "<PT>[•]<N> Rádio POP ligada.")
                        gift.client.musicName = 0
                        gift.client.config.musicName(0)
                    elif event == "config:music:mix":
                        gift.client.config.closeoption()
                        gift.client.sendPacket(Identifiers.old.send.Music, ["http://centova16.ciclanohost.com.br:9627/;"])
                        gift.client.musicNameLink = "http://centova16.ciclanohost.com.br:9627/currentsong?sid=1"
                        gift.client.musicOn = 1
                        gift.client.sendLangueMessage("", "<PT>[•]<N> Rádio MIX ligada.")
                        gift.client.musicName = 1
                        gift.client.config.musicName(1)
                    elif event == "config:music:off":
                        gift.client.config.closeoption()
                        gift.client.sendPacket(Identifiers.old.send.Music, [""])
                        gift.client.musicNameLink = ""
                        gift.client.musicOn = 0
                        gift.client.sendLangueMessage("", "<PT>[•]<N> Rádio desligada.")
                        gift.client.musicName = 0
                        gift.client.config.musicName(0)
                    ## End Rádio System ##

                    ## Personalizacion System ##
                    elif event == "config:personalizacao":
                        gift.client.config.personalizationopen()
                    ## End Personalizacion System ##
                ## End Configurations ##

                ## Email Confimation ##
                if event.startswith("email"):
                    if event == "email:confirm":
                        gift.client.email.openConfirmationBox()
                    elif event == "email:resend":
                        gift.client.email.sendCode()
                    elif event == "email:close":
                        gift.client.email.close()
                ## End Email Confimation ##

                ## Ranking ##
                if event.startswith("ranking"):
                    if event == "ranking:open":
                        gift.client.ranking.open()
                    elif event == "ranking:close":
                        gift.client.ranking.close()
                ## End Ranking ##

                ## Staff Chat ##
                if event.startswith("openStaffChat"):
                    gift.client.openStaffChat = True
                    gift.client.viewMessage = 0
                    gift.client.sendStaffChats()

                if event.startswith("closeStaffChat"):
                    gift.client.openStaffChat = False
                    gift.client.viewMessage = 0
                    gift.client.sendStaffChats()

                if event.startswith("clearStaffChat"):
                    if len(gift.client.server.staffChat) >= 1:
                            del gift.client.server.staffChat[:]
                            gift.client.sendStaffChats()
                            gift.server.sendStaffMessage(4, "<V>"+str(gift.client.Username)+" a effacé la discussion du staff.")
                    else: gift.client.sendLangueMessage("", "<R>Aucune série de discussions ne sera supprimée.")
                ## End Staff Chat ##        


                if event == "closed":
                    gift.client.sendPacket([29, 22], struct.pack("!l", 7999))
                    gift.client.sendPacket([29, 22], struct.pack("!l", 8000))
                    gift.client.sendPacket([29, 22], struct.pack("!l", 8001))
                    gift.client.sendPacket([29, 22], struct.pack("!l", 8249))
                    gift.client.sendPacket([29, 22], struct.pack("!l", 8250))

                    
                if event == "fechar":
                    gift.client.sendPacket([29, 22], struct.pack("!l", 10050))
                    gift.client.sendPacket([29, 22], struct.pack("!l", 10051))
                    gift.client.sendPacket([29, 22], struct.pack("!l", 10052))
                    gift.client.sendPacket([29, 22], struct.pack("!l", 10053))


                elif event == "fecharPop":
                    gift.client.sendPacket([29, 22], struct.pack("!l", 10056))
                    gift.client.sendPacket([29, 22], struct.pack("!l", 10057))
                    gift.client.sendPacket([29, 22], struct.pack("!l", 10058))

                        

                
                ## End Duxo Menu System ##
                    
                if event.startswith("fechadin"):
                    for x in range(0, 100):									
                        gift.client.sendPacket([29, 22], ByteArray().writeInt(x).toByteArray())


                        
                if textAreaID in [8983, 8984, 8985]:
                    if event.startswith("inventory"):
                        event = event.split("#")
                        if event[1] == "use":
                            gift.client.deathStats[4] = int(event[2])
                        else:
                            gift.client.deathStats[4] = 0
                        gift.client.sendDeathInventory(gift.client.page)

                if textAreaID == 123480 or textAreaID == 123479:
                    if event == "next":
                        if not gift.client.page >= 3:
                            gift.client.page += 1
                            gift.client.sendDeathInventory(gift.client.page)
                    else:
                        if not gift.client.page <= 1:
                            gift.client.page -= 1
                            gift.client.sendDeathInventory(gift.client.page)

                if textAreaID == 9012:
                    if event == "close":
                        ids = 131458, 123479, 130449, 131459, 123480, 6992, 8002, 23, 9012, 9013, 9893, 8983, 9014, 9894, 8984, 9015, 9895, 8985, 504, 505, 506, 507
                        for id in ids:
                            if id <= 507 and not id == 23:
                                gift.client.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
                            else:
                                gift.client.sendPacket([29, 22], ByteArray().writeInt(id).toByteArray())

                if textAreaID == 9009:
                    if event == "close":
                        ids = 39, 40, 41, 7999, 20, 9009, 7239, 8249, 270
                        for id in ids:
                            if id <= 41 and not id == 20:
                                gift.client.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
                            else:
                                gift.client.sendPacket([29, 22], ByteArray().writeInt(id).toByteArray())

                if textAreaID == 20:
                    if event.startswith("offset"):
                        event = event.split("#")
                        if event[1] == "offsetX":
                            if event[2] == "1":
                                if not gift.client.deathStats[0] >= 25:
                                    gift.client.deathStats[5] += 1
                                    gift.client.deathStats[0] += 1
                            else:
                                if not gift.client.deathStats[0] <= -25:
                                    gift.client.deathStats[5] -= 1
                                    gift.client.deathStats[0] -= 1
                        else:
                            if event[2] == "1":
                                if not gift.client.deathStats[1] >= 25:
                                    gift.client.deathStats[6] += 1
                                    gift.client.deathStats[1] += 1
                            else:
                                if not gift.client.deathStats[1] <= -25:
                                    gift.client.deathStats[6] -= 1
                                    gift.client.deathStats[1] -= 1
                    elif event == "show":
                        if gift.client.deathStats[3] == 1:
                            gift.client.deathStats[3] = 0
                        else:
                            gift.client.deathStats[3] = 1
                    gift.client.sendDeathProfile()

                    
                if event == "closeRanking":
                        i = 30000
                        while i <= 30010:
                            gift.client.room.removeTextArea(i, gift.client.playerName)
                            i += 1
                return

            elif CC == Identifiers.recv.Lua.Color_Picked:
                colorPickerId, color = packet.readInt(), packet.readInt()
                try:
                    if colorPickerId == 10000:
                        if color != -1:
                            gift.client.nameColor = "%06X" %(0xFFFFFF & color)
                            gift.client.room.setNameColor(gift.client.playerName, color)
                            gift.client.sendMessage("<font color='"+color+"'>" + "İsminizin rengi başarıyla değiştirildi." if gift.client.langue.lower() == "tr" else "You've changed color of your nickname successfully." + "</font>")
                    elif colorPickerId == 10001:
                        if color != -1:
                            gift.client.mouseColor = "%06X" %(0xFFFFFF & color)
                            gift.client.playerLook = "1;%s" %(gift.client.playerLook.split(";")[1])
                            gift.client.sendMessage("<font color='"+color+"'>" + "Farenizin rengini başarıyla değiştirdiniz. Yeni renk için sonraki turu bekleyin." if gift.client.langue.lower() == "tr" else "You've changed color of your mouse successfully.\nWait next round for your new mouse color." + "</font>")
                    elif colorPickerId == 10002:
                        if color != -1:
                            gift.client.nickColor = "%06X" %(0xFFFFFF & color)
                            gift.client.sendMessage("<font color='"+color+"'>" + "İsminizin rengini başarıyla değiştirdiniz. Yeni renk için sonraki turu bekleyin." if gift.client.langue.lower() == "tr" else "You've changed color of your nickname successfully.\nWait next round for your new nickname color." + "</font>")
                except: gift.client.sendMessage("<ROSE>" + "Renginizi Başarıyla Değiştiniz." if gift.client.langue.lower() == "tr" else "Incorrect color, select other one.")
                return
            
        elif C == Identifiers.recv.Cafe.C:
            if CC == Identifiers.recv.Cafe.Mulodrome_Close:
                gift.client.room.sendAll(Identifiers.send.Mulodrome_End)
                return

            elif CC == Identifiers.recv.Cafe.Mulodrome_Join:
                team, position = packet.readByte(), packet.readByte()

                if len(gift.client.mulodromePos) != 0:
                    gift.client.room.sendAll(Identifiers.send.Mulodrome_Leave, chr(gift.client.mulodromePos[0]) + chr(gift.client.mulodromePos[1]))

                gift.client.mulodromePos = [team, position]
                gift.client.room.sendAll(Identifiers.send.Mulodrome_Join, ByteArray().writeByte(team).writeByte(position).writeInt(gift.client.playerID).writeUTF(gift.client.playerName).writeUTF(gift.client.tribeName).toByteArray())
                if gift.client.playerName in gift.client.room.redTeam: gift.client.room.redTeam.remove(gift.client.playerName)
                if gift.client.playerName in gift.client.room.blueTeam: gift.client.room.blueTeam.remove(gift.client.playerName)
                if team == 1:
                    gift.client.room.redTeam.append(gift.client.playerName)
                else:
                    gift.client.room.blueTeam.append(gift.client.playerName)
                return

            elif CC == Identifiers.recv.Cafe.Mulodrome_Leave:
                team, position = packet.readByte(), packet.readByte()
                gift.client.room.sendAll(Identifiers.send.Mulodrome_Leave, ByteArray().writeByte(team).writeByte(position).toByteArray())
                if team == 1:
                    for playerName in gift.client.room.redTeam:
                        if gift.client.room.clients[playerName].mulodromePos[1] == position:
                            gift.client.room.redTeam.remove(playerName)
                            break
                else:
                    for playerName in gift.client.room.blueTeam:
                        if gift.client.room.clients[playerName].mulodromePos[1] == position:
                            gift.client.room.blueTeam.remove(playerName)
                            break
                return

            elif CC == Identifiers.recv.Cafe.Mulodrome_Play:
                if not len(gift.client.room.redTeam) == 0 or not len(gift.client.room.blueTeam) == 0:
                    gift.client.room.isMulodrome = True
                    gift.client.room.isRacing = True
                    gift.client.room.noShaman = True
                    gift.client.room.mulodromeRoundCount = 0
                    gift.client.room.never20secTimer = True
                    gift.client.room.sendAll(Identifiers.send.Mulodrome_End)
                    gift.client.room.mapChange()
                return

            elif CC == Identifiers.recv.Cafe.Reload_Cafe:
                gift.client.cafe.loadCafeMode()
                return

            elif CC == Identifiers.recv.Cafe.Open_Cafe_Topic:
                topicID = packet.readInt()
                gift.client.cafe.openCafeTopic(topicID)
                return

            elif CC == Identifiers.recv.Cafe.Create_New_Cafe_Topic:
                message , title = packet.readUTF(), packet.readUTF()
                if gift.client.privLevel >= 5 or (gift.client.privLevel != 0 and gift.client.cheeseCount >= 0):
                    gift.client.cafe.createNewCafeTopic(message, title)
                return

            elif CC == Identifiers.recv.Cafe.Create_New_Cafe_Post:
                topicID, message = packet.readInt(), packet.readUTF()
                if gift.client.privLevel >= 5 or (gift.client.privLevel != 0 and gift.client.cheeseCount >= 0):
                    gift.client.cafe.createNewCafePost(topicID, message)
                return

            elif CC == Identifiers.recv.Cafe.Open_Cafe:
                gift.client.isCafe = packet.readBoolean()
                return

            elif CC == Identifiers.recv.Cafe.Vote_Cafe_Post:
                topicID, postID, mode = packet.readInt(), packet.readInt(), packet.readBoolean()
                if gift.client.privLevel >= 5 or (gift.client.privLevel != 0 and gift.client.cheeseCount >= 0):
                    gift.client.cafe.voteCafePost(topicID, postID, mode)
                return

            elif CC == Identifiers.recv.Cafe.Delete_Cafe_Message:
                if gift.client.privLevel >= 7:
                    topicID, postID = packet.readInt(), packet.readInt()
                    gift.client.cafe.deleteCafePost(topicID, postID)
##                else:
##                	gift.client.sendMessage("Bu işlevi kullanma yetkiniz yok.")
                return

            elif CC == Identifiers.recv.Cafe.Delete_All_Cafe_Message:
                if gift.client.privLevel >= 7:
                    topicID, playerName = packet.readInt(), packet.readUTF()
                    gift.client.cafe.deleteAllCafePost(topicID, playerName)
                else:
                	gift.client.sendMessage("Vous n'êtes pas autorisé à utiliser cette fonction.")
                return

        elif C == Identifiers.recv.Inventory.C:
            if CC == Identifiers.recv.Inventory.Open_Inventory:
                gift.client.sendInventoryConsumables()
                return

            elif CC == Identifiers.recv.Inventory.Use_Consumable:
                id = packet.readShort()
                if gift.client.playerConsumables.has_key(id) and not gift.client.isDead and not gift.client.room.isRacing and not gift.client.room.isBootcamp and not gift.client.room.isDefilante and not gift.client.room.isSpeedRace and not gift.client.room.isMeepRace:
                    # if not id in [31, 34, 2240, 2247, 2262, 2332, 2340] or gift.client.pet == 0:
                    count = gift.client.playerConsumables[id]
                    if count > 0:
                        count -= 1
                        gift.client.playerConsumables[id] -= 1
                        if count == 0:
                            del gift.client.playerConsumables[id]
                            if gift.client.equipedConsumables:
                                for id in gift.client.equipedConsumables:
                                    if not id:
                                        gift.client.equipedConsumables.remove(id)
                                None
                                if id in gift.client.equipedConsumables:
                                    gift.client.equipedConsumables.remove(id)

                        if id in [1, 5, 6, 8, 11, 20, 24, 25, 26, 2250]:
                            if id == 11:
                                gift.client.room.objectID += 2
                            ids={1:65, 5:6, 6:34, 8:89, 11:90, 20:33, 24:63, 25:80, 26:95, 2250:97}   
                            gift.client.sendPlaceObject(gift.client.room.objectID if id == 11 else 0, ids[id], gift.client.posX + 28 if gift.client.isMovingRight else gift.client.posX - 28, gift.client.posY, 0, 0 if id == 11 or id == 24 else 10 if gift.client.isMovingRight else -10, -3, True, True)
                            
##                        if id == 1 or id == 5 or id == 6 or id == 8 or id == 11 or id == 20 or id == 24 or id == 25 or id == 26 or id == 2250:
##                                if id == 11:
##                                    gift.client.room.objectID += 2
##                                gift.client.sendPlaceObject(gift.client.room.objectID if id == 11 else 0, 65 if id == 1 else 6 if id == 5 else 34 if id == 6 else 89 if id == 8 else 90 if id == 11 else 33 if id == 20 else 63 if id == 24 else 80 if id == 25 else 95 if id == 26 else 114 if id == 2250 else 0, gift.client.posX + 28 if gift.client.isMovingRight else gift.client.posX - 28, gift.client.posY, 0, 0 if id == 11 or id == 24 else 10 if gift.client.isMovingRight else -10, -3, True, True)
                        if id == 10:
                            x = 0
                            for player in gift.client.room.clients.values():
                                if x < 5 and player != gift.client:
                                    if player.posX >= gift.client.posX - 400 and player.posX <= gift.client.posX + 400:
                                        if player.posY >= gift.client.posY - 300 and player.posY <= gift.client.posY + 300:
                                            player.sendPlayerEmote(3, "", False, False)
                                            x += 1

                        if id == 11:
                            gift.client.room.newConsumableTimer(gift.client.room.objectID)
                            gift.client.isDead = True
                            if not gift.client.room.noAutoScore: gift.client.playerScore += 1
                            gift.client.sendPlayerDied()
                            gift.client.room.checkChangeMap()
                    
                        if id == 28:
                            gift.client.parseSkill.sendBonfireSkill(gift.client.posX, gift.client.posY, 15)

                        if id in [31, 34, 2240, 2247, 2262, 2332, 2340,2437]:
                            gift.client.pet = {31:2, 34:3, 2240:4, 2247:5, 2262:6, 2332:7, 2340:8,2437:9}[id]
                            gift.client.petEnd = Utils.getTime() + (1200 if gift.client.pet == 8 else 3600)
                            gift.client.room.sendAll(Identifiers.send.Pet, ByteArray().writeInt(gift.client.playerCode).writeUnsignedByte(gift.client.pet).toByteArray())

                        if id == 33:
                            gift.client.sendPlayerEmote(16, "", False, False)
                        
                        if id == 21:
                            gift.client.sendPlayerEmote(12, "", False, False)        

                        if id == 35:
                            if len(gift.client.shopBadges) > 0:
                                gift.client.room.sendAll(Identifiers.send.Balloon_Badge, ByteArray().writeInt(gift.client.playerCode).writeShort(random.choice(gift.client.shopBadges.keys())).toByteArray())

                        if id == 800:
                            gift.client.shopCheeses += 5
                            gift.client.sendAnimZelda(2, 0)
                            gift.client.sendGiveCurrency(0, 5)

                        if id == 801:
                            gift.client.shopFraises += 5
                            gift.client.sendAnimZelda(2, 2)

                        if id == 2234:
                            x = 0
                            gift.client.sendPlayerEmote(20, "", False, False)
                            for player in gift.client.room.clients.values():
                                if x < 5 and player != gift.client:
                                    if player.posX >= gift.client.posX - 400 and player.posX <= gift.client.posX + 400:
                                        if player.posY >= gift.client.posY - 300 and player.posY <= gift.client.posY + 300:
                                            player.sendPlayerEmote(6, "", False, False)
                                            x += 1

                        if id == 2239:
                            gift.client.room.sendAll(Identifiers.send.Crazzy_Packet, ByteArray().writeByte(4).writeInt(gift.client.playerCode).writeInt(gift.client.shopCheeses).toByteArray())
                        
                        if id in [2252,2256,2349,2379]:
                            renkler = {2252:"56C93E",2256:"C93E4A",2349:"52BBFB",2379:"FF8400"}
                            renk = int(renkler[id],16)
                            gift.client.drawingColor = renk
                            gift.client.sendPacket(Identifiers.send.Crazzy_Packet, ByteArray().writeUnsignedByte(1).writeUnsignedShort(650).writeInt(renk).toByteArray())

                        if id in [9,12,13,17,18,19,22,27,407,2251,2258,2308,2439]: # kurkler
                            ids={9:"10",12:"33",13:"35",17:"37",18:"16",19:"42",22:"45",27:"51",407:"7",2251:"61",2258:"66",2308:"75",2439:"118"}[id]
                            look = gift.client.playerLook
                            index = look.index(";")
                            gift.client.fur = ids + look[index:]
                            
                        if id == 2246:
                            gift.client.sendPlayerEmote(24, "", False, False)

                        if id == 2100:
                            idlist = ["1", "5", "6", "8", "11", "20", "24", "25", "26", "31", "34", "2240", "2247", "2262", "2332", "2340", "33", "35", "800", "801", "2234", "2239", "2255", "10", "28"]
                            ids = int(random.choice(idlist))
                            if not ids in gift.client.playerConsumables:
                                gift.client.playerConsumables[ids] = 1
                            else:
                               counts = gift.client.playerConsumables[ids] + 1
                               gift.client.playerConsumables[ids] = counts
                            gift.client.sendAnimZeldaInventory(4, ids, 1)

                        if id == 2255:
                            gift.client.sendAnimZelda2(7, case="$De6", id=random.randint(0, 6))
                            
                        if id == 2259:
                            gift.client.room.sendAll(Identifiers.send.Crazzy_Packet, gift.client.getCrazzyPacket(5, [gift.client.playerCode, (gift.client.playerTime / 86400),(gift.client.playerTime / 3600) % 24]));
                                
                        gift.client.updateInventoryConsumable(id, count)
                        gift.client.useInventoryConsumable(id)
                return

            elif CC == Identifiers.recv.Inventory.Equip_Consumable:
                id, equip = packet.readShort(), packet.readBoolean()
                try:
                    if equip:
                        gift.client.equipedConsumables.append(id)
                    else:
                        gift.client.equipedConsumables.remove(str(id))
                except: pass
                return
                
            elif CC == Identifiers.recv.Inventory.Trade_Invite:
                playerName = packet.readUTF()
                gift.client.tradeInvite(playerName)
                return
                
            elif CC == Identifiers.recv.Inventory.Cancel_Trade:
                playerName = packet.readUTF()
                gift.client.cancelTrade(playerName)
                return
                
            elif CC == Identifiers.recv.Inventory.Trade_Add_Consusmable:
                id, isAdd = packet.readShort(), packet.readBoolean()
                try:
                    gift.client.tradeAddConsumable(id, isAdd)
                except: pass
                return
                
            elif CC == Identifiers.recv.Inventory.Trade_Result:
                isAccept = packet.readBoolean()
                gift.client.tradeResult(isAccept)
                return

        elif C == Identifiers.recv.Tribulle.C:
            if CC == Identifiers.recv.Tribulle.Tribulle:
                if not gift.client.isGuest:
                    code = packet.readShort()
                    gift.client.tribulle.parseTribulleCode(code, packet)
                return

        elif C == Identifiers.recv.Transformice.C:
            if CC == Identifiers.recv.Transformice.Invocation:
                objectCode, posX, posY, rotation, position, invocation = packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readUTF(), packet.readBoolean()
                if gift.client.isShaman:
                    showInvocation = True
                    if gift.client.room.isSurvivor:
                        showInvocation = invocation
                    pass
                    if showInvocation:
                        gift.client.room.sendAllOthers(gift.client, Identifiers.send.Invocation, ByteArray().writeInt(gift.client.playerCode).writeShort(objectCode).writeShort(posX).writeShort(posY).writeShort(rotation).writeUTF(position).writeBoolean(invocation).toByteArray())
                return

            elif CC == Identifiers.recv.Transformice.Remove_Invocation:
                if gift.client.isShaman:
                    gift.client.room.sendAllOthers(gift.client, Identifiers.send.Remove_Invocation, ByteArray().writeInt(gift.client.playerCode).toByteArray())
                return

            elif CC == Identifiers.recv.Transformice.Change_Shaman_Badge:
                badge = packet.readByte()
                if str(badge) or badge == 0 in gift.client.shamanBadges:
                    gift.client.equipedShamanBadge = str(badge)
                    gift.client.sendProfile(gift.client.playerName)
                return
                
            elif CC == Identifiers.recv.Transformice.Crazzy_Packet:
                type = packet.readByte()
                if type == 2:
                    posX = int(packet.readShort())
                    posY = int(packet.readShort())
                    lineX = int(packet.readShort())
                    lineY = int(packet.readShort())
                    gift.client.room.sendAllOthers(gift.client, Identifiers.send.Crazzy_Packet, gift.client.getCrazzyPacket(2,[gift.client.playerCode, gift.client.drawingColor, posX, posY, lineX, lineY]))
                       

            elif CC == Identifiers.recv.Transformice.NPC_Functions:
                id = packet.readByte()
                if id == 4:
                    gift.client.openNpcShop(packet.readUTF())
                else:
                    gift.client.buyNPCItem(packet.readByte())
                return

            
            elif CC == Identifiers.recv.Transformice.Full_Look:
                p = ByteArray(packet.toByteArray())
                visuID = p.readShort()

                shopItems = [] if gift.client.shopItems == "" else gift.client.shopItems.split(",")
                look = gift.server.newVisuList[visuID].split(";")
                look[0] = int(look[0])
                lengthCloth = len(gift.client.clothes)
                buyCloth = 5 if (lengthCloth == 0) else (50 if lengthCloth == 1 else 100)

                gift.client.visuItems = {-1: {"ID": -1, "Buy": buyCloth, "Bonus": True, "Customizable": False, "HasCustom": False, "CustomBuy": 0, "Custom": "", "CustomBonus": False}, 22: {"ID": gift.client.getFullItemID(22, look[0]), "Buy": gift.client.getItemInfo(22, look[0])[6], "Bonus": False, "Customizable": False, "HasCustom": False, "CustomBuy": 0, "Custom": "", "CustomBonus": False}}

                count = 0
                for visual in look[1].split(","):
                    if not visual == "0":
                        item, customID = visual.split("_", 1) if "_" in visual else [visual, ""]
                        item = int(item)
                        itemID = gift.client.getFullItemID(count, item)
                        itemInfo = gift.client.getItemInfo(count, item)
                        gift.client.visuItems[count] = {"ID": itemID, "Buy": itemInfo[6], "Bonus": False, "Customizable": bool(itemInfo[2]), "HasCustom": customID != "", "CustomBuy": itemInfo[7], "Custom": customID, "CustomBonus": False}
                        if gift.client.parseShop.checkInShop(gift.client.visuItems[count]["ID"]):
                            gift.client.visuItems[count]["Buy"] -= itemInfo[6]
                        if len(gift.client.custom) == 1:
                            if itemID in gift.client.custom:
                                gift.client.visuItems[count]["HasCustom"] = True
                            else:
                                gift.client.visuItems[count]["HasCustom"] = False
                        else:
                            if str(itemID) in gift.client.custom:
                                gift.client.visuItems[count]["HasCustom"] = True
                            else:
                                gift.client.visuItems[count]["HasCustom"] = False
                    count += 1
                hasVisu = map(lambda y: 0 if y in shopItems else 1, map(lambda x: x["ID"], gift.client.visuItems.values()))
                visuLength = reduce(lambda x, y: x + y, hasVisu)
                allPriceBefore = 0
                allPriceAfter = 0
                promotion = 70.0 / 100

                p.writeUnsignedShort(visuID)
                p.writeUnsignedByte(20)
                p.writeUTF(gift.server.newVisuList[visuID])
                p.writeUnsignedByte(visuLength)

                for category in gift.client.visuItems.keys():
                    if len(gift.client.visuItems.keys()) == category:
                        category = 22
                    itemID = gift.client.getSimpleItemID(category, gift.client.visuItems[category]["ID"])

                    buy = [gift.client.visuItems[category]["Buy"], int(gift.client.visuItems[category]["Buy"] * promotion)]
                    customBuy = [gift.client.visuItems[category]["CustomBuy"], int(gift.client.visuItems[category]["CustomBuy"] * promotion)]

                    p.writeShort(gift.client.visuItems[category]["ID"])
                    p.writeUnsignedByte(2 if gift.client.visuItems[category]["Bonus"] else (1 if not gift.client.parseShop.checkInShop(gift.client.visuItems[category]["ID"]) else 0))
                    p.writeUnsignedShort(buy[0])
                    p.writeUnsignedShort(buy[1])
                    p.writeUnsignedByte(3 if not gift.client.visuItems[category]["Customizable"] else (2 if gift.client.visuItems[category]["CustomBonus"] else (1 if gift.client.visuItems[category]["HasCustom"] == False else 0)))
                    p.writeUnsignedShort(customBuy[0])
                    p.writeUnsignedShort(customBuy[1])
                    
                    allPriceBefore += buy[0] + customBuy[0]
                    allPriceAfter += (0 if (gift.client.visuItems[category]["Bonus"]) else (0 if gift.client.parseShop.checkInShop(itemID) else buy[1])) + (0 if (not gift.client.visuItems[category]["Customizable"]) else (0 if gift.client.visuItems[category]["CustomBonus"] else (0 if gift.client.visuItems[category]["HasCustom"] else (customBuy[1]))))
                    
                p.writeShort(allPriceBefore)
                p.writeShort(allPriceAfter)
                gift.client.priceDoneVisu = allPriceAfter

                gift.client.sendPacket(Identifiers.send.Buy_Full_Look, p.toByteArray())

            elif CC == Identifiers.recv.Transformice.Map_Info:
                gift.client.room.cheesesList = []
                cheesesCount = packet.readByte()
                i = 0
                while i < cheesesCount / 2:
                    cheeseX, cheeseY = packet.readShort(), packet.readShort()
                    gift.client.room.cheesesList.append([cheeseX, cheeseY])
                    i += 1
                
                gift.client.room.holesList = []
                holesCount = packet.readByte()
                i = 0
                while i < holesCount / 3:
                    holeType, holeX, holeY = packet.readShort(), packet.readShort(), packet.readShort()
                    gift.client.room.holesList.append([holeType, holeX, holeY])
                    i += 1
                return

        if gift.server.isDebug:
            print "[%s] Packet not implemented - C: %s - CC: %s - packet: %s" %(gift.client.playerName, C, CC, repr(packet.toByteArray()))

    def parsePacketUTF(gift, packet):
        values = packet.split(chr(1))
        C = ord(values[0][0])
        CC = ord(values[0][1])
        values = values[1:]

        if C == Identifiers.old.recv.Player.C:
            if CC == Identifiers.old.recv.Player.Conjure_Start:
                gift.client.room.sendAll(Identifiers.old.send.Conjure_Start, values)
                return

            elif CC == Identifiers.old.recv.Player.Conjure_End:
                gift.client.room.sendAll(Identifiers.old.send.Conjure_End, values)
                return

            elif CC == Identifiers.old.recv.Player.Conjuration:
                reactor.callLater(10, gift.client.sendConjurationDestroy, int(values[0]), int(values[1]))
                gift.client.room.sendAll(Identifiers.old.send.Add_Conjuration, values)
                return

            elif CC == Identifiers.old.recv.Player.Snow_Ball:
                gift.client.sendPlaceObject(0, 34, int(values[0]), int(values[1]), 0, 0, 0, False, True)
                return

            elif CC == Identifiers.old.recv.Player.Bomb_Explode:
                gift.client.room.sendAll(Identifiers.old.send.Bomb_Explode, values)
                return

        elif C == Identifiers.old.recv.Room.C:
            if CC == Identifiers.old.recv.Room.Anchors:
                gift.client.room.sendAll(Identifiers.old.send.Anchors, values)
                gift.client.room.anchors.extend(values)
                return

            elif CC == Identifiers.old.recv.Room.Begin_Spawn:
                if not gift.client.isDead:
                    gift.client.room.sendAll(Identifiers.old.send.Begin_Spawn, [gift.client.playerCode] + values)
                return

            elif CC == Identifiers.old.recv.Room.Spawn_Cancel:
                gift.client.room.sendAll(Identifiers.old.send.Spawn_Cancel, [gift.client.playerCode])
                return

            elif CC == Identifiers.old.recv.Room.Totem_Anchors:
                if gift.client.room.isTotemEditor:
                    if gift.client.tempTotem[0] < 20:
                        gift.client.tempTotem[0] = int(gift.client.tempTotem[0]) + 1
                        gift.client.sendTotemItemCount(gift.client.tempTotem[0])
                        gift.client.tempTotem[1] += "#3#" + chr(1).join(map(str, [values[0], values[1], values[2]]))
                return

            elif CC == Identifiers.old.recv.Room.Move_Cheese:
                gift.client.room.sendAll(Identifiers.old.send.Move_Cheese, values)
                return

            elif CC == Identifiers.old.recv.Room.Bombs:
                gift.client.room.sendAll(Identifiers.old.send.Bombs, values)
                return

        elif C == Identifiers.old.recv.Balloons.C:
            if CC == Identifiers.old.recv.Balloons.Place_Balloon:
                gift.client.room.sendAll(Identifiers.old.send.Balloon, values)
                return

            elif CC == Identifiers.old.recv.Balloons.Remove_Balloon:
                gift.client.room.sendAllOthers(gift.client, Identifiers.old.send.Balloon, [gift.client.playerCode, "0"])
                return

        elif C == Identifiers.old.recv.Map.C:
            if CC == Identifiers.old.recv.Map.Vote_Map:
                if len(values) == 0:
                    gift.client.room.receivedNo += 1
                else:
                    gift.client.room.receivedYes += 1
                return

            elif CC == Identifiers.old.recv.Map.Load_Map:
                values[0] = values[0].replace("@", "")
                if values[0].isdigit():
                    code = int(values[0])
                    gift.client.room.CursorMaps.execute("select * from Maps where Code = ?", [code])
                    rs = gift.client.room.CursorMaps.fetchone()
                    if rs:
                        if gift.client.playerName == rs["Name"] or gift.client.privLevel >= 6:
                            gift.client.sendPacket(Identifiers.old.send.Load_Map, [rs["XML"], rs["YesVotes"], rs["NoVotes"], rs["Perma"]])
                            gift.client.room.EMapXML = rs["XML"]
                            gift.client.room.EMapLoaded = code
                            gift.client.room.EMapValidated = False
                        else:
                            gift.client.sendPacket(Identifiers.old.send.Load_Map_Result, [])
                    else:
                        gift.client.sendPacket(Identifiers.old.send.Load_Map_Result, [])
                else:
                    gift.client.sendPacket(Identifiers.old.send.Load_Map_Result, [])
                return

            elif CC == Identifiers.old.recv.Map.Validate_Map:
                mapXML = values[0]
                if gift.client.room.isEditor:
                    gift.client.sendPacket(Identifiers.old.send.Map_Editor, [""])
                    gift.client.room.EMapValidated = False
                    gift.client.room.EMapCode = 1
                    gift.client.room.EMapXML = mapXML
                    gift.client.room.mapChange()
                return

            elif CC == Identifiers.old.recv.Map.Map_Xml:
                gift.client.room.EMapXML = values[0]
                return

            elif CC == Identifiers.old.recv.Map.Return_To_Editor:
                gift.client.room.EMapCode = 0
                gift.client.sendPacket(Identifiers.old.send.Map_Editor, ["", ""])
                return

            elif CC == Identifiers.old.recv.Map.Export_Map:
                isTribeHouse = len(values) != 0
                if gift.client.cheeseCount < 40 and gift.client.privLevel < 6 and not isTribeHouse:
                    gift.client.sendMessage("<ROSE>Vous avez besoin de 40 fromages pour valider la map", False)
                elif gift.client.shopCheeses < (5 if isTribeHouse else 40) and gift.client.privLevel < 6:
                    gift.client.sendPacket(Identifiers.old.send.Editor_Message, ["", ""])
                elif gift.client.room.EMapValidated or isTribeHouse:
                    if gift.client.privLevel < 6:
                        gift.client.shopCheeses -= 5 if isTribeHouse else 40

                    code = 0
                    if gift.client.room.EMapLoaded != 0:
                        code = gift.client.room.EMapLoaded
                        gift.client.room.CursorMaps.execute("update Maps set XML = ?, Updated = ? where Code = ?", [gift.client.room.EMapXML, Utils.getTime(), code])
                    else:
                        gift.server.lastMapEditeurCode += 1
                        gift.server.configs("game.lastMapCodeId", str(gift.server.lastMapEditeurCode))
                        gift.server.updateConfig()
                        code = gift.server.lastMapEditeurCode
                        
                    gift.client.room.CursorMaps.execute("insert into Maps (Code, Name, XML, YesVotes, NoVotes, Perma, Del) values (?, ?, ?, ?, ?, ?, ?)", [code, gift.client.playerName, gift.client.room.EMapXML, 0, 0, 22 if isTribeHouse else 0, 0])
                    gift.client.sendPacket(Identifiers.old.send.Map_Editor, ["0"])
                    gift.client.enterRoom(gift.server.recommendRoom(gift.client.langue))
                    gift.client.sendPacket(Identifiers.old.send.Map_Exported, [code])
                return

            elif CC == Identifiers.old.recv.Map.Reset_Map:
                gift.client.room.EMapLoaded = 0
                return

            elif CC == Identifiers.old.recv.Map.Exit_Editor:
                gift.client.sendPacket(Identifiers.old.send.Map_Editor, ["0"])
                gift.client.enterRoom(gift.server.recommendRoom(gift.client.langue))
                return


        if gift.server.isDebug:
            print "[%s][OLD] Packet not implemented - C: %s - CC: %s - values: %s" %(gift.client.playerName, C, CC, repr(values))

    def descriptPacket(gift, packetID, packet):
        data = ByteArray()
        while packet.bytesAvailable():
            packetID = (packetID + 1) % len(gift.server.packetKeys)
            data.writeByte(packet.readByte() ^ gift.server.packetKeys[packetID])
        return data
