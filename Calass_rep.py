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
from classe_carte import carte


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
   
    def oriente_carte_libre(self, carte_libre, sens):
        test = ["horaire","anti-horaire"]
        if sens not in test:
            print("Mauvaises instructions de sens")
        else:
            carte_libre.pivoter(sens)
    
    def modifier_plateau(self, coord_x, coord_y):
        """
        Fait coulisser une ligne ou une colonne
        
        :param coord_x: abscisse du lieu où l'on souhaite faire coulisser la carte
        :param coord_y: ordonnée du lieu où l'on souhaite faire coulisser la carte
        """
        self.ref_plateau.coulisser(coord_x, coord_y)
            
        
    def heuristique():
        "Un peu tôt"
        
class Joueur_IA(Joueur):
    def __init__(self, _niv):
        self.niv = _niv
