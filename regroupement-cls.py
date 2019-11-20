# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 12:11:26 2019

@author: augus
"""
import math
import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np
import random
#[Nord,Sud,Est,Ouest] Definition du dictionnaire de la connectivité 
connectivité={'coin':[[0,1,1,0],[1,0,1,0],[1,0,0,1],[0,1,0,1]],
              'couloir':[[1,1,0,0],[0,0,1,1]],
              'carrefour':[[1,1,1,0],[1,0,1,1],[1,1,0,1],[0,1,1,1]]}

"""
Construction de la classe carte

"""

class carte():
    def __init__(self,type_carte,dict_elements,\
                 position_graph,position_detail,
                 orientation):
        """type_carte : str
        dict_elements : dict {fantome,pepite,joueur)
        position_graph : ref noeud networkX
        position_detail : (int,int)
        orientation : int
        connectivité : [[],[],[],[]]"""
        self.type=type_carte
        self.elements=dict_elements
        self.position_G=position_graph
        self.position_D=position_detail
        self.orientation=orientation
        self.connectivité=connectivité[type_carte]
    
    def pivoter(self,sens):
        if sens=='horaire' :
            if self.orientation < len(self.connectivité):
                self.orientation=self.connectivité[self.orientation+1]
            else :
                self.orientation=self.connectivité[0] #retour au premier
        
        else: #anti-horaire
            if self.orientation > 0:
                self.orientation=self.connectivité[self.orientation-1]
            else :
                self.orientation=self.connectivité[-1] #retour au dernier
        

"""

Construction de la classe joueur

"""


class joueur(object):
    
    """ Initilialisation de la classe """
      
    def __init__(self,joueur = "1"):
        if joueur == "1" :
            print("Veuillez indentifier le joueur")
        else :
            self.identifiant = joueur 
            self.nb_points = 0
            self.ordre_de_mission = []
            self.ref_plateau = "null"
            self.position_graphe = "Non placé"
            self.position_detail = ("xcarte" , "ycarte")
            
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
        
        
"""
Essai de programme principal

"""


#Créeons un plateau de 5 sur 5 avec 15 couloir, 6 coin, 4 carrefour

plateau_dispo  = []
print(plateau_dispo)
LISTE_CARTE = []


for i in range(1,16):
    new_carte  = carte('couloir',0,0,(0,0),0)
    LISTE_CARTE.append(new_carte)

for i in range(1,7):
    new_carte  = carte('coin',0,0,(0,0),0)
    LISTE_CARTE.append(new_carte)
    
for i in range(1,5):
    new_carte  = carte('carrefour',0,0,(0,0),0)
    LISTE_CARTE.append(new_carte)


random.shuffle(LISTE_CARTE)

plateau_voir = []

print(LISTE_CARTE[0])
for i in range (1,6):
    liste_inter1 = []
    liste_inter2 = []
    for j in range (1,6):
        print(i)
        inter = random.choice(LISTE_CARTE)
        inter.position_D = (i,j)
        liste_inter1.append(inter)
        liste_inter2.append(inter.type)
        LISTE_CARTE.remove(inter)
    plateau_dispo.append(liste_inter1)
    plateau_voir.append(liste_inter2)

    
print(plateau_dispo)
print(plateau_voir)
    

# Carte solo

carte_solo = new_carte  = carte('couloir',0,0,(0,0),0)



















       