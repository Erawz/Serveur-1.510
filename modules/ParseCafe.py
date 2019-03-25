#coding: utf-8
# Modules
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

class Cafe:
    def __init__(gift, player, server):
        gift.client = player
        gift.server = player.server
        gift.CursorCafe = player.server.CursorCafe
    
    def loadCafeMode(gift):
        can = gift.client.privLevel >= 1
        if not can:
            gift.client.sendLangueMessage("<ROSE>$PasAutoriseParlerSurServeur")
        gift.client.sendPacket(Identifiers.send.Open_Cafe, ByteArray().writeBoolean(can).toByteArray())

        packet = ByteArray()
        gift.CursorCafe.execute("select * from CafeTopics where Langue = ? order by Date desc limit 0, 20", [gift.client.langue])
        for rs in gift.CursorCafe.fetchall():
            packet.writeInt(rs["TopicID"]).writeUTF(rs["Title"]).writeInt(gift.server.getPlayerID(rs["Author"])).writeInt(rs["Posts"]).writeUTF(rs["LastPostName"]).writeInt(Utils.getSecondsDiff(rs["Date"]))
        gift.client.sendPacket(Identifiers.send.Cafe_Topics_List, packet.toByteArray())

    def openCafeTopic(gift, topicID):
        packet = ByteArray().writeBoolean(True).writeInt(topicID)
        gift.CursorCafe.execute("select * from CafePosts where TopicID = ? order by PostID asc", [topicID])
        for rs in gift.CursorCafe.fetchall():
            packet.writeInt(rs["PostID"]).writeInt(gift.server.getPlayerID(rs["Name"])).writeInt(Utils.getSecondsDiff(rs["Date"])).writeUTF(rs["Name"]).writeUTF(rs["Post"]).writeBoolean(str(gift.client.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"])
        gift.client.sendPacket(Identifiers.send.Open_Cafe_Topic, packet.toByteArray())

    def createNewCafeTopic(gift, title, message):
        gift.CursorCafe.execute("insert into CafeTopics values (null, ?, ?, '', 0, ?, ?)", [title, gift.client.playerName, Utils.getTime(), gift.client.langue])
        gift.createNewCafePost(gift.CursorCafe.lastrowid, message)
        gift.loadCafeMode()

    def createNewCafePost(gift, topicID, message):
        commentsCount = 0
        gift.CursorCafe.execute("insert into CafePosts values (null, ?, ?, ?, ?, 0, ?)", [topicID, gift.client.playerName, message, Utils.getTime(), gift.client.playerCode])
        gift.CursorCafe.execute("update CafeTopics set Posts = Posts + 1, LastPostName = ?, Date = ? where TopicID = ?", [gift.client.playerName, Utils.getTime(), topicID])
        gift.CursorCafe.execute("select count(*) as count from CafePosts where TopicID = ?", [topicID])
        rs = gift.CursorCafe.fetchone()
        commentsCount = rs["count"]
        gift.openCafeTopic(topicID)
        for player in gift.server.players.values():
            if player.isCafe:
                player.sendPacket(Identifiers.send.Cafe_New_Post, ByteArray().writeInt(topicID).writeUTF(gift.client.playerName).writeInt(commentsCount).toByteArray())

    def voteCafePost(gift, topicID, postID, mode):
        points = 0
        votes = ""

        gift.CursorCafe.execute("select Points, Votes from CafePosts where TopicID = ? and PostID = ?", [topicID, postID])
        rs = gift.CursorCafe.fetchone()
        if rs:
            points = rs["Points"]
            votes = rs["Votes"]

        votes += str(gift.client.playerCode) if votes == "" else "," + str(gift.client.playerCode)
        if mode:
            points += 2
        else:
            points -= 2

        gift.CursorCafe.execute("update CafePosts set Points = ?, Votes = ? where TopicID = ? and PostID = ?", [points, votes, topicID, postID])
        gift.openCafeTopic(topicID)

    def deleteCafePost(gift, topicID, postID):
        gift.CursorCafe.execute("delete from CafePosts where TopicID = ? and PostID = ?", [topicID, postID])
        gift.client.sendPacket(Identifiers.send.Delete_Cafe_Message, ByteArray().writeInt(topicID).writeInt(postID).toByteArray())
        gift.openCafeTopic(topicID)

    def deleteAllCafePost(gift, topicID, playerName):
        gift.CursorCafe.execute("delete from CafePosts where TopicID = ? and Name = ?", [topicID, playerName])
        gift.CursorCafe.execute("delete from CafeTopics where TopicID = ?", [topicID])
        gift.loadCafeMode()
        gift.openCafeTopic(topicID)
