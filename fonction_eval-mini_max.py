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
import math as math
import random as rd

joker = 5 # en realité égal au joueur qui utilise le joker

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
    
def is_terminal_node(plateau) :
    dict_vide = {'fantome' : False , 'pepite' : False, 'joueur': False}
    taille = len(plateau)
    compteur=0
    for i in plateau :
        if i.elements == dict_vide :
            compteur += 1
    return (compteur == taille^2)
    
def mini_max(plateau, position, depth, alpha, beta, maximizingPlayer, terminal_node):
    """
    La fonction mini_max permet de calculer le meilleur gain que le joueur peut faire, c'est-à-dire :
        1) maximiser son gain en minimisant, potentiellement, le gain dans les prochains tour du joueur avec le plus de points
        2) si 1 n'est pas possible / simple dans un futur proche, maximiser le gain du joueur en minimisant celui dont le tour est le prochain. 
    
    :param position: position du joueur
    :param joueur: c'est le tour de quel joueur
    :param ordre_joueurs: quel est l'ordre des joueurs
        
    :returns chemin_optimal: le chemin que le joueur a intérêt à suivre pour garantir un gain maximal dans le court terme
    """
    is_terminal = is_terminal_node(plateau)
    carte_test = plateau.carte_en_dehors
    
    if depth == 0 or is_terminal:
        if is_terminal: #il n'y a plus de pépites ni de fantonmes à capturer
            return (None, 0)
        else: # Depth is zero
            chemins = tous_les_chemins_possibles(position)
            points = [fonction_evaluation(i, joker) for i in chemins]
            le_chemin = max(points)
            return (None, fonction_evaluation(le_chemin, joker))
    
    if maximizingPlayer:
        value = -math.inf
        entree = rd.choice(plateau.entrees)
        for orientation in range(1,5):
            carte_test.orientation = orientation
            for une_entree in plateau.entrees:
                p_copy = plateau.copy()
                p_copy.coulisser_detail(une_entree[0], une_entree[1], carte_test)
                new_score = mini_max(p_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    entree = une_entree
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return (entree, value)
    
    else: # Minimizing player
        value = math.inf
        entree = rd.choice(plateau.entrees)
        for orientation in range(1,5):
            carte_test.orientation = orientation
            for une_entree in plateau.entrees:
                p_copy = plateau.copy()
                p_copy.coulisser_detail(une_entree[0], une_entree[1], carte_test)
                new_score = mini_max(p_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    entree = une_entree
                    beta = min(beta, value)
                if alpha >= beta:
                    break
        return (entree, value)
 