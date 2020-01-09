# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:21:37 2020

@author: augus
"""

from Classe_plateau import Plateau
from Calass_rep import Joueur,Joueur_IA
from classe_carte import carte
import os
from tkinter import filedialog as tkfd
import vizpygame as vpyg


class SandC2(object):
    
    def __init__(self):
        pass
    
    def read_file(self, _file_path):
        
        """ Permet d'ouvrir un fichier en mode lecture """
        
        file = open(_file_path, 'r')
        content = file.readlines()
        file.close()
        return content
        
    def charge_game_file(self):#,plateau):
        
        """ Ouvre un fichier de sauvegarde au bon format et transfère les informations 
        de ce dernier dans les bon attributs du jeu """
        
        file = tkfd.askopenfilename()
        if file!= "":
            content = self.read_file(file)
            sauv = [val.split(",") for val in content]
            #plateau.taille = int(sauv[0][1])
            taille = int(sauv[0][1])
            pts_pepite = int(sauv[1][1])
            pts_fantome = int(sauv[2][1])
            pts_ordre_mission = int(sauv[3][1])
            nb_ordre_mission = int(sauv[4][1])
            
            """ Génération d'un plateau avec les paramètres de sauvegarde """
            
            compteur = 5
            plateau = Plateau(taille)
            
            working_plateau = plateau
            working_plateau.pts_pepite = pts_pepite
            working_plateau.pts_fantome = pts_fantome
            working_plateau.pts_ordre_mission = pts_ordre_mission
            for i in range(working_plateau.taille):
                for j in range(working_plateau.taille):
                    working_plateau.labyrinthe_detail[i][j]=carte('couloir')
                    
                    working_plateau.labyrinthe_detail[i][j].position_D = (i,j)
                    working_plateau.labyrinthe_detail[i][j].type = sauv[compteur][1]
                    working_plateau.labyrinthe_detail[i][j].nom = sauv[compteur][1]
                    working_plateau.labyrinthe_detail[i][j].orientation= int(sauv[compteur][2])
                    working_plateau.labyrinthe_detail[i][j].position_G = int(sauv[compteur][3])
                    working_dico={}
                    if sauv[compteur][4] == '[]':
                        working_dico['fantome']=[]
                    else:
                        working_dico['fantome'] = int(sauv[compteur][3])
                    if sauv[compteur][5] == 'False':
                        working_dico['pepite']=False
                    else:
                        working_dico['pepite']=True
                    if sauv[compteur][6] == '[]':
                        working_dico['joueur']=[]
                    else:
                        try:
                            val = sauv[compteur][6][2:-2].split(",")
                        except:
                            val = [sauv[compteur][6][2:-2]]
                        print("===========================", val)
                        working_dico['joueur']=[i for i in val]
                        print("done",working_dico)
                    working_plateau.labyrinthe_detail[i][j].elements = working_dico
                    compteur+=1
            #print(sauv[compteur])
            plateau=working_plateau
            for i in range(plateau.taille):
                for j in range(plateau.taille):
                    print("testultime",plateau.labyrinthe_detail[i][j].type)
            
            """ On génère les connexions """
            
            for i in range(plateau.taille):
                for j in range(plateau.taille): 
                    plateau.etablir_connexion(plateau.labyrinthe_detail[i][j])
                    
            
            plateau.carte_en_dehors.type = sauv[compteur][1]
            plateau.carte_en_dehors.orientation = sauv[compteur][2]
            compteur+=1
            Liste_joueur = []
            while sauv[compteur][0]=="Joueur":
                A = Joueur(sauv[compteur][1])
                A.nb_points = int(sauv[compteur][2])
                A.position_graphe = int(sauv[compteur][3])
                A.position_detail = (int(sauv[compteur][4]),int(sauv[compteur][5]))
                key = 6
                print(nb_ordre_mission)
                A.ordre_de_mission={}
                while key < 5 + (nb_ordre_mission)*2:
                    #print(sauv[compteur][key])
                    #print(sauv[compteur][key+1])
                    if sauv[compteur][key+1]=='False':
                        A.ordre_de_mission[int(sauv[compteur][key])]=False
                    else:
                        A.ordre_de_mission[int(sauv[compteur][key])]=True
                    #print(A.ordre_de_mission)
                    key= key +2
                Liste_joueur.append(A)
                compteur+=1
            plateau.Liste_Joueur_H = Liste_joueur
            Liste_joueur = []
            while sauv[compteur][0]=="Joueur_IA":
                A = Joueur_IA(sauv[compteur][1],sauv[compteur][6])
                A.nb_points = int(sauv[compteur][2])
                A.position_graphe = int(sauv[compteur][3])
                A.position_detail = (int(sauv[compteur][4]),int(sauv[compteur][5]))
                key = 7
                #print(nb_ordre_mission)
                A.ordre_de_mission={}
                while key < 6 + (nb_ordre_mission)*2:
                    #print(sauv[compteur][key])
                    #print(sauv[compteur][key+1])
                    if sauv[compteur][key+1]=='False':
                        A.ordre_de_mission[int(sauv[compteur][key])]=False
                    else:
                        A.ordre_de_mission[int(sauv[compteur][key])]=True
                    #print(A.ordre_de_mission)
                    key= key +2
                Liste_joueur.append(A)
                compteur+=1
            plateau.Liste_Joueur_IA = Liste_joueur
            plateau.Liste_Joueur = plateau.Liste_Joueur_H + plateau.Liste_Joueur_IA
        #print(plateau.Liste_Joueur[0])
            plateau.maj_classement
            current = sauv[compteur][1]
            #print(current)
            for i in plateau.Liste_Joueur:
                #print(i.identifiant)
                if i.identifiant == current:
                    current_player = i
 #          
                
           
        print("in charge_game_file")
        vpyg.ecran(plateau)
        #return((plateau,current_player))
     
    def save_game_file(self, plateau, current_player):
        """ Permet de sauvegarder les fichiers sous forme de texte dans un fichier csv crée, permet d'accéder
        aux informations """
       
        file = tkfd.asksaveasfile(mode='w' , filetypes = [('CSV Files', '*.csv')],
                                  defaultextension=".csv")
        
        if file:
            try:
                file.write("dim_plateau," + str(plateau.taille) + "\n"+
                           "pts_pepite,"+ str(plateau.pts_pepite)+"\n"+
                           "pts_fantome," + str(plateau.pts_fantome) + "\n"+
                           "pts_ordre_mission," + str(plateau.pts_ordre_mission) + "\n"
                           "nb_ordre_mission,"+str(len(plateau.Liste_Joueur[0].ordre_de_mission))+"\n")
                for i in range(len(plateau.labyrinthe_detail)):
                    for j in range(len(plateau.labyrinthe_detail)):
                        #print(plateau.labyrinthe_detail[i][j])
                        file.write("Carte_position" + "("+ str(plateau.labyrinthe_detail[i][j].position_D[0])+"-"+str(plateau.labyrinthe_detail[i][j].position_D[1])+")"+","
                                   +str(plateau.labyrinthe_detail[i][j].type)+","
                                   +str(plateau.labyrinthe_detail[i][j].orientation)+","+str(plateau.labyrinthe_detail[i][j].position_G)+",")
                        for value in plateau.labyrinthe_detail[i][j].elements.values():
                            file.write(str(value)+",")
                        file.write("\n")
                file.write("Carte_en_dehors,"
                               +str(plateau.carte_en_dehors.type)+","
                               +str(plateau.carte_en_dehors.orientation)+","+"\n")
                for i in plateau.Liste_Joueur_H:
                    file.write("Joueur,"+str(i.identifiant)+","+str(i.nb_points)+","+str(i.position_graphe)+","+str(i.position_detail[0])+","+str(i.position_detail[1])+",")
                    for key,value in i.ordre_de_mission.items():
                        file.write(str(key)+","+str(value)+",")
                    file.write("\n")
                    if i.identifiant == current_player.identifiant:
                        current = str(current_player.identifiant)
                for i in plateau.Liste_Joueur_IA:
                    file.write("Joueur_IA,"+str(i.identifiant)+","+str(i.nb_points)+","+str(i.position_graphe)+","+str(i.position_detail[0])+","+str(i.position_detail[1])+","+str(i.niv)+",")
                    for key,value in i.ordre_de_mission.items():
                        file.write(str(key)+","+str(value)+",")
                    file.write("\n")
                    if i.identifiant == current_player.identifiant:
                        current = str(current_player.identifiant)
                file.write("current,"+current +","+"\n")
                file.write("fin"+"\n")          
                file.close()
                print("Le fichier a bien été sauvegardé")
                
            except IndexError:
                print("Une erreur de valeur est survenue lors de la sauvegarde de fichier.")
                file.close()
        print("in save_config_file")

    