# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:21:37 2020

@author: augus
"""

from Classe_plateau import Plateau
from Calass_rep import Joueur
from classe_carte import carte
import os
from tkinter import filedialog as tkfd

class SandC2(object):
    
    def __init__(self):
        print('yeah')
    
    def read_file(self, _file_path):
        file = open(_file_path, 'r')
        content = file.readlines()
        file.close()
        return content
        
    def charge_game_file(self,plateau):
        file = tkfd.askopenfilename()
        if file!= "":
            content = self.read_file(file)
            sauv = [val.split(",") for val in content]
            plateau.taille = int(sauv[0][1])
            pts_pepite = int(sauv[1][1])
            pts_fantome = int(sauv[2][1])
            pts_ordre_mission = int(sauv[3][1])
            nb_ordre_mission = int(sauv[4][1])
            """ Généaration d'un plateau avec nos paramètres ? """
            compteur = 5
            new_plateau = Plateau(plateau.taille)
            plateau = new_plateau
            plateau.pts_pepite = pts_pepite
            plateau.pts_fantome = pts_fantome
            plateau.pts_ordre_mission = pts_ordre_mission
            for i in range(plateau.taille):
                for j in range(plateau.taille):
                    plateau.labyrinthe_detail[i][j]=carte('couloir')
                    print(sauv[compteur][1])
                    plateau.labyrinthe_detail[i][j].position_D = (i,j)
                    plateau.labyrinthe_detail[i][j].type = sauv[compteur][1]
                    plateau.labyrinthe_detail[i][j].orientation= int(sauv[compteur][2])
                    plateau.labyrinthe_detail[i][j].position_G = int(sauv[compteur][3])
                    if sauv[compteur][4] == '[]':
                        plateau.labyrinthe_detail[i][j].elements['fantome']=[]
                    else:
                        plateau.labyrinthe_detail[i][j].elements['fantome'] = int(sauv[compteur][3])
                    if sauv[compteur][5] == 'False':
                        plateau.labyrinthe_detail[i][j].elements['pepite']=False
                    else:
                        plateau.labyrinthe_detail[i][j].elements['pepite']=True
                    if sauv[compteur][6] == '[]':
                        plateau.labyrinthe_detail[i][j].elements['joueur']=[]
                    else:
                        sauv[compteur][6]
                    compteur+=1
            print(sauv[compteur])
            print(plateau.labyrinthe_detail)
            "" "On génère les connexions ?"
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
                    print(sauv[compteur][key])
                    print(sauv[compteur][key+1])
                    if sauv[compteur][key+1]=='False':
                        A.ordre_de_mission[int(sauv[compteur][key])]=False
                    else:
                        A.ordre_de_mission[int(sauv[compteur][key])]=True
                    print(A.ordre_de_mission)
                    key= key +2
                Liste_joueur.append(A)
                compteur+=1
            plateau.Liste_Joueur = Liste_joueur
            print(plateau.Liste_Joueur[0])
            plateau.maj_classement
            
 #joueur
                    
                
           
        print("in charge_game_file")
        return(plateau)
    
    
     
    def save_game_file(self,plateau):
        
       
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
                        print(plateau.labyrinthe_detail[i][j])
                        file.write("Carte_position" + "("+ str(plateau.labyrinthe_detail[i][j].position_D[0])+"-"+str(plateau.labyrinthe_detail[i][j].position_D[1])+")"+","
                                   +str(plateau.labyrinthe_detail[i][j].type)+","
                                   +str(plateau.labyrinthe_detail[i][j].orientation)+","+str(plateau.labyrinthe_detail[i][j].position_G)+",")
                        for value in plateau.labyrinthe_detail[i][j].elements.values():
                            file.write(str(value)+",")
                        file.write("\n")
                file.write("Carte_en_dehors,"
                               +str(plateau.carte_en_dehors.type)+","
                               +str(plateau.carte_en_dehors.orientation)+","+"\n")
                for i in plateau.Liste_Joueur:
                    file.write("Joueur,"+str(i.identifiant)+","+str(i.nb_points)+","+str(i.position_graphe)+","+str(i.position_detail[0])+","+str(i.position_detail[1])+",")
                    for key,value in i.ordre_de_mission.items():
                        file.write(str(key)+","+str(value)+",")
                    file.write("\n")

                
                
                file.write("fin"+"\n")          
                file.close()
                print("Le fichier a bien été sauvegardé")
                
            except IndexError:
                print("Une erreur de valeur est survenue lors de la sauvegarde de fichier.")
                file.close()
        print("in save_config_file")

    