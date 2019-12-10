# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 15:14:44 2019

@author: Liliana JALPA PINEDA

IA - facile

Utilise l'algorithme min-max pour déterminer la meilleure stratégie à la prochaine
étape. En essayant de minimiser si possible le gain en points du joeur avec le plus
de points, sinon en essayant de minimiser le gain du prochain joueur,
tout en maximisant son propre gain.

"""

import pandas as pd
import numpy as np

def initialisation_points(chemin_fichier_config) :
    
    config = pd.read_csv(chemin_fichier_config, sep=',', header = None, index_col = 0).T
                     
    # définition des points en fonction de l'element
    global points_fantome, points_fantome_mission, points_pepite
    
    points_fantome = config.pts_fantome
    points_fantome_mission = config.pts_fantome_mission
    points_pepite = config.pts_pepite
    

def fonction_evaluation(un_chemin, joueur):
    #labyrinthe_detail ?
    """
    La fonction d'evaluation permet de calculer le gain total si on suit un chemin donné.
    Fonction simple qui somme la valeur en point des entités recueillies sur le chemin.
    Le calcul se fait en fonction du nombre de pépites recueillies ainsi que du nombre de fantomes recueillis.
    
    :param un_chemin: chemin a evaluer
    :param labyrinthe_detail: matrice avec les cartes que l'on va traverser pour savoir s'il y a une pépite/fantome dessus
    :param chemin_fichier_config: chemin vers le fichier de configuration pour connaitre la valeur d'une pepite, fantome, fantome dans mission
    
    :returns gain: gain que l'on peut obtenir si on suit un chelin
    """
    # initialisation du gain
    gain = 0
    
    # si dans chemin coordonnees dans labyrinthe detail
#    for coord in un_chemin :
#        carte = labyrinthe_detail[coord]
    
    # si dans chemin directement cartes 
    for carte in un_chemin :
        if carte.elements['pepite'] is True :
            gain+= points_pepite
        if carte.elements['fantome'] is not np.nan :
            if carte.elements['fantome'] in joueur.ordre_de_mission : 
                gain+= points_fantome_mission
            else:
                gain+= points_fantome
    return(gain)
    
def tous_les_chemins_possibles(position):
    liste_chemins = []
    return(liste_chemins)

def mini_max(position, joueur, ordre_joueurs):
    """
    La fonction mini_max permet de calculer le meilleur gain que le joueur peut faire, c'est-à-dire :
        1) maximiser son gain en minimisant, potentiellement, le gain dans les prochains tour du joueur avec le plus de points
        2) si 1 n'est pas possible / simple dans un futur proche, maximiser le gain du joueur en minimisant celui dont le tour est le prochain. 
    
    :param position: position du joueur
    :param joueur: c'est le tour de quel joueur
    :param ordre_joueurs: quel est l'ordre des joueurs
        
    :returns chemin_optimal: le chemin que le joueur a intérêt à suivre pour garantir un gain maximal dans le court terme
    """
    # combien de points à chaque joueur ? 
    points = [joueur.nb_points]
    
    for joujou in ordre_joueurs :
        points += [joujou.nb_points]
    
    # quels sont les chemins qui s'offrent à notre joueur 
    chemins_possibles_j1 = tous_les_chemins_possibles(position)
    
    # quels sont les gains potentiels pour tous ces chemins
    # la liste sera triée dans l'ordre croissant
    # dans la liste on a des tuples, (i,j) i index dans la liste des chemins, j gain associé au chemin
    gains_potentiels = []
    for chemin in chemins_possibles_j1 :
        # appel de la fontion définie plus haut
        gain = fonction_evaluation(chemin, joueur)
        if gains_potentiels == [] : # premier element
            gains_potentiels += [(chemins_possibles_j1.index(chemin),gain)]
        else: # tri dans l'ordre decroissant
            j=0
            n=len(gains_potentiels)
            while j<n and gain<gains_potentiels[j][1]:
                j=j+1
            x = (chemins_possibles_j1.index(chemin),gain)
            gains_potentiels.insert(j,x) #liste des gains possibles triée par ordre decroissant
    
    indice_chemin_opti = gains_potentiels[0][0]
    chemin_optimal = [chemins_possibles_j1(indice_chemin_opti)]
    
    return (chemin_optimal)