# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:30:15 2019

@author:  Abel, Anaëlle, Augustin, Eliott, Liliana
"""

import random as rd
import networkx as nx
import math
import numpy as np
from time import time

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
            self.ordre_de_mission = {}
            self.ref_plateau = "null"
            self.position_graphe = "Non placé"
            self.position_detail = ("xcarte" , "ycarte")
            self.pepite=0
            self.deplacement_effectué=False
            self.carte_visit=[]
            self.joker_used=False
            self.liste_paths = [] #liste des chemins accessibles au joueur. Utile après rot card et coullissage
    
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
        ordre_mission = {}
        for i in range(nb_ordre):
            fantome = rd.randint(1,nb_ghost)
            while fantome in ordre_mission:
                fantome = rd.randint(1,nb_ghost)
            ordre_mission[fantome]=True
        self.ordre_de_mission = ordre_mission
    
    def generate_list_paths(self, _plateau):
        self.liste_paths = list(nx.single_source_shortest_path(_plateau.graph,
                                                    self.position_graphe).values())
    
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
        if (_card.elements["pepite"]):
            
            self.maj_points(self.ref_plateau.pts_pepite)
            _card.element_virtuels['coup_capture_pepite'] = self.ref_plateau.compteur_coup
            _card.element_virtuels['joueur_capture_pepite'] = self.identifiant
            if _reset_value:
                self.pepite = self.pepite +  1
                _card.elements["pepite"] = False
            
        if (_card.elements["fantome"] != []):
            if (_card.elements["fantome"] == self.ref_plateau.ordre_fantome):
                if (_card.elements["fantome"] in list(self.ordre_de_mission.keys())):
                    self.maj_points(self.ref_plateau.pts_ordre_mission)
                    _card.element_virtuels['coup_capture_fantome'] = self.ref_plateau.compteur_coup
                    _card.element_virtuels['joueur_capture_fantome'] = self.identifiant
                    if _reset_value:
                        self.ordre_de_mission[_card.elements["fantome"]]=False#maj ordre de mission
                else:
                    self.maj_points(self.ref_plateau.pts_fantome)
                    _card.element_virtuels['coup_capture_fantome'] = self.ref_plateau.compteur_coup
                    _card.element_virtuels['joueur_capture_fantome'] = self.identifiant
                if _reset_value:
                    _card.elements["fantome"] = []
                    self.ref_plateau.ordre_fantome += 1
                
    
    def retrancher_pts_carte(self, _card, _reset_value = True):
        """
        retranche les points qui était contenus dans _card en se basant sur les
        souvenir de _card.element_virtuels
        """
        if (_card.element_virtuels['coup_capture_pepite'] == self.ref_plateau.compteur_coup):
            if (_card.element_virtuels["pepite"]):
                self.maj_points(self.ref_plateau.pts_pepite, -1)
                if _reset_value:
                    _card.elements["pepite"] = True
                    self.pepite = self.pepite -  1
        
        if (_card.element_virtuels['coup_capture_fantome'] == self.ref_plateau.compteur_coup):      
            if (_card.element_virtuels["fantome"] != []):
                if (_card.element_virtuels["fantome"] == self.ref_plateau.ordre_fantome-1):
                    if (_card.element_virtuels["fantome"] in list(self.ordre_de_mission.keys())):
                        self.maj_points(self.ref_plateau.pts_ordre_mission, -1)
                        
                        if _reset_value:
                            self.ordre_de_mission[_card.element_virtuels["fantome"]]=True
                    else:
                        self.maj_points(self.ref_plateau.pts_fantome, -1)
                        
                    if _reset_value:
                        _card.elements["fantome"] = _card.element_virtuels["fantome"]
                    self.ref_plateau.ordre_fantome -= 1
    
    def maj_position(self, _carte):
         self.position_graphe = _carte.position_G
         self.position_detail = _carte.position_D
         self.carte_visit.append(self.position_detail)
   
    def oriente_carte_libre(self, carte_libre, sens):
        carte_libre.pivoter(sens)
    
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
        if (card_path != []):
            card_path[0].elements["joueur"].remove(self.identifiant)
            card_path[-1].elements["joueur"].append(self.identifiant)
        for _card in card_path:
            self.maj_position(_card)
            
            if (_backward):
                self.retrancher_pts_carte(_card)
            else:
                self.compter_pts_carte(_card)
        _plateau.maj_classement()#on met a jour le classement à la fin du tour d'un joueur
    
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
            self.ref_plateau.compteur_coup -= 1
            self.effectuer_chemin(_plateau, _description_coup[2], _backward)
            self.modifier_plateau(_plateau, _description_coup[1], _backward)
            self.rotation_carte(_plateau, _description_coup[0], _backward)
            
        else:
            self.rotation_carte(_plateau, _description_coup[0])
            self.modifier_plateau(_plateau, _description_coup[1])
            self.effectuer_chemin(_plateau, _description_coup[2])
            self.ref_plateau.compteur_coup += 1
    
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
        
        self.ref_plateau.compteur_coup += 1
        
        return [nb_rotation, fleche, path]
    
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
        ordre_fantomes = self.ref_plateau.ordre_fantome
        card_path = plateau.translate_GraphPath2CardsPath(chemin)
        for carte in card_path :
            if carte.elements['pepite'] == True :
                gain+= plateau.pts_pepite
            if carte.elements['fantome'] != [] :
                if (carte.elements['fantome'] == ordre_fantomes):
                    if carte.elements['fantome'] in self.ordre_de_mission : 
                        gain+= plateau.pts_ordre_mission
                    else:
                        gain+= plateau.pts_fantome
                    ordre_fantomes += 1
        return(gain)
    
    def greedy(self, plateau):
        best_coup = [-1,0,"",[]]
        for i in range (1,5):
            self.rotation_carte(plateau,i)
            for j in plateau.liste_row_col:
                fleche = j
                self.modifier_plateau(plateau,fleche)
                self.generate_list_paths(plateau)
                for t in self.liste_paths:
                    gain = self.heuristique(t,plateau)
                    if gain > best_coup[0]:
                        best_coup = [gain,i,j,t]
                self.modifier_plateau(plateau, fleche, True)
            self.rotation_carte(plateau, i, True)
        self.coup_cible(plateau, best_coup[1:])
        return best_coup[1:]

##################################################################################
#Classe Joueur IA
##################################################################################

class Joueur_IA(Joueur):
    
    def __init__(self, _identifiant = "none", _niv ="Normale"):
        Joueur.__init__(self, _identifiant = _identifiant)
        self.niv = _niv
        self.UCT_solver = None
    
    def jouer(self):
        """
        faire jouer une IA en fonction de son niveau
        """
        if (self.niv == "Facile"):
            coup_alea = self.coup_alea(self.ref_plateau)
            self.coup_cible(self.ref_plateau, coup_alea, True)
                
        elif (self.niv == "Normale"):
            description_coup = self.UCT_solver.jouer_UCT(self.ref_plateau, self)
            self.coup_cible(self.ref_plateau, description_coup)
            
        elif (self.niv == "Difficile"):
            self.greedy(self.ref_plateau)
    
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
            self.ref_plateau.compteur_coup -= 1
            self.effectuer_chemin(_plateau, _description_coup[2], _backward)
            self.modifier_plateau(_plateau, _description_coup[1], _backward)
            self.rotation_carte(_plateau, _description_coup[0], _backward)
            
        else:
            self.rotation_carte(_plateau, _description_coup[0])
            self.modifier_plateau(_plateau, _description_coup[1])
            self.effectuer_chemin(_plateau, _description_coup[2])
            self.ref_plateau.compteur_coup += 1
            
    def is_terminal_node(self,plateau) : ## actualiser pour dire que s'il ne reste pas suffisament de points pour dépasser le premier is over
        dict_vide = {'fantome' : False , 'pepite' : False, 'joueur': False}
        taille = plateau.taille
        compteur=0
        for i in plateau :
            if i.elements == dict_vide :
                compteur += 1
        return (compteur == taille^2)
            
    def mini_max(self,plateau, id_joueur, joueur_initial, depth, alpha, beta, maximizingPlayer):
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
                return (None, None, None, 0)
            else: # Depth is zero
                dico_chemins = plateau.chemin_possible(id_joueur)
                chemins_coord = [dico_chemins[coord] for coord in dico_chemins.keys()]
                points = [self.fonction_evaluation(plateau, i) for i in chemins_coord]
                le_chemin = chemins_coord[points.index(max(points))]
                return (None, None, le_chemin,max(points))
        
        if maximizingPlayer: #joker player #la personne qui utilise le joker
            value = -math.inf
            entree = rd.choice(plateau.entrees)
            for orientation in range(1,5):
                carte_test.orientation = orientation
                for une_entree in plateau.entrees:
                    p_copy = plateau.copy()
                    p_copy.coulisser_detail(une_entree[0], une_entree[1], carte_test)
                    id_next_joueur = self.joueur_suivant.identification
                    new_score = self.mini_max(self, p_copy, id_next_joueur,joueur_initial, depth-1, alpha, beta, False)[3]
                    if new_score > value:
                        value = new_score
                        entree = une_entree
                        ori = orientation
                        chem = self.mini_max(self, p_copy, id_next_joueur,joueur_initial, depth-1, alpha, beta, False)[2]
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return (entree, ori, le_chemin, value)
        
        else: # Minimizing player
            value = math.inf
            entree = rd.choice(plateau.entrees)
            for orientation in range(1,5):
                carte_test.orientation = orientation
                for une_entree in plateau.entrees:
                    p_copy = plateau.copy()
                    p_copy.coulisser_detail(une_entree[0], une_entree[1], carte_test)
                    id_next_joueur = self.joueur_suivant.identification
                    if id_next_joueur == joueur_initial :
                        mini = self.mini_max(self, p_copy, id_next_joueur, joueur_initial, depth-1, alpha, beta, True)
                        new_score = mini[3]
                    else :
                        mini = self.mini_max(self, p_copy, id_next_joueur, joueur_initial, depth-1, alpha, beta, False)
                        new_score = mini[3]
                    if new_score < value:
                        value = new_score
                        entree = une_entree
                        ori = orientation
                        chem = mini[2]
                        beta = min(beta, value)
                    if alpha >= beta:
                        break
            return (entree, ori, chem, value)

##################################################################################
#Classe Upper Confidence Bound
##################################################################################

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
    def __init__(self,  _nb_rollout = 1,
                 _temps_ressource = 10):
        self.nb_rollout = _nb_rollout
        self.temps_ressource = _temps_ressource
    
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
            
            if (_enfant.ucb_score > _max and _enfant.ucb_score != 10000):# and _enfant.ucb_score != 10000):#on refuse de choisir un noeud non evalué
                _max = _enfant.ucb_score
                self.meilleur_noeud = _enfant
        
        print("UCB score du meilleur noeud :", self.meilleur_noeud.ucb_score)        
        return self.meilleur_noeud.description_coup
        
    
    def recherche_UCT(self):
        """
        Réalise les 4 étapes de l'UCT et met à jour le meilleur_noeud
        """
        
        #1
        self.selection()
        
        #2 si nécessaire
        _extension = False
        if (self.noeud_selectionne.nb_visit != 0 or self.noeud_selectionne == self.racine):
            _extension = True
            self.extension(self.noeud_selectionne)
            self.noeud_selectionne = self.noeud_selectionne.enfants[0]
            
        #3
        compteur_victoires = self.rollout(self.noeud_selectionne, _extension,
                                          self.nb_rollout)
        
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
                
                if (_enfant.ucb_score > _max):
                    _max = _enfant.ucb_score
                    noeud_max = _enfant
            
            self.noeud_selectionne = noeud_max
            self.racine.plateau.dict_ID2J[self.noeud_selectionne.joueur_createur].coup_cible(
                                                            self.racine.plateau,
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
                    
    
    def rollout(self, _noeud_source, _extension_bool,
                _nb_parties = 1, _nb_coup_max = 100):
        """
        joue plusieurs parties au hasard en partant de la situation du plateau
        telle que décrite dans le noeud étendu
        
        _noeud_source(UCT_node):
            noeud pour lequel on effectue le roll out
        """
        
        #on joue le coup stocké dans _noeud_source
        _plateau = self.racine.plateau
        j_playing = _plateau.dict_ID2J[_noeud_source.joueur_createur]
        if (_extension_bool):
            j_playing.coup_cible(_plateau, _noeud_source.description_coup)
        
        #on initilise la comptabilisation des victoires
        compteur_victoires = {}
        for _j in _plateau.Liste_Joueur:
            compteur_victoires[_j.identifiant] = 0
        
        #ROLLOUT en tant que tel
        for k in range(_nb_parties):
            nb_coup_rollout = 0
            rollout_action_list = []
            #joue aleatoirement jusqu'a une victoire ou un nb_coup_rollout >= _nb_coup_max
            while (not _plateau.check_gagnant() and nb_coup_rollout < _nb_coup_max):
                j_playing = _plateau.dict_ID2J[j_playing.joueur_suivant]
                coup_alea = j_playing.coup_alea(_plateau)
                rollout_action_list += [[j_playing]+coup_alea]
                nb_coup_rollout+=1
                
            #comptabilise la victoire du vainqueur
            compteur_victoires[_plateau.Liste_Classement[0][1].identifiant] += 1#on incrémente le compteur de victoire
            
            #remet le plateau dans l'etat AVANT ROLLOUT
            for i in range(nb_coup_rollout-1, -1, -1):
                j_retro_playing = rollout_action_list[i][0]
                j_retro_playing.coup_cible(_plateau, rollout_action_list[i][1:], True)
                
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