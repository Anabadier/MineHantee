# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 11:10:06 2019

@author: lili-japi
"""

import math as math
import random as rd

#===================================================================
#________________________Classe plateau_____________________________
#===================================================================


class Plateau(object) :
    """
    Attributs :
        taille (int)
        labyrinthe_detail (matrice d’objet cartes) :
            matrice carrée de taille “self.taille”.
            Elle contient les objets cartes afin de
            donner la situation actuelle du plateau
        labyrinthe_graphe (graphe de networkx) :
            donne la connectivité du réseau fourni par le labyrinthe.
            Pratique pour le calcul de chemin.
    
    Méthode :
        __init__(_chemin_fichier_config) : Lit le fichier de configuration,
            affiche les informations (sous texte puis dans interface graphique;
            la modification et l’enregistrement d’un nouveau fichier de
            configuration doit être possible), initialisation du plateau avec
            génération de la position des cartes, de la position des fantômes,
            de la position des pépites ; création des attributs
            “labyrinthe_detail” et “labyrinthe_graphe”
        placer_cartes : initialise la position des cartes
        placer_fantomes : initialise la position des fantômes
        placer_pepites : initialise la position des pépites
        placer_joueur : initialise la position des joueurs
        coulisser : Effectue tous les changements associés à l’introduction
            d’une carte dans le plateau au début du tour d’un joueur.
            Notamment, appelle les méthodes “coulisser_detail”
            et “coulisser_graphe”.
        coulisser_detail : change les positions des objets cartes dans la
            matrice “self.labyrinthe_detail”
        coulisser_graphe : change la connectivité de “self.labyrinthe_graphe”
            lorsque qu’une nouvelle carte est insérée dans le plateau.
            La nouvelle carte doit être connectée au réseau; la carte sortante
            ne doit plus être connectée; les cartes intermédiaire doivent
            modifier leur connection.
        check_deplacement : vérifie que le déplacement demandé par un joueur
            est valide. Si possible, effectue la mise à jour de la position du
            joueur sinon, renvoie un message d’erreur visible par le joueur
    """
    
    # T=np.array([[{"position":(idx_ligne,idx_colonne), "mobile": True, "type": None , "element":{'fantome' : None, 'pepite' : bool , 'joueur' :None}, 'orientation' : None ,'connectivite' : []} for idx_colonne in range (taille)] for idx_ligne in range (taille)])
    
    def __init__(self, matrice_cartes, graphe_networkx):
        """
        Initialise les valeurs du plateau.
        :param matrice_cartes: array - matrice carré de taille "self.taille" qui contient les objets cartes
        :param graphe_networkx: ddonne la connectivité du réseau fourni par le labyrinthe
        :return:
        """
        self.taille = int()
        self.labyrinthe_graphe = graphe_networkx #donne la connectivité du réseau fourni par le labyrinthe. Pratique pour le calcul de chemin
        try:
            if self.taille >= 7 :
                self.labyrinthe_detail = matrice_cartes #matrice carrée de taille “self.taille”. Elle contient les objets cartes afin de donner la situation actuelle du plateau
        except:
            print(f"Le plateau doit être de taille au moins 7")
            raise
        
    def placer_cartes_fixes (self):
        """
        Initialise la position des cartes fixes     
        :param:
        :return:
        """    
        middle= math.floor(self.taille/2) + 1
        if middle%2 == 0 :
            i = 0
            while i < self.taille :
                for j in range(self.taille):
                    self.matrice_cartes[i,j]['fixe']=True
                    
                    
    def placer_cartes_non_fixes (self):
        """
        Initialise la position des cartes non fixes (aléatoirement)
        :param:
        :return:
        """    
        cartes_dispo = {'coin' : 16, 'tunnel' : 15, 'T' : 5} # à adapter
        type_carte = ['coin', 'tunnel', 'T']
        for i in range (self.taille) :
            for j in range (self.taille) :
                if self.matrice_cartes[i,j]['fixe'] is False :
                    actualisation = 0
                    while actualisation == 0 :
                        x = rd.randint(0,len(type_carte)-1)
                        if cartes_dispo[type_carte[x]]>0:
                            actualisation = -1
                        else :
                            type_carte.remove(type_carte[x])
                    cartes_dispo[type_carte[x]]+=actualisation
                    self.matrice_cartes[i,j]['type'] = type_carte[x]
                    
    def placer_fantomes_et_pepites (self): 
        """
        Initialise la position des fantômes
        :param:
        :return:
        """
        for i in range (self.taille) :
            for j in range (self.taille) :
                if self.matrice_cartes[i,j]['fixe'] is False :
                    self.matrice_cartes[i,j]['fantome'] = True
                    self.matrice_cartes[i,j]['pepite'] = True

    
    def placer_joueur (self, joueurs):
        """
        Initialise la position des joueurs (dans le carré le plus intérieur ayant 4 coins)
        :param joueurs: nombre de joueurs selectionné
        :return:
        """
        
        middle= math.floor(self.taille/2) + 1
        nb_joueurs = [i for i in range(joueurs)]
        
        if middle%2 == 0 :
            a = middle-2
            b = middle+2
        else :
            a = middle-3
            b = middle+3
            
        possibles = [(a,a),(a,b),(b,a),(b,b)]
        while len(nb_joueurs) > 0 :
            joueur_num = rd.randint(0,len(nb_joueurs)-1)
            place_coord = rd.randint(0,len(possibles)-1)
            self.matrice_cartes[possibles[place_coord]]['joueur'] = True
            self.matrice_cartes[possibles[place_coord]]['num_joueur'] = nb_joueurs[joueur_num]
            nb_joueurs.remove(nb_joueurs[joueur_num])
            possibles.remove(possibles[place_coord])
        
    
    def coulisser_detail (self,coord_x, coord_y,nouvelle_carte):
        """
        Change les positions des objets cartes dans la matrice “self.labyrinthe_detail”
        :param coord_x: abscisse du lieu où l'on souhaite faire coulisser la carte
        :param coord_y: ordonnée du lieu où l'on souhaite faire coulisser la carte
        :return:
        """
        ## on modifie la ligne
        # en coulissant de gauche à droite
        if coord_x == -1 :
            carte_sortante = self.labyrinthe_detail[self.taille-1,coord_y]
            for i in range(self.taille-1, 0, -1) :
                self.labyrinthe_detail[i,coord_y] = self.labyrinthe_detail[i-1,coord_y]
            self.labyrinthe_detail[0,coord_y] = nouvelle_carte
        # en coulissant de droite à gauche    
        if coord_x == self.taille :
            carte_sortante = self.labyrinthe_detail[0,coord_y]
            for i in range(self.taille) :
                self.labyrinthe_detail[i,coord_y] = self.labyrinthe_detail[i+1,coord_y]
            self.labyrinthe_detail[self.taille-1,coord_y] = nouvelle_carte
                
        ## on modifie la colonne
        # en coulissant de haut en bas
        if coord_y == -1 :
            carte_sortante = self.labyrinthe_detail[coord_x, self.taille-1]
            for i in range(self.taille-1, 0, -1) :
                self.labyrinthe_detail[coord_x,i] = self.labyrinthe_detail[coord_x, i-1]
            self.labyrinthe_detail[coord_x, 0] = nouvelle_carte
        # en coulissant du bas vers le haut
        if coord_y == self.taille :
            carte_sortante = self.labyrinthe_detail[coord_x,0]
            for i in range(self.taille) :
                self.labyrinthe_detail[coord_x, i] = self.labyrinthe_detail[coord_x,i+1]
            self.labyrinthe_detail[coord_x,self.taille-1] = nouvelle_carte
        
        #la nouvelle carte à coulisser sera la carte qui est sortie
        nouvelle_carte = carte_sortante 
    
    def coulisser_graphe (self) :
        """
        Change la connectivité de “self.labyrinthe_graphe”
        lorsque qu’une nouvelle carte est insérée dans le plateau.
        La nouvelle carte doit être connectée au réseau; la carte sortante
        ne doit plus être connectée; les cartes intermédiaire doivent
        modifier leur connection.
        """
        pass
    
    def coulisser (self):
        """
        Effectue tous les changements associés à l’introduction
        d’une carte dans le plateau au début du tour d’un joueur.
        Notamment, appelle les méthodes “coulisser_detail”
        et “coulisser_graphe”.
        """
        pass
    
    def check_deplacement (self):
        """
        Vérifie que le déplacement demandé par un joueur
        est valide. Si possible, effectue la mise à jour de la position du
        joueur sinon, renvoie un message d’erreur visible par le joueur.
        """
        pass