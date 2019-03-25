#coding: utf-8
import time, random, thread, urllib2, smtplib

# Library
from twisted.internet import reactor

# Modules
from ByteArray import ByteArray

# Utils
from utils import *

class config:
    def __init__(gift, client, server):
        gift.client = client
        gift.server = client.server
        currentPage = 1

    def close(gift):
        i = 10000
        while i <= 12000:
            gift.client.room.removeTextArea(i, gift.client.Username)
            i += 1
        gift.client.sendMenu()

    def close2(gift):
        i = 10000
        while i <= 12000:
            gift.client.room.removeTextArea(i, gift.client.Username)
            i += 1

    def closeFFARaceInformation(gift):
        i = 150
        while i <= 300:
            gift.client.room.removeTextArea(i, gift.client.Username)
            i += 1
        gift.client.sendMenu()
        gift.client.removeImage(1)

    def closeoption(gift):
        i = 10004
        while i <= 10005:
            gift.client.room.removeTextArea(i, gift.client.Username)
            i += 1

    def open(gift):
        gift.close2()
        text = "<p align=\'center\'><font size=\'20\' color=\'#990000\'>Configurações do seu jogo</font></p>"
        text += "\n<font size=\'18\'>-</font> <font size=\'13\'><a href=\'event:config:personalizacao\'>Personalização</a></font>"
        gift.client.room.addTextArea(10002, str(text), gift.client.Username, 64, 46, 680, 320, 0x000000, 0x313131, 95, False)
        gift.client.room.addTextArea(10003, "<font size=\'28\' color=\'#990000\'><a href=\'event:config:close\'>X</a></font>", gift.client.Username, 754, 40, 50, 50, 0, 0, 0, False)

    def options(gift, id=0, option1="", option2="", option3="", option4="", option5=""):
        id = "Cor do nome <J>(VIP)</J>" if id == 1 else "Música" if id == 2 else ""
        opt = "Escolha uma das opções abaixo: "+str(id)+"\n"
        opt += "\n<font size=\'18\'>-</font> <font size=\'13\'>"+str(option1)+"</font>" if option1 != "" else ""
        opt += "\n<font size=\'18\'>-</font> <font size=\'13\'>"+str(option2)+"</font>" if option2 != "" else ""
        opt += "\n<font size=\'18\'>-</font> <font size=\'13\'>"+str(option3)+"</font>" if option3 != "" else ""
        opt += "\n<font size=\'18\'>-</font> <font size=\'13\'>"+str(option4)+"</font>" if option4 != "" else ""
        opt += "\n<font size=\'18\'>-</font> <font size=\'13\'>"+str(option5)+"</font>" if option5 != "" else ""
        gift.client.room.addTextArea(10004, str(opt), gift.client.Username, 280, 150, 260, 140, 0x000000, 0xFFFFFF, 95, False)
        gift.client.room.addTextArea(10005, "<font size=\'28\' color=\'#990000\'><a href=\'event:config:closeoption\'>X</a></font>", gift.client.Username, 548, 146, 50, 50, 0, 0, 0, False)

    def personalizationopen(gift):
        text = "<p align=\'center\'><font size=\'20\' color=\'#990000\'>Personalize seu jogo</font></p>"
        text += "\n<font size=\'18\'>-</font> <font size=\'13\'><a href=\'event:config:colormouse\'>Cor do rato</a></font>"
        text += "\n<font size=\'18\'>-</font> <font size=\'13\'><a href=\'event:config:colornick\'>Cor do nome <J>(VIP)</J></a></font>"
        gift.client.room.addTextArea(10006, str(text), gift.client.Username, 420, 94, 300, 240, 0x000000, 0x313131, 95, False)

    def musicName(gift, enable = 1):
        music = ""
        if enable == 0:
            gift.client.room.removeTextArea(15000, gift.client.Username)
            gift.client.musicName = 0
        else:
            if gift.client.musicOn == 1:
                if gift.client.musicNameLink != "" and gift.client.musicName == 1:
                    try:
                        gift.client.room.removeTextArea(15000, gift.client.Username)
                        music = urllib2.urlopen(gift.client.musicNameLink).read()
                        gift.client.room.addTextArea(15000, "<font face=\'Arial\'>"+str(music)+"</font>", gift.client.Username, 6, 379, 274, 18, 0x000000, 0x313131, 68, False)
                        reactor.callLater(30, gift.musicName)
                    except Exception as e:
                        gift.client.sendLangueMessage("", "<R>Mauvaise connexion ou erreur système ...")
                else:
                    gift.client.room.removeTextArea(15000, gift.client.Username)
                    gift.client.musicNameLink = ""
                    gift.client.musicName = 0
                    gift.musicName(0)
            else:
                pass
                #gift.client.sendMessage("<R>Ligue a rádio para usar essa função.")

    def FFARaceHelp(gift, id):
        if id == 0:
            gift.close2()
            gift.closeFFARaceInformation()
            gift.client.room.addTextArea(150, "", gift.client.Username, 160, 168, 480, 108, 3294800, 2570047, 100, False)
            gift.client.room.addTextArea(151, "", gift.client.Username, 155, 150, 490, 13, 2570047, 2570047, 100, False)
            gift.client.room.addTextArea(152, "<V><b><font size=\'15\'>FFA Race Help</font></b>", gift.client.Username, 155, 145, 465, 0, 0x000000, 0x000000, 100, False)
            gift.client.room.addTextArea(153, "", gift.client.Username, 635, 152, 8, 8, 40349, 40349, 100, False)
            gift.client.room.addTextArea(154, "<p align=\'center\'><font size=\'14\' color=\'#324650\'><b><a href=\'event:ffarace:close\'>X", gift.client.Username, 627, 146, 25, 25, 0x000000, 0x000000, 100, False)

            # About
            gift.client.room.addTextArea(155, "", gift.client.Username, 168, 252, 100, 13, 6590372, 6590372, 100, False)
            gift.client.room.addTextArea(156, "", gift.client.Username, 172, 254, 100, 13, 1185564, 1185564, 100, False)
            gift.client.room.addTextArea(157, "", gift.client.Username, 170, 253, 100, 13, 3952740, 3952740, 100, False)
            gift.client.room.addTextArea(158, "<p align=\'center\'><a href=\'event:ffarace:newHelp1\'>About", gift.client.Username, 170, 251, 100, 0, 0x000000, 0x000000, 100, False)
            gift.client.room.addTextArea(159, "", gift.client.Username, 170, 180, 100, 55, 3952740, 2570047, 100, False)

            # How To Play
            gift.client.room.addTextArea(160, "", gift.client.Username, 289, 252, 100, 13, 6590372, 6590372, 100, False)
            gift.client.room.addTextArea(161, "", gift.client.Username, 291, 254, 100, 13, 1185564, 1185564, 100, False)
            gift.client.room.addTextArea(162, "", gift.client.Username, 290, 253, 100, 13, 3952740, 3952740, 100, False)
            gift.client.room.addTextArea(163, "<p align=\'center\'><a href=\'event:ffarace:newHelp2\'>How To Play", gift.client.Username, 290, 251, 100, 0, 0x000000, 0x000000, 100, False)
            gift.client.room.addTextArea(164, "", gift.client.Username, 290, 180, 100, 55, 3952740, 2570047, 100, False)

            # Commands
            gift.client.room.addTextArea(165, "", gift.client.Username, 409, 252, 100, 13, 6590372, 6590372, 100, False)
            gift.client.room.addTextArea(166, "", gift.client.Username, 411, 254, 100, 13, 1185564, 1185564, 100, False)
            gift.client.room.addTextArea(167, "", gift.client.Username, 410, 253, 100, 13, 3952740, 3952740, 100, False)
            gift.client.room.addTextArea(168, "<p align=\'center\'><a href=\'event:ffarace:newHelp3\'>Commands", gift.client.Username, 410, 251, 100, 0, 0x000000, 0x000000, 100, False)
            gift.client.room.addTextArea(169, "", gift.client.Username, 410, 180, 100, 55, 3952740, 2570047, 100, False)

            # Updates
            gift.client.room.addTextArea(170, "", gift.client.Username, 529, 252, 100, 13, 6590372, 6590372, 100, False)
            gift.client.room.addTextArea(171, "", gift.client.Username, 531, 254, 100, 13, 1185564, 1185564, 100, False)
            gift.client.room.addTextArea(172, "", gift.client.Username, 530, 253, 100, 13, 3952740, 3952740, 100, False)
            gift.client.room.addTextArea(173, "<p align=\'center\'><a href=\'event:ffarace:newHelp4\'>Updates", gift.client.Username, 530, 251, 100, 0, 0x000000, 0x000000, 100, False)
            gift.client.room.addTextArea(174, "", gift.client.Username, 530, 180, 100, 55, 3952740, 2570047, 100, False)

            gift.client.sendPacket([29, 19], "\x00\x00\x00\x01\x00\x0b2e0YbYf.png\x07\x00\x00\x00\x01\x00\xa0\x00\xb1")

        if id == 1:
            gift.closeFFARaceInformation()
            gift.client.room.addTextArea(175, "", gift.client.Username, 200, 65, 400, 300, 3294800, 2570047, 100, False)
            gift.client.room.addTextArea(176, "", gift.client.Username, 195, 60, 410, 12, 2570047, 2570047, 100, False)
            gift.client.room.addTextArea(177, "<V><b><font size=\'15\'>About</font></b>", gift.client.Username, 195, 55, 385, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(178, "", gift.client.Username, 595, 62, 8, 8, 40349, 40349, 100, False)
            gift.client.room.addTextArea(179, "<p align=\'center\'><font size=\'17\' color=\'#324650\'><b><a href=\'event:ffarace:close\'>X", gift.client.Username, 591, 53, 0, 0, 0, 0, 0, False)
            gift.client.sendPacket([29, 20], ByteArray().writeInt(180).writeUTF("gift minigame was created by <J>Kmlcan <N>& <J>Recorvert<N>, on 3rd of October, 2013. Recorvert told Kmlcan his minigame idea about mice trying to race around the map with the cannonballs, Kmlcan liked the idea, then they started to code it. They had many problems because they were not professional at Lua. A couple people from Lua team said that gift minigame won\'t be approven, so they stopped working on it.\n\nOne day Kmlcan decided to remake gift marvelous minigame as he was much better at Lua scripting than before. He tried to add so many stuff because \'just racing\' was not too interesting. He added profiles, and a little leaderboard. The style of the minigame was completely changed, and it was so much better than the old version.\n\nFor more information, please visit <VP><a href=\'event:ffarace:thread2\'>gift page</a><N>.").writeShort(200).writeShort(78).writeShort(400).writeShort(300).writeInt(3294800).writeInt(2570047).writeShort(0).writeBool(True).toByteArray())
            gift.client.room.addTextArea(181, "", gift.client.Username, 489, 342, 100, 13, 6590372, 6590372, 100, False)
            gift.client.room.addTextArea(182, "", gift.client.Username, 491, 344, 100, 13, 1185564, 1185564, 100, False)
            gift.client.room.addTextArea(183, "", gift.client.Username, 490, 343, 100, 13, 3952740, 3952740, 100, False)
            gift.client.room.addTextArea(184, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 201, 350, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(185, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 199, 350, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(186, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 200, 351, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(187, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 200, 349, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(188, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 201, 349, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(189, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 199, 349, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(190, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 201, 351, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(191, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 199, 351, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(192, "<font size=\'9\'>v3.7.2", gift.client.Username, 200, 350, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(193, "<p align=\'center\'><a href=\'event:ffarace:newHelp0\'>Go Back", gift.client.Username, 490, 341, 100, 0, 0, 1, 0, False)

        if id == 2:
            gift.closeFFARaceInformation()
            gift.client.room.addTextArea(175, "", gift.client.Username, 200, 65, 400, 300, 3294800, 2570047, 100, False)
            gift.client.room.addTextArea(176, "", gift.client.Username, 195, 60, 410, 12, 2570047, 2570047, 100, False)
            gift.client.room.addTextArea(177, "<V><b><font size=\'15\'>How To Play</font></b>", gift.client.Username, 195, 55, 385, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(178, "", gift.client.Username, 595, 62, 8, 8, 40349, 40349, 100, False)
            gift.client.room.addTextArea(179, "<p align=\'center\'><font size=\'17\' color=\'#324650\'><b><a href=\'event:ffarace:close\'>X", gift.client.Username, 591, 53, 0, 0, 0, 0, 0, False)
            gift.client.sendPacket([29, 20], ByteArray().writeInt(180).writeUTF("<VP><b>Firing cannons</b>\n<N>To fire cannonballs, press <J>SPACE<N> or <J>duck<N>! The cannonball will be fired to the direction you\'re looking at.\n\n<VP><b>Earning FFARPs</b>\n<N>FFARP is the currency of FFA Race, you can earn these by getting firsts. And with the FFARPs you can buy some cool cannon styles for yourself!\n\n<VP><b>Anti FFA grounds</b>\n<N>Anti FFA grounds are the gray grounds within the map. If you\'re inside these grounds, you are not able to fire cannons. So, be careful!\n\n<VP><b>Making maps</b>\n<N>If you\'ve made a map, you can send it <J><a href=\'event:ffarace:thread3\'>here</a><N>.").writeShort(200).writeShort(78).writeShort(400).writeShort(300).writeInt(3294800).writeInt(2570047).writeShort(0).writeBool(True).toByteArray())
            gift.client.room.addTextArea(181, "", gift.client.Username, 489, 342, 100, 13, 6590372, 6590372, 100, False)
            gift.client.room.addTextArea(182, "", gift.client.Username, 491, 344, 100, 13, 1185564, 1185564, 100, False)
            gift.client.room.addTextArea(183, "", gift.client.Username, 490, 343, 100, 13, 3952740, 3952740, 100, False)
            gift.client.room.addTextArea(184, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 201, 350, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(185, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 199, 350, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(186, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 200, 351, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(187, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 200, 349, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(188, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 201, 349, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(189, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 199, 349, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(190, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 201, 351, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(191, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 199, 351, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(192, "<font size=\'9\'>v3.7.2", gift.client.Username, 200, 350, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(193, "<p align=\'center\'><a href=\'event:ffarace:newHelp0\'>Go Back", gift.client.Username, 490, 341, 100, 0, 0, 1, 0, False)

        if id == 3:
            gift.closeFFARaceInformation()
            gift.client.room.addTextArea(175, "", gift.client.Username, 200, 65, 400, 300, 3294800, 2570047, 100, False)
            gift.client.room.addTextArea(176, "", gift.client.Username, 195, 60, 410, 12, 2570047, 2570047, 100, False)
            gift.client.room.addTextArea(177, "<V><b><font size=\'15\'>Commands</font></b>", gift.client.Username, 195, 55, 385, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(178, "", gift.client.Username, 595, 62, 8, 8, 40349, 40349, 100, False)
            gift.client.room.addTextArea(179, "<p align=\'center\'><font size=\'17\' color=\'#324650\'><b><a href=\'event:ffarace:close\'>X", gift.client.Username, 591, 53, 0, 0, 0, 0, 0, False)
            gift.client.sendPacket([29, 20], ByteArray().writeInt(180).writeUTF("\n\n\n\n\n\n\n\n\n\n\n\n\n<VP><b>!challenge / !ch</b><N> Shows the challenge page.\n<VP><b>!off [x] [y]</b><N> Change your offsets.\n<VP><b>!stats [name]</b><N> Check specified player\'s stats.\n<VP><b>!top5 [mapcode]</b><N> Shows the best 5 times of specified map.\n<VP><b>!help</b><N> Shows gift menu.").writeShort(200).writeShort(78).writeShort(400).writeShort(300).writeInt(3294800).writeInt(2570047).writeShort(0).writeBool(True).toByteArray())
            gift.client.room.addTextArea(181, "", gift.client.Username, 489, 342, 100, 13, 6590372, 6590372, 100, False)
            gift.client.room.addTextArea(182, "", gift.client.Username, 491, 344, 100, 13, 1185564, 1185564, 100, False)
            gift.client.room.addTextArea(183, "", gift.client.Username, 490, 343, 100, 13, 3952740, 3952740, 100, False)
            gift.client.room.addTextArea(184, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 201, 350, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(185, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 199, 350, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(186, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 200, 351, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(187, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 200, 349, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(188, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 201, 349, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(189, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 199, 349, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(190, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 201, 351, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(191, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 199, 351, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(192, "<font size=\'9\'>v3.7.2", gift.client.Username, 200, 350, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(193, "<p align=\'center\'><a href=\'event:ffarace:newHelp0\'>Go Back", gift.client.Username, 490, 341, 100, 0, 0, 1, 0, False)

        if id == 4:
            gift.closeFFARaceInformation()
            gift.client.room.addTextArea(175, "", gift.client.Username, 200, 65, 400, 300, 3294800, 2570047, 100, False)
            gift.client.room.addTextArea(176, "", gift.client.Username, 195, 60, 410, 12, 2570047, 2570047, 100, False)
            gift.client.room.addTextArea(177, "<V><b><font size=\'15\'>Updates</font></b>", gift.client.Username, 195, 55, 385, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(178, "", gift.client.Username, 595, 62, 8, 8, 40349, 40349, 100, False)
            gift.client.room.addTextArea(179, "<p align=\'center\'><font size=\'17\' color=\'#324650\'><b><a href=\'event:ffarace:close\'>X", gift.client.Username, 591, 53, 0, 0, 0, 0, 0, False)
            gift.client.sendPacket([29, 20], ByteArray().writeInt(180).writeUTF("<J>[\xe2\x80\xa2] <N>Changed the challenge system.\n<J>[\xe2\x80\xa2] <N>Added challenge system and changed the profile a little bit. Removed records temporary.\n<J>[\xe2\x80\xa2] <N>Added <VP>Double FFA<N> grounds.\nAdded the last picture of the help, 4 new cannons. Records are now saving!\n<J>[\xe2\x80\xa2] <N>Added click mode and two new cannons.\n<J>[\xe2\x80\xa2] <N>Added one image on the commands page and language selection in tribe houses.\n<J>[\xe2\x80\xa2] <N>The help has been reformed.\n<J>[\xe2\x80\xa2] <N>Added two new cannons.\n<J>[\xe2\x80\xa2] <N>International FFA Race tournament was cancelled.\n<J>[\xe2\x80\xa2] <N>Added one new cannon.\n<J>[\xe2\x80\xa2] <N>All the admins have left the team.\n<J>[\xe2\x80\xa2] <N>Records and music mode added.\n<J>[\xe2\x80\xa2] <N>FFA Race has been recoded!\n<J>[\xe2\x80\xa2] <N>International FFA Race tournament was announced.").writeShort(200).writeShort(78).writeShort(400).writeShort(300).writeInt(3294800).writeInt(2570047).writeShort(0).writeBool(True).toByteArray())
            gift.client.room.addTextArea(181, "", gift.client.Username, 489, 342, 100, 13, 6590372, 6590372, 100, False)
            gift.client.room.addTextArea(182, "", gift.client.Username, 491, 344, 100, 13, 1185564, 1185564, 100, False)
            gift.client.room.addTextArea(183, "", gift.client.Username, 490, 343, 100, 13, 3952740, 3952740, 100, False)
            gift.client.room.addTextArea(184, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 201, 350, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(185, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 199, 350, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(186, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 200, 351, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(187, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 200, 349, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(188, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 201, 349, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(189, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 199, 349, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(190, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 201, 351, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(191, "<font color=\'#1\'><font size=\'9\'>v3.7.2", gift.client.Username, 199, 351, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(192, "<font size=\'9\'>v3.7.2", gift.client.Username, 200, 350, 100, 0, 0, 1, 0, False)
            gift.client.room.addTextArea(193, "<p align=\'center\'><a href=\'event:ffarace:newHelp0\'>Go Back", gift.client.Username, 490, 341, 100, 0, 0, 1, 0, False)

class ranking:
    def __init__(gift, client, server):
        gift.client = client
        gift.server = client.server
        currentPage = 1

    def close(gift):
        i = 10000
        while i <= 12000:
            gift.client.room.removeTextArea(i, gift.client.Username)
            i += 1
        gift.client.sendMenu()

    def close2(gift):
        i = 10000
        while i <= 12000:
            gift.client.room.removeTextArea(i, gift.client.Username)
            i += 1

    def open(gift):
        gift.close()
        gift.client.room.addTextArea(10002, "", gift.client.Username, 4, 25, 792, 410, 0x000008, 0x000000, 92, False)
        gift.client.room.addTextArea(10003, "<p align=\'center\'><font size=\'22\' family=\'Arial\' color=\'#BEBB56\'><a href=\'#\'><b>Ranking "+str(gift.server.miceName)+"</b></a></font></p>", gift.client.Username, 235, 27, 340, 45, 0, 0, 100, False)
        gift.client.room.addTextArea(10016, "<font size=\'23\' color=\'#990000\'><a href=\'event:ranking:close\'>X</a></font>", gift.client.Username, 762, 34, 50, 50, 0, 0, 0, False)

        # Firsts
        gift.client.room.addTextArea(10004, "<p align=\'center\'><font size=\'11\'><BV><b>Firsts</b></BV></font></p>", gift.client.Username, -82, 81, 340, 45, 0, 0, 100, False)
        gift.client.Cursor.execute("select Username, FirstCount from Users where PrivLevel < 7 ORDER By FirstCount DESC LIMIT 22")
        rs = gift.client.Cursor.fetchall()
        pos = 1
        text = ""
        count = ""
        gift.client.updateDatabase()
        for rrf in rs:
            posfirsts = "0"+str(pos) if pos <= 9 else pos
            playerName = str(rrf[0])
            firstCount = rrf[1]
            if pos == 1:
                text += "<font size=\'11\' color=\'#FADE55\'>"+str(posfirsts)+"</font> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            elif pos == 2:
                text += "<font size=\'11\' color=\'#EFEBE0\'>"+str(posfirsts)+"</font> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            elif pos == 3:
                text += "<font size=\'11\' color=\'#B44F0D\'>"+str(posfirsts)+"</font> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            else:
                text += "<font size=\'11\'><CH>"+str(posfirsts)+"</CH> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            count += "<V>"+str(firstCount)+"</V>\n"
            gift.client.room.addTextArea(10005, str(text), gift.client.Username, 8, 107, 340, 420, 0, 0, 100, False)
            gift.client.room.addTextArea(10006, str(count), gift.client.Username, 135, 107, 340, 420, 0, 0, 100, False)
            pos += 1

        # Queijos
        gift.client.room.addTextArea(10007, "<p align=\'center\'><font size=\'11\'><BV><b>Fromages</b></BV></font></p>", gift.client.Username, 117, 81, 340, 45, 0, 0, 100, False)
        gift.client.Cursor.execute("select Username, CheeseCount from Users where PrivLevel < 7 ORDER By CheeseCount DESC LIMIT 22")
        rs = gift.client.Cursor.fetchall()
        pos = 1
        text = ""
        count = ""
        gift.client.updateDatabase()
        for rrf in rs:
            poscheeses = "0"+str(pos) if pos <= 9 else pos
            playerName = str(rrf[0])
            cheeseCount = rrf[1]
            if pos == 1:
                text += "<font size=\'11\' color=\'#FADE55\'>"+str(poscheeses)+"</font> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            elif pos == 2:
                text += "<font size=\'11\' color=\'#EFEBE0\'>"+str(poscheeses)+"</font> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            elif pos == 3:
                text += "<font size=\'11\' color=\'#B44F0D\'>"+str(poscheeses)+"</font> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            else:
                text += "<font size=\'11\'><CH>"+str(poscheeses)+"</CH> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            count += "<V>"+str(cheeseCount)+"</V>\n"
            gift.client.room.addTextArea(10008, str(text), gift.client.Username, 203, 107, 340, 420, 0, 0, 100, False)
            gift.client.room.addTextArea(10009, str(count), gift.client.Username, 350, 107, 340, 420, 0, 0, 100, False)
            pos += 1

        # Saves
        gift.client.room.addTextArea(10010, "<p align=\'center\'><font size=\'11\'><BV><b>Saves</b></BV></font></p>", gift.client.Username, 333, 81, 340, 45, 0, 0, 100, False)
        gift.client.Cursor.execute("select Username, ShamanSaves from Users where PrivLevel < 7 ORDER By ShamanSaves DESC LIMIT 22")
        rs = gift.client.Cursor.fetchall()
        pos = 1
        text = ""
        count = ""
        gift.client.updateDatabase()
        for rrf in rs:
            possaves = "0"+str(pos) if pos <= 9 else pos
            playerName = str(rrf[0])
            savesCount = rrf[1]
            if pos == 1:
                text += "<font size=\'11\' color=\'#FADE55\'>"+str(possaves)+"</font> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            elif pos == 2:
                text += "<font size=\'11\' color=\'#EFEBE0\'>"+str(possaves)+"</font> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            elif pos == 3:
                text += "<font size=\'11\' color=\'#B44F0D\'>"+str(possaves)+"</font> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            else:
                text += "<font size=\'11\'><CH>"+str(possaves)+"</CH> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            count += "<V>"+str(savesCount)+"</V>\n"
            gift.client.room.addTextArea(10011, str(text), gift.client.Username, 427, 107, 340, 420, 0, 0, 100, False)
            gift.client.room.addTextArea(10012, str(count), gift.client.Username, 556, 107, 340, 420, 0, 0, 100, False)
            pos += 1

        # Bootcamps
        gift.client.room.addTextArea(10013, "<p align=\'center\'><font size=\'11\'><BV><b>Bootcamps</b></BV></font></p>", gift.client.Username, 517, 81, 340, 45, 0, 0, 100, False)
        gift.client.Cursor.execute("select Username, BootcampCount from Users where PrivLevel < 7 ORDER By BootcampCount DESC LIMIT 22")
        rs = gift.client.Cursor.fetchall()
        pos = 1
        text = ""
        count = ""
        gift.client.updateDatabase()
        for rrf in rs:
            posbootcamps = "0"+str(pos) if pos <= 9 else pos
            playerName = str(rrf[0])
            bootcampCount = rrf[1]
            if pos == 1:
                text += "<font size=\'11\' color=\'#FADE55\'>"+str(posbootcamps)+"</font> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            elif pos == 2:
                text += "<font size=\'11\' color=\'#EFEBE0\'>"+str(posbootcamps)+"</font> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            elif pos == 3:
                text += "<font size=\'11\' color=\'#B44F0D\'>"+str(posbootcamps)+"</font> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            else:
                text += "<font size=\'11\'><CH>"+str(posbootcamps)+"</CH> <V>-</V> "+str(playerName)+"</font>"
                text += "<br />"
            count += "<V>"+str(bootcampCount)+"</V>\n"
            gift.client.room.addTextArea(10014, str(text), gift.client.Username, 613, 107, 340, 420, 0, 0, 100, False)
            gift.client.room.addTextArea(10015, str(count), gift.client.Username, 749, 107, 340, 420, 0, 0, 100, False)
            pos += 1

class email:
    def __init__(gift, client, server):
        gift.client = client
        gift.server = client.server
        currentPage = 1

    def close(gift):
        i = 10000
        while i <= 12000:
            gift.client.room.removeTextArea(i, gift.client.Username)
            i += 1

    def openConfirmationBox(gift):
        gift.close()
        text = "<p align=\'center\'><font size=\'20\' color=\'#990000\'>Confirme seu endereço de email</font></p>"
        text += "\n<font size=\'15\'>Clique <a href=\'event:email:resend\'>aqui</a> para reenviar o código para seu endereço de email.</font>"
        text += "\n<font size=\'15\'>Para confirmar seu endereço de email:</font>"
        text += "\n<font size=\'13\'>1. Entre no email que você usou para criar sua conta.</font>"
        text += "\n<font size=\'13\'>2. Copie o código enviado para o seu email e digite na caixa de texto abaixo.</font>"
        text += "\n<font size=\'13\'>3. Pronto, desfrute dos nossos sistemas e seja feliz!</font>"
        gift.client.room.addTextArea(10002, str(text), gift.client.Username, 64, 46, 680, 128, 0x000000, 0x313131, 95, False)
        gift.client.room.addPopup(10004, 2, "Digite o código recebido em seu email!\n <center>Ex: B2HGDA87Y.</center>", gift.client.Username, 280, 181, 240, True)
        gift.client.room.addTextArea(10003, "<font size=\'28\' color=\'#990000\'><a href=\'event:email:close\'>X</a></font>", gift.client.Username, 754, 40, 50, 50, 0, 0, 0, False)

    def sendCode(gift):
        code = TFMUtils.getRandomChars(random.randint(8,10))
        gift.client.codeEmailConfirmation = str(code)

        # Credenciais
        remetente    = 'andrielkogama@gmail.com'
        senha        = 'andriel2004'

        # Informações da mensagem
        destinatario = str(gift.client.emailAddress)
        assunto      = "Confirme sua conta do \'+str(gift.server.miceName)"
        texto        = "Caro \'+str(gift.client.Username)+\', confirme sua conta do \'+str(gift.server.miceName)+\' usando o seguinte código abaixo: \n\'+str(code)+\' \nDivirta-se desfrutando de nossos sistemas!"

        # Preparando a mensagem
        msg = "\r\n".join([
          'From: %s' % remetente,
          'To: %s' % destinatario,
          'Subject: %s' % assunto,
          '',
          '%s' % texto
          ])

        # Enviando o email
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(remetente,senha)
        server.sendmail(remetente, destinatario, msg)
        server.quit()

        gift.client.sendMessage("<BL>Verifique seu endereço de email!")
        gift.client.updateDatabase()

class radios:
    def __init__(gift, client, server):
        gift.client = client
        gift.server = client.server
        gift.Cursor = client.Cursor
        currentPage = 1
        
    def open(gift):
        gift.client.room.addTextArea(13000, "<p align=\'center\'><img src=\'https://i.imgur.com/feG3iCj.png\' hspace=\'0\' vspace=\'-2\'>", gift.client.Username, 180, 15, 455, 370, 0, 0, 0, False)
        gift.client.room.addTextArea(13001, "<p align=\'center\'><N>Olá <J>"+str(gift.client.Username)+"</J>, bem-vindo ao reprodutor de músicas do "+str(gift.server.miceName)+"!", gift.client.Username, 220, 85, 420, 100, 0, 0, 0, False)
        gift.client.room.addTextArea(13002, "<p align=\'center\'><N>Todas as rádios estão em Português.", gift.client.Username, 220, 104, 350, 100, 0, 0, 0, False)
        gift.client.room.addTextArea(13003, "<p align=\'center\'><N>Desfrute do nosso sistema abaixo!", gift.client.Username, 220, 120, 350, 100, 0, 0, 0, False)
        gift.client.room.addTextArea(13004, "<p align=\'center\'><N>Escolha uma das opções de rádio acima.", gift.client.Username, 220, 345, 350, 100, 0, 0, 0, False)
        gift.client.room.addTextArea(13005, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>", gift.client.Username, 335, 130, 350, 100, 0, 0, 0, False)
        gift.client.room.addTextArea(13006, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>", gift.client.Username, 335, 165, 350, 100, 0, 0, 0, False)
        gift.client.room.addTextArea(13007, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>", gift.client.Username, 335, 200, 350, 100, 0, 0, 0, False)
        gift.client.room.addTextArea(13008, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>", gift.client.Username, 335, 235, 350, 100, 0, 0, 0, False)
        gift.client.room.addTextArea(13009, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>", gift.client.Username, 335, 270, 350, 100, 0, 0, 0, False)
        gift.client.room.addTextArea(13010, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>", gift.client.Username, 335, 305, 350, 100, 0, 0, 0, False)
        gift.client.room.addTextArea(13011, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>", gift.client.Username, 465, 285, 350, 100, 0, 0, 0, False)
        gift.client.room.addTextArea(13012, "<N><a href=\'event:config:music:funk\'>FUNK</a>", gift.client.Username, 377, 145, 50, 20, 0, 0, 0, False)
        gift.client.room.addTextArea(13013, "<N><a href=\'event:config:music:eletronica\'>ELETRÔNICA</a>", gift.client.Username, 356, 180, 100, 20, 0, 0, 0, False)
        gift.client.room.addTextArea(13014, "<N><a href=\'event:config:music:sertaneja\'>SERTANEJA</a>", gift.client.Username, 360, 215, 100, 20, 0, 0, 0, False)
        gift.client.room.addTextArea(13015, "<N><a href=\'event:config:music:rap\'>RAP</a>", gift.client.Username, 381, 250, 100, 20, 0, 0, 0, False)
        gift.client.room.addTextArea(13016, "<N><a href=\'event:config:music:pop\'>POP</a>", gift.client.Username, 381, 285, 100, 20, 0, 0, 0, False)
        gift.client.room.addTextArea(13017, "<N><a href=\'event:config:music:mix\'>MIX</a>", gift.client.Username, 381, 320, 100, 20, 0, 0, 0, False)
        gift.client.room.addTextArea(13018, "<N><a href=\'event:config:music:off\'>DESLIGAR</a>", gift.client.Username, 494, 300, 100, 23, 0, 0, 0, False)
        gift.client.room.addTextArea(13019, "<R><font size=\'14\'><b><a href=\'event:config:close2\'>X</a></b></font></R>", gift.client.Username, 192, 54, 34, 34, 0, 0, 0, False)
