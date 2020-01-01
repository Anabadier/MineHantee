# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 18:06:56 2019

@author: anael
"""
import pygame
from pygame.locals import *
import random
import os
import sys

from classe_carte import carte
import Jeu_mine
# =============================================================================
# Initialisation
# =============================================================================
#Paramètres de la fenêtre

#nombre_case_cote = 7
#taille_case = 350/nombre_case_cote
#cote_fenetre = nombre_case_cote * taille_case

dic_case_img={'0110':'NXXO_2.png','1010':'XSXO_2.png','1001':'XSEX_2.png','0101':'NXEX_2.png',\
              '1100':'XXEO_2.png','0011':'NSXX_2.png',\
              '1110':'XXXO_2.png','1011':'XSXX_2.png','1101':'XXEX_2.png','0111':'NXXX_2.png'}

##On génère une matrice aléatoire
#def genere_mat():
#    Mat_plat=[[[] for i in range(nombre_case_cote)] for i in range(nombre_case_cote)]
#    for i in range(len(Mat_plat)):
#        for j in range(len(Mat_plat[i])):
#            Mat_plat[i][j]=random.choice(list(dic_case_img.keys()))
#    print(Mat_plat)
#    return(Mat_plat)
    

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREY = 192, 192, 192
CIEL = 0, 200, 255
RED = 255, 0, 0
ORANGE = 255, 100, 0
GREEN = 0, 255, 0


# =============================================================================
# Générer plateau
# =============================================================================

pygame.init() #initialisation des modules

def genere_carte(carte,size):
    """génerer les images de cartes"""
    image=pygame.image.load(os.path.abspath(os.path.join('img_cartes',dic_case_img[carte]))).convert_alpha()
    carte=pygame.transform.scale(image, size) #forcer la taille de la case
    return(carte)

def afficher(plat,plateau,fenetre,id_joueur=None):
    """afficher les cartes sur le plateau"""
    global pepite, fantome
    
    Mat_plat=plat.labyrinthe_detail
    
    dic_boutons_fleches={} #dictionnaire de tous les boutons flèches
    img_fleche_haut=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"fleche_haut.png"))).convert_alpha()
    img_fleche_bas=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"fleche_bas.png"))).convert_alpha()
    img_fleche_gauche=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"fleche_gauche.png"))).convert_alpha()
    img_fleche_droite=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"fleche_droite.png"))).convert_alpha()
    
    img_pepite=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"triskel.png"))).convert_alpha()
    pepite=pygame.transform.scale(img_pepite,(int((taille_case-1)/2),int((taille_case-1)/2)))
    
    img_fantome=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"fantome.png"))).convert_alpha()
    fantome=pygame.transform.scale(img_fantome,(int((taille_case-1)/2),int((taille_case-1)/2)))
    
    img_perso=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"pinguin.png"))).convert_alpha()
    perso=pygame.transform.scale(img_perso,(int((taille_case-1)/1.5),int((taille_case-1)/1.5)))

    
    num_ligne=0
    for ligne in Mat_plat:
        num_case=0
        for case in ligne:
            x=num_case*taille_case
            y=num_ligne*taille_case
            #cartes immobiles 
#            if num_case%2==0 and num_ligne%2==0:
#                plateau.fill(RED, (x,y,int(taille_case),int(taille_case)))
            num_case+=1
            print(case.nom)
            carte=genere_carte(case.nom,(int(taille_case),int(taille_case)))
            plateau.blit(carte,(x,y))
            
            #case transparente si accessible
            if case.nom=='1001':
                cache= pygame.Surface((int(taille_case),int(taille_case))) #case à surligner
                cache.set_alpha(70)  #transparence
                cache.fill((255,255,0))   #jaune
                plateau.blit(cache,(x,y))
                
            #Si pépite/fantome sur la carte, voir condition avec la matrice des instances de cartes
            if case.elements['pepite'] == True:
                plateau.blit(pepite,(x,y))
            if case.elements['fantome'] == True:
                plateau.blit(fantome,(x+taille_case/5,y+taille_case/5))
            if case.elements['joueur']==True:
                plateau.blit(perso,(x+taille_case/6,y+taille_case/6))
            
            #Si paire : peut coulisser : insérer bouton de chaque côté
            if num_case%2==0:
                fleche_gauche=Button_img(fenetre, img_fleche_gauche, (90-int(taille_case-5), 100+x),(int(taille_case-5),int(taille_case-5)))
                dic_boutons_fleches["G"+str(num_case-1)]=fleche_gauche
                fleche_droite=Button_img(fenetre, img_fleche_droite, (500-int(taille_case), 100+x),(int(taille_case-5),int(taille_case-5)))
                dic_boutons_fleches["D"+str(num_case-1)]=fleche_droite
            if num_ligne%2!=0:
                fleche_haut=Button_img(fenetre, img_fleche_haut, (y+100, 90-int(taille_case-5)),(int(taille_case-5),int(taille_case-5)))
                dic_boutons_fleches["H"+str(num_ligne)]=fleche_haut
                fleche_bas=Button_img(fenetre, img_fleche_bas, (y+100, 500-int(taille_case)),(int(taille_case-5),int(taille_case-5)))
                dic_boutons_fleches["B"+str(num_ligne)]=fleche_bas
            
        num_ligne+=1
        
        
    #extraire carte_ej de la méthode coulisser
    carte_ej=plat.carte_en_dehors
    carte_eject=genere_carte(carte_ej.nom,(50,50)) #aléatoire pour le moment
    fenetre.fill((250,250,250) , (625,80,50,50)) #remplit en blanc la position de l'ancienne carte
    fenetre.blit(carte_eject,(625,80))

    
    ##Rafraîchissement de l'écran
    pygame.display.flip()
    return(dic_boutons_fleches)
	
class Button:
    '''Ajout d'un bouton avec un texte sur img
    Astuce: ajouter des espaces dans les textes pour avoir une même largeur
    de boutons
    dx, dy décalage du bouton par rapport au centre
    action si click
    Texte noir
    Source : https://wiki.labomedia.org/index.php/Pygame:_des_exemples_pour_d%C3%A9buter.html#Des_rectangles_comme_boutons
    '''

    def __init__(self, fond, text, color, font, dx, dy):
        self.fond = fond
        self.text = text
        self.color = color
        self.font = font
        self.dec = dx, dy
        self.state = False  # enable or not
        self.title = self.font.render(self.text, True, BLACK)
        textpos = self.title.get_rect()
        textpos.centerx = self.fond.get_rect().centerx + self.dec[0]
        textpos.centery = self.dec[1]
        self.textpos = [textpos[0], textpos[1], textpos[2], textpos[3]]
        self.rect = pygame.draw.rect(self.fond, self.color, self.textpos,3)
        self.fond.blit(self.title, self.textpos)

    def update_button(self, fond, action=None,arg=None):
        self.fond = fond
        mouse_xy = pygame.mouse.get_pos()
        over = self.rect.collidepoint(mouse_xy)
        if over:
            if arg:
                action(arg)
            else:
                action()


    def display_button(self, fond):
        self.fond = fond
        self.rect = pygame.draw.rect(self.fond, self.color, self.textpos)
        self.fond.blit(self.title, self.textpos)

class Button_img:
    '''Ajout d'un bouton/image '''

    def __init__(self, fond, img, pos, size):
        self.fond = fond
        self.img=pygame.transform.scale(img, size) #on redimensionne l'image
        self.rect = self.img.get_rect() #définition de hauteur/largeur
        self.rect.topleft=pos #définition de la position
        self.rect=self.rect #on récupère les coordonnées du rectangle
        self.fond.blit(self.img, pos)

    def update_button(self, fond, action=None,arg=None):
        self.fond = fond
        mouse_xy = pygame.mouse.get_pos()
        over = self.rect.collidepoint(mouse_xy)
        if over:
            if arg:
                action(arg)
            else:
                action()

    def display_button(self, fond):
        self.fond = fond
        self.rect = pygame.draw.rect(self.fond, self.color, self.textpos)
        self.fond.blit(self.img, self.textpos)
		
#Création de la fenêtre
def ecran(plat):
    global fenetre,plateau,cote_fenetre,nombre_case,taille_case
    
    nombre_case_cote=plat.taille
    taille_case = 350/nombre_case_cote
    cote_fenetre = nombre_case_cote * taille_case
    
    fenetre = pygame.display.set_mode((800,600))
    fenetre.fill((255,255,255)) #remplissage fond blanc
    
    plateau=pygame.Surface((cote_fenetre,cote_fenetre))
    #si on veut importer une image de fond
    #fond = pygame.image.load(os.path.join('img_cartes',"fondbeige.png")).convert()     
    #plateau.blit(fond, (0,0))
    #pour Colorer le fond :
    plateau.fill((250,250,250))
    dic_boutons_fleches=afficher(plat,plateau,fenetre)
    fenetre.blit(plateau,(100,100))
    
    #Boutons menus
    bouton_pause=Button(fenetre, " Pause ", GREY, pygame.font.SysFont('freesans', 18), -300, 550) #création boutton
    bouton_pause.display_button(fenetre) #affichage
    
    bouton_save=Button(fenetre, " Sauvegarder ",GREY,pygame.font.SysFont('freesans', 18), -200, 550)
    bouton_save.display_button(fenetre)
    
    bouton_quit=Button(fenetre, " Quitter ",GREY,pygame.font.SysFont('freesans', 18), -100, 550)
    bouton_quit.display_button(fenetre)
    
    #Carte éjectée
    pivotgauche=pygame.image.load(os.path.abspath(os.path.join('img_cartes','pivotgauche.png'))).convert_alpha()
    bouton_pivot_gauche=Button_img(fenetre,pivotgauche,(550,80),(50,50))
    pivotdroit=pygame.image.load(os.path.abspath(os.path.join('img_cartes','pivotdroit.png'))).convert_alpha()
    bouton_pivot_droit=Button_img(fenetre,pivotdroit,(700,80),(50,50))
    carte_ej=plat.carte_en_dehors
    carte_eject=genere_carte(carte_ej.nom,(50,50))
    fenetre.fill((250,250,250) , (625,80,50,50)) #remplit en blanc la position de l'ancienne carte
    fenetre.blit(carte_eject,(625,80))
    
    #Affichage du score
    valscore=0
    score(valscore)
    
    #BOUCLE INFINIE
    continuer = 1
    pygame.key.set_repeat(400, 30) #maintenir déplacement quand touche enfoncée
    while continuer:       
    	for event in pygame.event.get():	#Attente des événements
            if event.type == pygame.MOUSEBUTTONDOWN:
                bouton_pause.update_button(fenetre, action=pause)
                bouton_save.update_button(fenetre, action=save)
                bouton_quit.update_button(fenetre, action=gamequit)
                for i in dic_boutons_fleches:
                    dic_boutons_fleches[i].update_button(fenetre,action=deplacement,arg=[i,plat])
                bouton_pivot_gauche.update_button(fenetre,action=chgmt_orientation,arg={'carte':plat.carte_en_dehors,'sens':'gauche'})
                bouton_pivot_droit.update_button(fenetre,action=chgmt_orientation,arg={'carte':plat.carte_en_dehors,'sens':'droit'})
            elif event.type == QUIT:
                continuer=0
                pygame.quit()
    	#Rafraichissement
    	pygame.display.flip()
    
def pause():
    print("pause")

def save():
    print("save")

def gamequit():
    print("Quit")
    pygame.quit()
    sys.exit()
    
def deplacement(i):
    """Actualise la matrice des cartes
    i : list[fleche,plateau]"""
    global carte_ej
    fleche=i[0]
    plat=i[1]
    print("la flèche "+str(fleche)+" a été cliquée")
    convertFlecheCoord={'G':[int(fleche[1:]),-1],'D':[int(fleche[1:]),plat.taille],
                        'H':[-1,int(fleche[1:])],'B':[plat.taille,int(fleche[1:])]}
    coord_x=convertFlecheCoord[fleche[0]][0]
    coord_y=convertFlecheCoord[fleche[0]][1]
    #print(coord_x,coord_y)
    #régénérer plat
    plat.coulisser(coord_x,coord_y)
    plateau=pygame.Surface((cote_fenetre,cote_fenetre))
#    fond = pygame.image.load(os.path.join('img_cartes',"fondbeige.png")).convert()
#    plateau.blit(fond, (0,0))
    plateau.fill((250,250,250)) #fond blanc
    afficher(plat,plateau,fenetre)
    fenetre.blit(plateau,(100,100))
    
    
def chgmt_orientation(arg):
    print('bouton '+str(arg['sens'])+' cliqué')
    print(arg['carte'].elements)
    arg['carte'].pivoter(arg['sens'])
    print(arg['carte'].elements)
    fenetre.fill((250,250,250) , (625,80,50,50)) #remplit en blanc la position de l'ancienne carte
    carte_ej=genere_carte(arg['carte'].nom,(50,50)) 
    fenetre.blit(carte_ej,(625,80))
    if arg['carte'].elements['pepite'] == True:
        fenetre.blit(pepite,(625,80))
    if arg['carte'].elements['fantome'] == True:
        fenetre.blit(fantome,(625+taille_case/5,80+taille_case/5))
    pygame.display.flip()
    
def score(valscore):
    police = pygame.font.Font(None,36)
    texte = police.render("Score "+str(valscore),True,pygame.Color("#000000"))
    rectTexte = texte.get_rect() #surface rectangle autour du texte
    rectTexte.topleft=(600,300)
    fenetre.fill(WHITE,rectTexte)  #efface précédent score
    print(rectTexte)
    fenetre.blit(texte,rectTexte)
    
if __name__=="__main__":
    ecran(Jeu_mine.JEU())

