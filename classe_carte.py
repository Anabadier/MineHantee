# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 05:18:23 2019

@author: anael
"""

class carte():
    def __init__(self,type_carte,dict_elements=None,\
                 position_graph=None,position_detail=None,orientation=0,mobilite=True):
        """type_carte : str
        dict_elements : dict {fantome,pepite,joueur)
        position_graph : ref noeud networkX
        position_detail : (int,int)
        orientation : int
        nom : str ('0010')
        mobilite : bool """
        #[Nord,Sud,Est,Ouest] 
        dict_connectivité={'coin':['0110','1010','1001','0101'],
              'couloir':['1100','0011'],
              'carrefour':['1110','1011','1101','0111']}
        self.type=type_carte
        self.elements=dict_elements
        self.position_G=position_graph
        self.position_D=position_detail
        self.connectivite=dict_connectivité[type_carte]
        self.orientation=orientation
        self.nom=self.connectivite[orientation] #nom, ref de l'image et orientation de la carte
        self.mobilite=mobilite
        
        
    
    def pivoter(self,sens):
        if sens=='droit' :
            if self.orientation < len(self.connectivite)-1:
                self.orientation=self.orientation+1
                self.nom=self.connectivite[self.orientation]
            else :
                self.orientation=0 #retour au premier
                self.nom=self.connectivite[self.orientation]
        
        else: #anti-horaire
            if self.orientation > 0:
                self.orientation=self.orientation-1
                self.nom=self.connectivite[self.orientation]
            else :
                self.orientation=len(self.connectivite)-1 #retour au dernier
                self.nom=self.connectivite[self.orientation]

