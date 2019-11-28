# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 05:18:23 2019

@author: anael
"""



#[Nord,Sud,Est,Ouest] 
connectivité={'coin':['0110','1010','1001','0101'],
              'couloir':['1100','0011'],
              'carrefour':['1110','1011','1101','0111']}

class carte():
    def __init__(self,type_carte,dict_elements,\
                 position_graph,position_detail,
                 orientation):
        """type_carte : str
        dict_elements : dict {fantome,pepite,joueur)
        position_graph : ref noeud networkX
        position_detail : (int,int)
        orientation : int
        nom : str ('0010')"""
        self.type=type_carte
        self.elements=dict_elements
        self.position_G=position_graph
        self.position_D=position_detail
        self.nom=orientation
        self.connectivité=connectivité[type_carte]
    
    def pivoter(self,sens):
        if sens=='horaire' :
            if self.orientation < len(self.connectivité):
                self.orientation=self.connectivité[self.orientation+1]
            else :
                self.orientation=self.connectivité[0] #retour au premier
        
        else: #anti-horaire
            if self.orientation > 0:
                self.orientation=self.connectivité[self.orientation-1]
            else :
                self.orientation=self.connectivité[-1] #retour au dernier

