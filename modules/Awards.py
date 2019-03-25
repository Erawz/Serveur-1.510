#coding: utf-8
import os, struct, urllib
from datetime import datetime
from twisted.internet import reactor
from modules import ByteArray, Identifiers

class AwardsPlayers:

    def __init__(this, client, server):
        this.client = client
        this.server = client.server

    def sendMenu(this):
        this.client.sendPacket([29, 20], '\x00\x00*\xf8\x00\x00\x03\t\x00\x18\x00\x12\x00\x14\x00\x1826\x00\x1826d\x00')
        this.client.sendPacket([29, 20], "\x00\x00*\xf9\x00A<a href='event:fullMenu:open'><font size='15'><N>?</N></font></a>\x03\x0c\x00\x18\x00\x12\x00\x14\x00\x00\x00\x00\x00\x00\x00\x00d\x00")

    def sendPremio(this):
        if os.path.exists('./include/premiados.txt'):
            BadUsers = str(open('./include/premiados.txt', 'r').read()).split(', ')
        else:
            fo = open('./include/premiados.txt', 'wb')
            fo.write('10.0.0.1')
            fo.close()
        now = datetime.now()
        if this.client.Username not in BadUsers:
            with open('./include/premiados.txt', 'r+') as f:
                old = f.read()
                f.seek(0)
                f.write('' + this.client.Username + ', ' + old)
            this.client.firstCount += 5000
            this.client.cheeseCount += 5000
            this.client.nowCoins += 3000
            this.client.sendClientMessage('<S>Voc\xc3\xaa recebeu <J>5.000 <S>firsts e <J>3.000 <S>moedas!')

    def sendpremiohours(this):
        if this.client.privLevel >= 1:
            #if this.client.langueByte == 3:
                #this.client.rebootTimer = reactor.callLater(360, this.sendAnuncioConstante1)
                #this.client.rebootTimer = reactor.callLater(720, this.sendAnuncioConstante1)
                #this.client.rebootTimer = reactor.callLater(1080, this.sendAnuncioConstante1)
                #this.client.rebootTimer = reactor.callLater(1440, this.sendAnuncioConstante1)
                #this.client.rebootTimer = reactor.callLater(1800, this.sendAnuncioConstante1)
                #this.client.rebootTimer = reactor.callLater(2160, this.sendAnuncioConstante1)
                #this.client.rebootTimer = reactor.callLater(2520, this.sendAnuncioConstante1)
                #this.client.rebootTimer = reactor.callLater(360, this.shopMessage)
            this.client.rebootTimer = reactor.callLater(15, this.sendpremiomessage)
            this.client.rebootTimer = reactor.callLater(20, this.sendfbMessage)
            #this.client.rebootTimer = reactor.callLater(25, this.msgs)
            this.client.rebootTimer = reactor.callLater(3600, this.sendpremio1hora)
            this.client.rebootTimer = reactor.callLater(7200, this.sendpremio2horas)
            this.client.rebootTimer = reactor.callLater(10800, this.sendpremio3horas)
            this.client.rebootTimer = reactor.callLater(14400, this.sendpremio4horas)
            this.client.rebootTimer = reactor.callLater(18000, this.sendpremio5horas)
            #this.client.rebootTimer = reactor.callLater(600, this.eventMessage)

    def shopMessage(this):
        this.client.sendLangueMessage("", '<BL>Ol\xc3\xa1, <J>'+str(this.client.Username)+'<BL>. Vendemos cargo de Mod/Admin por apenas <J>R$30,00! <BL>Agora voc\xc3\xaa pode comprar por <J>boleto<BL>,<J> cart\xc3\xa3o de cr\xc3\xa9dito <BL>e<J> dep\xc3\xb3sito<BL>. Ao comprar, voc\xc3\xaa ter\xc3\xa1 diversos comandos: <VP>Banir<N>,<VP> mover jogadores da sala<BL>,<VP> expulsar<BL>,<VP> ganhar moedas<BL>,<VP> ajudar a fazer eventos <BL>e<VP> muito mais<BL>! Acesse a nossa lojinha e saiba mais: <J>'+str(this.server.shopURL))
        reactor.callLater(1200, this.shopMessage)

    def eventMessage(this):
        if this.client.langueByte == 3:
            this.client.sendLangueMessage("", '<J>[EVENTO] <N>Participe do nosso <CH>Evento de Aventura<N> coletando o item do evento e firstando voc\xc3\xaa ganhar\xc3\xa1 7 firsts/moedas e podendo ganhar at\xc3\xa9 mesmo medalhas e t\xc3\xadtulos que ningu\xc3\xa9m possu\xc3\xad. <CH>Digite: /sala #eventoaventura1')
        elif this.client.langueByte == 4:
            this.client.sendLangueMessage("", '<J>[EVENTO] <N>Participe de nuestro <CH>Evento de Aventura<N> recogiendo el \xc3\xadtem del evento y en primer lugar usted ganar\xc3\xa1 7 firsts / monedas y pudiendo ganar incluso medallas y t\xc3\xadtulos que nadie pose\xc3\xada. <CH>Introduzca: /room #eventoaventura1')
        else:
            this.client.sendLangueMessage("", '<J>[EVENT] <N>Participate in our <CH>Adventure Event<N> collecting the item of the event and firstando you will win 7 firsts / coins and can win even medals and titles that no one has. <CH>Type: /room #eventoaventura1')
        reactor.callLater(3600, this.eventMessage)

    def sendpremiomessage(this):
        if this.client.langueByte == 3:
            this.client.sendLangueMessage("", '<ROSE>Pr\xc3\xaamios por ficar online:\n<J> 1 hora <VP>= <J> 5 <V>firsts/queijos/moedas e <J>1000<V> queijos/morangos.\n<J> 2 horas <VP>= <J> 10 <V>firsts/queijos/moedas e <J>2000<V> queijos/morangos.\n<J> 3 horas <VP>= <J> 20 <V>firsts/queijos/moedas e <J>3000<V> queijos/morangos.\n<J> 4 horas <VP>= <J> 30 <V>firsts/queijos/moedas e <J>4000<V> queijos/morangos.\n<J> 5 horas <VP>= <J> 50 <V>firsts/queijos/moedas e <J>5000<V> queijos/morangos.')
        elif this.client.langueByte == 4:
            this.client.sendLangueMessage("", '<ROSE>Premios por estar en l\xc3\xadnea:\n<J> 1 hora <VP>= <J> 5 <V>firsts/quesos/monedas e <J>1000<V> quesos/fresas.\n<J> 2 horas <VP>= <J> 10 <V>firsts/quesos/monedas e <J>2000<V> quesos/fresas.\n<J> 3 horas <VP>= <J> 20 <V>firsts/quesos/monedas e <J>3000<V> quesos/fresas.\n<J> 4 horas <VP>= <J> 30 <V>firsts/quesos/monedas e <J>4000<V> quesos/fresas.\n<J> 5 horas <VP>= <J> 50 <V>firsts/quesos/monedas e <J>5000<V> quesos/fresas.')
        else:
            this.client.sendLangueMessage("", '<ROSE>Awards for being online:\n<J> 1 hour <VP>= <J> 5 <V>firsts/cheeses/moedas e <J>1000<V> cheeses/fraises.\n<J> 2 hours <VP>= <J> 10 <V>firsts/cheeses/moedas e <J>2000<V> cheeses/fraises.\n<J> 3 hours <VP>= <J> 20 <V>firsts/cheeses/moedas e <J>3000<V> cheeses/fraises.\n<J> 4 hours <VP>= <J> 30 <V>firsts/cheeses/moedas e <J>4000<V> cheeses/fraises.\n<J> 5 hours <VP>= <J> 50 <V>firsts/cheeses/moedas e <J>5000<V> cheeses/fraises.')
        reactor.callLater(1440, this.sendpremiomessage)

    def sendfbMessage(this):
        if not str(this.server.fbURL) in ["","em breve"] and str(this.server.fbURL).startswith("http://") or str(this.server.fbURL).startswith("https://") or str(this.server.fbURL).startswith("www."):
            if this.client.langueByte == 3:
                this.client.sendLangueMessage("", "<CH>Curta nossa página do facebook: <b>"+str(this.server.fbURL)+"</b>")
            elif this.client.langueByte == 4:
                this.client.sendLangueMessage("", "<CH>Corta nuestra pagina de facebook: <b>"+str(this.server.fbURL)+"</b>")
            else:
                this.client.sendLangueMessage("", "<CH>Enjoy our facebook page: <ab>"+str(this.server.fbURL)+"</b>")
        reactor.callLater(725, this.sendpremiomessage)

    def sendpremio1hora(this):
        this.client.shopCheeses += 1000
        this.client.shopFraises += 1000
        this.client.firstCount += 5
        this.client.cheeseCount += 5
        this.client.shamanSaves += 5
        this.client.nowCoins += 5
        this.client.nowTokens += 5
        if this.client.langueByte == 3:
            this.client.sendLangueMessage("", '<R><b>Voc\xc3\xaa ganhou o pr\xc3\xaamio de uma hora online:</b> <VP>+1000 queijos e morangos na loja e +5 fichas, +5 firsts, queijos, saves no perfil e moedas.')
        elif this.client.langueByte == 4:
            this.client.sendLangueMessage("", '<R><b>Usted gan\xc3\xb3 el premio de una hora en l\xc3\xadnea:</b> <VP>+1000 quesos y fresas en la tienda y +5 fichas, +5 firsts, quesos, saves en el perfil y monedas.')
        else:
            this.client.sendLangueMessage("", '<R><b>You won the one hour prize online: </b> <VP>+1000 cheeses and strawberries in the store and +5 chips, +5 firsts, cheeses, saves in profile and coins.')

    def sendpremio2horas(this):
        this.client.shopCheeses += 2000
        this.client.shopFraises += 2000
        this.client.firstCount += 10
        this.client.cheeseCount += 10
        this.client.shamanSaves += 10
        this.client.nowCoins += 10
        this.client.nowTokens += 6
        if this.client.langueByte == 3:
            this.client.sendLangueMessage("", '<R><b>Voc\xc3\xaa ganhou o pr\xc3\xaamio de duas horas online:</b> <VP>+2000 queijos e morangos na loja e +6 fichas, +10 firsts, queijos, saves no perfil e moedas.')
        elif this.client.langueByte == 4:
            this.client.sendLangueMessage("", '<R><b>Usted gan\xc3\xb3 el premio de dos horas en l\xc3\xadnea:</b> <VP>+2000 quesos y fresas en la tienda y +6 fichas, +10 firsts, quesos, saves en el perfil y monedas.')
        else:
            this.client.sendLangueMessage("", '<R><b>You won the two-hour prize online:</b> <VP>+2000 cheeses and strawberries in the store and +6 chips, +10 firsts, cheeses, saves in profile and coins.')

    def sendpremio3horas(this):
        this.client.shopCheeses += 3000
        this.client.shopFraises += 3000
        this.client.firstCount += 20
        this.client.cheeseCount += 20
        this.client.shamanSaves += 20
        this.client.nowCoins += 20
        this.client.nowTokens += 7
        if this.client.langueByte == 3:
            this.client.sendLangueMessage("", '<R><b>Voc\xc3\xaa ganhou o pr\xc3\xaamio de tr\xc3\xaas horas online:</b> <VP>+3000 queijos e morangos na loja e +7 fichas, +20 firsts, queijos, saves no perfil e moedas.')
        elif this.client.langueByte == 4:
            this.client.sendLangueMessage("", '<R><b>Usted gan\xc3\xb3 el premio de tres horas en l\xc3\xadnea:</b> <VP>+3000 quesos y fresas en la tienda y +7 fichas, +20 firsts, quesos, saves en el perfil y monedas.')
        else:
            this.client.sendLangueMessage("", '<R><b>You won the three-hour prize online:</b> <VP>+3000 cheeses and strawberries in the store and +7 chips, +20 firsts, cheeses, saves in profile and coins.')

    def sendpremio4horas(this):
        this.client.shopCheeses += 4000
        this.client.shopFraises += 4000
        this.client.firstCount += 30
        this.client.cheeseCount += 30
        this.client.shamanSaves += 30
        this.client.nowCoins += 30
        this.client.nowTokens += 8
        if this.client.langueByte == 3:
            this.client.sendLangueMessage("", '<R><b>Voc\xc3\xaa ganhou o pr\xc3\xaamio de quatro horas online:</b> <VP>+4000 queijos e morangos na loja e +8 fichas, +30 firsts, queijos, saves no perfil e moedas.')
        elif this.client.langueByte == 4:
            this.client.sendLangueMessage("", '<R><b>Usted gan\xc3\xb3 el premio de cuatro horas en l\xc3\xadnea:</b> <VP>+4000 quesos y fresas en la tienda y +8 fichas, +30 firsts, quesos, saves en el perfil y monedas.')
        else:
            this.client.sendLangueMessage("", '<R><b>You won the four-hour prize online:</b> <VP>+4000 cheeses and strawberries in the store and +8 chips, +30 firsts, cheeses, saves in profile and coins.')

    def sendpremio5horas(this):
        this.client.shopCheeses += 5000
        this.client.shopFraises += 5000
        this.client.firstCount += 50
        this.client.cheeseCount += 50
        this.client.shamanSaves += 50
        this.client.nowCoins += 50
        this.client.nowTokens += 10
        if this.client.langueByte == 3:
            this.client.sendLangueMessage("", '<R><b>Voc\xc3\xaa ganhou o pr\xc3\xaamio de cinco horas online:</b> <VP>+5000 queijos e morangos na loja e +10 fichas, +50 firsts, queijos, saves no perfil e moedas.')
        elif this.client.langueByte == 4:
            this.client.sendLangueMessage("", '<R><b>Usted gan\xc3\xb3 el premio de cinco horas en l\xc3\xadnea:</b> <VP>+5000 quesos y fresas en la tienda y +10 fichas, +50 firsts, quesos, saves en el perfil y monedas.')
        else:
            this.client.sendLangueMessage("", '<R><b>You won the five-hour prize online:</b> <VP>+5000 cheeses and strawberries in the store and +10 chips, +50 firsts, cheeses, profile saves and coins.')

    def sendAnuncioConstante1(this):
        this.client.sendLangueMessage("", '<VP>[An\xc3\xbancio] <ROSE>Adquira <VP><b>[MOD]</b> <ROSE>e fa\xc3\xa7a eventos, ganhe 20 mil moedas, t\xc3\xadtulo de MOD, comandos, respeito, etc. Saiba mais acessando: <u><b>'+str(this.server.shopURL)+'</b></u>')

    def sendAdsense(this):
        reactor.callLater(600, this.client.sendMessage, '<BL>Compre agora mesmo cargo de <J>VIP<BL> do <J>'+str(this.server.miceName)+'<BL>, basta voc\xc3\xaa acessar <J>'+str(this.server.shopURL)+'<BL> e seguir as instru\xc3\xa7\xc3\xb5es.')
        reactor.callLater(750, this.client.sendMessage, '<BL>Clique nos an\xc3\xbancios para ganhar <J>pr\xc3\xaamios</J>.')
        reactor.callLater(2000, this.sendAdsense)
        
    # MENSAGENS #

    def msgs(this):
        #this.msg1()
        reactor.callLater(10, this.msg2)
        reactor.callLater(30, this.msg3)
        reactor.callLater(50, this.msg4)

    def msg1(this):
        if this.client.langueByte == 3:
            this.client.sendLangueMessage("", "<N>Está perdido ? Não sabe os comandos e novidades ? Abra o menu <J><b>?</b></J> em cima do lado direito e veja as novidades !")
    
    def msg2(this):
        if this.client.langueByte == 3:
            this.client.sendLangueMessage("", "<N>Pedimos <J>"+this.client.Username+"</J> que você clique no <J>anúncio</J> acima para manter nosso servidor online, lembre-se que o servidor é mantido de acordo com os cliques recebidos, isso só depende de você ^~^")

    def msg3(this):
        if this.client.langueByte == 3:
            this.client.sendLangueMessage("", "<N>Lembre-se de convidar seus amigos para jogar <J><b>"+this.server.miceName+"</b></J>! :-) ")

    def msg4(this):
        if this.client.langueByte == 3:
            this.client.sendLangueMessage("", "<N>Nosso Standalone já está disponível. Para baixa-lo, clique em <J><b>Standalone</b></J> no menu do nosso site.")

    # MENSAGENS #