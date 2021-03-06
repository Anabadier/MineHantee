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
import SaC2
# =============================================================================
# Initialisation
# =============================================================================
#Paramètres de la fenêtre



dic_case_img={'0110':'NXXO_3.png','1010':'XSXO_3.png','1001':'XSEX_3.png','0101':'NXEX_3.png',\
              '1100':'XXEO_3.png','0011':'NSXX_3.png',\
              '1110':'XXXO_3.png','1011':'XSXX_3.png','1101':'XXEX_3.png','0111':'NXXX_3.png'}

img_pinguin=['pinguin.png','pinguin_1.png','pinguin_2.png','pinguin_3.png']
    


BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREY = 192, 192, 192
CIEL = 0, 200, 255
RED = 255, 0, 0
ORANGE = 255, 100, 0
GREEN = 0, 255, 0
BLEU = 3,34,76
BLEUGRIS=178,198,213



# =============================================================================
# Générer plateau
# =============================================================================

pygame.init() #initialisation des modules

def genere_carte(carte,size):
    """génerer les images de cartes"""
    image=pygame.image.load(os.path.abspath(os.path.join('img_cartes',dic_case_img[carte]))).convert_alpha()
    carte=pygame.transform.scale(image, size) #forcer la taille de la case
    return(carte)
    
    
def afficher(plat,plateau,fenetre,joueur):
    """afficher les cartes sur le plateau"""
    global img_pepite,img_fantome

    print('actualisation plateau')
    
    Mat_plat=plat.labyrinthe_detail
    
    dic_boutons_fleches={} #dictionnaire de tous les boutons flèches
    img_fleche_haut=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"Fleche_sud.png"))).convert_alpha()
    img_fleche_bas=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"Fleche_nord.png"))).convert_alpha()
    img_fleche_gauche=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"Fleche_est.png"))).convert_alpha()
    img_fleche_droite=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"Fleche_ouest.png"))).convert_alpha()
    
    img_pepite=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"pépite.gif"))).convert_alpha()
    pepite=pygame.transform.scale(img_pepite,(int((taille_case-1)/2),int((taille_case-1)/2)))
    
    img_fantome=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"poisson2.gif")))
    fantome=pygame.transform.scale(img_fantome,(int((taille_case-1)/2),int((taille_case-1)/2)))
    
    chemins=plat.chemin_possible(joueur.identifiant).values()
    path=[]
    for coord in chemins:
        for elem in coord :
            path.append(elem)
    path=set(path)

    
    num_ligne=0
    for ligne in Mat_plat:
        num_case=0
        for case in ligne:
            coord=(num_ligne,num_case)
            x=num_case*taille_case
            y=num_ligne*taille_case
            
            #cartes immobiles 
#            if num_case%2==0 and num_ligne%2==0:
#                plateau.fill(RED, (x,y,int(taille_case),int(taille_case)))
            
            
            carte=genere_carte(case.nom,(int(taille_case),int(taille_case)))
            plateau.blit(carte,(x,y))
            
            #case surlignée si accessible
            
            if coord in path and (joueur in plat.Liste_Joueur_H and coord not in joueur.carte_visit):
                cache= pygame.Surface((int(taille_case),int(taille_case))) #case à surligner
                cache.set_alpha(70)  #transparence
                cache.fill((255,255,0))   #jaune
                plateau.blit(cache,(x,y))
            
            num_case+=1  
            #print(case.elements)
            #Si pépite/fan ààpm tome sur la carte, voir condition avec la matrice des instances de cartes
            if case.elements['pepite'] == True:
                plateau.blit(pepite,(x,y))
            if case.elements['fantome'] != []:
                plateau.blit(fantome,(x+taille_case/5,y+taille_case/5))
                ecrire(case.elements['fantome'],plateau,(x+taille_case/5,y+taille_case/5),WHITE,20)
            
            if case.elements['joueur']!=[]:
                for j in case.elements['joueur']:
                    img_perso=pygame.image.load(os.path.abspath(os.path.join('img_cartes',dict_pinguin_img[j]))).convert_alpha()
                    perso=pygame.transform.scale(img_perso,(int((taille_case-1)/1.5),int((taille_case-1)/1.5)))
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

    def __init__(self, fond, text, color, font, dx, dy,fontcol=BLACK):
        self.fond = fond
        self.text = text
        self.color = color
        self.font = font
        self.dec = dx, dy
        self.state = False  # enable or not
        self.title = self.font.render(self.text, True, fontcol )
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
        
        
def ecrire(texte,frame,pos,fontcolor=pygame.Color("#000000"),fontsize=36,fontname=None):
    """texte : str
    frame : surface
    pos : (tuple)"""
    police = pygame.font.SysFont(fontname,fontsize)
    texte = police.render(str(texte),True,fontcolor)
    rectTexte = texte.get_rect() #surface rectangle autour du texte
    rectTexte.topleft=pos #ancrage du texte
    
    frame.blit(texte,rectTexte)
    

		
#Création de la fenêtre
def ecran(plat):
    global fenetre,plateau,cote_fenetre,nombre_case,taille_case,current_player,dict_pinguin_img
    
    
    dict_pinguin_img={}
    c=0
    for j in plat.Liste_Joueur:
        dict_pinguin_img[j.identifiant]=img_pinguin[c]
        c+=1
    
    
    fenetre = pygame.display.set_mode((1000,600))
    fond = pygame.image.load(os.path.join('img_cartes',"Iceberg.jpg")).convert()    
    fenetre.fill((255,255,255)) #remplissage fond blanc
    fenetre.blit(fond,(0,0))
  
    nombre_case_cote=plat.taille
    taille_case = 350/nombre_case_cote
    cote_fenetre = nombre_case_cote * taille_case
    
    plateau=pygame.Surface((cote_fenetre,cote_fenetre))
    
    current_player=plat.Liste_Joueur[0]
    
    #si on veut importer une image de fond
    #fond = pygame.image.load(os.path.join('img_cartes',"Iceberg.jpg")).convert()     
    #plateau.blit(fond, (0,0))
    #pour Colorer le fond :
    plateau.fill((250,250,250))
    dic_boutons_fleches=afficher(plat,plateau,fenetre,joueur=current_player)
    fenetre.blit(plateau,(100,100))
    
    #Boutons menus
    
    
    bouton_save=Button(fenetre, 
                       " Sauvegarder ",
                       BLEU,
                       pygame.font.SysFont('chiller', 24), 
                       -300, 
                       550,
                       fontcol=WHITE)
    bouton_save.display_button(fenetre)
    
    bouton_quit=Button(fenetre, " Quitter ",BLEU,pygame.font.SysFont('chiller', 24), -150, 550,fontcol=WHITE)
    bouton_quit.display_button(fenetre)
    
    bouton_suiv=Button(fenetre, " Suivant ",BLEU,pygame.font.SysFont('chiller', 24), 350,40,fontcol=WHITE)
    bouton_suiv.display_button(fenetre)
    
    
    #Carte éjectée
    pivotgauche=pygame.image.load(os.path.abspath(os.path.join('img_cartes','pivotgauche.png'))).convert_alpha()
    bouton_pivot_gauche=Button_img(fenetre,
                                   pivotgauche,
                                   (550,80),
                                   (50,50))
    pivotdroit=pygame.image.load(os.path.abspath(os.path.join('img_cartes','pivotdroit.png'))).convert_alpha()
    bouton_pivot_droit=Button_img(fenetre,
                                  pivotdroit,
                                  (700,80),
                                  (50,50))
    carte_ej=plat.carte_en_dehors
    carte_eject=genere_carte(carte_ej.nom,(50,50))
    fenetre.fill((250,250,250) , (625,80,50,50)) #remplit en blanc la position de l'ancienne carte
    fenetre.blit(carte_eject,(625,80))
    
    
    
    #Joker
    joker=pygame.image.load(os.path.abspath(os.path.join('img_cartes','joker.png'))).convert_alpha()
    boutonJoker=Button_img(fenetre,
                           joker,
                           (800,75),
                           (50,50))
    
    
    #Fenetre Score
    fenetreScore(current_player,plat)
    
    while current_player in plat.Liste_Joueur_IA and plat.check_gagnant()==False: #si le joueur est une IA 
    #while current_player in plat.Liste_Joueur_IA:
        current_player.jouer()
        nextplayer([plat,current_player])
        
    
    
    #BOUCLE INFINIE
    continuer = 1
    while continuer:  
    	for event in pygame.event.get():	#Attente des événements
            if event.type == pygame.MOUSEBUTTONDOWN:
                bouton_save.update_button(fenetre, action=save,arg=[plat,current_player])
                bouton_quit.update_button(fenetre, action=gamequit)
                bouton_suiv.update_button(fenetre, action=nextplayer,arg=[plat,current_player])
                for i in dic_boutons_fleches:
                    dic_boutons_fleches[i].update_button(fenetre,action=deplacement,arg=[i,plat,current_player])
                bouton_pivot_gauche.update_button(fenetre,
                                                  action=chgmt_orientation,
                                                  arg={'carte':plat.carte_en_dehors,'sens':'gauche'})
                bouton_pivot_droit.update_button(fenetre,
                                                 action=chgmt_orientation,
                                                 arg={'carte':plat.carte_en_dehors,'sens':'droit'})
                boutonJoker.update_button(fenetre,
                                          action=Joker,
                                          arg=[plat,current_player])
                
            elif event.type==KEYDOWN: #evenement clavier
                
                if event.key in [273,274,275,276]:
                    move_player(plat,current_player,event.key,plateau,fenetre)
            elif event.type == QUIT:
                continuer=0
                pygame.quit()
    	#Rafraichissement
    	pygame.display.flip()
    


def save(arg):
    print("save")
    plat=arg[0]
    current_player=arg[1]
    sac = SaC2.SandC2()
    sac.save_game_file(plat, current_player)

def gamequit():
    print("Quit")
    pygame.quit()
    sys.exit()
    
def deplacement(arg):
    """Actualise la matrice des cartes
    arg : list[fleche,plateau]"""
    global carte_ej
    fleche=arg[0]
    plat=arg[1]
    current_player=arg[2]
    if current_player in plat.Liste_Joueur_H:
        if current_player.deplacement_effectué==False :
            coord_x, coord_y = plat.convertir_Fleche2Coord(fleche)
            #print(coord_x,coord_y)
            #régénérer plat
            plat.coulisser(coord_x,coord_y)
            current_player.deplacement_effectué=True
            plateau=pygame.Surface((cote_fenetre,cote_fenetre)) #vider le plateau
            #fond = pygame.image.load(os.path.join('img_cartes',"Iceberg.jpg")).convert()
            #plateau.blit(fond, (0,0))
            plateau.fill((250,250,250)) #fond blanc
            afficher(plat,plateau,fenetre,current_player)
            fenetre.blit(plateau,(100,100))
    
    
def chgmt_orientation(arg):
    
    arg['carte'].pivoter(arg['sens'])
   
    fenetre.fill((250,250,250) , (625,80,50,50)) #remplit en blanc la position de l'ancienne carte
    carte_ej=genere_carte(arg['carte'].nom,(50,50)) 
    fenetre.blit(carte_ej,(625,80))
    pygame.display.flip()
    

def move_player(plat,joueur,move,plateau,fenetre):
    if joueur in plat.Liste_Joueur_H and joueur.deplacement_effectué==True:
        plat.deplacement_joueur(plat,joueur,move)
        plateau=pygame.Surface((cote_fenetre,cote_fenetre)) #vider le plateau
        plateau.fill((250,250,250)) #fond blanc
        afficher(plat,plateau,fenetre,joueur)
        fenetre.blit(plateau,(100,100))
        fenetreScore(joueur,plat)
    
def nextplayer(arg):
    global current_player
    
    plat=arg[0]
    current_player=arg[1]
    current_player.deplacement_effectué=False
    current_player.carte_visit=[current_player.position_detail]
    current_player=plat.dict_ID2J[current_player.joueur_suivant]
    
    plateau=pygame.Surface((cote_fenetre,cote_fenetre)) #vider le plateau
    plateau.fill((250,250,250)) #fond blanc
    afficher(plat,plateau,fenetre,current_player)
    fenetre.blit(plateau,(100,100))
        
    fenetreScore(current_player,plat)
    
    while current_player in plat.Liste_Joueur_IA and plat.check_gagnant()==False: #si le joueur est une IA
    #while current_player in plat.Liste_Joueur_IA:
        current_player.jouer()
        nextplayer([plat,current_player])
        
    return current_player

def Joker(arg):
    print("help needed")
    plat=arg[0]
    current_player=arg[1]
    if current_player.joker_used==False and current_player.deplacement_effectué==False :
        current_player.greedy(plat)
        nextplayer([plat,current_player])
        current_player.joker_used=True
        fenetreScore(current_player,plat)

        
def fenetreScore(joueur,plat):
    '''joueur : objet de la classe joueur
    plat : objet plateau'''
    pepite=pygame.transform.scale(img_pepite,(25,25))
    fantome=pygame.transform.scale(img_fantome,(25,25))
    
    
    img_croix=pygame.image.load(os.path.abspath(os.path.join('img_cartes',"croix.png"))).convert_alpha()
    croix=pygame.transform.scale(img_croix,(25,25))
    
    
    scoreframe=pygame.Surface((400,400))
    
    scoreframe.fill(WHITE)
    
    fenetre.fill(BLEUGRIS , (530,30,250,40))
    ecrire("Au tour de: "+str(joueur.identifiant),
                       fenetre,
                       (550,30),
                       BLEU,
                       30,
                       fontname="chiller")
    
    
    valscore=joueur.nb_points
    pepitescore=joueur.pepite
    
    img_perso=pygame.image.load(os.path.abspath(os.path.join('img_cartes',dict_pinguin_img[joueur.identifiant]))).convert_alpha()
    perso=pygame.transform.scale(img_perso,(25,25))
    scoreframe.blit(perso,(50,50))
    ecrire('Score : '+str(valscore),scoreframe,(100,50),BLEU,fontname="chiller")
    scoreframe.blit(pepite,(350,60))
    ecrire(pepitescore,scoreframe,(280,60))
    
    ordreMission=pygame.Surface((380,100),pygame.SRCALPHA)
    ordreMission.fill(WHITE)
    ecrire('Ordre de mission : ',
           ordreMission,
           (5,5),
           BLEU,
           fontsize=30,
           fontname="chiller")
 
    
    nombre_fantomes=len(joueur.ordre_de_mission)
    taille_espace=(360-50*nombre_fantomes)/(nombre_fantomes-1)

    for i in range (nombre_fantomes):
        ordreMission.blit(fantome,(10+i*(50+taille_espace),50))
        #print(joueur.ordre_de_mission[list(joueur.ordre_de_mission.keys())[i]])
        if joueur.ordre_de_mission[list(joueur.ordre_de_mission.keys())[i]]==False:
            ordreMission.blit(croix,(10+i*(50+taille_espace),50))
        ecrire(list(joueur.ordre_de_mission.keys())[i],
               ordreMission,
               (20+i*(50+taille_espace),80),
               CIEL,
               20)
        
    scoreframe.blit(ordreMission,(10,100))
        
    scoreAdverse=pygame.Surface((380,180))
    scoreAdverse.fill(WHITE)
    ecrire('Scores des pinguins ennemis : ',
           scoreAdverse,
           (5,5),
           BLEU,
           fontsize=30,
           fontname="chiller")
    
    
    Ladverse=plat.Liste_Joueur #suppression du joueur concerné
    idj=Ladverse.index(joueur)        

    
    for i in range(len(Ladverse)):
        if i !=idj:
            frameJoueur=pygame.Surface((360,50))
            frameJoueur.fill(WHITE)
            adv=Ladverse[i]
            img_perso=pygame.image.load(os.path.abspath(os.path.join('img_cartes',dict_pinguin_img[adv.identifiant]))).convert_alpha()
            perso=pygame.transform.scale(img_perso,(25,25))
            frameJoueur.blit(perso,(0,0))
            ecrire(adv.nb_points,
                   frameJoueur,
                   (30,5),
                   fontsize=25)
                
            nombre_fantomes=len(adv.ordre_de_mission)
            taille_espace=(300-50*nombre_fantomes)/(nombre_fantomes-1)
            for j in range (nombre_fantomes):
                frameJoueur.blit(fantome,(50+j*(50+taille_espace),0))  
                #print(adv.ordre_de_mission[list(adv.ordre_de_mission.keys())[j]])
                if adv.ordre_de_mission[list(adv.ordre_de_mission.keys())[j]]==False:
                    frameJoueur.blit(croix,(50+j*(50+taille_espace),0))
            
                ecrire(list(adv.ordre_de_mission.keys())[j],
                       frameJoueur,
                       (50+j*(50+taille_espace),0),
                       CIEL,
                       20)
                
            scoreAdverse.blit(frameJoueur,(10,40+i*50)) 
        
    scoreframe.blit(scoreAdverse,(10,200))
    fenetre.blit(scoreframe,(550,150))
    
    fenetre.fill(WHITE , (550,170,250,30))
    if current_player.joker_used==True:
        print('Joker used')
        ecrire("Joker déjà utilisé ",
                       fenetre,
                       (600,170),
                       RED,
                       25,
                       fontname="chiller") 
    
    #print("==========================",plat.check_gagnant())
    
    if plat.check_gagnant()==True:
        winner(plat)
        
    
        
        
def winner(plat):
    newfenetre = pygame.display.set_mode((1000,600))
    fond = pygame.image.load(os.path.join('img_cartes',"Iceberg.jpg")).convert()    
    newfenetre.blit(fond,(0,0))
    
    podium_img=pygame.image.load(os.path.join("img_cartes","podium.png")).convert_alpha()
    podium=pygame.transform.scale(podium_img,(450,300))
    winframe=pygame.Surface((700,400))
    winframe.fill(WHITE)
    winframe.blit(podium,(120,70))
    
    Classement=plat.Liste_Classement
    gagnant=Classement[0][1]
    
    img_perso=pygame.image.load(os.path.abspath(os.path.join('img_cartes',dict_pinguin_img[gagnant.identifiant]))).convert_alpha()
    perso=pygame.transform.scale(img_perso,(100,100))
    winframe.blit(perso,(300,30))    
    ecrire(gagnant.nb_points,winframe,(310,150),BLACK,70,'chiller')

    
    
    n=0 #compteur joueur
    for adv in Classement[1:]:
            pos=(140+n*300,130)
            if len(Classement)==4 :
                if adv!=Classement[-1]: # on n'affiche pas le 4e
                    img_perso=pygame.image.load(os.path.abspath(os.path.join('img_cartes',dict_pinguin_img[adv[1].identifiant]))).convert_alpha()
                    perso=pygame.transform.scale(img_perso,(100,100))                
                    winframe.blit(perso,pos)
            else :
                img_perso=pygame.image.load(os.path.abspath(os.path.join('img_cartes',dict_pinguin_img[adv[1].identifiant]))).convert_alpha()
                perso=pygame.transform.scale(img_perso,(100,100))                
                winframe.blit(perso,pos)
            if n==0: #joueur2
                ecrire(adv[1].nb_points,winframe,(pos[0]+70,pos[1]+130),BLACK,70,'chiller')
            if n==1 : #joueur 3
                ecrire(adv[1].nb_points,winframe,(pos[0]-40,pos[1]+130),BLACK,70,'chiller')
            n+=1
    
    
    if len(Classement)>3:
        ecrire(Classement[-1][1].identifiant+" tu es un looser...",winframe,(200,350),BLEU,30,'chiller')
        
        
    bouton_quit=Button(fenetre, " Quitter ",BLEU,pygame.font.SysFont('chiller', 30), -150, 550,fontcol=WHITE)
    bouton_quit.display_button(fenetre)
    newfenetre.blit(winframe,(170,100))
    
if __name__=="__main__":
    ecran(Jeu_mine.JEU())

