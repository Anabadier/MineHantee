# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 22:22:27 2019

@author: augus
"""

import math
import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np

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
        
    def heuristique():
        "Un peu tôt"
       
             
 
           
             

      
    
