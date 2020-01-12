# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 11:14:37 2019

@author: eliot
"""


import socket, threading
import Launcher as Lch
import Jeu_mine as Jm
import vizpygame as vpyg
import time

class Client(object):
    def __init__(self, _ref_launcher):
        self.CONNEXION = False
        self.launcher = _ref_launcher
        self.PORT = int(self.launcher.PORT)
        self.HOST = self.launcher.HOST
        self.pseudo = self.launcher.value_pseudos[0]
        print(22, self.launcher.value_pseudos[0])
        print(22, self.pseudo)
        # création ref
        self.ref_socket = {}
        
        self.serveur_creator = False
        
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
                
                print(48)
                self.envoyer_Pseudo()
                print(50)
                
            except socket.error:
                print('Erreur','La connexion au serveur a échoué.')
    
    def envoyer_parametre_plateau(self):
        
        parametres = "PARA_S {0} {1} {2} {3} {4} {5} {6}".format(
                                              self.launcher.value_DimPlateau,
                                              self.launcher.value_NbFantome,
                                              self.launcher.value_NbFantomeOdM,
                                              self.launcher.value_NbPepite,
                                              self.launcher.value_PtsPepite,
                                              self.launcher.value_PtsFantome,
                                              self.launcher.value_PtsFantomeOdM)
        parametres = bytes(parametres,"UTF8")
        self.ref_socket[0].send(parametres)
        self.launch_game()
    
    
    def envoyer_ordre_set_paramatre_in_client(self):
        message = "SET PARA CLIENT"
        print(70, message)
        message = bytes(message,"UTF8")
        self.ref_socket[0].send(message)
        print(68, "sent")
    
    def envoyer_Pseudo(self):
        if self.CONNEXION == True:
            try:
                message = "PSEUDO " + self.pseudo
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
    
    def launch_game(self):
        print("in 98")
        self.launcher.launch_game()

class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn, _client):
        threading.Thread.__init__(self)
        self.client = _client
        self.client.ref_socket[0] = conn
        self.connexion = conn  # réf. du socket de connexion
    
    def receiver_manager(self, _message):
        if _message[:4] == "RANK":
            self.maj_server_creator_bool(int(_message.split()[-1]))
        
        if _message[:7] == "PARA_CL":
            self.set_board_parameter_in_client_launcher(_message)
        
    def maj_server_creator_bool(self, _val):
        print(109, _val)
        if (_val == 1):
            self.client.serveur_creator = True
            self.client.envoyer_parametre_plateau()
        else:
            print(113)
            self.client.envoyer_ordre_set_paramatre_in_client()
    
    def set_board_parameter_in_client_launcher(self, _message):
        _message_split = _message.split()
        self.client.launcher.value_DimPlateau = int(_message_split[1])
        self.client.launcher.value_NbJoueur = int(_message_split[2])
        self.client.launcher.value_NbJoueur_IA = int(_message_split[3])
        self.client.launcher.value_NbFantome = int(_message_split[4])
        self.client.launcher.value_NbFantomeOdM = int(_message_split[5])
        self.client.launcher.value_NbPepite = int(_message_split[6])
        self.client.launcher.value_PtsPepite = int(_message_split[7])
        self.client.launcher.value_PtsFantome = int(_message_split[8])
        self.client.launcher.value_PtsFantomeOdM = int(_message_split[9])
        
        self.client.launch_game()
              
    def run(self):
        while True:
            try:
                # en attente de réception
                message_recu = self.connexion.recv(4096)
                message_recu = message_recu.decode(encoding='UTF-8')
                print('the client recieved:', message_recu)
                
                if (message_recu !=""):
                    self.receiver_manager(message_recu)
                
                if "FIN" in message_recu:
                    self._client.CONNEXION = False
                    
            except socket.error:
                pass       
        

if __name__=="__main__":
    Lch.LauncherMineHantee()
    
