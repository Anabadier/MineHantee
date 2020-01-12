# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:04:21 2019

@author: eliot
"""

import socket, sys, threading, time

class Server(object):
    def __init__(self, _PORT, _HOST, _nb_joueurs_tot = 2, _nb_IA = 0):
        #self.launcher = _ref_launcher
        self.PORT = int(_PORT)
        self.HOST = _HOST
        
        self.serveur_DimPlateau = 0
        self.serveur_NbJoueur = int(_nb_joueurs_tot)
        self.serveur_NbJoueur_IA = int(_nb_IA)
        self.serveur_NbFantome = 0
        self.serveur_NbFantomeOdM = 0
        self.serveur_NbPepite = 0
        self.serveur_PtsPepite = 0
        self.serveur_PtsFantome = 0
        self.serveur_PtsFantomeOdM = 0
# =============================================================================
#         self.nb_joueur_H = int(_nb_joueurs_tot) - int(_nb_IA)
#         self.nb_IA
# =============================================================================
        
        self.dict_clients = {}  # dictionnaire des connexions clients
        self.dict_pseudos = {}  # dictionnaire des pseudos
        #dict_reponses = {}  # dictionnaire des réponses des clients
        self.dict_scores = {} # dictionnaire des scores de la dernière question
        
        self.connexion_counter = 0
        
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
        
        while self.connexion_counter < self.serveur_NbJoueur:
            # Attente connexion nouveau client
            try:
                connexion, adresse = mySocket.accept()
                print("Someone is trying to connect with,", connexion)
                # Créer un nouvel objet thread pour gérer la connexion
                self.connexion_counter+=1
                th = ThreadClient(connexion, self)
                # The entire Python program exits when no alive non-daemon threads are left
                th.setDaemon(1)
                th.start()
            except:
                sys.exit()
        
        print("Le quota de joueurs est atteints {0}/{1}".format(self.connexion_counter,
                                                                  self.serveur_NbJoueur))

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
    
    def receiver_manager(self, _message):
        if _message[:6] == "PSEUDO":
            self.get_pseudo_client(_message)
        
        if _message[:6] == "PARA_S":
            if (self.serveur.connexion_counter == 1):
                self.set_board_parameter_in_server(_message)
        
        if _message == "SET PARA CLIENT":
            self.set_board_parameter_in_client()
        
    
    def set_board_parameter_in_server(self, _message):
        _message_split = _message.split()
        self.serveur.serveur_DimPlateau = int(_message_split[1])
        self.serveur.serveur_NbFantome = int(_message_split[2])
        self.serveur.serveur_NbFantomeOdM = int(_message_split[3])
        self.serveur.serveur_NbPepite = int(_message_split[4])
        self.serveur.serveur_PtsPepite = int(_message_split[5])
        self.serveur.serveur_PtsFantome = int(_message_split[6])
        self.serveur.serveur_PtsFantomeOdM = int(_message_split[7])
        
        print(106, self.serveur.serveur_DimPlateau,
        self.serveur.serveur_NbFantome,
        self.serveur.serveur_NbFantomeOdM,
        self.serveur.serveur_NbPepite,
        self.serveur.serveur_PtsPepite,
        self.serveur.serveur_PtsFantome,
        self.serveur.serveur_PtsFantomeOdM)
        
    def set_board_parameter_in_client(self):
        parametres = "PARA_CL {0} {1} {2} {3} {4} {5} {6} {7} {8}".format(
                                              self.serveur.serveur_DimPlateau,
                                              self.serveur.serveur_NbJoueur,
                                              self.serveur.serveur_NbJoueur_IA,
                                              self.serveur.serveur_NbFantome,
                                              self.serveur.serveur_NbFantomeOdM,
                                              self.serveur.serveur_NbPepite,
                                              self.serveur.serveur_PtsPepite,
                                              self.serveur.serveur_PtsFantome,
                                              self.serveur.serveur_PtsFantomeOdM)
        parametres = bytes(parametres,"UTF8")
        self.serveur.dict_clients[self.nom].send(parametres)
        
    
    def get_pseudo_client(self, _message):
        # attente réponse client
        #pseudo = self.connexion.recv(4096)
        print(135)
        pseudo = _message.split()[-1]
        print(137, pseudo)
        #pseudo = pseudo.decode(encoding='UTF-8')
        print(139, pseudo)
        self.serveur.dict_pseudos[self.nom] = pseudo
        print(141, self.serveur.dict_pseudos)
        print("Pseudo du client", self.connexion.getpeername(),"-->", pseudo)
    
    def get_creator_status(self):
        try :
            message = "RANK {0}".format(self.serveur.connexion_counter)
            status = bytes(message,"UTF8")
            self.serveur.dict_clients[self.nom].send(status)
            print("Le serveur a envoyé", message, "a", self.serveur.dict_clients[self.nom])
        except:
            print("creator_status n'a pas pu être envoyé au joueur")
        
    def run(self):
          
# =============================================================================
#         if (self.serveur.connexion_counter < self.serveur.serveur_NbJoueur):
#             self.manage_connexion_client()
# =============================================================================
        
        self.get_creator_status()
        
        while True:
            try:
                # attente action du client
                reponse = self.connexion.recv(4096)
                reponse = reponse.decode(encoding='UTF-8')
                print('the server recieved:', reponse)
                
                if (reponse != ""):
                    self.receiver_manager(reponse)
                
                reponse = ""
                    
            except:
                print(reponse)
                # fin du thread
                #break

        print("\nFin du thread",self.nom)
        self.connexion.close()

if __name__=="__main__":    
    #valeurs de port et de l'adresse pour fonctionner seul
# =============================================================================
#     PORT = 50026
#     HOST = "127.0.0.1"
#     Server(PORT, HOST,2,0)
# =============================================================================
    c = 0
    while True:
        if c == 0:
            PORT = sys.argv[1]
            HOST = sys.argv[2]
            nb_J = sys.argv[3]
            nb_IA = sys.argv[4]
            Server(PORT, HOST, nb_J, nb_IA)
            c+=1
