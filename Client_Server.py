'''A faire : Envoi de la liste des connecte
            Codifie l'utilisation
            Codifie l'utilisation du chat.py'''


#!/usr/bin/env python3
# echo.py
# author: Sébastien Combéfis
# version: February 15, 2016

#Enregistrement de la liste des connecte
#Se deconnecter -> Suppression d'une entree du dico
#Envoi de donne du server au client

import socket
import sys
import pickle
import json

SERVERADDRESS = (socket.gethostname(), 7000)

class EchoServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        self.__connectedlist = {}
        print('server')

    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                receive = self._receive(client).decode()
                receive = receive.split('/')
                username = receive[0]
                adress = addr
                strlist = 'test'

                if receive[1] == 'connect' :
                    self.connection(username, adress, client)
                if receive[1] == 'disconnect' :
                    self.disconnection(username)
                client.close()
            except OSError:
                print('Erreur lors de la réception du message.')

    def connection(self, username, adress, client):
        self.__connectedlist[username] = adress
        print('Connection de',username, adress)
        print('Liste de connectés : ', self.__connectedlist)
        self.send(client)

    def disconnection(self, username):
        del self.__connectedlist[username]
        print('Deconnection de',username)
        print('Liste de connectés : ', self.__connectedlist)

    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)

    def send(self, client):
        #client.sendall(pickle.dumps(self.__connectedlist))
        client.sendall(pickle.dumps('ok'))

class EchoClient():
    def __init__(self, message, status):
        self.__message = message
        self.__status = status
        self.__s = socket.socket()


    def run(self):
        try:
            self.__s.connect(SERVERADDRESS)
            self._send()
            self.__s.close()
        except OSError:
            print('Serveur introuvable, connexion impossible.')

    def _send(self):
        totalsent = 0
        msg = (self.__message +'/' + self.__status).encode()
        try:
            while totalsent < len(msg):
                sent = self.__s.send(msg[totalsent:])
                totalsent += sent
        except OSError:
            print("Erreur lors de l'envoi du message.")

    def connect(self):
        try :
            self.__s.connect(SERVERADDRESS)
            self._send()
            print('Connected')
            print(self.receive())
            self.__s.close()
        except OSError:
            print('Serveur introuvable, connexion impossible.')

    def disconnect(self):
        try :
            self.__s.connect(SERVERADDRESS)
            self._send()
            print('Disconnected')
            self.__s.close()
        except OSError:
            print('Serveur introuvable, connexion impossible.')

    def receive(self):
        response = b""
        r = self.__s.recv(1024)
        while r :
            response += r
            r = self.__s.recv(1024)

        return pickle.loads(response)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        EchoServer().run()

    elif len(sys.argv) == 4 and sys.argv[1] == 'client' and sys.argv[2] == 'connect':
        EchoClient(sys.argv[3], sys.argv[2]).connect()

    elif len(sys.argv) == 4 and sys.argv[1] == 'client' and sys.argv[2] == 'disconnect':
        EchoClient(sys.argv[3], sys.argv[2]).disconnect()

    elif len(sys.argv) == 3 and sys.argv[1] == 'client':
        EchoClient(sys.argv[2].encode()).run()
