# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:04:21 2019

@author: eliot
"""

import socket, sys, threading, time

class Server(object):
    def __init__(self, _PORT, _HOST):
        #self.launcher = _ref_launcher
        self.PORT = int(_PORT)
        self.HOST = _HOST
        self.nb_joueur = 1 #self.launcher.Scale_NbJoueur.get()
        
        self.dict_clients = {}  # dictionnaire des connexions clients
        self.dict_pseudos = {}  # dictionnaire des pseudos
        #dict_reponses = {}  # dictionnaire des réponses des clients
        self.dict_scores = {} # dictionnaire des scores de la dernière question
        
        self.connexion_manager()
    
    def connexion_manager(self):
        print("Création du serveur...")
        print("Port :", self.PORT)
        print("Adresse :", self.HOST)
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print((self.HOST, self.PORT))
            mySocket.bind((self.HOST, self.PORT))
        except socket.error:
            print("La liaison du socket à l'adresse choisie a échoué.")
            sys.exit()
        print("Serveur prêt, en attente de clients...")
        mySocket.listen(5)
        
        while len(self.dict_clients) < self.nb_joueur:
            # Attente connexion nouveau client
            try:
                connexion, adresse = mySocket.accept()
                print(connexion)
                # Créer un nouvel objet thread pour gérer la connexion
                th = ThreadClient(connexion, self)
                # The entire Python program exits when no alive non-daemon threads are left
                th.setDaemon(1)
                th.start()
            except:
                sys.exit()
            
        

class ThreadClient(threading.Thread):
    '''dérivation de classe pour gérer la connexion avec un client'''
    
    def __init__(self, _conn, _serveur):

        threading.Thread.__init__(self)
        self.connexion = _conn
        self.serveur = _serveur
        
        # Mémoriser la connexion dans le dictionnaire
        
        self.nom = self.getName() # identifiant du thread "<Thread-N>"
        self.serveur.dict_clients[self.nom] = self.connexion
        self.serveur.dict_scores[self.nom] = 0
        
        print("Connexion du client", self.connexion.getpeername(),self.nom, self.connexion)
        
        
    def run(self):
        
        # Choix du pseudo    
        message = bytes("Attente des autres clients...\n", "utf-8")
        self.connexion.send(message)
        
        # Choix du pseudo    
        
        self.connexion.send(b"Entrer un pseudo :\n")
        # attente réponse client
        pseudo = self.connexion.recv(4096)
        pseudo = pseudo.decode(encoding='UTF-8')
        
        self.serveur.dict_pseudos[self.nom] = pseudo
        
        print("Pseudo du client", self.connexion.getpeername(),">", pseudo)
        
        message = b"Attente des autres clients...\n"
        self.connexion.send(message)
        # Réponse aux questions
       
        while True:
            try:
                # attente action du client
                reponse = self.connexion.recv(4096)
                reponse = reponse.decode(encoding='UTF-8')
                
                if (reponse != ""):
                    print('the server recieved:', reponse)
                
            except:
                # fin du thread
                break

        print("\nFin du thread",self.nom)
        self.connexion.close()

if __name__=="__main__":    
    #valeurs de port et de l'adresse pour fonctionner seul
# =============================================================================
#     PORT = 50278
#     HOST = "127.0.0.1"
# =============================================================================
    c = 0
    while True:
        if c == 0:
            PORT = sys.argv[1]
            HOST = sys.argv[2]
            Server(PORT, HOST)
