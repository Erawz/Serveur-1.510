#coding: utf-8
import re, time as _time

# Modules
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
from bs4 import BeautifulSoup


# Library
from collections import deque

class Tribulle:
    try:
        
        def __init__(gift, player, server):
            gift.client = player
            gift.server = player.server
            gift.Cursor = player.Cursor

            gift.TRIBE_RANKS = "0|${trad#TG_0}|0;0|${trad#TG_1}|0;2|${trad#TG_2}|0;3|${trad#TG_3}|0;4|${trad#TG_4}|32;5|${trad#TG_5}|160;6|${trad#TG_6}|416;7|${trad#TG_7}|932;8|${trad#TG_8}|2044;9|${trad#TG_9}|2046"
            
        def getTime(gift):
            return int(_time.time() / 60)

        def sendPacket(gift, code, result):
            gift.client.sendPacket([60, 3], ByteArray().writeShort(code).writeBytes(result).toByteArray())
      
        def sendPacketToPlayer(gift, playerName, code, result):
            player = gift.server.players.get(playerName)
            if player != None:
                player.tribulle.sendPacket(code, result)

        def sendPacketWholeTribe(gift, code, result, all=False):
            for player in gift.server.players.values():
                if player.playerCode != gift.client.playerCode or all:
                    if player.tribeCode == gift.client.tribeCode:
                        player.tribulle.sendPacket(code, result)

        def sendPacketWholeChat(gift, chatID, code, result, all=False):
            for player in gift.server.players.values():
                if player.playerCode != gift.client.playerCode or all:
                    if chatID in player.chats:
                        player.tribulle.sendPacket(code, result)

        def updateTribeData(gift):
            for player in gift.server.players.values():
                if player.tribeCode == gift.client.tribeCode:
                    player.tribeHouse = gift.client.tribeHouse
                    player.tribeMessage = gift.client.tribeMessage
                    player.tribeRanks = gift.client.tribeRanks

        def parseTribulleCode(gift, code, packet):
            if code == 28:
                gift.sendFriendsList(packet)
            elif code == 30:
                gift.closeFriendsList(packet)
            elif code == 18:
                gift.addFriend(packet)
            elif code == 20:
                gift.removeFriend(packet)
            elif code == 46:
                gift.sendIgnoredsList(packet)
            elif code == 42:
                gift.ignorePlayer(packet)
            elif code == 44:
                gift.removeIgnore(packet)
            elif code == 52:
                gift.whisperMessage(packet)
            elif code == 60:
                gift.disableWhispers(packet)
            elif code == 10:
                gift.changeGender(packet)
            elif code == 22:
                gift.marriageInvite(packet)
            elif code == 24:
                gift.marriageAnswer(packet)
            elif code == 26:
                gift.marriageDivorce(packet)
            elif code == 108:
                gift.sendTribeInfo(packet)
            elif code == 84:
                gift.createTribe(packet)
            elif code == 78:
                gift.tribeInvite(packet)
            elif code == 80:
                gift.tribeInviteAnswer(packet)
            elif code == 98:
                gift.changeTribeMessage(packet)
            elif code == 102:
                gift.changeTribeCode(packet)
            elif code == 110:
                gift.closeTribe(packet)
            elif code == 118:
                gift.createNewTribeRank(packet)
            elif code == 120:
                gift.deleteTribeRank(packet)
            elif code == 116:
                gift.renameTribeRank(packet)
            elif code == 122:
                gift.changeRankPosition(packet)
            elif code == 114:
                gift.setRankPermition(packet)
            elif code == 112:
                gift.changeTribePlayerRank(packet)
            elif code == 132:
                gift.showTribeHistorique(packet)
            elif code == 82:
                gift.leaveTribe(packet)
            elif code == 104:
                gift.kickPlayerTribe(packet)
            elif code == 126:
                gift.setTribeMaster(packet)
            elif code == 128:
                gift.finishTribe(packet)
            elif code == 54:
                gift.customChat(packet)
            elif code == 48:
                gift.chatMessage(packet)
            elif code == 58:
                gift.chatMembersList(packet)
            elif code == 50:
                gift.sendTribeChatMessage(packet)
            else:
                if gift.server.isDebug:
                    print "[%s] [WARN][%s] Invalid tribulle code -> Code: %s packet: %s" %(_time.strftime("%H:%M:%S"), gift.client.playerName, code, repr(packet.toByteArray()))
            
        def sendFriendsList(gift, readPacket):
            if gift.client.isBlockAttack:
                p = ByteArray().writeShort(3 if readPacket == None else 34)
                if readPacket == None:
                    p.writeByte(gift.client.gender).writeInt(gift.client.playerID)
                if gift.client.marriage == "":
                    p.writeInt(0).writeUTF("").writeByte(1).writeInt(0).writeByte(1).writeByte(1).writeInt(1).writeUTF("").writeInt(0)
                else:
                    gift.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [gift.client.marriage])
                    rs = gift.Cursor.fetchone()
                    player = gift.server.players.get(gift.client.marriage)
                    p.writeInt(rs[1]).writeUTF(rs[0].lower()).writeByte(rs[2]).writeInt(rs[1]).writeByte(1).writeBoolean(gift.server.checkConnectedAccount(rs[0])).writeInt(4).writeUTF(player.roomName if player else "").writeInt(rs[3])
                infos = {}
                gift.Cursor.execute("select Username, PlayerID, FriendsList, Marriage, Gender, LastOn from Users where Username in (%s)" %(Utils.joinWithQuotes(gift.client.friendsList)))
                for rs in gift.Cursor.fetchall():
                    infos[rs[0]] = [rs[1], rs[2], rs[3], rs[4], rs[5]]

                gift.client.openingFriendList = True
                isOnline = []
                friendsOn = []
                friendsOff = []
                isOffline = []
                for playerName in gift.client.friendsList:
                    if not infos.has_key(playerName):
                        continue
                    if not gift.client.friendsList == ['']:
                        player = gift.server.players.get(playerName)
                        info = infos[playerName]
                        isFriend = gift.client.playerName in player.friendsList if player != None else gift.client.playerName in info[1].split(",")
                        if gift.server.checkConnectedAccount(playerName):
                            if isFriend:
                                friendsOn.append(playerName)
                            else:
                                isOnline.append(playerName)
                        else:
                            if isFriend:
                                friendsOff.append(playerName)
                            else:
                                isOffline.append(playerName)
                playersNames = friendsOn + isOnline + friendsOff + isOffline
                
                p.writeShort(len(playersNames)-1 if playersNames == [''] else len(playersNames))
                for playerName in playersNames:
                    if not infos.has_key(playerName):
                        continue
                    if not playersNames == ['']:
                        info = infos[playerName]
                        player = gift.server.players.get(playerName)
                        isFriend = gift.client.playerName in player.friendsList if player != None else gift.client.playerName in info[1].split(",")
                        genderID = player.gender if player else int(info[3])
                        isMarriage = gift.client.playerName == player.marriage if player else info[2] == gift.client.playerName
                        p.writeInt(info[0]).writeUTF(playerName.lower()).writeByte(genderID).writeInt(info[0]).writeByte(1 if isFriend else 0).writeBoolean(gift.server.checkConnectedAccount(playerName)).writeInt(4 if isFriend and player != None else 1).writeUTF(player.roomName if isFriend and player != None else "").writeInt(info[4] if isFriend else 0)
                if readPacket == None:
                    p.writeShort(len(gift.client.ignoredsList)-1 if gift.client.ignoredsList == [''] else len(gift.client.ignoredsList))

                    for playerName in gift.client.ignoredsList:
                        if not gift.client.ignoredsList == ['']:
                            p.writeUTF(playerName.lower())
                    p.writeUTF(gift.client.tribeName)
                    p.writeInt(gift.client.tribeCode)
                    p.writeUTF(gift.client.tribeMessage)
                    p.writeInt(gift.client.tribeHouse)
                    if not gift.client.tribeRanks == "":
                        rankInfo = gift.client.tribeRanks.split(";")
                        rankName = rankInfo[gift.client.tribeRank].split("|")
                        p.writeUTF(rankName[1])
                        p.writeInt(rankName[2])
                    else:
                        p.writeUTF("")
                        p.writeInt(0)
                gift.client.sendPacket([60, 3], p.toByteArray())
                if not readPacket == None and not gift.client.marriage == "":
                    gift.sendPacket(15 if readPacket == "0" else 29, ByteArray().writeInt(gift.client.tribulleID+1).writeByte(1).toByteArray())
                gift.client.isBlockAttack = False
                gift.client.blockAttack()
##            else:
##                gift.client.sendMessage("<ROSE>,")
                
        def closeFriendsList(gift, readPacket):
            gift.client.openingFriendList = False
            gift.sendPacket(31, ByteArray().writeBytes(readPacket.toByteArray()).writeByte(1).toByteArray())

        def addFriend(gift, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            #if not "#" in playerName: playerName += "#0000"
            id = gift.server.getPlayerID(playerName)
            player = gift.server.players.get(playerName)
            isFriend = gift.checkFriend(playerName, gift.client.playerName)
            gift.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [playerName])
            rs = gift.Cursor.fetchone()
            if not gift.server.checkExistingUser(playerName):
                gift.sendPacket(19, ByteArray().writeInt(tribulleID).writeByte(12).toByteArray())
            else:
                gift.client.friendsList.append(playerName)
                if playerName in gift.client.ignoredsList:
                    gift.client.ignoredsList.remove(playerName)
                gift.sendPacket(36, ByteArray().writeInt(rs[1]).writeUTF(Utils.parsePlayerName(playerName)).writeByte(rs[2]).writeInt(rs[1]).writeShort(gift.server.checkConnectedAccount(playerName)).writeInt(4 if isFriend else 0).writeUTF(player.roomName if isFriend and player != None else "").writeInt(rs[3] if isFriend else 0).toByteArray())
                gift.sendPacket(19, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                if player != None:
                    player.tribulle.sendPacket(35, ByteArray().writeInt(gift.client.playerID).writeUTF(gift.client.playerName.lower()).writeByte(gift.client.gender).writeInt(gift.client.playerID).writeByte(1).writeByte(gift.server.checkConnectedAccount(gift.client.playerName)).writeInt(4 if isFriend else 0).writeUTF(gift.client.roomName if isFriend else "").writeInt(gift.client.lastOn if isFriend else 0).toByteArray())
            
        def removeFriend(gift, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray()
            id = gift.server.getPlayerID(playerName)
            player = gift.server.players.get(playerName)

            if playerName in gift.client.friendsList:
                packet.writeInt(id)
                gift.client.friendsList.remove(playerName)
                gift.sendPacket(37, packet.toByteArray())
                gift.sendPacket(21, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                if player != None:
                    player.tribulle.sendPacket(35, ByteArray().writeInt(gift.client.playerID).writeUTF(gift.client.playerName.lower()).writeByte(gift.client.gender).writeInt(gift.client.playerID).writeShort(1).writeInt(0).writeUTF("").writeInt(0).toByteArray())              

        def sendFriendConnected(gift, playerName):
            if playerName in gift.client.friendsList:
                id = gift.server.getPlayerID(playerName)
                player = gift.server.players.get(playerName)
                gift.sendPacket(35, ByteArray().writeInt(player.playerID).writeUTF(playerName.lower()).writeByte(player.gender).writeInt(player.playerID).writeByte(1).writeByte(1).writeInt(1).writeUTF("").writeInt(player.lastOn).toByteArray())
                gift.sendPacket(32, ByteArray().writeUTF(player.playerName.lower()).toByteArray())
                   
        def sendFriendChangedRoom(gift, playerName, langueID):
            if playerName in gift.client.friendsList:
                player = gift.server.players.get(playerName)
                gift.sendPacket(35, ByteArray().writeInt(player.playerID).writeUTF(playerName.lower()).writeByte(player.gender).writeInt(player.playerID).writeByte(1).writeByte(1).writeInt(4).writeUTF(player.roomName).writeInt(player.lastOn).toByteArray())
                    
        def sendFriendDisconnected(gift, playerName):
            if playerName in gift.client.friendsList:
                gift.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [playerName])
                rs = gift.Cursor.fetchone()
                gift.sendPacket(35, ByteArray().writeInt(rs[1]).writeUTF(playerName.lower()).writeByte(rs[2]).writeInt(rs[1]).writeByte(1).writeByte(0).writeInt(1).writeUTF("").writeInt(rs[3]).toByteArray())
                gift.sendPacket(33, ByteArray().writeUTF(playerName.lower()).toByteArray())
                
        def sendIgnoredsList(gift, readPacket):
            tribulleID = readPacket.readInt()
            packet = ByteArray().writeInt(tribulleID).writeShort(len(gift.client.ignoredsList))
            for playerName in gift.client.ignoredsList:
                packet.writeUTF(playerName)
            gift.sendPacket(47, packet.toByteArray())
    
        def ignorePlayer(gift, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            #if not "#" in playerName: playerName += "#0000"
            packet = ByteArray().writeInt(tribulleID)

            if not gift.server.checkExistingUser(playerName):
                gift.sendPacket(43, packet.writeByte(12).toByteArray())
            else:
                gift.client.ignoredsList.append(playerName)

                if playerName in gift.client.friendsList:
                    gift.client.friendsList.remove(playerName)
                gift.sendPacket(43, packet.writeByte(1).toByteArray())

        def removeIgnore(gift, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray().writeInt(tribulleID)

            gift.client.ignoredsList.remove(playerName)
            gift.sendPacket(45, packet.writeByte(1).toByteArray())

        def whisperMessage(gift, readPacket):
            tribulleID, playerName, message = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF()), readPacket.readUTF().replace("\n", "").replace("&amp;#", "&#").replace("<", "&lt;")
            #if not "#" in playerName: playerName += "#0000"
            isCheck = gift.server.checkMessage(gift.client, message)

##            if gift.client.cheeseCount > 3:

            if gift.client.isGuest:
                    gift.client.sendLangueMessage("", "$Créer_Compte_Parler")
                    
            elif not message == "":
                can = True

                packet = ByteArray().writeInt(tribulleID)
                if playerName.startswith("*") or not gift.server.players.has_key(playerName):
                    can = False
                    packet.writeByte(12)
                    packet.writeShort(0)
                    gift.sendPacket(53, packet.toByteArray())
                else:
                    if gift.client.isMute:
                        if not gift.client.isGuest:
                            muteInfo = gift.server.getModMuteInfo(gift.client.playerName)
                            timeCalc = Utils.getHoursDiff(muteInfo[1])
                            if timeCalc <= 0:
                                gift.server.removeModMute(gift.client.playerName)
                            else:
                                can = False
                                gift.client.sendModMute(gift.client.playerName, timeCalc, muteInfo[0], True)

                    if can:
                        player = gift.server.players.get(playerName)
                        if player != None:
                            if player.silenceType != 0:
                                if (gift.client.privLevel >= 3 or (player.silenceType == 2 and gift.checkFriend(playerName, gift.client.playerName))):
                                    pass
                                else:
                                    gift.sendSilenceMessage(playerName, tribulleID)
                                    return

                            if not (gift.client.playerName in player.ignoredsList) and not isCheck:
                                player.tribulle.sendPacket(66, ByteArray().writeUTF(gift.client.playerName.lower()).writeInt(gift.client.langueID+1).writeUTF(player.playerName.lower()).writeUTF(message).toByteArray())
                            gift.sendPacket(66, ByteArray().writeUTF(gift.client.playerName.lower()).writeInt(player.langueID+1).writeUTF(player.playerName.lower()).writeUTF(message).toByteArray())

                            if isCheck:
                                gift.server.sendStaffMessage(7, "<V>%s<BL> está enviando mensagens no cochicho com palavras suspeitas [<R>%s<BL>]." %(gift.client.playerName, message))
                                
                            #if gift.client.privLevel >= 1:
                                #gift.client.sendWhisperMessageAdmin(1, "[WHISPER] [<J>%s</J>] - [<J>%s</J>] - [<J>%s</J>]  - <J>%s</J> => <J>%s</J> : <CH>%s" %(gift.client.ipAddress, gift.client.roomName, gift.client.langue, gift.client.playerName, playerName, message))
                            
                            if not gift.server.chatMessages.has_key(gift.client.playerName):
                                messages = deque([], 60)
                                messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), "> [%s] %s" %(player.playerName, message)])
                                gift.server.chatMessages[gift.client.playerName] = messages
                            else:
                                gift.server.chatMessages[gift.client.playerName].append([_time.strftime("%Y/%m/%d %H:%M:%S"), "> [%s] %s" %(player.playerName, message)])
##            else:
##                 gift.client.sendMessage("<ROSE>You need 3 cheeses to speak.")            

        def disableWhispers(gift, readPacket):
            tribulleID, type, message = readPacket.readInt(), readPacket.readByte(), readPacket.readUTF()
            gift.sendPacket(61, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())

            gift.client.silenceType = type
            gift.client.silenceMessage = "" if gift.server.checkMessage(gift.client, message) else message

        def sendSilenceMessage(gift, playerName, tribulleID):
            player = gift.server.players.get(playerName)
            if player != None:
                gift.sendPacket(53, ByteArray().writeInt(tribulleID).writeByte(25).writeUTF(player.silenceMessage).toByteArray())

        def changeGender(gift, readPacket):
            tribulleID, gender = readPacket.readInt(), readPacket.readByte()
            gift.client.gender = gender
            gift.sendPacket(12, ByteArray().writeInt(tribulleID).writeByte(gender).toByteArray())
            gift.sendPacket(12, ByteArray().writeByte(gender).toByteArray())
            gift.client.sendProfile(gift.client.playerName)
            #for player in gift.server.players.values():
            #    if gift.client.playerName and player.playerName in gift.client.friendsList and player.friendsList:
            #        player.tribulle.sendPacket(11, ByteArray().writeInt(tribulleID).writeByte(gender).toByteArray())

    
        def marriageInvite(gift, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray().writeInt(tribulleID)

            player = gift.server.players.get(playerName)
            if not gift.server.checkConnectedAccount(playerName) or not gift.server.checkExistingUser(playerName):
                gift.sendPacket(23, packet.writeByte(11).toByteArray())
            elif not player.marriage == "":
                gift.sendPacket(23, packet.writeByte(15).toByteArray())
            else:
                if not gift.client.playerName in player.ignoredMarriageInvites:
                    player.marriageInvite = [gift.client.playerName, tribulleID]
                    player.tribulle.sendPacket(38, ByteArray().writeUTF(gift.client.playerName).toByteArray())
                    gift.sendPacket(23, packet.writeByte(1).toByteArray())

    
        def marriageAnswer(gift, readPacket):
            tribulleID, playerName, answer = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF()), readPacket.readByte()

            player = gift.server.players.get(playerName)
            if player != None:
                if answer == 0:
                    gift.sendPacket(25, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                    player.tribulle.sendPacket(40, ByteArray().writeUTF(gift.client.playerName.lower()).toByteArray())

                elif answer == 1:
                    player.marriage = gift.client.playerName
                    gift.client.marriage = player.playerName

                    if not gift.client.playerName in player.friendsList:
                        player.friendsList.append(gift.client.playerName)

                    if not player.playerName in gift.client.friendsList:
                        gift.client.friendsList.append(player.playerName)

                    gift.sendPacket(39, ByteArray().writeUTF(player.playerName.lower()).toByteArray())
                    player.tribulle.sendPacket(39, ByteArray().writeUTF(gift.client.playerName.lower()).toByteArray())

                    if gift.client.openingFriendList:
                        gift.sendFriendsList("0")

                    if player.openingFriendList:
                        player.tribulle.sendFriendsList("0")

                    gift.sendPacket(37, ByteArray().writeInt(player.playerID).toByteArray())
                    player.tribulle.sendPacket(37, ByteArray().writeInt(gift.client.playerID).toByteArray())

                    gift.sendPacket(25, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                    
        def marriageDivorce(gift, readPacket):
            tribulleID = readPacket.readInt()

            time = Utils.getTime() + 3600

            gift.sendPacket(41, ByteArray().writeUTF(gift.client.marriage).writeByte(1).toByteArray())
            player = gift.server.players.get(gift.client.marriage)
            if player != None:
                player.tribulle.sendPacket(41, ByteArray().writeUTF(player.marriage).writeByte(1).toByteArray())
                player.marriage = ""
                player.lastDivorceTimer = time
            else:
                gift.removeMarriage(gift.client.marriage, time)

            gift.client.marriage = ""
            gift.client.lastDivorceTimer = time
            
        def sendTribe(gift, isNew):
            if gift.client.tribeName == "":
                gift.sendPacket(Identifiers.tribulle.send.ET_ErreurInformationsTribu, ByteArray().writeInt(0).writeByte(0).toByteArray())
                return

            if not gift.client.tribeChat in gift.client.chats:
                gift.client.chats.append(gift.client.tribeChat)

            gift.sendPacket(Identifiers.tribulle.send.ET_SignaleRejointCanal, ByteArray().writeInt(gift.client.tribeChat).writeUTF("~" + gift.client.tribeName.lower()).writeBytes(chr(0) * 5).toByteArray())
            gift.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleMembreRejointCanal, ByteArray().writeInt(gift.client.tribeChat).writeInt(gift.client.playerID).writeUTF(gift.client.playerName.lower()).toByteArray())
            gift.sendTribeInfo()

        def sendLoginMessageTribe(gift):
            packet = ByteArray()
            packet.writeInt(0)
            packet.writeInt(0)
            packet.writeInt(0)
            packet.writeInt(0)
            packet.writeInt(0)
            packet.writeShort(1)
            packet.writeInt(0)
            packet.writeShort(0)

            members = gift.getTribeMembers(gift.client.tribeCode)
            packet.writeShort(len(members))

            infos = {}
            gift.Cursor.execute("select Username, PlayerID, Gender, LastOn, TribeRank, TribeJoined from Users where Username in (%s)" %(Utils.joinWithQuotes(members)))
            for rs in gift.Cursor.fetchall():
                infos[rs[0]] = [rs[1], rs[2], rs[3], rs[4], rs[5]]

            for member in members:
                if not infos.has_key(member):
                    continue

                info = infos[member]
                player = gift.server.players.get(member)
                packet.writeInt(info[0])
                packet.writeUTF(member.lower())
                packet.writeByte(info[1])
                packet.writeInt(info[0])
                packet.writeInt(info[2] if not gift.server.checkConnectedAccount(member) else 0)
                packet.writeByte(info[3])
                packet.writeInt(4)
                packet.writeUTF(player.roomName if player != None else "")
            

        def sendTribeInfo(gift, readPacket=""):
                if not readPacket == "":
                    tribulleID, connected = readPacket.readInt(), readPacket.readByte()
                else:
                    tribulleID = gift.client.tribulleID + 1
                    connected = 0
                if gift.client.tribeName == "":
                    gift.sendPacket(109, ByteArray().writeInt(gift.client.tribulleID).writeByte(17).toByteArray())
                    return
                members = gift.getTribeMembers(gift.client.tribeCode)
                packet = ByteArray()
                packet.writeInt(gift.client.tribeCode)
                packet.writeUTF(gift.client.tribeName)
                packet.writeUTF(gift.client.tribeMessage)
                packet.writeInt(gift.client.tribeHouse)
                
                infos = {}
                gift.client.isTribeOpen = True
                gift.Cursor.execute("select Username, PlayerID, Gender, LastOn, TribeRank, TribeJoined from Users where Username in (%s)" %(Utils.joinWithQuotes(members)))
                for rs in gift.Cursor.fetchall():
                    infos[rs[0]] = [rs[1], rs[2], rs[3], rs[4], rs[5]]

                isOnline = []
                isOffline = []

                for member in members:
                    if gift.server.checkConnectedAccount(member):
                        isOnline.append(member)
                    else:
                        isOffline.append(member)

                if connected == 1:
                    playersTribe = isOnline + isOffline
                else:
                    playersTribe = isOnline

                packet.writeShort(len(playersTribe))
                    
                for member in playersTribe:
                    if not infos.has_key(member):
                        continue

                    info = infos[member]
                    player = gift.server.players.get(member)
                    packet.writeInt(info[0])
                    packet.writeUTF(member.lower())
                    packet.writeByte(info[1])
                    packet.writeInt(info[0])
                    packet.writeInt(info[2] if not gift.server.checkConnectedAccount(member) else 0)
                    packet.writeByte(info[3])
                    packet.writeInt(4)
                    packet.writeUTF(player.roomName if player != None else "")

                packet.writeShort(len(gift.client.tribeRanks.split(";")))

                for rank in gift.client.tribeRanks.split(";"):
                    ranks = rank.split("|")
                    packet.writeUTF(ranks[1]).writeInt(ranks[2])

                gift.sendPacket(130, packet.toByteArray())
                gift.client.isBlockAttack = False
                gift.client.blockAttack()
            
        def closeTribe(gift, readPacket):
            tribulleID = readPacket.readInt()
            gift.client.isTribeOpen = False
            gift.sendPacket(111, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())

        def sendTribeMemberConnected(gift):
            gift.sendPacketWholeTribe(88, ByteArray().writeUTF(gift.client.playerName.lower()).toByteArray(), True)
            gift.sendPacketWholeTribe(131, ByteArray().writeInt(gift.client.playerID).writeUTF(gift.client.playerName.lower()).writeByte(gift.client.gender).writeInt(gift.client.playerID).writeInt(0).writeByte(gift.client.tribeRank).writeInt(1).writeUTF("").toByteArray())

        def sendTribeMemberChangeRoom(gift):
            gift.sendPacketWholeTribe(131, ByteArray().writeInt(gift.client.playerID).writeUTF(gift.client.playerName.lower()).writeByte(gift.client.gender).writeInt(gift.client.playerID).writeInt(0).writeByte(gift.client.tribeRank).writeInt(4).writeUTF(gift.client.roomName).toByteArray())

        def sendTribeMemberDisconnected(gift):
            gift.sendPacketWholeTribe(90, ByteArray().writeUTF(gift.client.playerName.lower()).toByteArray())
            gift.sendPacketWholeTribe(131, ByteArray().writeInt(gift.client.playerID).writeUTF(gift.client.playerName.lower()).writeByte(gift.client.gender).writeInt(gift.client.playerID).writeInt(gift.client.lastOn).writeByte(gift.client.tribeRank).writeInt(1).writeUTF("").toByteArray())
            
        def sendPlayerInfo(gift):
            gift.sendPacket(Identifiers.tribulle.send.ET_ReponseDemandeInfosJeuUtilisateur, ByteArray().writeInt(0).writeInt(gift.client.playerID).writeInt(gift.client.playerID).writeInt(gift.getInGenderMarriage(gift.client.playerName)).writeInt(gift.server.getPlayerID(gift.client.marriage) if not gift.client.marriage == "" else 0).writeUTF(gift.client.marriage).toByteArray())

        def createTribe(gift, readPacket):
            tribulleID, tribeName = readPacket.readInt(), readPacket.readUTF()
            createTime = gift.getTime()
            if len(tribeName) > 15:
                gift.client.sendMessage("Max 15 Chararacters")
                return
            if not bool(BeautifulSoup(tribeName, "html.parser").find()):
                gift.sendPacket(85, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                if not gift.checkExistingTribe(tribeName):
                    if gift.client.shopCheeses >= 500:
                        gift.Cursor.execute("insert into Tribe  values(NULL, %s, '', '0', %s, '', %s, %s, 0)", [tribeName, gift.TRIBE_RANKS, gift.client.playerName, gift.server.lastChatID])
                        gift.client.shopCheeses -= 500
                        gift.client.tribeCode = gift.Cursor.lastrowid
                        gift.client.tribeRank = 9
                        gift.client.tribeName = tribeName
                        gift.client.tribeJoined = createTime
                        gift.client.tribeMessage = "Welcome ^-^"
                        gift.client.tribeRanks = gift.TRIBE_RANKS

                        gift.setTribeHistorique(gift.client.tribeCode, 1, createTime, gift.client.playerName, tribeName)

                        gift.client.updateDatabase()

                        gift.sendPacket(89, ByteArray().writeUTF(gift.client.tribeName).writeInt(gift.client.tribeCode).writeUTF(gift.client.tribeMessage).writeInt(0).writeUTF(gift.client.tribeRanks.split(";")[9].split("|")[1]).writeInt(2049).toByteArray())
                    else:
                        gift.sendPacket(85, ByteArray().writeInt(gift.tribulleID).toByteArray())
            else:
                gift.client.sendMessage("<ROSE>Tribename contains HTML.")
        def tribeInvite(gift, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray().writeInt(tribulleID)
            player = gift.server.players.get(playerName)

            if not gift.server.checkConnectedAccount(playerName) or not gift.server.checkExistingUser(playerName):
                gift.sendPacket(79, packet.writeByte(11).toByteArray())
            elif not player.tribeName == "":
                gift.sendPacket(79, packet.writeByte(18).toByteArray())
            else:
                if not gift.client.tribeCode in player.ignoredTribeInvites:
                    player.tribeInvite = [tribulleID, gift.client]
                    player.tribulle.sendPacket(86, ByteArray().writeUTF(gift.client.playerName.lower()).writeUTF(gift.client.tribeName).toByteArray())
                    gift.sendPacket(79, packet.writeByte(1).toByteArray())

        def tribeInviteAnswer(gift, readPacket):
            tribulleID, playerName, answer = readPacket.readInt(), readPacket.readUTF(), readPacket.readByte()
            resultTribulleID = int(gift.client.tribeInvite[0])
            player = gift.client.tribeInvite[1]
            gift.client.tribeInvite = []

            if player != None:

                if answer == 0:
                    gift.client.ignoredTribeInvites.append(player.tribeCode)
                    player.tribulle.sendPacket(87, ByteArray().writeUTF(gift.client.playerName.lower()).writeByte(0).toByteArray())

                elif answer == 1:
                    members = gift.getTribeMembers(player.tribeCode)
                    members.append(gift.client.playerName)
                    gift.setTribeMembers(player.tribeCode, members)

                    gift.client.tribeCode = player.tribeCode
                    gift.client.tribeRank = 0
                    gift.client.tribeName = player.tribeName
                    gift.client.tribeJoined = gift.getTime()
                    tribeInfo = gift.getTribeInfo(gift.client.tribeCode)
                    gift.client.tribeName = str(tribeInfo[0])
                    gift.client.tribeMessage = str(tribeInfo[1])
                    gift.client.tribeHouse = int(tribeInfo[2])
                    gift.client.tribeRanks = tribeInfo[3]
                    gift.client.tribeChat = int(tribeInfo[4])

                    gift.setTribeHistorique(gift.client.tribeCode, 2, gift.getTime(), player.playerName, gift.client.playerName)

                    packet = ByteArray()
                    packet.writeUTF(gift.client.tribeName)
                    packet.writeInt(gift.client.tribeCode)
                    packet.writeUTF(gift.client.tribeMessage)
                    packet.writeInt(gift.client.tribeHouse)

                    rankInfo = gift.client.tribeRanks.split(";")
                    rankName = rankInfo[gift.client.tribeRank].split("|")
                    packet.writeUTF(rankName[1])
                    packet.writeInt(rankName[2])
                    gift.sendPacket(89, packet.toByteArray())
                    player.tribulle.sendPacket(87, ByteArray().writeUTF(gift.client.playerName).writeByte(1).toByteArray())
                    gift.sendPacketWholeTribe(91, ByteArray().writeUTF(gift.client.playerName).toByteArray(), True)
                    for member in members:
                        player = gift.server.players.get(member)
                        if player != None:
                            if player.isTribeOpen:
                                player.tribulle.sendTribeInfo()

        def changeTribeMessage(gift, readPacket):
            tribulleID, message = readPacket.readInt(), readPacket.readUTF()
            gift.Cursor.execute("update Tribe set Message = %s where Code = %s", [message, gift.client.tribeCode])
            gift.client.tribeMessage = message
            gift.setTribeHistorique(gift.client.tribeCode, 6, gift.getTime(), message, gift.client.playerName)
            gift.updateTribeData()
            gift.sendTribeInfo()
            gift.sendPacketWholeTribe(125, ByteArray().writeUTF(gift.client.playerName.lower()).writeUTF(message).toByteArray(), True)
            
        def changeTribeCode(gift, readPacket):
            tribulleID, mapCode = readPacket.readInt(), readPacket.readInt()
            gift.Cursor.execute("update Tribe set House = %s where Code = %s", [mapCode, gift.client.tribeCode])
            
            mapInfo = gift.client.room.getMapInfo(mapCode)
            if mapInfo[0] == None:
                gift.client.sendPacket(Identifiers.old.send.Tribe_Result, [16])
            elif mapInfo[4] != 22 and mapInfo[4] != 0 and mapInfo[4] != 1 and mapInfo[4] != 2 and mapInfo[4] != 3 and mapInfo[4] != 4 and mapInfo[4] != 5 and mapInfo[4] != 6 and mapInfo[4] != 7 and mapInfo[4] != 8 and mapInfo[4] != 9 and mapInfo[4] != 10 and mapInfo[4] != 11 and mapInfo[4] != 13 and mapInfo[4] != 17 and mapInfo[4] != 18 and mapInfo[4] != 19 and mapInfo[4] != 22 and mapInfo[4] != 41 and mapInfo[4] != 42 and mapInfo[4] != 44:
            #elif mapInfo[4] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 41, 42, 44]:
                gift.client.sendPacket(Identifiers.old.send.Tribe_Result, [17])

            elif mapInfo[0] != None and mapInfo[4] == 22:
                gift.setTribeHistorique(gift.client.tribeCode, 8, gift.getTime(), gift.client.playerName, mapCode)
                    
            room = gift.server.rooms.get("*\x03" + gift.client.tribeName)
            if room != None:
                room.mapChange()

            gift.updateTribeData()
            gift.sendTribeInfo()

        def createNewTribeRank(gift, readPacket):
            tribulleID, rankName = readPacket.readInt(), readPacket.readUTF()

            ranksID = gift.client.tribeRanks.split(";")
            s = ranksID[1]
            f = ranksID[1:]
            f = ";".join(map(str, f))
            s = "%s|%s|%s" % ("0", rankName, "0")
            del ranksID[1:]
            ranksID.append(s)
            ranksID.append(f)
            gift.client.tribeRanks = ";".join(map(str, ranksID))
            members = gift.getTribeMembers(gift.client.tribeCode)
            for playerName in members:
                player = gift.server.players.get(playerName)
                tribeRank = gift.getPlayerTribeRank(playerName)
                if player != None:
                    if player.tribeRank >= 1:
                        player.tribeRank += 1
                        gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [tribeRank+1, playerName])
                else:
                    if tribeRank >= 1:
                        gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [tribeRank+1, playerName])

            gift.updateTribeRanks()
            gift.updateTribeData()
            gift.sendTribeInfo()
            for member in members:
                player = gift.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def deleteTribeRank(gift, readPacket):
            tribulleID, rankID = readPacket.readInt(), readPacket.readByte()

            rankInfo = gift.client.tribeRanks.split(";")
            del rankInfo[rankID]
            gift.client.tribeRanks = ";".join(map(str, rankInfo))

            gift.updateTribeRanks()
            gift.updateTribeData()

            members = gift.getTribeMembers(gift.client.tribeCode)
            for playerName in members:
                player = gift.server.players.get(playerName)
                if player != None:
                    if player.tribeRank == rankID:
                        player.tribeRank = 0
                    else:
                        continue
                else:
                    tribeRank = gift.getPlayerTribeRank(playerName)
                    if tribeRank == rankID:
                        gift.Cursor.execute("update users set TribeRank = 0 where Username = %s", [playerName])
                    else:
                        continue
            for playerName in members:
                player = gift.server.players.get(playerName)
                tribeRank = gift.getPlayerTribeRank(playerName)
                if player != None:
                    if player.tribeRank >= 1:
                        player.tribeRank -= 1
                        gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [tribeRank-1, playerName]) 
                else:
                    if tribeRank >= 1:
                        gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [tribeRank-1, playerName]) 
            gift.sendTribeInfo()
            for member in members:
                player = gift.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()
            
        def renameTribeRank(gift, packet):
            tribulleID, rankID, rankName = packet.readInt(), packet.readByte(), packet.readUTF()
            rankInfo = gift.client.tribeRanks.split(";")
            rank = rankInfo[rankID].split("|")
            rank[1] = rankName
            rankInfo[rankID] = "|".join(map(str, rank))
            gift.client.tribeRanks = ";".join(map(str, rankInfo))
            gift.updateTribeRanks()
            gift.updateTribeData()
            gift.sendTribeInfo()
            members = gift.getTribeMembers(gift.client.tribeCode)
            for member in members:
                player = gift.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def changeRankPosition(gift, packet):
            if gift.client.isBlockAttack:
                tribulleID, rankID, rankID2 = packet.readInt(), packet.readByte(), packet.readByte()
                ranks = gift.client.tribeRanks.split(";")
                rank = ranks[rankID]
                rank2 = ranks[rankID2]
                ranks[rankID] = rank2
                ranks[rankID2] = rank
                gift.client.tribeRanks = ";".join(map(str, ranks))
                gift.updateTribeRanks()
                gift.updateTribeData()
                up = (rankID2 > rankID)
                down = (rankID > rankID2)
                members = gift.getTribeMembers(gift.client.tribeCode)
                for member in members:
                    player = gift.server.players.get(member)
                    if player != None:
                        if player.tribeRank == rankID:
                            player.tribeRank = rankID2
                            gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID2, member])
                        if up:
                            if player.tribeRank == rankID2:
                                player.tribeRank -= 1
                                gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID2 - 1, member])
                        if down:
                            if player.tribeRank == rankID2:
                                player.tribeRank += 1
                                gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID2 + 1, member])
                    else:   
                        gift.Cursor.execute("select TribeRank from users where Username = %s", [member])
                        rankPlayer = gift.Cursor.fetchone()[0]

                        if rankPlayer == rankID:
                            gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID2, member])
                        if up:
                            if rankPlayer == rankID2:
                                gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID2 - 1, member])
                        if down:
                            if rankPlayer == rankID2:
                                gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID2 + 1, member])
                    
                gift.updateTribeRanks()
                gift.updateTribeData()
                gift.sendTribeInfo()
                gift.client.isBlockAttack = False
                gift.client.blockAttack()
                for member in members:
                    player = gift.server.players.get(member)
                    if player != None:
                        if player.isTribeOpen:
                            player.tribulle.sendTribeInfo()

        def setRankPermition(gift, packet):
            if gift.client.isBlockAttack:
                tribulleID, rankID, permID, type = packet.readInt(), packet.readByte(), packet.readInt(), packet.readByte()
                rankInfo = gift.client.tribeRanks.split(";")
                perms = rankInfo[rankID].split("|")
                soma = 0
                if type == 0:
                    soma = int(perms[2]) + 2**permID
                elif type == 1:
                    soma = int(perms[2]) - 2**permID
                perms[2] = str(soma)
                join = "|".join(map(str, perms))
                rankInfo[rankID] = join
                gift.client.tribeRanks = ";".join(map(str, rankInfo))
                gift.updateTribeRanks()
                gift.updateTribeData()
                gift.sendTribeInfo()
                gift.client.isBlockAttack = False
                gift.client.blockAttack()
                members = gift.getTribeMembers(gift.client.tribeCode)
                for member in members:
                    player = gift.server.players.get(member)
                    if player != None:
                        if player.isTribeOpen:
                            player.tribulle.sendTribeInfo()

        def changeTribePlayerRank(gift, packet):
            tribulleID, playerName, rankID = packet.readInt(), packet.readUTF(), packet.readByte()

            rankInfo = gift.client.tribeRanks.split(";")
            rankName = rankInfo[rankID].split("|")[1]

            player = gift.server.players.get(playerName)
            gift.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [playerName])
            rs = gift.Cursor.fetchone()
            if player != None:
                player.tribeRank = rankID
                gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID, playerName])
            else:
                gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID, playerName])
            gift.setTribeHistorique(gift.client.tribeCode, 5, gift.getTime(), playerName, str(rankID), rankName, gift.client.playerName)
            gift.sendPacket(131, ByteArray().writeInt(rs[1]).writeUTF(playerName.lower()).writeByte(rs[2]).writeInt(rs[1]).writeInt(0 if gift.server.checkConnectedAccount(playerName) else rs[3]).writeByte(rankID).writeInt(1).writeUTF("" if player == None else player.roomName).toByteArray())
            gift.sendPacketWholeTribe(124, ByteArray().writeUTF(gift.client.playerName.lower()).writeUTF(playerName.lower()).writeUTF(rankName).toByteArray(), True)
            gift.sendPacket(113, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
            members = gift.getTribeMembers(gift.client.tribeCode)
            for member in members:
                player = gift.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def showTribeHistorique(gift, readPacket):
            tribulleID, sla, sla2 = readPacket.readInt(), readPacket.readInt(), readPacket.readInt()

            historique = gift.getTribeHistorique(gift.client.tribeCode).split("|")
            
            packet = ByteArray()
            packet.writeInt(tribulleID)
            packet.writeShort(len(historique) - 1 if historique == [''] else len(historique))
            for event in historique:
                event = event.split("/")
                if not historique == [''] and not event[1] == '':
                    packet.writeInt(event[1])
                    packet.writeInt(event[0])
                    if int(event[0]) == 8:
                        packet.writeUTF('{"code":"%s","auteur":"%s"}' % (event[3], event[2]))
                    elif int(event[0]) == 6:
                        try:
                            packet.writeUTF('{"message":"%s","auteur":"%s"}' % (event[2], event[3]))
                        except:
                            pass
                    elif int(event[0]) == 5:
                        packet.writeUTF('{"cible":"%s","ordreRang":"%s","rang":"%s","auteur":"%s"}' % (event[2], event[3], event[4], event[5]))
                    elif int(event[0]) == 4:
                        packet.writeUTF('{"membreParti":"%s","auteur":"%s"}' % (event[2], event[2]))
                    elif int(event[0]) == 3:
                        packet.writeUTF('{"membreExclu":"%s","auteur":"%s"}' % (event[2], event[3]))
                    elif int(event[0]) == 2:
                        packet.writeUTF('{"membreAjoute":"%s","auteur":"%s"}' % (event[3], event[2]))
                    elif int(event[0]) == 1:
                        packet.writeUTF('{"tribu":"%s","auteur":"%s"}' % (event[3], event[2]))

            packet.writeInt(len(historique))
            
            gift.sendPacket(133, packet.toByteArray())
    
        def leaveTribe(gift, packet):
            tribulleID = packet.readInt()
            p = ByteArray().writeInt(tribulleID)

            if gift.client.tribeRank == (len(gift.client.tribeRanks.split(";"))-1):
                p.writeByte(4)
            else:
                p.writeByte(1)
                
                gift.sendPacketWholeTribe(92, ByteArray().writeUTF(gift.client.playerName.lower()).toByteArray(), True)

                members = gift.getTribeMembers(gift.client.tribeCode)
                if gift.client.playerName in members:
                    members.remove(gift.client.playerName)
                    gift.setTribeMembers(gift.client.tribeCode, members)

                    gift.setTribeHistorique(gift.client.tribeCode, 4, gift.getTime(), gift.client.playerName)
                    
                    gift.client.tribeCode = 0
                    gift.client.tribeName = ""
                    gift.client.tribeRank = 0
                    gift.client.tribeJoined = 0
                    gift.client.tribeHouse = 0
                    gift.client.tribeMessage = ""
                    gift.client.tribeRanks = ""
                    gift.client.tribeChat = 0
                for member in members:
                    player = gift.server.players.get(member)
                    if player != None:
                        if player.isTribeOpen:
                            player.tribulle.sendTribeInfo()
            gift.sendPacket(83, p.toByteArray())

        def kickPlayerTribe(gift, packet):
            tribulleID, playerName = packet.readInt(), packet.readUTF()
            p = ByteArray().writeInt(tribulleID)
            player = gift.server.players.get(playerName)

            tribeCode = player.tribeCode if player != None else gift.getPlayerTribeCode(playerName)

            if tribeCode != 0:
                p.writeByte(1)
                members = gift.getTribeMembers(gift.client.tribeCode)
                if playerName in members:
                    members.remove(playerName)
                    gift.setTribeMembers(gift.client.tribeCode, members)
                    
                    gift.setTribeHistorique(gift.client.tribeCode, 3, gift.getTime(), playerName, gift.client.playerName)
                    gift.sendPacketWholeTribe(93, ByteArray().writeUTF(playerName.lower()).writeUTF(gift.client.playerName.lower()).toByteArray(), True)

                    if player != None:
                        player.tribeCode = 0
                        player.tribeName = ""
                        player.tribeRank = 0
                        player.tribeJoined = 0
                        player.tribeHouse = 0
                        player.tribeMessage = ""
                        player.tribeRanks = ""
                        player.tribeChat = 0
                    else:
                        gift.Cursor.execute("update users set TribeCode = 0, TribeRank = 0, TribeJoined = 0 where Username = %s", [playerName])
                members = gift.getTribeMembers(gift.client.tribeCode)
                for member in members:
                    player = gift.server.players.get(member)
                    if player != None:
                        if player.isTribeOpen:
                            player.tribulle.sendTribeInfo()
            gift.sendPacket(105, p.toByteArray())

        def setTribeMaster(gift, packet):
            tribulleID, playerName = packet.readInt(), packet.readUTF()

            rankInfo = gift.client.tribeRanks.split(";")
            gift.client.tribeRank = (len(rankInfo)-2)
            gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [len(rankInfo)-2, gift.client.playerName])
            player = gift.server.players.get(playerName)
            if player != None:
                player.tribeRank = (len(rankInfo)-1)
                gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [len(rankInfo)-1, playerName])
            else:
                gift.Cursor.execute("update users set TribeRank = %s where Username = %s", [len(rankInfo)-1, playerName])
            gift.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [playerName])
            rs = gift.Cursor.fetchone()
            gift.sendPacket(131, ByteArray().writeInt(rs[1]).writeUTF(playerName.lower()).writeByte(rs[2]).writeInt(rs[1]).writeInt(0 if gift.server.checkConnectedAccount(playerName) else rs[3]).writeByte(len(rankInfo)-1).writeInt(4).writeUTF("" if player == None else player.roomName).toByteArray())
            gift.sendPacket(131, ByteArray().writeInt(gift.client.playerID).writeUTF(gift.client.playerName.lower()).writeByte(gift.client.gender).writeInt(gift.client.playerID).writeInt(0).writeByte(len(rankInfo)-2).writeInt(4).writeUTF(gift.client.roomName).toByteArray())
            gift.sendPacket(127, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
            members = gift.getTribeMembers(gift.client.tribeCode)
            for member in members:
                player = gift.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def finishTribe(gift, packet):
            tribulleID = packet.readInt()
            p = ByteArray()
            p.writeInt(tribulleID).writeByte(1)
            members = gift.getTribeMembers(gift.client.tribeCode)
            gift.Cursor.execute("update users set TribeCode = 0, TribeRank = 0, TribeJoined = 0 where TribeCode = %s", [gift.client.tribeCode])
            gift.Cursor.execute("delete from Tribe where Code = %s", [gift.client.tribeCode])
            for member in members:
                player = gift.server.players.get(member)
                if player != None:
                    player.tribulle.sendPacket(93, ByteArray().writeUTF(player.playerName.lower()).writeUTF(gift.client.playerName.lower()).toByteArray())
                    player.tribeCode, player.tribeRank, player.tribeJoined, player.tribeHouse, player.tribeChat, player.tribeRankID = 0, 0, 0, 0, 0, 0
                    player.tribeMessage, player.tribeName = "", ""
                    player.tribeRanks = ""
                    player.tribeInvite = []
                    player.tribulle.sendPacket(127, p.toByteArray())
                gift.client.sendPacket([6, 9], ByteArray().writeUTF("Tribe distributed.").toByteArray())

        def customChat(gift, packet):
            tribulleID, chatName = packet.readInt(), packet.readUTF()

            if re.match("^[ a-zA-Z0-9]*$", chatName):
                chatID = gift.getChatID(chatName)
                if chatID == -1:
                    chatID = gift.server.lastChatID + 1
                    gift.server.configs("ids.lastChatID", str(chatID))
                    gift.Cursor.execute("insert into Chats (ID, Name) values (%s, %s)", [chatID, chatName])

                chatID = gift.getChatID(chatName)

                gift.client.chats.append(chatID)
                gift.sendPacket(62, ByteArray().writeUTF(chatName).toByteArray())
                gift.sendPacket(55, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
            else:
                gift.sendPacket(55, ByteArray().writeInt(tribulleID).writeByte(8).toByteArray())

        
            
        def chatMessage(gift, packet):
            tribulleID, chatName, message = packet.readInt(), packet.readUTF(), packet.readUTF()
            chatID = gift.getChatID(chatName)
            gift.sendPacketWholeChat(chatID, 64, ByteArray().writeUTF(gift.client.playerName.lower()).writeInt(gift.client.langueID+1).writeUTF(chatName).writeUTF(message).toByteArray(), True)
            gift.sendPacket(49, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
            #gift.client.sendWhisperMessageAdmin(1, "[<J>%s</J>] [<J>%s</J>] [<J>CHAT</J>] - %s => %s" %(gift.client.ipAddress, chatName, gift.client.playerName, message))
            
        def chatMembersList(gift, packet):
            tribulleID, chatName = packet.readInt(), packet.readUTF()
            p = ByteArray().writeInt(tribulleID).writeByte(1)
            chatID = gift.getChatID(chatName)
            length = 0
            for player in gift.server.players.values():
                if chatID in player.chats:
                    length += 1
            p.writeShort(length)

            for player in gift.server.players.values():
                if chatID in player.chats:
                    p.writeUTF(player.playerName)
            gift.sendPacket(59, p.toByteArray())

        def sendTribeChatMessage(gift, readPacket):
            tribulleID, message = readPacket.readInt(), readPacket.readUTF()
            gift.sendPacketWholeTribe(65, ByteArray().writeUTF(gift.client.playerName.lower()).writeUTF(message).toByteArray(), True)
            #gift.client.sendWhisperMessageAdmin(1, "[TRIBECHAT] [<J>%s</J>] - [<J>%s</J>] - [%s]: <CH>%s" %(gift.client.ipAddress, gift.client.tribeName, gift.client.playerName, message))

        def getGenderID(gift, genderID, isFriendToo, isMarriedWithMe):
            dictionary = {0:{0:{0:0, 1:1}, 1:{0:2, 1:3}}, 1:{0:{0:4, 1:5}, 1:{0:6, 1:7}}, 2:{0:{0:8, 1:9}, 1:{0:10, 1:11}}}
            return dictionary[genderID][int(isMarriedWithMe)][int(isFriendToo)]

        def getPlayerLastOn(gift, playerName):
            player = gift.server.players.get(playerName)
            if player != None:
                return gift.server.players[playerName].lastOn
            else:
                gift.Cursor.execute("select LastOn from Users where Username = %s", [playerName])
                rs = gift.Cursor.fetchone()
                if rs:
                    return rs[0]
                else:
                    return 0

        def checkFriend(gift, playerName, playerNameToCheck):
            checkList = gift.server.players[playerName].friendsList if gift.server.players.has_key(playerName) else gift.getUserFriends(playerName)
            return playerNameToCheck in checkList

        def getUserFriends(gift, playerName):
            gift.Cursor.execute("select FriendsList from Users where Username = %s", [playerName])
            rs = gift.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return []

        def getPlayerGender(gift, playerName):
            gift.Cursor.execute("select Gender from Users where Username = %s", [playerName])
            rs = gift.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

        def getPlayerTribeRank(gift, playerName):
            gift.Cursor.execute("select TribeRank from users where Username = %s", [playerName])
            rs = gift.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

        def getPlayerMarriage(gift, playerName):
            gift.Cursor.execute("select Marriage from Users where Username = %s", [playerName])
            rs = gift.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return ""

        def removeMarriage(gift, playerName, time):
            gift.Cursor.execute("update Users set Marriage = '', LastDivorceTimer = %s where Username = %s", [time, playerName])

        def getInGenderMarriage(gift, playerName):
            if gift.server.players.has_key(playerName):
                player = gift.server.players.get(playerName)
                gender = player.gender
                marriage = player.marriage
            else:
                gender = gift.getPlayerGender(playerName)
                marriage = gift.getPlayerMarriage(playerName)
            return (5 if gender == 1 else 9 if gender == 2 else 1) if marriage == "" else (7 if gender == 1 else 11 if gender == 2 else 3)

        def getInGendersMarriage(gift, marriage, gender):
            return (5 if gender == 1 else 9 if gender == 2 else 1) if marriage == "" else (7 if gender == 1 else 11 if gender == 2 else 3)

        def updateTribeRanks(gift):
            gift.Cursor.execute("update tribe set Ranks = %s where Code = %s", [gift.client.tribeRanks, gift.client.tribeCode])

        def getTribeMembers(gift, tribeCode):
            gift.Cursor.execute("select Members from Tribe where Code = %s", [tribeCode])
            rs = gift.Cursor.fetchone()
            if rs:
                return rs[0].split(",")
            else:
                return []

        def setTribeMembers(gift, tribeCode, members):
            gift.Cursor.execute("update Tribe set Members = %s where Code = %s", [",".join(map(str, members)), tribeCode])

        def checkExistingTribe(gift, tribeName):
            gift.Cursor.execute("select 1 from Tribe where Name = %s", [tribeName])
            return gift.Cursor.fetchone() != None

        def checkExistingTribeRank(gift, rankName):
            for rank in gift.client.tribeRanks.values():
                checkRankName = rank.split("|")[0]
                if checkRankName == rankName:
                    return True
            return False

        def getTribeHistorique(gift, tribeCode):
            gift.Cursor.execute("select Historique from Tribe where Code = %s", [tribeCode])
            rs = gift.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return ""

        def setTribeCache(gift, tribeCode, historique):
            gift.Cursor.execute("update Tribe set historique = %s where Code = %s", [historique, tribeCode])

        def setTribeHistorique(gift, tribeCode, *data):
            historique = gift.getTribeHistorique(tribeCode)
            if historique == "":
                historique = "/".join(map(str, data))
            else:
                historique = "/".join(map(str, data)) + "|" + historique
            gift.setTribeCache(tribeCode, historique)

        def getChatID(gift, chatName):
            gift.Cursor.execute("select ID from Chats where Name = %s", [chatName])
            rs = gift.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return -1

        def getPlayerTribeCode(gift, playerName):
            gift.Cursor.execute("select TribeCode from users where Username = %s", [playerName])
            rs = gift.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

        def getTribeInfo(gift, tribeCode):
            tribeRanks = ""
            gift.Cursor.execute("select * from tribe where Code = %s", [tribeCode])
            rs = gift.Cursor.fetchone()
            if rs:
                tribeRanks = rs[4]
                return [rs[1], rs[2], rs[3], tribeRanks, rs[7]]
            else:
                return ["", "", 0, tribeRanks, 0]
    except:
        pass
