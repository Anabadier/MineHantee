# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:30:15 2019

@author: augus
"""

import math
import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import networkx as nx
import pandas








#[Nord,Sud,Est,Ouest] Definition du dictionnaire de la connectivité 
connectivité={'coin':[[0,1,1,0],[1,0,1,0],[1,0,0,1],[0,1,0,1]],
              'couloir':[[1,1,0,0],[0,0,1,1]],
              'carrefour':[[1,1,1,0],[1,0,1,1],[1,1,0,1],[0,1,1,1]]}


##################################################################################
#Classe Ghost
##################################################################################

class ghost(object):
    def __init__(self,posi=(0,0),identifiant=0):
        self.id = identifiant

##################################################################################
#Classe Carte
##################################################################################

#
#class carte(object):
#    def __init__(self,type_carte,dict_elements,\
#                 position_graph,position_detail,
#                 orientation,mobilite=True):
#        """type_carte : str
#        dict_elements : dict {fantome,pepite,joueur)
#        position_graph : ref noeud networkX
#        position_detail : (int,int)
#        orientation : int
#        connectivité : [[],[],[],[]]"""
#        self.type=type_carte
#        self.elements=dict_elements
#        self.position_G=position_graph
#        self.position_D=position_detail
#        self.orientation=orientation
#        self.mobilite=mobilite
#        self.connectivite=connectivite[type_carte]
#    
#    def pivoter(self,sens):
#        if sens=='horaire' :
#            if self.orientation < len(self.connectivité):
#                self.orientation=self.connectivité[self.orientation+1]
#            else :
#                self.orientation=self.connectivité[0] #retour au premier
#        
#        else: #anti-horaire
#            if self.orientation > 0:
#                self.orientation=self.connectivité[self.orientation-1]
#            else :
#                self.orientation=self.connectivité[-1] #retour au dernier
#        
from carte import carte
##################################################################################
#Classe Joueur
##################################################################################


class Joueur(object):
    
    """ Initilialisation de la classe """
      
    def __init__(self,joueur = "none"):
        if joueur == "none" :
            print("Veuillez indentifier le joueur")
        else :
            self.identifiant = joueur 
            self.nb_points = 0
            self.ordre_de_mission = []
            self.ref_plateau = "null"
            self.position_graphe = "Non placé"
            self.position_detail = ("xcarte" , "ycarte")
    
    def generer_odre_mission(self,nb_ordre,nb_ghost):
        ordre_mission = []
        for i in range(nb_ordre):
            fantome = random.randint(1,nb_ghost)
            while fantome in ordre_mission:
                fantome = random.randint(1,nb_ghost)
            ordre_mission.append(fantome)
        self.ordre_de_mission = ordre_mission

       
    def maj_points(self,points):
        if type(points) != str :
            print("Mauvaix format de points, doit être un string")
        else :
            point_transfo = int(points)
            self.nb_points = self.nb_points + point_transfo
    
    def maj_position(self,carte,noeud):
         self.postion_graphe = carte.position_G
         self.position_detail = carte.position_D
   
    def oriente_carte_libre(carte_libre,sens):
        test = ["horaire","anti-horaire"]
        if sens not in test:
            print("Mauvaises instructions de sens")
        else:
            carte_libre.pivoter(sens)
            
        
    def heuristique():
        "Un peu tôt"
        
        
        
        

###############################################################################
# Classe Plateau
###############################################################################
cartes_disponibles = {'coin' : 20, 'couloir' : 25, 'carrefour' : 16}

class Plateau(object) :
    '''
    Le fichier de configuration en exemple :
    fichier Config :
        dim_plateau,7
        nb_fantomes, 8
        nb_pepites, 10
        
        #types dict et list non pris en charge dans le format csv
        proportion cartes types [0.33,0.33,0.34] #pas les bonnes proportions
        cartes_disponibles, {'coin' : 20, 'couloir' : 25, 'carrefour' : 16}
                            #pas les bons chiffres
    '''
    
    def __init__(self, dim_plateau): #chemin_fichier_config) :
        
        #self.config = pandas.read_csv(chemin_fichier_config, sep=';', 
                                     # header = None, index_col = 0).T
        
        
        self.taille = dim_plateau #int(self.config.dim_plateau)
        self.labyrinthe_detail = np.array([[object]*self.taille]*self.taille)
        
        graph = nx.Graph()
        graph.add_nodes_from(list(range(self.taille**2)))
        node_pos = [(i,j) for i in range(self.taille) for j in range(self.taille)]
        
        for k in range(self.taille**2) : 
            graph.node[k]['pos'] = node_pos[k]
        
        self.node_pos = node_pos
        self.graph = graph
        
        # print(self.config)
        

#        
    def placer_carte_libre(self,liste_carte):
        for i in range (self.taille):
            for j in range (self.taille):
                if type(self.labyrinthe_detail[i,j]) == type :
                    
                    new_carte = random.choice(liste_carte)
                    new_carte.position_D=(i,j)
                    self.labyrinthe_detail[i][j] = new_carte
                    
                    liste_carte.remove(new_carte)
    
    def etablir_connexion(self,carte):
        #Connexion Nord
        if carte.connectivite[carte.orientation][0] == 1 and i != 0:
            if self.labyrinthe_detail[i-1][j].connectivite[self.labyrinthe_detail[i-1][j].orientation][1] == 1 :
                print('Youhou !')
                self.graph.add_edge(self.node_pos.index((i-1,j)),self.node_pos.index((i,j)))
        
        #Connexion Ouest
        if carte.connectivite[carte.orientation][3] == 1 and j != 0:
            if self.labyrinthe_detail[i][j-1].connectivite[self.labyrinthe_detail[i][j-1].orientation][2] == 1 :
                self.graph.add_edge(self.node_pos.index((i,j)),self.node_pos.index((i,j-1)))
        
        #Connexion Est
        if carte.connectivite[carte.orientation][2] == 1 and j != self.taille-1:
            if self.labyrinthe_detail[i][j+1].connectivite[self.labyrinthe_detail[i][j+1].orientation][3] == 1 :
                self.graph.add_edge(self.node_pos.index((i,j)),self.node_pos.index((i,j+1)))
        
        #Connexion Sud
        if carte.connectivite[carte.orientation][1] == 1 and i != self.taille-1:
            if self.labyrinthe_detail[i+1][j].connectivite[self.labyrinthe_detail[i+1][j].orientation][0] == 1 :
                self.graph.add_edge(self.node_pos.index((i,j)),self.node_pos.index((i+1,j)))

        
 
    
    def placer_pepites(self, nb_pepites) :
        '''
        place les pepites sur le plateau
        '''
        compteur = 0
        while compteur != nb_pepites:
            i = random.randint(0,self.taille-1)
            j = random.randint(0,self.taille-1)
            if self.labyrinthe_detail[i][j].elements['pepite']==[]:
                self.labyrinthe_detail[i][j].elements['pepite'] = True
                compteur+=1
    
    def placer_joueurs(self, liste_joueur) :
        '''
        Place les joueurs sur le plateau
        '''
        for joueur in liste_joueur:
            a = random.choice([2,self.taille-3])
            b = random.choice([2,self.taille-3])
            while self.labyrinthe_detail[a][b].elements['joueur'] != []:
                a = random.choice([2,self.taille-3])
                b = random.choice([2,self.taille-3])
            self.labyrinthe_detail[a][b].elements['joueur'] = joueur.identifiant
            joueur.position_detail=(a,b)
        
    
    def placer_fantomes(self,liste_ghost):
        compteur=0
        arret = len(liste_ghost)
        while compteur!=arret:
            i = random.randint(1,self.taille-1)
            j = random.randint(1,self.taille-1)
            if self.labyrinthe_detail[i][j].mobilite == True and self.labyrinthe_detail[i][j].elements['fantome']==[]:
                self.labyrinthe_detail[i][j].elements['fantome']=liste_ghost[0].id
                del liste_ghost[0]
                compteur+=1
                print(compteur)
                

    def generer_carte_fixe(self,nb_fantome,nb_pepites) :
        '''
        génère un plateau aléatoirement selon les contraintes imposées 
        dans le fichier de configuration
        '''
        
        #Generation des cartes sur le plateau
        taille = self.taille
        
        Nb_CF = (taille//2 + 1)**2
        Pair = (Nb_CF%2 == 0)
        
        dico_connectivite = {'couloir' : [[0,0,1,1],[1,1,0,0],[0,0,1,1],[1,1,0,0]],
                             'coin' : [[0,1,1,0],[0,1,0,1],[1,0,0,1],[1,0,1,0]],
                             'carrefour' : [[0,1,1,1],[1,1,0,1],[1,0,1,1],[1,1,1,0]]}
        
        #Construction des listes des cartes fixes sur le plateau, selon
        #que le nombre de cartes fixes est pair ou impair
        liste_CF_PP = [(i,j) for i in range(0,taille, 2) for j in range(0, taille, 2)]
        liste_CF_PI = [(i,j) for i in range(1,taille, 2) for j in range(1, taille, 2)]
    
        #On stocke la liste des index des cartes fixes sur le plateau
        if Pair :
            self.Index_Cartes_fixes = liste_CF_PP
        else :
            self.Index_Cartes_fixes = liste_CF_PI

        
        for i in range(taille) :
            for j in range(taille) :
                
                if ((i,j) in self.Index_Cartes_fixes):
                    
                    
                    Nord_ouvert = (i > 0 and i <= taille-1)  
                    Sud_ouvert =  (i >= 0 and i < taille-1)
                    Est_ouvert = (j < taille//2)
                    Ouest_ouvert = (j > taille//2)
                    
                    orientation_CF = [int(Nord_ouvert), int(Sud_ouvert),
                                         int(Est_ouvert), int(Ouest_ouvert)]
                    
                    if sum(orientation_CF) > 2 :
                        type_CF = 'carrefour'
                    else :
                        type_CF = 'coin'
                    
                    carte_in = carte(type_CF, {'fantome':[],'pepite':[],'joueur':[]}, 0, 
                                               (i,j), dico_connectivite[type_CF].index(orientation_CF),mobilite=False)
                    self.labyrinthe_detail[i][j] = carte_in
                
    
   
    def coulisser_detail (self,coord_x, coord_y):
        """
        Change les positions des objets cartes dans la matrice “self.labyrinthe_detail”
        :param coord_x: abscisse du lieu où l'on souhaite faire coulisser la carte
        :param coord_y: ordonnée du lieu où l'on souhaite faire coulisser la carte
        :return:
        """
        ## on modifie la ligne
        # en coulissant de gauche à droite
        if coord_x == -1 :
            carte_sortante = self.labyrinthe_detail[self.taille-1,coord_y]
            for i in range(self.taille-1, 0, -1) :
                self.labyrinthe_detail[i,coord_y] = self.labyrinthe_detail[i-1,coord_y]
            self.labyrinthe_detail[0,coord_y] = self.carte_en_dehors
        # en coulissant de droite à gauche    
        if coord_x == self.taille :
            carte_sortante = self.labyrinthe_detail[0,coord_y]
            for i in range(self.taille) :
                self.labyrinthe_detail[i,coord_y] = self.labyrinthe_detail[i+1,coord_y]
            self.labyrinthe_detail[self.taille-1,coord_y] = self.carte_en_dehors
                
        ## on modifie la colonne
        # en coulissant de haut en bas
        if coord_y == -1 :
            carte_sortante = self.labyrinthe_detail[coord_x, self.taille-1]
            for i in range(self.taille-1, 0, -1) :
                self.labyrinthe_detail[coord_x,i] = self.labyrinthe_detail[coord_x, i-1]
            self.labyrinthe_detail[coord_x, 0] = self.carte_en_dehors
        # en coulissant du bas vers le haut
        if coord_y == self.taille :
            carte_sortante = self.labyrinthe_detail[coord_x,0]
            for i in range(self.taille) :
                self.labyrinthe_detail[coord_x, i] = self.labyrinthe_detail[coord_x,i+1]
            self.labyrinthe_detail[coord_x,self.taille-1] = self.carte_en_dehors
        
        #la nouvelle carte à coulisser sera la carte qui est sortie
        self.carte_en_dehors = carte_sortante 
    
    def coulisser_graphe (self) :
        """
        Change la connectivité de “self.labyrinthe_graphe”
        lorsque qu’une nouvelle carte est insérée dans le plateau.
        La nouvelle carte doit être connectée au réseau; la carte sortante
        ne doit plus être connectée; les cartes intermédiaire doivent
        modifier leur connection.
        """
        pass
    
    def coulisser (self):
        """
        Effectue tous les changements associés à l’introduction
        d’une carte dans le plateau au début du tour d’un joueur.
        Notamment, appelle les méthodes “coulisser_detail”
        et “coulisser_graphe”.
        """
        pass
    
    def check_deplacement (self):
        """
        Vérifie que le déplacement demandé par un joueur
        est valide. Si possible, effectue la mise à jour de la position du
        joueur sinon, renvoie un message d’erreur visible par le joueur.
        """
        pass
 