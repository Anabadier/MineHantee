# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:30:15 2019

@author: augus
"""

import random as rd
import networkx as nx
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
      
    def __init__(self, _indentifiant = "none"):
        if _indentifiant == "none" :
            print("Veuillez indentifier le joueur")
        else :
            self.identifiant = _indentifiant 
            self.nb_points = 0
            self.ordre_de_mission = []
            self.ref_plateau = "null"
            self.position_graphe = "Non placé"
            self.position_detail = ("xcarte" , "ycarte")
    
    def generer_odre_mission(self,nb_ordre,nb_ghost):
        ordre_mission = []
        for i in range(nb_ordre):
            fantome = rd.randint(1,nb_ghost)
            while fantome in ordre_mission:
                fantome = rd.randint(1,nb_ghost)
            ordre_mission.append(fantome)
        self.ordre_de_mission = ordre_mission
       
    def maj_points(self,points):
        if type(points) != str :
            print("Mauvaix format de points, doit être un string")
        else :
            point_transfo = int(points)
            self.nb_points = self.nb_points + point_transfo
    
    def maj_position(self, _carte, noeud):
         self.position_graphe = _carte.position_G
         self.position_detail = _carte.position_D
   
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
    
    def __init__(self, _indentifiant = "none", _niv ="facile"):
        
        Joueur.__init__(self)
        self.identifiant = _indentifiant
        self.niv = _niv
        
        self.liste_row_col = [] #liste des lignes et colonnes que l'on peut faire coulisser
        
    def generate_liste_row_col(self):
        for i in range(1, self.ref_plateau.taille, 2):
            for _char in ["G", "D", "H", "B"]:
                self.liste_row_col += [_char + str(i)]
    def coup_alea(self, _plateau):
        """
        joue un coup complet aléatoirement (rotation de la carte libre, choix
        de la ligne ou de la colonne à jouer, déplacement)
        
        _plateau(instance de la classe Plateau):
            référence du plateau sur lequel on joue. Important car on utiisera
            cette fonction dans le "RollOut" de l'UCT sur des copies du plateau
            d'origine.
        """
        self.rotation_carte_alea(_plateau)
        self.coulisser_alea(_plateau)
        self.deplacement_alea(_plateau)
        
    def rotation_carte_alea(self, _plateau):
        """
        tourne la carte libre aléatoirement
        
        _plateau(instance de la classe Plateau):
            référence du plateau sur lequel on joue. Important car on utiisera
            cette fonction dans le "RollOut" de l'UCT sur des copies du plateau
            d'origine.
        """
        nb_rotation = rd.choice([1,2,3,4])
        
        for i in range(nb_rotation):
            self.oriente_carte_libre(_plateau.carte_en_dehors, "horaire")
    
    def coulisser_alea(self, _plateau):
        """
        introduit la carte libre dans une colonne ou une ligne aléatoirement
        
        _plateau(instance de la classe Plateau): facultatif
            référence du plateau sur lequel on joue. Important car on utiisera
            cette fonction dans le "RollOut" de l'UCT sur des copies du plateau
            d'origine.
        """
        fleche = rd.choice(self.liste_row_col)
        
        convertFlecheCoord={'G':[int(fleche[1:]),-1],'D':[int(fleche[1:]),_plateau.taille],
                            'H':[-1,int(fleche[1:])],'B':[_plateau.taille,int(fleche[1:])]}
        coord_x=convertFlecheCoord[fleche[0]][0]
        coord_y=convertFlecheCoord[fleche[0]][1]
        
        _plateau.coulisser(coord_x, coord_y)
    
    def deplacement_alea(self, _plateau):
        """
        déplacment aléatoire sur le plateau parmis les chemins accessible
        sur le graphe correspondant
        
        _plateau(instance de la classe Plateau):
            référence du plateau sur lequel on joue. Important car on utiisera
            cette fonction dans le "RollOut" de l'UCT sur des copies du plateau
            d'origine.
        """
        paths = []
        for _node in list(_plateau.nodes()):
            paths += nx.all_simple_paths(_plateau.graph,
                                         self.position_graphe, _node)
        
        path = rd.choice(paths)
        