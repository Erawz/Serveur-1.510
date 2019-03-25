#coding: utf-8
#Imp - Gifted
import re, sys, base64, hashlib, time as _time, random as _random

# Modules
from time import gmtime, strftime
from langues import Langues
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

# Library
from datetime import datetime

class ParseCommands:
    def __init__(gift, client, server):
        gift.client = client
        gift.server = client.server
        gift.Cursor = client.Cursor
        gift.currentArgsCount = 0

    def requireNoSouris(gift, playerName):
        if not playerName.startswith("*"):
            return True

    def requireArgs(gift, argsCount):
        if gift.currentArgsCount < argsCount:
            gift.client.sendMessage("Arguments invalides.")
            return False

        return True
    
    def requireTribe(gift, canUse=False, tribePerm=8):
        if (not(not gift.client.tribeName == "" and gift.client.room.isTribeHouse and tribePerm != -1 and gift.client.tribeRanks[gift.client.tribeRank].split("|")[2].split(",") [tribePerm] == "1")) if (argsCount >= 1) else "":
            canUse = True              

    def parseCommand(gift, command):                
        values = command.split(" ")
        gifted = command
        command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        argsNotSplited = " ".join(args)
        gift.currentArgsCount = argsCount
        gift.Cursor.execute("insert into commandlog values (%s, %s, %s)", [Utils.getTime(), gift.client.playerName, gifted])
        #if gift.client.privLevel >= 1:
            #gift.client.sendLuaMessageAdmin("<font color='#A566A9'>[%s]</font> - <font color='#A566A9'>[%s]</font><font color='#E35A4F'> write command: <CH>/%s" %(gift.client.ipAddress, gift.client.playerName, command))
        try:
            if command in ["profil", "perfil", "profile"]:
                if gift.client.privLevel >= 1:
                    gift.client.sendProfile(Utils.parsePlayerName(args[0]) if len(args) >= 1 else gift.client.playerName)
			
	    elif command in ["editeur", "editor"]:
                if gift.client.privLevel >= 1:
                    gift.client.sendPacket(Identifiers.send.Room_Type, 1)
                    gift.client.enterRoom("\x03[Editeur] %s" %(gift.client.playerName))
                    gift.client.sendPacket(Identifiers.old.send.Map_Editor, [])

	    elif command in ["chatlog"]:
                if gift.client.privLevel >= 7 and len(args) == 1:
                    gift.client.openChatLog(Utils.parsePlayerName(args[0]))


            elif command in ["vbot", "virarbot", "tfbot"]:
                if gift.client.privLevel >= 11:
                    botName = gift.client.playerName
                    botLook = gift.client.playerLook
                    botTitle = gift.client.titleNumber
                    otherPlayer = False

                    if len(args) >= 1:
                        botName = Utils.parsePlayerName(args[0])
                    if len(args) >= 2:
                        if ";" in args[1]:
                            botLook = args[1]
                        else:
                            otherPlayer = True if int(args[1]) == 1 or str(args[1]) == "1" else False
                    if len(args) == 3:
                        botTitle = int(args[2])

                    for client in gift.client.room.clients.values():
                        if otherPlayer:
                            if botName == client.playerName:
                                if client.privLevel >= gift.client.privLevel:
                                    gift.client.sendMessage("")
                                else:
                                    client.room.sendAll([8, 30], ByteArray().writeInt(client.playerCode).writeUTF(client.playerName).writeShort(client.titleNumber).writeByte(0).writeUTF(client.playerLook).writeShort(client.posX).writeShort(client.posY).writeShort(11).writeByte(250).writeShort(0).toByteArray())
                        else:
                            client.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF(botName).writeShort(botTitle).writeBoolean(True).writeUTF(botLook).writeShort(gift.client.posX).writeShort(gift.client.posY).writeShort(1).writeByte(11).writeShort(0).toByteArray())
                            gift.sendServerMessageAdmin("Bot name  => %s i, Bot Title => %s, Bot Look => %s" %(botName, botTitle, botLook)) 
            

            elif command in ["luaadmin"]:
                if gift.client.playerName in ["Loveditoi"]:
                    gift.client.isLuaAdmin = not gift.client.isLuaAdmin
                    gift.client.sendMessage("You can run scripts as administrator." if gift.client.isLuaAdmin else "You can not run scripts as administrator anymore.")
    
            elif command in ["time", "temps"]:
                if gift.client.privLevel >= 1:
                    gift.client.playerTime += abs(Utils.getSecondsDiff(gift.client.loginTime))
                    gift.client.loginTime = Utils.getTime()
                    gift.client.sendLangueMessage("", "$TempsDeJeu", gift.client.playerTime / 86400, gift.client.playerTime / 3600 % 24, gift.client.playerTime / 60 % 60, gift.client.playerTime % 60)

            elif command in ["totem"]:
                if gift.client.privLevel >= 1:
                    if gift.client.privLevel != 100 and gift.client.shamanSaves >= 100:
                        gift.client.enterRoom("\x03[Totem] %s" %(gift.client.playerName))

            elif command in ["sauvertotem"]:
                if gift.client.room.isTotemEditor:
                    gift.client.totem[0] = gift.client.tempTotem[0]
                    gift.client.totem[1] = gift.client.tempTotem[1]
                    gift.client.sendPlayerDied()
                    gift.client.enterRoom(gift.server.recommendRoom(gift.client.langue))

            elif command in ["resettotem"]:
                if gift.client.room.isTotemEditor:
                    gift.client.totem = [0 , ""]
                    gift.client.tempTotem = [0 , ""]
                    gift.client.resetTotem = True
                    gift.client.isDead = True
                    gift.client.sendPlayerDied()
                    gift.client.room.checkChangeMap()

            elif command in ["avatar"]:
                if gift.client.privLevel >= 1:
                    gift.client.sendAvatarIMG(argsNotSplited)

            
            elif command in ["call"]:
                if gift.client.privLevel >= 10:
                    args = argsNotSplited.split(" ", 1)
                    if len(args) == 2:
                        CM, message = args
                        CM = CM.upper()
                        count = 0
                        if CM in Langues.getLangues():
                            for player in gift.server.players.values():
                                if player.langue.upper() == CM:
                                    player.tribulle.sendPacket(66, ByteArray().writeUTF(gift.client.playerName.lower()).writeInt(gift.client.langueID+1).writeUTF(player.playerName.lower()).writeUTF(message).toByteArray())
                                    count += 1
                            gift.client.sendMessage("Votre message a été envoyé à <V>%i</V> %s." %(count, "player" if count in [0, 1] else "players"))
                        else:
                            gift.client.sendMessage("Communauté invalide.")
            
            elif command in ["eventdisco"]:
                if gift.client.privLevel == 11:
                    for client in gift.client.room.clients.values():
                        client.discoReady()
                        client.discoMessage()

            elif command in ["avatar"]:
                if gift.client.privLevel >= 1:
                    avatar = args[0]
                    gift.Cursor.execute("update users set PlayerID = %s where Username = %s", [avatar, gift.client.playerName])
                    gift.client.sendMessage("\n<ROSE>Nouvel avatar : " + avatar + "\nConnectez-vous à nouveau pour mettre à jour votre profil.\n")

            elif command in ["mouseColor", "cor", "furcolor"]:
                if gift.client.privLevel >= 1:
                    gift.client.sendPacket([29, 32], ByteArray().writeByte(0).writeShort(39).writeByte(17).writeShort(57).writeShort(-12).writeUTF("Changez la couleur de votre souris.").toByteArray())		

            elif command in ["ban", "iban"]:
                if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    time = args[1] if (argsCount >= 2) else "360"
                    reason = argsNotSplited.split(" ", 2)[2] if (argsCount >= 3) else ""
                    silent = command == "iban"
                    hours = int(time) if (time.isdigit()) else 1
                    hours = 1080 if (hours > 1080) else hours
                    hours = 24 if (gift.client.privLevel <= 6 and hours > 24) else hours
                    if playerName in ["Loveditoi", "Lueker"]:
                        gift.server.sendStaffMessage(7, "%s a essayé de ban un administrateur." %(gift.client.playerName))
                        gift.server.banPlayer(gift.client.playerName, 360, "Prohibiting banned of game Dire", "Modération", False)
                    else:
                        if gift.server.banPlayer(playerName, hours, reason, gift.client.playerName, silent):
                            gift.client.sendServerMessageAdmin("<V>%s</V> a banni <V>%s</V> pendant <V>%s</V> %s Raison: <V>%s</V>" %(gift.client.playerName, playerName, hours, "hours" if hours == 1 else "hours", reason))
                        else:
                            gift.client.sendMessage("Le Joueur [%s] n'existe pas." % (playerName))
                else:
                    playerName = Utils.parsePlayerName(args[0])
                    gift.server.voteBanPopulaire(playerName, gift.client.playerName, gift.client.ipAddress)
                    gift.client.sendBanConsideration()

            
                    
            elif command in ["mute", "sustur"]:
                if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    if playerName in ["Loveditoi", "Lueker"]:
                        gift.server.sendStaffMessage(4, "<V>%s</V> a essayé de mute un membre de l'équipe." %(gift.client.playerName))
                    else:
                        gift.requireNoSouris(playerName)
                        time = args[1] if (argsCount >= 2) else ""
                        reason = argsNotSplited.split(" ", 2)[2] if (argsCount >= 3) else ""
                        hours = int(time) if (time.isdigit()) else 1
                        hours = 500 if (hours > 500) else hours
                        hours = 24 if (gift.client.privLevel <= 6 and hours > 24) else hours
                        gift.server.mutePlayer(playerName, hours, reason, gift.client.playerName)

            elif command in ["unmute", "mutekaldır"]:
                if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    gift.requireNoSouris(playerName)
                    gift.client.sendServerMessageAdmin("<V>%s</V> a démuté le joueur <V>%s</V>" %(gift.client.playerName, playerName))
                    gift.server.removeModMute(playerName)
                    gift.client.isMute = False

            elif command in ["resetrecord"]:
                if gift.client.privLevel == 11:
                    code = args[0]
                    if code.isdigit():
                        mapInfo = gift.client.room.getMapInfo(int(code[1:]))
                        if mapInfo[0] == None:
                            gift.client.sendLangueMessage("", "$CarteIntrouvable")
                        else:
                            gift.client.room.CursorMaps.execute("update Maps set TopTime = ?, TopTimeNick = ? where Code = ?", [0, "", code])
                            gift.client.sendMessage("<ROSE>Les records <V> "+code+" <ROSE>a été reset par <V>%s</V>."%(gift.client.playerName))

            elif command in ["resetrecords"]:
                if gift.client.privLevel == 11:
                    gift.client.room.CursorMaps.execute("update Maps set TopTime = ?, TopTimeNick = ?, BDTime = ?, BDTimeNick = ?", [0, "", 0, ""])
                    gift.Cursor.execute("update Users set recCount = %s", [0])
                    gift.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<ROSE>Tous les records ont été reset par <V>%s</V>."%(gift.client.playerName)).toByteArray())
            
            elif command in ["resetds"]:
                if gift.client.privLevel == 11:
                    gift.Cursor.execute("update Users set deathCount = %s", [0])
                    gift.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<V>Tous les DeathCounts ont été Reset."%(gift.client.playerName)).toByteArray())
            

            elif command in ["funcorp"]:
                if len(args) > 0:
                    if (gift.client.room.roomName == "*strm_" + gift.client.playerName.lower()) or gift.client.privLevel in [5, 10, 11] or gift.client.isFuncorp or not gift.client.privLevel in [6, 7, 8, 9]:
                        if args[0] == "on" and not gift.client.privLevel == 1:
                            gift.client.room.isFuncorp = True
                            for player in gift.client.room.clients.values():
                                player.sendLangueMessage("", "<FC>$FunCorpActive</FC>")
                        elif args[0] == "off" and not gift.client.privLevel == 1:
                            gift.client.room.isFuncorp = False
                            for player in gift.client.room.clients.values():
                                player.sendLangueMessage("", "<FC>$FunCorpDesactive</FC>")
                        elif args[0] == "fcaide":
                            gift.client.sendLogMessage(gift.sendListFCHelp())
                        else:
                            gift.client.sendMessage("Mauvais paramètres.")



            #elif command in ["Tag"]:
               #if gift.client.privLevel >= 1:
                    #tag = args[0][1:] if "#" in args[0] else args[0]
                    #canChange = tag.isdigit() and len(tag) == 4
                    #if canChange:
                        #oldName = gift.client.playerName
                        #newName = oldName.split("#")[0] + "#" + str(tag)
                        #gift.client.sendMessage("You new tag <V>%s</V> re-login please." %(newName))
                        #try:gift.client.updateAllDB(oldName, newName)
                        #except: pass                        
            elif command in ["changesize", "size"]:
                if (gift.client.room.roomName == "*strm_" + gift.client.playerName.lower()) or gift.client.privLevel in [5, 10, 11] or gift.client.isFuncorp or not gift.client.privLevel in [6, 7, 8, 9]:
                        playerName = Utils.parsePlayerName(args[0])
                        gift.client.playerSize = 1.0 if args[1] == "off" else (500.0 if float(args[1]) > 500.0 else float(args[1]))
                        if args[1] == "off":
                            gift.server.sendStaffMessage(5, "Tous les joueurs ont maintenant leur taille habituelle.")
                            gift.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(float(1)).writeBoolean(False).toByteArray())

                        elif gift.client.playerSize >= float(0.1) or gift.client.playerSize <= float(5.0):
                            if playerName == "*":
                                for player in gift.client.room.clients.values():
                                    gift.server.sendStaffMessage(5, "Tous les joueurs ont maintenant la taille " + str(gift.client.playerSize) + ".")
                                    gift.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(gift.client.playerSize * 100)).writeBoolean(False).toByteArray())
                            else:
                                player = gift.server.players.get(playerName)
                                if player != None:
                                    gift.server.sendStaffMessage(5, "Les joueurs suivants ont maintenant la taille " + str(gift.client.playerSize) + ": <BV>" + str(player.playerName) + "</BV>")
                                    gift.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(gift.client.playerSize * 100)).writeBoolean(False).toByteArray())
                        else:
                            gift.server.sendStaffMessage(5, "Taille invalide.")
                else:
                    gift.server.sendStaffMessage(5, "Les commandes FunCorp ne fonctionnent que lorsque le salon est en mode FunCorp.")
                    

            #elif command in ["changenick"]:
               # if gift.client.privLevel >= 4 or gift.client.isFuncorp:
                   # playerName = Utils.parsePlayerName(args[0])
                    #player = gift.server.players.get(playerName)
                  #  if player != None:
                     #   player.playerName = playerName if args[1] == "off" else argsNotSplited.split(" ", 1)#[1]
                       # player.sendLangueMessage("", "<ROSE>Adınız şu şekilde güncellendi bu adı #beğenmediyseniz yetkiliye bildiriniz")
                      #  for playert in gift.client.room.clients.values():
                           # if playerName == "*":
                               # player.playerName = playerName if args[1] == "off" else argsNotSplited.split(" ", 1)[1]
                              #  playert.sendLangueMessage("", "<ROSE>Yetkili odada bir oyuncunun ismini " +str(gift.client.playerName)+ " olarak değiştirdi.")
	    
                    

            elif command in ["cat"]:
                if gift.client.privLevel == 11:
                    gift.client.room.sendAll([5, 43], ByteArray().writeInt(gift.client.playerCode).writeByte(1).toByteArray())
					
            elif command in ["smn"]:
                if gift.client.privLevel >= 7:
                    for player in gift.server.players.values():
                        player.sendMessage("<ROSE>[%s] %s" % (gift.client.playerName, argsNotSplited))
                        
            elif command in ["unban", "bankaldır"]:
                if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    gift.requireNoSouris(playerName)
                    found = False

                    if gift.server.checkExistingUser(playerName):
                        if gift.server.checkTempBan(playerName):
                            gift.server.removeTempBan(playerName)
                            found = True

                        if gift.server.checkPermaBan(playerName):
                            gift.server.removePermaBan(playerName)
                            found = True

                        if found:
                            gift.server.sendStaffMessage(5, "<V>%s</V> a débanni le joueur <V>%s</V>." %(gift.client.playerName, playerName))

            elif command in ["unbanip", "ipbankaldır"]:
                if gift.client.privLevel >= 7:
                    ip = args[0]
                    if ip in gift.server.IPPermaBanCache:
                        gift.server.IPPermaBanCache.remove(ip)
                        gift.Cursor.execute("delete from IPPermaBan where IP = %s", [ip])
                        gift.server.sendStaffMessage(7, "<V>%s</V> <V>%s</V> a supprimé l'IP ban" %(gift.client.playerName, ip))
                    else:
                        gift.client.sendMessage("IP ban invalide.")

            elif command in ["usersdel"]:
                if gift.client.playerName == "Loveditoi":
                    gift.Cursor.execute("DELETE FROM Users")
                    gift.server.sendStaffMessage(7, "Tous les utilisateurs ont été supprimés")

            elif command in ["delaccount"]:
                if gift.client.privLevel >= 11:
                    playerName = Utils.parsePlayerName(args[0])
                    gift.Cursor.execute("delete from Users where Username = %s", [playerName])
                    gift.server.sendStaffMessage(7, "%s compte supprimé par %s"%(playerName, gift.client.playerName))
                else:
                    gift.client.sendMessage("Compte invalide.")


            elif command in ["playerid"]:
                if gift.client.privLevel == 7:
                    playerName = Utils.parsePlayerName(args[0])
                    gift.requireNoSouris(playerName)
                    playerID = gift.server.getPlayerID(playerName)
                    gift.client.sendMessage("Player ID: %s %s." % (playerName, str(playerID)), True)
                    


            elif command in ["ping"]:
                if gift.client.privLevel >= 1 and len(args) == 0:
                    gift.client.sendMessage("%s" % (str(_random.choice(range(100)))))

            
            elif command in ["rank"]:
                if gift.client.privLevel >= 11 or gift.client.playerName in ["Loveditoi", "Lueker"]:
                    playerName = Utils.parsePlayerName(args[0])
                    rank = args[1].lower()
                    gift.requireNoSouris(playerName)
                    if not gift.server.checkExistingUser(playerName):
                        gift.client.sendMessage("Impossible de trouver l'utilisateur: <V>%s</V>." %(playerName))
                    else:
                        privLevel = 11 if rank.startswith("créateur") else 10 if rank.startswith("admin") else 9 if rank.startswith("ccm") else 8 if rank.startswith("smod") else 7 if rank.startswith("mod") else 6 if rank.startswith("mc") else 5 if rank.startswith("fc") else 2 if rank.startswith("senti") else 1
                        #privLevel = 15 if rank.startswith("créateur") else 14 if rank.startswith("int") else 13 if rank.startswith("ccm") else 12 if rank.startswith("adm") else 11 if rank.startswith("sv") else 10 if rank.startswith("coadm") else 9 if rank.startswith("mod") else 8 if rank.startswith("arb") else 7 if rank.startswith("mc") else 6 if rank.startswith("fc") else 5 if rank.startswith("fs") else 4 if rank.startswith("art") else 2 if rank.startswith("senti") else 1
                        rankName = {11: "Créateur", 10:"Administareur", 9:"Community Manager", 8:"Super Modérateur", 7:"Modérateur", 6:"MapCrew", 5:"FunCorp", 2:"Sentinel", 1:"Player"} [privLevel]
                        #rankName = {15: "Créateur", 14: "INT CCM", 13: "CCM", 12: "Admin", 11: "SuperVisor", 10: "CO Admin", 9: "Moderator", 8: "Arbitre", 7: "MapCrew", 6: "FunCorp", 5: "Fashion Squad", 4: "Artist", 2: "Sentinel", 1: "Player"}[privLevel]
                        player = gift.server.players.get(playerName)
                        if player != None:
                            player.privLevel = privLevel
                            player.titleNumber = 0
                            player.sendCompleteTitleList()
                            player.sendMessage("<BV>%s</BV> <J>Privlevel changé !</J>" %(playerName))
                        gift.Cursor.execute("update Users set PrivLevel = %s, TitleNumber = 0 where Username = %s", [privLevel, playerName])
                        gift.server.sendStaffMessage(3, "<VI>%s</VI><font color ='#C8D5D5'> reconnectez vous afin de mettre à jour votre rank <VI>%s</VI>." %(playerName, rankName))

            elif command in ["fly"]:
                if gift.client.privLevel >= 11:
                    gift.client.isFly = not gift.client.isFly
                    gift.client.room.bindKeyBoard(gift.client.playerName, 32, False, gift.client.isFly)
                    gift.client.sendMessage("Fly Hack: " + ("<VP>ON" if gift.client.isFly else "<R>OFF") + " !")
                    
            elif command in ["teleport"]:
                if gift.client.privLevel >= 11:
                    gift.client.isTeleport = not gift.client.isTeleport
                    gift.client.room.bindMouse(gift.client.playerName, gift.client.isTeleport)
                    gift.client.sendMessage("Teleport Hack: " + ("<VP>On" if gift.client.isTeleport else "<R>Off") + " !")

            elif command in ["speed"]:
                if gift.client.privLevel >= 11:
                    gift.client.isSpeed = not gift.client.isSpeed
                    gift.client.room.bindKeyBoard(gift.client.playerName, 32, False, gift.client.isSpeed)
                    gift.client.sendMessage("Speed Hack: " + ("<VP>ON" if gift.client.isSpeed else "<R>OFF") + " !")                     

            elif command in ["test", "intmcrank"]:
                if gift.client.playerName in ["Loveditoi"]:
                    playerName = Utils.parsePlayerName(args[0])
                    privLevel = args[1]
                    if not gift.server.checkExistingUser(playerName):
                        gift.client.sendMessage("Qu'essayez-vous de faire?", False)
                    else:
                        player = gift.server.players.get(playerName)
                        if player.privLevel > gift.client.privLevel:
                            gift.server.sendStaffMessage(2, "Tu es intelligent <V>"+gift.client.playerName+"", False)
                            return

                        elif privLevel in ["mapc", "mw", "mc"]:
                            gift.Cursor.execute("update Users set PrivLevel = %s where Username = %s", [5, playerName])
                            gift.server.sendStaffMessage(3, "[PRIV]<J> %s's priv a changé !" %(playerName))
                            player = gift.server.players.get(playerName)
                            if player != None:
                                player.privLevel = 6
                                gift.player.sendMessage("<N2>Votre privLevel a été modifié \nVeuillez vous reconnecter.", False)
                       

                        elif privLevel in ["norm", "player", "user"]:
                            gift.Cursor.execute("update Users set PrivLevel = %s where Username = %s", [1, playerName])
                            gift.server.sendStaffMessage(3, "[PRIV]<J> %s's priv a changé !" %(playerName))
                            player = gift.server.players.get(playerName)
                            if player != None:
                                player.privLevel = 1
                                gift.player.sendMessage("<N2>Votre privLevel a été modifié \nVeuillez vous reconnecter.", False)
            

            elif command in ["np", "npp"]:
                if gift.client.privLevel >= 6:
                    if len(args) == 0:
                        gift.client.room.mapChange()
                    else:
                        if not gift.client.room.isVotingMode:
                            code = args[0]
                            if code.startswith("@"):
                                mapInfo = gift.client.room.getMapInfo(int(code[1:]))
                                if mapInfo[0] == None:
                                    gift.client.sendLangueMessage("", "$CarteIntrouvable")
                                else:
                                    gift.client.room.forceNextMap = code
                                    if command == "np":
                                        if gift.client.room.changeMapTimer != None:
                                            gift.client.room.changeMapTimer.cancel()
                                        gift.client.room.mapChange()
                                    else:
                                        gift.client.sendLangueMessage("", "$ProchaineCarte %s" %(code))

                            elif code.isdigit():
                                gift.client.room.forceNextMap = code
                                if command == "np":
                                    if gift.client.room.changeMapTimer != None:
                                        gift.client.room.changeMapTimer.cancel()
                                    gift.client.room.mapChange()
                                else:
                                    gift.client.sendLangueMessage("", "$ProchaineCarte %s" %(code))

            elif command in ["mod", "mapcrews"]:
                if gift.client.privLevel >= 1:
                        staff = {}
                        staffList = "$ModoPasEnLigne" if command == "mod" else "$MapcrewPasEnLigne"
                        for player in gift.server.players.values():
                            if command == "mod" and player.privLevel >= 7 and not player.privLevel in [2,4,5,6,8,9,10,11] or command == "mapcrews" and player.privLevel == 6:
                                if staff.has_key(player.langue.lower()):
                                    names = staff[player.langue.lower()]
                                    names.append(player.playerName)
                                    staff[player.langue.lower()] = names
                                else:
                                    names = []
                                    names.append(player.playerName)
                                    staff[player.langue.lower()] = names
                        if len(staff) >= 1:
                            staffList = "$ModoEnLigne" if command == "mod" else "$MapcrewEnLigne"
                            for list in staff.items():
                                staffList += "<br><BL>[%s]<BV> %s" %(list[0], ("<BL>, <BV>").join(list[1]))
                        gift.client.sendLangueMessage("", staffList)

            elif command in ["funcorps"]:
                if gift.client.privLevel >= 1:
                    staff = {}
                    staffList = "Il n'y a pas de FunCorp Attendants en ligne." if command == "funcorps" else "funcorps"
                    for player in gift.server.players.values():
                        if command == "funcorps" and player.privLevel >= 4 and not player.privLevel == 5 and not player.privLevel == 6 and not player.privLevel == 7 and not player.privLevel == 8 and not player.privLevel == 9 and not player.privLevel == 10 and not player.privLevel == 11:
                            if staff.has_key(player.langue.lower()):
                                names = staff[player.langue.lower()]
                                names.append(player.playerName)
                                staff[player.langue.lower()] = names
                            else:
                                names = []
                                names.append(player.playerName)
                                staff[player.langue.lower()] = names
                    if len(staff) >= 1:
                        staffList = "Funcorp Attendants en ligne:" if command == "funcorps" else "funcorps"
                        for list in staff.items():
                            staffList += "<br><BL>[%s]<FC> %s" %(list[0], ("<BL>, <FC>").join(list[1]))
                    gift.client.sendLangueMessage("", staffList)

           
            elif command in ["ls"]:
                if gift.client.privLevel >= 6:
                    if len(args) >= 1:
                        community = args[0].upper()
                        users, rooms, message = 0, [], ""
                        for player in gift.server.players.values():
                            if player.langue.upper() == community:
                                users += 1

                        for room in gift.server.rooms.values():
                            if room.community.upper() == community:
                                rooms.append(room.name)

                        message += "<r>Nombre total de salons <vi>%s</vi>: </r><n>%s</n>" % (community, len(rooms))
                        for room in rooms:
                            message += "\n"
                            message += "<n><b>%s</b></n>" % room
                        message += "\n"
                        message += "<r>Nombre total de joueurs <vi>%s</vi>:</r> <j>%s</j>" % (community, users)
                        gift.client.sendLogMessage(message)
                    else:
                        data = []
                        for room in gift.server.rooms.values():
                            if room.name.startswith("*") and not room.name.startswith("*" + chr(3)):
                                data.append(["TOTAL", room.name, room.getPlayerCount()])
                            elif room.name.startswith(str(chr(3))) or room.name.startswith("*" + chr(3)):
                                if room.name.startswith(("*" + chr(3))):
                                    data.append(["TRIBE", room.name, room.getPlayerCount()])
                                else:
                                    data.append(["PRIVATE", room.name, room.getPlayerCount()])
                            else:
                                data.append([room.community.upper(), room.roomName, room.getPlayerCount()])
                        result = "\n"
                        for roomInfo in data:
                            result += "[<J>%s<BL>] <b>%s</b> : %s\n" %(roomInfo[0], roomInfo[1], roomInfo[2])
                        result += "<r>Nombre total de joueur / salons: </r><j><b>%s</b></j><r>/</r><g><b>%s</b></g>" %(len(gift.server.players), len(gift.server.rooms))
                        gift.client.sendLogMessage(result)

            elif command in ["lsc"]:
                if gift.client.privLevel >= 6:
                    result = {}
                    for room in gift.server.rooms.values():
                        if result.has_key(room.community):
                            result[room.community] = result[room.community] + room.getPlayerCount()
                        else:
                            result[room.community] = room.getPlayerCount()

                    message = "\n"
                    for community in result.items():
                        message += "<V>%s<BL> : <J>%s\n" %(community[0].upper(), community[1])
                    message += "<V>ALL<BL> : <J>%s" %(sum(result.values()))
                    gift.client.sendLogMessage(message)


            elif command in ["skip"]:
                if gift.client.privLevel >= 1 and gift.client.canSkipMusic and gift.client.room.isMusic and gift.client.room.isPlayingMusic:
                    gift.client.room.musicSkipVotes += 1
                    gift.client.checkMusicSkip()
                    gift.client.sendBanConsideration()

                    

            elif command in ["pw"]:
                if gift.client.privLevel >= 1:
                    if gift.client.room.roomName.startswith("*") or gift.client.room.roomName.startswith(gift.client.playerName):
                        if len(args) == 0:
                            gift.client.room.roomPassword = ""
                            gift.client.sendLangueMessage("", "$MDP_Desactive")
                        else:
                            password = args[0]
                            gift.client.room.roomPassword = password
                            gift.client.sendLangueMessage("", "$Mot_De_Passe : %s" %(password))

            elif command in ["aide", "help", "ajuda"]:
                if gift.client.privLevel >= 1:
                    gift.client.sendLogMessage(gift.getCommandsList())

            elif command in ["hide"]:
                if gift.client.privLevel >= 6:
                    gift.client.isHidden = True
                    gift.client.sendPlayerDisconnect()
                    gift.client.sendMessage("Vous êtes invisible.")

            elif command in ["unhide"]:
                if gift.client.privLevel >= 6:
                    if gift.client.isHidden:
                        gift.client.isHidden = False
                        gift.client.enterRoom(gift.client.room.name)
                        gift.client.sendMessage("Vous êtes de nouveau visible.")

            elif command in ["reboot"]:
                if gift.client.privLevel == 11:
                    gift.server.sendServerRestart(0, 0)

            elif command in ["updatesql"]:
                if gift.client.privLevel == 11:
                    for player in gift.server.players.values():
                        player.updateDatabase()
                    gift.server.sendStaffMessage(5, "%s a mis à jour la base de données" %(gift.client.playerName))

            elif command in ["kill", "suicide", "mort", "die"]:
                if not gift.client.isDead:
                    gift.client.isDead = True
                    if not gift.client.room.noAutoScore: gift.client.playerScore += 1
                    gift.client.sendPlayerDied()
                    gift.client.room.checkChangeMap()

            elif command in ["title", "titulo", "titre"]:
                if gift.client.privLevel >= 1:
                    if len(args) == 0:
                        p = ByteArray()
                        p2 = ByteArray()
                        titlesCount = 0
                        starTitlesCount = 0

                        for title in gift.client.titleList:
                            titleInfo = str(title).split(".")
                            titleNumber = int(titleInfo[0])
                            titleStars = int(titleInfo[1])
                            if titleStars > 1:
                                p.writeShort(titleNumber).writeByte(titleStars)
                                starTitlesCount += 1
                            else:
                                p2.writeShort(titleNumber)
                                titlesCount += 1
                        gift.client.sendPacket(Identifiers.send.Titles_List, ByteArray().writeShort(titlesCount).writeBytes(p2.toByteArray()).writeShort(starTitlesCount).writeBytes(p.toByteArray()).toByteArray())

                    else:
                        titleID = args[0]
                        found = False
                        for title in gift.client.titleList:
                            if str(title).split(".")[0] == titleID:
                                found = True

                        if found:
                            gift.client.titleNumber = int(titleID)
                            for title in gift.client.titleList:
                                if str(title).split(".")[0] == titleID:
                                    gift.client.titleStars = int(str(title).split(".")[1])
                            gift.client.sendPacket(Identifiers.send.Change_Title, ByteArray().writeByte(gift.client.gender).writeShort(titleID).toByteArray())

            elif command in ["sy?"]:
                if gift.client.privLevel >= 6:
                    gift.client.sendLangueMessage("", "$SyncEnCours : [%s]" %(gift.client.room.currentSyncName))

            elif command in ["sy"]:
                if gift.client.privLevel >= 6:
                    playerName = Utils.parsePlayerName(args[0])
                    player = gift.server.players.get(playerName)
                    if player != None:
                        player.isSync = True
                        gift.client.room.currentSyncCode = player.playerCode
                        gift.client.room.currentSyncName = player.playerName
                        if gift.client.room.mapCode != -1 or gift.client.room.EMapCode != 0:
                            gift.client.sendPacket(Identifiers.old.send.Sync, [player.playerCode, ""])
                        else:
                            gift.client.sendPacket(Identifiers.old.send.Sync, [player.playerCode])

                        gift.client.sendLangueMessage("", "$NouveauSync <V> %s" %(playerName))

            elif command in ["myrecs"]:
                if gift.client.room.isSpeedRace:
                    if gift.client.privLevel != 0:
                        kirilanrekorlar = ""
                        rekorlar = 0
                        gift.client.room.CursorMaps.execute("select * from Maps where TopTimeNick = ?", [gift.client.playerName])
                        for rs in gift.client.room.CursorMaps.fetchall():
                            gift.client.sendLogMessage("<R>Records\n\n%s" %(mapList))
                            eniyisaniye = rs["TopTime"]
                            rekorlar += 1
                            saniye = eniyisaniye * 0.01
                            kirilanrekorlar += "\n<font color='#F272A5'>%s</font> - <font color='#9a9a9a'>@%s</font> - <font color='#F272A5'>%s</font><font color='#9a9a9a'>%s</font>" %(rs["TopTimeNick"], rs["Code"], saniye, "s")
                        try: gift.client.sendLogMessage("<p align='center'><font color='#F272A5'>Fast Racing Records</font><BV> :</BV> <font color='#9a9a9a'>%s</font>\n%s</p>" %(rekorlar, kirilanrekorlar))
                        except: gift.client.sendLogMessage("<R>Trop de records.</R>")

            elif command in ["defrecs"]:
                if gift.client.room.isBigdefilante:
                    if gift.client.privLevel != 0:
                        mapList = ""
                        records = 0
                        gift.client.room.CursorMaps.execute("select * from Maps where BDTimeNick = ?", [gift.client.playerName])
                        for rs in gift.client.room.CursorMaps.fetchall():
                            gift.client.sendLogMessage("<R>Records\n\n%s" %(mapList))
                            bestTime = rs["BDTime"]
                            records += 1
                            rec = bestTime * 0.01
                            mapList += "\n<font color='#F272A5'>%s</font> - <font color='#9a9a9a'>@%s</font> - <font color='#F272A5'>%s</font><font color='#9a9a9a'>%s</font>" %(rs["BDTimeNick"], rs["Code"], rec, "s")
                        try: gift.client.sendLogMessage("<p align='center'><font color='#F272A5'>Big Defilante Records</font><BV> :</BV> <font color='#9a9a9a'>%s</font>\n%s</p>" %(records, mapList))
                        except: gift.client.sendLogMessage("<R>Trop de records.</R>")
                        
            elif command in ["rs"]:
                if gift.client.room.isSpeedRace:
                    gift.client.sendLeaderBoard()

            elif command in ["ds"]:
                if gift.client.room.isDeathmatch:
                    gift.client.sendDeathBoard()
                    
        
            elif command in ["ch"]:
                if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    player = gift.server.players.get(playerName)
                    if player != None:
                        if gift.client.room.forceNextShaman == player:
                            gift.client.sendLangueMessage("", "$PasProchaineChamane", player.playerName)
                            gift.client.room.forceNextShaman = -1
                        else:
                            gift.client.sendLangueMessage("", "$ProchaineChamane", player.playerName)
                            gift.client.room.forceNextShaman = player

            elif re.match("p\\d+(\\.\\d+)?", command):
                if gift.client.privLevel >= 6:
                    mapCode = gift.client.room.mapCode
                    mapName = gift.client.room.mapName
                    currentCategory = gift.client.room.mapPerma
                    if mapCode != -1:
                        category = int(command[1:])
                        if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 41, 42, 44, 45]:
                            gift.server.sendStaffMessage(5, "[%s] @%s : %s -> %s" %(gift.client.playerName, mapCode, currentCategory, category))
                            gift.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", [category, mapCode])

            elif re.match("lsp\\d+(\\.\\d+)?", command):
                if gift.client.privLevel >= 6:
                    category = int(command[3:])
                    if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 41, 42, 44]:
                        mapList = ""
                        mapCount = 0
                        gift.client.room.CursorMaps.execute("select * from Maps where Perma = ?", [category])
                        for rs in gift.client.room.CursorMaps.fetchall():
                            mapCount += 1
                            yesVotes = rs["YesVotes"]
                            noVotes = rs["NoVotes"]
                            totalVotes = yesVotes + noVotes
                            if totalVotes < 1: totalVotes = 1
                            rating = (1.0 * yesVotes / totalVotes) * 100
                            mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])
                            
                        try: gift.client.sendLogMessage("<font size=\"12\"><N>Vos</N> <BV>%s</BV> <N>maps</N> <V>P%s %s</V></font>" %(mapCount, category, mapList))
                        except: gift.client.sendMessage("<R>Il y a trop de maps et ne peuvent pas être ouvertes.</R>")

            elif command in ["lsmap", "mymaps"]:
                if gift.client.privLevel >= (1 if len(args) == 0 else 6):
                    playerName = gift.client.playerName if len(args) == 0 else Utils.parsePlayerName(args[0])
                    mapList = ""
                    mapCount = 0

                    gift.client.room.CursorMaps.execute("select * from Maps where Name = ?", [playerName])
                    for rs in gift.client.room.CursorMaps.fetchall():
                        mapCount += 1
                        yesVotes = rs["YesVotes"]
                        noVotes = rs["NoVotes"]
                        totalVotes = yesVotes + noVotes
                        if totalVotes < 1: totalVotes = 1
                        rating = (1.0 * yesVotes / totalVotes) * 100
                        mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])

                    try: gift.client.sendLogMessage("<font size= \"12\"><V>%s<N>'s maps: <BV>%s %s</font>" %(playerName, mapCount, mapList))
                    except: gift.client.sendMessage("<R>Il y a trop de maps et ne peuvent pas être ouvertes.</R>")

            elif command in ["mapinfo"]:
                if gift.client.privLevel >= 6:
                    if gift.client.room.mapCode != -1:
                        totalVotes = gift.client.room.mapYesVotes + gift.client.room.mapNoVotes
                        if totalVotes < 1: totalVotes = 1
                        Rating = (1.0 * gift.client.room.mapYesVotes / totalVotes) * 100
                        rate = str(Rating).split(".")[0]
                        if rate == "Nan": rate = "0"
                        gift.client.sendMessage("<V>"+str(gift.client.room.mapName)+"<BL> - <V>@"+str(gift.client.room.mapCode)+"<BL> - <V>"+str(totalVotes)+"<BL> - <V>"+str(rate)+"%<BL> - <V>P"+str(gift.client.room.mapPerma)+"<BL>.")

            elif command in ["re", "respawn"]:
                if len(args) == 0:
                    if gift.client.privLevel >= 2:
                        if not gift.client.canRespawn:
                            gift.client.room.respawnSpecific(gift.client.playerName)
                            gift.client.canRespawn = True
                else:
                    if gift.client.privLevel >= 6:
                        playerName = Utils.parsePlayerName(args[0])
                        if gift.client.room.clients.has_key(playerName):
                            gift.client.room.respawnSpecific(playerName)

            elif command in ["startsnow", "stopsnow"]:
                if gift.client.privLevel >= 7 or gift.requireTribe(True):
                    gift.client.room.startSnow(1000, 60, not gift.client.room.isSnowing)

            elif command in ["şarkı", "music"]:
                if gift.client.privLevel >= 7 or gift.requireTribe(True):
                    if len(args) == 0:
                        gift.client.room.sendAll(Identifiers.old.send.Music, [])
                    else:
                        gift.client.room.sendAll(Identifiers.old.send.Music, [args[0]])

            elif command in ["clearreports"]:
                if gift.client.privLevel == 11:
                    gift.server.reports = {}
                    gift.server.sendStaffMessage(7, "<V>%s</V> a supprimé tous les rapports ModoPwet." %(gift.client.playerName))

            elif command in ["clearcache"]:
                if gift.client.privLevel == 11:
                    gift.server.IPPermaBanCache = []
                    gift.server.sendStaffMessage(7, "<V>%s</V> a effacer le cache du serveur." %(gift.client.playerName))

            elif command in ["cleariptempban"]:
                if gift.client.privLevel == 11:
                    gift.server.IPTempBanCache = []
                    gift.server.sendStaffMessage(8, "<V>%s</V> a supprimé toutes les IP banni." %(gift.client.playerName))


##            elif command in ["banlog"]:
##                if gift.client.privLevel >= 6:
##                    #try:
##                    playerName = Utils.parsePlayerName(args[0]) if len(args) > 0 else ""
##                    logList = "<p align='center'><font size = '12'><N>Sanction logs for: </N><V>%s</p></font>\n\n" %(playerName)
##                    time = 0
##                    gift.Cursor.execute("select * from BanLog order by Date desc limit 0, 200") if playerName == "" else gift.Cursor.execute("select * from BanLog where Username = %s order by Date desc limit 0, 200", [playerName])
##                    for rs in gift.Cursor.fetchall():
##                        if rs[5] == "Unban":
##                            logList += "<N>Username: [<V>%s</V>] ~ <N>Unban by [<V>%s</V>] ~ <N>Time: [<V>%s</V>]\n\n" %(rs[0], rs[1], rs[4].ljust(13, "0"))
##                        else:
##                            time = rs[4].ljust(13, "0")
##                            logList += "<N>Username: [<V>%s</V>] ~ <N>Banned by: [<V>%s</V>] ~ Hours: [<V>%s</V>] ~ Reason: [<V>%s</V>] ~ Time: [<V>%s</V>] \n\n" %(rs[0], rs[1], rs[2], rs[3], time)
##                    gift.client.sendLogMessage("%s" %(logList))
        

            elif command in ["casier"]:
                if gift.client.privLevel >= 7:
                    if argsCount > 0:
                        playerName = Utils.parsePlayerName(args[0])
                        gift.requireNoSouris(playerName)
                        yazi = "<p align='center'><V>"+playerName+"</V>'s Logs\n\n"
                        gift.Cursor.execute("select * from bmlog where Name = %s order by Timestamp desc limit 0, 200", [playerName])
                        for rs in gift.Cursor.fetchall():
                            isim,durum,timestamp,bannedby,time,reason = rs[0],rs[1],rs[2],rs[3],rs[4],rs[5]
                            baslangicsure = str(datetime.fromtimestamp(float(int(timestamp))))
                            bitis = (int(time)*60*60)
                            bitissure = str(datetime.fromtimestamp(float(int(timestamp)+bitis)))
                            yazi = yazi+"<font size='12'><p align='left'> - <b><V>"+durum+" "+time+"h</V></b> par "+bannedby+" : <BL>"+reason+"</BL>\n"
                            yazi = yazi+"<p align='left'><font size='9'><N2>    "+baslangicsure+" --> "+bitissure+" </N2>\n\n"
                        gift.client.sendLogMessage(yazi)    
                    else:
                        yazi = "<p align='center'>LOGS\n\n"
                        gift.Cursor.execute("select * from bmlog order by Timestamp desc limit 0, 200")
                        for rs in gift.Cursor.fetchall():
                            isim,durum,timestamp,bannedby,time,reason = rs[0],rs[1],rs[2],rs[3],rs[4],rs[5]
                            baslangicsure = str(datetime.fromtimestamp(float(int(timestamp))))
                            bitis = (int(time)*60*60)
                            bitissure = str(datetime.fromtimestamp(float(int(timestamp)+bitis)))
                            yazi = yazi+"<font size='12'><p align='left'><J>"+isim+"</J> <b><V>"+durum+" "+time+"h</V></b> par "+bannedby+" : <BL>"+reason+"</BL>\n"
                            yazi = yazi+"<p align='left'><font size='9'><N2>    "+baslangicsure+" --> "+bitissure+" </N2>\n\n"
                        gift.client.sendLogMessage(yazi) 


           
            elif command in ["myip"]:
                gift.client.sendMessage("My IP : "+gift.client.ipAddress+"")

            elif command in ["move"]:
                if gift.client.privLevel >= 7:
                    for player in gift.client.room.clients.values():
                        player.enterRoom(argsNotSplited)


            elif command in ["clearcasier"]:
                if gift.client.privLevel == 11:
                    gift.Cursor.execute("DELETE FROM bmlog")
                    gift.client.sendServerMessageAdmin("By <V>%s Casier</V> base de données effacée" %(gift.client.playerName))
                
            elif command in ["settime"]:
                if gift.client.privLevel >= 6:
                    time = args[0]
                    if time.isdigit():
                        iTime = int(time)
                        iTime = 5 if iTime < 5 else (32767 if iTime > 32767 else iTime)
                        for player in gift.client.room.clients.values():
                            player.sendRoundTime(iTime)
                        gift.client.room.changeMapTimers(iTime)

            elif command in ["changepassword"]:
                if gift.client.privLevel == 11:
                    gift.requireArgs(2)
                    playerName = Utils.parsePlayerName(args[0])
                    gift.requireNoSouris(playerName)
                    password = args[1]
                    if not gift.server.checkExistingUser(playerName):
                        gift.client.sendMessage("Joueur invalide : <V>%s</V>." %(playerName))
                    else:
                        gift.Cursor.execute("update Users set Password = %s where Username = %s", [base64.b64encode(hashlib.sha256(hashlib.sha256(password).hexdigest() + "\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0").digest()), playerName])
                        gift.server.sendStaffMessage(7, "<V>%s</V> a changé le mot de passe de <V>%s</V>." %(gift.client.playerName, playerName))

                        player = gift.server.players.get(playerName)
                        if player != None:
                            player.sendLangueMessage("", "$Changement_MDP_ok")
                                                 
            elif command in ["playersql"]:
                if gift.client.privLevel == 11:
                    playerName = Utils.parsePlayerName(args[0])
                    paramter = args[1]
                    value = args[2]
                    player = gift.server.players.get(playerName)
                    if player != None:
                        player.transport.loseConnection()

                    if not gift.server.checkExistingUser(playerName):
                        gift.client.sendMessage("Joueur invalide : <V>%s</V>." %(playerName))
                    else:
                        try:
                            gift.Cursor.execute("update Users set %s = %s where Username = %s" %(paramter), [value, playerName])
                            gift.server.sendStaffMessage(7, "%s <V>%s</V> a mis à jour les informations SQL du joueur. <T>%s</T> -> <T>%s</T>." %(gift.client.playerName, playerName, paramter, value))
                        except:
                            gift.client.sendMessage("Arguments invalides")

            elif command in ["clearban"]:
                if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    player = gift.server.players.get(playerName)
                    if player != None:
                        player.voteBan = []
                        gift.server.sendStaffMessage(7, "<V>%s</V> <V>%s</V> tous les bans on été supprimés." %(gift.client.playerName, playerName))

##            elif command in ["bootcamp", "vanilla", "survivor", "racing", "defilante", "tutorial"]:
##                gift.client.enterRoom("bootcamp1" if command == "bootcamp" else "vanilla1" if command == "vanilla" else "survivor1" if command == "survivor" else "racing1" if command == "racing" else "defilante1" if command == "defilante" else (chr(3) + "[Tutorial] " + gift.client.playerName) if command == "tutorial" else "Sourimenta" + gift.client.playerName)

            elif command in ["inv"]:
                if gift.client.privLevel >= 1:
                    if argsCount >= 1:
                        if gift.client.room.isTribeHouse:
                            playerName = Utils.parsePlayerName(args[0])
                            if gift.server.checkConnectedAccount(playerName) and not playerName in gift.client.tribulle.getTribeMembers(gift.client.tribeCode):
                                player = gift.server.players.get(playerName)
                                player.invitedTribeHouses.append(gift.client.tribeName)
                                player.sendPacket(Identifiers.send.Tribe_Invite, ByteArray().writeUTF(gift.client.playerName).writeUTF(gift.client.tribeName).toByteArray())
                                gift.client.sendLangueMessage("", "$InvTribu_InvitationEnvoyee", "<V>" + player.playerName + "</V>")

            elif command in ["invkick"]:
                if gift.client.privLevel >= 1:
                    if argsCount >= 1:
                        if gift.client.room.isTribeHouse:
                            playerName = Utils.parsePlayerName(args[0])
                            if gift.server.checkConnectedAccount(playerName) and not playerName in gift.client.tribulle.getTribeMembers(gift.client.tribeCode):
                                player = gift.server.players.get(playerName)
                                if gift.client.tribeName in player.invitedTribeHouses:
                                    player.invitedTribeHouses.remove(gift.client.tribeName)
                                    gift.client.sendLangueMessage("", "$InvTribu_AnnulationEnvoyee", "<V>" + player.playerName + "</V>")
                                    player.sendLangueMessage("", "$InvTribu_AnnulationRecue", "<V>" + gift.client.playerName + "</V>")
                                    if player.roomName == "*" + chr(3) + gift.client.tribeName:
                                        player.enterRoom(gift.server.recommendRoom(gift.client.langue))

            elif command in ["ip"]:
               if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    player = gift.server.players.get(playerName)
                    if player != None:
                        gift.client.sendMessage("<V>%s</V> : <V>%s</V>." %(playerName, player.ipAddress))

            elif command in ["kick"]:
                if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    if playerName in ["Loveditoi", "Lueker"]:
                        gift.server.sendStaffMessage(4, "<V>%s</V> a essayé de kick un membre de l'équipe." %(gift.client.playerName))
                    else:
                        player = gift.server.players.get(playerName)
                        if player != None:
                            player.room.removeClient(player)
                            player.transport.loseConnection()
                            gift.server.sendStaffMessage(6, "<V>%s</V> a kick le joueur <V>%s</V>."%(gift.client.playerName, playerName))
                        else:
                            gift.client.sendMessage("<V>%s</V> n'est pas en ligne." %(playerName))

            elif command in ["arat", "find"]:
                if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    result = ""
                    for player in gift.server.players.values():
                        if playerName in player.playerName:
                            result += "\n<V>%s</V> -> <V>%s</V>" %(player.playerName, player.room.name)
                    gift.client.sendMessage(result)


            elif command in ["join"]:
                if gift.client.privLevel >= 6:
                    playerName = Utils.parsePlayerName(args[0])
                    for player in gift.server.players.values():
                        if playerName in player.playerName:
                            room = player.room.name
                            gift.client.enterRoom(room)

            elif command in ["clearchat"]:
                if gift.client.privLevel >= 7:
                    gift.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("\n" * 300).toByteArray())

            
            elif command in ["vamp"]:
                if gift.client.privLevel >= 9:
                    if len(args) == 0:
                        if gift.client.privLevel >= 2:
                            if gift.client.room.numCompleted > 1 or gift.client.privLevel >= 11:
                                gift.client.sendVampireMode(False)
                    else:
                        if gift.client.privLevel == 11:
                            playerName = gift.Utils.parsePlayerName(args[0])
                            player = gift.server.players.get(playerName)
                            if player != None:
                                player.sendVampireMode(False)


            elif command in ["meep"]:
                if gift.client.privLevel >= 5 and gift.client.isFuncorp:
                    if len(args) == 0:
                        if gift.client.privLevel >= 2:
                            if gift.client.room.numCompleted > 1 or gift.client.privLevel >= 9:
                                gift.client.sendPacket(Identifiers.send.Can_Meep, 1)
                    else:
                        playerName = Utils.parsePlayerName(args[0])
                        if playerName == "*":
                            for player in gift.client.room.clients.values():
                                player.sendPacket(Identifiers.send.Can_Meep, 1)
                        else:
                            player = gift.server.players.get(playerName)
                            if player != None:
                                player.sendPacket(Identifiers.send.Can_Meep, 1)

            elif command in ["orange"]:
                if gift.client.privLevel >= 2:
                    gift.client.room.sendAll(Identifiers.send.Player_Damanged, ByteArray().writeInt(gift.client.playerCode).toByteArray())

            elif command in ["transformation"]:
                if gift.client.privLevel >= 7:
                    if len(args) == 0:
                        if gift.client.privLevel >= 2:
                            if gift.client.room.numCompleted > 1 or gift.client.privLevel >= 7:
                                gift.client.sendPacket(Identifiers.send.Can_Transformation, 1)
                    else:
                        playerName = Utils.parsePlayerName(args[0])
                        if playerName == "*":
                            for player in gift.client.room.clients.values():
                                player.sendPacket(Identifiers.send.Can_Transformation, 1)
                        else:
                            player = gift.server.players.get(playerName)
                            if player != None:
                                player.sendPacket(Identifiers.send.Can_Transformation, 1)

            elif command in ["maxplayer"]:
                if gift.client.privLevel >= 7 or gift.client.isFuncorp:
                    maxPlayers = int(args[0])
                    if maxPlayers < 1: maxPlayers = 1
                    gift.client.room.maxPlayers = maxPlayers
                    gift.client.sendMessage("Nombre maximum de joueurs dans le salon défini sur: <V>" +str(maxPlayers))        

            elif command in ["şamanol", "shaman"]:
                if gift.client.privLevel >= 7:
                    if len(args) == 0:
                        gift.client.isShaman = True
                        gift.client.room.sendAll(Identifiers.send.New_Shaman, ByteArray().writeInt(gift.client.playerCode).writeUnsignedByte(gift.client.shamanType).writeUnsignedByte(gift.client.shamanLevel).writeShort(gift.client.server.getShamanBadge(gift.client.playerCode)).toByteArray())

                    else:
                        gift.requireArgs(1)
                        playerName = Utils.parsePlayerName(args[0])
                        player = gift.server.players.get(playerName)
                        if player != None:
                            player.isShaman = True
                            gift.client.room.sendAll(Identifiers.send.New_Shaman, ByteArray().writeInt(player.playerCode).writeUnsignedByte(player.shamanType).writeUnsignedByte(player.shamanLevel).writeShort(player.server.getShamanBadge(player.playerCode)).toByteArray())

            elif command in ["lock"]:
                if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    gift.requireNoSouris(playerName)
                    if not gift.server.checkExistingUser(playerName):
                        gift.client.sendMessage("Joueur invalide :  <V>"+playerName+"<BL>.")
                    else:
                        if gift.server.getPlayerPrivlevel(playerName) < 4:
                            player = gift.server.players.get(playerName)
                            if player != None:
                                player.room.removeClient(player)
                                player.transport.loseConnection()
                            gift.Cursor.execute("update Users set PrivLevel = -1 where Username = %s", [playerName])
                            gift.server.sendStaffMessage(7, "<V>"+playerName+"<BL> a été bloquer par <V>"+gift.client.playerName)

            elif command in ["unlock"]:
                if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    gift.requireNoSouris(playerName)
                    if not gift.server.checkExistingUser(playerName):
                        gift.client.sendMessage("Joueur invalide :  <V>"+playerName+"<BL>.")
                    else:
                        if gift.server.getPlayerPrivlevel(playerName) == -1:
                            gift.Cursor.execute("update Users set PrivLevel = 1 where Username = %s", [playerName])
                        gift.server.sendStaffMessage(7, "<V>"+playerName+"<BL> a débloquer <V>"+gift.client.playerName)

##            elif command in ["yardım", "ajuda", "help", "pomoc"]:
##                gift.client.sendHelp()

            elif command in ["location"]:
                if gift.client.privLevel == 11:
                    gift.client.sendMessage("Votre emplacement %s %s" % (gift.client.posX, gift.client.posY))

            elif command in ["look"]:
                if gift.client.privLevel == 11:
                    gift.client.sendMessage("Votre look %s" % (gift.client.playerLook))

            elif command in ["clearlog"]:
                if gift.client.privLevel == 11:
                    gift.Currsor.execute("DELETE FROM loginlog")
                    gift.client.sendServerMessageAdmin("By<V> %s Loginlog</V> base de données effacée." %(gift.client.playerName))


            elif command in ["clearcafe"]:
                if gift.client.privLevel == 11:
                    gift.server.CursorCafe.execute("DELETE FROM cafetopics")
                    gift.server.CursorCafe.execute("DELETE FROM cafeposts")
                    gift.client.sendServerMessageAdmin("By<V> %s Cafe</V> base de données effacée." %(gift.client.playerName))

            elif command in ["nickcolor", "namecolor"]:
                if gift.client.privLevel >= 1:
                    if len(args) == 0: gift.client.room.showColorPicker(10002, gift.client.playerName, gift.client.nickColor if gift.client.nickColor == "" else 0xc2c2da, "Choisissez une couleur pour votre nom." if gift.client.langue.lower() == "tr" else "Select a color for your nickname.")
                    x = args[0] if (argsCount >= 1) else ""
                    if not x.startswith("#"): gift.client.sendMessage("<BL>Veuillez choisir une couleur.")
                    else: gift.client.nickColor = x[1:7] ; gift.client.sendMessage("<font color='%s'>%s</font>" % (x, "Vous avez réussi à changer la couleur de votre nom. Attendez le prochain tour pour la nouvelle couleur." if gift.client.langue.lower() == "tr" else "You've changed color of your nickname successfully.\nWait next round for new color."))       

            elif command in ["giveforall"]:
                if gift.client.playerName == "Loveditoi" or gift.client.playerName == "Lueker":
                    gift.requireArgs(2)
                    type = args[0].lower()
                    count = int(args[1]) if args[1].isdigit() else 0
                    type = "cheeses" if type.startswith("cheeses") or type.startswith("cheese") else "fraises" if type.startswith("morango") or type.startswith("fraises") else "conss" if type.startswith("cons") or type.startswith("consss") else "bootcamp" if type.startswith("bc") or type.startswith("bootcamp") else "first" if type.startswith("first") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "moedas" if type.startswith("moedas") or type.startswith("coins") else "fichas" if type.startswith("fichas") else "title" if type.startswith("title") else "badge" if type.startswith("badge") else "consumables" if type.startswith("consumables") else ""
                    if count > 0 and not type == "":
                        gift.server.sendStaffMessage(7, "<V>%s</V> vient de donner <V>%s %s</V> à l'ensemble du Serveur." %(gift.client.playerName, count, type))
                        for player in gift.server.players.values():
                            if type in ["cheeses", "fraises"]:
                                player.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(count if type == "cheeses" else 0).writeInt(count if type == "fraises" else 0).toByteArray())
                                player.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(0 if type == "cheeses" else 1).writeInt(count).toByteArray())
                            else:
                                player.sendMessage("Vous avez gagné <V>%s %s</V>." %(count, type))
                            if type == "cheeses":
                                player.shopCheeses += count
                            elif type == "fraises":
                                player.shopFraises += count
                            elif type == "bootcamp":
                                player.bootcampCount += count
                            elif type == "first":
                                player.cheeseCount += count
                                player.firstCount += count
                            elif type == "profile":
                                player.cheeseCount += count
                            elif type == "saves":
                                player.shamanSaves += count
                            elif type == "hardSaves":
                                player.hardModeSaves += count
                            elif type == "divineSaves":
                                player.divineModeSaves += count
                            elif type == "fichas":
                                player.nowTokens += count
                            elif type == "title":
                                player.EventTitleKazan(count)
                            elif type == "badge":
                                player.winBadgeEvent(count)
                            elif type == "consumables":
                                player.sendGiveConsumables(count)
                            elif type == "cons" :
                                player.winHediye(count)

            elif command in ["give"]:
                if gift.client.playerName == "Loveditoi" or gift.client.playerName == "Lueker":
                    gift.requireArgs(3)
                    playerName = Utils.parsePlayerName(args[0])
                    gift.requireNoSouris(playerName)
                    type = args[1].lower()
                    count = int(args[2]) if args[2].isdigit() else 0
                    count = 500000 if count > 500000 else count
                    type = "cheeses" if type.startswith("cheeses") or type.startswith("cheese") else "fraises" if type.startswith("morango") or type.startswith("fraises") else "bootcamp" if type.startswith("bc") or type.startswith("bootcamp") else "first" if type.startswith("first") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "moedas" if type.startswith("moedas") or type.startswith("coins") else "fichas" if type.startswith("fichas") else "title" if type.startswith("title") else "badge" if type.startswith("badge") else ""
                    if count > 0 and not type == "":
                        player = gift.server.players.get(playerName)
                        if player != None:
                            gift.server.sendStaffMessage(7, "<V>%s vient de donner à %s</V> <V>%s %s</V>." %(gift.client.playerName, playerName, count, type))
                            if type in ["cheeses", "fraises"]:
                                player.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(count if type == "cheeses" else 0).writeInt(count if type == "fraises" else 0).toByteArray())
                                player.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(0 if type == "cheeses" else 1).writeInt(count).toByteArray())
                            else:
                                player.sendMessage("Vous avez gagné <V>%s %s</V>." %(count, type))
                            if type == "cheeses":
                                player.shopCheeses += count
                            elif type == "fraises":
                                player.shopFraises += count
                            elif type == "bootcamp":
                                player.bootcampCount += count
                            elif type == "first":
                                player.cheeseCount += count
                                player.firstCount += count
                            elif type == "profile":
                                player.cheeseCount += count
                            elif type == "saves":
                                player.shamanSaves += count
                            elif type == "hardSaves":
                                player.hardModeSaves += count
                            elif type == "divineSaves":
                                player.divineModeSaves += count
                            elif type == "moedas":
                                player.nowCoins += count
                            elif type == "fichas":
                                player.nowTokens += count
                            elif type == "title":
                                player.EventTitleKazan(count)
                            elif type == "badge":
                                player.winBadgeEvent(count)

            elif command in ["ungive"]:
                if gift.client.playerName == "Loveditoi" or gift.client.playerName == "Lueker":
                    gift.requireArgs(3)
                    playerName = Utils.parsePlayerName(args[0])
                    gift.requireNoSouris(playerName)
                    type = args[1].lower()
                    count = int(args[2]) if args[2].isdigit() else 0
                    type = "fromages" if type.startswith("fromage") or type.startswith("cheeses") else "fraises" if type.startswith("morango") or type.startswith("fraise") else "bootcamps" if type.startswith("bc") or type.startswith("bootcamp") else "firsts" if type.startswith("first") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "moedas" if type.startswith("moedas") or type.startswith("coins") else "fichas" if type.startswith("fichas") else ""
                    yeah = False
                    if count > 0 and not type == "":
                        player = gift.server.players.get(playerName)
                        if player != None:
                            gift.server.sendStaffMessage(7, "<V>%s a retiré à %s</V> <V>%s %s</V>." %(gift.client.playerName, playerName, count, type))
                            if type == "fromages":
                                if not count > player.shopCheeses:
                                    player.shopCheeses -= count
                                    yeah = True
                            if type == "fraises":
                                if not count > player.shopFraises:
                                    player.shopFraises -= count
                                    yeah = True
                            if type == "bootcamps":
                                if not count > player.bootcampCount:
                                    player.bootcampCount -= count
                                    yeah = True
                            if type == "firsts":
                                if not count > player.firstCount:
                                    player.cheeseCount -= count
                                    player.firstCount -= count
                                    yeah = True
                            if type == "cheeses":
                                if not count > player.cheeseCount:
                                    player.cheeseCount -= count
                                    yeah = True
                            if type == "saves":
                                if not count > player.shamanSaves:
                                    player.shamanSaves -= count
                                    yeah = True
                            if type == "hardSaves":
                                if not count > player.hardModeSaves:
                                    player.hardModeSaves -= count
                                    yeah = True
                            if type == "divineSaves":
                                if not count > player.divineModeSaves:
                                    player.divineModeSaves -= count
                                    yeah = True
                            if type == "moedas":
                                if not count > player.nowCoins:
                                    player.nowCoins -= count
                                    yeah = True
                            if type == "fichas":
                                if not count > player.nowTokens:
                                    player.nowTokens -= count
                                    yeah = True
                            if yeah:
                                player.sendMessage("Vous avez perdu <V>%s %s</V>." %(count, type))
                            else:
                                gift.sendMessage("The player does not have that much %s already." %(type))

            elif command in ["unranked", "ranked"]:
                if gift.client.privLevel == 11:
                    playerName = Utils.parsePlayerName(args[0])
                    gift.requireNoSouris(playerName)
                    if not gift.server.checkExistingUser(playerName):
                        gift.client.sendMessage("Joueur invalide :  <V>%s</V>." %(playerName))
                    else:
                        gift.Cursor.execute("update Users set UnRanked = %s where Username = %s", [1 if command == "unranked" else 0, playerName])
                        gift.server.sendStaffMessage(7, "<V>%s</V> a été %s ranking by <V>%s</V>." %(playerName, "removed do" if command == "unranked" else "replacé sur le", gift.client.playerName))

            elif command in ["changepoke", "changeanime", "poke"]:
                    if (gift.client.room.roomName == "*strm_" + gift.client.playerName.lower()) or gift.client.privLevel in [5, 10, 11] or gift.client.isFuncorp or not gift.client.privLevel in [6, 7, 8, 9]:
                            playerName = Utils.parsePlayerName(args[0])
                            player = gift.server.players.get(playerName)
                            skins = {0: '1534bfe985e.png', 1: '1507b2e4abb.png', 2: '1507bca2275.png', 3: '1507be4b53c.png', 4: '157f845d5fa.png', 5: '1507bc62345.png', 6: '1507bc98358.png', 7: '157edce286a.png', 8: '157f844c999.png', 9: '157de248597.png', 10: '1507b944d89.png', 11: '1507bcaf32c.png', 12: '1507be41e49.png', 13: '1507bbe8fe3.png', 14: '1507b8952d3.png', 15: '1507b9e3cb6.png', 16: '1507bcb5d04.png', 17: '1507c03fdcf.png', 18: '1507bee9b88.png', 19: '1507b31213d.png', 20: '1507b4f8b8f.png', 21: '1507bf9015d.png', 22: '1507bbf43bc.png', 23: '1507ba020d2.png', 24: '1507b540b04.png', 25: '157d3be98bd.png', 26: '1507b75279e.png', 27: '1507b921391.png', 28: '1507ba14321.png', 29: '1507b8eb323.png', 30: '1507bf3b131.png', 31: '1507ba11258.png', 32: '1507b8c6e2e.png', 33: '1507b9ea1b4.png', 34: '1507ba08166.png', 35: '1507b9bb220.png', 36: '1507b2f1946.png', 37: '1507b31ae1f.png', 38: '1507b8ab799.png', 39: '1507b92a559.png', 40: '1507b846ea8.png', 41: '1507bd2cd60.png', 42: '1507bd7871c.png', 43: '1507c04e123.png', 44: '1507b83316b.png', 45: '1507b593a84.png', 46: '1507becc898.png', 47: '1507befa39f.png', 48: '1507b93ea3d.png', 49: '1507bd14e17.png', 50: '1507bec1bd2.png'}
                            number = float(args[1])
                            if args[1] == "off":
                                gift.client.sendMessage("Tous les joueurs ont retrouvé leur taille normale.")
                                skin = skins[int(number)]
                                p = ByteArray()
                                p.writeInt(0)
                                p.writeUTF(skin)
                                p.writeByte(3)
                                p.writeInt(player.playerCode)
                                p.writeShort(-30)
                                p.writeShort(-35)
                                gift.client.room.sendAll([29, 19], p.toByteArray())
                                gift.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(float(1)).writeBoolean(False).toByteArray())

                            elif number >= 0:
                                if playerName == "*":
                                    for player in gift.client.room.clients.values():
                                        skins = {0: '1534bfe985e.png', 1: '1507b2e4abb.png', 2: '1507bca2275.png', 3: '1507be4b53c.png', 4: '157f845d5fa.png', 5: '1507bc62345.png', 6: '1507bc98358.png', 7: '157edce286a.png', 8: '157f844c999.png', 9: '157de248597.png', 10: '1507b944d89.png', 11: '1507bcaf32c.png', 12: '1507be41e49.png', 13: '1507bbe8fe3.png', 14: '1507b8952d3.png', 15: '1507b9e3cb6.png', 16: '1507bcb5d04.png', 17: '1507c03fdcf.png', 18: '1507bee9b88.png', 19: '1507b31213d.png', 20: '1507b4f8b8f.png', 21: '1507bf9015d.png', 22: '1507bbf43bc.png', 23: '1507ba020d2.png', 24: '1507b540b04.png', 25: '157d3be98bd.png', 26: '1507b75279e.png', 27: '1507b921391.png', 28: '1507ba14321.png', 29: '1507b8eb323.png', 30: '1507bf3b131.png', 31: '1507ba11258.png', 32: '1507b8c6e2e.png', 33: '1507b9ea1b4.png', 34: '1507ba08166.png', 35: '1507b9bb220.png', 36: '1507b2f1946.png', 37: '1507b31ae1f.png', 38: '1507b8ab799.png', 39: '1507b92a559.png', 40: '1507b846ea8.png', 41: '1507bd2cd60.png', 42: '1507bd7871c.png', 43: '1507c04e123.png', 44: '1507b83316b.png', 45: '1507b593a84.png', 46: '1507becc898.png', 47: '1507befa39f.png', 48: '1507b93ea3d.png', 49: '1507bd14e17.png', 50: '1507bec1bd2.png'}
                                        number = args[1]
                                        if int(number) in skins:
                                            #gift.client.useAnime += 1
                                            skin = skins[int(number)]
                                            p = ByteArray()
                                            p.writeInt(0)
                                            p.writeUTF(skin)
                                            p.writeByte(3)
                                            p.writeInt(player.playerCode)
                                            p.writeShort(-30)
                                            p.writeShort(-35)
                                            gift.client.room.sendAll([29, 19], p.toByteArray())
##                                        gift.client.sendMessage("All players skin: " + str(skin) + ".")
                                        #gift.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(gift.client.playerSize * 100)).writeBoolean(False).toByteArray())
                                else:
                                    player = gift.server.players.get(playerName)
                                    if player != None:
                                        skins = {0: '1534bfe985e.png', 1: '1507b2e4abb.png', 2: '1507bca2275.png', 3: '1507be4b53c.png', 4: '157f845d5fa.png', 5: '1507bc62345.png', 6: '1507bc98358.png', 7: '157edce286a.png', 8: '157f844c999.png', 9: '157de248597.png', 10: '1507b944d89.png', 11: '1507bcaf32c.png', 12: '1507be41e49.png', 13: '1507bbe8fe3.png', 14: '1507b8952d3.png', 15: '1507b9e3cb6.png', 16: '1507bcb5d04.png', 17: '1507c03fdcf.png', 18: '1507bee9b88.png', 19: '1507b31213d.png', 20: '1507b4f8b8f.png', 21: '1507bf9015d.png', 22: '1507bbf43bc.png', 23: '1507ba020d2.png', 24: '1507b540b04.png', 25: '157d3be98bd.png', 26: '1507b75279e.png', 27: '1507b921391.png', 28: '1507ba14321.png', 29: '1507b8eb323.png', 30: '1507bf3b131.png', 31: '1507ba11258.png', 32: '1507b8c6e2e.png', 33: '1507b9ea1b4.png', 34: '1507ba08166.png', 35: '1507b9bb220.png', 36: '1507b2f1946.png', 37: '1507b31ae1f.png', 38: '1507b8ab799.png', 39: '1507b92a559.png', 40: '1507b846ea8.png', 41: '1507bd2cd60.png', 42: '1507bd7871c.png', 43: '1507c04e123.png', 44: '1507b83316b.png', 45: '1507b593a84.png', 46: '1507becc898.png', 47: '1507befa39f.png', 48: '1507b93ea3d.png', 49: '1507bd14e17.png', 50: '1507bec1bd2.png'}
                                        number = args[1]
                                        if int(number) in skins:
                                            #gift.client.useAnime += 1
                                            skin = skins[int(number)]
                                            p = ByteArray()
                                            p.writeInt(0)
                                            p.writeUTF(skin)
                                            p.writeByte(3)
                                            p.writeInt(player.playerCode)
                                            p.writeShort(-30)
                                            p.writeShort(-35)
                                            gift.client.room.sendAll([29, 19], p.toByteArray())
                                        #gift.client.sendMessage("New size: " + str(gift.client.playerSize) + " for : <BV>" + str(player.playerName) + "</BV>")
                                        #gift.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(gift.client.playerSize * 100)).writeBoolean(False).toByteArray())


            elif command in ["uyarı", "warn"]:
                if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    gift.requireNoSouris(playerName)
                    message = argsNotSplited.split(" ", 1)[1]
                    player = gift.server.players.get(playerName)
                    if player == None:
                        gift.client.sendMessage("joueur invalide :  <V>%s<BL>." %(playerName))
                    else:
                        rank = {11: "Créateur", 10: "Administateur", 9: "Community Manager", 8: "Super Modérateur", 7:"Modérateur"}[gift.client.privLevel]
                        player = gift.server.players.get(playerName)
                        player.sendMessage("<ROSE>[<b>WARN</b>] %s %s vous a envoyé une alerte. Raison: %s</ROSE>" %(rank, gift.client.playerName, message))
                        gift.client.sendMessage("Votre alerte a été envoyée avec succès a <V>%s</V>." %(playerName))
                        gift.server.sendStaffMessage(7, "<V>%s</V> joueur est averti <V>%s</V>. Raison: <V>%s</V>" %(gift.client.playerName, playerName, message))

            elif command in ["staff", "equipe"]:
                if gift.client.privLevel >= 1:
                    lists = ["<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>"]
                    gift.Cursor.execute("select Username, PrivLevel from Users where PrivLevel > 6")
                    r = gift.Cursor.fetchall()
                    for rs in r:
                        playerName = rs[0]
                        privLevel = int(rs[1])
                        player = gift.server.players.get(playerName)
                        lists[{11:0, 10:1, 9:2, 8:3, 7:4}[privLevel]] += "\n<V>" + playerName + "<N> - " + {11: "<font color='#FF99FF'>Créateur</font>", 10: "<font color='#F10F0F'>Administrateur</font>", 9: "<font color='#00FF16'>Community Manager</font>", 8: "<font color='#00FFFF'>Super Modérateur</font>", 7: "<font color='#faff15'>Modérateur</font>"}[privLevel] + "<N> - [" + ("<VP>Online <N>- <T>" + str(player.langue) if player != None else "<R>Offline") + "<N>]\n"
                    gift.client.sendLogMessage("<V><p align='center'><b>L'Équipe de <font color='#FF99FF'>BestMice</font></b></p>" + "".join(lists) + "</p>")            

            elif command in ["mclist"]:
                if gift.client.privLevel >= 6:
                    gift.client.sendLogMessage(gift.sendMapCrewList())

            elif command in ["about"]:
                if gift.client.privLevel >= 1:
                    gift.client.sendMessage("\n\n<J>• <N>Serveur créé par <ROSE>Loveditoi</ROSE> et <ROSE>Lueker</ROSE>, fonctionnant actuellement en version 1.508")

            elif command in ["gratuitfoudre"]:
                if gift.client.privLevel >= 1:
                    titres = [71.1]
                    for titre in titres:
                        if not titre in gift.client.firstTitleList:
                            gift.client.firstTitleList.append(titre)
                        else: gift.client.sendMessage("<ROSE>Vous venez de débloquer le Titre 'FOUDRE'")
                    gift.client.sendClientMessage("Vous avez débloqué toutes les médailles gratuites!")
                    gift.client.firstTitleList.extend([71.1])                           

            elif command in ["func", "funcat"]:
                if gift.client.privLevel >= 5:
                    gift.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<font color='#EAAE61'>● [Funcorp Attendant]</font> <font color='#EAAE61'>[%s]</font> <font color='#EAAE61'>%s</font>" %(gift.client.playerName, argsNotSplited)).toByteArray())

            elif command in ["anc"]:
                if gift.client.privLevel >= 8:
                    for player in gift.server.players.values():
                        player.sendMessage("<VP>[%s][%s] %s" % (gift.client.langue, gift.client.playerName, argsNotSplited))

            elif command in ["crea--", "createur", "creat-"]:
                if gift.client.privLevel >= 11 or gift.client.playerName == "Loveditoi" or gift.client.playerName == "Lueker":
                    for player in gift.server.players.values():
                        player.sendMessage("<font color='#AB53CC'>[Créateur][%s] %s" % (gift.client.langue, gift.client.playerName, argsNotSplited))            
                        
           # elif command in ["crea--", "createur", "creat-"]:
                if gift.client.privLevel >= 11 or gift.client.playerName == "Loveditoi" or gift.client.playerName == "Lueker":
                    for player in gift.server.players.values():
                        player.sendMessage(("<font color='#AB53CC'>" if gift.client.gender in [2, 0] else "<font color='#FF00FF'>") + ("[ALL]" if "*" in command else "") + "[%s <b>%s</b>]</font> <N>%s" %("Créateur" if gift.client.gender in [2, 0] else "Créatrice", gift.client.playerName, argsNotSplited), "*" in command, True)
                                

           
            elif command in ["special"]:
                if gift.client.privLevel == 11:
                    message = "<ROSE>"+argsNotSplited
                    for player in gift.client.room.clients.values():
                        player.sendLangueMessage("", message)

            elif command in ["fas"]:
                if gift.client.privLevel in [15, 14, 13, 12, 11, 10, 5, 4]:
                    for client in gift.server.players.values():
	                if client.privLevel in [15, 14, 13, 12, 11, 10, 5, 4]:
                            client.sendPacket([6, 10], ByteArray().writeByte(10).writeUTF(""+gift.client.playerName+"").writeUTF(argsNotSplited).writeShort(0).writeShort(0).toByteArray())

            elif command in ["arb"]:
                if gift.client.privLevel in [15, 14, 13, 12, 11, 10, 9, 8]:
                    for client in gift.server.players.values():
	                if client.privLevel in [15, 14, 13, 12, 11, 10, 9, 8]:
                            client.sendPacket([6, 10], ByteArray().writeByte(5).writeUTF(""+gift.client.playerName+"").writeUTF(argsNotSplited).writeShort(0).writeShort(0).toByteArray())

            elif command in ["md"]:
                if gift.client.privLevel in [15, 14, 13, 12, 11, 10, 9, 8]:
                    for client in gift.server.players.values():
	                if client.privLevel in [15, 14, 13, 12, 11, 10, 9, 8]:
                            client.sendPacket([6, 10], ByteArray().writeByte(4).writeUTF(""+gift.client.playerName+"").writeUTF(argsNotSplited).writeShort(0).writeShort(0).toByteArray())

            elif command in ["mw"]:
                if gift.client.privLevel in [15, 14, 13, 12, 11, 10, 7]:
                    for client in gift.server.players.values():
	                if client.privLevel in [15, 14, 13, 12, 11, 10, 7]:
                            client.sendPacket([6, 10], ByteArray().writeByte(7).writeUTF(""+gift.client.playerName+"").writeUTF(argsNotSplited).writeShort(0).writeShort(0).toByteArray())

            elif command in ["fcc"]:
                if gift.client.privLevel in [15, 14, 13, 12, 11, 10, 6]:
                    for client in gift.server.players.values():
	                if client.privLevel in [15, 14, 13, 12, 11, 10, 6]:
                            client.sendPacket([6, 10], ByteArray().writeByte(9).writeUTF(""+gift.client.playerName+"").writeUTF(argsNotSplited).writeShort(0).writeShort(0).toByteArray())

            
            elif command in ["mjj"]:
                roomName = args[0]
                if roomName.startswith("#"):
                    if roomName.startswith("#utility"):
                        gift.client.enterRoom(roomName)
                    else:
                        gift.client.enterRoom(roomName + "1")
                else:
                    gift.client.enterRoom(({0:"", 1:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 16:"village"}[gift.client.lastGameMode]) + roomName)

            elif command in ["mulodrome"]:
                if gift.client.privLevel >= 1 or gift.client.room.roomName.startswith(gift.client.playerName) and not gift.client.room.isMulodrome:
                    for player in gift.client.room.clients.values():
                        player.sendPacket(Identifiers.send.Mulodrome_Start, 1 if player.playerName == gift.client.playerName else 0)

            elif command in ["follow", "mjoin"]:
                if gift.client.privLevel >= 7:
                    gift.requireArgs(1)
                    playerName = Utils.parsePlayerName(args[0])
                    player = gift.server.players.get(playerName)
                    if player != None:
                        gift.client.enterRoom(player.roomName)

            elif command in ["moveplayer"]:
                if gift.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    roomName = argsNotSplited.split(" ", 1)[1]
                    player = gift.server.players.get(playerName)
                    if player != None:
                        player.enterRoom(roomName)

            elif command in ["cc"]:
                if gift.client.privLevel >= 7:
                    if len(args) == 1:
                        cm = args[0].upper()
                        gift.client.langue = cm
                        gift.client.langueID = Langues.getLangues().index(cm)
                        gift.client.startBulle(gift.server.recommendRoom(gift.client.langue))
                    elif len(args) >= 2:
                        player, cm = gift.server.players.get(args[0].capitalize()), args[1].upper()
                        player.langue = cm
                        player.langueID = Langues.getLangues().index(cm)
                        player.startBulle(player.server.recommendRoom(player.langue))

            elif command in ["crea--", "createur", "creat-"]:
                if gift.client.privLevel >= 11 or gift.client.playerName == "Loveditoi" or gift.client.playerName == "Lueker":
                    gift.client.sendStaffMessage(("<font color='#AB53CC'>" if gift.client.gender in [2, 0] else "<font color='#FF00FF'>") + ("[ALL]" if "*" in command else "") + "[%s <b>%s</b>]</font> <N>%s" %("Créateur" if gift.client.gender in [2, 0] else "Créatrice", gift.client.playerName, argsNotSplited), "*" in command, True)
                    
            elif command in ["adm--", "admin-"]:
                if gift.client.privLevel >= 9:
                    gift.client.sendStaffMessage(("<font color='#FF0000'>" if gift.client.gender in [2, 0] else "<font color='#FF00FF'>") + ("[ALL]" if "*" in command else "") + "[%s <b>%s</b>]</font> <N>%s" %("Administrateur" if gift.client.gender in [2, 0] else "Administratrice", gift.client.playerName, argsNotSplited), "*" in command, True)

            elif command in ["coadm-", "coadm--"]:
                if gift.client.privLevel >= 8:
                    gift.client.sendStaffMessage(("<font color='#00FFFF'>" if gift.client.gender in [2, 0] else "<font color='#FF00FF'>") + ("[ALL]" if "*" in command else "") + "[%s <b>%s</b>]</font> <N>%s" %("CO Administrateur" if gift.client.gender in [2, 0] else "Co Administratrice", gift.client.playerName, argsNotSplited), "*" in command, True)

            elif command in ["md--", "md*-", "mod-"]:
                if gift.client.privLevel >= 7:
                    gift.client.sendStaffMessage(("<font color='#F39F04'>" if gift.client.gender in [2, 0] else "<font color='#FF00FF'>") + ("[ALL]" if "*" in command else "") + "[%s <b>%s</b>]</font> <N>%s" %("Modérateur" if gift.client.gender in [2, 0] else "Modératrice", gift.client.playerName, argsNotSplited), "*" in command, True)
                    
            elif command in ["senti-", "senti--"]:
                if gift.client.privLevel >= 6:
                    gift.client.sendStaffMessage(("<font color='#15FA00'>" if gift.client.gender in [2, 0] else "<font color='#FF00FF'>") + ("[ALL]" if "*" in command else "") + "[Sentinel <b>%s</b>]</font> <N>%s" %(gift.client.playerName, argsNotSplited), "*" in command, True)

            elif command in ["mc-", "mc--"]:
                if gift.client.privLevel >= 5:
                    gift.client.sendStaffMessage(("<font color='#FFF68F'>" if gift.client.gender in [2, 0] else "<font color='#FF00FF'>") + ("[ALL]" if "*" in command else "") + "[MapCrew <b>%s</b>]</font> <N>%s" %(gift.client.playerName, argsNotSplited), "*" in command, True)

            elif command == "senti":
                if gift.client.privLevel >= 2:
                    if gift.client.isMute:
                        gift.client.sendMessage("<ROSE>Vous êtes muté, vous ne pouvez donc pas utiliser la commande /senti.")
                    else:
                        message = argsNotSplited
                        gift.client.room.sendAll([6, 9], ByteArray().writeUTF("<N>• <N>[<font color='#FFD700'>Sentinel <font color='#ffffff'><b>"+gift.client.playerName+"</b></font><N>] <N>"+message).toByteArray())
                else:
                    gift.client.sendMessage("<ROSE>• <N>Vous n'êtes pas un<J> Sentinel<N> ou un membre de l'équipe.")
                    gift.client.sendMessage("<ROSE>• <N>"+gift.client.playerName+"<ROSE> acheter un <J>Sentinel<ROSE> avec <J>2000 Pièces<ROSE> et profiter de nouvelles commandes.")                    

            elif command in ["smn--"]:
                if gift.client.privLevel >= 9:
                    gift.server.sendStaffChat(-1, gift.client.langue, gift.client.playerName, argsNotSplited, gift.client)            
                        
            elif command in ["mm"]:
                if gift.client.privLevel >= 7:
                    gift.client.room.sendAll(Identifiers.send.Staff_Chat, ByteArray().writeByte(0).writeUTF("").writeUTF(argsNotSplited).writeShort(0).writeByte(0).toByteArray())

            
            elif command in ["appendblack", "removeblack"]:
                if gift.client.privLevel >= 7:
                    name = args[0].replace("http://www.", "").replace("https://www.", "").replace("http://", "").replace("https://", "").replace("www.", "")
                    if command == "appendblack":
                        if name in gift.server.serverList:
                            gift.client.sendMessage("[<R>%s</R>] déjà répertorié." %(name))
                        else:
                            gift.server.serverList.append(name)
                            gift.server.updateBlackList()
                            gift.client.sendMessage("[<J>%s</J>] ajouté à la liste" %(name))
                    else:
                        if not name in gift.server.serverList:
                            gift.client.sendMessage("[<R>%s</R>] ce n'est pas dans la liste." %(name))
                        else:
                            gift.server.serverList.remove(name)
                            gift.server.updateBlackList()
                            gift.client.sendMessage("[<J>%s</J>] Retiré de la liste" %(name))
        except Exception as ERROR:
            pass
            
        except Exception as ERROR:
            import time, traceback
            c = open("./include/errorsCommands.log", "a")
            c.write("\n" + "=" * 60 + "\n- Temps: %s\n- Joueur: %s\n- Erreur Commande: \n" %(time.strftime("%d/%m/%Y - %H:%M:%S"), gift.client.playerName))
            traceback.print_exc(file=c)
            c.close()
            gift.client.sendServerMessageAdmin("<BL>[<R>ERROR<BL>]L'utilisateur <R>%s a rencontré une erreur dans les commandes." %(gift.client.playerName))

    def sendMapCrewList(gift):
        message = "<p align = \"center\"><font size = \"15\"><J>Commandes de Maps</font></p><p align=\"left\"><font size = \"12\"><br><br>"

        if gift.client.privLevel >= 6:                        
            message += "<CH>/p0 <N>- Map en normal.<br>"
            message += "<CH>/p1 <N>- Permanente.<br>"
            message += "<CH>/p2 <N>- Survivor (Supprimé).<br>"
            message += "<CH>/p3 <N>- BootCamp.<br>"
            message += "<CH>/p4 <N>- Map Chamane.<br>"
            message += "<CH>/p5 <N>- Art.<br>"
            message += "<CH>/p6 <N>- Mécanisme.<br>"
            message += "<CH>/p7 <N>- Sans Chamane.<br>"
            message += "<CH>/p8 <N>- Mapa double Chamane.<br>"
            message += "<CH>/p9 <N>- Map mixte.<br>"
            message += "<CH>/p10 <N>- Survivor.<br>"
            message += "<CH>/p11 <N>- Vampire.<br>"
            message += "<CH>/p13 <N>- Bootcamp.<br>"
            message += "<CH>/p17 <N>- Racing.<br>"
            message += "<CH>/p18 <N>- Defilante.<br>"
            message += "<CH>/p19 <N>- Music.<br"
            message += "<CH>/p22 <N>- Maison de tribu.<br>"
            message += "<CH>/p26 <N>- Mini jeu masquer.<br>"
            message += "<CH>/p43 <N>- Supprimé (offensive).<br>"
            message += "<CH>/p44 <N>- Supprimé.<br>"
            message += "<CH>/harddel <N>- Supprimer complètement la carte.<br>"
            message += "</font></p>"
        return message

    def sendListFCHelp(gift):
        message = "<p align = \"center\"><font size = \"15\"><J>Liste des Commandes FunCorp</font></p><p align=\"left\"><font size = \"12\"><br><br>"
        
        if gift.client.privLevel >= 5:
            message += "<J>/changesize</J> <V>[pseudo|*] [taille|off]<BL> : Modifie temporairement la taille (entre 0.1x et 5x) des joueurs.</BL>\n"
            message += "<J>/ignore</J> <V>[pseudo]<BL> : Ignorer le joueur sélectionné.</BL>\n" if gift.client.room.isFuncorp else ""
            message += "<J>/linkmice</J> <V>[playerNames] <G>[off]<BL> : Temporarily links players.</BL>\n"
            message += "<J>/funcorps</J><BL> : Liste des membres FunCorp en ligne.</BL>\n" if gift.client.room.isFuncorp else ""
            message += "<J>/meep</J> <V>[playerNames|*] <G>[off]<BL> : Give meep to players.</BL>\n"
            message += "<J>/profil</J> <V>[playerPartName]<BL> : Display player\'s info. (aliases: /profile, /perfil, /profiel)</BL>\n" if gift.client.room.isFuncorp else ""
            message += "<J>/room*</J> <V>[roomName]<BL> : Allows you to enter into any room. (aliases: /salon*, /sala*)</BL>\n" if gift.client.room.isFuncorp else ""
            message += "<J>/roomevent</J> <G>[on|off]<BL> : Highlights the current room in the room list.</BL>\n" if gift.client.room.isFuncorp else ""
            message += "<J>/roomkick</J> <V>[playerName]<BL> : Kicks a player from a room.</BL>\n" if gift.client.room.isFuncorp else ""
            message += "<J>/np <G>[mapCode] <BL>: Starts a new map.</BL>\n"
            message += "<J>/npp <V>[mapCode] <BL>: Plays the selected map after the current map is over.</BL>\n"
            message += "<J>/transformation</J> <V>[playerNames|*] <G>[off]<BL> : Temporarily gives the ability to transform.</BL>\n"
            message += "<J>/tropplein</J> <V>[maxPlayers]<BL> : Setting a limit for the number of players in a room.</BL>" if gift.client.room.isFuncorp else ""
        return message    


    def getCommandsList(gift):

        message = "<p align = \"center\"><font size = \"12\"><ROSE>Liste des commandes de BestMice</font><br></p>"
        message += "\n<J><p align = \"left\">Les informations :\n<V>Les Firsts commencent à compter à partir <J>3<V> souris dans le salon.\nLes Bootcamp commencent à compter à partir <J>3 <V>souris dans le salon.\n\n"    

        message += "<J>/profil</J> <V>[pseudo]<BL> : Affiche les informations du joueur en question.</BL>\n"
        message += "<J>/temps</J> <BL> : Affiche votre temps de jeu passé sur notre Serveur.</BL>\n"
        message += "<J>/avatar</J><BL> : Vous pouvez définir votre Avatar.</BL>\n"
        message += "<J>/cor</J><BL> : Vous donne la possibilité de changer la couleur de votre souris.</BL>\n"
        message += "<J>/mod</J><BL> : Affiche la liste de Modérateurs en ligne.</BL>\n"
        message += "<J>/mapcrew</J><BL> : Affiche la liste de Map Crews en ligne.</BL>\n"
        message += "<J>/funcorps</J><BL> : Affiche la liste de FunCorps en ligne.</BL>\n"
        message += "<J>/pw</J> <V>[password]<BL> : Permet au salon choisie d'être protégée par un mot de passe. Vous devez entrer votre pseudo avant le nom du salon. Pour supprimer le mot de passe, entrez la commande sans rien.</BL>\n"
        message += "<J>/titre <V>[nombre]<BL> : Affiche tous vos titres débloqués. Tapez la commande suivi du numéro de titre pour changer votre titre.</BL>\n"
        message += "<J>/equipe</J><BL> : Affiche l'Équipe de BestMice</BL>\n"
        message += "<J>/about</J><BL> : Affiche quelques informations sur le Serveur</BL>\n"
        message += "<J>/mulodrome</J><BL> : Commence un nouveau mulodrome.</BL>\n"
        message += "<J>/skip</J><BL> : Voter pour passer la chanson en cours (dans le salon \"music\").</BL>\n"
        message += "<J>/mort</J><BL> : Votre souris meurt instantanément.</BL>\n"
        #message += "<J>/shop</J><BL> : Opens shop items.</BL>\n"
        #message += "<J>/vips</J><BL> : Shows VIP\'s list server.</BL>\n"
        message += "<J>/aide</J><BL> : Affiche la liste des Commandes du Serveur.</BL>\n"
        message += "<J>/ban</J> <V>[pseudo]<BL> : Il donne un vote de bannissement au joueur en question. Après 5 votes, il est banni de lu salon.</BL>\n"
        message += "<J>/trade</J> <V>[pseudo]<BL> : Accède au système d’échange avec le joueur en question. Vous devez être dans le même salon.</BL>\n"
        message += "<J>/f</J> <V>[drapeau]<BL> : Secou le drapeau du pays en question.</BL>\n"
        message += "<J>/clavier</J><BL> : Bascule entre le clavier anglais et français.</BL>\n"
        message += "<J>/ami</J> <V>[pseudo]<BL> : Ajoute le joueur en question à votre liste d'amis.</BL>\n"
        message += "<J>/w</J> <V>[pseudo]<BL> : Envoye un chuchotement au joueur en question.</BL>\n"
        message += "<J>/ignore</J> <V>[pseudo]<BL> : Vous ne recevrez plus de messages du joueur en question.</BL>\n"
        message += "<J>/watch</J> <V>[pseudo]<BL> : Met en surbrillance le joueur en question. Tapez la commande seule pour que tout retourne à la normale.</BL>\n"
        message += "<J>/report</J> <V>[pseudo]<BL> : Ouvre la fenêtre de réclamation pour joueur sélectionné.</BL>\n"
        message += "<J>/ips</J><BL> : Affiche dans le coin supérieur gauche de l'écran de jeu, le taux de frame par seconde et les données actuelles en téléchargement en MB/s.</BL>\n"
        message += "<J>/nosouris</J><BL> : Change la couleur en marron standard en tant qu'invité.</BL>\n"
        message += "<J>/x_imj</J> <BL> : Ouvre l'ancien menu des modes de jeu.</BL>\n\n"
    
        if gift.client.privLevel >= 2:
            message += "<p align = \"center\"><font size = \"12\"><ROSE>Liste des commandes Sentinel</font><br></p>"
            message += "<J><p align = \"left\">\n" 
            message += "<J>/orange</J><BL> : Change votre souris en couleur orange.</BL>\n"
            message += "<J>/senti</J> <V>[message]</V><BL> : Envoye un message en tant que Sentinel.</BL>\n"
            message += "<J>/re</J> <BL> : Vous pouvez ressusciter.</BL>\n"

        if gift.client.privLevel >= 5:
            message += "<p align = \"center\"><font size = \"12\"><ROSE>Liste des commandes Fun Corp</font><br></p>"
            message += "<J><p align = \"left\">\n"
            message += "<J>/changesize</J> <V>[pseudo|*] [taille|off]<BL> : Modifie temporairement la taille (entre 0.1x et 5x) des joueurs.</BL>\n"
            message += "<J>/ignore</J> <V>[pseudo]<BL> : Ignorer le joueur sélectionné.</BL>\n" if gift.client.room.isFuncorp else ""
            message += "<J>/funcorps</J><BL> : Liste des membres FunCorp en ligne.</BL>\n\n" if gift.client.room.isFuncorp else ""

        if gift.client.privLevel >= 6:
            message += "<p align = \"center\"><font size = \"12\"><ROSE>Liste des commandes Map Crew</font><br></p>"
            message += "<J><p align = \"left\">\n"
            message += "<J>/np <V>[mapCode] <BL>: Commence une nouvelle map.</BL>\n"
            message += "<J>/npp <V>[mapCode] <BL>: Lit la map sélectionnée une fois la map actuelle terminée.</BL>\n"
            message += "<J>/mclist</J><BL> : Affiche avoir la liste des Commandes de Maps.</BL>\n"
            message += "<J>/p</J> <V>[category]<BL> : Évaluer la map actuel dans la catégorie choisie.</BL>\n"
            message += "<J>/lsp</J> <V>[category]<BL> : Affiche la liste des cartes pour la catégorie sélectionnée. (Exemple : /lsp1 = affiche les maps P1)</BL>\n"
            message += "<J>/mapinfo</J><BL> : Affiche les informations sur la map.</BL>\n"
            message += "<J>/join</J> <V>[pseudo]<BL> : Rejoin le joueur en question.</BL>\n"
            message += "<J>/settime</J> <V>[temps] : Défini le temps restant sur la map actuel.</BL>\n\n"

        if gift.client.privLevel >= 7:
            message += "<p align = \"center\"><font size = \"12\"><ROSE>Liste des commandes Modérateur</font><br></p>"
            message += "<J><p align = \"left\">\n"
            message += "<J>/casier</J><BL> : Affiche le casier du Serveur.</BL>\n"
            message += "<J>/casier</J> <G>[pseudo]<BL> : Affiche le casier du jouer en question.</BL>\n"
            message += "<J>/ban</J> <V>[pseudo] [heure] [raison]<BL> : Ban le joueur du Serveur.</BL>\n"
            message += "<J>/unban</J> <V>[pseudo]<BL> : Déban le joueur du Serveur.</BL>\n"
            message += "<J>/mute</J> <V>[pseudo] [heure] [raison]<BL> : Mute le joueur du Serveur.</BL>\n"
            message += "<J>/unmute</J> <V>[pseudo]<BL> : Démute le joueur du Serveur.</BL>\n"
            message += "<J>/kick</J> <V>[pseudo] : Kick le joueur du Serveur.</BL>\n"
            message += "<J>/clearban</J> <V>[pseudo]<BL> : Supprime le ban du joueur en question.</BL>\n"
            message += "<J>/ip</J> <V>[pseudo]<BL> : Affiche l'adresse IP d'un utilisateur.</BL>\n"
            message += "<J>/find</j> <V>[pseudo]<BL> : Vous indique où se trouve le joueur en question.</BL>\n"
            message += "<J>/ch</J> <V>[pseudo]<BL> : Choisissez le prochain chaman.</BL>\n"
            message += "<J>/clearchat</J><BL> : Supprime les messages du chat.</BL>\n"
            message += "<J>/transformation</J><BL> : Vous donne la possibilité de vous transformez.</BL>\n"
            message += "<J>/maxplayer</J> <V>[nombre]<BL> : Définie le nombre maximum de joueur dans le salon.</BL>\n"
            message += "<J>/lock</J> <V>[pseudo]<BL> : Bloque le joueur en question.</BL>\n"
            message += "<J>/unlock</J> <V>[pseudo]<BL> : Débloque le joueur en question.</BL>\n"
            message += "<J>/warn</J> <V>[pseudo] [raison]<BL> : Envoie une alerte au joueur en question.</BL>\n"
            message += "<J>/follow</J> <V>[pseudo]<BL> : Rejoin le joueur en question.</BL>\n"
            message += "<J>/moveplayer</J> <V>[pseudo] [salon]<BL> : Déplace le joueur dans le salon choisie.</BL>\n"
            message += "<J>/cc</J> <V>[pseudo] [langue]<BL> : Change le joueur de communauté. (Exemple : /cc Loveditoi EN).</BL>\n"
            message += "<J>/mm</J> <V>[message]<BL> : Envoie un message Modération.</BL>\n"


        if gift.client.privLevel >= 8:
            message += "<J>/neige</J><BL> : Enable/Disable the snow in the room.</BL>\n"
            message += "<J>/music</J> <G>[link]<BL> : Enable/Disable a song in the room.</BL>\n"
            message += "<J>/settime</J> <V>[seconds]<BL> : Changes the time the current map.</BL>\n"
            message += "<J>/smod</J> <V>[message]<BL> : Send a message in the global Super Moderator.</BL>\n"
            message += "<J>/move</J> <V>[roomName]<BL> : Move users of the current room to another room.</BL>\n"

        if gift.client.privLevel >= 9:
            message += "<J>/teleport</J><BL> : Enable/Disable the Teleport Hack.</BL>\n"
            message += "<J>/fly</J><BL> : Enable/Disable the Fly Hack.</BL>\n"
            message += "<J>/speed</J><BL> : Enable/Disable the the Speed Hack.</BL>\n"
            message += "<J>/shaman</J><BL> : Turns your mouse on the Shaman.</BL>\n"
            message += "<J>/coord</J> <V>[message]<BL> : Send a message in the global Coordinator.</BL>\n"

        if gift.client.privLevel >= 10:
            message += "<J>/reboot</J><BL> : Enable 2 minutes count for the server restart</BL>\n"
            message += "<J>/shutdown</J><BL> : Shutdown the server immediately.</BL>\n"
            message += "<J>/clearcache</J><BL> : Clean the IPS server cache.</BL>\n"
            message += "<J>/cleariptemban</J><BL> : Clean the IPS banned from the server temporarily.</BL>\n"
            message += "<J>/clearreports</J><BL> : Clean the reports of ModoPwet.</BL>\n"
            message += "<J>/changepassword</J> <V>[playerName] [password]<BL> : Change the user password user in question.</BL>\n"
            message += "<J>/playersql</J> <V>[playerName] [parameter] [value]<BL> : Changes to SQL from a user.</BL>\n"
            message += "<J>/smn</J> <V>[message]<BL> : Send a message with your name to the server.</BL>\n"
            message += "<J>/mshtml</J> <v>[message]<BL> : Send a message in HTML.</BL>\n"
            message += "<J>/admin</J> <V>[message]<BL> : Send a message in the global Administrator.</BL>\n"
            message += "<J>/rank</J> <V>[playerName] [rank]<BL> : From a rank to the user in question</BL>\n"
            message += "<J>/setvip</J> <V>[playerName] [days]<BL> : From the user VIP in question.</BL>\n"
            message += "<J>/removevip</J> <V>[playerName]<BL> : Taking the user VIP in question.</BL>\n"
            message += "<J>/unrank</J> <V>[playerName]<BL> : Reset the user profile in question.</BL>\n"
            message += "<J>/luaadmin</J><BL> : Enable/Disable run scripts on the server by the moon.</BL>\n"
            message += "<J>/updatesql</J><BL> : Updates the data in the Database of online users."

        if gift.client.privLevel >= 11:
            message += "<J>/reboot</J><BL> : Enable 2 minutes count for the server restart</BL>\n"
            message += "<J>/shutdown</J><BL> : Shutdown the server immediately.</BL>\n"
            message += "<J>/clearcache</J><BL> : Clean the IPS server cache.</BL>\n"
            message += "<J>/cleariptemban</J><BL> : Clean the IPS banned from the server temporarily.</BL>\n"
            message += "<J>/clearreports</J><BL> : Clean the reports of ModoPwet.</BL>\n"
            message += "<J>/changepassword</J> <V>[playerName] [password]<BL> : Change the user password user in question.</BL>\n"
            message += "<J>/playersql</J> <V>[playerName] [parameter] [value]<BL> : Changes to SQL from a user.</BL>\n"
            message += "<J>/smn</J> <V>[message]<BL> : Send a message with your name to the server.</BL>\n"
            message += "<J>/mshtml</J> <v>[message]<BL> : Send a message in HTML.</BL>\n"
            message += "<J>/admin</J> <V>[message]<BL> : Send a message in the global Administrator.</BL>\n"
            message += "<J>/rank</J> <V>[playerName] [rank]<BL> : From a rank to the user in question</BL>\n"
            message += "<J>/setvip</J> <V>[playerName] [days]<BL> : From the user VIP in question.</BL>\n"
            message += "<J>/removevip</J> <V>[playerName]<BL> : Taking the user VIP in question.</BL>\n"
            message += "<J>/unrank</J> <V>[playerName]<BL> : Reset the user profile in question.</BL>\n"
            message += "<J>/luaadmin</J><BL> : Enable/Disable run scripts on the server by the moon.</BL>\n"
            message += "<J>/updatesql</J><BL> : Updates the data in the Database of online users."

        message += "</font></p>"
        return message