# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 12:01:43 2019

@author: eliott
"""

import os
import tkinter as tk
from tkinter import ttk
import SaC

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
                                5:self.creer_serveur}
        
        self.launch()
        self.fen.mainloop()
    
    def retour(self):
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
                                 text = "Partie rapide")
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
                                                                padx = 15)
        self.Scale_DimPlateau = tk.Spinbox(master = self.fen,
                                    format_='%2.0f',
                                    from_ = 7, to = 25, increment = 2,
                                    width = 5,
                                    wrap = True,
                                    state = "readonly",
                                    textvariable = self.taile_plateau,
                                    command = self.update_nb_fantome_max, 
                                    bg = "white")
        self.Scale_DimPlateau.grid(column=1, row=_start_row)
        
        Scale_NbJoueur = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Nombre de Joueurs",
                                    from_ = 2, to = 4, resolution = 1,
                                    tickinterval = 2,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        Scale_NbJoueur.grid(column=2, row=_start_row, columnspan = 2)
        
        self.Scale_NbFantome = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Nombre de Fantômes",
                                    from_ = 1, to = self.nb_fantome_max, resolution = 1,
                                    tickinterval = self.nb_fantome_max-1,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        self.Scale_NbFantome.grid(column=0, row=_start_row+1, columnspan = 2)
        
        self.Scale_NbFantomeOdM = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Nombre de Fantômes sur l'ordre de mission",
                                    from_ = 1, to = self.nb_fantome_max, resolution = 1,
                                    tickinterval = self.nb_fantome_max-1,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        self.Scale_NbFantomeOdM.grid(column=2, row=_start_row+1, columnspan = 2)
        
        Scale_PtsPepite = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Points pour 1 pépite d'or",
                                    from_ = 1, to = 100, resolution = 1,
                                    tickinterval = 99,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        Scale_PtsPepite.grid(column=0, row=_start_row+2, columnspan = 4)
        
        Scale_PtsFantome = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Points pour 1 fantôme",
                                    from_ = 1, to = 100, resolution = 1,
                                    tickinterval = 99,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        Scale_PtsFantome.grid(column=0, row=_start_row+3, columnspan = 4)
        
        Scale_PtsFantomeOdM = tk.Scale(master = self.fen,
                                    orient = "horizontal",
                                    label = "Points pour 1 fantôme de l'OM",
                                    from_ = 1, to = 100, resolution = 1,
                                    tickinterval = 99,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        Scale_PtsFantomeOdM.grid(column=0, row=_start_row+4, columnspan = 4)
        
        
        scalers = [self.Scale_DimPlateau, Scale_NbJoueur,
                   self.Scale_NbFantome, self.Scale_NbFantomeOdM,
                   Scale_PtsPepite, Scale_PtsFantome, Scale_PtsFantomeOdM]
        SaverCharger = SaC.Save_and_Charge(scalers, self)
        values = SaverCharger.read_file(_file_path = os.getcwd()+"/config.csv")
        values = [val.split(",")[1] for val in values]
        SaverCharger.setScalersValues(values)
        
        ChargeConfig_Button = ttk.Button(master = self.fen,
                                        text = "Charger une configuration",
                                        command = SaverCharger.charge_config_file)
        ChargeConfig_Button.grid(column=1, row=_start_row+10, padx = 15)
        
        SaveConfig_Button = ttk.Button(master = self.fen,
                                        text = "Sauvegarder une configuration",
                                        command = SaverCharger.save_config_file)
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
                                 text = "Créer la partie")
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
        self.Scale_NbFantomeOdM.config(to = self.nb_fantome_max,
                                    tickinterval = self.nb_fantome_max-1)
    
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
                                 command = self.creer_serveur)
        creer_serveur.grid(column = 1, row = 0, padx = 15)
        
        Retour = ttk.Button(self.fen,
                            text = "Retour",
                            command = self.retour)
        Retour.grid(column = 2, row = 0, padx = 15)
    
    def rejoindre_serveur(self):
        self.fen.title("Jouer en ligne - Mine Hantée")
        if self.navigation_flow[-1] != 3:
            self.navigation_flow.append(3)
        for widget in self.fen.winfo_children():
            widget.destroy()
        
        tk.Label(self.fen, text = "Port:").grid(column=0, row=0, padx = 15)
        port = tk.Entry(self.fen)
        port.grid(column = 1, row = 0, padx = 15)
        port.insert(0,"50026")
        
        tk.Label(self.fen, text = "Addresse:").grid(column=0, row=1, padx = 15)
        addresse = tk.Entry(self.fen)
        addresse.grid(column = 1, row = 1, padx = 15)
        addresse.insert(0,"127.0.0.1")
        
        self.message_space = tk.Label(self.fen)
        self.message_space.grid(column=0, row=2, columnspan = 2, padx = 15)
        
        connexion_serveur = ttk.Button(self.fen,
                                 text = "Connexion au serveur")
        connexion_serveur.grid(column = 0, row = 4, padx = 15)
        
        Retour = ttk.Button(self.fen,
                            text = "Retour",
                            command = self.retour)
        Retour.grid(column = 1, row = 4, padx = 15)
    
    def creer_serveur(self):
        self.fen.title("Configurer une partie - Mine Hantée")
        if self.navigation_flow[-1] != 2:
            self.navigation_flow.append(2)
        for widget in self.fen.winfo_children():
            widget.destroy()
            
        self.taile_plateau = 7
        self.nb_fantome_max = 21
        
        tk.Label(self.fen, text = "Port:").grid(column=0, row=0, columnspan=2, padx = 15)
        port = tk.Entry(self.fen)
        port.grid(column = 2, row = 0, columnspan=2, padx = 15)
        port.insert(0,"50026")
        
        tk.Label(self.fen, text = "Addresse:").grid(column=0, row=1, columnspan=2, padx = 15)
        addresse = tk.Entry(self.fen)
        addresse.grid(column = 2, row = 1, columnspan=2, padx = 15)
        addresse.insert(0,"127.0.0.1")
        
        self.setup_scalers(_start_row=2)
        
        self.message_space = tk.Label(self.fen)
        self.message_space.grid(column=0, row=9, columnspan = 4, padx = 15)
        
        Creer_partie = ttk.Button(self.fen,
                                 text = "Créer la partie")
        Creer_partie.grid(column = 0, row = 12, padx = 15)
        
        Retour = ttk.Button(self.fen,
                                 text = "Retour",
                                 command = self.retour)
        Retour.grid(column = 3, row = 12, padx = 15)
        
if __name__=="__main__":
    LauncherMineHantee()