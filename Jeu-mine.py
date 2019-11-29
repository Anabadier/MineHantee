# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:46:27 2019

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

import Calass_rep





connectivite={'coin':[[0,1,1,0],[1,0,1,0],[1,0,0,1],[0,1,0,1]],
              'couloir':[[1,1,0,0],[0,0,1,1]],
              'carrefour':[[1,1,1,0],[1,0,1,1],[1,1,0,1],[0,1,1,1]]}

proportion= {'Couloir':0.38,
             'Coin':0.44,
             'Carrefour':0.18}



###################################################################################
#Extraction des fichiers de config , code d'Eliott 
##################################################################################

nombre_ghost = 6
nombre_pepite = 49
dimension = 7
nombre_joueur = 2
nombre_ordre_mission=4

#####################################################################################
#Initialisation du jeu 
####################################################################################

Liste_ghost=[]
for i in range (1,nombre_ghost+1):
    new_ghost = ghost(identifiant = i)            # Création des fantomes 
    Liste_ghost.append(new_ghost)

"""
Génértion des cartes
"""
    
Liste_carte = []

nombre_carte_mobile = (dimension**2)-((dimension//2+1)**2)+1

nombre_carrefour = round(nombre_carte_mobile*proportion['Carrefour'])
nombre_coin = round(nombre_carte_mobile*proportion['Coin'])                                
nombre_couloir = round(nombre_carte_mobile*proportion['Couloir'])

for i in range (0,nombre_carrefour):
    new_carte = carte("carrefour",{'fantome':[],'pepite':[],'joueur':[]},0,(0,0),random.randint(0,3))
    Liste_carte.append(new_carte)

for i in range (0,nombre_coin):
    new_carte = carte("coin",{'fantome':[],'pepite':[],'joueur':[]},0,(0,0),random.randint(0,3))
    Liste_carte.append(new_carte)
    
for i in range (0,nombre_couloir):
    new_carte = carte("couloir",{'fantome':[],'pepite':[],'joueur':[]},0,(0,0),random.randint(0,1))
    Liste_carte.append(new_carte)



carte_dehors = random.choice(Liste_carte)
Liste_carte.remove(carte_dehors) 
print(len(Liste_carte))   

"""
Remplissage du plateau

"""


plateau=Plateau(dimension)                                             


plateau.generer_carte_fixe(nombre_ghost,nombre_pepite)
plateau.placer_carte_libre(Liste_carte)
print(plateau.labyrinthe_detail)


""" 
Placement des fantomes
"""

plateau.placer_fantomes(Liste_ghost)

"""
Placement des pepites 
"""

plateau.placer_pepites(nombre_pepite)


"""
Etablissement des connexions du réseau entre les cartes
"""

for i in range (dimension):
    for j in range(dimension):
        plateau.etablir_connexion(plateau.labyrinthe_detail[i,j])

""" 
Génération des jouers et placement sur le plateau
"""

Liste_joueur=[]
for i in range(1,nombre_joueur+1):                      #génération des joueurs
    new_joueur = Joueur(i)
    new_joueur.ref_plateau = plateau
    Liste_joueur.append(new_joueur)
    


for joueur in Liste_joueur:
    joueur.generer_odre_mission(nombre_ordre_mission,nombre_ghost)          # Attribution des ordres de missions 
    
plateau.placer_joueurs(Liste_joueur)                                     # Placement des joueurs sur les cases qui lerus sont attribués 


################################################################################
# Déroulement du jeu
################################################################################