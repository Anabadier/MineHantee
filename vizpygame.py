# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 18:06:56 2019

@author: anael
"""
import pygame
from pygame.locals import *
import random
import os

# =============================================================================
# Initialisation
# =============================================================================
#Paramètres de la fenêtre
nombre_case_cote = 7
taille_case = 50
cote_fenetre = nombre_case_cote * taille_case

dic_case_img={'0110':'NXXO.png','1010':'XSXO.png','1001':'XSEX.png','0101':'NXEX.png',\
              '1100':'XXEO.png','0011':'NSXX.png',\
              '1110':'XXXO.png','1011':'XSXX.png','1101':'XXEX.png','0111':'NXXX.png'}

#On génère une matrice aléatoire
Mat_plat=[[[] for i in range(nombre_case_cote)] for i in range(nombre_case_cote)]
for i in range(len(Mat_plat)):
    for j in range(len(Mat_plat[i])):
        Mat_plat[i][j]=random.choice(list(dic_case_img.keys()))
Mat_plat
# =============================================================================
# Générer plateau
# =============================================================================

pygame.init() #initialisation des modules

def genere_carte(carte):
    """génerer les images de cartes"""
    image=pygame.image.load(os.path.abspath(dic_case_img[carte])).convert_alpha()
    carte=pygame.transform.scale(image, (49,49)) #forcer la taille de la case
    return(carte)

def afficher(Mat_plat):
    """afficher les cartes sur le plateau"""
    num_ligne=0
    for ligne in Mat_plat:
        num_case=0
        for case in ligne:
            x=num_case*taille_case
            y=num_ligne*taille_case
            num_case+=1
            carte=genere_carte(case)
            print(carte)
            print(x,y)
            fenetre.blit(carte,(x,y))
            ##Rafraîchissement de l'écran
            pygame.display.flip()
        num_ligne+=1
	
		
#Création de la fenêtre
fenetre = pygame.display.set_mode((cote_fenetre,cote_fenetre))

fond = pygame.image.load("fond_laby.jpg").convert()
fenetre.blit(fond, (0,0))

afficher(Mat_plat)


#BOUCLE INFINIE
continuer = 1
pygame.key.set_repeat(400, 30) #maintenir déplacement quand touche enfoncée
while continuer:
	for event in pygame.event.get():	#Attente des événements
		if event.type == QUIT:
			continuer = 0

	#Rafraichissement
	pygame.display.flip()

pygame.quit()

