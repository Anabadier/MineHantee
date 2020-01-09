# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 22:22:27 2019

@author: augus
"""

import math
import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np
import random as rd
import pandas as pd

def initialisation_points(chemin_fichier_config) :
    
    config = pd.read_csv(chemin_fichier_config, sep=',', header = None, index_col = 0).T
                     
    # définition des points en fonction de l'element
    global points_fantome, points_fantome_mission, points_pepite
    
    points_fantome = config.pts_fantome
    points_fantome_mission = config.pts_fantome_mission
    points_pepite = config.pts_pepite

"""
Définiton de la classe 

"""

class joueur(object):
    
    """ Initilialisation de la classe """
      
    def __init__(self,joueur = "def"):
        if joueur == "def" :
            print("Veuillez indentifier le joueur")
        else :
            self.identifiant = joueur 
            self.nb_points = 0
            self.ordre_de_mission = []
            self.ref_plateau = "null"
            self.position_graphe = "Non placé"
            self.position_detail = ["xcarte" , "ycarte"]
            
    def maj_points(self,points):
        if type(points) != str :
            print("Mauvaix format de points, doit être un string")
        else :
            point_transfo = int(points)
            self.nb_points = self.nb_points + point_transfo
    
    def maj_position(self,xcarte,ycarte,noeud):
         if type(xcarte) != int or type (ycarte) != int :
             print ("Mauvais format de coordonnées de la carte")
         elif type (noeud) != int:
             print("Mauvais format de noeuds")
         else:
             self.postion_graphe = noeud
             self.position_detail = [xcarte,ycarte]
   
    def oriente_carte_libre():
        print("A voir avec l'objet carte")
        
    def fonction_evaluation(self,plateau,un_chemin_coord):
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
        
        for coord in un_chemin_coord :
            carte = plateau.labyrinthe_detail[coord]

            if carte.elements['pepite'] is True :
                gain+= points_pepite
            if carte.elements['fantome'] is not False :
                if carte.elements['fantome'] in self.ordre_de_mission : 
                    gain+= points_fantome_mission
                else:
                    gain+= points_fantome
        return(gain)
    
    def is_terminal_node(self,plateau) : ## actualiser pour dire que s'il ne reste pas suffisament de points pour dépasser le premier is over
        dict_vide = {'fantome' : False , 'pepite' : False, 'joueur': False}
        taille = len(plateau)
        compteur=0
        for i in plateau :
            if i.elements == dict_vide :
                compteur += 1
        return (compteur == taille^2)
    
    #joker #alpha beta
    def mini_max(self,plateau, id_joueur, depth, alpha, beta, maximizingPlayer, terminal_node):
        """
        La fonction mini_max permet de calculer le meilleur gain que le joueur peut faire, c'est-à-dire :
            1) maximiser son gain en minimisant, potentiellement, le gain dans les prochains tour du joueur avec le plus de points
            2) si 1 n'est pas possible / simple dans un futur proche, maximiser le gain du joueur en minimisant celui dont le tour est le prochain. 
        
        :param position: position du joueur
        :param joueur: c'est le tour de quel joueur
        :param ordre_joueurs: quel est l'ordre des joueurs
            
        :returns chemin_optimal: le chemin que le joueur a intérêt à suivre pour garantir un gain maximal dans le court terme
        """
        is_terminal = self.is_terminal_node(plateau)
        carte_test = plateau.carte_en_dehors
        #joker = self
        
        if depth == 0 or is_terminal:
            if is_terminal: #il n'y a plus de pépites ni de fantonmes à capturer
                return (None, None, 0)
            else: # Depth is zero
                dico_chemins = plateau.chemin_possible(id_joueur)[1]
                chemins_coord = [dico_chemins[coord] for coord in dico_chemins.keys()]  # /!\ à revoir
                points = [self.fonction_evaluation(plateau, i) for i in chemins_coord]
                le_chemin = chemins_coord[points.index(max(points))]
                return (None, None, max(points))
        
        if maximizingPlayer: #joker player #la personne qui utilise le joker
            value = -math.inf
            entree = rd.choice(plateau.entrees)
            for orientation in range(1,5):
                carte_test.orientation = orientation
                for une_entree in plateau.entrees:
                    p_copy = plateau.copy()
                    p_copy.coulisser_detail(une_entree[0], une_entree[1], carte_test)
                    id_next_joueur = self.next_joueur.identification # /!\ à revoir mais c'est l'idée
                    new_score = self.mini_max(self, p_copy, id_next_joueur, depth-1, alpha, beta, False)[1]
                    if new_score > value:
                        value = new_score
                        entree = une_entree
                        ori = orientation
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return (entree, ori, value)
        
        else: # Minimizing player
            value = math.inf
            entree = rd.choice(plateau.entrees)
            for orientation in range(1,5):
                carte_test.orientation = orientation
                for une_entree in plateau.entrees:
                    p_copy = plateau.copy()
                    p_copy.coulisser_detail(une_entree[0], une_entree[1], carte_test)
                    id_next_joueur = self.next_joueur.identification # /!\ à revoir mais c'est l'idée
                    if id_next_joueur == id_joueur :
                        new_score = self.mini_max(self, p_copy, id_next_joueur, depth-1, alpha, beta, True)[1]
                    else :
                        new_score = self.mini_max(self, p_copy, id_next_joueur, depth-1, alpha, beta, False)[1]
                    if new_score < value:
                        value = new_score
                        entree = une_entree
                        ori = orientation
                        beta = min(beta, value)
                    if alpha >= beta:
                        break
            return (entree, ori, value)
       
             
 
           
             

      
    
