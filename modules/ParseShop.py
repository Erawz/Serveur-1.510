#coding: utf-8
import binascii

from ByteArray import ByteArray
from Identifiers import Identifiers

class ParseShop:
    def __init__(gift, player, server):
        gift.client = player
        gift.server = player.server
        gift.Cursor = player.Cursor

    def getShopLength(gift):
        return 0 if gift.client.shopItems == "" else len(gift.client.shopItems.split(","))

    def checkUnlockShopTitle(gift):
        if gift.server.shopTitleList.has_key(gift.getShopLength()):
            title = gift.server.shopTitleList[gift.getShopLength()]
            gift.client.checkAndRebuildTitleList("shop")
            gift.client.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
            gift.client.sendCompleteTitleList()
            gift.client.sendTitleList()

    def checkAndRebuildBadges(gift):
        rebuild = False
        for badge in gift.server.shopBadges.items():
            if not gift.client.shopBadges.has_key(badge[0]) and gift.checkInShop(badge[0]):
                gift.client.shopBadges[str(badge[1])] = 0
                rebuild = True

        if rebuild:
            badges = gift.client.shopBadges
            gift.client.shopBadges = {}
            for badge, count in badges.items():
                if not gift.client.shopBadges.has_key(badge):
                    gift.client.shopBadges[badge] = count

##    def checkAndRebuildBadges(gift):
##        rebuild = False
##        for badge in gift.server.shopBadges.items():
##            if not badge[1] in gift.client.shopBadges and gift.checkInShop(badge[0]):
##                gift.client.shopBadges.append(str(badge[1]))
##                rebuild = True
##
##        if rebuild:
##            tempBadges = []
##            tempBadges.extend(gift.client.shopBadges)
##            gift.client.shopBadges = []
##            gift.client.shopBadgesCounts = {}
##            for badge in tempBadges:
##                if not badge in gift.client.shopBadges:
##                    gift.client.shopBadges.append(badge)
##
    def checkUnlockShopBadge(gift, itemID):
        if not gift.client.isGuest:
            if gift.server.shopBadges.has_key(itemID):
                unlockedBadge = gift.server.shopBadges[itemID]
                gift.sendUnlockedBadge(unlockedBadge)
                gift.checkAndRebuildBadges()

    def checkInShop(gift, checkItem):
        if not gift.client.shopItems == "":
            for shopItem in gift.client.shopItems.split(","):
                if checkItem == int(shopItem.split("_")[0] if "_" in shopItem else shopItem):
                    return True
        else:
            return False

    def checkInShamanShop(gift, checkItem):
        if not gift.client.shamanItems == "":
            for shamanItems in gift.client.shamanItems.split(","):
                if checkItem == int(shamanItems.split("_")[0] if "_" in shamanItems else shamanItems):
                    return True
        else:
            return False

    def checkInPlayerShop(gift, type, playerName, checkItem):
        gift.Cursor.execute("select %s from Users where Username = %s" %(type), [playerName])
        for rs in gift.Cursor.fetchall():
            items = rs[type]
            if not items == "":
                for shopItem in items.split(","):
                    if checkItem == int(shopItem.split("_")[0] if "_" in shopItem else shopItem):
                        return True
            else:
                return False

    def getItemCustomization(gift, checkItem, isShamanShop):
        items = gift.client.shamanItems if isShamanShop else gift.client.shopItems
        if not items == "":
            for shopItem in items.split(","):
                itemSplited = shopItem.split("_")
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                if int(itemSplited[0]) == checkItem:
                    return "" if custom == "" else ("_" + custom)
        else:
            return ""

    def getShamanItemCustom(gift, code):
        item = gift.client.shamanItems.split(",")
        if "_" in item:
            itemSplited = item.split("_")
            custom = (itemSplited[1] if len(itemSplited) >= 2 else "").split("+")
            if int(itemSplited[0]) == code:
                packet = ByteArray().writeByte(len(custom))
                x = 0
                while x < len(custom):
                    packet.writeInt(int(custom[x], 16))
                    x += 1
                return packet.toByteArray()
        return chr(0)

    def getShopItemPrice(gift, fullItem):
        itemCat = (0 if fullItem / 10000 == 1 else fullItem / 10000) if fullItem > 9999 else fullItem / 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        return gift.getItemPromotion(itemCat, item, gift.server.shopListCheck[str(itemCat) + "|" + str(item)][1])
                
    def getShamanShopItemPrice(gift, fullItem):
        return gift.server.shamanShopListCheck[str(fullItem)][1]

    def getItemPromotion(gift, itemCat, item, price):
        for promotion in gift.server.shopPromotions:
            if promotion[0] == itemCat and promotion[1] == item:
                return int(promotion[2] / 100.0 * price)
        return price

    def sendShopList(gift):
        gift.sendShopList(True)

    def sendShopList(gift, sendItems=True):
        shopItems = [] if gift.client.shopItems == "" else gift.client.shopItems.split(",")

        packet = ByteArray().writeInt(gift.client.shopCheeses).writeInt(gift.client.shopFraises).writeUTF(gift.client.playerLook).writeInt(len(shopItems))
        for item in shopItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")

                packet.writeByte(len(realCustom)+1).writeInt(int(realItem))

                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeByte(0).writeInt(int(item))

        shop = gift.server.shopList if sendItems else []
        packet.writeInt(len(shop))

        for item in shop:
            value = item.split(",")
            packet.writeShort(int(value[0])).writeShort(int(value[1])).writeByte(int(value[2])).writeByte(int(value[3])).writeByte(int(value[4])).writeInt(int(value[5])).writeInt(int(value[6])).writeShort(0)
                
        visuais = gift.server.newVisuList
        packet.writeByte(len(visuais))
        i = len(visuais)
        for visual in visuais.items():
            packet.writeShort(visual[0])
            a = visual[1]
            packet.writeUTF("".join(a))
            packet.writeByte(visual[2])
            i -= 1

        packet.writeShort(len(gift.client.clothes))

        for clothe in gift.client.clothes:
            clotheSplited = clothe.split("/")
            packet.writeUTF(clotheSplited[1] + ";" + clotheSplited[2] + ";" + clotheSplited[3])    

        shamanItems = [] if gift.client.shamanItems == "" else gift.client.shamanItems.split(",")
        packet.writeShort(len(shamanItems))

        for item in shamanItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")

                packet.writeShort(int(realItem))

                packet.writeBoolean(item in gift.client.shamanLook.split(",")).writeByte(len(realCustom)+1)

                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBoolean(item in gift.client.shamanLook.split(",")).writeByte(0)

        shamanShop = gift.server.shamanShopList if sendItems else []
        packet.writeShort(len(shamanShop))

        for item in shamanShop:
            value = item.split(",")
            packet.writeInt(int(value[0])).writeByte(int(value[1])).writeByte(int(value[2])).writeByte(int(value[3])).writeInt(int(value[4])).writeShort(int(value[5]))

        gift.client.sendPacket(Identifiers.send.Shop_List, packet.toByteArray())
             
    def sendShamanItems(gift):
        shamanItems = [] if gift.client.shamanItems == "" else gift.client.shamanItems.split(",")

        packet = ByteArray().writeShort(len(shamanItems))
        for item in shamanItems:
            if "_" in item:
                custom = item.split("_")[1] if len(item.split("_")) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")
                packet.writeShort(int(item.split("_")[0])).writeBoolean(item in gift.client.shamanLook.split(",")).writeByte(len(realCustom) + 1)
                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBoolean(item in gift.client.shamanLook.split(",")).writeByte(0)
        gift.client.sendPacket(Identifiers.send.Shaman_Items, packet.toByteArray())

    def sendLookChange(gift):
        try:
            p = ByteArray()
            look = gift.client.playerLook.split(";")
            p.writeByte(int(look[0]))

            for item in look[1].split(","):
                if "_" in item:
                    itemSplited = item.split("_")
                    realItem = itemSplited[0]
                    custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                    realCustom = [] if custom == "" else custom.split("+")
                    p.writeInt(int(realItem)).writeByte(len(realCustom))
                    x = 0
                    while x < len(realCustom):
                        p.writeInt(int(realCustom[x], 16))
                        x += 1
                else:
                    p.writeInt(int(item)).writeByte(0)

            p.writeInt(int(gift.client.mouseColor, 16))
            gift.client.sendPacket(Identifiers.send.Look_Change, p.toByteArray())
        except: pass

    def sendShamanLook(gift):
        items = ByteArray()

        count = 0        
        for item in gift.client.shamanLook.split(","):
            realItem = int(item.split("_")[0]) if "_" in item else int(item)
            if realItem != 0:
                items.writeShort(realItem)
                count += 1
        gift.client.sendPacket(Identifiers.send.Shaman_Look, ByteArray().writeShort(count).writeBytes(items.toByteArray()).toByteArray())

    def sendItemBuy(gift, fullItem):
        gift.client.sendPacket(Identifiers.send.Item_Buy, ByteArray().writeInt(fullItem).writeByte(1).toByteArray())

    def sendUnlockedBadge(gift, badge):
        gift.client.room.sendAll(Identifiers.send.Unlocked_Badge, ByteArray().writeInt(gift.client.playerCode).writeShort(badge).toByteArray())

    def sendGiftResult(gift, type, playerName):
        gift.client.sendPacket(Identifiers.send.Gift_Result, ByteArray().writeByte(type).writeUTF(playerName).writeByte(0).writeShort(0).toByteArray())

    def equipClothe(gift, packet):
        clotheID = packet.readByte()
        for clothe in gift.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                gift.client.playerLook = values[1]
                gift.client.mouseColor = values[2]
                gift.client.shamanColor = values[3]
                break
                
        gift.sendLookChange()
        gift.sendShopList(False)

    def saveClothe(gift, packet):
        clotheID = packet.readByte()
        for clothe in gift.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                values[1] = gift.client.playerLook
                values[2] = gift.client.mouseColor
                values[3] = gift.client.shamanColor
                gift.client.clothes[gift.client.clothes.index(clothe)] = "/".join(values)
                break

        gift.sendShopList(False)

    def sendShopInfo(gift):            
        gift.client.sendPacket(Identifiers.send.Shop_Info, ByteArray().writeInt(gift.client.shopCheeses).writeInt(gift.client.shopFraises).toByteArray())

    def equipItem(gift, packet):
        fullItem = packet.readInt()
        itemStr = str(fullItem)
        itemCat = (0 if fullItem / 10000 == 1 else fullItem /10000) if len(itemStr) > 4 else fullItem / 100
        item = int(itemStr[2 if len(itemStr) > 3 else 1:]) if len(itemStr) >= 3 else fullItem
        itemStr = str(item)

        equip = str(item) + gift.getItemCustomization(fullItem, False)

        lookList = gift.client.playerLook.split(";")
        lookItems = lookList[1].split(",")
        lookCheckList = lookItems[:]
        idx = 0
        while idx < len(lookCheckList):
            lookCheckList[idx] = lookCheckList[idx].split("_")[0] if "_" in lookCheckList[idx] else lookCheckList[idx]
            idx += 1

        if itemCat <= 10:
            if lookCheckList[itemCat] == itemStr:
                lookItems[itemCat] = "0"
            else:
                lookItems[itemCat] = str(equip)

        elif itemCat == 21:
            lookList[0] = "1"
            color = "bd9067" if item == 0 else "593618" if item == 1 else "8c887f" if item == 2 else "dfd8ce" if item == 3 else "4e443a" if item == 4 else "e3c07e" if item == 5 else "272220" if item == 6 else "78583a"
            gift.client.mouseColor = "78583a" if gift.client.mouseColor == color else color
        else:
            if lookList[0] == itemStr:
                lookList[0] = "1"
            else:
                lookList[0] = itemStr

        gift.client.playerLook = lookList[0] + ";" + ",".join(map(str, lookItems))
        gift.sendLookChange()
		
    def buyItem(gift, packet):
        fullItem, withFraises = packet.readInt(), packet.readBoolean()
        itemCat = ((fullItem - 10000) / 10000) if fullItem > 9999 else fullItem / 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        gift.client.shopItems += str(fullItem) if gift.client.shopItems == "" else "," + str(fullItem)
        price = gift.getItemPromotion(itemCat, item, gift.server.shopListCheck[str(itemCat) + "|" + str(item)][1 if withFraises else 0])
        if withFraises:
            gift.client.shopFraises -= price
        else:
            gift.client.shopCheeses -= price

        gift.sendItemBuy(fullItem)
        gift.sendShopList(False)
        gift.client.sendAnimZelda(0, fullItem)
        gift.checkUnlockShopTitle()
        gift.checkUnlockShopBadge(fullItem)

    def customItemBuy(gift, packet):
        fullItem, withFraises = packet.readInt(), packet.readBoolean()

        items = gift.client.shopItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        gift.client.shopItems = ",".join(items)
        if withFraises:
            gift.client.shopFraises -= 20
        else:
            gift.client.shopCheeses -= 2000

        if len(gift.client.custom) == 1:
            if not fullItem in gift.client.custom:
                gift.client.custom.append(fullItem)
        else:
            if not str(fullItem) in gift.client.custom:
                gift.client.custom.append(str(fullItem))
                
        gift.sendShopList(False)

    def customItem(gift, packet):
        fullItem, length = packet.readInt(), packet.readByte()
        custom = length
        customs = list()

        i = 0
        while i < length:
            customs.append(packet.readInt())
            i += 1

        items = gift.client.shopItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xffffff & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                gift.client.shopItems = ",".join(items)

                itemCat = (0 if fullItem / 10000 == 1 else fullItem / 10000) if fullItem > 9999 else fullItem / 100
                item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
                equip = str(item) + gift.getItemCustomization(fullItem, False)
                lookList = gift.client.playerLook.split(";")
                lookItems = lookList[1].split(",")

                if "_" in lookItems[itemCat]:
                    if lookItems[itemCat].split("_")[0] == str(item):
                        lookItems[itemCat] = equip
                                
                elif lookItems[itemCat] == str(item):
                    lookItems[itemCat] = equip
                gift.client.playerLook = lookList[0] + ";" + ",".join(lookItems)
                gift.sendShopList(False)
                gift.sendLookChange()
                break

    def buyShamanItem(gift, packet):
        fullItem, withFraises = packet.readShort(), packet.readBoolean()
        price = gift.server.shamanShopListCheck[str(fullItem)][1 if withFraises else 0]
        gift.client.shamanItems += str(fullItem) if gift.client.shamanItems == "" else "," + str(fullItem)

        if withFraises:
            gift.client.shopFraises -= price
        else:
            gift.client.shopCheeses -= price

        gift.sendShopList(False)
        gift.client.sendAnimZelda(1, fullItem)

    def equipShamanItem(gift, packet):
        fullItem = packet.readInt()
        item = str(fullItem) + gift.getItemCustomization(fullItem, True)
        itemStr = str(fullItem)
        itemCat = int(itemStr[:len(itemStr)-2])
        index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
        index -= 1
        lookItems = gift.client.shamanLook.split(",")

        if "_" in lookItems[index]:
            if lookItems[index].split("_")[0] == itemStr:
                lookItems[index] = "0"
            else:
                lookItems[index] = item

        elif lookItems[index] == itemStr:
            lookItems[index] = "0"
        else:
            lookItems[index] = item

        gift.client.shamanLook = ",".join(lookItems)
        gift.sendShamanLook()

    def customShamanItemBuy(gift, packet):
        fullItem, withFraises = packet.readShort(), packet.readBoolean()

        items = gift.client.shamanItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        gift.client.shamanItems = ",".join(items)
        if withFraises:
            gift.client.shopFraises -= 150
        else:
            gift.client.shopCheeses -= 4000
                
        gift.sendShopList(False)

    def customShamanItem(gift, packet):
        fullItem, length = packet.readShort(), packet.readByte()
        customs = []
        i = 0
        while i < length:
            customs.append(packet.readInt())
            i += 1

        items = gift.client.shamanItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xFFFFFF & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                gift.client.shamanItems = ",".join(items)

                item = str(fullItem) + gift.getItemCustomization(fullItem, True)
                itemStr = str(fullItem)
                itemCat = int(itemStr[len(itemStr)-2:])
                index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
                index -= 1
                lookItems = gift.client.shamanLook.split(",")

                if "_" in lookItems[index]:
                    if lookItems[index].split("_")[0] == itemStr:
                        lookItems[index] = item
                                
                elif lookItems[index] == itemStr:
                    lookItems[index] = item

                gift.client.shamanLook = ",".join(lookItems)
                gift.sendShopList()
                gift.sendShamanLook()
                break

    def buyClothe(gift, packet):
        clotheID, withFraises = packet.readByte(), packet.readBoolean()
        gift.client.clothes.append("%02d/%s/%s/%s" %(clotheID, "1;0,0,0,0,0,0,0,0,0,0,0", "78583a", "fade55" if gift.client.shamanSaves >= 1000 else "95d9d6"))
        if withFraises:
            gift.client.shopFraises -= 5 if clotheID == 0 else 50 if clotheID == 1 else 100
        else:
            gift.client.shopFraises -= 40 if clotheID == 0 else 1000 if clotheID == 1 else 2000 if clotheID == 2 else 4000

        gift.sendShopList(False)

    def sendGift(gift, packet):
        playerName, isShamanItem, fullItem, message = packet.readUTF(), packet.readBoolean(), packet.readShort(), packet.readUTF()
        if not gift.server.checkExistingUser(playerName):
            gift.sendGiftResult(1, playerName)
        else:
            player = gift.server.players.get(playerName)
            if player != None:
                if (player.parseShop.checkInShamanShop(fullItem) if isShamanItem else player.parseShop.checkInShop(fullItem)):
                    gift.sendGiftResult(2, playerName)
                else:
                    gift.server.lastGiftID += 1
                    player.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(gift.server.lastGiftID).writeUTF(gift.client.playerName).writeUTF(gift.client.playerLook).writeBoolean(isShamanItem).writeShort(fullItem).writeUTF(message).writeBoolean(False).toByteArray())
                    gift.sendGiftResult(0, playerName)
                    gift.server.shopGifts[gift.server.lastGiftID] = [gift.client.playerName, isShamanItem, fullItem]
                    gift.client.shopFraises -= gift.getShamanShopItemPrice(fullItem) if isShamanItem else gift.getShopItemPrice(fullItem)
                    gift.sendShopList()
            else:
                gifts = ""
                if (gift.checkInPlayerShop("ShamanItems" if isShamanItem else "ShopItems", playerName, fullItem)):
                    gift.sendGiftResult(2, playerName)
                else:
                    gift.Cursor.execute("select Gifts from Users where Username = %s", [playerName])
                    rs = gift.Cursor.fetchone()
                    gifts = rs[0]

                gifts += ("" if gifts == "" else "/") + binascii.hexlify("|".join(map(str, [gift.client.playerName, gift.client.playerLook, isShamanItem, fullItem, message])))
                gift.Cursor.execute("update Users set Gifts = %s where Username = %s", [gifts, playerName])
                gift.sendGiftResult(0, playerName)

    def giftResult(gift, packet):
        giftID, isOpen, message, isMessage = packet.readInt(), packet.readBoolean(), packet.readUTF(), packet.readBoolean()
        if isOpen:
            values = gift.server.shopGifts[int(giftID)]
            player = gift.server.players.get(str(values[0]))
            if player != None:
                player.sendLangueMessage("$DonItemRecu", gift.client.playerName)

            isShamanItem = bool(values[1])
            fullItem = int(values[2])
            if isShamanItem:
                gift.client.shamanItems += str(fullItem) if gift.client.shamanItems == "" else ",%s" %(fullItem)
                gift.sendShopList(False)
                gift.client.sendAnimZelda(1, fullItem)
            else:
                gift.client.shopItems += str(fullItem) if gift.client.shopItems == "" else ",%s" %(fullItem)
                gift.client.sendAnimZelda(0, fullItem)
                gift.checkUnlockShopTitle()
                gift.checkUnlockShopBadge(fullItem)

        elif not message == "":
            values = gift.server.shopGifts[int(giftID)]
            player = gift.server.players.get(str(values[0]))
            if player != None:
                player.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(giftID).writeUTF(gift.client.playerName).writeUTF(gift.client.playerLook).writeBoolean(bool(values[1])).writeShort(int(values[2])).writeUTF(message).writeBoolean(True).toByteArray())
            else:
                messages = ""
                gift.Cursor.execute("select Messages from Users where Username = %s", [str(values[0])])
                rs = gift.Cursor.fetchone()
                messages = rs[0]

                messages += ("" if messages == "" else "/") + binascii.hexlify("|".join(map(str, [gift.client.playerName, gift.client.playerLook, values[1], values[2], message])))
                gift.Cursor.execute("update Users set Messages = %s where Username = %s", [messages, str(values[0])])

    def checkGiftsAndMessages(gift, lastReceivedGifts, lastReceivedMessages):
        needUpdate = False
        gifts = lastReceivedGifts.split("/")
        for gift in gifts:
            if not gift == "":
                values = binascii.unhexlify(gift).split("|", 4)
                gift.server.lastGiftID += 1
                gift.client.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(gift.server.lastGiftID).writeUTF(values[0]).writeUTF(values[1]).writeBoolean(bool(values[2])).writeShort(int(values[3])).writeUTF(values[4] if len(values) > 4 else "").writeBoolean(False).toByteArray())
                gift.server.shopGifts[gift.server.lastGiftID] = [values[0], bool(values[2]), int(values[3])]
                needUpdate = True

        messages = lastReceivedMessages.split("/")
        for message in messages:
            if not message == "":
                values = binascii.unhexlify(message).split("|", 4)
                gift.client.sendPacket(Identifiers.send.Shop_GIft_Message, ByteArray().writeShort(0).writeShort(0).writeUTF(values[0]).writeBoolean(bool(values[1])).writeShort(int(values[2])).writeUTF(values[4]).writeUTF(values[3]).writeBoolean(True).toByteArray())
                needUpdate = True

        if needUpdate:
            gift.Cursor.execute("update Users set Gifts = '', Messages = '' where Username = %s", [gift.client.playerName])
