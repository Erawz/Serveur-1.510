#coding: utf-8
import re, base64, hashlib, urllib2, random, struct

from ByteArray import ByteArray
from Identifiers import Identifiers

class ParseCodeCmd:
    def __init__(gift, client, server):
        gift.client = client
        gift.server = client.server
        gift.Cursor = client.Cursor
        gift.currentArgsCount = 0
        
    def requireNoSouris(gift, playerName):
        if playerName.startswith("*"):
            pass
        else:
            return True

    def requireArgs(gift, argsCount):
        if gift.currentArgsCount < argsCount:
            gift.client.sendMessage("Invalid arguments.")
            return False

        return True

    def requireTribe(gift, canUse=False):
        if not gift.client.tribeName == "" and gift.client.room.isTribeHouse:
            tribeRankings = gift.client.tribeData[3]
            perm = tribeRankings[gift.client.tribeRank].split("|")[2]
            if perm.split(",")[8] == "1":
                canUse = True

    def parseCommandCode(gift, command):                
        values = command.split(" ")
        _command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        argsNotSplited = " ".join(args)
        gift.currentArgsCount = argsCount
        try:
            if command.startswith("codecadeau "):
                key = command.split(" ")[1].lower()
                if key == "291#4614818248#@sc4n3":
                    gift.client.sendMessage("You won 20 cheese")
                    gift.client.shopCheeses += 20
                if key == "testfraise":
                    gift.client.sendMessage("<font color='#F272A5'>You won 20 fraises</font")
                    gift.client.sendStaffMessage("<V>%s</V> vient d'utiliser le code %s." %(gift.client.playerName))
                    gift.client.shopFraises += 20    
                if key == "951#2954365943#@121@x":
                    gift.client.sendMessage("You won 20 fraises")
                    gift.client.shopFraises += 20
                if not key in ["291#4614818248#@sc4n3", "951#2954365943#@121@x", "testfraise"]:
                    gift.client.sendMessage("Code : "+str(key)+" est introuvable, gagner un code en événement ou rendez-vous sur notre Discord.")
        except Exception as ERROR:
            pass

   # def getCommandsList(gift):
        rank = "Player" if gift.client.privLevel == 1 else "VIP" if gift.client.privLevel == 2 else "Developer Lua" if gift.client.privLevel == 3 else "Helper" if gift.client.privLevel == 5 else "MapCrew" if gift.client.privLevel == 6 else "Modérateur" if gift.client.privLevel == 7 else "Super Modérateur" if gift.client.privLevel == 8 else "Coordinateur" if gift.client.privLevel == 9 else "Administrateur" if gift.client.privLevel == 10 else "Créateur" if gift.client.privLevel == 11 else ""
        message = rank + " commands:\n\n" 
        message += "<J>/profil</J> <V>[playerPartName]<BL> : Display player\'s info. (aliases: /profile, /perfil, /profiel)</BL>\n"
        message += "<J>/temps</J> <BL> : Affiche votre temps de jeu passé sur notre Serveur.</BL>"
        message += "<J>/avatar</J><BL> : Vous pouvez définir votre Avatar.</BL>\n"
        message += "<J>/cor</J><BL> : Vous donne la possibilité de changer la couleur de votre souris.</BL>\n"
        message += "<J>/mod</J><BL> : Affiche la liste de Modérateurs en ligne.</BL>\n"
        message += "<J>/mapcrew</J><BL> : Affiche la liste de Map Crews en ligne.</BL>\n"
        message += "<J>/funcorps</J><BL> : Affiche la liste de FunCorps en ligne.</BL>\n"
        message += "<J>/pw</J> <G>[password]<BL> : Permet au salon choisie d'être protégée par un mot de passe. Vous devez entrer votre pseudo avant le nom de la salle. Pour supprimer le mot de passe, entrez la commande sans rien.</BL>\n"
        message += "<J>/titre <G>[nombre]<BL> : Affiche tous vos titres débloqués. Tapez la commande suivi du numéro de titre pour changer votre titre.</BL>\n"
        message += "<J>/equipe</J><BL> : Affiche l'Équipe de BestMice</BL>\n"
        message += "<J>/about</J><BL> : Affiche quelques informations sur le Serveur</BL>\n"
        message += "<J>/mulodrome</J><BL> : Starts a new mulodrome.</BL>\n"
        message += "<J>/skip</J><BL> : Vote for the current song (the room \"music\") is skipped.</BL>\n"
        message += "<J>/mort</J><BL> : Votre souris meurt instantanément.</BL>\n"
        #message += "<J>/shop</J><BL> : Opens shop items.</BL>\n"
        #message += "<J>/vips</J><BL> : Shows VIP\'s list server.</BL>\n"
        message += "<J>/lsmap</J> "+("<G>[playerName] " if gift.client.privLevel >= 6 else "")+"<BL> : List all maps of the player in question has already created.</BL>\n"
        message += "<J>/info</J> <G>[mapCode]<BL> : Displays information about the current map or specific map, if placed the code.</BL>\n"
        message += "<J>/help</J><BL> : Server Command List. (aliases: /ajuda)</BL>\n"
        message += "<J>/ban</J> <V>[playerName]<BL> : It gives a vote of banishment to the player in question. After 5 votes he is banished from the room.</BL>\n"
        message += "<J>/colormouse</J> <G>[color|off]<BL> : Change the color of your mouse.</BL>\n"
        message += "<J>/trade</J> <V>[playerName]<BL> : Accesses exchange system inventory items with the player in question. You must be in the same room player.</BL>\n"
        message += "<J>/f</J> <G>[flag]<BL> : Balance the flag of the country in question.</BL>\n"
        message += "<J>/clavier</J><BL> : Toggles between English and French keyboard.</BL>\n"
        message += "<J>/colormouse</J> <V>[playerNames|*] [color|off]<BL> : Temporarily gives a colorized fur.</BL>\n"
        message += "<J>/friend</J> <V>[playerName]<BL> : Adds the player in question to your list of friends. (aliases: /amigo, /ami)</BL>\n"
        message += "<J>/c</J> <V>[playerName]<BL> : Send whispering in question for the selected player. (aliases: /w)</BL>\n"
        message += "<J>/ignore</J> <V>[playerName]<BL> : You will no longer receive messages from the player in question.</BL>\n"
        message += "<J>/watch</J> <G>[playerName]<BL> : Highlights the player in question. Type the command alone so that everything returns to normal.</BL>\n"
        message += "<J>/shooting </J><BL> : Enable/Desable the speech bubbles mice.</BL>\n"
        message += "<J>/report</J> <V>[playerName]<BL> : Opens the complaint window for the selected player.</BL>\n"
        message += "<J>/ips</J><BL> : Shows in the upper left corner of the game screen, the frame rate per second and current data in MB/s download.</BL>\n"
        message += "<J>/nosouris</J><BL> : Changes the color to the standard brown while as a guest.</BL>\n"
        message += "<J>/x_imj</J> <BL> : Opens the old menu of game modes.</BL>\n"
        message += "<J>/report</J> <V>[playerName]<BL> : Opens the complaint window for the selected player.</BL>\n"
    
        if gift.client.privLevel == 2 or gift.client.privLevel >= 5:
            message += "<J>/vamp</J> <BL> : Turns your mouse into a vampire.</BL>\n"
            message += "<J>/meep</J><BL> : Enables meep.</BL>\n"
            message += "<J>/pink</J><BL> : Let your mouse pink.</BL>\n"
            message += "<J>/transformation</J> <V>[playerNames|*] <G>[off]<BL> : Temporarily gives the ability to transform.</BL>\n"
            message += "<J>/namecor</J> <V>"+("[playerName] " if gift.client.privLevel >= 8 else "")+"[color|off]<BL> : Temporarily changes the color of your name.</BL>\n"
            message += "<J>/vip</J> <G>[message]</G><BL> : Send a message vip global.</BL>\n"
            message += "<J>/re</J> <BL> : Respawn the player.</BL>\n"
            message += "<J>/freebadges</J> <BL> : You earn new medals.</BL>\n"

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

        if gift.client.privLevel >= 5:
            message += "<J>/sy?</J><BL> : It shows who is the Sync (synchronizer) current.</BL>\n"
            message += "<J>/ls</J><BL> : Shows the list of server rooms.</BL>\n"
            message += "<J>/clearchat</J><BL> : Clean chat.</BL>\n"
            message += "<J>/ban</J> <V>[playerName] [hours] [argument]<BL> : Ban a player from the server. (aliases: /iban)</BL>\n"
            message += "<J>/mute</J> [playerName] [hours] [argument]<BL> : Mute a player.</BL>\n"
            message += "<J>/find</J> <V>[playerName]<BL> : It shows the current room of a user.</BL>\n"
            message += "<J>/hel</J> <V>[message]<BL> : Send a message in the global Helper.</BL>\n"
            message += "<J>/hide</J><BL> : Makes your invisible mouse.</BL>\n"
            message += "<J>/unhide</J><BL> : Take the invisibility of your mouse.</BL>\n"
            message += "<J>/rm</J> <V>[message]<BL> : Send a message in the global only in the room that is.</BL>\n"

        if gift.client.privLevel >= 6:
            message += "<J>/np <G>[mapCode] <BL>: Starts a new map.</BL>\n"
            message += "<J>/npp <V>[mapCode] <BL>: Plays the selected map after the current map is over.</BL>\n"
            message += "<J>/p</J><V>[category]<BL> : Evaluate a map to the chosen category.</BL>\n"
            message += "<J>/lsp</J><V>[category]<BL> : Shows the map list for the selected category.</BL>\n"
            message += "<J>/kick</J> <V>[playerName]<BL> : Expelling a server user.</BL>\n"
            message += "<J>/mapc</J> <V>[message]<BL> : Send a message in the global MapCrew.</BL>\n"

        if gift.client.privLevel >= 7:
            message += "<J>/log</J> <G>[playerName]<BL> : Shows the bans log server or a specific player.</BL>\n"
            message += "<J>/unban</J> <V>[playerName]<BL> : Unban a server player.</BL>\n"
            message += "<J>/unmute</J> <V>[playerName]<BL> : Unmute a player.</BL>\n"
            message += "<J>/sy</J> <G>[playerName]<BL> : Define who will be the sync. Type the command with nothing to reset.</BL>\n"
            message += "<J>/clearban</J> <V>[playerName]<BL> : Clean the ban vote of a user.</BL>\n"
            message += "<J>/ip</J> <V>[playerName]<BL> : Shows the IP of a user.</BL>\n"
            message += "<J>/ch [Nome]</J><BL> :Escolhe o próximo shaman.</BL>\n"
            message += "<J>/md</J> <V>[message]<BL> : Send a message in the global Moderator.</BL>\n"
            message += "<J>/lock</J> <V>[playerName]<BL> : Blocks a user.</BL>\n"
            message += "<J>/unlock</J> <V>[playerName]<BL> : Unlock a user.</BL>\n"
            message += "<J>/nomip</J> <V>[playerName]<BL> : It shows the history of a user IPs.</BL>\n"
            message += "<J>/ipnom</J> <V>[IP]<BL> : Shows the history of an IP.</BL>\n"
            message += "<J>/warn</J> <V>[playerName] [reason]<BL> : Sends an alert to a specific user.</BL>\n"

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
        if gift.client.privLevel == 12 or gift.client.privLevel >= 13:
            message += "<J>/vamp</J> <BL> : Turns your mouse into a vampire.</BL>\n"
            message += "<J>/meep</J><BL> : Enables meep.</BL>\n"
            message += "<J>/pink</J><BL> : Let your mouse pink.</BL>\n"
            message += "<J>/transformation</J> <V>[playerNames|*] <G>[off]<BL> : Temporarily gives the ability to transform.</BL>\n"
            message += "<J>/namecor</J> <V>"+("[playerName] " if gift.client.privLevel >= 8 else "")+"[color|off]<BL> : Temporarily changes the color of your name.</BL>\n"
            message += "<J>/vip</J> <G>[message]</G><BL> : Send a message vip global.</BL>\n"
            message += "<J>/re</J> <BL> : Respawn the player.</BL>\n"
            message += "<J>/freebadges</J> <BL> : You earn new medals.</BL>\n"

        if gift.client.privLevel >= 15:
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

        if gift.client.privLevel >= 12:
            message += "<J>/sy?</J><BL> : It shows who is the Sync (synchronizer) current.</BL>\n"
            message += "<J>/ls</J><BL> : Shows the list of server rooms.</BL>\n"
            message += "<J>/clearchat</J><BL> : Clean chat.</BL>\n"
            message += "<J>/ban</J> <V>[playerName] [hours] [argument]<BL> : Ban a player from the server. (aliases: /iban)</BL>\n"
            message += "<J>/mute</J> [playerName] [hours] [argument]<BL> : Mute a player.</BL>\n"
            message += "<J>/find</J> <V>[playerName]<BL> : It shows the current room of a user.</BL>\n"
            message += "<J>/hel</J> <V>[message]<BL> : Send a message in the global Helper.</BL>\n"
            message += "<J>/hide</J><BL> : Makes your invisible mouse.</BL>\n"
            message += "<J>/unhide</J><BL> : Take the invisibility of your mouse.</BL>\n"
            message += "<J>/rm</J> <V>[message]<BL> : Send a message in the global only in the room that is.</BL>\n"

        if gift.client.privLevel >= 13:
            message += "<J>/np <G>[mapCode] <BL>: Starts a new map.</BL>\n"
            message += "<J>/npp <V>[mapCode] <BL>: Plays the selected map after the current map is over.</BL>\n"
            message += "<J>/p</J><V>[category]<BL> : Evaluate a map to the chosen category.</BL>\n"
            message += "<J>/lsp</J><V>[category]<BL> : Shows the map list for the selected category.</BL>\n"
            message += "<J>/kick</J> <V>[playerName]<BL> : Expelling a server user.</BL>\n"
            message += "<J>/mapc</J> <V>[message]<BL> : Send a message in the global MapCrew.</BL>\n"

        if gift.client.privLevel >= 14:
            message += "<J>/log</J> <G>[playerName]<BL> : Shows the bans log server or a specific player.</BL>\n"
            message += "<J>/unban</J> <V>[playerName]<BL> : Unban a server player.</BL>\n"
            message += "<J>/unmute</J> <V>[playerName]<BL> : Unmute a player.</BL>\n"
            message += "<J>/sy</J> <G>[playerName]<BL> : Define who will be the sync. Type the command with nothing to reset.</BL>\n"
            message += "<J>/clearban</J> <V>[playerName]<BL> : Clean the ban vote of a user.</BL>\n"
            message += "<J>/ip</J> <V>[playerName]<BL> : Shows the IP of a user.</BL>\n"
            message += "<J>/ch [Nome]</J><BL> :Escolhe o próximo shaman.</BL>\n"
            message += "<J>/md</J> <V>[message]<BL> : Send a message in the global Moderator.</BL>\n"
            message += "<J>/lock</J> <V>[playerName]<BL> : Blocks a user.</BL>\n"
            message += "<J>/unlock</J> <V>[playerName]<BL> : Unlock a user.</BL>\n"
            message += "<J>/nomip</J> <V>[playerName]<BL> : It shows the history of a user IPs.</BL>\n"
            message += "<J>/ipnom</J> <V>[IP]<BL> : Shows the history of an IP.</BL>\n"
            message += "<J>/warn</J> <V>[playerName] [reason]<BL> : Sends an alert to a specific user.</BL>\n"

        if gift.client.privLevel >= 15:
            message += "<J>/neige</J><BL> : Enable/Disable the snow in the room.</BL>\n"
            message += "<J>/music</J> <G>[link]<BL> : Enable/Disable a song in the room.</BL>\n"
            message += "<J>/settime</J> <V>[seconds]<BL> : Changes the time the current map.</BL>\n"
            message += "<J>/smod</J> <V>[message]<BL> : Send a message in the global Super Moderator.</BL>\n"
            message += "<J>/move</J> <V>[roomName]<BL> : Move users of the current room to another room.</BL>\n"

        if gift.client.privLevel >= 15:
            message += "<J>/teleport</J><BL> : Enable/Disable the Teleport Hack.</BL>\n"
            message += "<J>/fly</J><BL> : Enable/Disable the Fly Hack.</BL>\n"
            message += "<J>/speed</J><BL> : Enable/Disable the the Speed Hack.</BL>\n"
            message += "<J>/shaman</J><BL> : Turns your mouse on the Shaman.</BL>\n"
            message += "<J>/coord</J> <V>[message]<BL> : Send a message in the global Coordinator.</BL>\n"

        if gift.client.privLevel >= 15:
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