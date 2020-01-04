# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 12:01:43 2019

@author: eliott
"""

import os
import subprocess
import threading

import tkinter as tk
from tkinter import ttk

import SaC
import clientMH as cMH

import Jeu_mine as Jm

import vizpygame as vpyg


class LauncherMineHantee(object):
    def __init__(self):
        self.fen = tk.Tk()
        self.fen.grid_columnconfigure(0,weight=1)
        self.fen.grid_columnconfigure(1,weight=1)
        self.fen.grid_rowconfigure(0,weight=1)
        self.fen.grid_rowconfigure(1,weight=1)
        
        style = ttk.Style(self.fen)
        #theme dispo : ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        style.theme_use('xpnative')
        
        self.navigation_flow = [0]
        self.navigation_tool = {0:self.launch,
                                1:self.jouer_local, 
                                2:self.configurer_partie,
                                3:self.jouer_ligne,
                                4:self.rejoindre_serveur,
                                5:self.creer_configurer_serveur}
        
        self.SaverCharger = SaC.Save_and_Charge(_ref_launcher=self)
        
        self.partie_en_ligne = False
        self.server_subprocess = None
        
        self.launch()
        self.fen.mainloop()
    
    def retour(self):
        
        if (self.partie_en_ligne):
            self.partie_en_ligne = False
        
        self.navigation_flow = self.navigation_flow[:-1]
        self.navigation_tool[self.navigation_flow[-1]]()
        

    def launch(self):
        self.fen.title("Jeu de la Mine Hantée")
        if self.navigation_flow[-1] != 0:
            self.navigation_flow.append(0)
        for widget in self.fen.winfo_children():
            widget.destroy()
        
        Jouer_local = ttk.Button(self.fen,
                                 text = "Jouer en Local",
                                 command = self.jouer_local)
        Jouer_local.grid(column = 0, row = 0, padx = 15)
        
        Jouer_Ligne = ttk.Button(self.fen,
                                 text = "Jouer en Ligne", 
                                 command = self.jouer_ligne)
        Jouer_Ligne.grid(column = 1, row = 0, padx = 15)        
    
    def jouer_local(self):
        self.fen.title("Jouer en local - Mine Hantée")
        if self.navigation_flow[-1] != 1:
            self.navigation_flow.append(1)
        for widget in self.fen.winfo_children():
            widget.destroy()
        
        Partie_rapide = ttk.Button(self.fen,
                                 text = "Partie rapide",
                                 command = self.choix_pseudo)
        Partie_rapide.grid(column = 0, row = 0, padx = 15)
        
        Configurer_partie = ttk.Button(self.fen,
                                 text = "Configurer une partie",
                                 command = self.configurer_partie)
        Configurer_partie.grid(column = 1, row = 0, padx = 15)
        
        Retour = ttk.Button(self.fen,
                                 text = "Retour",
                                 command = self.retour)
        Retour.grid(column = 2, row = 0, padx = 15)
    
    def setup_scalers(self, _start_row = 0):
        
        tk.Label(self.fen, text = "Dimension du plateau:").grid(column=0, 
                                                                row=_start_row,
                                                                padx = 15,
                                                                columnspan = 2)
        self.Scale_DimPlateau = tk.Spinbox(master = self.fen,
                                    format_='%2.0f',
                                    from_ = 7, to = 25, increment = 2,
                                    width = 5,
                                    wrap = True,
                                    state = "readonly",
                                    textvariable = self.taile_plateau,
                                    command = self.update_nb_fantome_max, 
                                    bg = "white")
        self.Scale_DimPlateau.grid(column=2, row=_start_row, columnspan = 2)
        
        self.Scale_NbJoueur = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Nombre de Joueurs",
                                    from_ = 2, to = 4, resolution = 1,
                                    tickinterval = 2,
                                    width = 20, length = 500,
                                    command = self.update_nb_joueur_IA_max,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        self.Scale_NbJoueur.grid(column=0, row=_start_row+1, columnspan = 2)
        
        self.Scale_NbJoueur_IA = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Nombre d'IA parmis les joueurs",
                                    from_ = 0, to = self.Scale_NbJoueur.get(), resolution = 1,
                                    tickinterval = self.Scale_NbJoueur.get(),
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        self.Scale_NbJoueur_IA.grid(column=2, row=_start_row+1, columnspan = 2)
        
        self.Scale_NbFantome = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Nombre de Fantômes",
                                    from_ = 1, to = self.nb_fantome_max, resolution = 1,
                                    tickinterval = self.nb_fantome_max-1,
                                    width = 20, length = 500,
                                    command = self.update_nb_fantome_OM_max,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        self.Scale_NbFantome.grid(column=0, row=_start_row+2, columnspan = 2)
        
        self.Scale_NbFantomeOdM = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Nombre de Fantômes sur l'OdM",
                                    from_ = 1, to = 21, resolution = 1,
                                    tickinterval = self.nb_fantome_max-1,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        self.Scale_NbFantomeOdM.grid(column=2, row=_start_row+2, columnspan = 2)
        
        self.Scale_NbPepite = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Nombre de pépites",
                                    from_ = 1, to = self.taile_plateau*self.taile_plateau, resolution = 1,
                                    tickinterval = self.taile_plateau*self.taile_plateau-1,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        self.Scale_NbPepite.grid(column=0, row=_start_row+3, columnspan = 2)
        
        self.Scale_PtsPepite = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Points pour 1 pépite d'or",
                                    from_ = 1, to = 100, resolution = 1,
                                    tickinterval = 99,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        self.Scale_PtsPepite.grid(column=2, row=_start_row+3, columnspan = 2)
        
        self.Scale_PtsFantome = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Points pour 1 fantôme",
                                    from_ = 1, to = 100, resolution = 1,
                                    tickinterval = 99,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        self.Scale_PtsFantome.grid(column=0, row=_start_row+4, columnspan = 4)
        
        self.Scale_PtsFantomeOdM = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Points pour 1 fantôme de l'OM",
                                    from_ = 1, to = 100, resolution = 1,
                                    tickinterval = 99,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        self.Scale_PtsFantomeOdM.grid(column=0, row=_start_row+5, columnspan = 4)
        
        
        scalers = [self.Scale_DimPlateau, self.Scale_NbJoueur, self.Scale_NbJoueur_IA,
                   self.Scale_NbFantome, self.Scale_NbFantomeOdM, self.Scale_NbPepite,
                   self.Scale_PtsPepite, self.Scale_PtsFantome, self.Scale_PtsFantomeOdM]
        self.SaverCharger.scalers = scalers
        values = self.SaverCharger.read_file(_file_path = os.getcwd()+"/config.csv")
        values = [val.split(",")[1] for val in values]
        self.SaverCharger.setScalersValues(values)
        
        ChargeConfig_Button = ttk.Button(master = self.fen,
                                        text = "Charger une configuration",
                                        command = self.SaverCharger.charge_config_file)
        ChargeConfig_Button.grid(column=1, row=_start_row+10, padx = 15)
        
        SaveConfig_Button = ttk.Button(master = self.fen,
                                        text = "Sauvegarder une configuration",
                                        command = self.SaverCharger.save_config_file)
        SaveConfig_Button.grid(column=2, row=_start_row+10, padx = 15)
    
    def configurer_partie(self):
        
        self.fen.title("Configurer une partie - Mine Hantée")
        if self.navigation_flow[-1] != 2:
            self.navigation_flow.append(2)
        for widget in self.fen.winfo_children():
            widget.destroy()
            
        self.taile_plateau = 7
        self.nb_fantome_max = 21
        
        self.setup_scalers()
        
        self.message_space = tk.Label(self.fen)
        self.message_space.grid(column=0, row=9, columnspan = 4, padx = 15)
        
        Creer_partie = ttk.Button(self.fen,
                                 text = "Créer la partie",
                                 command = self.choix_pseudo)
        Creer_partie.grid(column = 0, row = 10, padx = 15)
        
        Retour = ttk.Button(self.fen,
                                 text = "Retour",
                                 command = self.retour)
        Retour.grid(column = 3, row = 10, padx = 15)
        
    def update_nb_fantome_max(self):
        N = int(self.Scale_DimPlateau.get())
        self.nb_fantome_max = N**2-4*(N-1)-((N-4)//2+1)**2
        self.Scale_NbFantome.config(to = self.nb_fantome_max,
                                    tickinterval = self.nb_fantome_max-1)
        self.Scale_NbPepite.config(to = N*N,
                                    tickinterval = N*N-1)
    
    def update_nb_fantome_OM_max(self, N):
        self.Scale_NbFantomeOdM.config(to = int(N),
                                       tickinterval = int(N)-1)
    
    def update_nb_joueur_IA_max(self, N):
        self.Scale_NbJoueur_IA.config(to = int(N),
                                       tickinterval = int(N))
        
    
    def jouer_ligne(self):
        self.fen.title("Jouer en ligne - Mine Hantée")
        if self.navigation_flow[-1] != 3:
            self.navigation_flow.append(3)
        for widget in self.fen.winfo_children():
            widget.destroy()
            
        rejoindre_serveur = ttk.Button(self.fen,
                                 text = "Rejoindre un serveur", 
                                 command = self.rejoindre_serveur)
        rejoindre_serveur.grid(column = 0, row = 0, padx = 15)
        
        creer_serveur = ttk.Button(self.fen,
                                 text = "Créer un serveur",
                                 command = self.creer_configurer_serveur)
        creer_serveur.grid(column = 1, row = 0, padx = 15)
        
        Retour = ttk.Button(self.fen,
                            text = "Retour",
                            command = self.retour)
        Retour.grid(column = 2, row = 0, padx = 15)
    
    def rejoindre_serveur(self):
        self.fen.title("Jouer en ligne - Mine Hantée")
        if self.navigation_flow[-1] != 4:
            self.navigation_flow.append(4)
        for widget in self.fen.winfo_children():
            widget.destroy()
        
        tk.Label(self.fen, text = "Port:").grid(column=0, row=0, padx = 15)
        self.PORT = tk.Entry(self.fen)
        self.PORT.grid(column = 1, row = 0, padx = 15)
        self.PORT.insert(0,"50026")
        
        tk.Label(self.fen, text = "Addresse:").grid(column=0, row=1, padx = 15)
        self.HOST = tk.Entry(self.fen)
        self.HOST.grid(column = 1, row = 1, padx = 15)
        self.HOST.insert(0,"127.0.0.1")
        
        self.message_space = tk.Label(self.fen)
        self.message_space.grid(column=0, row=2, columnspan = 2, padx = 15)
        
        connexion_serveur = ttk.Button(self.fen,
                                 text = "Connexion au serveur", 
                                 command = self.serveur_choix_pseudo)
        connexion_serveur.grid(column = 0, row = 4, padx = 15)
        
        Retour = ttk.Button(self.fen,
                            text = "Retour",
                            command = self.retour)
        Retour.grid(column = 1, row = 4, padx = 15)
    
    def creer_configurer_serveur(self):
        self.fen.title("Configurer une partie - Mine Hantée")
        if self.navigation_flow[-1] != 5:
            self.navigation_flow.append(5)
        for widget in self.fen.winfo_children():
            widget.destroy()
            
        self.taile_plateau = 7
        self.nb_fantome_max = 21
        
        tk.Label(self.fen, text = "Port:").grid(column=0, row=0, columnspan=2, padx = 15)
        self.PORT = tk.Entry(self.fen)
        self.PORT.grid(column = 2, row = 0, columnspan=2, padx = 15)
        self.PORT.insert(0,"50026")
        
        tk.Label(self.fen, text = "Addresse:").grid(column=0, row=1, columnspan=2, padx = 15)
        self.HOST = tk.Entry(self.fen)
        self.HOST.grid(column = 2, row = 1, columnspan=2, padx = 15)
        self.HOST.insert(0,"127.0.0.1")
        
        self.setup_scalers(_start_row=2)
        
        self.message_space = tk.Label(self.fen)
        self.message_space.grid(column=0, row=9, columnspan = 4, padx = 15)
        
        Creer_serveur = ttk.Button(self.fen,
                                 text = "Créer la partie",
                                 command = self.creer_serveur)
        Creer_serveur.grid(column = 0, row = 12, padx = 15)
        
        Retour = ttk.Button(self.fen,
                                 text = "Retour",
                                 command = self.retour)
        Retour.grid(column = 3, row = 12, padx = 15)
    
    def subprocess_creation_serveur(self):
        subprocess.Popen(["cmd.exe", "/c", "start",
                          "python", "serveurMH.py",
                          self.PORT, self.HOST],shell = True)
        
    def creer_serveur(self):
        self.PORT = self.PORT.get()
        self.HOST = self.HOST.get()
        self.thread_serveur = threading.Thread(target = self.subprocess_creation_serveur)
        self.thread_serveur.start()
        self.partie_en_ligne = True
        self.choix_pseudo()
    
    def serveur_choix_pseudo(self):
        self.PORT = self.PORT.get()
        self.HOST = self.HOST.get()
        self.partie_en_ligne = True
        self.choix_pseudo()
    
    def choix_pseudo(self):
        #avant de construire la fenetre du pseudo, on enregistre les valeurs des
        #scalers
        self.get_plateau_options()
        
        
        self.fen.title("Joindre la partie - Mine Hantée")
        if self.navigation_flow[-1] != 6:
            self.navigation_flow.append(6)
        for widget in self.fen.winfo_children():
            widget.destroy()
        
        if (self.partie_en_ligne):
            tk.Label(self.fen, text = "Pseudonyme:").grid(column=0, row=0, padx = 15)
            self.PSEUDO = tk.Entry(self.fen)
            self.PSEUDO.grid(column = 1, row = 0, padx = 15)
            self.PSEUDO.insert(0,"Joueur_1")
        
        else:
            for i in range (self.value_NbJoueur-self.value_NbJoueur_IA):
                tk.Label(self.fen, text = "Pseudonyme Joueur "+str(i)+":").grid(
                                                    column=0, row=i, padx = 15)
                self.PSEUDO = tk.Entry(self.fen)
                self.PSEUDO.grid(column = 1, row = i, padx = 15)
                self.PSEUDO.insert(0,"Joueur_"+str(i))
        
        for i in range (self.value_NbJoueur_IA):
            k = i+self.value_NbJoueur-self.value_NbJoueur_IA
            tk.Label(self.fen, text = "Difficulté IA "+str(i)+":").grid(
                                                column=0, row=k, padx = 15)
            self.IA_NIV = ttk.Combobox(self.fen,
                                       state = "readonly",
                                       values = ["facile", "normale", "difficile"])
            self.IA_NIV.grid(column = 1, row = k, padx = 15)
            self.IA_NIV.set("normale")
        
        self.message_space = tk.Label(self.fen)
        self.message_space.grid(column=0, row=1, columnspan = 2)
        
        Creer_serveur = ttk.Button(self.fen,
                                   text = "Rejoindre la partie",
                                   command = self.rejoindre_partie)
        Creer_serveur.grid(column = 0, row = 5, padx = 15)
        
        Retour = ttk.Button(self.fen,
                                 text = "Retour",
                                 command = self.retour)
        Retour.grid(column = 1, row = 5, padx = 15)
    
    def get_plateau_options(self):
        
        try :
            self.value_DimPlateau = int(self.Scale_DimPlateau.get())
            self.value_NbJoueur = int(self.Scale_NbJoueur.get())
            self.value_NbJoueur_IA = int(self.Scale_NbJoueur_IA.get())
            self.value_NbFantome = int(self.Scale_NbFantome.get())
            self.value_NbFantomeOdM = int(self.Scale_NbFantomeOdM.get())
            self.value_NbPepite = int(self.Scale_NbPepite.get())
            self.value_PtsPepite = int(self.Scale_PtsPepite.get())
            self.value_PtsFantome = int(self.Scale_PtsFantome.get())
            self.value_PtsFantomeOdM = int(self.Scale_PtsFantomeOdM.get())
        except:
            self.value_DimPlateau = 7
            self.value_NbJoueur = 2
            self.value_NbJoueur_IA = 1
            self.value_NbFantome = 21
            self.value_NbFantomeOdM = 3
            self.value_NbPepite = 49
            self.value_PtsPepite = 1
            self.value_PtsFantome = 5
            self.value_PtsFantomeOdM = 15
            
        print(self.value_DimPlateau,
            self.value_NbJoueur,
            self.value_NbJoueur_IA,
            self.value_NbFantome,
            self.value_NbFantomeOdM,
            self.value_NbPepite,
            self.value_PtsPepite,
            self.value_PtsFantome,
            self.value_PtsFantomeOdM)
            
    
    def rejoindre_partie(self):
        self.pseudo = self.PSEUDO.get()
        if (self.partie_en_ligne):
            self.ref_client = cMH.Client(self)
            self.plateau_exemple()
        
        else:
            self.fen.destroy()
            plateau = Jm.JEU(dimension = self.value_DimPlateau,
                              nombre_joueur = self.value_NbJoueur,
                              nombre_joueur_IA = self.value_NbJoueur_IA,
                              nombre_ghost = self.value_NbFantome,
                              nombre_ordre_mission = self.value_NbFantomeOdM,
                              nombre_pepite = self.value_NbPepite,
                              pts_pepite = self.value_PtsPepite,
                              pts_fantome = self.value_PtsFantome,
                              pts_ordre_mission = self.value_PtsFantomeOdM,
                              _SaC = self.SaverCharger)
            vpyg.ecran(plateau)
            
    
    def plateau_exemple(self):
        self.fen.title("Joindre la partie - Mine Hantée")
        if self.navigation_flow[-1] != 6:
            self.navigation_flow.append(6)
        for widget in self.fen.winfo_children():
            widget.destroy()
        
        Info_serveur = ttk.Button(self.fen,
                                   text = "touche test",
                                   command = self.ref_client.envoyer_Touche)
        Info_serveur.grid(column = 0, row = 2, padx = 15)

        
if __name__=="__main__":
    LauncherMineHantee()