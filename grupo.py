#!/usr/bin/env python

import telepot.aio, time, re, datetime, sqlite3, os

def handle(msg):
        chat_id = msg['chat']['id']
        mensagem = msg['text']
        if mensagem == '/gerar' or mensagem == '/gerar@ittalarmpi_bot':
                print("Enviar arquivos")
        #if chat_id == 114701736:
        data = datetime.datetime.fromtimestamp(msg['date']).strftime('%Y-%m-%d %H:%M:%S')
        portal = mensagem[mensagem.find("Portal: ")+8:mensagem.find("\n")]
        for i in range(0, len(msg['entities'])):
                if 'url' in msg['entities'][i]:
                        buscar = msg['entities'][i]['url']
                        achou = buscar.find("https://www.ingress.com/")
                        if (achou == 0):
                                coordenada = msg['entities'][i]['url']
                                latitude = coordenada[coordenada.find("intel?ll=")+9:coordenada.find(",-")]
                                longitude = coordenada[coordenada.find(",")+1:coordenada.find("&z=15&pll")]
        discovered = mensagem[mensagem.find("Discovered by: ")+14:mensagem.find("\n\nGUID")]
        bot.sendMessage(chat_id, 'Portal: {0} \nLatitude: {1} \nLongitude: {2} \nDiscovered by: {3}'.format(portal, latitude, longitude, discovered))

        print("Conectar com o banco de dados")

        print(data)
        print(coordenada)
        print(latitude + " , " + longitude)
        print(discovered)

bot = telepot.Bot('TOLKEN')
bot.message_loop(handle)

try:
    print ('Iniciando ...')
    while True:
        time.sleep(5)

except KeyboardInterrupt:
    print ('Saindo')
