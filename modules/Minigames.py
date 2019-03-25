# -*- coding: utf-8 -*-
import re, struct, random, time

__author__ = "Duxo"
__date__ = "$7/06/2017 13:10:00$"

class Utility:
    def __init__(gift, client, server):
        gift.client = client
        gift.isCommand = False
        gift.lastObjID = 0
        gift.canExplosion = False
        gift.isFireworks = False
        gift.conjX = 0
        gift.conjY = 0

    def spawnObj(gift, objID, posX, posY, angle):
        itemID = random.randint(100, 999)
        objID = int(objID)
        posX = int(posX)
        posY = int(posY)
        data = struct.pack("!ihhhhhbb", itemID, objID, posX, posY, angle, 0, 1, 0)        
        gift.client.room.sendAll([5, 20], data)
        gift.lastObjID = struct.unpack("!i", data[:4])[0]        

    def removeObj(gift):
        gift.client.sendPacket([4, 8], struct.pack("!i?", gift.lastObjID, True))

    def playerWin(gift):
        timeTaken = int((time.time() - (gift.client.playerStartTimeMillis if gift.client.room.autoRespawn else gift.client.room.gameStartTimeMillis)) * 100)
        place = gift.client.room.numCompleted
        if place == 0:
            place = place + 1
        gift.client.sendPlayerWin(place, timeTaken)

    def buildConj(gift):
        if gift.isFireworks == True:
            gift.client.sendPacket([4, 14], [int(gift.conjX), int(gift.conjY)])    

    def removeConj(gift):
        if gift.isFireworks == True:
            gift.client.sendPacket([4, 15], [int(gift.conjX), int(gift.conjY)])

    def newCoordsConj(gift):
        gift.conjX = random.randint(0, 79)
        gift.conjY = random.randint(2, 39)

    def explosionPlayer(gift, posX, posY):
        data = struct.pack("!h", int(posX))
        data += "\x00\x842"
        data += struct.pack("!h?", int(posY), True)
        gift.client.sendPacket([5, 17], data)
    
    def moreSettings(gift, setting):
        if setting == "giveAdmin":
            if not gift.client.playerName in gift.client.room.adminsRoom:
                gift.client.room.adminsRoom.append(gift.client.playerName)

        elif setting == "join":
            gift.sendMessage("<J>Welcome to #utility!")
            gift.consoleChat(1, "", ""+str(gift.client.playerName)+" joined the room.")
            gift.client.sendPacket([29, 20], "\x00\x00\x1c\x16\x00t<font color=\'#000000\'><p align=\'center\'><b><font size=\'128\' face=\'Soopafresh,Verdana\'>#utility</font></b></p></font>\x00_\x00d\x02X\x00\xc8\x002FP\x00\x00\x00\x00\x00\x01")
            gift.client.sendPacket([29, 20], "\x00\x00\x1c{\x00t<font color=\'#000000\'><p align=\'center\'><b><font size=\'128\' face=\'Soopafresh,Verdana\'>#utility</font></b></p></font>\x00i\x00d\x02X\x00\xc8\x002FP\x00\x00\x00\x00\x00\x01")
            gift.client.sendPacket([29, 20], "\x00\x00\x1c\xe0\x00t<font color=\'#000000\'><p align=\'center\'><b><font size=\'128\' face=\'Soopafresh,Verdana\'>#utility</font></b></p></font>\x00d\x00_\x02X\x00\xc8\x002FP\x00\x00\x00\x00\x00\x01")
            gift.client.sendPacket([29, 20], "\x00\x00\x1dE\x00t<font color=\'#000000\'><p align=\'center\'><b><font size=\'128\' face=\'Soopafresh,Verdana\'>#utility</font></b></p></font>\x00d\x00i\x02X\x00\xc8\x002FP\x00\x00\x00\x00\x00\x01")
            gift.client.sendPacket([29, 20], "\xff\xff\xff\xed\x00W<p align=\'center\'><b><font size=\'128\' face=\'Soopafresh,Verdana\'>#utility</font></b></p>\x00d\x00d\x02X\x00\xc8\x002FP\x00\x00\x00\x00\x00\x01")
            gift.client.sendPacket([29, 20], "\xff\xff\xff\xf0\x00\x80<p align=\'center\'><a href=\'event:info' target='_blank'><b>?</b></a></p>\x00\x05\x00\x1c\x00\x10\x00\x10\x002FP\x002FPd\x00")
            gift.client.sendPacket([29, 20], "\xff\xff\xff\xef\x00><p align=\'center\'><a href=\'event:info\'><b><i>i</i></b></a></p>\x00!\x00\x1c\x00\x10\x00\x10\x002FP\x002FPd\x00")            
    
        elif setting == "removePopups":        
            popupID = [7190, 7291, 7392, 7493, -19]
            for id in popupID:
                gift.removePopups(id)        

    def removePopups(gift, popupID):
        gift.client.sendPacket([29, 22], struct.pack("!i", popupID))
            
    def consoleChat(gift, type, username, message):
        for client in gift.client.room.clients.values():
            if client.playerName in gift.client.room.adminsRoom:                
                if type == 1:
                    prefix = "<font color='#AAAAAA'>Ξ [Utility] "
                elif type == 2:
                    prefix = "<font color='#AAAAAA'>Ξ ["+str(username)+"] "

                elif type == 3:
                    prefix = ""

                message = prefix + message 
                
                client.sendPacket([6, 9], struct.pack("!h", len(message)) + message)

    def sendMessage(gift, message):
        gift.client.sendPacket([6, 9], struct.pack("!h", len(message)) + message)

    def staffChat(gift, username, message):
        for client in gift.client.room.clients.values():
            if client.playerName in gift.client.room.adminsRoom:
                prefix = "<font color='#00FFFF'>Ξ ["+str(username)+"] "
                client.Utility.sendMessage(prefix + message + "</font>")
    
    def sentCommand(gift, command):
        command = command[1:]
        if command == "admins":
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            admins = ', '.join(gift.client.room.adminsRoom)
            gift.sendMessage("The current room admins are: "+str(admins)+".")            
            gift.isCommand = True

        elif command.startswith("admin "):
            playerName = command.split(" ")[1]
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                if playerName in gift.client.room.adminsRoom:
                    gift.sendMessage(""+str(playerName)+" is already an admin.")
                else:
                    gift.client.room.adminsRoom.append(playerName)
                    for client in gift.client.room.clients.values():
                        client.Utility.sendMessage(""+str(playerName)+" is now an admin.")
            gift.isCommand = True

        elif command.startswith("me "):
            message = command.split(" ")[1]
            if not gift.client.playerName in gift.client.room.playersBan:
                for client in gift.client.room.clients.values():
                    client.Utility.sendMessage("<V>*"+str(gift.client.playerName)+" <N>"+str(message)+"")
            gift.isCommand = True

        elif command.startswith("c "):
            message = command.split(" ")[1]
            gift.staffChat(gift.client.playerName, message)
            gift.isCommand = True

        elif command.startswith("spawn "):
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.consoleChat(2, gift.client.playerName, "!" + command)
                try:
                    objID = command.split(" ")[1]
                except:
                    objID = 0
                try:
                    posX = command.split(" ")[2]
                except:
                    posX = 140
                try:
                    posY = command.split(" ")[3]
                except:
                    posY = 320
                gift.spawnObj(objID, posX, posY, 0)
            gift.isCommand = True

        elif command == "snow":
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.consoleChat(2, gift.client.playerName, "!" + command)
                gift.client.room.sendAll([5, 23], struct.pack("!?h", True, 10))
            gift.isCommand = True

        elif command.startswith("snow "):            
            event = command.split(" ")[1]
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.consoleChat(2, gift.client.playerName, "!" + command)
                if event == "on":
                    gift.client.room.sendAll([5, 23], struct.pack("!?h", True, 10))
                elif event == "off":
                    gift.client.room.sendAll([5, 23], struct.pack("!?h", False, 10))
            gift.isCommand = True

        elif command.startswith("time "):
            time = command.split(" ")[1]
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.consoleChat(2, gift.client.playerName, "!" + command)
                try:
                    if time > 32767:
                        time = 32767
                    gift.client.room.sendAll([5, 22], struct.pack("!H", int(time)))
                except:
                    time = 32767
                    gift.client.room.sendAll([5, 22], struct.pack("!H", int(time)))
            gift.isCommand = True

        elif command.startswith("ban "):
            playerName = command.split(" ")[1]
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.consoleChat(2, gift.client.playerName, "!" + command)
                if not playerName in gift.client.room.playersBan:
                    if playerName in gift.client.room.adminsRoom:
                        gift.sendMessage(""+str(playerName)+" is an admin and can't be banned.")
                    else:
                        gift.client.room.playersBan.append(playerName)
                        for client in gift.client.room.clients.values():
                            client.Utility.sendMessage("<R>"+str(playerName)+" has been banned.")            
                else:
                    gift.sendMessage(""+str(playerName)+" is already banned.")
            gift.isCommand = True

        elif command.startswith("unban "):
            playerName = command.split(" ")[1]
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                if playerName in gift.client.room.playersBan:
                    num = None
                    for i, x in enumerate(gift.client.room.playersBan):
                        if x == playerName:
                            num = i
                    del gift.client.room.playersBan[num]
                    for client in gift.client.room.clients.values():
                        client.Utility.sendMessage(""+str(playerName)+" has been unbanned.")
            gift.isCommand = True

        elif command == "banlist":
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.consoleChat(2, gift.client.playerName, "!" + command)
                banList = ' '.join(gift.client.room.playersBan)
                gift.sendMessage(str(banList))
            gift.isCommand = True

        elif command == "vampire":
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.consoleChat(2, gift.client.playerName, "!" + command)
                gift.client.room.sendAll([8, 66], struct.pack("!i", gift.client.playerCode))
            gift.isCommand = True

        elif command.startswith("vampire "):
            event = command.split(" ")[1]
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.consoleChat(2, gift.client.playerName, "!" + command)
                if not event in ["me", "all"]:
                    for client in gift.client.room.clients.values():
                        if event == client.playerName:
                            client.room.sendAll([8, 66], struct.pack("!i", client.playerCode))
                elif event == "me":
                    gift.client.room.sendAll([8, 66], struct.pack("!i", gift.client.playerCode))
                elif event == "all":
                    for client in gift.client.room.clients.values():
                        client.room.sendAll([8, 66], struct.pack("!i", client.playerCode))
            gift.isCommand = True

        elif command == "name":
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.consoleChat(2, gift.client.playerName, "!" + command)
                color = "000000"
                data = struct.pack("!i", gift.client.playerCode)
                data += struct.pack("!i", int(color, 16))
                gift.client.room.sendAll([29, 4], data)
            gift.isCommand = True
                
        elif command.startswith("name "):
            event = command.split(" ")[1]
            try:
                color = command.split(" ")[2]
            except:
                color = "000000"                
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.consoleChat(2, gift.client.playerName, "!" + command)
                if not event in ["me", "all"]:
                    for client in gift.client.room.clients.values():
                        if event == client.playerName:
                            data = struct.pack("!i", client.playerCode)
                            data += struct.pack("!i", int(color, 16))
                            client.room.sendAll([29, 4], data)                                                        
                elif event == "me":
                    data = struct.pack("!i", gift.client.playerCode)
                    data += struct.pack("!i", int(color, 16))
                    gift.client.room.sendAll([29, 4], data)
                elif event == "all":
                    for client in gift.client.room.clients.values():
                        data = struct.pack("!i", client.playerCode)
                        data += struct.pack("!i", int(color, 16))
                        client.room.sendAll([29, 4], data)                    
            gift.isCommand = True

        elif command.startswith("tp "):
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.consoleChat(2, gift.client.playerName, "!" + command)
                try:
                    posX = command.split(" ")[1]
                    posY = command.split(" ")[2]
                    if posX == "all":
                        try:
                            posX = command.split(" ")[2]
                            posY = command.split(" ")[3]
                            for client in gift.client.room.clients.values():
                                client.room.sendAll([8, 3], struct.pack("!hhih", int(posX), int(posY), 0, 0))
                        except:
                            pass
                    elif not posX.isdigit():
                        try:
                            playerName = command.split(" ")[1]
                            posX = command.split(" ")[2]
                            posY = command.split(" ")[3]
                            for client in gift.client.room.clients.values():
                                if playerName == client.playerName:
                                    client.room.sendAll([8, 3], struct.pack("!hhih", int(posX), int(posY), 0, 0))                                    
                        except:
                            pass
                    elif posX and posY.isdigit():
                        gift.client.room.sendAll([8, 3], struct.pack("!hhih", int(posX), int(posY), 0, 0))
                except:
                    pass
            gift.isCommand = True

        elif command == "meep":
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.client.sendPacket([8, 39], "\x01")
            gift.isCommand = True

        elif command.startswith("meep "):
            event = command.split(" ")[1]
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                if event == "me":
                    gift.client.sendPacket([8, 39], "\x01")
                elif event == "all":
                    for client in gift.client.room.clients.values():
                        client.sendPacket([8, 39], "\x01")
                elif not event in ["me", "all"]:
                    for client in gift.client.room.clients.values():
                        if event == client.playerName:
                            client.sendPacket([8, 39], "\x01")
            gift.isCommand = True

        elif command == "disco":
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                if gift.client.room.discoRoom == False:
                    gift.client.room.discoRoom = True
                    for client in gift.client.room.clients.values():
                        client.reactorDisco()
                elif gift.client.room.discoRoom == True:
                    gift.client.room.discoRoom = False
            gift.isCommand = True

                    
      

        elif command == "ffa":
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.client.isFFA = True
                gift.client.room.bindKeyBoard(gift.client.playerName, 40, False, gift.client.isFFA)
            gift.isCommand = True

        elif command.startswith("ffa "):
            event = command.split(" ")[1]
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                if event == "me":
                    gift.client.isFFA = True
                    gift.client.room.bindKeyBoard(gift.client.playerName, 40, False, gift.client.isFFA)
                elif event == "on":
                    for client in gift.client.room.clients.values():
                        client.isFFA = True
                        client.room.bindKeyBoard(client.playerName, 40, False, client.isFFA)
                elif event == "off":
                    for client in gift.client.room.clients.values():
                        client.isFFA = False
                if not event in ["me", "on", "off"]:
                    for client in gift.client.room.clients.values():
                        if event == client.playerName:
                            client.isFFA = True
                            client.room.bindKeyBoard(client.playerName, 40, False, client.isFFA)
            gift.isCommand = True

        elif command == "shaman":
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.client.sendShamanCode(gift.client.playerCode, 0)
            gift.isCommand = True

        elif command.startswith("shaman "):
            event = command.split(" ")[1]
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                if event == "me":
                    gift.client.sendShamanCode(gift.client.playerCode, 0)
                elif event == "all":
                    for client in gift.client.room.clients.values():
                        client.sendShamanCode(client.playerCode, 0)
                if not event in ["me", "all"]:
                    for client in gift.client.room.clients.values():
                        if event == client.playerName:
                            client.sendShamanCode(client.playerCode, 0)
            gift.isCommand = True

        elif command in ["np", "map"]:
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.client.room.mapChange()
            gift.isCommand = True

        elif command.startswith("np ") or command.startswith("map "):
            mapCode = command.split(" ")[1]
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                try:
                    gift.client.room.forceNextMap = mapCode
                    gift.client.room.mapChange()
                except:
                    pass
            gift.isCommand = True

        elif command in ["kill", "mort"]:
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if not gift.client.isDead:
                gift.client.isDead = True
                if not gift.client.room.noAutoScore: gift.client.playerScore += 1
                gift.client.sendPlayerDied()
            gift.isCommand = True

        elif command.startswith("kill ") or command.startswith("mort "):
            event = command.split(" ")[1]
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if event == "me":
                if not gift.client.isDead:
                    gift.client.isDead = True
                    if not gift.client.room.noAutoScore: gift.client.playerScore += 1
                    gift.client.sendPlayerDied()
            elif event == "all":
                if gift.client.playerName in gift.client.room.adminsRoom:
                    for client in gift.client.room.clients.values():
                        if not client.isDead:
                            client.isDead = True
                            if not client.room.noAutoScore: client.playerScore += 1
                            client.sendPlayerDied()
            if not event in ["me", "all"]:
                if gift.client.playerName in gift.client.room.adminsRoom:
                    for client in gift.client.room.clients.values():
                        if event == client.playerName:
                            if not client.isDead:
                                client.isDead = True
                                if not client.room.noAutoScore: client.playerScore += 1
                                client.sendPlayerDied()
            gift.isCommand = True

        elif command == "cheese":
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.client.room.sendAll([5, 19], [gift.client.playerCode])
            gift.isCommand = True

        elif command.startswith("cheese "):
            event = command.split(" ")[1]
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                if event == "me":
                    gift.client.room.sendAll([5, 19], [gift.client.playerCode])
                elif event == "all":
                    for client in gift.client.room.clients.values():
                        client.room.sendAll([5, 19], [client.playerCode])
                if not event in ["me", "all"]:
                    for client in gift.client.room.clients.values():
                        if event == client.playerName:
                            client.room.sendAll([5, 19], [client.playerCode])
            gift.isCommand = True

        elif command == "explosion":
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                if gift.canExplosion == False:
                    gift.client.isExplosion = True
                    gift.client.room.bindMouse(gift.client.playerName, gift.client.isExplosion)
                    gift.canExplosion = True
                elif gift.canExplosion == True:
                    gift.client.isExplosion = False
                    gift.client.room.bindMouse(gift.client.playerName, gift.client.isExplosion)
                    gift.canExplosion = False
            gift.isCommand = True

        elif command.startswith("explosion "):
            event = command.split(" ")[1]
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                if event == "me":
                    if gift.canExplosion == False:
                        gift.client.isExplosion = True
                        gift.client.room.bindMouse(gift.client.playerName, gift.client.isExplosion)
                        gift.canExplosion = True
                    elif gift.canExplosion == True:
                        gift.client.isExplosion = False
                        gift.client.room.bindMouse(gift.client.playerName, gift.client.isExplosion)
                        gift.canExplosion = False
                elif event in ["all", "on"]:
                    for client in gift.client.room.clients.values():
                        if client.Utility.canExplosion == False:
                            client.isExplosion = True
                            client.room.bindMouse(client.playerName, client.isExplosion)
                            client.Utility.canExplosion = True
                        elif client.Utility.canExplosion == True:
                            client.isExplosion = False
                            client.room.bindMouse(client.playerName, client.isExplosion)
                            client.Utility.canExplosion = False
                elif event == "off":
                    for client in gift.client.room.clients.values():
                        client.isExplosion = False
                        client.room.bindMouse(client.playerName, client.isExplosion)
                        client.Utility.canExplosion = False
                if not event in ["me", "all", "on", "off"]:
                    for client in gift.client.room.clients.values():
                        if event == client.playerName:
                            if client.Utility.canExplosion == False:
                                client.isExplosion = True
                                client.room.bindMouse(client.playerName, client.isExplosion)
                                client.Utility.canExplosion = True
                            elif client.Utility.canExplosion == True:
                                client.isExplosion = False
                                client.room.bindMouse(client.playerName, client.isExplosion)
                                client.Utility.canExplosion = False
            gift.isCommand = True
            
        elif command == "pw":
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.client.room.roomPassword = ""
                for client in gift.client.room.clients.values():
                    client.Utility.sendMessage("The room's password has been removed.")
            gift.isCommand = True

        elif command.startswith("pw "):
            password = command.split(" ")[1]
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.client.room.roomPassword = str(password)                
                for client in gift.client.room.clients.values():
                    client.Utility.sendMessage(""+str(gift.client.playerName)+" has set a room password.")
                gift.sendMessage("The room's password has been set to: "+str(password)+"")
            gift.isCommand = True

        elif command == "win":
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                gift.playerWin()
                gift.client.isDead = True
            gift.isCommand = True

        elif command.startswith("win "):
            event = command.split(" ")[1]
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                if event == "me":
                    gift.playerWin()
                    gift.client.isDead = True
                elif event == "all":
                    for client in gift.client.room.clients.values():
                        client.Utility.playerWin()
                        client.isDead = True
                if not event in ["me", "all"]:
                    for client in gift.client.room.clients.values():
                        if event == client.playerName:
                            client.Utility.playerWin()
                            client.isDead = True
            gift.isCommand = True

        elif command == "fireworks":
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:            
                for client in gift.client.room.clients.values():
                    client.Utility.isFireworks = True
                    client.fireworksUtility()
            gift.isCommand = True

        elif command.startswith("fireworks "):
            event = command.split(" ")[1]
            gift.consoleChat(2, gift.client.playerName, "!" + command)
            if gift.client.playerName in gift.client.room.adminsRoom:
                if event == "off":
                    for client in gift.client.room.clients.values():
                        client.Utility.isFireworks = False
                elif event != "off":
                    for client in gift.client.room.clients.values():
                        client.Utility.isFireworks = True
                        client.fireworksUtility()
            gift.isCommand = True
