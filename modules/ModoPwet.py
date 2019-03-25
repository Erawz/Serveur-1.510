from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
import math

class ModoPwet:

    def __init__(gift, player, server):
        gift.client = player
        gift.server = player.server

    def checkReport(gift, array, playerName):
        return playerName in array

    def makeReport(gift, playerName, type, comments):
        playerName = Utils.parsePlayerName(playerName)
        repatan = gift.client.playerName         
        gift.server.sendStaffMessage(8, '[REPORT] [<V>%s</V>] a report <V>[%s]</V> pour la raison suivante: <J>%s</J> -> <V>%s</V>' % (repatan,playerName,{0:"Hack", 1:"Spam / Flood", 2:"Insultes", 3:"Pishing", 4:"Autre"}[type],'-' if comments == '' else comments))

        if gift.server.players.get(playerName):
            if gift.server.reports.has_key(playerName):
                if gift.server.reports[playerName]['reporters'].has_key(repatan):
                    r = gift.server.reports[playerName]['reporters'][repatan]
                    if r[0] != type:
                        gift.server.reports[playerName]['reporters'][repatan]=[type,comments,Utils.getTime()]
                        
                else:
                    gift.server.reports[playerName]['reporters'][repatan]=[type,comments,Utils.getTime()]
                gift.server.reports[playerName]['durum'] = 'En-ligne' if gift.server.checkConnectedAccount(playerName) else 'disconnected'
            else:
                gift.server.reports[playerName] = {}
                gift.server.reports[playerName]['reporters'] = {repatan:[type,comments,Utils.getTime()]}
                gift.server.reports[playerName]['durum'] = 'En-ligne' if gift.server.checkConnectedAccount(playerName) else 'disconnected'
                gift.server.reports[playerName]['dil'] = gift.getModopwetLangue(playerName)
                gift.server.reports[playerName]['isMuted'] = False
            gift.updateModoPwet()
            gift.client.sendBanConsideration()

    def getModopwetLangue(gift, playerName):
        player = gift.server.players.get(playerName)
        if player != None:
            return player.langue
        else:
            return 'EN'

    def updateModoPwet(gift):
        for player in gift.server.players.values():
            if player.isModoPwet and player.privLevel >= 5:
                player.modoPwet.openModoPwet(True)

    def getPlayerRoomName(gift, playerName):
        player = gift.server.players.get(playerName)
        if player != None:
            return player.roomName
        else:
            return '0'
            
    def getRoomMods(gift,room):
        s = []
        i = ""
        for player in gift.server.players.values():
            if player.roomName == room and player.privLevel >= 5:
                s.append(player.playerName)
                
        if len(s) == 1:
            return s[0]
        else:
            for isim in s:
                i = i+isim+", "
        return i
        
    def getPlayerKarma(gift, playerName):
        player = gift.server.players.get(playerName)
        if player:
            return player.playerKarma
        else:
            return 0
    
    def banHack(gift, playerName,iban):
        if gift.server.banPlayer(playerName, 360, "Hack (last warning before account deletion)", gift.client.playerName, iban):
            gift.server.sendStaffMessage(5, "<V>%s<BL> a banni <V>%s<BL> pendant <V>360 <BL>heures. Raison: <V>Hack (last warning before account deletion)<BL>." %(gift.client.playerName, playerName))
        gift.updateModoPwet()
        
    def deleteReport(gift,playerName,handled):
        if handled == 0:
            gift.server.reports[playerName]["durum"] = "deleted"
            gift.server.reports[playerName]["deletedby"] = gift.client.playerName
        else:
            if gift.server.reports.has_key(playerName):
                del gift.server.reports[playerName]
                
        gift.updateModoPwet()
        
    def sirala(gift,verilen):
        for i in verilen[1]["reporters"]:
            return verilen[1]["reporters"][i][2]
            
    def sortReports(gift,reports,sort):  
        if sort:
            return sorted(reports.items(), key=gift.sirala,reverse=True)
        else:
            return sorted(reports.items(), key=lambda (x): len(x[1]["reporters"]),reverse=True)
    
    def openModoPwet(gift,isOpen=False,modopwetOnlyPlayerReports=False,sortBy=False):
        if isOpen:
            if len(gift.server.reports) <= 0:
                gift.client.sendPacket(Identifiers.send.Modopwet_Open, 0)
            else:
                gift.client.sendPacket(Identifiers.send.Modopwet_Open, 0)
                reports,bannedList,deletedList,disconnectList = gift.sortReports(gift.server.reports,sortBy),{},{},[]
                sayi = 0
                p = ByteArray()  
                for i in reports:
                    isim = i[0]
                    v = gift.server.reports[isim]
                    if gift.client.modoPwetLangue == 'ALL' or v["dil"] == gift.client.modoPwetLangue:
                        oyuncu = gift.server.players.get(isim)
                        saat = math.floor(oyuncu.playerTime/3600) if oyuncu else 0
                        odaisim = oyuncu.roomName if oyuncu else "0"
                        sayi += 1
                        gift.client.lastReportID += 1
                        if sayi >= 255:
                            break  
                        p.writeByte(sayi)
                        p.writeShort(gift.client.lastReportID)
                        p.writeUTF(v["dil"])
                        p.writeUTF(isim)
                        p.writeUTF(odaisim)
                        p.writeByte(1) # alttaki modname uzunlugu ile alakali
                        p.writeUTF(gift.getRoomMods(odaisim))
                        p.writeInt(saat) #idk
                        p.writeByte(int(len(v["reporters"])))
                        for name in v["reporters"]:
                            r = v["reporters"][name]
                            p.writeUTF(name)
                            p.writeShort(gift.getPlayerKarma(name)) #karma
                            p.writeUTF(r[1])
                            p.writeByte(r[0])
                            p.writeShort(int(Utils.getSecondsDiff(r[2])/60)) #05m felan rep suresi
                                
                        mute = v["isMuted"]
                        p.writeBoolean(mute) #isMute
                        if mute:
                            p.writeUTF(v["mutedBy"])
                            p.writeShort(v["muteHours"])
                            p.writeUTF(v["muteReason"])
                            
                        if v['durum'] == 'banned':
                            x = {}
                            x['banhours'] = v['banhours']
                            x['banreason'] = v['banreason']
                            x['bannedby'] = v['bannedby']
                            bannedList[isim] = x
                        if v['durum'] == 'deleted':
                            x = {}
                            x['deletedby'] = v['deletedby']
                            deletedList[isim] = x
                        if v['durum'] == 'disconnected':
                            disconnectList.append(isim)

                gift.client.sendPacket(Identifiers.send.Modopwet_Open, ByteArray().writeByte(int(len(reports))).writeBytes(p.toByteArray()).toByteArray())
                for user in disconnectList:
                    gift.changeReportStatusDisconnect(user)

                for user in deletedList.keys():
                    gift.changeReportStatusDeleted(user, deletedList[user]['deletedby'])

                for user in bannedList.keys():
                    gift.changeReportStatusBanned(user, bannedList[user]['banhours'], bannedList[user]['banreason'], bannedList[user]['bannedby'])

    def changeReportStatusDisconnect(gift, playerName):
        gift.client.sendPacket(Identifiers.send.Modopwet_Disconnected, ByteArray().writeUTF(playerName).toByteArray())

    def changeReportStatusDeleted(gift, playerName, deletedby):
        gift.client.sendPacket(Identifiers.send.Modopwet_Deleted, ByteArray().writeUTF(playerName).writeUTF(deletedby).toByteArray())

    def changeReportStatusBanned(gift, playerName, banhours, banreason, bannedby):
        gift.client.sendPacket(Identifiers.send.Modopwet_Banned, ByteArray().writeUTF(playerName).writeUTF(bannedby).writeInt(int(banhours)).writeUTF(banreason).toByteArray())

    def openChatLog(gift, playerName):
        if gift.server.chatMessages.has_key(playerName):
            packet = ByteArray().writeUTF(playerName).writeByte(len(gift.server.chatMessages[playerName]))
            for message in gift.server.chatMessages[playerName]:
                packet.writeUTF(message[1]).writeUTF(message[0])
            gift.client.sendPacket(Identifiers.send.Modopwet_Chatlog, packet.toByteArray())
