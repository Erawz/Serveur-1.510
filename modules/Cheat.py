# -*- coding: cp1252 -*-
import json
class AntiCheat:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        
    def update(this):
        ac = ("[F.A.C] ")
        this.ac_config = open('./cheat/anticheat_config.txt', 'r').read()
        this.ac_c = json.loads(this.ac_config)
        this.learning = this.ac_c['learning']
        this.bantimes = this.ac_c['ban_times']
        this.s_list = open('./cheat/anticheat_allow', 'r').read()
        if this.s_list != "":
            this.s_list = this.s_list.split(',')
            this.s_list.remove("")
        else:
            this.s_list = []
            
    def readPacket(this, packet, pd=None):
        #print "Player: %s Packet: %s" %(this.client.Username, int(packet))
        ac = ("[R.A.C] ")
        if packet == " " or packet == "":
            this.list.remove(packet)
        if str(packet) not in this.server.s_list and str(packet) != "":
            if this.server.learning == "true":
                this.server.sendStaffMessage(5, "<V>[ANT-HACK] J'ai trouvé un nouveau colis venant de "+this.client.Username+" ["+str(packet)+"]")
                this.server.s_list.append(str(packet))
                w = open('./cheat/anticheat_allow', 'a')
                w.write(str(packet) + ",")
                w.close()
            else:
                if this.client.privLevel < 10:
                    if packet == 55 or packet == 31 or packet == 51 or packet == 23:
                        this.client.dac += 1
                        this.server.sendStaffMessage(5, "<ROSE>[ANT-HACK]<V> Le Joueur <J>"+this.client.Username+" <V>est soupçonné de hack! <J>"+str(3-this.client.dac)+" <V>alertes il sera banni automatiquement.")
                        this.client.sendMessage("<V>Cher, <J>"+this.client.Username+"<V>, nous avons détecté un Hack dans votre jeu, veuillez le désactiver ou il sera banni dans quelques secondes.")
                    else:
                        this.client.dac = 3
                    if this.client.dac >= 0 and this.client.dac <= 2:
                        this.client.dac += 1
                    else:
                        bans_done = 0
                        bl = open('./cheat/anticheat_bans.txt', 'r').read()
                        lista = bl.split('|')
                        lista.remove("")
                        for listas in lista:
                            data = listas.split(" ")
                            data.remove("")
                            name = data[1]
                            if name == this.client.Username:
                                bans_done += 1
                        if bans_done == 0:
                            tb = int(this.server.bantimes)
                        elif bans_done == 1:
                            tb = int(this.server.bantimes)*2
                        elif bans_done == 2:
                            tb = int(this.server.bantimes)*3
                        elif bans_done >= 3:
                            tb = int(this.server.bantimes)*4
                        if int(packet) == 31:
                            info = "Fly"
                        elif int(packet) == 51 or int(packet) == 55:
                            info = "Speed"
                        elif int(packet) == 23:
                            info = "Auto-Win"
                        else:
                            info = "Unknown"
                            
                        bans_done += 1
                        x = open('./cheat/anticheat_bans.txt', 'a')
                        x.write("| Joueur: "+this.client.Username+" | Temps: "+str(tb)+" heure(s) | Banni pour: "+str(packet)+" | Data: "+info+" | +Info: "+repr(pd)+" |\n")
                        x.close()
                        this.server.sendStaffMessage(5, "<V>[ANT-HACK]<J> Le Joueur "+this.client.Username+" a été banni pour l'utilisation de hack pendant "+str(tb)+" heure(s). ["+info+"]")
                        if int(packet) == 51 or int(packet) == 55 or int(packet) == 31 or int(packet) == 23:
                            this.server.banPlayer(this.client.Username, int(tb), "Hack détecté [Ban #"+str(bans_done)+" - "+info+"]", "ANT-HACK", False, 0)
                        else:
                            this.server.banPlayer(this.client.Username, 0, "Activité suspecte détectée [Ban #"+str(bans_done)+" - "+info+"]", "ANT-HACK", False, 0)
                else:
                    if int(packet) == 31:
                        info = "Fly"
                    elif int(packet) == 51 or int(packet) == 55:
                        info = "Speed"
                    elif int(packet) == 23:
                        info = "Auto-Win"
                    else:
                        info = "Unknown"
                    this.client.dac += 1
