#coding: utf-8
import struct, random, time as _time
from twisted.internet import reactor
from utils import Utils

class fullMenu:
    def __init__(gift, client, server):
        gift.client = client
        gift.server = client.server
        gift.Cursor = client.Cursor
        currentPage = 1
        
    def sendMenu(gift):
        if gift.client.privLevel >= 11:
            bg = ""
            text = "<a href='event:openPanel'><font size='15'><font color='#D9BA68'>PANEL</font></a>"
            gift.client.sendAddPopupText(11000, 745, 24, 58, 18, '0394AA', '0394AA', 100, str(bg))
            gift.client.sendAddPopupText(11001, 745, 24, 58, 20, 'B6A2C3', 'B6A2C3', 100, str(text))
