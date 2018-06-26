#!/usr/bin/env python

import telepot.aio, time, re, datetime, sqlite3, os, os.path, subprocess

token = 'abcdefg1234567890'
chat_id_follow = 123456789

def handle(msg):
        chat_id = msg['chat']['id']
        mensagem = msg['text']
        if mensagem == '/portais' or mensagem == '/portais@ittalarmpi_bot':
            bot.sendDocument(chat_id, 'draw.txt')
            bot.sendDocument(chat_id, 'table.csv')
        elif chat_id == chat_id_follow:
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
            portal = portal.replace(',', ';')
            discovered = discovered.replace(',', ';')

            # criando a tabela dados na base.db caso não exista
            if (os.path.isfile('base.db') == False):
                conn = sqlite3.connect('base.db')
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE dados (seq BIGINT, data DATE NOT NULL, portal TEXT NOT NULL, latitude FLOAT, longitude FLOAT, discovered TEXT NOT NULL);")
                sequencial = 1
            # se a tabela já existir, descobrir qual é o maior valor do sequencial
            else:
                conn = sqlite3.connect('base.db')
                cursor = conn.cursor()
                cursor.execute("SELECT MAX(seq) FROM dados;")
                fetch = cursor.fetchone()
                sequencial = fetch[0] + 1

            # inserir dados na base.db
            cursor = conn.cursor()
            cursor.execute("INSERT INTO dados (seq, data, portal, latitude, longitude, discovered) VALUES (?,?,?,?,?,?);", (sequencial, data, portal, latitude, longitude, discovered))
            conn.commit()
            conn.close()

            # inserir dados no draw.txt
            if (os.path.isfile('draw.txt') == False):
                file_draw = open('draw.txt', 'a+')
                file_draw.write("[")
            else:
                subprocess.call(["sed -i -r '$ s/.$//' draw.txt"], shell = True)
                file_draw = open('draw.txt', 'a+')
                file_draw.write(",")
            file_draw.write('{"type":"marker","latLng":{"lat":')
            file_draw.write(latitude + ',"lng":' + longitude)
            file_draw.write('},"color":"#ff0000"}]')
            file_draw.close()

            # inserir dados no table.csv
            if (os.path.isfile('table.csv') == False):
                file_table = open('table.csv', 'a+')
                file_table.write('Sequencial,Portal,Latitude,Longitude,Discovered\n')
            else:
                file_table = open('table.csv', 'a+')
            file_table.write(str(sequencial) + "," + portal + "," + str(latitude) + "," + str(longitude) + "," + discovered + "\n")
            file_table.close()

            bot.sendMessage(chat_id, 'O portal {0} foi arquivado.'.format(portal))

bot = telepot.Bot(token)
bot.message_loop(handle)

try:
    print ('Aguardando comandos')
    while True:
        time.sleep(5)

except KeyboardInterrupt:
    print ('Saindo')
