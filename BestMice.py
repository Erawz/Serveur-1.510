#coding: utf-8
#Source by edit:Gifted
import re, os, sys, json, time, random, MySQLdb, ftplib, urllib2, socket, sqlite3, threading, traceback, binascii, ConfigParser, time as _time

# Others
sys.dont_write_bytecode = True
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

# Imports Components
#from PIL import Image, ImageOps
from utils import *
from modules import *
from time import gmtime, strftime

# Library
from datetime import datetime, date
from twisted.internet import reactor, protocol
from datetime import timedelta

class Client:
    def __init__(gift):

        # String
        gift.langue = ""
        gift.packages = ""
        gift.nickColor = "#95d9d6"
        gift.mouseName = ""
        gift.roomName = ""
        gift.emailAddress = ""
        gift.marriage = ""
        gift.shopItems = ""
        gift.tribeName = ""
        gift.nameColor = ""
        gift.chatColor = ""
        gift.tradeName = ""
        gift.playerName = ""
        gift.shamanItems = ""
        gift.lastMessage = ""
        gift.tribeMessage = ""
        gift.tempMouseColor = ""
        gift.silenceMessage = ""
        gift.currentCaptcha = ""
        gift.mouseColor = "78583a"
        gift.shamanColor = "95d9d6"
        gift.modoPwetLangue = "ALL"
        gift.playerLook = "1;0,0,0,0,0,0,0,0,0,0,0"
        gift.shamanLook = "0,0,0,0,0,0,0,0,0,0"
        gift.fur = ""
        gift.botVillage = ""
        gift.lastNpc = ""
        #gift.dailyReward = ""
        
        # Integer
        gift.lastReportID = 0
        gift.playerKarma = 0
        gift.pingTime = 0
        gift.flypoints = 0
        gift.pet = 0
        gift.activeArtefact = 0
        gift.posX = 0
        gift.ClientGotHole = 1
        gift.posY = 0
        gift.velX = 0
        gift.velY = 0
        gift.gender = 0
        gift.playerTime = 0
        gift.loginTime = 0
        gift.petEnd = 0
        gift.viewMessage = 0
        gift.priceDoneVisu = 0
        gift.lastOn = 0
        gift.regDate = 0
        gift.langueID = 0
        gift.useAnime = 0
        gift.playerID = 0
        gift.banHours = 0
        gift.iceCount = 2
        gift.privLevel = 0
        gift.nowTokens = 0
        gift.nowCoins = 0
        gift.shamanExp = 0
        gift.tribeCode = 0
        gift.tribeRank = 0
        gift.tribeChat = 0
        gift.titleStars = 0
        gift.firstCount = 0
        gift.playerCode = 0
        gift.shamanType = 0
        gift.tribeHouse = 0
        gift.tribeJoined = 0
        gift.silenceType = 0
        gift.playerScore = 0
        gift.titleNumber = 0
        gift.cheeseCount = 0
        gift.shopFraises = 0
        gift.shamanSaves = 0
        gift.shamanLevel = 1
        gift.lastGameMode = 0
        gift.bubblesCount = 0
        gift.currentPlace = 0
        gift.shamanCheeses = 0
        gift.hardModeSaves = 0
        gift.bootcampCount = 0
        gift.shopCheeses = 100
        gift.shamanExpNext = 32
        gift.ambulanceCount = 0
        gift.defilantePoints = 0
        gift.divineModeSaves = 0
        gift.lastDivorceTimer = 0
        gift.TimeGiro = 0
        gift.equipedShamanBadge = 0
        gift.playerStartTimeMillis = 0
        gift.racingRounds = 0
        gift.fastracingRounds = 0
        gift.bootcampRounds = 0
        gift.survivorDeath = 0
        gift.countTime = 1
        gift.countP = 0
        gift.cannonX = 2
        gift.cannonY = 8
        gift.cXpos = 189
        gift.cYpos = 133
        gift.cnCustom = 0
        gift.page = 1
        gift.lastPacketID = random.randint(0, 99)
        gift.authKey = random.randint(0, 2147483647)
        gift.TFMUtils = Utils
        gift.tribulleID = 0
        gift.artefactID = 0
        gift.drawingColor = 0

        # Bool
        gift.isLuaAdmin = False
        gift.isAfk = False
        gift.isDead = False
        gift.isMute = False
        gift.isCafe = False
        gift.isGuest = False
        gift.isVoted = False
        gift.isTrade = False
        gift.useTotem = False
        gift.openStaffChat = False
        gift.isHidden = False
        gift.isClosed = False
        gift.isShaman = False
        gift.hasEnter = False
        gift.isSkill = False
        gift.isSuspect = False
        gift.isVampire = False
        gift.isLuaAdmin = False
        gift.hasCheese = False
        gift.hasBolo = False
        gift.hasBolo2 = False
        gift.giftGet = False
        gift.isJumping = False
        gift.resetTotem = False
        gift.isModoPwet = False
        gift.isModoPwetNotifications = False
        gift.canRespawn = False
        gift.enabledLua = False
        gift.isNewPlayer = False
        gift.isEnterRoom = False
        gift.tradeConfirm = False
        gift.canUseConsumable = True
        gift.canSkipMusic = False
        gift.isReloadCafe = False
        gift.isMovingLeft = False
        gift.isMovingRight = False
        gift.isOpportunist = False
        gift.qualifiedVoted = False
        gift.desintegration = False
        gift.canShamanRespawn = False
        gift.validatingVersion = False
        gift.canRedistributeSkills = False
        gift.libCn = False
        gift.canCN = False
        gift.isFly = False
        gift.isSpeed = False
        gift.isFFA = False
        gift.canSpawnCN = True
        gift.isTeleport = False
        gift.isExplosion = False
        gift.chatdisabled = False
        gift.canKiss = True
        gift.openingFriendList = False
        gift.isTribeOpen = False
        gift.hasArtefact = False

        gift.showButtons = True

        #Degiskenler
        gift.isBlockAttack = True

        # Others
        gift.Cursor = Cursor
        gift.CMDTime = time.time()
        gift.CAPTime = time.time()
        gift.CTBTime = time.time()

        # Nonetype
        gift.room = None
        gift.awakeTimer = None
        gift.skipMusicTimer = None
        gift.resSkillsTimer = None

        # List
        gift.totem = [0, ""]
        gift.PInfo = [0, 0, 400]
        gift.tempTotem = [0, ""]
        gift.racingStats = [0] * 4
        gift.survivorStats = [0] * 4

        gift.chats = []
        gift.invitedTribeHouses = []
        gift.voteBan = []
        gift.clothes = []
        gift.titleList = []
        gift.friendsList = []
        gift.tribeInvite = []
        gift.shamanBadges = []
        gift.ignoredsList = []
        gift.mulodromePos = []
        gift.shopTitleList = []
        gift.marriageInvite = []
        gift.firstTitleList = []
        gift.cheeseTitleList = []
        gift.shamanTitleList = []
        gift.specialTitleList = []
        gift.bootcampTitleList = []
        gift.hardModeTitleList = []
        gift.equipedConsumables = []
        gift.ignoredTribeInvites = []
        gift.divineModeTitleList = []
        gift.ignoredMarriageInvites = []
        gift.custom = []
        gift.dailyQuest = [0, 0, 0, 0]
        gift.deathStats = []
        gift.visuDone = []

        # Dict
        gift.shopBadges = {}
        gift.tribeRanks = ""
        gift.playerSkills = {}
        gift.tradeConsumables = {}
        gift.playerConsumables = {}
        gift.itensBots = {"Papaille": [(4, 800, 50, 4, 2253, 50), (4, 800, 50, 4, 2254, 50), (4, 800, 50, 4, 2257, 50), (4, 800, 50, 4, 2260, 50), (4, 800, 50, 4, 2261, 50)], "Santa Claus": [(1, 34, 1, 4, 2254, 100), (1, 174, 1, 4, 2254, 100), (4, 6, 50, 4, 2253, 50), (3, 312, 1, 4, 2253, 50)], "Easter Chappie": [(1, 65, 1, 4, 2254, 100), (1, 64, 1, 4, 2254, 100), (1, 170, 1, 4, 2254, 100), (4, 6, 50, 4, 2254, 100), (3, 426, 1, 4, 2254, 100)], "Buffy": [(1, 147, 1, 4, 2254, 200), (2, 17, 1, 4, 2254, 150), (2, 18, 1, 4, 2254, 150), (2, 19, 1, 4, 2254, 150), (3, 398, 1, 4, 2254, 150), (3, 392, 1, 4, 2254, 50)], "Indiana Mouse": [(3, 255, 1, 4, 2257, 50), (3, 394, 1, 4, 2257, 50), (3, 395, 1, 4, 2257, 50), (3, 320, 1, 4, 2257, 50), (3, 393, 1, 4, 2257, 50), (3, 402, 1, 4, 2257, 50), (3, 397, 1, 4, 2257, 50), (3, 341, 1, 4, 2257, 50), (3, 335, 1, 4, 2257, 25), (3, 403, 1, 4, 2257, 50), (1, 6, 1, 4, 2257, 50), (1, 17, 1, 4, 2257, 50)], "Elise": [(4, 31, 2, 4, 2261, 5), (4, 2256, 2, 4, 2261, 5), (4, 2232, 2, 4, 2253, 1), (4, 21, 5, 4, 2253, 1), (4, 33, 2, 4, 2260, 1), (4, 33, 2, 4, 2254, 1)], "Oracle": [(1, 145, 1, 4, 2253, 200), (2, 16, 1, 4, 2253, 150), (2, 21, 1, 4, 2253, 150), (2, 24, 1, 4, 2253, 150), (2, 20, 1, 4, 2253, 150), (3, 390, 1, 4, 2253, 50), (3, 391, 1, 4, 2253, 200), (3, 399, 1, 4, 2253, 150)], "Prof": [(4, 800, 20, 4, 2257, 10), (4, 19, 2, 4, 2257, 5), (4, 2258, 2, 4, 2257, 4), (4, 2262, 5, 4, 2257, 2), (4, 2259, 10, 4, 2257, 1), (4, 20, 1, 4, 2257, 2)], "Cassidy": [(1, 154, 1, 4, 2261, 200), (2, 23, 1, 4, 2261, 150), (3, 400, 1, 4, 2261, 100)], "Von Drekkemouse": [(2, 22, 1, 4, 2260, 150), (1, 153, 1, 4, 2260, 200), (3, 401, 1, 4, 2260, 100)], "Tod": [(4, 2259, 10, 4, 2257, 1), (4, 2258, 10, 4, 2254, 230), (3, 401, 1, 4, 2260, 100)], "Fishing2017": [(1, 184, 1, 4, 2257, 200), (2, 24, 1, 4, 2257, 150), (2, 29, 1, 4, 2257, 150), (3, 422, 1, 4, 2257, 200)]}
        gift.aventureCounts = {}
        gift.aventurePoints = {}
        gift.visusRemove = []


    def dataReceived(gift, packet):
        if packet.startswith("<policy-file-request/>"):
            gift.transport.write("<cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"*\"/></cross-domain-policy>")
            gift.transport.loseConnection()
        else:
            gift.packages += packet
            while gift.packages.strip(chr(0)):
                if len(gift.packages) >= 5:
                    sizeBytes, package, length = 0, "", 0
                    p = ByteArray(gift.packages)
                    sizeBytes = p.readByte()
                    if sizeBytes == 1:
                        length = p.readUnsignedByte()
                    elif sizeBytes == 2:
                        length = p.readUnsignedShort()
                    elif sizeBytes == 3:
                        length = ((p.readUnsignedByte() & 0xFF) << 16) | ((p.readUnsignedByte() & 0xFF) << 8) | (p.readUnsignedByte() & 0xFF) 
                    else:
                        gift.packages = ""
                    if (length >= 1 and p.getLength() >= 3):
                        length += 1
                        if length == p.getLength():
                            package = p.toByteArray()
                            gift.packages = ""
                        elif length > p.getLength():
                            break
                        else:
                            package = p.toByteArray()[:length]
                            gift.packages = p.toByteArray()[length:]
                    else:
                        gift.packages = ""
                    if package:
                        if len(package) >= 3:
                            gift.parseString(ByteArray(package))
                    p
                else:
                    gift.packages = ""

    def getText(gift, object, *params):
        keys = object.split(".")
        json = gift.server.menu["texts"][gift.langue]
        i = 0
        while i < len(keys):
            key = keys[i]
            if i == len(keys) - 1:
                text = json[key]
                count = 0
                while count < len(params):
                    text = text.replace("%" + str(count + 1), str(params[count]))
                    count += 1
                return text
            else: json = json[key]
            i += 1
        return ""
        
    def close(gift):
        i = 10002
        while i <= 10500:
            gift.room.removeTextArea(i, gift.playerName)
            i += 1

    def sendAddPopupText(gift, id, x, y, l, a, fur1, fur2, opcit, Message):
        bg = int(fur1, 16)
        bd = int(fur2, 16)
        data = struct.pack("!i", id)
        data = data + struct.pack("!h", len(Message))
        data = data + Message + struct.pack("!hhhhiibb", int(x), int(y), int(l), int(a), int(bg), int(bd), int(opcit), 0)
        gift.sendPacket([29, 20], data)

    
    def makeConnection(gift, transport):
        gift.transport = transport
        gift.server = gift.factory
        gift.ipAddress = gift.transport.getPeer().host
        gift.modoPwet = ModoPwet(gift, gift.server)
        gift.cafe = Cafe(gift, gift.server)
        gift.tribulle = Tribulle(gift, gift.server)
        gift.parseShop = ParseShop(gift, gift.server)
        gift.parseSkill = ParseSkill(gift, gift.server)
        gift.parsePackets = ParsePackets(gift, gift.server)
        gift.parseCommands = ParseCommands(gift, gift.server)
        gift.parseCodeCmd = ParseCodeCmd(gift, gift.server)
        gift.fullMenu = fullMenu(gift, gift.server)
        gift.ranking = ranking(gift, gift.server)
        gift.email = email(gift, gift.server)
        gift.radios = radios(gift, gift.server)
        gift.DailyQuest = DailyQuest(gift, gift.server)
        gift.Utility = Utility(gift, gift.server)
        #gift.UnoTFM = UnoTFM(gift, gift.server) // en attente
        gift.AntiCheat = AntiCheat(gift, gift.server)
        #gift.tagGenerator = Generator(gift, gift.server)
        if gift.server.connectedCounts.has_key(gift.ipAddress):
            gift.server.connectedCounts[gift.ipAddress] += 1
        else:
            gift.server.connectedCounts[gift.ipAddress] = 1
        if gift.server.connectedCounts[gift.ipAddress] >= 9999999999999999999999999 or gift.ipAddress in gift.server.IPPermaBanCache or gift.ipAddress in gift.server.IPTempBanCache:
            gift.transport.setTcpKeepAlive(0)
            gift.transport.setTcpNoDelay(True)
            gift.transport.loseConnection()
            gift.server.IPTempBanCache.append(gift.ipAddress)

    def checkReport(gift, array, playerName):
        return playerName in array

    def connectionLost(gift, args):
        gift.isClosed = True
        if gift.server.connectedCounts.has_key(gift.ipAddress):
            count = gift.server.connectedCounts[gift.ipAddress] - 1
            if count <= 0:
                del gift.server.connectedCounts[gift.ipAddress]
            else:
                gift.server.connectedCounts[gift.ipAddress] = count

        if gift.server.players.has_key(gift.playerName):
            del gift.server.players[gift.playerName]
                
            if gift.isTrade:
                gift.cancelTrade(gift.tradeName)

            if gift.server.reports.has_key(gift.playerName):
                if not gift.server.reports[gift.playerName]["durum"] == "banned":
                    gift.server.reports[gift.playerName]["durum"] = "disconnected"
                    gift.modoPwet.updateModoPwet()

            if gift.server.chatMessages.has_key(gift.playerName):
                gift.server.chatMessages[gift.playerName] = {}
                del gift.server.chatMessages[gift.playerName]

            for player in gift.server.players.values():
                if gift.playerName and player.playerName in gift.friendsList and player.friendsList:
                    player.tribulle.sendFriendDisconnected(gift.playerName)

            if gift.tribeCode != 0:
                gift.tribulle.sendTribeMemberDisconnected()

            if not gift.playerName == "":
                if not gift.isGuest:
                    gift.updateDatabase()
                
            if gift.privLevel >= 5:
                gift.server.sendStaffChat(7, gift.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(4).writeUTF("BestMice").writeUTF("%s vient de se déconnecter." % gift.playerName).writeShort(0).writeShort(0).toByteArray())
                gift.server.sendStaffChat(7, gift.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(9).writeUTF("BestMice").writeUTF("%s vient de se déconnecter." % gift.playerName).writeShort(0).writeShort(0).toByteArray())
                gift.server.sendStaffChat(7, gift.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(7).writeUTF("BestMice").writeUTF("%s vient de se déconnecter." % gift.playerName).writeShort(0).writeShort(0).toByteArray())
                gift.server.sendStaffChat(7, gift.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(5).writeUTF("BestMice").writeUTF("%s vient de se déconnecter." % gift.playerName).writeShort(0).writeShort(0).toByteArray())
                gift.server.sendStaffChat(7, gift.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(10).writeUTF("BestMice").writeUTF("%s vient de se déconnecter." % gift.playerName).writeShort(0).writeShort(0).toByteArray())
            reactor.callFromThread(gift.updateDatabase)

        if gift.room != None:
            gift.room.removeClient(gift)

        gift.sendModInfo(0)
        #gift.sendLordInfo(0)

    def sendAllModerationChat(gift, type, message):
        gift.server.sendStaffChat(type, gift.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(1 if type == -1 else type).writeUTF(gift.playerName).writeUTF(message).writeShort(0).writeShort(0).toByteArray())

    def sendPacket(gift, identifiers, packet=""):
        if gift.isClosed:
            return

        p = ByteArray().writeBytes(("".join(map(chr, identifiers)) + chr(packet)) if type(packet) == int else "".join(map(chr, identifiers)) + packet) if type(packet) != list else ByteArray().writeBytes(chr(1) + chr(1)).writeUTF(chr(1).join(map(str, ["".join(map(chr, identifiers))] + packet)))
        gift.transport.write((ByteArray().writeByte(1).writeUnsignedByte(p.getLength()) if p.getLength() <= 0xFF else ByteArray().writeByte(2).writeUnsignedShort(p.getLength()) if p.getLength() <= 0xFFFF else ByteArray().writeByte(3).writeUnsignedByte((p.getLength() >> 16) & 0xFF).writeUnsignedByte((p.getLength() >> 8) & 0xFF).writeUnsignedByte(p.getLength() & 0xFF) if p.getLength() <= 0xFFFFFF else 0).writeBytes(p.toByteArray()).toByteArray())
        gift.transport.setTcpKeepAlive(1)
        gift.transport.setTcpNoDelay(True)

    def parseString(gift, packet):
        if gift.isClosed:
            return

        if packet in ["", " ", "\x00", "\x01"]:
            gift.server.IPTempBanCache.append(gift.ipAddress)
            gift.transport.loseConnection()
            gift.breakLoop()
             
        packetID, C, CC = packet.readByte(), packet.readByte(), packet.readByte()        
        if not gift.validatingVersion:
            if (C == Identifiers.recv.Informations.C and CC == Identifiers.recv.Informations.Correct_Version) and not (gift.isClosed):
                version = packet.readShort()
                ckey = packet.readUTF()

                if not ckey == gift.server.CKEY and version != gift.server.Version:
                    print "[%s] [WARN] Invalid version or CKey (%s, %s)" %(time.strftime("%H:%M:%S"), version, ckey)
                    gift.transport.loseConnection()
                else:
                    gift.validatingVersion = True
                    gift.sendCorrectVersion()
            else:
                gift.transport.loseConnection()
        else:
            try:
                gift.lastPacketID = (gift.lastPacketID + 1) % 100
                gift.lastPacketID = packetID
                gift.parsePackets.parsePacket(packetID, C, CC, packet)
            except:
                with open("./include/SErros.log", "a") as f:
                    traceback.print_exc(file=f)
                    f.write("\n")

    def sendPing(gift):
        gift.pingTime = int(round(time.time() * 1000))
        gift.sendPacket([28, 6], ByteArray().writeByte(0).toByteArray())


    def sendLeaderBoard(gift):
        position = 1
        shown = "<font color ='#BDEE77'><p align='center'><b>Classement FastRacing</font></p>\n"
        shown += "<p align='left'><font size='12'>"
        close = '<a href="event:closed"><font color="#DFB57C"><font size="12">CLOSED</font></a> '
        gift.Cursor.execute("select Username, recCount from users where PrivLevel < 200 ORDER By recCount DESC LIMIT 100")
        for rrf in gift.Cursor.fetchall():
            playerName = str(rrf[0])
            recCount = rrf[1]
            shown += "<p align='center'><font color='#C1EBA8'>"+str(position)+"</font> <font color='#C1EBA8'>-</font> <font color='#C7A8EB'>"+str(playerName)+"</font> <font color='#C1EBA8'>-</font> <font color='#E9A46D'>"+str(recCount)+"</font></p>"
            shown += "<br />"
            position += 1

        #gift.sendMBox(close, 380, 350, 55, 22, "100%", "171C1B", "8F2519", 8249)
        #gift.sendAddPopupText(7999, 0, 25, 799, 309, '171C1B', '8F2519', 100, shown + "</font></p>")
        gift.sendLogMessage(shown + "</font></p>")

    def sendDeathBoard(gift):
        position = 1
        shown = "<V><p align='center'><FC>Classement DeathMatch</font></p>\n"
        shown += "<p align='center'><font size='12'>"
        gift.Cursor.execute("select Username, deathCount from users where PrivLevel < 200 ORDER By deathCount DESC LIMIT 100")
        for rrf in gift.Cursor.fetchall():
            playerName = str(rrf[0])
            deathCount = rrf[1]
            shown += "<font color='#E96D84'>"+str(position)+"</font> <font color='#3C5064'>-</font> <font color='#B7E96D'>"+str(playerName)+"</font> <font color='#3C5064'>-</font> <font color='#6DB5E9'>"+str(deathCount)+"</font>"
            shown += "<br />"
            position += 1

        gift.sendLogMessage(shown + "</font></p>")

    def sendAvatarIMG(gift, url):
        try:
            gift.sendMessage("<BV>Chargement de votre avatar ... Ce processus peut prendre quelques minutes.")
            if len(str(gift.playerID)) == 4:
                playerID = str(gift.playerID)[:3]
            elif len(str(gift.playerID)) == 5:
                playerID = str(gift.playerID)[1:]
            elif len(str(gift.playerID)) == 6:
                playerID = str(gift.playerID)[3:]
            elif len(str(gift.playerID)) == 7:
                playerID = str(gift.playerID)[4:]
            elif len(str(gift.playerID)) == 8:
                playerID = str(gift.playerID)[6:]
            elif len(str(gift.playerID)) == 9:
                playerID = str(gift.playerID)[7:]
            elif len(str(gift.playerID)) == 10:
                playerID = str(gift.playerID)[9:]

            img = urllib2.urlopen(url).read()
            with file('include/avatars/'+str(gift.playerID)+'.jpg', 'wb') as code:
                code.write(img)
                code.close()
                
            img = Image.open('include/avatars/'+str(gift.playerID)+'.jpg')
            width, height = img.size
            width = int(96 * 1.0)
            height = int(96 * 1.0)
            img_red = img.resize((width, height), Image.ANTIALIAS)
            border = ImageOps.expand(img_red, border=2, fill="black")
            border.save('include/avatars/'+str(gift.playerID)+'.jpg')
            filename = 'include/avatars/'+str(gift.playerID)+'.jpg'
            fh = open(filename, 'rb')
            session = ftplib.FTP("ftp://lin5.yoncu.com", "Ja*s13sczx*", "ceomicec*")
            dir = "/tmp"
            session.cwd(dir)
            # if not str(playerID) in session.nlst():
                # session.mkd(str(playerID))
                # session.cwd(str(playerID))
            session.storbinary('STOR '+dir+'/'+str(playerID)+'.jpg', fh)
            fh.close()
            session.quit()

            gift.sendMessage("<BV>Votre avatar a été modifié avec succès.")
        except Exception as error:
            gift.sendMessage("<BV>Votre avatar a bien été changé.")
            #player.sendMessage("<R>Erro ao completa o upload do avatar")
            gift.server.sendStaffMessage(7, "<R>Erreur d'avatar: " + str(error)) 

    def sendAvatarIMGS(gift, url):
        try:
            gift.sendMessage("<BV>Chargement de votre avatar ... Ce processus peut prendre quelques minutes.")
            if len(str(gift.playerID)) == 4:
                playerID = str(gift.playerID)[:3]
            elif len(str(gift.playerID)) == 5:
                playerID = str(gift.playerID)[1:]
            elif len(str(gift.playerID)) == 6:
                playerID = str(gift.playerID)[3:]
            elif len(str(gift.playerID)) == 7:
                playerID = str(gift.playerID)[4:]
            elif len(str(gift.playerID)) == 8:
                playerID = str(gift.playerID)[6:]
            elif len(str(gift.playerID)) == 9:
                playerID = str(gift.playerID)[7:]
            elif len(str(gift.playerID)) == 10:
                playerID = str(gift.playerID)[9:]

            img = urllib2.urlopen(url).read()
            with file('include/avatars/'+str(gift.playerID)+'.jpg', 'wb') as code:
                code.write(img)
                code.close()
                
            img = Image.open('include/avatars/'+str(gift.playerID)+'.jpg')
            width, height = img.size
            width = int(96 * 1.0)
            height = int(96 * 1.0)
            img_red = img.resize((width, height), Image.ANTIALIAS)
            border = ImageOps.expand(img_red, border=2, fill="black")
            border.save('include/avatars/'+str(gift.playerID)+'.jpg')
            dbimg = open('include/avatars/'+str(gift.playerID)+'.jpg', 'rb')
            session = ftplib.FTP("ftp://lin5.yoncu.com/", "ceomicec", "Ja*s13sczx*")
            try:
                session.cwd("/public_html/avatars/" + str(playerID))
            except Exception as e:
                session.cwd("/public_html/avatars/")
                if not str(playerID) in session.nlst():
                    session.mkd(str(playerID))
                    session.cwd(str(playerID))
            session.storbinary('STOR /public_html/avatars/'+str(playerID)+'/'+str(gift.playerID)+'.jpg', dbimg)
            session.quit()

            img = Image.open('include/avatars/'+str(gift.playerID)+'.jpg')
            width, height = img.size
            width = int(50 * 1.0)
            height = int(50 * 1.0)
            img_red = img.resize((width, height), Image.ANTIALIAS)
            img_red.convert('RGB').save('include/avatars/'+str(gift.playerID)+'_50.jpg')
            dbimg = open('include/avatars/'+str(gift.playerID)+'_50.jpg', 'rb')
            session = ftplib.FTP("ftp://lin5.yoncu.com", "ceomicec", "Ja*s13sczx*")
            try:
                session.cwd("/public_html/avatars/" + str(playerID))
            except Exception as e:
                session.cwd("/public_html/avatars/")
                if not str(playerID) in session.nlst():
                    session.mkd(str(playerID))
                    session.cwd(str(playerID))
            session.storbinary('STOR /public_html/avatars/'+str(playerID)+'/'+str(gift.playerID)+'_50.jpg', dbimg)
            session.quit()

            gift.sendMessage("<V>Votre avatar a été traité avec succès.")
            gift.sendMessage("<J>Il peut s'avérer nécessaire de réécrire et d'effacer le cache du navigateur pour que l'avatar fonctionne normalement.")
        except Exception as error:
            gift.sendMessage("<R>Erreur lors du téléchargement de l'avatar..")
            c = open("./include/SErrors.log", "a")
            c.write("\n" + "=" * 60 + "\n- Player: %s\n- Error: %s\n" %(gift.playerName, error))
            traceback.print_exc(file=c)
            c.close()
            print(str(error))



    def blockAttack(gift):
        reactor.callLater(1.5, gift.sendBlockAttack)
        
    def sendBlockAttack(gift):
        gift.isBlockAttack = True

    def loginPlayer(gift, playerName, password, startRoom):
        #if not "#" in playerName and not "@" in playerName:
           # playerName += "#0000"
        playerName = "Souris" if playerName == "" else playerName
        if password == "":
            playerName = gift.server.checkAlreadyExistingGuest("*" + (playerName[0].isdigit() or str(playerName) > 12 or str(playerName) < 3 or "Souris" if "+" in playerName else playerName))
            startRoom = "\x03[Tutorial] %s" %(playerName)
            gift.isGuest = False
            
##        playerName = "" if playerName == "" else playerName
##        if password == "":
##            playerName = gift.server.checkConnectedAccount("#" + (playerName[0].isdigit() or len(playerName) > 12 or len(playerName) < 3 or "0000" if "+" in playerName else playerName))

        if not gift.isGuest and playerName in gift.server.userPermaBanCache:
            gift.sendPacket(Identifiers.old.send.Player_Ban_Login, [gift.server.getPermBanInfo(playerName)])
            gift.transport.loseConnection()
            return

        if not gift.isGuest:
            banInfo = gift.server.getTempBanInfo(playerName)
            timeCalc = Utils.getHoursDiff(banInfo[1])
            if timeCalc <= 0:
                gift.server.removeTempBan(playerName)
            else:
                gift.sendPacket(Identifiers.old.send.Player_Ban_Login, [timeCalc, banInfo[0]])
                gift.transport.loseConnection()
                return

        if gift.server.checkConnectedAccount(playerName):
            gift.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(1).writeUTF("").writeUTF("").toByteArray())
        else:
            letters, gifts, messages = "", "", ""
            if not gift.isGuest and not playerName == "":
                Cursor.execute("select * from Users where Email = %s and Password = %s", [playerName, password])
                players = []
                for rs in Cursor.fetchall():
                    players.append(rs[0])
                if len(players) > 1:
                    i = 0
                    p = ByteArray()
                    while i != len(players):
                        p.writeBytes(players[i]).writeShort(-15708)
                        i += 1
                    gift.sendPacket([26, 12], ByteArray().writeByte(11).writeShort(len(p.toByteArray())).writeBytes(p.toByteArray()).writeShort(0).toByteArray())
                else:
                    gift.Cursor.execute("select * from Users where "+("Email" if "@" in playerName else "Username")+" = %s and Password = %s", [playerName, password])
                    rs = gift.Cursor.fetchone()
                    if rs:
                        playerName = rs[0]
                        gift.playerID = rs[2]
                        gift.privLevel = rs[3]
                        gift.titleNumber = rs[4]
                        gift.firstCount = rs[5]
                        gift.cheeseCount = rs[6]
                        gift.shamanCheeses = rs[7]
                        gift.shopCheeses = rs[8]
                        gift.shopFraises = rs[9]
                        gift.shamanSaves = rs[10]
                        gift.hardModeSaves = rs[11]
                        gift.divineModeSaves = rs[12]
                        gift.bootcampCount = rs[13]
                        gift.shamanType = rs[14]
                        gift.shopItems = rs[15]
                        gift.shamanItems = rs[16]
                        gift.clothes = map(str, filter(None, rs[17].split("|")))
                        gift.playerLook = rs[18]
                        gift.shamanLook = rs[19]
                        gift.mouseColor = rs[20]
                        gift.shamanColor = rs[21]
                        gift.regDate = rs[22]
                        gift.shopBadges = eval(rs[23])
                        gift.firstTitleList = map(float, filter(None, rs[25].split(",")))
                        gift.shamanTitleList = map(float, filter(None, rs[26].split(",")))
                        gift.shopTitleList = map(float, filter(None, rs[27].split(",")))
                        gift.bootcampTitleList = map(float, filter(None, rs[28].split(",")))
                        gift.hardModeTitleList = map(float, filter(None, rs[29].split(",")))
                        gift.divineModeTitleList = map(float, filter(None, rs[30].split(",")))
                        gift.specialTitleList = map(float, filter(None, rs[31].split(",")))
                        gift.banHours = rs[32]
                        gift.shamanLevel = rs[33]
                        gift.shamanExp = rs[34]
                        gift.shamanExpNext = rs[35]

                        for skill in map(str, filter(None, rs[36].split(";"))):
                            values = skill.split(":")
                            gift.playerSkills[int(values[0])] = int(values[1])

                        gift.lastOn = rs[37]
                        gift.friendsList = rs[38].split(",")
                        gift.ignoredsList = rs[39].split(",")
                        gift.gender = rs[40]
                        gift.lastDivorceTimer = rs[41]
                        gift.marriage = rs[42]
                        gift.tribeCode = rs[43]
                        gift.tribeRank = rs[44]
                        gift.tribeJoined = rs[45]
                        gifts = rs[46]
                        message = rs[47]
                        gift.visuDone = rs[59].split("|")
                        gift.custom = map(str, filter(None, rs[60].split(",")))
                        gift.survivorStats = map(int, rs[48].split(","))
                        gift.racingStats = map(int, rs[49].split(","))
                        
                        for consumable in map(str, filter(None, rs[50].split(";"))):
                            values = consumable.split(":")
                            gift.playerConsumables[int(values[0])] = int(values[1])

                        gift.equipedConsumables = []
                        gift.pet = rs[52]
                        gift.petEnd = 0 if gift.pet == 0 else Utils.getTime() + rs[53]
                        gift.shamanBadges = map(int, filter(None, rs[54].split(",")))
                        gift.equipedShamanBadge = rs[55]
                        gift.totem = [rs[57], rs[58].replace("%"[0], chr(1))]
                        gift.nowCoins = rs[61]
                        gift.nowTokens = rs[62]
                        gift.deathStats = map(int, rs[63].split(","))
                        vipTime = rs[64]
                        gift.langueStaff = rs[65]
                        gift.votemayor, gift.candidatar, gift.isMayor, gift.isPresidente, gift.votepresidente, gift.addpresidente=map(int, rs[66].split("#"))
                        for counts in map(str, filter(None, rs[69].split(";"))):
                            values = counts.split(":")
                            f = []
                            aux = 0
                            for i in xrange(len(values[1])):
                                try:
                                    aux = aux * 10 + int(values[1][i])
                                except:
                                    if aux > 0:
                                        f.append(aux)
                                    aux = 0
                                    pass
                            gift.aventureCounts[int(values[0])] = int(f[0]), int(f[1])
                        #gift.aventureCounts = eval(rs["AventureCounts"])
                        for points in map(str, filter(None, rs[70].split(";"))):
                            values = points.split(":")
                            gift.aventurePoints[int(values[0])] = int(values[1])
                        gift.aventureSaves = rs[71]
                        gift.emailAddress = rs[82]
                        #gift.recList = eval(rs[83])
                        gift.dailyQuest = map(str, filter(None, rs[83].split(","))) if rs[83] != "" else [0, 0, 0, 1]
                        gift.remainingMissions = rs[84]
                        letters = rs[85]
                        gift.playerTime = rs[89]
                        gift.playerKarma = int(rs[90]) if rs[90] != None else 0
                        gift.loginTime = Utils.getTime()
                    else:
                        reactor.callLater(1, lambda: gift.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF("").writeUTF("").toByteArray()))
                        return

            if "@" not in playerName:
                if gift.privLevel == -1:
                    gift.sendPacket(Identifiers.old.send.Player_Ban_Login, ["The account has been permanently removed."])
                    gift.transport.loseConnection()
                    return

                gift.server.lastPlayerCode += 1
                gift.playerName = playerName
                gift.playerCode = gift.server.lastPlayerCode

                Cursor.execute("insert into loginlog (Username, IP, Date, Community) select %s, %s, %s,%s where not exists (select 1 from loginlog where Username = %s and IP = %s and Date = %s and Community = %s)", [playerName, gift.ipAddress, Utils.getTime(), gift.langue, playerName, gift.ipAddress, Utils.getTime(), gift.langue])

                for name in ["cheese", "first", "shaman", "shop", "bootcamp", "hardmode", "divinemode"]:
                    gift.checkAndRebuildTitleList(name)

                gift.sendCompleteTitleList()
                gift.parseShop.checkAndRebuildBadges()
                
                for title in gift.titleList:
                    if str(title).split(".")[0] == str(gift.titleNumber):
                        gift.titleStars = int(str(title).split(".")[1])
                        break

                gift.isMute = playerName in gift.server.userMuteCache
                gift.server.players[gift.playerName] = gift
                gift.sendPlayerIdentification()
                gift.sendLogin()
                gift.parseShop.sendShamanItems()
                gift.sendPacket([60, 4], chr(1))
                if startRoom.startswith("\x03[Tutorial]"):
                    if not gift.isGuest:
                        gift.DailyQuest.loadDailyQuest(True)
                else:
                    gift.DailyQuest.loadDailyQuest(False)
                gift.parseSkill.sendShamanSkills(False)
                gift.parseSkill.sendExp(gift.shamanLevel, gift.shamanExp, gift.shamanExpNext)
                if gift.shamanSaves >= 100:
                    gift.sendShamanType(gift.shamanType, (gift.shamanSaves >= 100 and gift.hardModeSaves >= 100))

                gift.server.checkPromotionsEnd()
                gift.sendTimeStamp()
                gift.sendPromotions()

                if gift.tribeCode != 0:
                    tribeInfo = gift.tribulle.getTribeInfo(gift.tribeCode)
                    gift.tribeName = tribeInfo[0]
                    gift.tribeMessage = tribeInfo[1]
                    gift.tribeHouse = tribeInfo[2]
                    gift.tribeRanks = tribeInfo[3]
                    gift.tribeChat = tribeInfo[4]

                #gift.tribulle.sendTribe(False)
                #gift.tribulle.sendPlayerInfo()
                #gift.tribulle.sendIgnoredsList()
                gift.tribulle.sendFriendsList(None)

                for player in gift.server.players.values():
                    if gift.playerName and player.playerName in gift.friendsList and player.friendsList:
                        player.tribulle.sendFriendConnected(gift.playerName)

   
                if gift.tribeCode != 0:
                    gift.tribulle.sendTribeMemberConnected()

                if gift.privLevel >= 6:
                    gift.server.sendStaffChat(7, gift.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(4).writeUTF("BestMice").writeUTF("%s vient de se connecter." % gift.playerName).writeShort(0).writeShort(0).toByteArray())    
                    gift.server.sendStaffChat(7, gift.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(9).writeUTF("BestMice").writeUTF("%s vient de se connecter." % gift.playerName).writeShort(0).writeShort(0).toByteArray())
                    gift.server.sendStaffChat(7, gift.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(7).writeUTF("BestMice").writeUTF("%s vient de se connecter." % gift.playerName).writeShort(0).writeShort(0).toByteArray())
                    gift.server.sendStaffChat(7, gift.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(5).writeUTF("BestMice").writeUTF("%s vient de se connecter." % gift.playerName).writeShort(0).writeShort(0).toByteArray())
                    gift.server.sendStaffChat(7, gift.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(10).writeUTF("BestMice").writeUTF("%s vient de se connecter." % gift.playerName).writeShort(0).writeShort(0).toByteArray())

                gift.sendInventoryConsumables()
                gift.parseShop.checkGiftsAndMessages(gifts, messages)
                gift.checkLetters(letters)
                gift.resSkillsTimer = reactor.callLater(10, setattr, gift, "canRedistributeSkills", True)
                gift.startBulle(gift.server.checkRoom(startRoom, gift.langue) if not startRoom == "" and not startRoom == "1" else gift.server.recommendRoom(gift.langue))
                gift.langueStaff = gift.langue
                gift.sendModInfo(1)
                gift.sendLordInfo(1)
                gift.sendHelpMessage()
                gift.sendModHelpMessage()
                #gift.sendArbHelpMessage()
                reactor.callLater(1200, gift.sendAutoMessage)

            #while gift.server.checkExistingUser(playerName + "#" + tag):
               ## tag = "".join([str(random.choice(range(9))) for x in range(4)])
               # playerName += "#" + tag
                

##        if gift.langue.lower() in ["tr"]:
##            gift.sendMessage("<V>[MF]</V> <R>/casier [nick]</R> oyuncunun susturulma geçmişine bakar.")
##            gift.sendMessage("<V>[MF]</V> <R>/banlog [nick]</R> oyuncunun ban geçmişine bakar.")
##            gift.sendMessage("<V>[MF]</V> <R>/log [nick]</R> oyuncunun giriş geçmişine bakar.")
##            gift.sendMessage("<V>[MF]</V> <R>/chatlog [nick]</R> oyuncunun sohbet chat geçmişine bakar.")
##            gift.sendMessage("<V>[MF]</V> <R>/ban [nick] [saat] [sebep]</R> oyuncuyu sunucudan uzaklaştırır.")
##            gift.sendMessage("<V>[MF]</V> <R>/mute [nick] [saat] [sebep]</R> oyuncuyu susturur.")
##            gift.sendMessage("<V>[MF]</V> <R>/kick [nick]</R> oyuncuyu sunucudan tekmeler.")
##
##
    def sendModHelp(gift):
        if gift.langue.lower() in ["fr"]:
            gift.sendMessage("<V>[MF]</V> <R>/casier [nick]</R> oyuncunun susturulma geçmişine bakar.")
##            gift.sendMessage("<V>[MF]</V> <R>/banlog [nick]</R> oyuncunun ban geçmişine bakar.")
##            gift.sendMessage("<V>[MF]</V> <R>/log [nick]</R> oyuncunun giriş geçmişine bakar.")
##            gift.sendMessage("<V>[MF]</V> <R>/chatlog [nick]</R> oyuncunun sohbet chat geçmişine bakar.")
            gift.sendMessage("<V>[MF]</V> <R>/ban [pseudo] [heure] [raison]</R> oyuncuyu sunucudan uzaklaştırır.")
            gift.sendMessage("<V>[MF]</V> <R>/mute [pseudo] [heure] [raison]</R> oyuncuyu susturur.")
            gift.sendMessage("<V>[MF]</V> <R>/kick [pseudo]</R> oyuncuyu sunucudan tekmeler.")
            gift.sendMessage("<V>[MF]</V> <R>/music [lien]</R> odada müzik açmanızı sağlar.")
            gift.sendMessage("<V>[MF]</V> <R>/cc [pseudo] [langue]</R> bir ülkeden başka ülkeye yönlendirmek için. Kısaltmalar Kullanın örnek: tr,en.")
            gift.sendMessage("<V>[MF]</V> <R>/startsnow - /stopsnow</R> kar yağdırmaya başlar ve durdurmayı sağlar.")
##       
##
##    def sendArbHelpMessage(gift):
##        if gift.privLevel in [8]:
##            if gift.langue.lower() in ["tr"]:
##                gift.sendMessage("<V>[MF]</V><font color ='#E9AFB9'> Arbitre bilgileri için <R>/arbhelp</R> yazınız.</font>")
##
    def sendModHelpMessage(gift):
        if gift.privLevel in [9]:
            if gift.langue.lower() in ["fr"]:
                gift.sendMessage("<V>[MF]</V><font color ='#E9AFB9'> Pour en savoir plus sur les commandes Modérateur, veuillez taper <R>/modhelp</R>.</font>")
##
    def sendHelp(gift):
        if gift.privLevel >= 1:   
##            if gift.langue.lower() in ["tr"]:
##                    gift.sendMessage("<R>/namecolor</R> isim ve chat renginizi değiştirmek için kullanılır.")
##                    gift.sendMessage("<R>/ranking</R> oyuncu sıralamasını gösterir")
            if gift.langue.lower() in ["en"]:
                    gift.sendMessage("<R>/namecolor</R> pour changer la couleur du nom.")
                    gift.sendMessage("<R>/ranking</R> montre le classement des joueurs.")
##            if gift.langue.lower() in ["br"]:
##                    gift.sendMessage("<R>/namecolor</R> para mudar a cor do nome por favor escreva")
##                    gift.sendMessage("<R>/ranking</R> mostra o ranking do jogador")
##            if gift.g() in ["pl"]:
##                    gift.sendMessage("<R>/namecolor</R> aby zmienić kolor nazwy, napisz.")
##                    gift.sendMessage("<R>/ranking</R> pokazuje ranking graczy.")
##        
    def sendHelpMessage(gift):
##        if gift.langue.lower() in ["br"]:
##            gift.sendMessage("<font color ='#50E27A'>Para aprender sobre o jogo, por favor escreva </font><R>/ajuda")
        if gift.langue.lower() in ["fr"]:
            gift.sendMessage("<font color ='#50E27A'>Pour en savoir plus sur notre Serveur, veuillez taper <R>/aide</R>.</font>")
##        if gift.langue.lower() in ["tr"]:
##            gift.sendMessage("<font color ='#50E27A'>Oyun hakkında bilgi edinmek için lütfen <R>/yardım</R> yazın</font>")
##        if gift.langue.lower() in ["pl"]:
##            gift.sendMessage("<font color ='#50E27A'>Aby dowiedzieć się więcej o grze, wpisz <R>/pomoc</R>.</font>")

    def sendAutoMessage(gift):
        gift.sendMessage('<VP>✓ [%s] Notre Discord - https://discord.gg/9ccpuht' %(gift.langue))
        reactor.callLater(1200, gift.sendAutoMessage)

    def winBadgeEvent(gift, badge):
        if not badge in gift.shopBadges:
            gift.sendAnimZelda(3, badge)
            try: gift.shopBadges[badge] += 1;
            except:gift.shopBadges[badge] = 1
            gift.parseShop.checkAndRebuildBadges()
            gift.parseShop.sendUnlockedBadge(badge)
            
    def EventTitleKazan(gift, title):
        if not title in gift.specialTitleList:
            gift.specialTitleList.append(title + 0.1)
            gift.sendUnlockedTitle(title, 1)
            gift.sendCompleteTitleList()
            gift.sendTitleList()

    def winHediye(gift, test):
        if not test in gift.playerConsumables:
            gift.playerConsumables[2100] += test
        else:
            count = gift.playerConsumables[2100] + test
            gift.playerConsumables[2100] = count
            gift.sendAnimZeldaInventory(4, 2100, test)

   
    def checkAndRebuildTitleList(gift, type):
        titlesLists = [gift.cheeseTitleList, gift.firstTitleList, gift.shamanTitleList, gift.shopTitleList, gift.bootcampTitleList, gift.hardModeTitleList, gift.divineModeTitleList]
        titles = [gift.server.cheeseTitleList, gift.server.firstTitleList, gift.server.shamanTitleList, gift.server.shopTitleList, gift.server.bootcampTitleList, gift.server.hardModeTitleList, gift.server.divineModeTitleList]
        typeID = 0 if type == "cheese" else 1 if type == "first" else 2 if type == "shaman" else 3 if type == "shop" else 4 if type == "bootcamp" else 5 if type == "hardmode" else 6 if type == "divinemode" else 0
        count = gift.cheeseCount if type == "cheese" else gift.firstCount if type == "first" else gift.shamanSaves if type == "shaman" else gift.parseShop.getShopLength() if type == "shop" else gift.bootcampCount if type == "bootcamp" else gift.hardModeSaves if type == "hardmode" else gift.divineModeSaves if type == "divinemode" else 0
        tempCount = count
        rebuild = False
        while tempCount > 0:
            if titles[typeID].has_key(tempCount):
                if not titles[typeID][tempCount] in titlesLists[typeID]:
                    rebuild = True
                    break
            tempCount -= 1

        if rebuild:
            titlesLists[typeID] = []
            x = 0
            while x <= count:
                if titles[typeID].has_key(x):
                    title = titles[typeID][x]                    
                    i = 0
                    while i < len(titlesLists[typeID]):
                        if str(titlesLists[typeID][i]).startswith(str(title).split(".")[0]):
                            del titlesLists[typeID][i]
                        i += 1                        
                    titlesLists[typeID].append(title)
                x += 1
                
        gift.cheeseTitleList = titlesLists[0]
        gift.firstTitleList = titlesLists[1]
        gift.shamanTitleList = titlesLists[2]
        gift.shopTitleList = titlesLists[3]
        gift.bootcampTitleList = titlesLists[4]
        gift.hardModeTitleList = titlesLists[5]
        gift.divineModeTitleList = titlesLists[6]

    def discoColors(gift):
        colors = ["000000", "FF0000", "17B700", "F2FF00", "FFB900", "00C0D9", "F600A8", "850000", "62532B", "EFEAE1", "201E1C"]
        sColor = random.choice(colors)                
        data = struct.pack("!i", gift.playerCode)
        data += struct.pack("!i", int(sColor, 16))
        gift.room.sendAll([29, 4], data)
        gift.discoReady()
        for client in gift.room.clients.values():
            client.sendTitleMessage('<font color="#9327FC">Disco Time !</font>')
            reactor.callLater(4, client.sendTitleMessage, '<font color="#FC3027">Disco Time !</font>')
            reactor.callLater(4, client.sendTitleMessage, '<font color="#F727FC">Disco Time !</font>')
            reactor.callLater(4, client.sendTitleMessage, '<font color="#9FFC27">Disco Time !</font>')
            reactor.callLater(4, client.sendTitleMessage, '<font color="#27F0FC">Disco Time !</font>')
            reactor.callLater(4, client.sendTitleMessage, '<font color="#D3FC27">Disco Time !</font>')

    def sendTitleMessage(gift, message):
        for client in gift.room.clients.values():
            info = struct.pack('!h', len(message)) + message + '\n'
            client.room.sendPacket([29, 25], info)    

    def discoMessage(gift):
        gift.sendMessage("<font color='#E9A144'>Disco time begins to entertaining namecolor.</font>")

    def discoReady(gift):
        reactor.callLater(4, gift.discoColors)
            
    def getConnectedPlayerCount(gift):
        return len(gift.server.players)

    def updateDatabase(gift):
        if not gift.isGuest:
            Cursor.execute("update Users set PrivLevel = %s, TitleNumber = %s, FirstCount = %s, CheeseCount = %s, ShamanCheeses = %s, ShopCheeses = %s, ShopFraises = %s, ShamanSaves = %s, HardModeSaves = %s, DivineModeSaves = %s, BootcampCount = %s, ShamanType = %s, ShopItems = %s, ShamanItems = %s, Clothes = %s, Look = %s, ShamanLook = %s, mouseColor = %s, shamanColor = %s, RegDate = %s, Badges = %s, CheeseTitleList = %s, FirstTitleList = %s, ShamanTitleList = %s, ShopTitleList = %s, BootcampTitleList = %s, HardModeTitleList = %s, DivineModeTitleList = %s, SpecialTitleList = %s, BanHours = %s, ShamanLevel = %s, ShamanExp = %s, ShamanExpNext = %s, Skills = %s, LastOn = %s, FriendsList = %s, IgnoredsList = %s, Gender = %s, LastDivorceTimer = %s, Marriage = %s, TribeCode = %s, TribeRank = %s, TribeJoined = %s, SurvivorStats = %s, RacingStats = %s, Consumables = %s, EquipedConsumables = %s, Pet = %s, PetEnd = %s, ShamanBadges = %s, EquipedShamanBadge = %s, VisuDone = %s, CustomItems = %s, Coins = %s, Tokens = %s, DeathStats = %s, Langue = %s, Mayor = %s, AventureCounts = %s, AventurePoints = %s, SavesAventure = %s, DailyQuest = %s, RemainingMissions = %s, Time = %s, Karma = %s where Username = %s", [gift.privLevel, gift.titleNumber, gift.firstCount, gift.cheeseCount, gift.shamanCheeses, gift.shopCheeses, gift.shopFraises, gift.shamanSaves, gift.hardModeSaves, gift.divineModeSaves, gift.bootcampCount, gift.shamanType, gift.shopItems, gift.shamanItems, "|".join(map(str, gift.clothes)), gift.playerLook, gift.shamanLook, gift.mouseColor, gift.shamanColor, gift.regDate, str(gift.shopBadges), ",".join(map(str, gift.cheeseTitleList)), ",".join(map(str, gift.firstTitleList)), ",".join(map(str, gift.shamanTitleList)), ",".join(map(str, gift.shopTitleList)), ",".join(map(str, gift.bootcampTitleList)), ",".join(map(str, gift.hardModeTitleList)), ",".join(map(str, gift.divineModeTitleList)), ",".join(map(str, gift.specialTitleList)), gift.banHours, gift.shamanLevel, gift.shamanExp, gift.shamanExpNext, ";".join(map(lambda skill: "%s:%s" %(skill[0], skill[1]), gift.playerSkills.items())), gift.tribulle.getTime(), ",".join(map(str, filter(None, gift.friendsList))), ",".join(map(str, filter(None, gift.ignoredsList))), gift.gender, gift.lastDivorceTimer, gift.marriage, gift.tribeCode, gift.tribeRank, gift.tribeJoined, ",".join(map(str, gift.survivorStats)), ",".join(map(str, gift.racingStats)), ";".join(map(lambda consumable: "%s:%s" %(consumable[0], 250 if consumable[1] > 250 else consumable[1]), gift.playerConsumables.items())), ",".join(map(str, gift.equipedConsumables)), gift.pet, abs(Utils.getSecondsDiff(gift.petEnd)), ",".join(map(str, gift.shamanBadges)), gift.equipedShamanBadge, "|".join(map(str, gift.visuDone)), ",".join(map(str, gift.custom)), gift.nowCoins, gift.nowTokens, ",".join(map(str, gift.deathStats)), gift.langueStaff, "#".join([str(gift.votemayor), str(gift.candidatar), str(gift.isMayor), str(gift.isPresidente), str(gift.votepresidente), str(gift.addpresidente)]), ";".join(map(lambda aventure: "%s:%s" %(aventure[0], aventure[1]), gift.aventureCounts.items())), ";".join(map(lambda points: "%s:%s" %(points[0], points[1]), gift.aventurePoints.items())), gift.aventureSaves, ",".join(map(str, gift.dailyQuest)), gift.remainingMissions, (gift.playerTime+Utils.getSecondsDiff(gift.loginTime)), gift.playerKarma, gift.playerName])
   # def updateAllDB(gift, oldName, newName):
##        try: gift.updateAllDBFriends(oldName, newName)
##        except: pass
##        try: gift.updateAllDBTribes(oldName, newName)
##        except: pass
        #gift.Cursor.execute("update Users set Username = %s where Username = %s", [newName, oldName])
        #gift.playerName = newName
       # x = gift.server.players[oldName]
       # del gift.server.players[oldName]
       # gift.server.players[gift.playerName] = x
      #  del x
##
##    def updateAllDBFriends(gift, oldName, newName):
##        gift.Cursor.execute("select Username, FriendsList from Users")
##        rs = gift.Cursor.fetchall()
##        inList = []
##        if not "," in rs[1] and not len(rs[1]) > 0:
##            return
##        elif len(rs[1]) != 0 and not "," in rs[1]:
##            inList.append(rs[1])
##        for rrf in rs:
##            if oldName in rs[1].split(","):
##                inList.append(rs[0])
##        if len(inList) == 0:
##            return
##        for user in inList:
##            gift.Cursor.execute("select FriendsList from Users where Username = %s", [user])
##            xdd = gift.Cursor.fetchone()
##            friendList = xdd[0].split(",") if "," in xdd[0] else xdd[0] if len(xdd[0]) > 0 else None
##            if friendList is None:
##                return
##            friendList[friendList.index(oldName)] = newName
##            gift.Cursor.execute("update Users set FriendsList = %s where Username = %s", [",".join(friendList) if len(friendList) > 1 else friendList[0], user])
##            gift.friendsList = friendList
##
##    def updateAllDBTribes(gift, oldName, newName):
##        gift.Cursor.execute("select Code, Members from Tribe")
##        rs = gift.Cursor.fetchall()
##        inList = []
##        if not "," in rs[1] and not len(rs[1]) > 0:
##            return
##        elif len(rs[1]) != 0 and not "," in rs[1]:
##            inList.append(rs[1])
##        for rrf in rs:
##            if oldName in rs[1].split(","):
##                inList.append(rs[0])
##        if len(inList) == 0:
##            pass
##        for tribeCode in inList:
##            gift.Cursor.execute("select Members from Tribe where Code = %s", [tribeCode])
##            tribeMembers = rs[0].split(",")
##            tribeMembers[tribeMembers.index(oldName)] = newName
##            gift.Cursor.execute("update Tribe set Members = %s where Code = %s", [",".join(tribeMembers), tribeCode])

    def startBulle(gift, roomName):
        gift.sendBulle()
        reactor.callLater(0.4, lambda: gift.enterRoom(roomName))

    def enterRoom(gift, roomName):
        if gift.isTrade:
            gift.cancelTrade(gift.tradeName)

        roomName = roomName.replace("<", "&lt;")
        if not roomName.startswith("*") and not (len(roomName) > 3 and roomName[2] == "-" and gift.privLevel >= 7):
            roomName = "%s-%s" %(gift.langue, roomName)
            
        for rooms in ["\x03[Editeur] ", "\x03[Totem] ", "\x03[Tutorial] "]:
            if roomName.startswith(rooms) and not gift.playerName == roomName.split(" ")[1]:
                roomName = "%s-%s" %(gift.langue, gift.playerName)
                
        if not gift.isGuest:
            nomSalon = ["#utility0%s" % (gift.playerName or gift.tribeName), "#utility00%s" % (gift.playerName or gift.tribeName)]
            if roomName == nomSalon[0] or nomSalon[1]:
                if re.search(gift.playerName, roomName):
                    reactor.callLater(0.1, gift.Utility.moreSettings, "giveAdmin")
                else:
                    if not gift.tribeName == '':
                        if re.search(gift.tribeName, roomName):
                            reactor.callLater(0.1, gift.Utility.moreSettings, "giveAdmin")
        if not gift.isGuest: 					   
           if re.search("#utility", roomName):
               reactor.callLater(0.1, gift.Utility.moreSettings, "join")
               reactor.callLater(1.5, gift.Utility.moreSettings, "removePopups")

        if gift.room != None:
            gift.room.removeClient(gift)

        gift.roomName = roomName
        gift.sendGameType(11 if "music" in roomName else 4, 0)
        gift.sendEnterRoom(roomName)
        gift.server.addClientToRoom(gift, roomName)
        gift.sendPacket(Identifiers.old.send.Anchors, gift.room.anchors)
        gift.sendPacket([29, 1], "")
##        gift.fullMenu.sendMenu()

        for player in gift.server.players.values(): 
            if gift.playerName and player.playerName in gift.friendsList and player.friendsList:
                player.tribulle.sendFriendChangedRoom(gift.playerName, gift.langueID)

        if gift.tribeCode != 0:
            gift.tribulle.sendTribeMemberChangeRoom()

        if gift.room.isMusic and gift.room.isPlayingMusic:
            gift.sendMusicVideo(False)

        if gift.room.isTribeHouse and gift.room.isPlayingMusic:
            gift.sendMusicdeo(False)

##        if not gift.room.isTotemEditor and not gift.room.isEditor and not gift.room.isRacing and not gift.room.isBootcamp and not gift.room.isSurvivor and not gift.room.isVillage and not gift.room.isDefilante:

        if roomName.startswith(gift.langue + "-" + "music") or roomName.startswith(gift.langue + "-" + "*music"):
            gift.canSkipMusic = False
            if gift.skipMusicTimer != None:
                gift.skipMusicTimer.cancel()
            gift.skipMusicTimer = reactor.callLater(15, setattr, gift, "canSkipMusic", True)

        if gift.room.isDeathmatch:
            gift.room.bindKeyBoard(gift.playerName, 3, False, gift.room.isDeathmatch)
            gift.room.bindKeyBoard(gift.playerName, 32, False, gift.room.isDeathmatch)
            gift.room.bindKeyBoard(gift.playerName, 79, False, gift.room.isDeathmatch)
            gift.room.bindKeyBoard(gift.playerName, 80, False, gift.room.isDeathmatch)
            gift.sendMessage("<CH><ROSE>#DeathMatch <CH>Bienvenue dans notre module.", True)
            gift.sendMessage("<V><ROSE>Appuyez sur ↓<V> ou <ROSE>ESPACE <V>pour tirer un canon.", True)
            gift.sendMessage("<V><ROSE>Appuyez sur la touche 'P'<V> pour afficher votre profil, vous pouvez regarder l'inventaire en appuyant sur <ROSE>'O'<V>", True)
            gift.sendMessage("<V><ROSE>#Deathmatch<V> vous avez besoin de <ROSE>3 <V>joueurs pour avoir accès au Module.", True)
            gift.sendMessage("<V><ROSE>#Deathmatch<ROSE> <V>Tapez <ROSE>/ds <V>pour afficher le classement.", True)

        if gift.room.isFFARace:
            gift.room.bindKeyBoard(gift.playerName, 3, False, gift.room.isFFARace)
            gift.room.bindKeyBoard(gift.playerName, 32, False, gift.room.isFFARace)
            gift.canCannon = True
            gift.sendMessage("<N>Bienvenue dans notre module <J>#ffarace")
            gift.sendMessage("<N>Appuyez sur  <R>↓ <N>ou <R>ESPACE <N>pour tirer un canon.")
            gift.sendMessage("<N>Essayez d'être le <R><b>first</b> <N>et le <R><b>survivant</b> <N>!")

        if gift.room.isSpeedRace:
            gift.sendMessage("<ROSE>Bienvenue dans notre module Fast Racing!\n<V>Si vous trouvé un </V><R>bug</R><V> ? Rapporter le </V><J>'Nous'</J><V></V>\n<V>Pour voir vos propres records, tapez <FC>/myrecs\n<V>Pour voir le classement, tapez <FC>/rs", True)
        if gift.room.isBigdefilante:
            gift.sendMessage("<font color='#636363'>[BD]</font> <font color='#9a9a9a'>Bienvenue dans notre module Big Defilante!</font>\n<font color='#9a9a9a'>Pour voir vos propres records tapez</font><font color='#F272A5'><b> /defrecs</b>")
        if gift.room.isMeepRace:
            gift.sendMessage("<font color='#636363'>[MR]</font> <font color='#9a9a9a'>Bienvenue dans notre module Meep Racing!</font>")
    
        if gift.room.isFly:
            gift.room.bindKeyBoard(gift.playerName, 32, False, gift.room.isFly)
            gift.sendLangueMessage("", "<N>Appuyez sur la touche ESPACE pour utiliser les vols..")
            
        if gift.room.isFuncorp:
            gift.sendLangueMessage("", "<FC>$FunCorpActive</FC>")
            
    def resetPlay(gift):
        gift.iceCount = 2
        gift.bubblesCount = 0
        gift.currentPlace = 0
        gift.ambulanceCount = 0
        gift.defilantePoints = 0
        gift.bootcampRounds = 0
        gift.artefactID = 0
        
        gift.isAfk = True
        gift.isDead = False
        gift.useTotem = False
        gift.hasEnter = False
        gift.isShaman = False
        gift.isVampire = False
        gift.hasCheese = False
        gift.isSuspect = False
        gift.hasBolo = False
        gift.hasBolo2 = False
        gift.canRespawn = False
        gift.giftGet = False
        gift.isNewPlayer = False
        gift.isOpportunist = False
        gift.desintegration = False
        gift.canShamanRespawn = False
        gift.canKiss = True
        gift.hasArtefact = False
        gift.room.isFly = False

        gift.a = []
        gift.i = []
        gift.s = []
        
    def sendAccountTime(gift):
        eventTime = 1
        date = datetime.now() + timedelta(hours=int(eventTime))
        timetuple = date.timetuple()
        eventTime_ = int(str(thetime.mktime(timetuple)).split(".")[0])
        gift.Cursor.execute('select IP from Account where IP = %s', [gift.ipAddress])
        rrf = gift.Cursor.fetchone()
        if rrf is None:
           gift.Cursor.execute('insert into Account values (%s, %s)', [gift.ipAddress, eventTime_])
        else:
           gift.Cursor.execute('update Account set Time = %s where IP = %s', [eventTime_, gift.ipAddress])

    def checkTimeAccount(gift):
        #return
#        gift.Cursor.execute('SELECT Time FROM Account WHERE IP = %s', [gift.ipAddress])
        rrf = gift.Cursor.fetchone()
        if rrf is None:
            return True
        else:
            if (int(str(thetime.time()).split(".")[0]) >= int(rrf[0])):
                return True
            else:
                return False

    def startFrogEvent(gift):
        gift.sendPacket([5, 51], "\t\x00,\x07\x00i\x07\xb2")
        gift.sendPacket([5, 51], "\t\x00-\x07\x00\xc3\x07\xb2")
        gift.sendPacket([5, 51], "\t\x00.\x07\x00\xcd\x07\xb2")
        gift.sendPacket([5, 51], "\t\x00/\x08\x011\x07\xb2")
        gift.sendPacket([5, 51], "\t\x000\x08\x01\x8b\x07\xb2")
        gift.sendPacket([5, 51], "\t\x001\x08\x01\x90\x07\xc1")
        gift.sendPacket([5, 51], "\t\x002\x08\x01\x95\x07\xb2")
        gift.sendPacket([5, 51], "\t\x003\x08\x01\xf9\x07\xb2")
        gift.sendPacket([5, 51], "\t\x004\x07\x02S\x07\xb2")
        gift.sendPacket([5, 51], "\t\x005\x07\x02]\x07\xb2")
        gift.sendPacket([5, 51], "\t\x006\x07\x02\xc1\x07\xb2")
        reactor.callLater(13, gift.travarRatos)

    def travarRatos(gift):
        gift.room.sendAll([100, 66], "\x01")

    def enableKey(gift, key, onKeyPress = True, onKeyLeave = True):
        if not gift.isDead:
            gift.sendPacket([29, 2], struct.pack('!hbb', int(key), onKeyPress, onKeyLeave))

    def disableKey(gift, key, onKeyPress = False, onKeyLeave = False):
        gift.sendPacket([29, 2], struct.pack('!hbb', int(key), onKeyPress, onKeyLeave))

##    def firstcounts8(gift):
##        gift.firstCount += 350
##        gift.cheeseCount += 350
##        gift.sendMessage("<font color='#729169'>[Soldier] Everyone in the room win 350 first.")

    def sendSaintConsumables(gift):
        id = 2236
        if not id in gift.playerConsumables:
            gift.playerConsumables[id] = 5
        else:
            count = gift.playerConsumables[id] + 5
            gift.playerConsumables[id] = count
            gift.sendAnimZeldaInventory(4, id, 5)

    def sendSaintBadge(gift):
        gift.sendAnimZelda(3, 132)
        gift.parseShop.sendUnlockedBadge(132)
        try: gift.shopBadges[132] += 1
        except: gift.shopBadges[132] = 1


    def sendSaintMessage(gift):
        gift.sendMessage("<font color='#EA489E'>[Saint Valentine] Happy Valentine's Day ^^</font>")

    def sendSaintTitle(gift):
        gift.specialTitleList.append(250.1)
        gift.sendUnlockedTitle(250, 1)
        gift.sendCompleteTitleList()
        gift.sendTitleList()

    def sendSaintEvent(gift):
        gift.sendSaintMessage()
        reactor.callLater(20, gift.sendSaintTitle)
        reactor.callLater(40, gift.sendSaintBadge)
        reactor.callLater(60, gift.sendSaintConsumables)

    def sendStartSaintEvent(gift):
        gift.room.mapCode == 20410
            
    

    def startPlay(gift):
        gift.playerStartTimeMillis = gift.room.gameStartTimeMillis
        gift.isNewPlayer = gift.isDead
        gift.sendMap(newMapCustom=True) if gift.room.mapCode != -1 else gift.sendMap() if gift.room.isEditor and gift.room.EMapCode != 0 else gift.sendMap(True)

        if gift.room.mapCode == 20001 or gift.room.mapCode == 20002:
            gift.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Fish Man").writeShort(335).writeBoolean(True).writeUTF("87;58,6,0,0,0,0,0,0,0").writeShort(1625).writeShort(356).writeShort(11).writeByte(0).writeShort(0).toByteArray())
            gift.sendNPC(1, 4, "Fish Man", 335, "87;58,6,0,0,0,0,0,0,0", 1625, 356, 11, 0)
            gift.room.isNoShamanMap = True


        shamanCode, shamanCode2 = 0, 0
        if gift.room.isDoubleMap:
            shamans = gift.room.getDoubleShamanCode()
            shamanCode = shamans[0]
            shamanCode2 = shamans[1]
        else:
            shamanCode = gift.room.getShamanCode()

        if gift.playerCode == shamanCode or gift.playerCode == shamanCode2:
            gift.isShaman = True

        if gift.isShaman and not gift.room.noShamanSkills:
            gift.parseSkill.getkills()

        if gift.room.currentShamanName != "" and not gift.room.noShamanSkills:
            gift.parseSkill.getPlayerSkills(gift.room.currentShamanSkills)

        if gift.room.currentSecondShamanName != "" and not gift.room.noShamanSkills:
            gift.parseSkill.getPlayerSkills(gift.room.currentSecondShamanSkills)

        gift.sendPlayerList()
        if gift.room.catchTheCheeseMap and not gift.room.noShamanSkills:
            gift.sendPacket(Identifiers.old.send.Catch_The_Cheese_Map, [shamanCode])
            gift.sendPacket(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(shamanCode).writeBoolean(True).toByteArray())
            if not gift.room.currentMap in [108, 109]:
                gift.sendShamanCode(shamanCode, shamanCode2)
        else:
            gift.sendShamanCode(shamanCode, shamanCode2)

        gift.sendSync(gift.room.getSyncCode())
        gift.sendRoundTime(gift.room.roundTime + (gift.room.gameStartTime - Utils.getTime()) + gift.room.addTime)
        gift.sendMapStartTimer(False) if gift.isDead or gift.room.isTutorial or gift.room.isTotemEditor or gift.room.isBootcamp or gift.room.isDefilante or gift.room.getPlayerCountUnique() < 2 else gift.sendMapStartTimer(True)

        if gift.room.isTotemEditor:
            gift.initTotemEditor()

            
        if gift.room.mapCode == 20410:
            gift.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Mark").writeShort(116).writeBoolean(True).writeUTF("122;174_FFB0AF+FFBCBB+FFC3C2,0,0,66_FFC3C2,0,3_D49F9E,0,9_F6A1A0+F1BDA9+FFD0DA,10_FFC9C8+FFD2D2+FF6461+FFC6C5,0,0").writeShort(600).writeShort(359).writeShort(1).writeByte(11).writeShort(0).toByteArray())
            gift.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Gwen").writeShort(116).writeBoolean(True).writeUTF("108;172,20,0,0,40,0,0,0,0,0,0").writeShort(654).writeShort(359).writeShort(1).writeByte(11).writeShort(0).toByteArray())
            gift.sendSaintEvent()
            

       
        if gift.room.isFlyGame:
            gift.sendPacket([29, 25], struct.pack('!h', len('<font color="#E9E253">#Fly')) + '<font color="#EFC262">#Fly')
            gift.enableKey(32)
            if gift.flypoints == 0:
                gift.flypoints += 99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
       
        if gift.room.isSpeedRace:
            gift.sendPacket([29, 25], struct.pack('!h', len('<font color="#E2E05A">Fastracing')) + '<font color="#E2E05A">Fastracing')

        if gift.useAnime >= 1:
            gift.useAnime = 0

        if gift.room.isMeepRace:
            gift.sendPacket(Identifiers.send.Can_Meep, 1)

        if gift.room.isMulodrome:
            if not gift.playerName in gift.room.redTeam and not gift.playerName in gift.room.blueTeam:
                if not gift.isDead:
                    gift.isDead = True
                    gift.sendPlayerDied()

        if gift.room.isSurvivor and gift.isShaman:
            gift.sendPacket(Identifiers.send.Can_Meep, 1)

        if gift.room.isOldSurvivor and gift.isShaman:
            gift.sendPacket(Identifiers.send.Can_Meep, 0)

        gift.isEvent = True
        gift.room.bindKeyBoard(gift.playerName, 32, False, gift.isEvent)

        gift.isPositioncmd = True
        gift.room.bindKeyBoard(gift.playerName, 78, False, gift.isPositioncmd)
        
        if gift.room.mapCode == 20001 or gift.room.mapCode == 20002:
            gift.sendLangueMessage("", "<font color='#95CAD9'>[Fishing Event] Aller dans les zones <ROSE>d'eau</ROSE> <font color='#95CAD9'>et appuyez sur la touche <ROSE>ESPACE</ROSE>.")

        if gift.room.currentMap in range(200, 211) and not gift.isShaman:
            gift.sendPacket(Identifiers.send.Can_Transformation, 1)

        if gift.room.isVillage:
            reactor.callLater(0.1, gift.sendBotsVillage)

        elif gift.room.isFFARace:
            reactor.callLater(1.3, gift.enableSpawnCN)


    def sendFishingCount(gift):
        gift.sendPlayerEmote(14, "", False, False)
        item = ["30", "1", "5", "21", "22", "23", "24", "25", "28", "32", "33", "407", "35", "2349", "2252", "2240", "2247", "14", "15", "16", "20", "2", "3", "4", "6", "8", "800", "29", "2234", "2246", "2256", "2330", "11", "31", "34", "26"]
        id = random.choice(item)
        if not id in gift.playerConsumables:
            gift.playerConsumables[id] = 1
        else:
            count = gift.playerConsumables[id] + 1
            gift.playerConsumables[id] = count
        gift.sendAnimZeldaInventoryx(4, id, 1)    
        id2 = 2343
        if not id2 in gift.playerConsumables:
            gift.playerConsumables[id2] = 3
        else:
            count = gift.playerConsumables[id2] + 3
            gift.playerConsumables[id2] = count
        gift.sendAnimZeldaInventoryx(4, id2, 3)

    def sendBotsVillage(gift):
        gift.sendPacket([8, 30], "\xff\xff\xff\xff\x00\x06Oracle\x01+\x01\x00*61;0,0,0,0,0,19_3d100f+1fa896+ffe15b,0,0,0\x08\x8b\x01}\x00\x01\x0b\x00\x00")
        gift.sendPacket([8, 30], "\xff\xff\xff\xfe\x00\x08Papaille\x01*\x01\x00\x134;2,0,2,2,0,0,0,0,1\tZ\x00\xd1\x00\x01\x0b\x00\x00")
        gift.sendPacket([8, 30], "\xff\xff\xff\xfd\x00\x05Elise\x01]\x01\x00\x143;10,0,1,0,1,0,0,1,0\t\x19\x00\xd1\x01\x01\x0b\x00\x00")
        gift.sendPacket([8, 30], "\xff\xff\xff\xfc\x00\x05Buffy\x01[\x01\x00\x06$Buffy\x07t\x01\xf3\x00\x01\x0b\x00\x00")
        gift.sendPacket([8, 30], "\xff\xff\xff\xfb\x00\rIndiana Mouse\x01(\x00\x00\x1445;0,0,0,0,0,0,0,0,0\x00\xae\x02\xca\x00\x01\x0b\x00\x00")
        gift.sendPacket([8, 30], "\xff\xff\xff\xfa\x00\x04Prof\x01G\x00\x00\n$Proviseur\x01!\x02\xcb\x00\x01\x0b\x00\x00")
        gift.sendPacket([8, 30], "\xff\xff\xff\xf9\x00\x07Cassidy\x01\x18\x00\x00\x07$Barman\n\xd2\x02%\x00\x01\x0b\x00\x00")
        gift.sendPacket([8, 30], "\xff\xff\xff\xf8\x00\x0fVon Drkkemouse\x01\x1f\x00\x00\n$Halloween\x06\x88\x01z\x00\x01\x0b\x00\x00")
        gift.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Wise Stranger").writeShort(319).writeBoolean(True).writeUTF("106;125_902424+D9D9D9,20,0,0,1,0,0,0,0").writeShort(2145).writeShort(635).writeShort(1).writeByte(11).writeShort(0).toByteArray())
        gift.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Savior").writeShort(354).writeBoolean(True).writeUTF("28;113_CAC5C5+EDE4DB+FFFFFF,9_000000,0,0,0,19_B8B8B8+1FA896+FFF9E1,0,3,0").writeShort(1794).writeShort(751).writeShort(1).writeByte(11).writeShort(0).toByteArray())

    def sendNPC(gift, id, id2, name, title, look, px, py, mode, end):
        gift.sendPacket([8, 30], ByteArray().writeShort(id).writeShort(id2).writeUTF(name).writeShort(title).writeByte(0).writeUTF(look).writeShort(px).writeShort(py).writeShort(mode).writeByte(5).writeShort(end).toByteArray()) 

    def getPlayerData(gift):
        data = ByteArray()
        data.writeUTF(gift.playerName if gift.mouseName == "" else gift.mouseName)
        data.writeInt(gift.playerCode)
        data.writeBoolean(gift.isShaman)
        data.writeBoolean(gift.isDead)
        data.writeShort(gift.playerScore)
        data.writeBoolean(gift.hasCheese)
        data.writeShort(gift.titleNumber)
        data.writeByte(gift.titleStars)
        data.writeByte(gift.gender)
        data.writeUTF("")
        data.writeUTF("1;0,0,0,0,0,0,0,0,0,0,0" if gift.room.isBootcamp else (gift.fur if gift.fur != "" else gift.playerLook))
        data.writeBoolean(False)
        data.writeInt(int(gift.tempMouseColor if not gift.tempMouseColor == "" else gift.mouseColor, 16))
        data.writeInt(int(gift.shamanColor, 16))
        data.writeInt(0)
        try:data.writeInt(int(gift.nickColor.lower() if gift.nickColor != "" else "#95d9d6", 16))
        except:data.writeInt(-1)
        return data.toByteArray()


    def sendShamanCode(gift, shamanCode, shamanCode2):
        gift.sendShaman(shamanCode, shamanCode2, gift.server.getShamanType(shamanCode), gift.server.getShamanType(shamanCode2), gift.server.getShamanLevel(shamanCode), gift.server.getShamanLevel(shamanCode2), gift.server.getShamanBadge(shamanCode), gift.server.getShamanBadge(shamanCode2))

    def sendCorrectVersion(gift):
        gift.sendPacket(Identifiers.send.Correct_Version, ByteArray().writeInt(gift.getConnectedPlayerCount()).writeByte(gift.lastPacketID).writeUTF('en').writeUTF('en').writeInt(gift.authKey).toByteArray())
        gift.sendPacket(Identifiers.send.Banner_Login, ByteArray().writeByte(1).writeByte(gift.server.adventureID).writeByte(1).writeBoolean(False).toByteArray())
        gift.sendPacket(Identifiers.send.Image_Login, ByteArray().writeUTF(gift.server.adventureIMG).toByteArray())
        gift.awakeTimer = reactor.callLater(999999, gift.transport.loseConnection)

##    def sendLogin(gift):
##        if gift.privLevel >= 7:
##            #gift.sendPlayerIdentification()
##            gift.sendPacket([26, 2], ByteArray().writeInt(gift.playerID).writeUTF(gift.playerName).writeInt(60000).writeByte(gift.langueID).writeInt(gift.playerCode).writeBoolean(True).writeByte(5).writeByte(5).writeBoolean(False).writeByte(10).writeByte(-1).writeByte(-1).writeByte(-1).toByteArray())
##        else:
##            #gift.sendPlayerIdentification()
##            gift.sendPacket([26, 2], ByteArray().writeInt(gift.playerID).writeUTF(gift.playerName).writeInt(60000).writeByte(gift.langueID).writeInt(gift.playerCode).writeBoolean(True).writeByte(1).writeByte(3 if gift.privLevel == 3 else 0).writeBoolean(False).toByteArray())
##

##    def sendLogin(gift):
##        if gift.privLevel >= 7:
##            #gift.sendPlayerIdentification()
##            gift.sendPacket([26, 2], ByteArray().writeInt(gift.playerID).writeUTF(gift.playerName).writeInt(60000).writeByte(gift.langueID).writeInt(gift.playerCode).writeBoolean(True).writeByte(5).writeByte(5).writeBoolean(False).writeByte(10).writeByte(-1).writeByte(-1).writeByte(-1).toByteArray())
##        else:
##            #gift.sendPlayerIdentification()
##            gift.sendPacket([26, 2], ByteArray().writeInt(gift.playerID).writeUTF(gift.playerName).writeInt(60000).writeByte(gift.langueID).writeInt(gift.playerCode).writeBoolean(True).writeByte(1).writeByte(3 if gift.privLevel == 3 else 0).writeBoolean(False).toByteArray())


    def sendLogin(gift):
        gift.sendPacket(Identifiers.old.send.Login, [gift.playerName, gift.playerCode, gift.privLevel, 30, 1 if gift.isGuest else 0, 0, 0, 0])
        if gift.isGuest:
            gift.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(1).writeByte(10).toByteArray())
            gift.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(2).writeByte(5).toByteArray())
            gift.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(3).writeByte(15).toByteArray())
            gift.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(4).writeByte(200).toByteArray())

    def sendPlayerIdentification(gift, createAccount = False):
        if gift.isGuest:
            gift.sendPacket(Identifiers.send.Player_Identification, ByteArray().writeInt(gift.playerID).writeUTF(gift.playerName).writeInt(600000).writeByte(gift.langueID).writeInt(gift.playerCode).writeByte(gift.privLevel).writeByte(0).writeByte(0).writeBoolean(False).toByteArray())
        else:
            if createAccount:
                gift.sendPacket(Identifiers.send.Player_Identification, ByteArray().writeInt(gift.playerID).writeUTF(gift.playerName).writeInt(600000).writeByte(gift.langueID).writeInt(gift.playerCode).writeBoolean(True).writeByte(1).writeByte(0).writeBoolean(False).toByteArray())
            else:
                if gift.privLevel >= 5:
                    gift.sendPacket(Identifiers.send.Player_Identification, ByteArray().writeInt(gift.playerID).writeUTF(gift.playerName).writeInt(600000).writeByte(gift.langueID).writeInt(gift.playerCode).writeBoolean(True).writeByte(5).writeByte(5).writeBoolean(False).writeByte(10).writeByte(-1).writeByte(-1).writeByte(-1).toByteArray())

                elif gift.privLevel >= 1 and gift.privLevel <= 6:
                    gift.sendPacket(Identifiers.send.Player_Identification, ByteArray().writeInt(gift.playerID).writeUTF(gift.playerName).writeInt(600000).writeByte(gift.langueID).writeInt(gift.playerCode).writeBoolean(True).writeByte(1).writeByte(3 if gift.privLevel == 3 else 0).writeBoolean(False).toByteArray())
        gift.sendPacket([100, 6], "\x00\x00")
            

    def sendPlayerIdentifications(gift):
        data = ByteArray()
        data.writeInt(gift.playerID)
        data.writeUTF(gift.playerName)
        data.writeInt(gift.playerTime)
        data.writeByte(gift.langueID)
        data.writeInt(gift.playerCode)
        data.writeBoolean(not gift.isGuest)

        permsCount = 0
        perms = ByteArray()
        permsList = [False, False, False, gift.privLevel >= 3, False, gift.privLevel >= 5, False, False, False, False, gift.privLevel == 10, gift.privLevel == 5, False, gift.privLevel == 4, False, False]
        i = 0
        while i < len(permsList):
            if permsList[i]:
                permsCount += 1
                perms.writeByte(i)
            i += 1

        data.writeByte(permsCount)
        data.writeBytes(perms.toByteArray())
        data.writeBoolean(False)
        gift.sendPacket(Identifiers.send.Player_Identification, data.toByteArray())

    def sendTimeStamp(gift):
        gift.sendPacket(Identifiers.send.Time_Stamp, ByteArray().writeInt(Utils.getTime()).toByteArray())

    def enableSpawnCN(gift):
        gift.canSpawnCN = True

    def sendGiveConsumables(gift, id, count):
        if not id in gift.playerConsumables:
          	gift.playerConsumables[id] = count
        else:
           x = gift.playerConsumables[id] + count
           gift.playerConsumables[id] = x
        gift.sendAnimZeldaInventory(4, id, count)

        
    def getCrazzyPacket(gift,type,info): 
        data = ByteArray()
        data.writeByte(type)

        if type == 1:
            data.writeShort(int(info[0]))
            data.writeInt(int(str(info[1]), 16))
            
        if type == 2:
            data.writeInt(int(info[0]))
            data.writeInt(int(info[1]))
            data.writeShort(int(info[2]))
            data.writeShort(int(info[3]))
            data.writeShort(int(info[4]))
            data.writeShort(int(info[5]))
        

        if type == 4:
            data.writeInt(int(info[0]))
            data.writeInt(int(info[1]))
        

        if type == 5:
            data.writeInt(int(info[0]))
            data.writeShort(int(info[1]))
            data.writeByte(int(info[2]))
        

        return data.toByteArray()    

    def fireworksUtility(gift):
        if gift.room.isUtility and gift.Utility.isFireworks == True:
            gift.Utility.newCoordsConj()
            reactor.callLater(0.2, gift.Utility.buildConj)
            reactor.callLater(1, gift.Utility.removeConj)
            reactor.callLater(1.5, gift.fireworksUtility)
    
    def discoUtility(gift):
        if gift.room.isUtility == True:
            colors = ["000000", "FF0000", "17B700", "F2FF00", "FFB900", "00C0D9", "F600A8", "850000", "62532B", "EFEAE1", "201E1C"]
            sColor = random.choice(colors)                
            data = struct.pack("!i", gift.playerCode)
            data += struct.pack("!i", int(sColor, 16))
            gift.room.sendAll([29, 4], data)
            if gift.room.discoRoom == True:
                gift.reactorDisco()

    def reactorDisco(gift):
        if gift.room.isUtility == True:
            if gift.room.discoRoom == True:
                reactor.callLater(0.7, gift.discoUtility)

    def sendPromotions(gift):
        for promotion in [[22, 124, 9], [5, 50, 9], [8, 13,9]]:
            gift.sendPacket(Identifiers.send.Promotion, ByteArray().writeBoolean(False).writeBoolean(True).writeInt(promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)).writeBoolean(True).writeInt(promotion[2]).writeByte(0).toByteArray())

    def sendGameType(gift, gameType, serverType):
        gift.sendPacket(Identifiers.send.Room_Type, gameType)
        gift.sendPacket(Identifiers.send.Room_Server, serverType)

    def sendEnterRoom(gift, roomName):
        found = False
        rooms = roomName[3:]
        count = "".join(i for i in rooms if i.isdigit())
        for room in ["vanilla", "survivor", "racing", "music", "bootcamp", "defilante", "village", "#deathmatch"]:
            if rooms.startswith(room) and not count == "" or rooms.isdigit():
                found = not (int(count) < 1 or int(count) > 1000000000 or rooms == room)
        gift.sendPacket(Identifiers.send.Enter_Room, ByteArray().writeBoolean(found).writeUTF(roomName).toByteArray())

    def sendMap(gift, newMap=False, newMapCustom=False):
        gift.sendPacket(Identifiers.send.New_Map, ByteArray().writeInt(gift.room.currentMap if newMap else gift.room.mapCode if newMapCustom else -1).writeShort(gift.room.getPlayerCount()).writeByte(gift.room.lastRoundCode).writeShort(0).writeUTF("" if newMap else gift.room.mapXML.encode("zlib") if newMapCustom else gift.room.EMapXML.encode("zlib")).writeUTF("" if newMap else gift.room.mapName if newMapCustom else "-").writeByte(0 if newMap else gift.room.mapPerma if newMapCustom else 100).writeBoolean(gift.room.mapInverted if newMapCustom else False).toByteArray())

    def sendPlayerList(gift):
        players = gift.room.getPlayerList()
        data = ByteArray().writeShort(len(players))
        for player in players:
            data.writeBytes(player)
        
        gift.sendPacket([144, 1], data.toByteArray())

    def sendSync(gift, playerCode):
        gift.sendPacket(Identifiers.old.send.Sync, [playerCode, ""] if (gift.room.mapCode != 1 or gift.room.EMapCode != 0) else [playerCode])

    def sendRoundTime(gift, time):
        gift.sendPacket(Identifiers.send.Round_Time, ByteArray().writeShort(0 if time < 0 or time > 32767 else time).toByteArray())

    def sendMapStartTimer(gift, startMap):
        gift.sendPacket(Identifiers.send.Map_Start_Timer, ByteArray().writeBoolean(startMap).toByteArray())

    def sendPlayerDisconnect(gift):
        gift.room.sendAll(Identifiers.old.send.Player_Disconnect, [gift.playerCode])

    def sendChangeMap(gift, time):
       gift.room.sendAll([5, 22], ByteArray().writeShort(time).toByteArray())
       if gift.room.changeMapTimer:
               try:
                       gift.room.changeMapTimer.cancel()
               except:
                       gift.room.changeMapTimer=None
       gift.room.changeMapTimer = reactor.callLater(time, gift.room.mapChange)

    def getPing(gift, ip, user):
        if str(ip) != str(gift.ipAddress):
            userPing = True
        else:            
            userPing = False
            
        ping = os.popen("ping -n 1 %s"%(ip)).readlines()[-1]
        ping = str(ping.split("= ")[-1]).strip().replace('ms', '')
        
        try:
            if userPing:
                gift.sendMessage(str(user) + ", Latency: " + str(ping))
            else:
                gift.sendMessage(str(ping))
        except:
            gift.sendMessage("<ROSE>Could not ping player.")

    def sendPlayerDied(gift):
        gift.room.sendAll(Identifiers.old.send.Player_Died, [gift.playerCode, gift.playerScore])
        gift.hasCheese = False

        if gift.room.getAliveCount() < 1 or gift.room.catchTheCheeseMap or gift.isAfk:
            gift.canShamanRespawn = False

        if ((gift.room.checkIfTooFewRemaining() and not gift.canShamanRespawn) or (gift.room.checkIfShamanIsDead() and not gift.canShamanRespawn) or (gift.room.checkIfDoubleShamansAreDead())):
            gift.room.send20SecRemainingTimer()
         
        if gift.room.isDeathmatch:
            if gift.room.checkIfDeathMouse():
                if gift.room.getPlayerCount() >= 3:
                   gift.sendChangeMap(5)
                for client in gift.room.clients.values():
                     if not client.isDead:
                         gift.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<N>Félicitations <J>%s<N> a gagner le match" %(client.playerName)).toByteArray())
                         client.firstCount += 12
                         gift.Cursor.execute("update users set deathCount = deathCount + 1 where Username = %s", [client.playerName])
                         client.cheeseCount += 12
                         client.sendMessage("<J>gift round won for, one next map waiting.")

        if gift.room.isRacing:
            gift.racingRounds = 0
        if gift.room.isSpeedRace:
            gift.fastracingRounds = 0
        if gift.room.isRacing:
            if gift.room.checkIfDeathMouse():
                gift.sendChangeMap(20)


        if gift.canShamanRespawn:
            gift.isDead = False
            gift.isAfk = False
            gift.hasCheese = False
            gift.hasEnter = False
            gift.canShamanRespawn = False
            gift.playerStartTimeMillis = time.time()
            for player in gift.room.clients.values():
                gift.room.sendAll([144, 2], ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())
                player.sendShamanCode(gift.playerCode, 0)

    def sendShaman(gift, shamanCode, shamanCode2, shamanType, shamanType2, shamanLevel, shamanLevel2, shamanBadge, shamanBadge2):
        gift.sendPacket(Identifiers.send.Shaman_Info, ByteArray().writeInt(shamanCode).writeInt(shamanCode2).writeByte(shamanType).writeByte(shamanType2).writeShort(shamanLevel).writeShort(shamanLevel2).writeShort(shamanBadge).writeShort(shamanBadge2).toByteArray())

    def sendConjurationDestroy(gift, x, y):
        gift.room.sendAll(Identifiers.old.send.Conjuration_Destroy, [x, y])

    def sendGiveCheese(gift, distance=-1):
        if distance != -1 and distance != 1000 and not gift.room.catchTheCheeseMap and gift.room.countStats:
            if distance >= 30:
                gift.isSuspect = True

        gift.room.canChangeMap = False
        if not gift.hasCheese:
            gift.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(gift.playerCode).writeBoolean(True).toByteArray())
            gift.hasCheese = True
            
            gift.room.numGetCheese += 1 
            if gift.room.currentMap in range(108, 114):
                if gift.room.numGetCheese >= 10:
                    gift.room.killShaman()

            if gift.room.isTutorial:
                gift.sendPacket(Identifiers.send.Tutorial, 1)
        gift.room.canChangeMap = True

    def playerWin(gift, holeType, distance=-1):
        if distance != -1 and distance != 1000 and gift.isSuspect and gift.room.countStats:
            if distance >= 30:
                gift.server.sendStaffMessage(7, "[<V>ANTI-HACK</V>][<J>%s</J>][<V>%s</V>] Instant win detected." %(gift.ipAddress, gift.playerName))
                gift.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Instant win detected."])
                gift.transport.loseConnection()
                return

        timeTaken = int((time.time() - (gift.playerStartTimeMillis if gift.room.autoRespawn else gift.room.gameStartTimeMillis)) * 100)
        if timeTaken > 5:
            gift.room.canChangeMap = False
            canGo = gift.room.checkIfShamanCanGoIn() if gift.isShaman else True
            if not canGo:
                gift.sendSaveRemainingMiceMessage()

            if gift.isDead or not gift.hasCheese and not gift.isOpportunist:
                canGo = False

            if gift.room.isTutorial:
                gift.sendPacket(Identifiers.send.Tutorial, 2)
                gift.hasCheese = False
                reactor.callLater(10, lambda: gift.startBulle(gift.server.recommendRoom(gift.langue)))
                gift.sendRoundTime(10)
                return

            if gift.room.isEditor:
                if not gift.room.EMapValidated and gift.room.EMapCode != 0:
                    gift.room.EMapValidated = True
                    gift.sendPacket(Identifiers.old.send.Map_Validated, [""])

            if canGo:
                gift.isDead = True
                gift.hasCheese = False
                gift.hasEnter = True
                gift.room.numCompleted += 1
                place = gift.room.numCompleted
                if gift.room.isDoubleMap:
                    if holeType == 1:
                        gift.room.FSnumCompleted += 1
                    elif holeType == 2:
                        gift.room.SSnumCompleted += 1
                    else:
                        gift.room.FSnumCompleted += 1
                        gift.room.SSnumCompleted += 1

                gift.currentPlace = place

                if place == 1:
                    gift.playerScore += (4 if gift.room.isRacing else 4 if gift.room.isSpeedRace else 16) if not gift.room.noAutoScore else 0
                    if gift.room.getPlayerCountUnique() >= gift.server.needToFirst and gift.room.countStats and not gift.isShaman and not gift.canShamanRespawn:
                        gift.firstCount += 12
                        gift.cheeseCount += 12

                        timeTaken = int((time.time() - (gift.playerStartTimeMillis if gift.room.autoRespawn else gift.room.gameStartTimeMillis)) * 100)
                        if timeTaken > 100:
                            t = timeTaken / 100.0
                        else:
                            t = timeTaken / 10.0
                        if gift.room.isSpeedRace:
                            if int(gift.room.getPlayerCount()) >= int(gift.server.needToFirst):
                                if gift.room.mapCode not in (-1, 31, 41, 42, 54, 55, 59, 60, 62, 89, 92, 99, 114, 801):
                                    try:
                                        CursorMaps.execute('select TopTime from Maps where code = ?', [gift.room.mapCode])
                                        timeDB = CursorMaps.fetchone()
                                        if timeDB[0] == 0 or timeTaken < timeDB[0]:
                                            CursorMaps.execute('update Maps set TopTime = ?, TopTimeNick = ? where code = ?', [timeTaken, gift.playerName, gift.room.mapCode])
                                            gift.Cursor.execute("update users set recCount = recCount + 1 where Username = %s", [gift.playerName])
                                            for client in gift.room.clients.values():
                                                client.sendMessage("<BL>Nouveau record par <J>"+gift.playerName+"</J> <BL>avec un temps de</BL> <BL>(</BL><J>"+str(t)+"</J><BL>s)</BL>")
                                                    #client.sendMessage("<font color='#98D1EB'>[FR]:</font> <font color='#E56CA3'>New record</font> <font color='#98D1EB'>" + gift.playerName + "</font></font><font color='#E56CA3'>(</font><font color='#FFD700'>" + str(t) + "</font><font color='#E56CA3'>s)</font>")

                                    except:
                                        pass
                                    
                        timeTaken = int((time.time() - (gift.playerStartTimeMillis if gift.room.autoRespawn else gift.room.gameStartTimeMillis)) * 100)
                        if timeTaken > 100:
                            t = timeTaken / 100.0
                        else:
                            t = timeTaken / 10.0
                        if gift.room.isBigdefilante:
                            if int(gift.room.getPlayerCount()) >= int(gift.server.needToFirst):
                                if gift.room.mapCode not in (-1, 31, 41, 42, 54, 55, 59, 60, 62, 89, 92, 99, 114, 801):
                                    try:
                                        CursorMaps.execute('select BDTime from Maps where code = ?', [gift.room.mapCode])
                                        timeDB = CursorMaps.fetchone()
                                        if timeDB[0] == 0 or timeTaken < timeDB[0]:
                                            CursorMaps.execute('update Maps set BDTime = ?, BDTimeNick = ? where code = ?', [timeTaken, gift.playerName, gift.room.mapCode])
                                            for client in gift.room.clients.values():
                                                    client.sendMessage("<font color='#98D1EB'>[BD] :</font> <font color='#E56CA3'>Nouveau record</font> <font color='#'>" + gift.playerName + "</font> <font color='#E56CA3'>avec un temps de </font><font color='#E56CA3'>(</font><font color='#FFD700'>" + str(t) + "</font><font color='#E56CA3'>s)</font>")

                                    except:
                                        pass
                        				
                    if gift.room.isSpeedRace:
                        for player in gift.room.clients.values():
                                player.sendMessage("<R>%s</R> est le gagnant" %(gift.playerName))
                                player.sendRoundTime(3)
                                gift.room.changeMapTimers(3)

                    if gift.room.isBigdefilante:
                        for player in gift.room.clients.values():
                            player.sendRoundTime(3)
                            gift.room.changeMapTimers(3)

                elif place == 2:
                    if gift.room.getPlayerCountUnique() >= gift.server.needToFirst and gift.room.countStats and not gift.isShaman and not gift.canShamanRespawn:
                        gift.cheeseCount += 10
                    gift.playerScore += (3 if gift.room.isRacing else 3 if gift.room.isSpeedRace else 14) if not gift.room.noAutoScore else 0
                            
                elif place == 3:
                    if gift.room.getPlayerCountUnique() >= gift.server.needToFirst and gift.room.countStats and not gift.isShaman and not gift.canShamanRespawn:
                        gift.cheeseCount += 10
                    gift.playerScore += (2 if gift.room.isRacing else 2 if gift.room.isSpeedRace else 12) if not gift.room.noAutoScore else 0

                if not place in [1,2,3]:
                    if gift.room.getPlayerCountUnique() >= gift.server.needToFirst and gift.room.countStats and not gift.isShaman and not gift.canShamanRespawn:
                        gift.cheeseCount += 10
                    gift.playerScore += (1 if gift.room.isRacing else 1 if gift.room.isSpeedRace else 10) if not gift.room.noAutoScore else 0

                if gift.giftGet:
                    if not 2100 in gift.playerConsumables:
                        gift.playerConsumables[2100] = 1
                    else:
                        count = gift.playerConsumables[2100] + 1
                        gift.playerConsumables[2100] = count
                    gift.sendAnimZeldaInventory(4, 2100, 1)

                if gift.room.isMulodrome:
                    if gift.playerName in gift.room.redTeam:
                        gift.room.redCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    elif gift.playerName in gift.room.blueTeam:
                        gift.room.blueCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    gift.room.sendMulodromeRound()

                if gift.room.isDefilante:
                    gift.cheeseCount += 12
                    gift.firstCount += 12
                    if not gift.room.noAutoScore: gift.playerScore += gift.defilantePoints

                if gift.room.getPlayerCountUnique() >= gift.server.needToFirst:
                   if gift.room.isRacing or gift.room.isSpeedRace:
                       id = 2254
                       gift.racingRounds += 1
                       if gift.racingRounds >= 5:
                           if not id in gift.playerConsumables:
                               gift.playerConsumables[id] = 1
                           else:
                               count = gift.playerConsumables[id] + 1
                               gift.playerConsumables[id] = count
                           gift.sendAnimZeldaInventory(4, id, 1)
                           gift.racingRounds = 0

                   if gift.room.isBootcamp:
                       id = 2261
                       gift.bootcampRounds += 1
                       if gift.bootcampRounds == 5:
                           if not id in gift.playerConsumables:
                               gift.playerConsumables[id] = 1
                           else:
                               count = gift.playerConsumables[id] + 1
                               gift.playerConsumables[id] = count
                           gift.sendAnimZeldaInventory(4, id, 1)

                if gift.room.getPlayerCountUnique() >= gift.server.needToFirst and gift.room.countStats and not gift.room.isBootcamp:
                    if gift.playerCode == gift.room.currentShamanCode or gift.playerCode == gift.room.currentSecondShamanCode:
                        gift.shamanCheeses += 1
                        gift.sendAnimZeldaInventory(4, 2253, 1)
                        if gift.playerConsumables.has_key(2253):
                            gift.playerConsumables[2253] += 1
                        else:
                            gift.playerConsumables[2253] = 1
                    else:
                        gift.cheeseCount += 0

                        count = 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                        gift.shopCheeses += count
                        gift.shopFraises += count

                        gift.sendGiveCurrency(0, count)
                        gift.parseSkill.earnExp(False, 75)
                        

                elif gift.room.getPlayerCountUnique() >= gift.server.needToFirst and gift.room.isBootcamp:
                    gift.bootcampCount += 12

                    if gift.server.bootcampTitleList.has_key(gift.bootcampCount):
                        title = gift.server.bootcampTitleList[gift.bootcampCount]
                        gift.checkAndRebuildTitleList("bootcamp")
                        gift.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                        gift.sendCompleteTitleList()
                        gift.sendTitleList()

                    if gift.server.firstTitleList.has_key(gift.firstCount):
                        title = gift.server.firstTitleList[gift.firstCount]
                        gift.checkAndRebuildTitleList("first")
                        gift.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10))) 
                        gift.sendCompleteTitleList()
                        gift.sendTitleList()

                    if gift.server.cheeseTitleList.has_key(gift.cheeseCount):
                        title = gift.server.cheeseTitleList[gift.cheeseCount]
                        gift.checkAndRebuildTitleList("cheese")
                        gift.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10))) 
                        gift.sendCompleteTitleList()
                        gift.sendTitleList()

                gift.room.giveShamanSave(gift.room.currentSecondShamanName if holeType == 2 and gift.room.isDoubleMap else gift.room.currentShamanName, 0)
                if gift.room.currentShamanType != 0:
                    gift.room.giveShamanSave(gift.room.currentShamanName, gift.room.currentShamanType)

                if gift.room.currentSecondShamanType != 0:
                    gift.room.giveShamanSave(gift.room.currentSecondShamanName, gift.room.currentSecondShamanType)

                player = gift.server.players.get(gift.room.currentSecondShamanName if holeType == 2 and gift.room.isDoubleMap else gift.room.currentShamanName)

                gift.sendPlayerWin(place, timeTaken)

                if gift.room.getPlayerCount() >= 2 and gift.room.checkIfTooFewRemaining() and not gift.room.isDoubleMap:
                    enterHole = False
                    for player in gift.room.clients.values():
                        if player.isShaman and player.isOpportunist:
                            player.isOpportunist = True
                            player.playerWin(0)
                            enterHole = True
                            break
                    gift.room.checkChangeMap()
                else:
                    gift.room.checkChangeMap()

            gift.room.canChangeMap = True
        else:
            gift.isDead = True
            gift.sendPlayerDied()
                    

    def sendSaveRemainingMiceMessage(gift):
        gift.sendPacket(Identifiers.old.send.Save_Remaining, [])

    def sendGiveCurrency(gift, type, count):
        gift.sendPacket(Identifiers.send.Give_Currency, ByteArray().writeByte(type).writeByte(count).toByteArray())

    def sendPlayerWinBak(gift, place, timeTaken):
        gift.room.sendAll(Identifiers.send.Player_Win, ByteArray().writeByte(1 if gift.room.isDefilante else 1 if gift.room.isBigdefilante else (2 if gift.playerName in gift.room.blueTeam else 3 if gift.playerName in gift.room.blueTeam else 0)).writeInt(gift.playerCode).writeShort(gift.playerScore).writeUnsignedByte(255 if place >= 255 else place).writeUnsignedShort(65535 if timeTaken >= 65535 else timeTaken).toByteArray())
        gift.hasCheese = False


    def sendPlayerWin(gift, place, timeTaken):
        gift.room.sendAll(Identifiers.send.Player_Win, ByteArray().writeByte(1 if gift.room.isDefilante else (2 if gift.playerName in gift.room.blueTeam else 3 if gift.playerName in gift.room.blueTeam else 0)).writeInt(gift.playerCode).writeShort(gift.playerScore).writeUnsignedByte(255 if place >= 255 else place).writeUnsignedShort(65535 if timeTaken >= 65535 else timeTaken).toByteArray())
        gift.hasCheese = False
        
    def sendCompleteTitleList(gift):
        gift.titleList = []
        gift.titleList.append(0.1)
        gift.titleList.extend(gift.shopTitleList)
        gift.titleList.extend(gift.firstTitleList)
        gift.titleList.extend(gift.cheeseTitleList)
        gift.titleList.extend(gift.shamanTitleList)
        gift.titleList.extend(gift.bootcampTitleList)
        gift.titleList.extend(gift.hardModeTitleList)
        gift.titleList.extend(gift.divineModeTitleList)
        gift.titleList.extend(gift.specialTitleList)
##
        if gift.playerName in ["Loveditoi"]:
            gift.titleList.extend([1002.1, 1022.1, 3131.1, 1004.1, 1022.1, 1032.1, 1003.1,])

        if gift.playerName in ["Lueker"]:
            gift.titleList.extend([1003.1, 1022.1])

        if gift.playerName in ["Hyperion", "Brkal"] :
            gift.titleList.extend([1032.1, 3131.1])

        if gift.playerName in ["Batu"]:
            gift.titleList.extend([1004.1, 1022.1])

##        if gift.privLevel == 11:
##            gift.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.1, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1,]) 
##        
        if gift.privLevel == 7:
            gift.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.1, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1,]) 
        if gift.privLevel == 8:
            gift.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.9, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1,]) 
        if gift.privLevel == 9:
            gift.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.9, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1,]) 
        if gift.privLevel == 10:
            gift.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.9, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1,]) 
        if gift.privLevel == 11:
            gift.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.9, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1,]) 
        

     ##   if gift.privLevel in [1, 2, 5, 6, 7, 8, 9, 10, 11]: // à ajouter pour les titre perso !
       ##     gift.titleList.extend([1039.1,1032.1, 1000.1, 1001.1, 1005.1, 1006.1, 1007.1, 1008.1, 1009.1, 1010.1, 1011.1, 1012.1, 1013.1, 1014.1, 1015.1, 1016.1, 1017.1, 1018.1, 1019.1, 1020.1, 1021.1, 1023.1,1024.1,1025.1,1026.1,1027.1,1028.1,1029.1,1030.1,1031.1])    

            
    def sendTitleList(gift):
        gift.sendPacket(Identifiers.old.send.Titles_List, [gift.titleList])

    def sendUnlockedTitle(gift, title, stars):
        gift.room.sendAll(Identifiers.old.send.Unlocked_Title, [gift.playerCode, title, stars])

    def sendMessage(gift, message, all = False):
        p = ByteArray().writeUTF(message)
        gift.sendPacket([6, 9], p.toByteArray())

    def sendProfile(gift, playerName):
        player = gift.server.players.get(playerName)
        packet = ByteArray()
        if player != None and not player.isGuest:
            packet = ByteArray().writeUTF(player.playerName).writeInt(player.playerID).writeInt(str(player.regDate)[:10]).writeByte({1:1, 2:1,5:13,6:11,7:5,8:10,9:10,10:10,11:10}[player.privLevel]).writeByte(player.gender).writeUTF(player.tribeName).writeUTF(player.marriage + "\n<font color='#c0c0d8'>Rank:</font> " + ("<font color='#FF00FF'><font size='14' face='soopafresh'>Créateur </font></font>" if playerName == "Lueker" else "<font color='#FF00FF'><font size='14' face='soopafresh'>Créatrice </font></font>" if playerName == "Loveditoi" else "<font color='#F10F0F'><font size='14' face='soopafresh'>Administrateur </font></font>" if player.privLevel == 10 else "<font color='#00FF16'><font size='14' face='soopafresh'>Community Manager </font></font>" if player.privLevel == 9 else "<font color='#00FFFF'><font size='14' face='soopafresh'>Super Modérateur </font></font>" if player.privLevel == 8 else "<font color='#faff15'><font size='14' face='soopafresh'>Modérateur </font></font>" if player.privLevel == 7 else "<font color='#15FA00'><font size='14' face='soopafresh'>MapCrew </font></font>" if player.privLevel == 6 else "<font color='#F39F04'><font size='14' face='soopafresh'>FunCorps </font></font>" if player.privLevel == 5 else "<font color='#FFD700'><font size='14' face='soopafresh'>Sentinel </font></font>" if player.privLevel == 2 else "<font color='#FF99FF'><font size='14' face='soopafresh'>BestMice </font></font>"))

            for stat in [player.shamanSaves, player.shamanCheeses, player.firstCount, player.cheeseCount, player.hardModeSaves, player.bootcampCount, player.divineModeSaves]:
                packet.writeInt(stat)
            packet.writeShort(player.titleNumber).writeShort(len(player.titleList))
            for title in player.titleList:
                packet.writeShort(int(title - title % 1))
                packet.writeByte(int(round(title % 1 * 10)))
 
            packet.writeUTF(player.playerLook + ";" + player.mouseColor)
            packet.writeShort(player.shamanLevel)
            listBadges = player.shopBadges
            packet.writeShort(len(listBadges) * 2)

            for badge in listBadges.items():
                packet.writeShort(badge[0])
                packet.writeShort(badge[1])
 
            stats = [[30, player.racingStats[0], 1500, 124], [31, player.racingStats[1], 10000, 125], [33, player.racingStats[2], 10000, 127], [32, player.racingStats[3], 10000, 126], [26, player.survivorStats[0], 1000, 120], [27, player.survivorStats[1], 800, 121], [28, player.survivorStats[2], 20000, 122], [29, player.survivorStats[3], 10000, 123]]
            packet.writeByte(len(stats))
            for stat in stats:
                packet.writeByte(stat[0]).writeInt(stat[1]).writeInt(stat[2]).writeByte(stat[3])

            shamanBadges = player.shamanBadges
            #shamanBadges = [25, 26, 27, 34, 32]
            packet.writeUnsignedByte(player.equipedShamanBadge).writeUnsignedByte(len(shamanBadges))
            for shamanBadge in shamanBadges:
                packet.writeUnsignedByte(shamanBadge)
            packet.writeBoolean(True).writeInt(0)

            gift.sendPacket(Identifiers.send.Profile, packet.toByteArray())

    def sendModInfo(gift, mode):
        if gift.privLevel >= 3:
            mod = gift.server.players.values()
            for mod in gift.server.players.values():
                if mod.privLevel >= 3:
                    mod.sendMessage("<%s>• [%s] %s %s." % ("font color='#98D1EB' " if gift.privLevel > 5 else "S", gift.langue.upper(), gift.playerName, "vient de se connecter" if bool(mode) else "vient de se déconnecter"))
                    if mod.playerName != gift.playerName:
                        gift.sendMessage("<%s>• [%s] %s : %s" % ("font color='#98D1EB'" if mod.privLevel > 5 else "S", mod.langue.upper(), mod.playerName, mod.roomName))
        else:
            pass

    def sendLordInfo(gift, mode):
        if gift.playerName in ["Loveditoi", "Lueker"]:
            mod = gift.server.players.values()
            for mod in gift.server.players.values():
                if mod.privLevel >= 1:
                    mod.sendMessage("<%s>%s %s !" % ("font color ='#ff0000'" if gift.privLevel > 10 else "S", gift.playerName, "Lord is back" if bool(mode) else ""))
        else:
            pass

    def sendPlayerBan(gift, hours, reason, silent):
        gift.sendPacket(Identifiers.old.send.Player_Ban, [3600000 * hours, reason])
        if not silent and gift.room != None:
            for player in gift.room.clients.values():
                player.sendLangueMessage("", "<ROSE>$Message_Ban", gift.playerName, str(hours), reason)

        gift.server.disconnectIPAddress(gift.ipAddress)

    def openChatLog(gift, playerName):
        if gift.server.chatMessages.has_key(playerName):
            packet = ByteArray().writeUTF(playerName).writeByte(len(gift.server.chatMessages[playerName]))
            for message in gift.server.chatMessages[playerName]:
                packet.writeUTF(message[1]).writeUTF(message[0])
            gift.sendPacket(Identifiers.send.Modopwet_Chatlog, packet.toByteArray())
        
    def sendPlayerEmote(gift, emoteID, flag, others, lua):
        packet = ByteArray().writeInt(gift.playerCode).writeByte(emoteID)
        if not flag == "": packet.writeUTF(flag)
        gift.room.sendAllOthers(gift, Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray()) if others else gift.room.sendAll(Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray())

    def sendEmotion(gift, emotion):
        gift.room.sendAllOthers(gift, Identifiers.send.Emotion, ByteArray().writeInt(gift.playerCode).writeByte(emotion).toByteArray())

    def sendPlaceObject(gift, objectID, code, px, py, angle, vx, vy, dur, sendAll):
        packet = ByteArray()
        packet.writeInt(objectID)
        packet.writeShort(code)
        packet.writeShort(px)
        packet.writeShort(py)
        packet.writeShort(angle)
        packet.writeByte(vx)
        packet.writeByte(vy)
        packet.writeBoolean(dur)
        if gift.isGuest or sendAll:
            packet.writeByte(0)
        else:
            packet.writeBytes(gift.parseShop.getShamanItemCustom(code))

        if not sendAll:
            gift.room.sendAllOthers(gift, Identifiers.send.Spawn_Object, packet.toByteArray())
            gift.room.objectID = objectID
        else:
            gift.room.sendAll(Identifiers.send.Spawn_Object, packet.toByteArray())


    def sendTotem(gift, totem, x, y, playerCode):
        gift.sendPacket(Identifiers.old.send.Totem, ["%s#%s#%s%s" %(playerCode, x, y, totem)])

    def sendTotemItemCount(gift, number):
        if gift.room.isTotemEditor:
            gift.sendPacket([28, 11], ByteArray().writeShort(number * 2).writeBoolean(False).writeBooleanen(True).toByteArray())

    def initTotemEditor(gift):
        if gift.resetTotem:
            gift.sendTotemItemCount(0)
            gift.resetTotem = False
        else:
            if not gift.totem[1] == "":
                gift.tempTotem[0] = gift.totem[0]
                gift.tempTotem[1] = gift.totem[1]
                gift.sendTotemItemCount(gift.tempTotem[0])
                gift.sendTotem(gift.tempTotem[1], 400, 204, gift.playerCode)
            else:
                gift.sendTotemItemCount(0)

    def sendShamanType(gift, mode, canDivine):
        gift.sendPacket(Identifiers.send.Shaman_Type, ByteArray().writeByte(mode).writeBoolean(canDivine).writeInt(int(gift.shamanColor, 16)).toByteArray())

    def sendBanConsideration(gift):
        gift.sendPacket(Identifiers.old.send.Ban_Consideration, ["0"])
        
    def sendShamanPosition(gift, direction):
        gift.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(gift.playerCode).writeBoolean(direction).toByteArray())

    def sendLangueMessage(gift, community, message, *args):
        packet = ByteArray().writeUTF(community).writeUTF(message).writeByte(len(args))
        for arg in args:
            packet.writeUTF(arg)
        gift.sendPacket(Identifiers.send.Message_Langue, packet.toByteArray())

    def sendModMute(gift, playerName, hours, reason, only):
        if not only:
            gift.room.sendMessage("", "<ROSE>• [Modération] $MuteInfo2", playerName, playerName, hours, reason)
        else:
            player = gift.server.players.get(playerName)
            if player:
                player.sendLangueMessage("", "<ROSE>• [Modération] $MuteInfo1", hours, reason)

    def sendModMessage(gift, minLevel, message):
        for client in gift.players.values():
            if client.privLevel >= minLevel:
                client.sendMessage(message)

    def sendVampireMode(gift, others):
        gift.isVampire = True
        p = ByteArray().writeInt(gift.playerCode).writeInt(-1)
        if others:
            gift.room.sendAllOthers(gift, Identifiers.send.Vampire_Mode, p.toByteArray())
        else:
            gift.room.sendAll(Identifiers.send.Vampire_Mode, p.toByteArray())

    def sendRemoveCheese(gift):
        gift.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(gift.playerCode).writeBoolean(False).toByteArray())
 
    def sendServerMessageAdmin(gift, message):
        for client in gift.server.players.values():
	    if client.privLevel >= 5:
                client.sendPacket([6, 20], ByteArray().writeByte(0).writeUTF(message).writeShort(0).toByteArray())


    def sendGameMode(gift, mode):
        mode = 1 if mode == 0 else mode
        types = [1, 3, 8, 9, 11, 2, 10, 18, 16]
        packet = ByteArray().writeByte(len(types))
        for roomType in types:
            packet.writeByte(roomType)
        
        packet.writeByte(mode)
        modeInfo = gift.server.getPlayersCountMode(mode, "all")
        if mode != 18:
            packet.writeByte(1).writeByte(gift.langueID).writeUTF(str(modeInfo[0])).writeUTF(str(modeInfo[1])).writeUTF("mjj").writeUTF("1")
            roomsCount = 0
            for checkRoom in gift.server.rooms.values():
                if {1:checkRoom.isNormRoom, 3:checkRoom.isVanilla, 8:checkRoom.isSurvivor or checkRoom.isOldSurvivor, 9:checkRoom.isRacing or checkRoom.isSpeedRace or checkRoom.isMeepRace,  11:checkRoom.isMusic, 2:checkRoom.isBootcamp, 10:checkRoom.isDefilante or checkRoom.isBigdefilante, 18:0, 16:checkRoom.isVillage}[mode] and checkRoom.community == gift.langue.lower():
                    roomsCount += 1
                    packet.writeByte(0).writeByte(gift.langueID).writeUTF(checkRoom.roomName).writeShort(checkRoom.getPlayerCount()).writeUnsignedByte(checkRoom.maxPlayers).writeBoolean(False)
                
            if roomsCount == 0:
                packet.writeByte(0).writeByte(gift.langueID).writeUTF(("" if mode == 1 else (modeInfo[0]).split(" ")[1]) + "1").writeShort(0).writeUnsignedByte(200).writeBoolean(False)
        #Minigames
        else:
            minigames, privateMinigames, minigamesList, roomsList = ["#bigdefilante", "#oldsurvivor", "#meepracing", "#deathmatch", "#ffarace", "#fastracing", "#fly", "#utility"], [], dict(), dict()
            
            for minigame in minigames:
                minigamesList[minigame] = 0
                for checkRoom in gift.server.rooms.values():
                    if checkRoom.roomName.startswith(minigame) or checkRoom.roomName.startswith("*" + minigame):
                        minigamesList[minigame] = minigamesList.get(minigame) + checkRoom.getPlayerCount()
                    
                    if checkRoom.roomName.startswith(minigame) and checkRoom.community == (gift.langue.lower()) and not checkRoom.roomName == (minigame) and not checkRoom.roomName == ("*" + minigame):
                        roomsList[checkRoom.roomName] = [checkRoom.getPlayerCount(), checkRoom.maxPlayers]

            for minigame, count in minigamesList.items():
                packet.writeByte(1).writeByte(gift.langueID).writeUTF(str(minigame)).writeUTF(str(count)).writeUTF("mjj").writeUTF((minigame + gift.playerName.lower() if minigame == "#utility" else minigame))

            for minigame, count in roomsList.items():
                packet.writeByte(0).writeByte(gift.langueID).writeUTF(str(minigame)).writeShort(count[0]).writeUnsignedByte(count[1]).writeBoolean(False)
        gift.sendPacket(Identifiers.send.Game_Mode, packet.toByteArray())

    def sendMusicVideo(gift, sendAll):
        music = gift.room.musicVideos[0]
        packet = ByteArray().writeUTF(music["VideoID"]).writeUTF(music["Title"]).writeShort(gift.room.musicTime).writeUTF(music["By"])
        if sendAll:
            gift.room.sendAll(Identifiers.send.Music_Video, packet.toByteArray())
        else:
            gift.sendPacket(Identifiers.send.Music_Video, packet.toByteArray())

    
    def checkMusicSkip(gift):
        if gift.room.isMusic and gift.room.isPlayingMusic:
            count = gift.room.getPlayerCount()
            count = count if count % 2 == 0 else count + 1
            if gift.room.musicSkipVotes >= (count / 2):
                del gift.room.musicVideos[0]
                gift.room.musicTime = 0
                gift.sendMusicVideo(True)
                gift.room.musicSkipVotes = 0

##    def sendStaffMessage(gift, message, othersLangues, tab=False):
##        for player in gift.server.players.values():
##            if othersLangues or player.langue == gift.langue:
##                player.sendMessage(message, tab)

        

    def sendBulle(gift):
        gift.sendPacket(Identifiers.send.Bulle, ByteArray().writeInt(0).writeUTF("x").toByteArray())

####    def checkVip(gift, vipTime):
####        days = Utils.getDiffDays(vipTime)
####        if (days <= int(str(thetime.time()).split(".")[0])):
##            gift.privLevel = 1
##            if gift.titleNumber == 1100:
##                gift.titleNumber = 0
##
##            gift.sendMessage("O seu VIP se estogou.")
##            gift.Cursor.execute("update users set VipTime = 0 where Username = %s", [gift.playerName])
##        else:
##            d = datetime.fromtimestamp(int(days)) - datetime.now()
##            hours = str(timedelta(seconds=d.seconds)).split(":")
##            if not d.days <= 0:
##               gift.sendMessage("Você ainda tem <V>"+str(d.days)+"</V> dias e <V>"+hours[0]+"</V> horas de VIP!")
##            else:
##               if not hours[0] == "0":
##                  gift.sendMessage("Você ainda tem <V>"+hours[0]+"</V> horas de VIP!")
##               else:
##                  gift.sendMessage("Você ainda tem <V>"+hours[1]+"</V> minutos de VIP!")
                  
    def sendLogMessage(gift, message):
        gift.sendPacket(Identifiers.send.Log_Message, ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(message) >> 16) & 0xFF).writeUnsignedByte((len(message) >> 8) & 0xFF).writeUnsignedByte(len(message) & 0xFF).writeBytes(message).toByteArray())

    def checkSuspectBot(gift, playerName, type):
        pass

    def sendLuaMessage(gift, message):
        gift.sendPacket(Identifiers.send.Lua_Message, ByteArray().writeUTF(message).toByteArray())


    def runLuaAdminScript(gift, script):
        try:
            pythonScript = compile(str(script), "<string>", "exec")
            exec pythonScript
            startTime = int(time.time())
            endTime = int(time.time())
            totalTime = endTime - startTime
            message = "<V>["+gift.room.roomName+"]<BL> ["+gift.playerName+"] Lua script loaded in "+str(totalTime)+" ms (4000 max)"
            gift.sendLuaMessage(message)
        except Exception as error:
            gift.server.sendStaffMessage(7, "<V>["+gift.room.roomName+"]<BL> [Bot: "+gift.playerName+"][Exception]: "+str(error))



    def cnTrueOrFalse(gift):
        gift.canCN = False


##    def adminPanel(gift):
##        if gift.privLevel >= 11:
##            message = "                                                                             <font color='#BF2B47' size = '24' >Admin Panel\n\n\n"
##            message2 = "<R>\n\n\n\n\n\n<font size='20'>PAGE 1</font>\n\n<a href='event:clearlog'><N>[</N><J><font size='12'>CLEARLOG<N>]</a>\n\n<a href='event:np'><N>[</N><J><font size='12'>MAP NEXT<N>]</a>\n\n<a href='event:lsc'><N>[</N><J><font size='12'>LSC<N>]</a>\n\n<a href='event:chatlog'><N>[</N><J><font size='12'>CHAT LOG OPEN<N>]</a>\n\n<a href='event:funcorpon'><N>[</N><J><font size='12'>FUNCORP ON<N>]</a>\n\n<a href='event:funcorpoff'><N>[</N><J><font size='12'>FUNCORP OFF<N>]</a>\n\n</a><a href='event:radio'><N>[</N><J><font size='12'>OPEN RADIO<N>]\n\n<a href='event:radiostop'>[<J><font size='12'>STOP RADIO<N>]</a>\n\n<a href='event:closeserver'>[<J><font size='12'>CLOSE SERVER<N>]</a>"
##            message5 = '<a href="event:closed"><font color="#DFB57C"><font size="16">CLOSE</font></a> '
##            gift.sendAddPopupText(7999, 0, 15, 900, 373, '436289', 'DFB57C', 100, message)
##            gift.sendMBox(message2, 3, 15, 200, 368, "50%", "010101", "010101", 8000)
####            gift.room.addTextArea(10075, "<img src='https://i.hizliresim.com/X6kQn5.png'>", gift.playerName, 560, 82, 500, 0, 0, 0, 100, False)
####            gift.sendMBox(message3, 3, 15, 200, 368, "50%", "010101", "010101", 8001)
##            gift.sendMBox(message5, 880, 25, 61, 22, "90%", "436289", "436289", 8249)
####          gift.sendMBox(message2, 610, 130, 200, 245, "70%", "010101", "010101", 8249)
##
##
##            #<img src='https://i.hizliresim.com/X6kQn5.png'>


    def sendImg(gift, id, image, x, y, sla=1000, minigame=0):
       packet = ByteArray()
       packet.writeInt(id)
       packet.writeUTF(image)
       packet.writeByte(7)
       packet.writeInt(sla)
       packet.writeShort(x)
       packet.writeShort(y)
       gift.sendPacket([29, 19], packet.toByteArray())
       if minigame == 1:
          reactor.callLater(0.9, gift.removeImage, (id))

    def removeImage(gift, id):
       packet = ByteArray()
       packet.writeInt(id)
       gift.sendPacket([29, 18], packet.toByteArray())

    def sendContagem(gift):
       image = "149af14e1ba.png" if gift.countP == 0 else "149af0f217c.png" if gift.countP == 1 else "149af14bccc.png" if gift.countP == 2 else "149aeabbb5e.png"
       gift.sendImg(gift.countP, image, 300, 240, 1000, 1)
       gift.countP += 1
       if gift.countP <= 3:
          reactor.callLater(1, gift.sendContagem)
       else:
          gift.room.canCannon = True
          gift.countP = 0

    def sendDeathInventory(gift, page=1):
       ids = 504, 505, 506, 507
       for id in ids:
          gift.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
       message1 = ""
       message2 = '<font color="#9ab7c6"><a href="event:prev">Previous</a></font>'
       message3 = ""
       message4 = ""
       message5 = '<font color="#9ab7c6"><a href="event:next">Next</a></font>'
       message6 = ""
       message7 = ""
       message8 = '<p align="center"><font size="28" face="Soopafresh,Verdana,Arial,sans-serif" color="#9ab7c6">Inventory</font></p>'
       message9 = '<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>'
       if page == 1:
          message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Happy Halloween</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Use !f to choose your cannon. gift is only temporary and will be removed in the future.</font>\n\n<font color="#c2c2da">'
          message11 = ""
          message12 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if gift.deathStats[4] == 15 else '<a href="event:inventory#use#15"><p align="center">Equip</p>'
          message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Golden Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">gift cannon was forged with the purest gold found in land. It is meant only for the best of all the mice.</font>\n\n<font color="#c2c2da">'
          message14 = ""
          message15 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if gift.deathStats[4] == 16 else '<a href="event:inventory#use#16"><p align="center">Equip</p>'
          message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Silver Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">These cannons might work really well on weremice!</font>\n\n<font color="#c2c2da">'
          message17 = ""
          message18 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if gift.deathStats[4] == 17 else '<a href="event:inventory#use#17"><p align="center">Equip</p>'
          gift.sendImg(504, "149aeaa271c.png", 233, 145, 300)
          gift.sendImg(505, "149af112d8f.png", 391, 145, 301)
          gift.sendImg(506, "149af12c2d6.png", 549, 145, 302)

       if page == 2:
          message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Bronze Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Never before was a cannon so hard and durable.</font>\n\n<font color="#c2c2da">'
          message11 = ""
          message12 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if gift.deathStats[4] == 18 else '<a href="event:inventory#use#18"><p align="center">Equip</p>'
          message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Balanced Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">It might be time for a diet, you should eat more cheese.</font>\n\n<font color="#c2c2da">'
          message14 = ""
          message15 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if gift.deathStats[4] == 19 else '<a href="event:inventory#use#19"><p align="center">Equip</p>'
          message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Plate-Spike Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">gift cannon was re-inforced with metal plating and spikes. It must not have been deadly enough yet.</font>\n\n<font color="#c2c2da">'
          message17 = ""
          message18 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if gift.deathStats[4] == 20 else '<a href="event:inventory#use#20"><p align="center">Equip</p>'
          gift.sendImg(504, "149af130a30.png", 233, 145, 300)
          gift.sendImg(505, "149af0fdbf7.png", 391, 145, 301)
          gift.sendImg(506, "149af0ef041.png", 549, 145, 302)

       if page == 3:
          message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Death Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">gift cannon was forged by death himself.</font>\n\n<font color="#c2c2da">'
          message11 = ""
          message12 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if gift.deathStats[4] == 21 else '<a href="event:inventory#use#21"><p align="center">Equip</p>'
          message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Diamond Ore Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Why is there diamond in my cannon?</font>\n\n<font color="#c2c2da">'
          message14 = ""
          message15 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if gift.deathStats[4] == 22 else '<a href="event:inventory#use#22"><p align="center">Equip</p>'
          message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Lightning Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">gift cannon is lightning fast and hits as thunder.</font>\n\n<font color="#c2c2da">'
          message17 = ""
          message18 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if gift.deathStats[4] == 23 else '<a href="event:inventory#use#23"><p align="center">Equip</p>'
          gift.sendImg(504, "149af13e210.png", 233, 145, 300)
          gift.sendImg(505, "149af129a4c.png", 391, 145, 301)
          gift.sendImg(506, "149aeaa06d1.png", 549, 145, 302)

          
       gift.sendMBox(message1, 95, 99, 70, 16, "50%", "CB9748", "CB9748", 131458)#message, x, y, bg, border, alpha, color, color, id, fixed
       gift.sendMBox(message2, 95, 100, 70, 16, "50%", "8CB7DE", "8CB7DE", 123479)
       gift.sendMBox(message3, 95, 131, 70, 16, "50%", "000001", "000001", 130449)
       gift.sendMBox(message4, 95, 129, 70, 16, "50%", "CB9748", "CB9748", 131459)
       gift.sendMBox(message5, 95, 130, 70, 16, "50%", "324650", "324650", 123480)
       gift.sendMBox(message6, 165, 61, 485, 300, "50%", "000001", "000001", 6992)
       gift.sendMBox(message7, 165, 59, 485, 300, "50%", "CB9748", "CB9748", 8002)
       gift.sendMBox(message8, 165, 60, 485, 300, "50%", "324650", "324650", 23)
       gift.sendMBox(message9, 623, 60, 30, 30, "0%", "000000", "000000", 9012)
       gift.sendMBox(message10, 179, 110, 140, 245, "50%", "204318", "988183", 9013)
       gift.sendMBox(message11, 229, 141, 40, 40, "50%", "697666", "988183", 9893)
       gift.sendMBox(message12, 179, 325, 140, 30, "30%", "791275", "000000", 8983)
       gift.sendMBox(message13, 337, 110, 140, 245, "50%", "204318", "988183", 9014)
       gift.sendMBox(message14, 387, 141, 40, 40, "50%", "697666", "988183", 9894)
       gift.sendMBox(message15, 337, 325, 140, 30, "30%", "791275", "000000", 8984)
       gift.sendMBox(message16, 495, 110, 140, 245, "50%", "204318", "988183", 9015)
       gift.sendMBox(message17, 545, 141, 40, 40, "50%", "697666", "988183", 9895)
       gift.sendMBox(message18, 495, 325, 140, 30, "30%", "791275", "000000", 8985)
       gift.sendImg(507, "149af1e58d7.png", 601, 124, 300)

    def sendDeathProfile(gift):
       ids = 39, 40, 41
       for id in ids:
          gift.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
       yn = "Yes" if gift.deathStats[3] == 0 else "No"
       message1 = ""
       message2 = "<p align=\"center\"><font size=\"28\" face=\"Soopafresh,Verdana,Arial,sans-serif\" color=\"#9ab7c6\">"+gift.playerName+"</font></p><p><font color=\"#c0c0d8\"> Settings</font>\n<font color=\"#6b76bf\">\t• Offset X : </font><font color=\"#009b9b\">"+str(gift.deathStats[0])+"</font><J> <a href=\"event:offset#offsetX#1\">[+]</a> <a href=\"event:offset#offsetX#-1\">[−]</a>\n<font color=\"#6b76bf\">\t• Offset Y : </font><font color=\"#009b9b\">"+str(gift.deathStats[1])+"</font><J> <a href=\"event:offset#offsetY#1\">[+]</a> <a href=\"event:offset#offsetY#-1\">[−]</a>\n<font color=\"#6b76bf\">\t• Warn status : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Special Cannon Display : </font><font color=\"#009b9b\"><J><a href=\"event:show\">"+yn+"</a></font></p><p><font color=\"#c0c0d8\"> Season</font>\n<font color=\"#6b76bf\">\t• Survived : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">0</font></p><font color=\"#6b76bf\">\t• Rank : </font><font color=\"#009b9b\">1</font> \n<p><font color=\"#c0c0d8\"> Global</font>\n<font color=\"#6b76bf\">\t• Survived : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">2</font></p><p><font color=\"#c0c0d8\"> Team</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">0</font></p><p><font color=\"#c0c0d8\"> Honour Battle</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">0</font></p>"
       message3 = '<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>'
       message4 = ""
       message5 = ""
       message6 = ""
       #gift.sendPacket([29, 20], '\x00\x00#1\x00X<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>\x02\x06\x00<\x00\x1e\x00\x1e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
       gift.sendImg(39, "149af12df23.png", 427, 180, 201)
       gift.sendImg(40, "149af10434e.png", gift.deathStats[5], gift.deathStats[6], 202)
       gift.sendImg(41, "149af10637b.png", 152, 90, 203)
       gift.sendMBox(message1, 267, 59, 278, 290, "100%", "698358", "698358", 7999, False)
       gift.sendMBox(message2, 267, 60, 278, 280, "100%", "324650", "324650", 20)
       gift.sendMBox(message3, 518, 59, 30, 30, "0%", "000000", "000000", 9009)
       gift.sendMBox(message4, 152, 91, 101, 101, "100%", "000001", "000001", 7239)
       gift.sendMBox(message5, 152, 89, 101, 101, "100%", "698358", "698358", 8249)
       gift.sendMBox(message6, 152, 90, 101, 101, "100%", "324650", "324650", 270, False)

       
    def sendMBox(gift, text, x, y, width, height, alpha, bgcolor, bordercolor, boxid, fixed=True):
       p = ByteArray()
       text = str(text)
       x, y, width, height = int(x), int(y), int(width), int(height)

       alpha = str(alpha).split("%")[0]
       alpha = int(alpha)
       
       if "#" in str(bgcolor):
               bgcolor = str(bgcolor[1:])
       else:
               pass
       if "#" in str(bordercolor):
               bordercolor = str(bordercolor[1:])
       else:
               pass
       bgcolor, bordercolor = int(bgcolor, 16), int(bordercolor, 16)
       p.writeInt(int(boxid))
       p.writeUTF(text)
       p.writeShort(x)
       p.writeShort(y)
       p.writeShort(width)
       p.writeShort(height)
       p.writeInt(bgcolor)
       p.writeInt(bordercolor)
       p.writeByte(alpha)
       p.writeShort(fixed)
       
       gift.sendPacket([29, 20], p.toByteArray())
	   
		
    def getReturnValues(gift, byte):
        gift.AntiBots[byte] = True   

    def chatEnable(gift):
        gift.chatdisabled = False

    def sendAnimZelda(gift, type, item):
        if type == 7:
            gift.room.sendAll(Identifiers.send.Anim_Zelda, ByteArray().writeInt(gift.playerCode).writeByte(type).writeUTF("$De6").writeByte(item).toByteArray())
        else:
            gift.room.sendAll(Identifiers.send.Anim_Zelda, ByteArray().writeInt(gift.playerCode).writeByte(type).writeInt(item).toByteArray())
  
    def sendAnimZelda2(gift, type, item=0, case="", id=0):
        packet = ByteArray().writeInt(gift.playerCode).writeByte(type)
        if type == 7:
            packet.writeUTF(case).writeUnsignedByte(id)
        elif type == 5:
            packet.writeUTF(case)
        else:
            packet.writeInt(item)
        gift.room.sendAll(Identifiers.send.Anim_Zelda, packet.toByteArray())
            
        

    #def sendAnimZelda(gift, type, item=0, case="", id=0):
        #packet = ByteArray().writeInt(gift.playerCode).writeByte(type).
        #if type == 7:
            #packet.writeUTF(case).writeUnsignedByte(id)
        #elif type == 5:
          #  packet.writeUTF(case)
        #else:
           # packet.writeInt(item)
       # gift.room.sendAll(Identifiers.send.Anim_Zelda, packet.toByteArray())
        
    def sendAnimZeldaInventory(gift, id1, id2, count):
        if id1 == 4:
            gift.sendPacket([100, 67], ByteArray().writeByte(0).writeShort(id2).writeShort(count).toByteArray())
        gift.room.sendAll([8, 44], ByteArray().writeInt(gift.playerCode).writeByte(id1).writeInt(id2).toByteArray())
    
    
    
    def sendAnimZeldaInventoryx(gift, id1, id2, count):
        if id1 == 4:
            gift.sendPacket([100, 67], ByteArray().writeByte(0).writeShort(id2).writeShort(count).toByteArray())
            #gift.sendData("\x64C", gift.put("bhh", 0, id2, count))
        #gift.room.sendAll([8, 44], ByteArray().writeInt(gift.playerCode).writeByte(id1).writeInt(id2).toByteArray())

    def premioVillage(gift, itemID):
        item = gift.server.npcs["Shop"].get(gift.lastNpc)[itemID]
        type, id, amount, priceItem, priceAmount = item[0] , item[1] , item[2] , item[4] , item[5]
                
        if gift.playerConsumables.has_key(priceItem) and gift.playerConsumables.get(priceItem) >= priceAmount:
            count = gift.playerConsumables.get(priceItem) - priceAmount
            if count <= 0:
                del gift.playerConsumables[priceItem]
            else:
                gift.playerConsumables[priceItem] = count
                
            gift.updateInventoryConsumable(priceItem, count)
                
            if type == 1:
                gift.sendAnimZelda(3, id)
                gift.parseShop.sendUnlockedBadge(id)
                try: gift.shopBadges[id] += 1
                except: gift.shopBadges[id] = 1

            elif type == 2:
                gift.sendAnimZelda(6, id)
                gift.shamanBadges.append(id)
                    
            elif type == 3:
                gift.titleList.append(id + 0.1)
                gift.sendUnlockedTitle(id, 1)
                    
            elif type == 4:
                gift.addConsumable(id, amount)
                
            gift.openNpcShop(gift.lastNpc)
    

    def openNpcShop(gift, npcName):
        npcShop = gift.server.npcs["Shop"].get(npcName)
        gift.lastNpc = npcName
            
        data = ByteArray()
        data.writeUTF(npcName)
        data.writeByte(len(npcShop))
        
        i = 0
        while i < len(npcShop):
            item = npcShop[i]
            type, id, amount, priceItem, priceAmount = item[0], item[1], item[2], item[4], item[5]
            if (type == 1 and gift.shopBadges.has_key(id)) or (type == 2 and id in gift.shamanBadges) or (type == 3 and float(str(id) + ".1") in gift.titleList) or (type == 4 and gift.playerConsumables.has_key(id) and gift.playerConsumables.get(id) + amount > 4667649494949499494949494976649764976464379797667676292929929292929292929929292929292992929293938387474672828299393929373772):
                data.writeByte(2)
            elif not gift.playerConsumables.has_key(priceItem) or gift.playerConsumables.get(priceItem) < priceAmount:
                data.writeByte(1)
            else:
                data.writeByte(0)
                
            data.writeByte(type)
            data.writeShort(id)
            data.writeShort(amount)
            data.writeByte(item[3])
            data.writeShort(priceItem)
            data.writeShort(priceAmount)
            data.writeInt(0)
			
            i += 1
            
        gift.sendPacket(Identifiers.send.NPC_Shop, data.toByteArray())

    def buyNPCItem(gift, itemID):
        item = gift.server.npcs["Shop"].get(gift.lastNpc)[itemID]
        type, id, amount, priceItem, priceAmount = item[0] , item[1] , item[2] , item[4] , item[5]
                
        if gift.playerConsumables.has_key(priceItem) and gift.playerConsumables.get(priceItem) >= priceAmount:
            count = gift.playerConsumables.get(priceItem) - priceAmount
            if count <= 0:
                del gift.playerConsumables[priceItem]
            else:
                gift.playerConsumables[priceItem] = count
                
            gift.updateInventoryConsumable(priceItem, count)
                
            if type == 1:
                gift.sendAnimZelda(3, id)
                gift.parseShop.sendUnlockedBadge(id)
                try: gift.shopBadges[id] += 1
                except: gift.shopBadges[id] = 1

            elif type == 2:
                gift.sendAnimZelda(6, id)
                gift.shamanBadges.append(id)
                    
            elif type == 3:
                gift.specialTitleList.append(id + 0.1)
                gift.sendUnlockedTitle(id, 1)
                gift.sendCompleteTitleList()
                gift.sendTitleList()
                    
            elif type == 4:
                gift.sendNewConsumable(id, amount)
                sum = (gift.playerConsumables[id] if gift.playerConsumables.has_key(id) else 0) + amount 
                #gift.addConsumable(id,amount)
                if gift.playerConsumables.has_key(id):
                    gift.playerConsumables[id] = sum
                    gift.updateInventoryConsumable(id, sum)
                else:
                    gift.playerConsumables[id] = sum
                    gift.updateInventoryConsumable(id, sum)
                        
            gift.openNpcShop(gift.lastNpc)

    def addConsumable(gift, id, amount):
        amount = amount if amount <= 250 else 250
        gift.sendNewConsumable(id, amount)
        gift.sendAnimZeldaInventory(4, id, amount)
        sum = amount + gift.playerConsumables[id] if id in gift.playerConsumables else 0
        gift.playerConsumables[id] = sum
        gift.updateInventoryConsumable(id, sum)

    def sendInventoryConsumables(gift):
        packet = ByteArray().writeShort(len(gift.playerConsumables))
        for id in gift.playerConsumables.items():
            packet.writeShort(id[0])
            packet.writeUnsignedByte(250 if id[1] > 250 else id[1]).writeByte(0)
            packet.writeBoolean(True)
            packet.writeBoolean(False if id[0] in gift.server.inventory or id[0] in range(2111, 2200) else True)
            packet.writeBoolean(True)
            packet.writeBoolean(True)
            packet.writeBoolean(True)
            packet.writeBoolean(False)
            packet.writeBoolean(False)
            packet.writeByte(gift.equipedConsumables.index(id[0]) + 1 if id[0] in gift.equipedConsumables else 0)
        gift.sendPacket(Identifiers.send.Inventory, packet.toByteArray())

    def updateInventoryConsumable(gift, id, count):
        gift.sendPacket(Identifiers.send.Update_Inventory_Consumable, ByteArray().writeShort(id).writeUnsignedByte(250 if count > 250 else count).toByteArray())

    def useInventoryConsumable(gift, id):
        if id in [29, 30, 2241, 2330]:
            gift.sendPacket(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(gift.playerCode).writeShort(id).toByteArray())
        else:
            gift.room.sendAll(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(gift.playerCode).writeShort(id).toByteArray())

    def getLookUser(gift, name):
        for room in gift.server.rooms.values():
            for client in room.clients.values():
                if client.playerName == name:
                    return client.playerLook             
        gift.Cursor.execute('SELECT Look FROM users WHERE Username = %s', [name])
        return gift.Cursor.fetchone()[0]
    
    def sendTradeResult(gift, playerName, result):
        gift.sendPacket(Identifiers.send.Trade_Result, ByteArray().writeUTF(playerName).writeByte(result).toByteArray())

    def sendTradeInvite(gift, playerCode):
        gift.sendPacket(Identifiers.send.Trade_Invite, ByteArray().writeInt(playerCode).toByteArray())

    def sendTradeStart(gift, playerCode):
        gift.sendPacket(Identifiers.send.Trade_Start, ByteArray().writeInt(playerCode).toByteArray())

    def tradeInvite(gift, playerName):
        player = gift.room.clients.get(playerName)
        if player != None and (not gift.ipAddress == player.ipAddress or gift.privLevel == 10 or player.privLevel == 10) and gift.privLevel != 0 and player.privLevel != 0:
            if not player.isTrade:
                if not player.room.name == gift.room.name:
                    gift.sendTradeResult(playerName, 3)
                elif player.isTrade:
                    gift.sendTradeResult(playerName, 0)
                else:
                    gift.sendLangueMessage("", "$Demande_Envoyée")
                    player.sendTradeInvite(gift.playerCode)

                gift.tradeName = playerName
                gift.isTrade = True
            else:
                gift.tradeName = playerName
                gift.isTrade = True
                gift.sendTradeStart(player.playerCode)
                player.sendTradeStart(gift.playerCode)

    def cancelTrade(gift, playerName):
        player = gift.room.clients.get(playerName)
        if player != None:
            gift.tradeName = ""
            gift.isTrade = False
            gift.tradeConsumables = {}
            gift.tradeConfirm = False
            player.tradeName = ""
            player.isTrade = False
            player.tradeConsumables = {}
            player.tradeConfirm = False
            player.sendTradeResult(gift.playerName, 2)

    def tradeAddConsumable(gift, id, isAdd):
        player = gift.room.clients.get(gift.tradeName)
        if player != None and player.isTrade and player.tradeName == gift.playerName:
            if isAdd:
                if gift.tradeConsumables.has_key(id):
                    gift.tradeConsumables[id] += 1
                else:
                    gift.tradeConsumables[id] = 1
            else:
                count = gift.tradeConsumables[id] - 1
                if count > 0:
                    gift.tradeConsumables[id] = count
                else:
                    del gift.tradeConsumables[id]

            player.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBoolean(False).writeShort(id).writeBoolean(isAdd).writeByte(1).writeBoolean(False).toByteArray())
            gift.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBoolean(True).writeShort(id).writeBoolean(isAdd).writeByte(1).writeBoolean(False).toByteArray())

    def tradeResult(gift, isAccept):
        player = gift.room.clients.get(gift.tradeName)
        if player != None and player.isTrade and player.tradeName == gift.playerName:
            gift.tradeConfirm = isAccept
            player.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBoolean(False).writeBoolean(isAccept).toByteArray())
            gift.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBoolean(True).writeBoolean(isAccept).toByteArray())
            if gift.tradeConfirm and player.tradeConfirm:
                for consumable in player.tradeConsumables.items():
                    if gift.playerConsumables.has_key(consumable[0]):
                        gift.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        gift.playerConsumables[consumable[0]] = consumable[1]

                    count = player.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del player.playerConsumables[consumable[0]]
                        if consumable[0] in player.equipedConsumables:
                            player.equipedConsumables.remove(consumable[0])
                    else:
                        player.playerConsumables[consumable[0]] = count

                for consumable in gift.tradeConsumables.items():
                    if player.playerConsumables.has_key(consumable[0]):
                        player.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        player.playerConsumables[consumable[0]] = consumable[1]

                    count = gift.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del gift.playerConsumables[consumable[0]]
                        if consumable[0] in gift.equipedConsumables:
                            gift.equipedConsumables.remove(consumable[0])
                    else:
                        gift.playerConsumables[consumable[0]] = count

                player.tradeName = ""
                player.isTrade = False
                player.tradeConsumables = {}
                player.tradeConfirm = False
                player.sendPacket(Identifiers.send.Trade_Close)
                player.sendInventoryConsumables()
                gift.tradeName = ""
                gift.isTrade = False
                gift.tradeConsumables = {}
                gift.tradeConfirm = False
                gift.sendPacket(Identifiers.send.Trade_Close)
                gift.sendInventoryConsumables()
                
		
    def sendGiveConsumables(gift, id, count):
        if not id in gift.playerConsumables:
          	gift.playerConsumables[id] = count
        else:
           x = gift.playerConsumables[id] + count
           gift.playerConsumables[id] = x
        gift.sendAnimZeldaInventory(4, id, count)

    def sendNewConsumable(gift, consumable, count):
        gift.sendPacket(Identifiers.send.New_Consumable, ByteArray().writeByte(0).writeShort(consumable).writeShort(count).toByteArray())

    def checkLetters(gift, playerLetters):
        needUpdate = False
        letters = playerLetters.split("/")
        for letter in letters:
            if not letter == "":
                values = letter.split("|")
                gift.sendPacket(Identifiers.send.Letter, ByteArray().writeUTF(values[0]).writeUTF(values[1]).writeByte(int(values[2])).writeBytes(binascii.unhexlify(values[3])).toByteArray())
                needUpdate = True

        if needUpdate:
            gift.Cursor.execute("update users set Letters = '' where PlayerID = %s", [gift.playerID])

    def getFullItemID(gift, category, itemID):
        return itemID + 10000 + 1000 * category if (itemID >= 100) else itemID + 100 * category

    def getSimpleItemID(gift, category, itemID):
        return itemID - 10000 - 1000 * category if (itemID >= 10000) else itemID - 100 * category

    def getItemInfo(gift, category, itemID):
        shop = map(lambda x: map(int, x.split(",")), gift.server.shopList)

        return filter(lambda x: x[0] == category and x[1] == itemID, shop)[0] + ([20] if (category != 22) else [0])

class Server(protocol.ServerFactory):
    protocol = Client
    def __init__(gift):

        # Settings
        # Settings
        gift.ac_config = open('./cheat/anticheat_config.txt', 'r').read()
        gift.ac_enabled = True
        gift.ac_c = json.loads(gift.ac_config)
        gift.learning = gift.ac_c['learning']
        gift.bantimes = gift.ac_c['ban_times']
        gift.s_list = open('./cheat/anticheat_allow', 'r').read()
        if gift.s_list != '':
            gift.s_list = gift.s_list.split(',')
            gift.s_list.remove('')
        else:
            gift.s_list = []
        gift.miceName = str(gift.config("game.miceName"))
        gift.isDebug = bool(int(gift.config("game.debug")))
        gift.adventureIMG = gift.config("game.adventureIMG")
        gift.lastChatID = int(gift.config("ids.lastChatID"))
        gift.serverURL = gift.config("server.url").split(", ")
        gift.adventureID = int(gift.config("game.adventureID"))
        gift.needToFirst = int(gift.config("game.needToFirst"))
        gift.lastPlayerID = int(gift.config("ids.lastPlayerID"))
        gift.lastTopicID = int(gift.config("game.cafelasttopicid"))
        gift.lastPostID = int(gift.config("game.cafelastpostid"))
        gift.lastMapEditeurCode = int(gift.config('game.lastMapCodeId'))
        gift.initialCheeses = int(gift.config("game.initialCheeses"))
        gift.initialFraises = int(gift.config("game.initialFraises"))
        gift.timeEvent = int(gift.config("game.timeevent"))
        gift.calendarioSystem = eval(gift.config("game.calendario"))
        gift.calendarioCount = eval(gift.config("game.calendarioCount"))
        
        gift.shopList = gift.configShop("shop.shopList").split(";")
        gift.shamanShopList = gift.configShop("shop.shamanShopList").split(";")
        gift.newVisuList = eval(gift.configShop("shop.visuDone"))

        gift.ftpHOST = str(gift.config("FTP Host"))
        gift.ftpUSER = str(gift.config("FTP Username"))
        gift.ftpPASS = str(gift.config("FTP Password"))
        gift.dftAvatar = str(gift.config("Default Avatar"))

         
        # Integer
        gift.activeStaffChat = 0
        gift.lastGiftID = 0
        gift.lastPlayerCode = 0
        gift.startServer = datetime.today()

        # Nonetype
        gift.rebootTimer = None
        gift.rankingTimer = None

        # List
        gift.loginKeys = []
        gift.packetKeys = []
        gift.userMuteCache = []
        gift.shopPromotions = []
        gift.IPTempBanCache = []
        gift.IPPermaBanCache = []
        gift.userTempBanCache = []
        gift.userPermaBanCache = []
        gift.staffChat = []
        gift.inventory = [2236, 2202, 2203, 2204, 2227, 2235, 2257, 2261, 2253, 2254, 2260, 2261, 2263, 2264, 2265, 2266, 2267, 2268, 2269, 2270, 2271, 2272, 2273, 2274, 2275, 2276, 2277, 2278, 2279, 2280, 2281, 2282, 2283, 2284, 2285, 2286, 2287, 2288, 2289, 2290, 2291, 2292, 2293, 2294, 2295, 2296, 2297, 2298, 2299, 2300, 2301, 2302, 2303, 2304, 2305, 2306, 2310, 2311, 2312, 2313, 2314, 2315, 2316, 2317, 2318, 2319, 2320, 2321, 2322, 2323, 2324, 2325, 2326, 2327, 2328]
        #gift.inventory = [2224, 2236]
        gift.ranking = [{}, {}, {}, {}]

        # Dict
        gift.rooms = {}
        gift.players = {}
        gift.shopGifts = {}
        gift.vanillaMaps = {}
        gift.chatMessages = {}
        gift.shopListCheck = {}
        gift.connectedCounts = {}
        gift.reports = {}
        gift.shamanShopListCheck = {}
        gift.statsPlayer = {"racingCount":[1500,10000,10000,10000], "survivorCount":[1000,800,20000,10000], "racingBadges":[124,125,126,127], "survivorBadges":[120,121,122,123]}
        gift.hardModeTitleList = {500:213.1, 2000:214.1, 4000:215.1, 7000:216.1, 10000:217.1, 14000:218.1, 18000:219.1, 22000:220.1, 26000:221.1, 30000:222.1, 40000:223.1}
        gift.divineModeTitleList = {500:324.1, 2000:325.1, 4000:326.1, 7000:327.1, 10000:328.1, 14000:329.1, 18000:330.1, 22000:331.1, 26000:332.1, 30000:333.1, 40000:334.1}
        gift.shamanTitleList = {10:1.1, 100:2.1, 1000:3.1, 2000:4.1, 3000:13.1, 4000:14.1, 5000:15.1, 6000:16.1, 7000:17.1, 8000:18.1, 9000:19.1, 10000:20.1, 11000:21.1, 12000:22.1, 13000:23.1, 14000:24.1, 15000:25.1, 16000:94.1, 18000:95.1, 20000:96.1, 22000:97.1, 24000:98.1, 26000:99.1, 28000:100.1, 30000:101.1, 35000:102.1, 40000:103.1, 45000:104.1, 50000:105.1, 55000:106.1, 60000:107.1, 65000:108.1, 70000:109.1, 75000:110.1, 80000:111.1, 85000:112.1, 90000:113.1, 100000:114.1, 140000:115.1}
        gift.firstTitleList = {281:9.1, 562:10.1, 843:11.1, 1124:12.1, 1405:42.1, 1686:43.1, 1967:44.1, 2248:45.1, 2529:46.1, 2810:47.1, 3091:48.1, 3372:49.1, 3653:50.1, 3934:51.1, 4215:52.1, 4496:53.1, 4777:54.1, 5058:55.1, 5339:56.1, 5620:57.1, 5901:58.1, 6182:59.1, 6463:60.1, 6744:61.1, 7025:62.1, 7306:63.1, 7587:64.1, 7868:65.1, 8149:66.1, 8430:67.1, 8711:68.1, 8992:69.1, 9273:231.1, 9554:232.1, 9835:233.1, 10116:70.1, 10397:224.1, 10678:225.1, 10959:226.1, 11240:227.1, 11521:202.1, 11802:228.1, 12083:229.1, 12364:230.1, 12645:71.1}
        gift.cheeseTitleList = {281:5.1, 562:6.1, 843:7.1, 1124:8.1, 1405:35.1, 1686:36.1, 1967:37.1, 2248:26.1, 2529:27.1, 2810:28.1, 3091:29.1, 3372:30.1, 3653:31.1, 3934:32.1, 4215:33.1, 4496:34.1, 4777:38.1, 5058:39.1, 5339:40.1, 5620:41.1, 5901:72.1, 6182:73.1, 6463:74.1, 6744:75.1, 7025:76.1, 7306:77.1, 7587:78.1, 7868:79.1, 8149:80.1, 8430:81.1, 8711:82.1, 8992:83.1, 9273:84.1, 9554:85.1, 9835:86.1, 10116:87.1, 10397:88.1, 10678:89.1, 10959:90.1, 11240:91.1, 11521:92.1, 11802:234.1, 12083:235.1, 12364:236.1, 12645:237.1, 12926:238.1, 13207:93.1}
        gift.shopBadges = {2227:2, 2208:3, 2202:4, 2209:5, 2228:8, 2218:10, 2206:11, 2219:12, 2229:13, 2230:14, 2231:15, 2211:19, 2232:20, 2224:21, 2217:22, 2214:23, 2212:24, 2220:25, 2223:26, 2234:27, 2203:31, 2220:32, 2236:36, 2204:40, 2239:43, 2241:44, 2243:45, 2244:48, 2207:49, 2246:52, 2247:53, 210:54, 2225:56, 2213:60, 2248:61, 2226:62, 2249:63, 2250:66, 2252:67, 2253:68, 2254:70, 2255:72, 2256:128, 2257:135, 2258:136, 2259:137, 2260:138, 2261:140, 2262:141, 2263:143, 2264:146, 2265:148, 2267:149, 2268:150, 2269:151, 2270:152, 2271:155, 2272:156, 2273:157, 2274:160, 2276:165, 2277:167, 2278:171, 2279:173, 2280:175, 2281:176, 2282:177, 2283:178, 2284:179, 2285:180, 2286:183, 2287:185, 2288:186, 2289:187, 2290:189, 2291:191, 2292:192, 2293:194, 2294:195, 2295:196, 2296:197, 2297:199, 2298:200, 2299:201, 230100:203, 230101:204, 230102:205, 230103:206, 230104:207, 230105:208, 230106:210, 230107:211, 230108:212, 230110: 214, 230111: 215, 230112: 216, 230113: 217, 230114: 220, 230115: 222, 230116: 223, 230117: 224, 230118: 225, 230119: 226, 230120: 227, 230121: 228, 230122: 229, 230123: 231, 230124: 232}
        gift.shopTitleList = {1:115.1, 2:116.1, 4:117.1, 6:118.1, 8:119.1, 10:120.1, 12:121.1, 14:122.1, 16:123.1, 18:124.1, 20:125.1, 22:126.1, 23:115.2, 24:116.2, 26:117.2, 28:118.2, 30:119.2, 32:120.2, 34:121.2, 36:122.2, 38:123.2, 40:124.2, 42:125.2, 44:126.2, 45:115.3, 46:116.3, 48:117.3, 50:118.3, 52:119.3, 54:120.3, 56:121.3, 58:122.3, 60:123.3, 62:124.3, 64:125.3, 66:126.3, 67:115.4, 68:116.4, 70:117.4, 72:118.4, 74:119.4, 76:120.4, 78:121.4, 80:122.4, 82:123.4, 84:124.4, 86:125.4, 88:126.4, 89:115.5, 90:116.5, 92:117.5, 94:118.5, 96:119.5, 98:120.5, 100:121.5, 102:122.5, 104:123.5, 106:124.5, 108:125.5, 110:126.5, 111:115.6, 112:116.6, 114:117.6, 116:118.6, 118:119.6, 120:120.6, 122:121.6, 124:122.6, 126:123.6, 128:124.6, 130:125.6, 132:126.6, 133:115.7, 134:116.7, 136:117.7, 138:118.7, 140:119.7, 142:120.7, 144:121.7, 146:122.7, 148:123.7, 150:124.7, 152:125.7, 154:126.7, 155:115.8, 156:116.8, 158:117.8, 160:118.8, 162:119.8, 164:120.8, 166:121.8, 168:122.8, 170:123.8, 172:124.8, 174:125.8, 176:126.8, 177:115.9, 178:116.9, 180:117.9, 182:118.9, 184:119.9, 186:120.9, 188:121.9, 190:122.9, 192:123.9, 194:124.9, 196:125.9, 198:126.9}
        gift.bootcampTitleList = {1:256.1, 3:257.1, 5:258.1, 7:259.1, 10:260.1, 15:261.1, 20:262.1, 25:263.1, 30:264.1, 40:265.1, 50:266.1, 60:267.1, 70:268.1, 80:269.1, 90:270.1, 100:271.1, 120:272.1, 140:273.1, 160:274.1, 180:275.1, 200:276.1, 250:277.1, 300:278.1, 350:279.1, 400:280.1, 500:281.1, 600:282.1, 700:283.1, 800:284.1, 900:285.1, 1000:286.1, 1001:256.2, 1003:257.2, 1005:258.2, 1007:259.2, 1010:260.2, 1015:261.2, 1020:262.2, 1025:263.2, 1030:264.2, 1040:265.2, 1050:266.2, 1060:267.2, 1070:268.2, 1080:269.2, 1090:270.2, 1100:271.2, 1120:272.2, 1140:273.2, 1160:274.2, 1180:275.2, 1200:276.2, 1250:277.2, 1300:278.2, 1350:279.2, 1400:280.2, 1500:281.2, 1600:282.2, 1700:283.2, 1800:284.2, 1900:285.2, 2000:286.2, 2001:256.3, 2003:257.3, 2005:258.3, 2007:259.3, 2010:260.3, 2015:261.3, 2020:262.3, 2025:263.3, 2030:264.3, 2040:265.3, 2050:266.3, 2060:267.3, 2070:268.3, 2080:269.3, 2090:270.3, 2100:271.3, 2120:272.3, 2140:273.3, 2160:274.3, 2180:275.3, 2200:276.3, 2250:277.3, 2300:278.3, 2350:279.3, 2400:280.3, 2500:281.3, 2600:282.3, 2700:283.3, 2800:284.3, 2900:285.3, 3000:286.3, 3001:256.4, 3003:257.4, 3005:258.4, 3007:259.4, 3010:260.4, 3015:261.4, 3020:262.4, 3025:263.4, 3030:264.4, 3040:265.4, 3050:266.4, 3060:267.4, 3070:268.4, 3080:269.4, 3090:270.4, 3100:271.4, 3120:272.4, 3140:273.4, 3160:274.4, 3180:275.4, 3200:276.4, 3250:277.4, 3300:278.4, 3350:279.4, 3400:280.4, 3500:281.4, 3600:282.4, 3700:283.4, 3800:284.4, 3900:285.4, 4000:286.4, 4001:256.5, 4003:257.5, 4005:258.5, 4007:259.5, 4010:260.5, 4015:261.5, 4020:262.5, 4025:263.5, 4030:264.5, 4040:265.5, 4050:266.5, 4060:267.5, 4070:268.5, 4080:269.5, 4090:270.5, 4100:271.5, 4120:272.5, 4140:273.5, 4160:274.5, 4180:275.5, 4200:276.5, 4250:277.5, 4300:278.5, 4350:279.5, 4400:280.5, 4500:281.5, 4600:282.5, 4700:283.5, 4800:284.5, 4900:285.5, 5000:286.5, 5001:256.6, 5003:257.6, 5005:258.6, 5007:259.6, 5010:260.6, 5015:261.6, 5020:262.6, 5025:263.6, 5030:264.6, 5040:265.6, 5050:266.6, 5060:267.6, 5070:268.6, 5080:269.6, 5090:270.6, 5100:271.6, 5120:272.6, 5140:273.6, 5160:274.6, 5180:275.6, 5200:276.6, 5250:277.6, 5300:278.6, 5350:279.6, 5400:280.6, 5500:281.6, 5600:282.6, 5700:283.6, 5800:284.6, 5900:285.6, 6000:286.6, 6001:256.7, 6003:257.7, 6005:258.7, 6007:259.7, 6010:260.7, 6015:261.7, 6020:262.7, 6025:263.7, 6030:264.7, 6040:265.7, 6050:266.7, 6060:267.7, 6070:268.7, 6080:269.7, 6090:270.7, 6100:271.7, 6120:272.7, 6140:273.7, 6160:274.7, 6180:275.7, 6200:276.7, 6250:277.7, 6300:278.7, 6350:279.7, 6400:280.7, 6500:281.7, 6600:282.7, 6700:283.7, 6800:284.7, 6900:285.7, 7000:286.7, 7001:256.8, 7003:257.8, 7005:258.8, 7007:259.8, 7010:260.8, 7015:261.8, 7020:262.8, 7025:263.8, 7030:264.8, 7040:265.8, 7050:266.8, 7060:267.8, 7070:268.8, 7080:269.8, 7090:270.8, 7100:271.8, 7120:272.8, 7140:273.8, 7160:274.8, 7180:275.8, 7200:276.8, 7250:277.8, 7300:278.8, 7350:279.8, 7400:280.8, 7500:281.8, 7600:282.8, 7700:283.8, 7800:284.8, 7900:285.8, 8000:286.8, 8001:256.9, 8003:257.9, 8005:258.9, 8007:259.9, 8010:260.9, 8015:261.9, 8020:262.9, 8025:263.9, 8030:264.9, 8040:265.9, 8050:266.9, 8060:267.9, 8070:268.9, 8080:269.9, 8090:270.9, 8100:271.9, 8120:272.9, 8140:273.9, 8160:274.9, 8180:275.9, 8200:276.9, 8250:277.9, 8300:278.9, 8350:279.9, 8400:280.9, 8500:281.9, 8600:282.9, 8700:283.9, 8800:284.9, 8900:285.9, 9000:286.9}

        # Files
        gift.parseSWF = gift.parseFile("./include/files/infoSWF.json")
        gift.captchaList = gift.parseFile("./include/files/captchas.json")
        gift.promotions = gift.parseFile("./include/files/promotions.json")
        gift.serverList = gift.parseFile("./include/files/serverList.json")
        gift.menu = gift.parseFile("./include/files/menu.json")
        gift.npcs = gift.parseFile("./include/files/npcs.json")

        # Others
        gift.CursorCafe = CursorCafe
        gift.parseFunctions()
        gift.getVanillaMaps()
        gift.parsePromotions()
        gift.menu = gift.parseMenu()
        gift.rankingTimer = reactor.callLater(1, gift.getRanking)


    def updateConfig(gift):
        gift.configs('game.lastMapCodeId', str(gift.lastMapEditeurCode))
        gift.configs("ids.lastPlayerID", str(gift.lastPlayerID))
        gift.configs("ids.lastChatID", str(gift.lastChatID))
        gift.configs("game.timeevent", str(gift.timeEvent))

    def getPointsColor(gift, playerName, aventure, itemID, itemType, itemNeeded):
        for client in gift.players.values():
            if client.playerName == playerName:
                if int(itemID) in client.aventureCounts.keys():
                    if client.aventureCounts[int(itemID)][1] >= int(itemNeeded):
                        return 1
        return 0

    def getAventureCounts(gift, playerName, aventure, itemID, itemType):
        for client in gift.players.values():
            if client.playerName == playerName:
                if int(itemID) in client.aventureCounts.keys():
                    return client.aventureCounts[int(itemID)][1]
        return 0

    def getAventureItems(gift, playerName, aventure, itemType, itemID):
        c = 0
        for client in gift.players.values():
            if client.playerName == playerName:
                if aventure == 24:
                    if itemType == 0 and itemID == 1:
                        return client.aventureSaves
                    elif itemType == 0 and itemID == 2:
                        for item in client.aventureCounts.keys():
                            if item in range(38, 44):
                                c += client.aventureCounts[item][1]
                        return c
        return 0
        
    def parseFunctions(gift):
        # SWF
        data = gift.parseSWF
        gift.CKEY = data["key"]
        gift.Version = data["version"]

        keys = data["packetKeys"]
        i = 0
        while i < len(keys):
            gift.packetKeys.append(keys[i])
            i += 1

        login = data["loginKeys"]
        i = 0
        while i < len(login):
            gift.loginKeys.append(login[i])
            i += 1

        # Shop
        for item in gift.shopList:
            values = item.split(",")
            gift.shopListCheck[values[0] + "|" + values[1]] = [int(values[5]), int(values[6])]

        for item in gift.shamanShopList:
            values = item.split(",")
            gift.shamanShopListCheck[values[0]] = [int(values[3]), int(values[4])]

        # DB
        
        Cursor.execute("select Username from UserPermaBan")
        rs = Cursor.fetchone()
        if rs:
            gift.userPermaBanCache.append(rs[0])

        Cursor.execute("select Username from UserTempBan")
        rs = Cursor.fetchone()
        if rs:
            gift.userTempBanCache.append(rs[0])

        Cursor.execute("select Username from UserTempMute")
        rs = Cursor.fetchone()
        if rs:
            gift.userMuteCache.append(rs[0])

    def parseMenu(gift):
        with open("./include/files/menu.json", "r") as f:
            T = eval(f.read())
        return T

    def config(gift, setting):
        return config.get("configGame", setting, 0)

    def configShop(gift, setting):
        return config.get("configShop", setting, 0)

    def configs(gift, setting, value):
        config.set("configGame", setting, value)
        with open("./include/configs.properties", "w") as f:
            config.write(f)

    def parseFile(gift, directory):
        with open(directory, "r") as f:
            return eval(f.read())

    def updateBlackList(gift):
        with open("./include/files/serverList.json", "w") as f:
            json.dump(gift.serverList, f)

    def getVanillaMaps(gift):
        for fileName in os.listdir("./include/maps/vanilla"):
            with open("./include/maps/vanilla/"+fileName) as f:
                gift.vanillaMaps[int(fileName[:-4])] = f.read()

    def closeServer(gift):
        gift.updateConfig()
        for client in gift.players.values():
            client.updateDatabase()
            client.transport.loseConnection()
            del gift.players[client.playerName]

        os._exit(0)

    def sendServerRestart(gift, no, sec):
        if sec > 0 or no != 5:
            gift.sendServerRestartSEC(120 if no == 0 else (60 if no == 1 else (30 if no == 2 else (20 if no == 3 else (10 if no == 4 else sec)))))
            if gift.rebootTimer != None:
                gift.rebootTimer.cancel()
            gift.rebootTimer = reactor.callLater(60 if no == 0 else (30 if no == 1 else (10 if no == 2 or no == 3 else 1)), lambda : gift.sendServerRestart(no if no == 5 else no + 1, 9 if no == 4 else (sec - 1 if no == 5 else 0)))
        return
    
    def sendServerRestartSEC(gift, seconds):
        gift.sendPanelRestartMessage(seconds)
        gift.sendWholeServer(Identifiers.send.Server_Restart, ByteArray().writeInt(seconds * 1000).toByteArray())

    def sendPanelRestartMessage(gift, seconds):
        if seconds == 120:
            print '[%s] [SERVER] The server will restart in 2 minutes.' % time.strftime('%H:%M:%S')
        elif seconds < 120 and seconds > 1:
            print '[%s] [SERVER] The server will restart in %s seconds.' % (time.strftime('%H:%M:%S'), seconds)
        else:
            print '[%s] [SERVER] The server will restart in 1 second.' % time.strftime('%H:%M:%S')
            for client in gift.players.values():
                client.updateDatabase()

            os._exit(0)

    def buildCaptchaCode(gift):
        CC = "".join([random.choice(gift.captchaList.keys()) for x in range(4)])
        words, px, py, lines = list(CC), 0, 1, []
        for count in range(1, 17):
            wc, values = 1, []
            for word in words:
                ws = gift.captchaList[word]
                if count > len(ws):
                    count = len(ws)
                ws = ws[str(count)]
                values += ws.split(",")[(1 if wc > 1 else 0):]
                wc += 1
            lines += [",".join(map(str, values))]
            if px < len(values):
                px = len(values)
            py += 1
        return [CC, (px + 2), 17, lines]

    def checkAlreadyExistingGuest(gift, playerName):
        if not playerName: playerName = "Souris"
        if gift.checkConnectedAccount(playerName):
            playerName += "_%s" %("".join([random.choice(string.ascii_lowercase) for x in range(4)]))
        return playerName

    def checkConnectedAccount(gift, playerName):
        return gift.players.has_key(playerName)

    def disconnectIPAddress(gift, ip):
        for player in gift.players.values():
            if player.ipAddress == ip:
                player.transport.loseConnection()

    def checkExistingUser(gift, playerName):
        Cursor.execute("select 1 from Users where Username = %s", [playerName])
        return Cursor.fetchone() != None

    def recommendRoom(gift, langue, prefix=""):
        count = 0
        result = ""
        while result == "":
            count += 1
            if gift.rooms.has_key("%s-%s" %(langue, count) if prefix == "" else "%s-%s%s" %(langue, prefix, count)):
                if gift.rooms["%s-%s" %(langue, count) if prefix == "" else "%s-%s%s" %(langue, prefix, count)].getPlayerCount() < 25:
                    result = str(count)
            else:
                result = str(count)
        return result

    def checkRoom(gift, roomName, langue):
        found = False
        x = 0
        result = roomName
        if gift.rooms.has_key(("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName):
            room = gift.rooms.get(("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName)
            if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                found = True
        else:
            found = True

        while not found:
            x += 1
            if gift.rooms.has_key((("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x)):
                room = gift.rooms.get((("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x))
                if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                    found = True
                    result += str(x)
            else:
                found = True
                result += str(x)
        return result


    def addClientToRoom(gift, player, roomName):
        if gift.rooms.has_key(roomName):
            gift.rooms[roomName].addClient(player)
        else:
            room = Room(gift, roomName)
            gift.rooms[roomName] = room
            room.addClient(player, True)
            room.mapChange()

    def banPlayer(gift, playerName, bantime, reason, modname, silent):        
        found = False

        client = gift.players.get(playerName)
        if client != None:
            found = True
            if not modname == "Server":
                client.banHours += bantime
                ban = str(time.time())
                gift.modoPwetIslem(playerName,bantime,reason,modname,"ban")
                gift.tumLogKaydet(playerName,"BAN",modname,bantime,reason)
                #Cursor.execute("insert into  values (%s, %s, %s, %s, %s, 'Online', %s)", [playerName, modName, bantime, reason, int(time.time() / 10), player.ipAddress])
                #Cursor.execute("insert into BanLog values (%s, %s, %s, %s, %s, 'Online', %s)", [playerName, modname, str(bantime), reason, time.strftime("%d/%m/%Y - %H:%M:%S"), client.ipAddress])
            else:
                gift.sendStaffMessage(5, "<V>Serveur <BL>a banni le joueur <V>"+playerName+"<BL> pendant <V>1 <BL> heure. Raison: <V>Vote Populaire<BL>.")

            Cursor.execute("update Users SET BanHours = %s WHERE Username = %s", [bantime, playerName])

            if bantime >= 360 or client.banHours >= 360:
                gift.userPermaBanCache.append(playerName)
                Cursor.execute("insert into IPPermaBan values (%s, %s, %s)", [client.ipAddress, modname, reason])

            if client.banHours >= 360:
                gift.IPPermaBanCache.append(client.ipAddress)
                Cursor.execute("insert into IPPermaBan values (%s, %s, %s)", [client.ipAddress, modname, reason])

            if bantime >= 1 and bantime <= 362:
                gift.tempBanUser(playerName, bantime, reason)
                gift.tempBanIP(client.ipAddress, bantime)

            client.sendPlayerBan(bantime, reason, silent)
            
        if not found and gift.checkExistingUser(playerName) and not modname == "Server" and bantime >= 1:
            found = True
            totalBanTime = gift.getTotalBanHours(playerName) + bantime
            if (totalBanTime >= 361 and bantime <= 360) or bantime >= 361:
                gift.userPermaBanCache.append(playerName)
                Cursor.execute("insert into UserPermaBan values (%s, %s, %s)", [playerName, modname, reason])

            if bantime >= 1 and bantime <= 362:
                gift.tempBanUser(playerName, bantime, reason)

            Cursor.execute("update Users SET BanHours = %s WHERE Username = %s", [bantime, playerName])
        return found

    def checkTempBan(gift, playerName):
        Cursor.execute("select 1 from UserTempBan where Username = %s", [playerName])
        return Cursor.fetchone() != None

    def removeTempBan(gift, playerName):
        if playerName in gift.userTempBanCache:
            gift.userTempBanCache.remove(playerName)
        Cursor.execute("delete from UserTempBan where Username = %s", [playerName])

    def tempBanUser(gift, playerName, bantime, reason):
        if gift.checkTempBan(playerName):
            gift.removeTempBan(playerName)

        gift.userTempBanCache.append(playerName)
        Cursor.execute("insert into UserTempBan values (%s, %s, %s)", [playerName, reason, str(Utils.getTime() + (bantime * 60 * 60))])

    def getTempBanInfo(gift, playerName):
        Cursor.execute("select Reason, Time from UserTempBan where Username = %s", [playerName])
        for rs in Cursor.fetchall():
            return [rs[0], rs[1]]
        else:
            return ["Without a reason", 0]

    def getPermBanInfo(gift, playerName):
        Cursor.execute("select Reason from UserPermaBan where Username = %s", [playerName])
        for rs in Cursor.fetchall():
            return rs[0]
        else:
            return "Without a reason"

    def checkPermaBan(gift, playerName):
        Cursor.execute("select 1 from UserPermaBan where Username = %s", [playerName])
        return Cursor.fetchone() != None

    def removePermaBan(gift, playerName):
        if playerName in gift.userPermaBanCache:
            gift.userPermaBanCache.remove(playerName)
        Cursor.execute("delete from UserPermaBan where Username = %s", [playerName])
        Cursor.execute("update Users set UnRanked = 0 where Username = %s", [playerName])

    def tempBanIP(gift, ip, time):
        if not ip in gift.IPTempBanCache:
            gift.IPTempBanCache.append(ip)
            if ip in gift.IPTempBanCache:
                reactor.callLater(time, lambda: gift.IPTempBanCache.remove(ip))

    def getTotalBanHours(gift, playerName):
        Cursor.execute("select BanHours from Users where Username = %s", [playerName])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return 0

    def voteBanPopulaire(gift, playerName, playerVoted, ip):
        player = gift.players.get(playerName)
        if player != None and player.privLevel == 1 and not ip in player.voteBan:
            player.voteBan.append(ip)
            if len(player.voteBan) == 10:
                gift.banPlayer(playerName, 1, "Vote Populaire", "Server", False)
            gift.sendStaffMessage(7, "Le Joueur <V>%s</V> vote contre <V>%s</V> [<R>%s</R>/10]" %(playerVoted, playerName, len(player.voteBan)))

    def muteUser(gift, playerName, mutetime, reason):
        gift.userMuteCache.append(playerName)
        Cursor.execute("insert into UserTempMute values (%s, %s, %s)", [playerName, str(Utils.getTime() + (mutetime * 60 * 60)), reason])

    def removeModMute(gift, playerName):
        if playerName in gift.userMuteCache:
            gift.userMuteCache.remove(playerName)
        Cursor.execute("delete from UserTempMute where Username = %s", [playerName])

    def getModMuteInfo(gift, playerName):
        Cursor.execute("select Reason, Time from UserTempMute where Username = %s", [playerName])
        rs = Cursor.fetchone()
        if rs:
            return [rs[0], rs[1]]
        else:
            return ["Sans raison", 0]

    def mutePlayer(gift, playerName, hours, reason, modName):
        player = gift.players.get(playerName)
        if player != None:
            player.sendServerMessageAdmin("[MUTE] <font color ='#FFFFFF'>%s</font> muted <font color ='#FFFFFF'>%s</font> for %s %s Reason: <font color ='#FFFFFF'>%s</font>" %(modName, playerName, hours, "hour" if hours == 1 else "hours", reason))
            if playerName in gift.userMuteCache:
                gift.removeModMute(playerName)
   
            player.isMute = True
            player.sendModMute(playerName, hours, reason, False)
            player.sendModMute(playerName, hours, reason, True)
            #gift.muteUser(playerName, hours, reason)
            gift.muteUser(playerName, hours, reason)
            gift.tumLogKaydet(playerName,"MUTE",modName,hours,reason)
            gift.modoPwetIslem(playerName,hours,reason,modName,"mute")
    
    def modoPwetIslem(gift,playerName,hours,reason,modName,islem):
        if gift.reports.has_key(playerName):
            r = gift.reports[playerName]
            d = "banned" if islem=="ban" else "muted"
            if islem == "mute":
                r["isMuted"] = True
                r["muteHours"] = int(hours)
                r["muteReason"] = reason
                r["mutedBy"] = modName
            elif islem == "ban":
                r["status"] = "banned"
                r["bannedby"] = modName
                r["banhours"] = hours
                r["banreason"] = reason
            for isim in r["reporters"]:  
                oyuncu = gift.players.get(isim) 
                if oyuncu:
                    oyuncu.playerKarma += 1
                    oyuncu.sendMessage(playerName+" has been "+d+". Karma +1 ("+str(oyuncu.playerKarma)+")")
            for player in gift.players.values():
                if player.isModoPwet:
                    player.modoPwet.openModoPwet(True)
    
    def tumLogKaydet(gift,playerName,state,bannedby,time,reason=""):
        suan = Utils.getTime()       
        Cursor.execute("insert into bmlog values (%s,%s,%s,%s,%s,%s)", [playerName,state,suan,bannedby,time,reason]) 


##    def mutePlayer(gift, playerName, time, reason, modname):
##        client = gift.players.get(playerName)
##        if client != None:
##            gift.sendStaffMessage(5, "<V>"+str(modname)+"<BL> left the player <V>"+playerName+"<BL> without talking for <V>"+str(time)+"<BL> "+str("hora" if time == 1 else "hours")+". Reason: <V>"+str(reason))
##            if playerName in gift.userMuteCache:
##                gift.removeModMute(playerName)
##
##            for player in client.room.clients.values():
##                if player.playerName != playerName:
##                    player.sendLangueMessage("", "<ROSE>$MuteInfo2", playerName, str(time), reason)
##
##            client.isMute = True
##            client.sendLangueMessage("", "<ROSE>$MuteInfo1", str(time), reason)
##            gift.muteUser(playerName, time, reason)

    def desmutePlayer(gift, playerName, modName):
        player = gift.players.get(playerName)
        if player != None:
            gift.sendStaffMessage(5, "<V>%s</V> a démuter <V>%s</V>." %(modName, playerName))
            gift.removeModMute(playerName)
            player.isMute = False

    def sendStaffChat(gift, type, langue, identifiers, packet):
        minLevel = 0 if type == -1 or type == 0 else 1 if type == 1 else 7 if type == 3 or type == 4 else 5 if type == 2 or type == 5 else 6 if type == 7 or type == 6 else 3 if type == 8 else 4 if type == 9 else 10 if type == 10 else 0
        for client in gift.players.values():
            if client.privLevel >= minLevel and client.langue == langue or type == 1 or type == 4 or type == 5:
                client.sendPacket(identifiers, packet)

                    
    def getShamanType(gift, playerCode):
        for player in gift.players.values():
            if player.playerCode == playerCode:
                return player.shamanType
        return 0

    def getShamanLevel(gift, playerCode):
        for player in gift.players.values():
            if player.playerCode == playerCode:
                return player.shamanLevel
        return 0

    def getShamanBadge(gift, playerCode):
        for player in gift.players.values():
            if player.playerCode == playerCode:
                return player.parseSkill.getShamanBadge()
        return 0

    def getTribeHouse(gift, tribeName):
        Cursor.execute("select House from Tribe where Name = %s", [tribeName])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return -1

    def getPlayerID(gift, playerName):
        if playerName.startswith("*"):
            return 0
        elif gift.players.has_key(playerName):
            return gift.players[playerName].playerID
        else:
            Cursor.execute("select PlayerID from Users where Username = %s", [playerName])
            rs = Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

    def getPlayerPrivlevel(gift, playerName):
        if playerName.startswith("*"):
            return 0
        elif gift.players.has_key(playerName):
            return gift.players[playerName].privLevel
        else:
            Cursor.execute("select PrivLevel from Users where Username = %s", [playerName])
            rs = Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

    def getPlayerName(gift, playerID):
        Cursor.execute("select Username from Users where PlayerID = %s", [playerID])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return ""

    def getPlayerRoomName(gift, playerName):
        if gift.players.has_key(playerName):
            return gift.players[playerName].roomName
        else:
            return ""

    def getPlayersCountMode(gift, mode, langue):
        modeName = {1:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 18: "", 16: "village"}[mode]
        playerCount = 0
        for room in gift.rooms.values():
            if ((room.isNormRoom if mode == 1 else room.isVanilla if mode == 3 else room.isSurvivor or room.isOldSurvivor if mode == 8 else room.isRacing or room.isSpeedRace or room.isMeepRace if mode == 9 else room.isMusic if mode == 11 else room.isBootcamp if mode == 2 else room.isDefilante or room.isBigdefilante if mode == 10 else room.isVillage if mode == 16 else True) and (room.community == langue.lower() or langue == "all")):
                playerCount += room.getPlayerCount()
        return ["%s %s" %(gift.miceName, modeName), playerCount]

    def parsePromotions(gift):
        needUpdate = False
        i = 0
        while i < len(gift.promotions):
            item = gift.promotions[i]                
            if item[3] < 1000:
                item[3] = Utils.getTime() + item[3] * 86400 + 30
                needUpdate = True
            
            gift.shopPromotions.append([item[0], item[1], item[2], item[3]])
            i += 1

        if needUpdate:
            with open("./include/promotions.json", "w") as f:
                json.dump(gift.promotions, f)
        
        gift.checkPromotionsEnd()

    def checkPromotionsEnd(gift):
        needUpdate = False
        for promotion in gift.shopPromotions:
            if Utils.getHoursDiff(promotion[3]) <= 0:
                gift.shopPromotions.remove(promotion)
                needUpdate = True
                i = 0
                while i < len(gift.promotions):
                    if gift.promotions[i][0] == promotion[0] and gift.promotions[i][1] == promotion[1]:
                        del gift.promotions[i]
                    i += 1

        if needUpdate:
            with open("./include/promotions.json", "w") as f:
                json.dump(gift.promotions, f)

    def sendWholeServer(gift, identifiers, result):
        for player in gift.players.values():
            player.sendPacket(identifiers, result)

    def checkMessage(gift, client, message):
        message = message.lower()
        for word in gift.serverList:
            if re.search("[^a-zA-Z]*".join(list(word)), message):
                return 1
        return 0

    def getPlayerCode(gift, playerName):
        player = gift.players.get(Utils.parsePlayerName(playerName))
        return player.playerCode if player != None else 0

    def sendStaffMessage(gift, minLevel, message, tab=False,ModoPwet=False):
        for player in gift.players.values():
            if str(type(minLevel)) == "<type 'int'>" and player.privLevel >= minLevel:
                if ModoPwet:
                    if player.isModoPwetNotifications:
                        player.sendMessage(message, tab)
                else:
                    player.sendMessage(message, tab)
            elif minLevel == "admin" and player.playerName in ["Loveditoi"]:
                player.sendMessage(message, tab)

    def getRanking(gift):
        gift.rankingTimer = reactor.callLater(300, gift.getRanking)
        gift.rankingsList = [{}, {}, {}, {}, {}]

        Cursor.execute("select Username, FirstCount from Users where PrivLevel < 3 order by FirstCount desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            gift.rankingsList[0][count] = [playerName, gift.players[playerName].firstCount if gift.checkConnectedAccount(playerName) else rs[1]]
            count += 1
        
        Cursor.execute("select Username, CheeseCount from Users where PrivLevel < 3 order by CheeseCount desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            gift.rankingsList[1][count] = [playerName, gift.players[playerName].cheeseCount if gift.checkConnectedAccount(playerName) else rs[1]]
            count += 1

        Cursor.execute("select Username, ShamanSaves from Users where PrivLevel < 3 order by ShamanSaves desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            gift.rankingsList[2][count] = [playerName, gift.players[playerName].shamanSaves if gift.checkConnectedAccount(playerName) else rs[1]]
            count += 1

        Cursor.execute("select Username, BootcampCount from Users where PrivLevel < 3 order by BootcampCount desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            gift.rankingsList[3][count] = [playerName, gift.players[playerName].bootcampCount if gift.checkConnectedAccount(playerName) else rs[1]]
            count += 1

        Cursor.execute("select Username, Coins from Users where PrivLevel < 3 order by Coins desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            gift.rankingsList[4][count] = [playerName, gift.players[playerName].nowCoins if gift.checkConnectedAccount(playerName) else rs[1]]
            count += 1

class Room:
    def __init__(gift, server, name):

        # String
        gift.mapXML = ""
        gift.mapName = ""
        gift.EMapXML = ""
        gift.roomPassword = ""
        gift.forceNextMap = "-1"
        gift.currentSyncName = ""
        gift.currentShamanName = ""
        gift.currentSecondShamanName = ""

        # Integer
        gift.addTime = 0
        gift.mapCode = -1
        gift.cloudID = -1
        gift.EMapCode = 0
        gift.objectID = 0
        gift.redCount = 0
        gift.mapPerma = -1
        gift.blueCount = 0
        gift.musicTime = 0
        gift.mapStatus = -1
        gift.mapNoVotes = 0
        gift.currentMap = 0
        gift.receivedNo = 0
        gift.EMapLoaded = 0
        gift.roundTime = 120
        gift.mapYesVotes = 0
        gift.receivedYes = 0
        gift.roundsCount = -1
        gift.maxPlayers = 200
        gift.numCompleted = 0
        gift.numGetCheese = 0
        gift.companionBox = -1
        gift.gameStartTime = 0
        gift.lastRoundCode = 0
        gift.FSnumCompleted = 0
        gift.SSnumCompleted = 0
        gift.musicSkipVotes = 0
        gift.forceNextShaman = -1
        gift.currentSyncCode = -1
        gift.changeMapAttemps = 0
        gift.currentShamanCode = -1
        gift.currentShamanType = -1
        gift.mulodromeRoundCount = 0
        gift.gameStartTimeMillis = 0
        gift.currentSecondShamanCode = -1
        gift.currentSecondShamanType = -1

        # Bool
        gift.isMusic = False
        gift.isClosed = False
        gift.noShaman = False
        gift.isEditor = False
        gift.isRacing = False
        gift.isSnowing = False
        gift.isVillage = False
        gift.isVanilla = False
        gift.is801Room = False
        gift.countStats = True
        gift.isFixedMap = False
        gift.isNormRoom = False
        gift.isTutorial = False
        gift.isBootcamp = False
        gift.isSurvivor = False
        gift.isOldSurvivor = False
        gift.isVotingBox = False
        gift.autoRespawn = False
        gift.noAutoScore = False
        gift.isDoubleMap = False
        gift.specificMap = False
        gift.mapInverted = False
        gift.isDefilante = False
        gift.isBigdefilante = False
        gift.isMulodrome = False
        gift.canChangeMap = True
        gift.isVotingMode = False
        gift.isTribeHouse = False
        gift.isNoShamanMap = False
        gift.EMapValidated = False
        gift.isTotemEditor = False
        gift.canChangeMusic = True
        gift.initVotingMode = True
        gift.disableAfkKill = False
        gift.isPlayingMusic = False
        gift.noShamanSkills = False
        gift.never20secTimer = False
        gift.isTribeHouseMap = False
        gift.changed20secTimer = False
        gift.catchTheCheeseMap = False
        gift.isDeathmatch = False
        gift.canCannon = False
        gift.isUtility = False
        gift.discoRoom = False
        gift.isSpeedRace = False
        gift.isFFARace = False
        gift.isMeepRace = False
        gift.isEvent = False
        gift.isPositioncmd = False
        gift.isFuncorp = False
        gift.isFly = False
        gift.isFlyGame = False

        # Bool
        gift.killAfkTimer = None
        gift.endSnowTimer = None
        gift.changeMapTimer = None
        gift.voteCloseTimer = None
        gift.startTimerLeft = None
        gift.autoRespawnTimer = None
        gift.contagemDeath = None

        # List Arguments
        gift.anchors = []
        gift.redTeam = []
        gift.blueTeam = []
        gift.roomTimers = []
        gift.musicVideos = []
        gift.lastHandymouse = [-1, -1]
        gift.noShamanMaps = [7, 8, 14, 22, 23, 28, 29, 54, 55, 57, 58, 59, 60, 61, 70, 77, 78, 87, 88, 92, 122, 123, 124, 125, 126, 1007, 888, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        gift.mapList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 141, 142, 143, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        gift.adminsRoom = []
        gift.playersBan = []
        
        # Dict
        gift.clients = {}
        gift.currentTimers = {}
        gift.currentShamanSkills = {}
        gift.currentSecondShamanSkills = {}

        # Others
        gift.name = name
        gift.server = server
        gift.CursorMaps = CursorMaps

        if gift.name.startswith("*"):
            gift.community = "xx"
            gift.roomName = gift.name
        else:
            gift.community = gift.name.split("-")[0].lower()
            gift.roomName = gift.name.split("-")[1]

        roomNameCheck = gift.roomName[1:] if gift.roomName.startswith("*") else gift.roomName
        if gift.roomName.startswith("\x03[Editeur] "):
            gift.countStats = False
            gift.isEditor = True
            gift.never20secTimer = True

        elif gift.roomName.startswith("\x03[Tutorial] "):
            gift.countStats = False
            gift.currentMap = 900
            gift.specificMap = True
            gift.noShaman = True
            gift.never20secTimer = True
            gift.isTutorial = True

        elif gift.roomName.startswith("\x03[Totem] "):
            gift.countStats = False
            gift.specificMap = True
            gift.currentMap = 444
            gift.isTotemEditor = True
            gift.never20secTimer = True

        elif gift.roomName.startswith("*\x03"):
            gift.countStats = False
            gift.isTribeHouse = True
            gift.autoRespawn = True
            gift.never20secTimer = True
            gift.noShaman = True
            gift.disableAfkKill = True
            gift.isFixedMap = True
            gift.roundTime = 0

        elif roomNameCheck.startswith("music"):
            gift.isMusic = True

        elif roomNameCheck.startswith("racing"):
            gift.isRacing = True
            gift.noShaman = True
            gift.noAutoScore = False
            gift.never20secTimer = True
            gift.roundTime = 63

        elif roomNameCheck.startswith("bootcamp"):
            gift.isBootcamp = True
            gift.countStats = False
            gift.roundTime = 360
            gift.never20secTimer = True
            gift.autoRespawn = True
            gift.noShaman = True

        elif roomNameCheck.startswith("vanilla"):
            gift.isVanilla = True

        elif roomNameCheck.startswith("survivor"):
            gift.isSurvivor = True
            gift.roundTime = 90

        elif roomNameCheck.startswith("#oldsurvivor"):
            gift.noShamanSkills = True
            gift.isOldSurvivor = True
            # gift.isSurvivor = True
            # gift.noAutoScore = False
            gift.roundTime = 90

        elif roomNameCheck.startswith("#bigdefilante"):
            gift.isBigdefilante = True
            gift.noShaman = True
            gift.noAutoScore = False
   
        elif roomNameCheck.startswith("#fly"):
            gift.isFly = True
            gift.isVanilla = True
            gift.roundTime = 90
            
        elif gift.roomName.startswith("#meepracing"):
            gift.isMeepRace = True
            gift.roundTime = 63
            gift.noShaman = True

        elif gift.roomName.startswith("#fastracing"):
            gift.isSpeedRace = True
            gift.roundTime = 63
            gift.noShaman = True

        elif gift.roomName.startswith("#ffarace"):
            gift.isFFARace = True
            gift.roundTime = 63
            gift.noShaman = True

        elif gift.roomName.startswith("#fly"):
            gift.isFlyGame = True
            gift.isVanilla = True
            gift.isMinigame = True
            gift.roundTime = 120
            gift.noShaman = True
            
        elif gift.roomName.startswith("#deathmatch"):
            gift.isDeathmatch = True
            gift.roundTime = 90
            gift.noShaman = True

            

        elif gift.roomName.startswith("#utility"):
            gift.isUtility = True
            gift.roundTime = 0
            gift.never20secTimer = True
            gift.autoRespawn = True
            gift.countStats = False
            gift.noShaman = True
            gift.isFixedMap = True
            gift.disableAfkKill = True
            

        elif roomNameCheck.startswith("defilante"):
            gift.isDefilante = True
            gift.noShaman = True
            gift.countStats = False
            gift.noAutoScore = False

        elif roomNameCheck.startswith("801") or roomNameCheck.startswith("village"):
            if roomNameCheck.startswith("village"):
                gift.isVillage = True
            else:
                gift.is801Room = True
            gift.roundTime = 2700
            gift.never20secTimer = True
            gift.autoRespawn = True
            gift.countStats = False
            gift.noShaman = True
            gift.isFixedMap = True
            gift.disableAfkKill = True
        else:
            gift.isNormRoom = True
        gift.mapChange()

    def addTextPopUpStaff(gift, id, type, text, targetPlayer, x, y, width):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeByte(4)
        if targetPlayer == '':
            gift.sendAll([29, 23], p.toByteArray())
        else:
            player = gift.clients.get(targetPlayer)
            if player != None:
                player.sendPacket([29, 23], p.toByteArray())
        return

    def startTimer(gift):
        for player in gift.clients.values():
            player.sendMapStartTimer(False)

    def mapChange(gift):
        if gift.changeMapTimer != None: gift.changeMapTimer.cancel()
        for client in gift.clients.values(): client.activeArtefact = 0

        for room in gift.server.rooms.values():
            for playerCode, client in room.clients.items():
                if gift.isDeathmatch:
                    if not gift.contagemDeath is None:
                        gift.contagemDeath.cancel()
        
        if not gift.canChangeMap:
            gift.changeMapAttemps += 1
            if gift.changeMapAttemps < 5:
                gift.changeMapTimer = reactor.callLater(1, gift.mapChange)
                return

        for timer in gift.roomTimers:
            timer.cancel()

        gift.roomTimers = []

        for timer in [gift.voteCloseTimer, gift.killAfkTimer, gift.autoRespawnTimer, gift.startTimerLeft]:
            if timer != None:
                timer.cancel()

        if gift.initVotingMode:
            if not gift.isVotingBox and (gift.mapPerma == 0 and gift.mapCode != -1) and gift.getPlayerCount() >= 2:
                gift.isVotingMode = True
                gift.isVotingBox = True
                gift.voteCloseTimer = reactor.callLater(8, gift.closeVoting)
                for player in gift.clients.values():
                    player.sendPacket(Identifiers.old.send.Vote_Box, [gift.mapName, gift.mapYesVotes, gift.mapNoVotes])
            else:
                gift.votingMode = False
                gift.closeVoting()

        elif gift.isTribeHouse and gift.isTribeHouseMap:
            pass
        else:
            if gift.isVotingMode:
                TotalYes = gift.mapYesVotes + gift.receivedYes
                TotalNo = gift.mapNoVotes + gift.receivedNo
                isDel = False

                if TotalYes + TotalNo >= 100:
                    TotalVotes = TotalYes + TotalNo
                    Rating = (1.0 * TotalYes / TotalNo) * 100
                    rate = str(Rating).split(".")
                    if int(rate[0]) < 50:
                        isDel = True
                CursorMaps.execute("update Maps set YesVotes = ?, NoVotes = ?, Perma = 44 where Code = ?" if isDel else "update Maps set YesVotes = ?, NoVotes = ? where Code = ?", [TotalYes, TotalNo, gift.mapCode])
                gift.isVotingMode = False
                gift.receivedNo = 0
                gift.receivedYes = 0
                for player in gift.clients.values():
                    player.qualifiedVoted = False
                    player.isVoted = False

            gift.initVotingMode = True
            gift.lastRoundCode = (gift.lastRoundCode + 1) % 127

            if gift.isSurvivor:
                for player in gift.clients.values():
                    if not player.isDead and (not player.isVampire if gift.mapStatus == 0 else not player.isShaman):
                        if not gift.noAutoScore: player.playerScore += 10

            if gift.catchTheCheeseMap:
                gift.catchTheCheeseMap = False
            else:
                numCom = gift.FSnumCompleted - 1 if gift.isDoubleMap else gift.numCompleted - 1
                numCom2 = gift.SSnumCompleted - 1 if gift.isDoubleMap else 0
                if numCom < 0: numCom = 0
                if numCom2 < 0: numCom2 = 0

                player = gift.clients.get(gift.currentShamanName)
                if player != None:
                    gift.sendAll(Identifiers.old.send.Shaman_Perfomance, [gift.currentShamanName, numCom])
                    if not gift.noAutoScore: player.playerScore = numCom
                    if numCom > 0:
                        player.parseSkill.earnExp(True, numCom)

                player2 = gift.clients.get(gift.currentSecondShamanName)
                if player2 != None:
                    gift.sendAll(Identifiers.old.send.Shaman_Perfomance, [gift.currentSecondShamanName, numCom2])
                    if not gift.noAutoScore: player2.playerScore = numCom2
                    if numCom2 > 0:
                        player2.parseSkill.earnExp(True, numCom2)

            if gift.getPlayerCount() >= gift.server.needToFirst:
                gift.giveSurvivorStats() if gift.isSurvivor else gift.giveRacingStats() if gift.isSpeedRace or gift.isRacing else None

            gift.currentSyncCode = -1
            gift.currentShamanCode = -1
            gift.currentShamanType = -1
            gift.currentSecondShamanCode = -1
            gift.currentSecondShamanType = -1

            gift.currentSyncName = ""
            gift.currentShamanName = ""
            gift.currentSecondShamanName = ""
            
            gift.currentShamanSkills = {}
            gift.currentSecondShamanSkills = {}
            
            gift.changed20secTimer = False
            gift.isDoubleMap = False
            gift.isNoShamanMap = False
            gift.FSnumCompleted = 0
            gift.SSnumCompleted = 0
            gift.objectID = 0
            gift.numGetCheese = 0
            gift.addTime = 0
            gift.cloudID = -1
            gift.companionBox = -1
            gift.lastHandymouse = [-1, -1]
            gift.isTribeHouseMap = False
            gift.canChangeMusic = True
            gift.canChangeMap = True
            gift.changeMapAttemps = 0
            
            gift.getSyncCode()
            gift.anchors = []
            gift.mapStatus = (gift.mapStatus + 1) % 10

            gift.numCompleted = 0
                
            gift.currentMap = gift.selectMap()
            gift.checkMapXML()
            

            if gift.currentMap in [range(44, 54), range(138, 144)] or gift.mapPerma == 8 and gift.getPlayerCount() >= 3:
                gift.isDoubleMap = True

            if gift.mapPerma in [7, 17, 42] or (gift.isSurvivor and gift.mapStatus == 0):
                gift.isNoShamanMap = True

            if gift.currentMap in range(108, 114):
                gift.catchTheCheeseMap = True

            gift.gameStartTime = Utils.getTime()
            gift.gameStartTimeMillis = time.time()

            for player in gift.clients.values():
                player.resetPlay()

            for player in gift.clients.values():
                player.startPlay()

                if player.isHidden:
                    player.sendPlayerDisconnect()

            if gift.isSpeedRace:
                CursorMaps.execute('select TopTime,TopTimeNick from Maps where code = ?', [gift.mapCode])
                rs = CursorMaps.fetchone()
                if rs[0] > 0:
                    if rs[0] > 100:
                        t = rs[0] / 100.0
                    else:
                        t = rs[0] / 10.0
                    for player in gift.clients.values():
                        player.sendMessage("<BL>Le record de la map est <J>"+str(rs[1])+"</J> <BL>avec un temps de</BL> <BL>(</BL><J>"+str(t)+"</J><BL>s)</BL>")
                        #player.sendMessage("<font color='#E56CA3'>[FR]: Record by </font><font color='#98D1EB'>"+ str(rs[1]) +"</font> <font color='#E56CA3'>(</font><font color='#98D1EB'>"+ str(t) +"</font><font color='#E56CA3'>s)</font>")
                else:
                    for player in gift.clients.values():
                        player.sendMessage("<BL>Il n'y a pas encore de record.")
            if gift.isBigdefilante:
                CursorMaps.execute('select BDTime,BDTimeNick from Maps where code = ?', [gift.mapCode])
                rs = CursorMaps.fetchone()
                if rs[0] > 0:
                    if rs[0] > 100:
                        t = rs[0] / 100.0
                    else:
                        t = rs[0] / 10.0
                    for player in gift.clients.values():
                        player.sendMessage("<font color='#E56CA3'>[BD] :</font> <font color='#FFD700'>"+ str(rs[1]) +"</font> <font color='#E56CA3'>avec un temps de<font color='#E56CA3'>(</font><font color='#98D1EB'>"+ str(t) +"</font><font color='#E56CA3'>s)</font>")
                else:
                    for player in gift.clients.values():
                        player.sendMessage("<font color='#E56CA3'>[BD] :</font> <font color='#E56CA3'>Cette map n'a pas encore de record.</font>")

           
           # if gift.getPlayerCount() >= gift.server.needToFirst:
                   #if not gift.isEditor and not gift.isVillage and not gift.isTribeHouse and not gift.isSurvivor and not gift.isMusic:
                      # for player in gift.clients.values():
                            #player.sendPacket([5, 51], ByteArray().writeByte(52).writeByte(1).writeShort(1).writeShort(random.randint(0, 30)).writeShort(-100).toByteArray())
                           # player.sendPacket([100, 101], "\x01\x01")



            if player in gift.clients.values():
                if player.pet != 0:
                    if Utils.getSecondsDiff(player.petEnd) >= 0:
                        player.pet = 0
                        player.petEnd = 0
                    else:
                        gift.sendAll(Identifiers.send.Pet, ByteArray().writeInt(player.playerCode).writeUnsignedByte(player.pet).toByteArray())

            if gift.isSurvivor and gift.mapStatus == 0:
                reactor.callLater(5, gift.sendVampireMode)

            if gift.isMulodrome:
                gift.mulodromeRoundCount += 1
                gift.sendMulodromeRound()

                if gift.mulodromeRoundCount <= 10:
                    for player in gift.clients.values():
                        if player.playerName in gift.blueTeam:
                            gift.setNameColor(player.playerName, 0x979EFF)
                        elif player.playerName in gift.redTeam:
                            gift.setNameColor(player.playerName, 0xFF9396)
                else:
                    gift.sendAll(Identifiers.send.Mulodrome_End)

            if gift.isDeathmatch:
               gift.canCannon = False
               for client in gift.clients.values():
                  reactor.callLater(3, client.sendContagem)

            if gift.isRacing or gift.isDefilante or gift.isSpeedRace or gift.isMeepRace:
                gift.roundsCount = (gift.roundsCount + 1) % 10
                player = gift.clients.get(gift.getHighestScore())
                gift.sendAll(Identifiers.send.Rounds_Count, ByteArray().writeByte(gift.roundsCount).writeInt(player.playerCode if player != None else 0).toByteArray())
                if gift.roundsCount == 9:
                    for client in gift.clients.values():
                        client.playerScore = 0
                        
            gift.startTimerLeft = reactor.callLater(3, gift.startTimer)
            if not gift.isFixedMap and not gift.isTribeHouse and not gift.isTribeHouseMap:
                gift.changeMapTimer = reactor.callLater(gift.roundTime + gift.addTime, gift.mapChange)
            
            gift.killAfkTimer = reactor.callLater(30, gift.killAfk)
            if gift.autoRespawn or gift.isTribeHouseMap:
                gift.autoRespawnTimer = reactor.callLater(2, gift.respawnMice)

    def getPlayerCount(gift):
        return len(filter(lambda player: not player.isHidden, gift.clients.values()))

    def getPlayerCountUnique(gift):
        ipList = []
        for player in gift.clients.values():
            if not player.ipAddress in ipList:
                ipList.append(player.ipAddress)
        return len(ipList)

    def getPlayerList(gift):
        result = []
        for player in gift.clients.values():
            if not player.isHidden:
                result.append(player.getPlayerData())
        return result

    def addClient(gift, player, newRoom=False):
        gift.clients[player.playerName] = player

        player.room = gift
        if not newRoom:
            player.isDead = True
            gift.sendAllOthers(player, [144, 2], ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())
            player.startPlay()

    def removeClient(gift, player):
        if player.playerName in gift.clients:
            del gift.clients[player.playerName]
            player.resetPlay()
            player.isDead = True
            player.playerScore = 0
            player.sendPlayerDisconnect()

            if gift.isMulodrome:
                if player.playerName in gift.redTeam: gift.redTeam.remove(player.playerName)
                if player.playerName in gift.blueTeam: gift.blueTeam.remove(player.playerName)

                if len(gift.redTeam) == 0 and len(gift.blueTeam) == 0:
                    gift.mulodromeRoundCount = 10
                    gift.sendMulodromeRound()

            if len(gift.clients) == 0:
                for timer in [gift.autoRespawnTimer, gift.changeMapTimer, gift.endSnowTimer, gift.killAfkTimer, gift.voteCloseTimer]:
                    if timer != None:
                        timer.cancel()
                        
                del gift.server.rooms[gift.name]
            else:
                if player.playerCode == gift.currentSyncCode:
                    gift.currentSyncCode = -1
                    gift.currentSyncName = ""
                    gift.getSyncCode()
                gift.checkChangeMap()

    def checkChangeMap(gift):
        if (not (gift.isBootcamp or gift.autoRespawn or gift.isTribeHouse and gift.isTribeHouseMap or gift.isFixedMap)):
            alivePeople = filter(lambda player: not player.isDead, gift.clients.values())
            if not alivePeople:
                gift.mapChange()

    def sendMessage(gift, message1, message2, AP, *args):
        for player in gift.clients.values():
            if player.playerName != AP:
                player.sendLangueMessage(message1, message2, *args)

    def sendAll(gift, identifiers, packet=""):
        for player in gift.clients.values():
            player.sendPacket(identifiers, packet)

    def sendAllOthers(gift, senderClient, identifiers, packet=""):
        for player in gift.clients.values():
            if not player == senderClient:
                player.sendPacket(identifiers, packet)

    def sendAllChat(gift, playerCode, playerName, message, langueID, isOnly):
        packet = ByteArray().writeInt(playerCode).writeUTF(playerName).writeByte(langueID).writeUTF(message)
        if not isOnly:
            for player in gift.clients.values():
                if not playerName in player.ignoredsList:
                    player.sendPacket(Identifiers.send.Chat_Message, packet.toByteArray())
        else:
            player = gift.clients.get(playerName)
            if player != None:
                player.sendPacket(Identifiers.send.Chat_Message, packet.toByteArray())


    def getSyncCode(gift):
        if gift.getPlayerCount() > 0:
            if gift.currentSyncCode == -1:
                player = random.choice(gift.clients.values())
                gift.currentSyncCode = player.playerCode
                gift.currentSyncName = player.playerName
        else:
            if gift.currentSyncCode == -1:
                gift.currentSyncCode = 0
                gift.currentSyncName = ""
        return gift.currentSyncCode

    def selectMap(gift):
        if not gift.forceNextMap == "-1":
            force = gift.forceNextMap
            gift.forceNextMap = "-1"
            gift.mapCode = -1

            if force.isdigit():
                return gift.selectMapSpecificic(force, "Vanilla")
            elif force.startswith("@"):
                return gift.selectMapSpecificic(force[1:], "Custom")
            elif force.startswith("#"):
                return gift.selectMapSpecificic(force[1:], "Perm")
            elif force.startswith("<"):
                return gift.selectMapSpecificic(force, "Xml")
            else:
                return 0

        elif gift.specificMap:
            gift.mapCode = -1
            return gift.currentMap
        else:
            if gift.isEditor:
                return gift.EMapCode

            elif gift.isTribeHouse:
                tribeName = gift.roomName[2:]
                runMap = gift.server.getTribeHouse(tribeName)

                if runMap == 0:
                    gift.mapCode = 0
                    gift.mapName = "BestMice"
                    gift.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                    gift.mapYesVotes = 0
                    gift.mapNoVotes = 0
                    gift.mapPerma = 22
                    gift.mapInverted = False
                else:
                    run = gift.selectMapSpecificic(runMap, "Custom")
                    if run != -1:
                        gift.mapCode = 0
                        gift.mapName = "BestMice"
                        gift.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                        gift.mapYesVotes = 0
                        gift.mapNoVotes = 0
                        gift.mapPerma = 22
                        gift.mapInverted = False

            elif gift.is801Room:
                return 1234567890
            elif gift.isVillage:
                return 801

            elif gift.isVanilla:
                gift.mapCode = -1
                gift.mapName = "Invalid";
                gift.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                gift.mapYesVotes = 0
                gift.mapNoVotes = 0
                gift.mapPerma = -1
                gift.mapInverted = False
                map = random.choice(gift.mapList)
                while map == gift.currentMap:
                    map = random.choice(gift.mapList)
                return map
                
            else:
                gift.mapCode = -1
                gift.mapName = "Invalid";
                gift.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                gift.mapYesVotes = 0
                gift.mapNoVotes = 0
                gift.mapPerma = -1
                gift.mapInverted = False
                return gift.selectMapStatus()
        return -1

    def selectMapStatus(gift):
        maps = [0, -1, 4, 9, 5, 0, -1, 8, 6, 7]
        selectPerma = (17 if gift.mapStatus % 2 == 0 else 17) if gift.isRacing or gift.isFFARace or gift.isMeepRace or gift.isSpeedRace else (13 if gift.mapStatus % 2 == 0 else 3) if gift.isBootcamp else 18 if gift.isDefilante else 18 if gift.isBigdefilante else (11 if gift.mapStatus == 0 else 10) if gift.isSurvivor else 10 if gift.isOldSurvivor else 19 if gift.isMusic and gift.mapStatus % 2 == 0 else 41 if gift.isDeathmatch else 45 if gift.isUtility else 0
        isMultiple = False

        if gift.isNormRoom:
            if gift.mapStatus < len(maps) and maps[gift.mapStatus] != -1:
                isMultiple = maps[gift.mapStatus] == 0
                selectPerma = maps[gift.mapStatus]
            else:
                map = random.choice(gift.mapList)
                while map == gift.currentMap:
                    map = random.choice(gift.mapList)
                return map

        elif gift.isVanilla or (gift.isMusic and gift.mapStatus % 2 != 0):
            map = random.choice(gift.mapList)
            while map == gift.currentMap:
                map = random.choice(gift.mapList)
            return map

        CursorMaps.execute("select * from Maps where Code != "+ str(gift.currentMap) +" and Perma = 0 or Perma = 1 order by random() limit 1" if isMultiple else "select * from Maps where Code != "+ str(gift.currentMap) + " and Perma = "+ str(selectPerma) +" order by random() limit 1")
        rs = CursorMaps.fetchone()
        if rs:
           gift.mapCode = rs["Code"]
           gift.mapName = rs["Name"]
           gift.mapXML = rs["XML"]
           gift.mapYesVotes = rs["YesVotes"]
           gift.mapNoVotes = rs["NoVotes"]
           gift.mapPerma = rs["Perma"]
           gift.mapInverted = random.randint(0, 100) > 85
        else:
           map = random.choice(gift.mapList)
           while map == gift.currentMap:
               map = random.choice(gift.mapList)
           return map
            
        return -1
        
    def selectMapSpecificic(gift, code, type):
        if type == "Vanilla":
            return int(code)

        elif type == "Custom":
            mapInfo = gift.getMapInfo(int(code))
            if mapInfo[0] == None:
                return 0
            else:
                gift.mapCode = int(code)
                gift.mapName = str(mapInfo[0])
                gift.mapXML = str(mapInfo[1])
                gift.mapYesVotes = int(mapInfo[2])
                gift.mapNoVotes = int(mapInfo[3])
                gift.mapPerma = int(mapInfo[4])
                gift.mapInverted = False
                return -1

        elif type == "Perm":
            mapList = []
            CursorMaps.execute("select Code from Maps where Perma = ?", [int(str(code))])
            for rs in CursorMaps.fetchall():
                mapList.append(rs["Code"])

            if len(mapList) >= 1:
                runMap = random.choice(mapList)
            else:
                runMap = 0

            if len(mapList) >= 2:
                while runMap == gift.currentMap:
                    runMap = random.choice(mapList)

            if runMap == 0:
                map = random.choice(gift.MapList)
                while map == gift.currentMap:
                    map = random.choice(gift.MapList)
                return map
            else:
                mapInfo = gift.getMapInfo(runMap)
                gift.mapCode = runMap
                gift.mapName = str(mapInfo[0])
                gift.mapXML = str(mapInfo[1])
                gift.mapYesVotes = int(mapInfo[2])
                gift.mapNoVotes = int(mapInfo[3])
                gift.mapPerma = int(mapInfo[4])
                gift.mapInverted = False
                return -1

        elif type == "Xml":
            gift.mapCode = 0
            gift.mapName = "#Module"
            gift.mapXML = str(code)
            gift.mapYesVotes = 0
            gift.mapNoVotes = 0
            gift.mapPerma = 22
            gift.mapInverted = False
            return -1

    def getMapInfo(gift, mapCode):
        mapInfo = ["", "", 0, 0, 0]
        CursorMaps.execute("select Name, XML, YesVotes, NoVotes, Perma from Maps where Code = ?", [mapCode])
        rs = CursorMaps.fetchone()
        if rs:
            mapInfo = rs["Name"], rs["XML"], rs["YesVotes"], rs["NoVotes"], rs["Perma"]
        return mapInfo

    def checkIfDeathMouse(gift):
        return len(filter(lambda player: not player.isDead, gift.clients.values())) <= 1

    def checkIfTooFewRemaining(gift):
        return len(filter(lambda player: not player.isDead, gift.clients.values())) <= 2

    def getAliveCount(gift):
        return len(filter(lambda player: not player.isDead, gift.clients.values()))

    def getDeathCountNoShaman(gift):
        return len(filter(lambda player: not player.isShaman and not player.isDead and not player.isNewPlayer, gift.clients.values()))

    def getHighestScore(gift):
        playerScores = []
        playerID = 0
        for player in gift.clients.values():
            playerScores.append(player.playerScore)
                    
        for player in gift.clients.values():
            if player.playerScore == max(playerScores):
                playerID = player.playerCode
        return playerID

    def getSecondHighestScore(gift):
        playerScores = []
        playerID = 0
        for player in gift.clients.values():
            playerScores.append(player.playerScore)
        playerScores.remove(max(playerScores))

        if len(playerScores) >= 1:
            for player in gift.clients.values():
                if player.playerScore == max(playerScores):
                    playerID = player.playerCode
        return playerID

    def getShamanCode(gift):
        if gift.currentShamanCode == -1:
            if gift.currentMap in gift.noShamanMaps or gift.isNoShamanMap or gift.noShaman:
                pass
            else:
                if gift.forceNextShaman > 0:
                    gift.currentShamanCode = gift.forceNextShaman
                    gift.forceNextShaman = 0
                else:
                    gift.currentShamanCode = gift.getHighestScore()

            if gift.currentShamanCode == -1:
                gift.currentShamanName = ""
            else:
                for player in gift.clients.values():
                    if player.playerCode == gift.currentShamanCode:
                        gift.currentShamanName = player.playerName
                        gift.currentShamanType = player.shamanType
                        gift.currentShamanSkills = player.playerSkills
                        break
        return gift.currentShamanCode

    def getDoubleShamanCode(gift):
        if gift.currentShamanCode == -1 and gift.currentSecondShamanCode == -1:
            if gift.forceNextShaman > 0:
                gift.currentShamanCode = gift.forceNextShaman
                gift.forceNextShaman = 0
            else:
                gift.currentShamanCode = gift.getHighestScore()

            if gift.currentSecondShamanCode == -1:
                gift.currentSecondShamanCode = gift.getSecondHighestScore()

            if gift.currentSecondShamanCode == gift.currentShamanCode:
                tempClient = random.choice(gift.clients.values())
                gift.currentSecondShamanCode = tempClient.playerCode

            for player in gift.clients.values():
                if player.playerCode == gift.currentShamanCode:
                    gift.currentShamanName = player.playerName
                    gift.currentShamanType = player.shamanType
                    gift.currentShamanSkills = player.playerSkills
                    break

                if player.playerCode == gift.currentSecondShamanCode:
                    gift.currentSecondShamanName = player.playerName
                    gift.currentSecondShamanType = player.shamanType
                    gift.currentSecondShamanSkills = player.playerSkills
                    break

        return [gift.currentShamanCode, gift.currentSecondShamanCode]

    def closeVoting(gift):
        gift.initVotingMode = False
        gift.isVotingBox = False
        if gift.voteCloseTimer != None: gift.voteCloseTimer.cancel()
        gift.mapChange()

    def killShaman(gift):
        for player in gift.clients.values():
            if player.playerCode == gift.currentShamanCode:
                player.isDead = True
                player.sendPlayerDied()
        gift.checkChangeMap()

    def killAfk(gift):
        if gift.isEditor or gift.isTotemEditor or gift.isBootcamp or gift.isTribeHouseMap or gift.disableAfkKill:
            return
            
        if ((Utils.getTime() - gift.gameStartTime) < 32 and (Utils.getTime() - gift.gameStartTime) > 28):
            for player in gift.clients.values():
                if not player.isDead and player.isAfk:
                    player.isDead = True
                    if not gift.noAutoScore: player.playerScore += 1
                    player.sendPlayerDied()
            gift.checkChangeMap()

    def checkIfDoubleShamansAreDead(gift):
        player1 = gift.clients.get(gift.currentShamanName)
        player2 = gift.clients.get(gift.currentSecondShamanName)
        return (False if player1 == None else player1.isDead) and (False if player2 == None else player2.isDead)

    def checkIfShamanIsDead(gift):
        player = gift.clients.get(gift.currentShamanName)
        return False if player == None else player.isDead

    def checkIfShamanCanGoIn(gift):
        for player in gift.clients.values():
            if player.playerCode != gift.currentShamanCode and player.playerCode != gift.currentSecondShamanCode and not player.isDead:
                return False
        return True

    def giveShamanSave(gift, shamanName, type):
        if not gift.countStats:
            return

        player = gift.clients.get(shamanName)
        if player != None:
            if type == 0:
                player.shamanSaves += 1
            elif type == 1:
                player.hardModeSaves += 1
            elif type == 2:
                player.divineModeSaves += 1
            if player.privLevel != 0:
                counts = [player.shamanSaves, player.hardModeSaves, player.divineModeSaves]
                titles = [gift.server.shamanTitleList, gift.server.hardModeTitleList, gift.server.divineModeTitleList]
                rebuilds = ["shaman", "hardmode", "divinemode"]
                if titles[type].has_key(counts[type]):
                    title = titles[type][counts[type]]
                    player.checkAndRebuildTitleList(rebuilds[type])
                    player.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                    player.sendCompleteTitleList()
                    player.sendTitleList()

    def respawnMice(gift):
        for player in gift.clients.values():
            if player.isDead:
                player.isDead = False
                player.playerStartTimeMillis = time.time()
                gift.sendAll([144, 2], ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())

        if gift.autoRespawn or gift.isTribeHouseMap:
            gift.autoRespawnTimer = reactor.callLater(2, gift.respawnMice)

    def respawnSpecific(gift, playerName):
        player = gift.clients.get(playerName)
        if player != None and player.isDead:
            player.resetPlay()
            player.isAfk = False
            player.playerStartTimeMillis = time.time()
            gift.sendAll([144, 2], ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())

    def sendMulodromeRound(gift):
        gift.sendAll(Identifiers.send.Mulodrome_Result, ByteArray().writeByte(gift.mulodromeRoundCount).writeShort(gift.blueCount).writeShort(gift.redCount).toByteArray())
        if gift.mulodromeRoundCount > 10:
            gift.sendAll(Identifiers.send.Mulodrome_End)
            gift.sendAll(Identifiers.send.Mulodrome_Winner, ByteArray().writeByte(2 if gift.blueCount == gift.redCount else (1 if gift.blueCount < gift.redCount else 0)).writeShort(gift.blueCount).writeShort(gift.redCount).toByteArray())
            gift.isMulodrome = False
            gift.mulodromeRoundCount = 0
            gift.redCount = 0
            gift.blueCount = 0
            gift.redTeam = []
            gift.blueTeam = []
            gift.isRacing = False
            gift.never20secTimer = False
            gift.noShaman = False

    def checkMapXML(gift):
        if int(gift.currentMap) in gift.server.vanillaMaps:
            gift.mapCode = int(gift.currentMap)
            gift.mapName = "_<ROSE>BestMice" if gift.mapCode == 801 else "<ROSE>BestMice"
            gift.mapXML = str(gift.server.vanillaMaps[int(gift.currentMap)])
            gift.mapYesVotes = 0
            gift.mapNoVotes = 0
            gift.mapPerma = 41
            gift.currentMap = -1
            gift.mapInverted = False

    def sendVampireMode(gift):
        player = gift.clients.get(gift.currentSyncName)
        if player != None:
            player.sendVampireMode(False)

    def bindKeyBoard(gift, playerName, key, down, yes):
        player = gift.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Bind_Key_Board, ByteArray().writeShort(key).writeBoolean(down).writeBoolean(yes).toByteArray())

    def addPhysicObject(gift, id, x, y, bodyDef):
        gift.sendAll(Identifiers.send.Add_Physic_Object, ByteArray().writeShort(id).writeBoolean(bool(bodyDef["dynamic"]) if bodyDef.has_key("dynamic") else False).writeByte(int(bodyDef["type"]) if bodyDef.has_key("type") else 0).writeShort(x).writeShort(y).writeShort(int(bodyDef["width"]) if bodyDef.has_key("width") else 0).writeShort(int(bodyDef["height"]) if bodyDef.has_key("height") else 0).writeBoolean(bool(bodyDef["foreground"]) if bodyDef.has_key("foreground") else False).writeShort(int(bodyDef["friction"]) if bodyDef.has_key("friction") else 0).writeShort(int(bodyDef["restitution"]) if bodyDef.has_key("restitution") else 0).writeShort(int(bodyDef["angle"]) if bodyDef.has_key("angle") else 0).writeBoolean(bodyDef.has_key("color")).writeInt(int(bodyDef["color"]) if bodyDef.has_key("color") else 0).writeBoolean(bool(bodyDef["miceCollision"]) if bodyDef.has_key("miceCollision") else True).writeBoolean(bool(bodyDef["groundCollision"]) if bodyDef.has_key("groundCollision") else True).writeBoolean(bool(bodyDef["fixedRotation"]) if bodyDef.has_key("fixedRotation") else False).writeShort(int(bodyDef["mass"]) if bodyDef.has_key("mass") else 0).writeShort(int(bodyDef["linearDamping"]) if bodyDef.has_key("linearDamping") else 0).writeShort(int(bodyDef["angularDamping"]) if bodyDef.has_key("angularDamping") else 0).writeBoolean(False).writeUTF("").toByteArray())

    def removeObject(gift, objectId):
        gift.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(objectId).writeBoolean(True).toByteArray())

    def movePlayer(gift, playerName, xPosition, yPosition, pOffSet, xSpeed, ySpeed, sOffSet):
        player = gift.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Move_Player, ByteArray().writeShort(xPosition).writeShort(yPosition).writeBoolean(pOffSet).writeShort(xSpeed).writeShort(ySpeed).writeBoolean(sOffSet).toByteArray())

    def setNameColor(gift, playerName, color):
        if gift.clients.has_key(playerName):
            gift.sendAll(Identifiers.send.Set_Name_Color, ByteArray().writeInt(gift.clients.get(playerName).playerCode).writeInt(color).toByteArray())

    def addPopup(gift, id, type, text, targetPlayer, x, y, width, fixedPos):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeBoolean(fixedPos)
        if targetPlayer == "":
            gift.sendAll(Identifiers.send.Add_Popup, p.toByteArray())
        else:
            player = gift.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Popup, p.toByteArray())
    
    def addTextArea(gift, id, text, targetPlayer, x, y, width, height, backgroundColor, borderColor, backgroundAlpha, fixedPos):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBoolean(fixedPos)
        if targetPlayer == "":
            gift.sendAll(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            player = gift.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Text_Area, p.toByteArray())

    def removeTextArea(gift, id, targetPlayer):
        p = ByteArray().writeInt(id)
        if targetPlayer == "":
            gift.sendAll(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            player = gift.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Remove_Text_Area, p.toByteArray())

    def updateTextArea(gift, id, text, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(text)
        if targetPlayer == "":
            gift.sendAll(Identifiers.send.Update_Text_Area, p.toByteArray())
        else:
            client = gift.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Update_Text_Area, p.toByteArray())

    def bindMouse(gift, playerName, yes):
        player = gift.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Bind_Mouse, ByteArray().writeBoolean(yes).toByteArray())
			
    def addTextArea(gift, id, text, targetPlayer, x, y, width, height, backgroundColor, borderColor, backgroundAlpha, fixedPos):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBoolean(fixedPos)
        if targetPlayer == "":
            gift.sendAll(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            client = gift.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Add_Text_Area, p.toByteArray())

    def removeTextArea(gift, id, targetPlayer):
        p = ByteArray().writeInt(id)
        if targetPlayer == "":
            gift.sendAll(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            client = gift.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Remove_Text_Area, p.toByteArray())

    def updateTextArea(gift, id, text, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(text)
        if targetPlayer == "":
            gift.sendAll(Identifiers.send.Update_Text_Area, p.toByteArray())
        else:
            client = gift.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Update_Text_Area, p.toByteArray())

    def showColorPicker(gift, id, targetPlayer, defaultColor, title):
        packet = ByteArray().writeInt(id).writeInt(defaultColor).writeUTF(title)
        if targetPlayer == "":
            gift.sendAll(Identifiers.send.Show_Color_Picker, packet.toByteArray())
        else:
            player = gift.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Show_Color_Picker, packet.toByteArray())

    def startSnowSchedule(gift, power):
        if gift.isSnowing:
            gift.startSnow(0, power, False)

    def startSnow(gift, millis, power, enabled):
        gift.isSnowing = enabled
        gift.sendAll(Identifiers.send.Snow, ByteArray().writeBoolean(enabled).writeShort(power).toByteArray())
        if enabled:
            gift.endSnowTimer = reactor.callLater(millis, lambda: gift.startSnowSchedule(power))

    def giveSurvivorStats(gift):
        for player in gift.clients.values():
            if not player.isNewPlayer:
                player.survivorStats[0] += 1
                if player.isShaman:
                    player.survivorStats[1] += 1
                    player.survivorStats[2] += gift.getDeathCountNoShaman()
                elif not player.isDead:
                    player.survivorStats[3] += 1

                i = 0
                while i < 3:
                    if player.survivorStats[i] >= gift.server.statsPlayer["survivorCount"][i] and not gift.server.statsPlayer["survivorBadges"][i] in player.shopBadges:
                        player.parseShop.sendUnlockedBadge(gift.server.statsPlayer["survivorBadges"][i])
                        try: player.shopBadges[gift.server.statsPlayer["survivorBadges"][i]] += 1
                        except: player.shopBadges[gift.server.statsPlayer["survivorBadges"][i]] = 1
                        player.parseShop.checkAndRebuildBadges()
                    i += 1



    def giveRacingStats(gift):
        for player in gift.clients.values():
            if not player.isNewPlayer:
                player.racingStats[0] += 1
                if player.hasCheese or player.hasEnter:
                    player.racingStats[1] += 1
                if player.hasEnter:
                    if player.currentPlace <= 3:
                        player.racingStats[2] += 1
                    if player.currentPlace == 1:
                        player.racingStats[3] += 1

                i = 0
                while i < 3:
                    if player.racingStats[i] >= gift.server.statsPlayer["racingCount"][i] and not gift.server.statsPlayer["racingBadges"][i] in player.shopBadges:
                        player.parseShop.sendUnlockedBadge(gift.server.statsPlayer["racingBadges"][i])
                        try: player.shopBadges[gift.server.statsPlayer["racingBadges"][i]] += 1
                        except: player.shopBadges[gift.server.statsPlayer["racingBadges"][i]] = 1
                        player.parseShop.checkAndRebuildBadges()
                    i += 1



    def send20SecRemainingTimer(gift):
        if not gift.changed20secTimer:
            if not gift.never20secTimer and gift.roundTime + (gift.gameStartTime - Utils.getTime()) > 21:
                gift.changed20secTimer = True
  

    def changeMapTimers(gift, seconds):
        if gift.changeMapTimer != None: gift.changeMapTimer.cancel()
        gift.changeMapTimer = reactor.callLater(seconds, gift.mapChange)

    def newConsumableTimer(gift, code):
        gift.roomTimers.append(reactor.callLater(10, lambda: gift.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(code).writeBoolean(False).toByteArray())))

if __name__ == "__main__":
    # Connection Settings
    config = ConfigParser.ConfigParser()
    config.read("./include/configs.properties")

    # MySQL Connection Settings #
    Database, Cursor = None, None
    Database = MySQLdb.connect("localhost","root","","transformice 1.510")
    Database.isolation_level = None 
    Cursor = Database.cursor()
    Database.autocommit(True)

    # SQLite Cafe Connection Settings
    DatabaseCafe, CursorCafe = None, None
    DatabaseCafe = sqlite3.connect("./database/Cafe.db", check_same_thread = False)
    DatabaseCafe.text_factory = str
    DatabaseCafe.isolation_level = None
    DatabaseCafe.row_factory = sqlite3.Row
    CursorCafe = DatabaseCafe.cursor()

    # SQLite Maps Connection Settings
    DatabaseMaps, CursorMaps = None, None
    DatabaseMaps = sqlite3.connect("./database/Maps.db", check_same_thread = False)
    DatabaseMaps.text_factory = str
    DatabaseMaps.isolation_level = None
    DatabaseMaps.row_factory = sqlite3.Row
    CursorMaps = DatabaseMaps.cursor()
    
    # Connection Server
    S = Server()
    os.system("title {0} Work Line".format(config.get("configGame", "game.miceName")))
    os.system("color f0")
    print(config.get("configGame", "game developer").center(80))
    print(config.get("configGame", "discord name").center(80))
    print("="*60).center(80)
    portList = []
    portBugs = []
    for port in [44440, 44444, 5555, 3724, 6112]:
        try:
            reactor.listenTCP(port, S)
            portList.append(port)
        except:
            exit()
    print(str(portList)).center(80)
    print("="*60).center(80)

    print("[%s] %s Server Connected." %(time.strftime("%H:%M:%S"), config.get("configGame", "game.miceName")))
    print("[%s] %s Main Database Connected Succesfuly." %(time.strftime("%H:%M:%S"), config.get("configGame", "game.miceName")))
    print("[%s] %s Cafe Database Connected Succesfuly." %(time.strftime("%H:%M:%S"), config.get("configGame", "game.miceName")))
    print("[%s] %s Map List Database Connected Succesfuly." %(time.strftime("%H:%M:%S"), config.get("configGame", "game.miceName")))
    threading.Thread(target=reactor.run(), args=(False,)).start()
