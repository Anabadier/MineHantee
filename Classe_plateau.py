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
        self.SaC = _SaC
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
        
        #pour visualiser le graphe
        self.fig = plt.figure()
        self.ax_graph = self.fig.add_subplot(121)
        self.ax_graph2 = self.fig.add_subplot(122)
        
        
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
            self.labyrinthe_detail[a][b].elements['joueur'] = joueur.identifiant
            joueur.position_detail=(a,b)
        
    
    def placer_fantomes(self,liste_ghost):
        compteur=0
        arret = len(liste_ghost)
        while compteur!=arret:
            i = random.randint(1,self.taille-1)
            j = random.randint(1,self.taille-1)
            if self.labyrinthe_detail[i][j].mobilite == True and self.labyrinthe_detail[i][j].elements['fantome']==[]:
                self.labyrinthe_detail[i][j].elements['fantome']=liste_ghost[0].id
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
        liste_CF_PI = [(i,j) for i in range(1,taille, 2) for j in range(1, taille, 2)]
    
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
                    Est_ouvert = (j < taille//2)
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
        dict_vide = {'fantome' : False , 'pepite' : False, 'joueur': False}
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
        carte_sortante.elements = dict_vide
        self.carte_en_dehors = carte_sortante
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
        self.ax_graph2.clear()
        nx.draw_networkx(self.graph, pos = self.node_pos, ax = self.ax_graph2)#vérifier que les arrêtes ont été enlevées
        for i in range (self.taille):
            for j in range(self.taille):
                self.etablir_connexion(self.labyrinthe_detail[i,j])#on refait les connexions
        
        #on dessine
        self.ax_graph.clear()
        nx.draw_networkx(self.graph, pos = self.node_pos, ax = self.ax_graph)
        
    def chemin_possible(self,id_joueur):
    #        for i in self.labyrinthe_detail:
    #            if i.dict_elements["joueur"]==id_joueur:
    #                pos_joueur = i
        compteur=0
        for v in self.graph.node : 
            if self.graph.node[compteur]['pos']==(1,0):# pos_joueur 
                nodi=v
            compteur +=1
        #for v in self.graph.node:
        spl = nx.single_source_shortest_path(self.graph,source = nodi)
        dico={}
        for keys in spl.keys():
            #print(keys)
            z =  spl[keys]
            #print(spl[keys])
            inter=[]
            for i in z:
                inter.append(self.node_pos[i])
            dico[self.node_pos[keys]]=inter
        return(dico)
        