# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 23:53:33 2019

@author: HP
"""

#import pandas
import numpy as np
#import pygame
#from pygame.locals import *
import random
#import os
import networkx as nx
import matplotlib.pyplot as plt
#import math
import copy as cp
from classe_carte import carte
import SaC

###############################################################################
# Classe Plateau
###############################################################################
class Plateau(object) :
    '''
    Le fichier de configuration en exemple :
    fichier Config :
        dim_plateau,7
        nb_fantomes, 8
        nb_pepites, 10
        
        #types dict et list non pris en charge dans le format csv
        proportion cartes types [0.33,0.33,0.34] #pas les bonnes proportions
        cartes_disponibles, {'coin' : 20, 'couloir' : 25, 'carrefour' : 16}
                            #pas les bons chiffres
    '''
    
    def __init__(self, dim_plateau, _SaC = SaC.Save_and_Charge()): #chemin_fichier_config) :
        
        #self.config = pandas.read_csv(chemin_fichier_config, sep=';', 
                                     # header = None, index_col = 0).T
        
        
        self.taille = dim_plateau #int(self.config.dim_plateau)
        self.pts_pepite = 1
        self.pts_fantome = 5
        self.pts_ordre_mission = 15
        
        self.SaC = _SaC
        
        self.compteur_coup = 0
        
        self.Liste_Joueur_H = []
        self.Liste_Joueur_IA = []
        self.Liste_Joueur = self.Liste_Joueur_IA+self.Liste_Joueur_H
        self.Liste_Classement = []
        self.dict_ID2J = {}
        
        self.labyrinthe_detail = np.array([[object]*self.taille]*self.taille)
        entrees = []
        for i in [0,self.taille-1]:
            for j in [coord for coord in range(1,11,+2)]:
                entrees+=[(i,j),(j,i)]
        
        graph = nx.Graph()
        graph.add_nodes_from(list(range(self.taille**2)))
        node_pos = [(i,j) for i in range(self.taille) for j in range(self.taille)]
        
        for k in range(self.taille**2) : 
            graph.nodes[k]['pos'] = node_pos[k]
        
        self.node_pos = node_pos
        self.graph = graph
        self.carte_en_dehors=carte(random.choice(['coin','couloir','carrefour']),dict_elements={'fantome':[],'pepite':[],'joueur':[]})
        self.entrees = entrees
        self.liste_row_col = [] #liste des lignes et colonnes que l'on peut faire coulisser

        #pour visualiser le graphe
        #self.fig = plt.figure()
        #self.ax_graph = self.fig.add_subplot(111)
        
        
        
    def placer_carte_libre(self,liste_carte):
        for i in range (self.taille):
            for j in range (self.taille):
                if type(self.labyrinthe_detail[i,j]) == type :
                    
                    new_carte = random.choice(liste_carte)
                    new_carte.position_D=(i,j)
                    new_carte.position_G = self.node_pos.index((i,j))
                    self.labyrinthe_detail[i][j] = new_carte
                    
                    liste_carte.remove(new_carte)
    

    def etablir_connexion(self,carte):
        """
        carte(instance de carte):
            carte que l'on considère et que l'on cherche à relier à ces voisins
        """
        i, j = carte.position_D[0], carte.position_D[1]
        #Connexion Nord
        if carte.nom[0] == "1" and i != 0:
            if self.labyrinthe_detail[i-1][j].nom[1] == "1" :
                self.graph.add_edge(self.labyrinthe_detail[i-1][j].position_G,
                                    carte.position_G)
        
        #Connexion Ouest
        if carte.nom[3] == "1" and j != 0:
            if self.labyrinthe_detail[i][j-1].nom[2] == "1" :
                self.graph.add_edge(self.labyrinthe_detail[i][j-1].position_G,
                                    carte.position_G)
        
        #Connexion Est
        if carte.nom[2] == "1" and j != self.taille-1:
            if self.labyrinthe_detail[i][j+1].nom[3] == "1" :
                self.graph.add_edge(self.labyrinthe_detail[i][j+1].position_G,
                                    carte.position_G)
        
        #Connexion Sud
        if carte.nom[1] == "1" and i != self.taille-1:
            if self.labyrinthe_detail[i+1][j].nom[0] == "1" :
                self.graph.add_edge(self.labyrinthe_detail[i+1][j].position_G,
                                    carte.position_G)
 

    def set_objects_points(self, _pts_pepite = 1, _pts_fantome = 5,
                           _pts_ordre_mission = 15):
        self.pts_pepite = _pts_pepite
        self.pts_fantome = _pts_fantome
        self.pts_ordre_mission = _pts_ordre_mission

    def placer_pepites(self, nb_pepites) :
        '''
        place les pepites sur le plateau
        '''
        compteur = 0
        while compteur != nb_pepites:
            i = random.randint(0,self.taille-1)
            j = random.randint(0,self.taille-1)
            if self.labyrinthe_detail[i][j].elements['pepite']==[]:
                self.labyrinthe_detail[i][j].elements['pepite'] = True
                self.labyrinthe_detail[i][j].element_virtuels['pepite'] = True
                compteur+=1
    
    def placer_joueurs(self, liste_joueur) :
        '''
        Place les joueurs sur le plateau
        '''
        for joueur in liste_joueur:
            a = random.choice([2,self.taille-3])
            b = random.choice([2,self.taille-3])
            while self.labyrinthe_detail[a][b].elements['joueur'] != []:
                a = random.choice([2,self.taille-3])
                b = random.choice([2,self.taille-3])
            self.labyrinthe_detail[a][b].elements['joueur'].append(joueur.identifiant)
            self.labyrinthe_detail[a][b].element_virtuels['joueur'] = joueur.identifiant
            joueur.position_detail=(a,b)
            joueur.position_graphe=self.node_pos.index((a,b))
    
    def placer_fantomes(self,liste_ghost):
        compteur=0
        arret = len(liste_ghost)
        while compteur!=arret:
            i = random.randint(1,self.taille-1)
            j = random.randint(1,self.taille-1)
            if self.labyrinthe_detail[i][j].mobilite == True and self.labyrinthe_detail[i][j].elements['fantome']==[]:
                self.labyrinthe_detail[i][j].elements['fantome']=liste_ghost[0].id
                self.labyrinthe_detail[i][j].element_virtuels['fantome']=liste_ghost[0].id
                del liste_ghost[0]
                compteur+=1

    def generer_carte_fixe(self,nb_fantome,nb_pepites) :
        '''
        génère un plateau aléatoirement selon les contraintes imposées 
        dans le fichier de configuration
        '''
        
        #Generation des cartes sur le plateau
        taille = self.taille
        
        Nb_CF = (taille//2 + 1)**2
        Pair = (Nb_CF%2 == 0)
        
        dico_connectivite = {'couloir' : [[0,0,1,1],[1,1,0,0],[0,0,1,1],[1,1,0,0]],
                             'coin' : [[0,1,1,0],[0,1,0,1],[1,0,0,1],[1,0,1,0]],
                             'carrefour' : [[0,1,1,1],[1,1,0,1],[1,0,1,1],[1,1,1,0]]}
        
        #Construction des listes des cartes fixes sur le plateau, selon
        #que le nombre de cartes fixes est pair ou impair
        liste_CF_PP = [(i,j) for i in range(0,taille, 2) for j in range(0, taille, 2)]
        liste_CF_PI = [(i,j) for i in range(0,taille, 2) for j in range(0, taille, 2)]
    
        #On stocke la liste des index des cartes fixes sur le plateau
        if Pair :
            self.Index_Cartes_fixes = liste_CF_PP
        else :
            self.Index_Cartes_fixes = liste_CF_PI

        
        for i in range(taille) :
            for j in range(taille) :
                
                if ((i,j) in self.Index_Cartes_fixes):
                    
                    Nord_ouvert = (i > 0 and i <= taille-1)  
                    Sud_ouvert =  (i >= 0 and i < taille-1)
                    Est_ouvert = (j <= taille//2)
                    Ouest_ouvert = (j > taille//2)
                    
                    orientation_CF = [int(Nord_ouvert), int(Sud_ouvert),
                                         int(Est_ouvert), int(Ouest_ouvert)]
                    
                    if sum(orientation_CF) > 2 :
                        type_CF = 'carrefour'
                    else :
                        type_CF = 'coin'
                    carte_in = carte(type_CF, {'fantome':[],'pepite':[],'joueur':[]},
                                               self.node_pos.index((i,j)), 
                                               (i,j),
                                               dico_connectivite[type_CF].index(orientation_CF),
                                               mobilite=False)
                    self.labyrinthe_detail[i][j] = carte_in
                
             
    def coulisser_detail (self, coord_x, coord_y):
        """
        Change les positions des objets cartes dans la matrice “self.labyrinthe_detail”
        :param coord_x: abscisse du lieu où l'on souhaite faire coulisser la carte
        :param coord_y: ordonnée du lieu où l'on souhaite faire coulisser la carte
        :return:
        """
        #dict_vide = {'fantome' : "f" , 'pepite' : "f-", 'joueur': "f"}
        ## on modifie la ligne
        # en coulissant de gauche à droite
        if coord_y == -1:
            carte_sortante = self.labyrinthe_detail[coord_x,self.taille-1]#nouvelle carte libre
            for i in range(self.taille-1,0,-1) :#on opère le décalage dans la matrice
                self.labyrinthe_detail[coord_x,i] = self.labyrinthe_detail[coord_x,i-1]
                self.labyrinthe_detail[coord_x,i].position_D = (coord_x,i)
                self.labyrinthe_detail[coord_x,i].position_G = self.node_pos.index((coord_x,i))
            self.labyrinthe_detail[coord_x,0] = self.carte_en_dehors#on insère la carte dans la matrice
            self.labyrinthe_detail[coord_x,0].position_D = (coord_x,0)#on donne sa position dans la matrice à la carte
            self.labyrinthe_detail[coord_x,0].position_G = self.node_pos.index((coord_x,0))#on sa position dans le graphe à la carte
            
        
        # en coulissant de droite à gauche    
        if coord_y == self.taille :
            carte_sortante = self.labyrinthe_detail[coord_x,0]
            for i in range(self.taille-1) :
                self.labyrinthe_detail[coord_x,i] = self.labyrinthe_detail[coord_x,i+1]
                self.labyrinthe_detail[coord_x,i].position_D = (coord_x,i)
                self.labyrinthe_detail[coord_x,i].position_G = self.node_pos.index((coord_x,i))
            self.labyrinthe_detail[coord_x,self.taille-1] = self.carte_en_dehors
            self.labyrinthe_detail[coord_x,self.taille-1].position_D = (coord_x,self.taille-1)
            self.labyrinthe_detail[coord_x,self.taille-1].position_G = self.node_pos.index((coord_x,self.taille-1))
                
        
        ## on modifie la colonne
        # en coulissant de haut en bas
        if coord_x == -1 :
            carte_sortante = self.labyrinthe_detail[self.taille-1,coord_y]
            for i in range(self.taille-1, 0, -1) :
                self.labyrinthe_detail[i,coord_y] = self.labyrinthe_detail[i-1,coord_y]
                self.labyrinthe_detail[i,coord_y].position_D = (i,coord_y)
                self.labyrinthe_detail[i,coord_y].position_G = self.node_pos.index((i,coord_y))
            self.labyrinthe_detail[0,coord_y] = self.carte_en_dehors
            self.labyrinthe_detail[0,coord_y].position_D = (0,coord_y)
            self.labyrinthe_detail[0,coord_y].position_G = self.node_pos.index((0,coord_y))
                
        
        # en coulissant du bas vers le haut
        if coord_x == self.taille :
            carte_sortante = self.labyrinthe_detail[0,coord_y]
            for i in range(self.taille-1) :
                self.labyrinthe_detail[i,coord_y] = self.labyrinthe_detail[i+1,coord_y]
                self.labyrinthe_detail[i,coord_y].position_D = (i,coord_y)
                self.labyrinthe_detail[i,coord_y].position_G = self.node_pos.index((i,coord_y))
            self.labyrinthe_detail[self.taille-1,coord_y] = self.carte_en_dehors
            self.labyrinthe_detail[self.taille-1,coord_y].position_D = (self.taille-1,coord_y)
            self.labyrinthe_detail[self.taille-1,coord_y].position_G = self.node_pos.index((self.taille-1,coord_y))
        
        self.carte_en_dehors.elements = carte_sortante.elements
        self.carte_en_dehors.element_virtuels = carte_sortante.element_virtuels
        
        #print(self.carte_en_dehors.elements, self.carte_en_dehors.element_virtuels)
        #print("======================================================")
        #carte_sortante.elements = dict_vide
        self.carte_en_dehors = carte_sortante
        #print(self.carte_en_dehors.elements, self.carte_en_dehors.element_virtuels)
        # actualiser network graph


        
        #la nouvelle carte à coulisser sera la carte qui est sortie
        #self.carte_en_dehors = carte_sortante 
    
    
    def coulisser (self, coord_x, coord_y):
        """
        Effectue tous les changements associés à l’introduction
        d’une carte dans le plateau au début du tour d’un joueur.
        
        :param coord_x: abscisse du lieu où l'on souhaite faire coulisser la carte
        :param coord_y: ordonnée du lieu où l'on souhaite faire coulisser la carte
        """
        self.coulisser_detail(coord_x, coord_y)#on opère les chgmts dans la matrice
        self.SaC.log_plateau(self)#on contruit le log de la matrice
        self.graph.remove_edges_from(self.graph.edges())#on enlève toutes les connexions
        for i in range (self.taille):
            for j in range(self.taille):
                
                self.etablir_connexion(self.labyrinthe_detail[i,j])#on refait les connexions
                
                for _jID in (self.labyrinthe_detail[i,j].elements["joueur"]): #mise à jour des positions des joueurs sur la carte
                    _j = self.dict_ID2J[_jID]
                    _j.maj_position(self.labyrinthe_detail[i,j])
                    
        #on dessine
        #self.ax_graph.clear()
        #nx.draw_networkx(self.graph, pos = self.node_pos, ax = self.ax_graph)
            

    def translate_GraphPath2CardsPath(self, _graph_path):
        cards_path = []
        for _node_number in _graph_path:
            coords = self.node_pos[_node_number]
            cards_path += [self.labyrinthe_detail[coords[0]][coords[1]]]
        return cards_path
    
    def convertir_Fleche2Coord(self, _fleche, _backward = False):
        """
        Convertit l'identifiant du bouton fleche en les coordonnées de la ligne
        ou de la colonne à déplacer dans *labyrinthe_detail*
        
        _fleche(str):
            identifiant du type 'H1' pour la flèche en haut du plateau à gauche
            dans la visualisation PyGame
        
        _backward(bool):
            Si True, renvoie la fleche oppposée. Utile dans UCT
        """
        convertFlecheCoord={'G':[int(_fleche[1:]),-1],'D':[int(_fleche[1:]),self.taille],
                            'H':[-1,int(_fleche[1:])],'B':[self.taille,int(_fleche[1:])]}
        if (_backward):
            opposit_dict={'G':'D', 'D':'G', 'H':'B', 'B':'H'}
            _fleche = opposit_dict[_fleche[0]] + _fleche[1:]
            
        coord_x=convertFlecheCoord[_fleche[0]][0]
        coord_y=convertFlecheCoord[_fleche[0]][1]
        
        return coord_x, coord_y
    
    def maj_classement(self):
        """
        trie la liste Liste Classement des joueurs dans l'ordre décroissant de leurs
        nombre de points respectifs.
        """
                
        liste_Classement = np.array([_j.nb_points for _j in self.Liste_Joueur])
        rank = liste_Classement.argsort()
        self.Liste_Classement = [(liste_Classement[_r], self.Liste_Joueur[_r]) for _r in rank]
        self.Liste_Classement = self.Liste_Classement[::-1]
    
    def check_gagnant(self):
        """
        regarde si l'un des joueurs peut rattraper le joueur en tête.
        Return True s'il y a un gagnat (i.e. aucun des adversaire ne peut dépasser
        le joueur en tête)        
        """
        gagnant = False
        
        nb_joueur = len(self.Liste_Joueur)
        save_nb_points = [self.Liste_Classement[i][0] for i in range(nb_joueur)]
        
        for i in range(self.taille):#on traverse toutes les cartes
            for j in range(self.taille):
                for k in range (1, nb_joueur):#on ajoute les points de la carte aux joueurs
                    self.Liste_Classement[k][1].compter_pts_carte(self.labyrinthe_detail[i][j],
                                                                  _reset_value = False)

        c = 0
        for k in range (1, nb_joueur):#on regarde si le joueur en tête à toujours plus de points que les autres
            if self.Liste_Classement[0][0] > self.Liste_Classement[k][1].nb_points:
                c+=1
            self.Liste_Classement[k][1].nb_points = save_nb_points[k]#on remet les ancien compte de points

        if c == nb_joueur-1:#si le compteur est egal au nb d'adversaires alors le joueur en tête à gagné
            gagnant = True
        
        return gagnant
    
    def generate_liste_row_col(self):
        self.liste_row_col = []
        for i in range(1, self.taille, 2):
            for _char in ["G", "D", "H", "B"]:
                self.liste_row_col += [_char + str(i)]
    
# =============================================================================
#     def __deepcopy__(self, memo):
#         cls = self.__class__
#         result = cls.__new__(cls)
#         memo[id(self)] = result
#         for k, v in self.__dict__.items():
#             setattr(result, k, cp.deepcopy(v, memo))
#         return result
# =============================================================================
        
    def chemin_possible(self,id_joueur):
        for i in self.labyrinthe_detail: #recherche de la position du joueur
            for j in i:
                if id_joueur in j.elements["joueur"]:
                    pos_joueur = j.position_D
        compteur=0
        for v in self.graph.nodes : 
            if self.graph.nodes[compteur]['pos']==pos_joueur: 
                nodi=v
            compteur +=1
        spl = nx.single_source_shortest_path(self.graph,source = nodi)
        dico={}
        for keys in spl.keys():
            z =  spl[keys]
            inter=[]
            for i in z:
                inter.append(self.node_pos[i])
            dico[self.node_pos[keys]]=inter
        return(dico)
        
    def deplacement_joueur(self,plat,joueur,move):
        """
        joueur : 
            objet joueur
        move :
            code touche du clavier
        """
        
        pos_init=joueur.position_detail #ancienne position
        node_init = self.node_pos.index(pos_init)
        
        move_dict={275:(pos_init[0],pos_init[1]+1), #dico des mouvements
                   273:(pos_init[0]-1,pos_init[1]),
                   274:(pos_init[0]+1,pos_init[1]),
                   276:(pos_init[0],pos_init[1]-1)}
        #verif contraintes
        if pos_init[0]==0:
            move_dict[273]=pos_init
        elif pos_init[0]==self.taille-1:
            move_dict[274]=pos_init
        elif pos_init[1]==0:
            move_dict[276]=pos_init
        elif pos_init[1]==self.taille-1:
            move_dict[275]=pos_init
        pos_target=move_dict[move] #position de la carte visée par le déplacement
        node_target=self.node_pos.index(pos_target)
        
        
        chemins=plat.chemin_possible(joueur.identifiant).values()
        path=[]
        for coord in chemins:
            for elem in coord :
                path.append(elem)
        path=set(path)
        
        if pos_target in path:
            joueur.effectuer_chemin(self,[node_init,node_target])
        
      