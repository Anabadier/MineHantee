# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 11:14:37 2019

@author: eliot
"""


import socket, threading
import Launcher as Lch


class Client(object):
    def __init__(self, _ref_launcher):
        self.CONNEXION = False
        self.launcher = _ref_launcher
        self.PORT = int(self.launcher.PORT)
        self.HOST = self.launcher.HOST
        self.pseudo = self.launcher.pseudo
        # création ref
        self.ref_socket = {}
        
        print("Client créé")
        self.ConnexionServeur()
    
    def ConnexionServeur(self):
        
        # Établissement de la connexion
        # protocoles IPv4 et TCP
        print("Connexion au serveur...")
    
        if self.CONNEXION == False:
            try:
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                mySocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                mySocket.connect((self.HOST, self.PORT))
                # Dialogue avec le serveur : on lance un thread pour gérer la réception des messages
                th_R = ThreadReception(mySocket, self)
                th_R.start()
                self.CONNEXION = True
                
                print("Connecté au serveur", self.HOST, self.PORT)
                
                self.envoyer_Pseudo()
                
            except socket.error:
                print('Erreur','La connexion au serveur a échoué.')
    
    def envoyer_Pseudo(self):
        if self.CONNEXION == True:
            try:
                message = self.pseudo
                # émission 
                self.ref_socket[0].send(bytes(message,"UTF8"))
                print("Pseudo envoyé au serveur")
                
            except socket.error:
                print("L'envoie du pseudo a échoué")
                pass
    
    def envoyer_Touche(self, _touche ='touche test'):
        if self.CONNEXION == True:
            try:
                print("Envoie de la touche au serveur...")
                # émission 
                self.ref_socket[0].send(bytes(_touche,"UTF8"))
                
            except socket.error:
                print("Echec de l'envoie de la touche au server")
                pass
                

class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn, _client):
        threading.Thread.__init__(self)
        self.client = _client
        self.client.ref_socket[0] = conn
        self.connexion = conn  # réf. du socket de connexion
              
    def run(self):
        while True:
            try:
                # en attente de réception
                message_recu = self.connexion.recv(4096)
                message_recu = message_recu.decode(encoding='UTF-8')
                
                if (message_recu !=""):
                    print('the client recieved:', message_recu)
                
                if "FIN" in message_recu:
                    self._client.CONNEXION = False
                    
            except socket.error:
                pass       
        

if __name__=="__main__":
    Lch.LauncherMineHantee()
    
