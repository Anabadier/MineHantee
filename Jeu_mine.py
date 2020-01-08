# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:46:27 2019

@author: augus
"""

from math import ceil
import random
import networkx as nx

from Calass_rep import *
from Classe_plateau import Plateau
from classe_carte import carte

import SaC


def JEU(dimension = 7,
        nombre_joueur = 2, pseudos_joueurs = ["Joueur_1"],
        nombre_joueur_IA = 2, IA_niv = ["Facile", "Facile"],#Difficile
        nombre_ghost = 21, nombre_ordre_mission = 3,
        nombre_pepite = 49, pts_pepite = 1, pts_fantome = 5, pts_ordre_mission = 15,
        _SaC = SaC.Save_and_Charge()):    
    
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
    
    plateau=Plateau(dimension, _SaC)
    """
    Génération des cartes
    """
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
    Gestion des points
    """
    plateau.set_objects_points(pts_pepite, pts_fantome, pts_ordre_mission)
    
    """
    Etablissement des connexions du réseau entre les cartes
    """
    
    for i in range (dimension):
        for j in range(dimension):
            plateau.etablir_connexion(plateau.labyrinthe_detail[i,j])
    #nx.draw_networkx(plateau.graph, pos = plateau.node_pos, ax = plateau.ax_graph)
    
    """ 
    Génération des jouers et placement sur le plateau
    """
    
    for i in range(nombre_joueur_IA):#génération des joueurs IA
        new_joueur = Joueur_IA(_identifiant = IA_niv[i]+"_"+str(i), _niv = IA_niv[i])
        new_joueur.ref_plateau = plateau
        if (new_joueur.niv == "Difficile"):
            new_joueur.UCT_solver = UCT_2()
        #new_joueur.generate_liste_row_col()
        plateau.Liste_Joueur_IA.append(new_joueur)
    
    for i in range(nombre_joueur-nombre_joueur_IA):#génération des joueurs
        new_joueur = Joueur(_identifiant = pseudos_joueurs[i])
        new_joueur.ref_plateau = plateau
        plateau.Liste_Joueur_H.append(new_joueur)
    
    plateau.Liste_Joueur = plateau.Liste_Joueur_IA+plateau.Liste_Joueur_H
    
    for joueur in plateau.Liste_Joueur:
        joueur.generer_odre_mission(nombre_ordre_mission,nombre_ghost)# Attribution des ordres de missions 
        joueur.determiner_joueur_voisins_ordre()
        plateau.dict_ID2J[joueur.identifiant] = joueur
        
    plateau.placer_joueurs(plateau.Liste_Joueur)# Placement des joueurs sur les cases qui lerus sont attribués 
    
    plateau.maj_classement()
    
    plateau.generate_liste_row_col()

    ################################################################################
    # Déroulement du jeu
    ################################################################################
    _SaC.log_plateau(_plateau = plateau, _overwrite = True)#initialise le log
    
    
    return(plateau)

if __name__=="__main__":
    plateau = JEU()
    c = 0
    actions = []
    while (c<4):#not plateau.check_gagnant() ):
        print("Coup numéro:", c)
        for _j in plateau.Liste_Joueur_IA:
            print("=====================================================")
            print("Avant de jouer", _j.identifiant, ",", _j.nb_points, "points",
                  _j.position_detail, _j.position_graphe)
            _j.jouer()
# =============================================================================
#             coup_alea = _j.coup_alea(_j.ref_plateau)
#             print(coup_alea)
#             actions += [[_j]+coup_alea]
# =============================================================================
            print("Après avoir joué,",_j.identifiant,",", _j.nb_points, "points",
                  _j.position_detail, _j.position_graphe)
            c+=1
    #print(actions)
# =============================================================================
#     for i in range(c-1, -1, -1):
#         print("=====================================================")
#         print(actions[i][1:])
#         #print(605,rollout_action_list[i])
#         j_retro_playing = actions[i][0]
#         #print(606, j_retro_playing.identifiant, j_retro_playing.nb_points)
#         j_retro_playing.coup_cible(plateau, actions[i][1:], True)
# =============================================================================
            
        
