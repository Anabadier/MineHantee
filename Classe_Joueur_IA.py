# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 16:38:51 2020

@author: eliot
"""

from Calass_rep import Joueur

class Joueur_IA(Joueur):
    def __init__(self, _niv):
        self.niv = _niv
    
    def coup_alea(self):
        