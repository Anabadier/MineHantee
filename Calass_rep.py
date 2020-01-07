# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:30:15 2019

@author: augus
"""

import random as rd
import networkx as nx
import copy as cp
import numpy as np
import pickle
from time import time
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
    
    def determiner_joueur_voisins_ordre(self):
        index = self.ref_plateau.Liste_Joueur.index(self)
        if (index == len(self.ref_plateau.Liste_Joueur)-1):
            self.joueur_suivant = self.ref_plateau.Liste_Joueur[0].identifiant
        else:
            self.joueur_suivant = self.ref_plateau.Liste_Joueur[index+1].identifiant
            
        if (index == 0):
            self.joueur_precedant = self.ref_plateau.Liste_Joueur[len(self.ref_plateau.Liste_Joueur)-1].identifiant
        else:
            self.joueur_precedant = self.ref_plateau.Liste_Joueur[index-1].identifiant
            
    def generer_odre_mission(self,nb_ordre,nb_ghost):
        ordre_mission = []
        for i in range(nb_ordre):
            fantome = rd.randint(1,nb_ghost)
            while fantome in ordre_mission:
                fantome = rd.randint(1,nb_ghost)
            ordre_mission.append(fantome)
        self.ordre_de_mission = ordre_mission
    
    def maj_points(self, points, _sign = 1):
        """
        Mise à jour du nombre de points
        
        points (int):
            le nombre de points que l'on souhaite ajouter
            
        _sign (-1 ou 1):
            contrôle si l'on additionne les points ou les retranche
        """
        self.nb_points = self.nb_points + _sign * points
    
    def compter_pts_carte(self, _card, _reset_value = True):
        """
        ajoute les points contenu dans _card
        """
        print("add, ", self.nb_points)
        if (_card.elements["pepite"]):
                self.maj_points(self.ref_plateau.pts_pepite)
                print('add, ', _card.nom, _card.position_D, self.ref_plateau.pts_pepite, self.nb_points)
                if _reset_value:
                    _card.elements["pepite"] = False
            
        if (_card.elements["fantome"] != []):
            if (_card.elements["fantome"] in self.ordre_de_mission):
                self.maj_points(self.ref_plateau.pts_ordre_mission)
                print('add, ', _card.nom, _card.position_D, self.ref_plateau.pts_ordre_mission, self.nb_points)
            else:
                self.maj_points(self.ref_plateau.pts_fantome)
                print('add, ', _card.nom, _card.position_D, self.ref_plateau.pts_fantome, self.nb_points)
            if _reset_value:
                    _card.elements["fantome"] = []
    
    def retrancher_pts_carte(self, _card, _reset_value = True):
        """
        retranche les points qui était contenus dans _card en se basant sur les
        souvenir de _card.element_virtuels
        """
        print("ret, ", self.nb_points)
        if (_card.element_virtuels["pepite"]):
                self.maj_points(self.ref_plateau.pts_pepite, -1)
                print('ret, ',_card.nom, _card.position_D, self.ref_plateau.pts_pepite, self.nb_points)
                if _reset_value:
                    _card.elements["pepite"] = True
            
        if (_card.element_virtuels["fantome"] != []):
            if (_card.element_virtuels["fantome"] in self.ordre_de_mission):
                self.maj_points(self.ref_plateau.pts_ordre_mission, -1)
                print('ret, ',_card.nom, _card.position_D, self.ref_plateau.pts_ordre_mission)
            else:
                self.maj_points(self.ref_plateau.pts_fantome, -1)
                print('ret, ',_card.nom, _card.position_D, self.ref_plateau.pts_fantome)
            if _reset_value:
                    _card.elements["fantome"] = _card.element_virtuels["fantome"]
    
    def maj_position(self, _carte):
         self.position_graphe = _carte.position_G
         self.position_detail = _carte.position_D
   
    def oriente_carte_libre(self, carte_libre, sens):
        test = ["horaire","anti-horaire"]
        if sens not in test:
            print("Mauvaises instructions de sens")
        else:
            carte_libre.pivoter(sens)    
    
    def modifier_plateau(self, _plateau, _fleche, _backward = False):
        """
        introduit la carte libre dans une colonne ou une ligne qui correspond à
        _fleche
        
        _plateau(instance de la classe Plateau): facultatif
            référence du plateau sur lequel on joue. Important car on utiisera
            cette fonction dans le "RollOut" de l'UCT sur des copies du plateau
            d'origine.
        
        _fleche(str):
            identifiant du type 'H1' pour la flèche en haut du plateau à gauche
            dans la visualisation PyGame
        
        _backward(bool):
            Si True, renvoie la fleche oppposée. Utile dans UCT
        """
        
        coord_x, coord_y = _plateau.convertir_Fleche2Coord(_fleche, _backward)
        _plateau.coulisser(coord_x, coord_y)
    
    def effectuer_chemin(self, _plateau,  _path, _backward = False):
        """
        Opère les modifications sur le plateau et la comptabilisation des points
        une fois que le joueur a décidé d'un chemin
        
        _plateau(instance de la classe Plateau):
            référence du plateau sur lequel on joue. Important car on utiisera
            cette fonction dans le "RollOut" de l'UCT sur des copies du plateau
            d'origine.
        
        _path(list):
            liste des sommets du graphe que le joueur choisi de suivre
        
        _backward(bool):
            Si True, joue le chemin inversé. Utile dans UCT
        """
        
        if (_backward):
            _path = _path[::-1]
        
        card_path = _plateau.translate_GraphPath2CardsPath(_path)
        for _card in card_path:
            self.maj_position(_card)
            if (_backward):
                self.retrancher_pts_carte(_card)
            else:
                self.compter_pts_carte(_card)
        _plateau.maj_classement()#on met a jour le classement à la fin du tour d'un joueur
        #print(_plateau.Liste_Classement)
        
    def heuristique(self,chemin,plateau):
        """
        La fonction d'evaluation permet de calculer le gain total si on suit un
        chemin donné.
        Fonction simple qui somme la valeur en point des entités recueillies sur
        le chemin.
        Le calcul se fait en fonction du nombre de pépites recueillies ainsi que du
        nombre de fantomes recueillis.
        
        :param un_chemin: chemin a evaluer
        
        :param labyrinthe_detail: matrice avec les cartes que l'on va traverser
        pour savoir s'il y a une pépite/fantome dessus
        
        :param chemin_fichier_config: chemin vers le fichier de configuration pour
        connaitre la valeur d'une pepite, fantome, fantome dans mission
        
        :returns gain: gain que l'on peut obtenir si on suit un chelin
        """
        gain = 0
        for coord in chemin :
            carte = plateau.labyrinthe_detail[coord]
        for carte in chemin :
            if carte.elements['pepite'] is True :
                gain+= plateau.pts_pepite
            if carte.elements['fantome'] is not np.nan :
                if carte.elements['fantome'] in self.ordre_de_mission : 
                    gain+= plateau.pts_ordre_mission
                else:
                    gain+= plateau.pts_fantome
        return(gain)

class Joueur_IA(Joueur):
    
    def __init__(self, _identifiant = "none", _niv ="Normale"):
        Joueur.__init__(self, _identifiant = _identifiant)
        self.niv = _niv
        
        self.UCT_solver = None
        
        self.liste_paths = [] #liste des chemins accessibles au joueur. Utile après rot card et coullissage
    
    def generate_list_paths(self, _plateau):
        self.liste_paths = []
        for _node in list(_plateau.graph.nodes()):
            self.liste_paths += nx.all_simple_paths(_plateau.graph,
                                                    self.position_graphe, _node)
    
    def greedy(self, plateau):
        best_coup = (0,[])
        for i in range (1,5):
            self.rotation_carte(plateau,i)
            for j in plateau.liste_row_col:
                fleche = j
                self.modifier_plateau(plateau,fleche)
                liste_chemin = plateau.chemin_possible(self.identifiant)
                for t in liste_chemin:
                    gain = self.heuristique(t,plateau)
                    if gain > best_coup[0]:
                        best_coup[0],best_coup[1]=gain,t
        self.effectuer_chemin(plateau,best_coup[1])
    
    def jouer(self):
        """
        faire jouer une IA en fonction de son niveau
        """
        if (self.niv == "Facile"):
            
            coup_alea = self.coup_alea(self.ref_plateau)#a changer pour une approche greedy
            #self.greedy(self.ref_plateau)
            
            self.coup_cible(self.ref_plateau, coup_alea)
            self.coup_cible(self.ref_plateau, coup_alea, True)
                
        elif (self.niv == "Normale"):
            #Mettre AlphaBeta ici
            pass
            
        elif (self.niv == "Difficile"):
            description_coup = self.UCT_solver.jouer_UCT(self.ref_plateau, self)
            self.coup_cible(self.ref_plateau, description_coup)
    
    def coup_cible(self, _plateau, _description_coup, _backward = False):
        """
        _plateau(instance de la classe Plateau):
            référence du plateau sur lequel on joue. Important car on utiisera
            cette fonction dans le "RollOut" de l'UCT sur des copies du plateau
            d'origine.
            
        _description_coup(list):
            Liste au format [_nb_rotation horaire carte,
                             fleche identifiant,
                             chemin]
        _backward(bool):
            Si True, joue la séquence inverse pour annuler le coup décrit par
            _description_coup. Utile dans UCT
        """
        if (_backward):
            self.effectuer_chemin(_plateau, _description_coup[2], _backward)
            self.modifier_plateau(_plateau, _description_coup[1], _backward)
            self.rotation_carte(_plateau, _description_coup[0], _backward)
        else:
            self.rotation_carte(_plateau, _description_coup[0])
            self.modifier_plateau(_plateau, _description_coup[1])
            self.effectuer_chemin(_plateau, _description_coup[2])
    
    def coup_alea(self, _plateau):
        """
        Retourne le coup complet aléatoirement (rotation de la carte libre, choix
        de la ligne ou de la colonne à jouer, déplacement)
        
        _plateau(instance de la classe Plateau):
            référence du plateau sur lequel on joue. Important car on utiisera
            cette fonction dans le "RollOut" de l'UCT sur des copies du plateau
            d'origine.
        """
        nb_rotation = rd.choice([1,2,3,4])
        fleche = rd.choice(_plateau.liste_row_col)
        self.rotation_carte(_plateau, nb_rotation)
        self.modifier_plateau(_plateau, fleche)
        path = []
        self.generate_list_paths(_plateau)
        if (self.liste_paths != []):
            path = rd.choice(self.liste_paths)
            self.effectuer_chemin(_plateau, path)
        
        return [nb_rotation, fleche, path]
        
    def rotation_carte(self, _plateau, _nb_rotation, _backward = False):
        """
        tourne la carte libre autant de fois que _nb_rotation
        
        _plateau(instance de la classe Plateau):
            référence du plateau sur lequel on joue. Important car on utiisera
            cette fonction dans le "RollOut" de l'UCT sur des copies du plateau
            d'origine.
        
        _nb_rotation(int):
            nombre de fois que l'on doit tourner la carte dans le sens horaire
        
        _backward(bool):
            Si True, joue la carte dans le sens anti horaire. Utile dans UCT
        """
        if _backward:
            _sens = "anti-horaire"
        else:
            _sens = "horaire"
        
        for i in range(_nb_rotation):
            self.oriente_carte_libre(_plateau.carte_en_dehors, _sens)

class UCT_node(object):
    def __init__(self, _C = np.sqrt(2)):
        
        self.parent = None
        self.enfants  = []
        self.nb_visit = 0
        self.nb_gagne = 0
        
        self.description_coup = []# pour la mine hantée ["nb_rotation","fleche","chemin"]
        self.plateau = None
        self.joueur_createur = None
        
        self.ucb_score = 10000
        
        self.C = _C
    
    def calcul_ucb_score(self):
        self.ucb_score = self.nb_gagne / self.nb_visit + \
                         self.C * np.sqrt(np.log2(self.parent.nb_visit)/self.nb_visit)
  
class UCT_2(object):
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
    def __init__(self,  _nb_rollout = 10,
                 _temps_ressource = 10):
        
        
        self.nb_rollout = _nb_rollout
        self.temps_ressource = _temps_ressource
        self.action_list = []
    
    def initialise_UCT(self, _plateau, _joueur_UCT):
        self.racine = UCT_node()
        self.racine.plateau = _plateau
        self.racine.joueur_createur = _plateau.dict_ID2J[_joueur_UCT.identifiant].joueur_precedant
        
        self.meilleur_noeud = None
        self.noeud_selectionne = None
    
    def jouer_UCT(self, _plateau, _joueur_UCT):
        """
        Retourne le meilleur coup d'après UCT
        """
        self.initialise_UCT(_plateau, _joueur_UCT)
        
        temps_debut = time()
        while(time()-temps_debut < self.temps_ressource):
            self.recherche_UCT()
            
        _max = 0
        for _enfant in self.racine.enfants:
            if (_enfant.nb_visit != 0):
                _enfant.calcul_ucb_score()
            
            if (_enfant.ucb_score > _max and _enfant.ucb_score != 10000):#on refuse de choisir un noeud non evalué
                _max = _enfant.ucb_score
                self.meilleur_noeud = _enfant
                
        return self.meilleur_noeud.description_coup
        
    
    def recherche_UCT(self):
        """
        Réalise les 4 étapes de l'UCT et met à jour le meilleur_noeud
        """
        #1
        self.selection()
        
        #2 si nécessaire
        if (self.noeud_selectionne.nb_visit != 0 or self.noeud_selectionne == self.racine):
            self.extension(self.noeud_selectionne)
            self.noeud_selectionne = self.noeud_selectionne.enfants[0]
        
        #3
        compteur_victoires = self.rollout(self.noeud_selectionne, self.nb_rollout)
        
        #4
        self.retro_propagation(self.noeud_selectionne, compteur_victoires)
    
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
                    #print(_enfant.ucb_score)
                
                if (_enfant.ucb_score > _max):
                    _max = _enfant.ucb_score
                    noeud_max = _enfant
            
            self.noeud_selectionne = noeud_max
            
            self.racine.plateau.dict_ID2J[self.racine.joueur_createur].coup_cible(
                                                            self.racine.plateau,
                                                            self.noeud_selectionne.description_coup)
            
            self.action_list.append([self.noeud_selectionne.joueur_createur]+\
                                    self.noeud_selectionne.description_coup)
            
    def extension(self, _noeud_source):
        """
        ajoute tous les enfants au noeud selectionné quand il a déjà été visité
        (il y a déjà eu rollout).
        Ajouter les enfants d'un noeuds signifie d'ajouter toutes les actions
        accessible au jour suivant.
        
        _noeud_source(UCT_node):
            noeud à partir duquel on étend les choix possibles
        """
        c = 0
        joueur = self.racine.plateau.dict_ID2J[
                    self.racine.plateau.dict_ID2J[_noeud_source.joueur_createur].joueur_suivant]
        
        for _nb_rot_card in range(1,5):
            for _fleche in self.racine.plateau.liste_row_col:
                
                joueur.generate_list_paths(self.racine.plateau)
                if (joueur.liste_paths != []):
                    for _path in joueur.liste_paths:
                        _enfant = UCT_node()
                        _noeud_source.enfants += [_enfant]
                        _enfant.parent = _noeud_source
                        _enfant.description_coup = [_nb_rot_card, _fleche, _path]
                        _enfant.joueur_createur = joueur.identifiant
                        c+=1
                
                else:
                    _enfant = UCT_node()
                    _noeud_source.enfants += [_enfant]
                    _enfant.parent = _noeud_source
                    _enfant.description_coup = [_nb_rot_card, _fleche, []]
                    _enfant.joueur_createur = joueur.identifiant
                c+= 1
        print(c, "enfants ont été générés")
                    
    
    def rollout(self, _noeud_source, _nb_parties = 1, _nb_coup_max = 100):
        """
        joue plusieurs parties au hasard en partant de la situation du plateau
        telle que décrite dans le noeud étendu
        
        _noeud_source(UCT_node):
            noeud pour lequel on effectue le roll out
        """
        
        #on joue le coup stocké dans _noeud_source
        _plateau = self.racine.plateau
        j_playing = _plateau.dict_ID2J[_noeud_source.joueur_createur]
        j_playing.coup_cible(_plateau, _noeud_source.description_coup)
        self.action_list += [_noeud_source.description_coup]
        
        print(478, j_playing.nb_points,
              _plateau.dict_ID2J[j_playing.joueur_suivant].nb_points, end = " ; ")
        
        #on initilise la comptabilisation des victoires
        compteur_victoires = {}
        for _j in _plateau.Liste_Joueur:
            compteur_victoires[_j.identifiant] = 0
        
        #ROLLOUT en tant que tel
        for k in range(_nb_parties):
            nb_coup_rollout = 0
            rollout_action_list = []
            #joue aleatoirement jusqu'a une victoire ou un nb_coup_rollout >= _nb_coup_max
            while (not _plateau.check_gagnant() and nb_coup_rollout < 2):
                j_playing = _plateau.dict_ID2J[j_playing.joueur_suivant]
                
                coup_alea = j_playing.coup_alea(_plateau)
                rollout_action_list += [[j_playing]+coup_alea]
                j_playing.coup_cible(_plateau, coup_alea)
                
                print(495, j_playing.identifiant, j_playing.nb_points, end = " ; ")
                
                nb_coup_rollout+=1
                
            #comptabilise la victoire du vainqueur
            compteur_victoires[_plateau.Liste_Classement[0][1].identifiant] += 1#on incrémente le compteur de victoire
            
            #remet le plateau dans l'etat AVANT ROLLOUT
            for i in range(nb_coup_rollout-1, -1, -1):
                j_retro_playing = rollout_action_list[i][0]
                j_retro_playing.coup_cible(_plateau, rollout_action_list[i][1:], True)
                print(508, j_retro_playing.identifiant, j_retro_playing.nb_points, end = " ; ")
        print()
        print(compteur_victoires)
        return compteur_victoires
        
    def retro_propagation(self, _feuille, _compteur_victoires):
        """
        met à jour les noeuds traversés lors de la selection (tous les parents
        de la feuille)
        
        _feuille(UCT_node):
            noeud à partir duquel on remonte à la racine
            
        _compteur_victoires(dico, key = joueur, value = nombre de vitoire):
            le compteur de victoire à propager sur le reste des noeuds.
            Ce dictionnaire est généré par le rollout
        """
        noeud = _feuille
        while noeud.parent != None:
            noeud.nb_visit += 1
            noeud.nb_gagne += _compteur_victoires[noeud.joueur_createur]
            
            j_retro_playing = self.racine.plateau.dict_ID2J[noeud.joueur_createur]
            j_retro_playing.coup_cible(self.racine.plateau, noeud.description_coup, True)
            
            noeud = noeud.parent
            
        noeud.nb_visit += 1
        noeud.nb_gagne += _compteur_victoires[noeud.joueur_createur]


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
    def __init__(self,  _nb_rollout = 10,
                 _temps_ressource = 10):
        
        
        self.nb_rollout = _nb_rollout
        self.temps_ressource = _temps_ressource
    
    def initialise_UCT(self, _plateau, _joueur_UCT):
        self.racine = UCT_node()
        self.racine.plateau = _plateau.__deepcopy__({})
        self.racine.joueur_createur = _plateau.dict_ID2J[_joueur_UCT.identifiant].joueur_precedant
        
        self.meilleur_noeud = None
        self.noeud_selectionne = None
    
    def jouer_UCT(self, _plateau, _joueur_UCT):
        """
        Retourne le meilleur coup d'après UCT
        """
        self.initialise_UCT(_plateau, _joueur_UCT)
        
        temps_debut = time()
        while(time()-temps_debut < self.temps_ressource):
            
            self.recherche_UCT()
            
        _max = 0
        for _enfant in self.racine.enfants:
            if (_enfant.nb_visit != 0):
                _enfant.calcul_ucb_score()
                print(304, _enfant.joueur_createur, _enfant.ucb_score)
            
            if (_enfant.ucb_score > _max and _enfant.ucb_score != 10000):#on refuse de choisir un noeud non evalué
                _max = _enfant.ucb_score
                self.meilleur_noeud = _enfant
        
        print(306, self.meilleur_noeud.nb_gagne, self.meilleur_noeud.description_coup)
        return self.meilleur_noeud.description_coup
        
    
    def recherche_UCT(self):
        """
        Réalise les 4 étapes de l'UCT et met à jour le meilleur_noeud
        """
        #1
        self.selection()
        #2 si nécessaire
        if (self.noeud_selectionne.nb_visit != 0 or self.noeud_selectionne == self.racine):
            self.extension(self.noeud_selectionne)
            self.noeud_selectionne = self.noeud_selectionne.enfants[0]
        
        #3
        compteur_victoires = self.rollout(self.noeud_selectionne, self.nb_rollout)
        
        #4
        self.retro_propagation(self.noeud_selectionne, compteur_victoires)
    
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
                    #print(_enfant.ucb_score)
                
                if (_enfant.ucb_score > _max):
                    _max = _enfant.ucb_score
                    noeud_max = _enfant
            
            self.noeud_selectionne = noeud_max
    
    def extension(self, _noeud_source):
        """
        ajoute tous les enfants au noeud selectionné quand il a déjà été visité
        (il y a déjà eu rollout).
        Ajouter les enfants d'un noeuds signifie d'ajouter toutes les actions
        accessible au jour suivant.
        
        _noeud_source(UCT_node):
            noeud à partir duquel on étend les choix possibles
        """
        c = 0
        print(self.racine.enfants)
        for _nb_rot_card in range(1,5):
            for _fleche in _noeud_source.plateau_ap_coup.liste_row_col:
                #print('in', c)
                #tps_d1 = time()
                #_plateau = cp.deepcopy(self.noeud_selectionne.plateau_ap_coup)
                #tps_d1 = time()-tps_d1                
                
                joueur = self.racine.plateau.dict_ID2J[
                            self.racine.plateau.dict_ID2J[_noeud_source.joueur_createur].joueur_suivant]
                
                for i in range(_nb_rot_card):
                    joueur.oriente_carte_libre(_plateau.carte_en_dehors, "horaire")
                
                tps_d2 = time()
                joueur.modifier_plateau(_plateau, _fleche)
                tps_d2 = time()-tps_d2
                print(378, 'tps1=', tps_d1/(tps_d1+tps_d2), 'tps2=', tps_d2/(tps_d1+tps_d2) )
                
                joueur.generate_list_paths(_plateau)
                if (joueur.liste_paths != []):
                    for _path in joueur.liste_paths:
                        joueur.effectuer_chemin(_plateau, _path)
                        _enfant = UCT_node()
                        _noeud_source.enfants += [_enfant]
                        _enfant.parent = _noeud_source
                        _enfant.description_coup = [_nb_rot_card, _fleche, _path]
                        _enfant.joueur_createur = joueur.identifiant
                        c+=1
# =============================================================================
#                 
#                 else:
#                     joueur.effectuer_chemin(_plateau, [])
#                     _enfant = UCT_node()
#                     _noeud_source.enfants += [_enfant]
#                     _enfant.parent = _noeud_source
#                     _enfant.plateau_ap_coup = _plateau
#                     _enfant.description_coup = [_nb_rot_card, _fleche, []]
#                     _enfant.joueur_createur = joueur.identifiant
# =============================================================================
                c+= 1
        print(c, "enfants ont été générés")
                    
    
    def rollout(self, _noeud_source, _nb_parties = 1, _nb_coup_max = 100):
        """
        joue plusieurs parties au hasard en partant de la situation du plateau
        telle que décrite dans le noeud étendu
        
        _noeud_source(UCT_node):
            noeud pour lequel on effectue le roll out
        """
        
        compteur_victoires = {}
        for _j in _noeud_source.plateau_ap_coup.Liste_Joueur:
            compteur_victoires[_j.identifiant] = 0
            
        for k in range(_nb_parties):
            _plateau = self.noeud_selectionne.plateau_ap_coup.__deepcopy__({})
            j_playing = _plateau.dict_ID2J[_noeud_source.joueur_createur]
            c = 0
            while (not _plateau.check_gagnant() and c < _nb_coup_max):
                j_playing = _plateau.dict_ID2J[j_playing.joueur_suivant]
                j_playing.coup_alea(_plateau)
                c+=1
            compteur_victoires[_plateau.Liste_Classement[0][1].identifiant] += 1#on incrémente le compteur de victoire
        
        return compteur_victoires
        
    def retro_propagation(self, _feuille, _compteur_victoires):
        """
        met à jour les noeuds traversés lors de la selection (tous les parents
        de la feuille)
        
        _feuille(UCT_node):
            noeud à partir duquel on remonte à la racine
            
        _compteur_victoires(dico, key = joueur, value = nombre de vitoire):
            le compteur de victoire à propager sur le reste des noeuds.
            Ce dictionnaire est généré par le rollout
        """
        noeud = _feuille
        while noeud.parent != None:
            noeud.nb_visit += 1
            noeud.nb_gagne += _compteur_victoires[noeud.joueur_createur]
            noeud = noeud.parent
            
        noeud.nb_visit += 1
        noeud.nb_gagne += _compteur_victoires[noeud.joueur_createur]
            
    
    
    
    
    
    
    
    