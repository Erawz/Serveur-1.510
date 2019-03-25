# -*- coding: cp1252 -*-
import json
class AntiCheat:
    def __init__(gift, client, server):
        gift.client = client
        gift.server = client.server
        
    def update(self):
        ac = ("[F.A.C] ")
        gift.ac_config = open('./cheat/anticheat_config.txt', 'r').read()
        gift.ac_c = json.loads(gift.ac_config)
        gift.learning = gift.ac_c['learning']
        gift.bantimes = gift.ac_c['ban_times']
        gift.s_list = open('./cheat/anticheat_allow', 'r').read()
        if gift.s_list != "":
            gift.s_list = gift.s_list.split(',')
            gift.s_list.remove("")
        else: gift.s_list = []
            
    def readPacket(gift, packet, pd=None):
        ac = ("[R.A.C] ")
        if packet == " " or packet == "":
            gift.list.remove(packet)
        if str(packet) not in gift.server.s_list and str(packet) != "":
            if gift.server.learning == "true":
                gift.server.sendStaffMessage(4, "<V>[Anti-Hack] J'ai trouvé un nouveau hack venant de "+gift.client.playerName+" ["+str(packet)+"]")
                gift.server.s_list.append(str(packet))
                w = open('./cheat/anticheat_allow', 'a')
                w.write(str(packet) + ",")
                w.close()
            else:
                if gift.client.privLevel != 15:
                    if packet == 55 or packet == 31 or packet == 51:
                        gift.client.dac += 1
                        gift.server.sendStaffMessage(5, "<ROSE>[Anti-Hack]<V> Le joueur <J> "+ gift.client.playerName +" <V> est soupçonné d'avoir triché! <J>"+str(3-gift.client.dac)+" <V> alerteChère il sera banni automatiquement.")
                        gift.client.sendMessage("<V>Chère <J> "+ gift.client.playerName +" <V>, nous avons détecté Cheat Engine sur votre standalone, veuillez le désactiver ou il sera banni en quelques secondes.")
                    else: gift.client.dac = 3
                    if gift.client.dac >= 0 and gift.client.dac <= 2:
                        gift.client.dac += 1
                    else:
                        bans_done = 0
                        bl = open('./cheat/anticheat_bans.txt', 'r').read()
                        lista = bl.split('=')
                        lista.remove("")
                        for listas in lista:
                            data = listas.split(" ")
                            data.remove("")
                            name = data[1]
                            if name == gift.client.playerName:
                                bans_done += 1
                        if bans_done == 0:
                            tb = int(gift.server.bantimes)
                        elif bans_done == 1:
                            tb = int(gift.server.bantimes)*2
                        elif bans_done == 2:
                            tb = int(gift.server.bantimes)*3
                        elif bans_done >= 3:
                            tb = int(gift.server.bantimes)*4
                        if int(packet) == 31:
                            info = "Fly hack"
                        elif int(packet) == 51 or int(packet) == 55:
                            info = "Speed"
                        else: info = "Unknown"
                            
                        bans_done += 1
                        x = open('./cheat/anticheat_bans.txt', 'a')
                        x.write("= Player: "+ gift.client.playerName +" | Time: "+ str (tb) +" time (s) | Banned by: "+ str (packet) +" | Date: "+ info +" | + Info: "+ repr (pd) +"\n")
                        x.close()
                        gift.server.sendStaffMessage(5, "<V>[Anti-Hack]<J> Le Joueur "+ gift.client.playerName +" a été ban pour triche pendant "+ str (tb) +" temps (s). ["+ info +"]")
                        if int(packet) == 51 or int(packet) == 55 or int(packet) == 31:
                            gift.server.banPlayer(gift.client.playerName, int(tb), "Cheat Engine détecté [Ban #"+str(bans_done)+" - "+info+"]", "Anti-Hack", False)
                        else: gift.server.banPlayer(gift.client.playerName, 0, "Activité suspectée détectée [Ban #"+str(bans_done)+" - "+info+"]", "Anti-Hack", False)
                else:
                    if int(packet) == 31:
                        info = "Fly hack"
                    elif int(packet) == 51 or int(packet) == 55:
                        info = "Speed"
                    else: info = "Unknown"
                    gift.client.dac += 1
