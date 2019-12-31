# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:46:27 2019

@author: augus
"""

import math
from math import ceil
import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import networkx as nx
import pandas

from Calass_rep import *
    
def JEU(dimension = 7, nombre_joueur = 2, nombre_ghost = 6, nombre_ordre_mission = 4,
        nombre_pepite = 49, pts_pepite = 1, pts_fantome = 5, pts_ordre_mission = 15):    
    
    connectivite={'coin':[[0,1,1,0],[1,0,1,0],[1,0,0,1],[0,1,0,1]],
                  'couloir':[[1,1,0,0],[0,0,1,1]],
                  'carrefour':[[1,1,1,0],[1,0,1,1],[1,1,0,1],[0,1,1,1]]}
    
    proportion= {'Couloir':0.38,
                 'Coin':0.44,
                 'Carrefour':0.18}
    
    
    
    ###################################################################################
    #Extraction des fichiers de config , code d'Eliott 
    ##################################################################################
    
# =============================================================================
#     nombre_ghost = 6
#     nombre_pepite = 49
#     dimension = 7
#     nombre_joueur = 2
#     nombre_ordre_mission=4
# =============================================================================
    
    #####################################################################################
    #Initialisation du jeu 
    ####################################################################################
    
    Liste_ghost=[]
    for i in range (1,nombre_ghost+1):
        new_ghost = ghost(identifiant = i)            # Création des fantomes 
        Liste_ghost.append(new_ghost)
    
    """
    Génération des cartes
    """
        
    Liste_carte = []
    
    nombre_carte_mobile = (dimension**2)-((dimension//2+1)**2)+1
    
    nombre_carrefour = ceil(nombre_carte_mobile*proportion['Carrefour']) #arrondit supérieur
    nombre_coin = ceil(nombre_carte_mobile*proportion['Coin']) #arrondit supérieur   
    #nombre_couloir = round(nombre_carte_mobile*proportion['Couloir']) 
    nombre_couloir=nombre_carte_mobile-nombre_carrefour-nombre_coin #complément au nb de cartes
    
    
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
    
    """
    Remplissage du plateau
    
    """
    
    
    plateau=Plateau(dimension)                                             
    
    
    plateau.generer_carte_fixe(nombre_ghost,nombre_pepite)
    plateau.placer_carte_libre(Liste_carte)
    
    
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
    nx.draw_networkx(plateau.graph, pos = plateau.node_pos, ax = plateau.ax_graph)
    
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
    
    return(plateau)

if __name__=="__main__":
    JEU()