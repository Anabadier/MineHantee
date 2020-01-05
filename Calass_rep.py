# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:30:15 2019

@author: augus
"""

import random as rd
import networkx as nx
import copy as cp
import numpy as np
#from classe_carte import carte
#from Classe_plateau import Plateau

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
      
    def __init__(self, _identifiant = "none"):
        if _identifiant == "none" :
            print("Veuillez indentifier le joueur")
        else :
            print(_identifiant)
            self.identifiant = _identifiant 
            self.joueur_suivant = None
            self.joueur_precedant = None
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
       
    def maj_points(self, points):
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
    
    def determiner_joueur_voisins_ordre(self):
        index = self.ref_plateau.Liste_Joueur.index(self)
        if (index == len(self.ref_plateau.Liste_Joueur)-1):
            self.joueur_suivant = self.ref_plateau.Liste_Joueur[0]
        else:
            self.joueur_suivant = self.ref_plateau.Liste_Joueur[index+1]
            
        if (index == 0):
            self.joueur_precedant = self.ref_plateau.Liste_Joueur[len(self.ref_plateau.Liste_Joueur)-1]
        else:
            self.joueur_precedant = self.ref_plateau.Liste_Joueur[index-1]
    
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
    
    def __init__(self, _identifiant = "none", _niv ="Normale"):
        Joueur.__init__(self, _identifiant = _identifiant)
        self.niv = _niv
        
        self.liste_row_col = [] #liste des lignes et colonnes que l'on peut faire coulisser
        self.liste_paths = [] #liste des chemins accessibles au joueur. Utile après rot card et coullissage
        
    def generate_liste_row_col(self):
        self.liste_row_col = []
        for i in range(1, self.ref_plateau.taille, 2):
            for _char in ["G", "D", "H", "B"]:
                self.liste_row_col += [_char + str(i)]
    
    def generate_list_paths(self, _plateau):
        self.liste_paths = []
        for _node in list(_plateau.nodes()):
            self.liste_paths += nx.all_simple_paths(_plateau.graph,
                                                    self.position_graphe, _node)
    
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
        self.generate_list_paths(plateau)
        path = rd.choice(self.liste_paths)
        

class UCT_node(object):
    def __init__(self):
        
        self.parent = []
        self.enfants  = []
        self.nb_visit = 0
        self.nb_gagne = 0
        
        self.description_coup = []# pour la mine hantée ["nb_rotation","fleche","chemin"]
        self.plateau_ap_coup = None
        self.joueur_createur = None
        
        self.ucb_score = 10000
    
    def calcul_ucb_score(self):
        self.ucb_score = self.nb_gagne / self.nb_visit + \
                         self.C * np.sqrt(np.ln(self.parent.nb_visit)/self.nb_visit)
  
class UCT(object):
    """
    Application de l'IA Monte Carlo Tree Search-Upper Confidence Bound pour
    le jeu de la mine hantée.
    
    Le principe de MCTS UCB est d'explorer progressivement l'arbre des coups
    possible pour une IA. On part de la situation actuelle du plateau et on
    simule les coups suivant. On accorde plus de temps de recherche
    (simulation de Monte Carlo) aux noeuds de l'arbre (coup) qui semblent 
    apporter la victoire : on guide l'exploration de l'arbre.
    
    L'exploration des possiblités (i.e. la construction de l'arbre) se fait
    en 4 étapes :
        1)
            Selection. On parcours l'arbre de manière récursive en
            choisissant toujours le noeud qui maximise un score (UCB
            appliqué aux arbres)
                v_i = s_i / n_i + C * sqrt(ln(n_p)/n_i)
            *s_i est le nombre de victoires du joureur qui joue le coup
            associé au noeud
            *n_i est le nombre de fois que le noeud a été visité
            *n_p est le nombre de fois que le noeud parent a été visité
            *C une constante
        
        2)
            Extension. On ajoute tous les enfants possible du noeud selection
            à l'étape 1.
        
        3)
            Rollout. Après avoir simulé le coup joué en 1, on joue le reste
            de la simulation au hasard ou en stratégie "greedie" jusqu'à ce
            qu'un ou plusieurs gagnants soient déclarés.
        
        4)
            Retropropagation. On fait remonter le nombre de victoires de
    """
    def __init__(self, _plateau, _joueur_racine, _C = np.sqrt(2),
                 _nb_rollout = 10, _temps_ressource = 10):
        
        self.C = _C
        self.nb_rollout = _nb_rollout
        self.temps_ressource = _temps_ressource
        
        self.racine = UCT_node()
        self.racine.plateau_ap_coup = cp.deepcopy(_plateau)
        self.racine.joueur_createur = _joueur_racine
        
        self.meilleur_noeud = None
        self.noeud_selectionne = None
    
    def recherche_UCT(self):
        """
        Réalise les 4 étapes de l'UCT et met à jour le meilleur_noeud
        """
        self.selection()
        
        if (self.noeud_selectionne.nb_visit != 0):
            self.extension()
            self.noeud_selectionne = self.noeud_selectionne.enfants[0]
        
        self.rollout()
        self.retro_propagation()
    
    def selection(self):
        """
        avance dans l'arbre en choisissant le noeud qui maximise UCB
        """
        self.noeud_selectionne = self.racine
        while len(self.noeud_selectionne.enfants) != 0:
            _max = 0
            noeud_max = None
            for _enfant in self.noeud_selectionne.enfants:
                if (_enfant.nb_visit != 0):
                    _enfant.calcul_ucb_score()
                
                if (_enfant.ucb_score > _max):
                    _max = _enfant.ucb_score
                    noeud_max = _enfant
            
            self.noeud_selectionne = noeud_max
    
    def extension(self):
        """
        ajoute tous les enfants au noeud selectionné quand il a déjà été visité
        (il y a déjà eu rollout).
        Ajouter les enfants d'un noeuds signifie d'ajouter toutes les actions
        accessible au jour suivant.
        """
        joueur = self.noeud_selectionne.joueur_createur.joueur_suivant
        
        for _nb_rot_card in range(1,5):
            for _fleche in joueur.liste_row_col:
                
                _plateau = cp.deepcopy(self.noeud_selectionne.plateau_ap_coup)
                
                for i in range(_nb_rot_card):
                    self.oriente_carte_libre(_plateau.carte_en_dehors, "horaire")
                
                convertFlecheCoord={'G':[int(_fleche[1:]),-1],'D':[int(_fleche[1:]),_plateau.taille],
                            'H':[-1,int(_fleche[1:])],'B':[_plateau.taille,int(_fleche[1:])]}
                coord_x=convertFlecheCoord[_fleche[0]][0]
                coord_y=convertFlecheCoord[_fleche[0]][1]
                
                _plateau.coulisser(coord_x, coord_y)
                
                joueur.generate_list_paths(_plateau)
                
                for _path in joueur.liste_paths:
                    
                
                
    
    def rollout(self):
        """
        joue plusieurs parties au hasard en partant de la situation du plateau
        telle que décrite dans le noeud étendu
        """
        pass
    
    def retro_propagation(self):
        """
        met à jour les noeuds traversés lors de la selection (tous les parents
        de la feuille)
        """
        pass
    
    
    
    
    
    
    
    