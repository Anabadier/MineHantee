# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:28:20 2019

@author: eliot
"""
import os
import tkinter as tk
from tkinter import filedialog as tkfd

 
class Save_and_Charge(object):
    def __init__(self, _scalers):
        self.scalers = _scalers
    
    def setObjectValues(self, _list_Objects, _list_values):
        l = len(_list_values)
        try:
            for k in range(l):
                _list_Objects[k].set(_list_values[k])
            print("Les valeurs ont été chargées.")
        except IndexError:
            print("Un problème est survenu lors du chargement des valeurs.")
    
    def getObjectValues(self, _list_Objects):
        values = []
        for _obj in _list_Objects:
            values += [_obj.get()]
        return values
    
    def read_file(self, _file_path):
        file = open(_file_path, 'r')
        content = file.readlines()
        file.close()
        return content
    
    def charge_config_file(self):
        file_path = tkfd.askopenfilename()
        
        if (file_path != ""):
            content = self.read_file(_file_path=file_path)
            values = [val.split(",")[1] for val in content]
            self.setObjectValues(self.scalers, values)
    
    def save_config_file(self):
        values = self.getObjectValues(self.scalers)

        file = tkfd.asksaveasfile(mode='w',
                                  filetypes = [('CSV Files', '*.csv')],
                                  defaultextension=".csv")
        if file:
            try:
                file.write("dim_plateau" + str(values[0])+ "\n" +
                           "nb_joueur" + str(values[1])+ "\n" +
                           "nb_fantome_OdM" + str(values[2])+ "\n" +
                           "pts_pepite" + str(values[3])+ "\n" +
                           "pts_fantome" + str(values[4])+ "\n" +
                           "pts_fantome_OdM" + str(values[5]))
                file.close()
                print("Le fichier a bien été sauvegardé")
                
            except IndexError:
                print("Une erreur de valeur est survenue lors de la sauvegarde de fichier.")
                file.close()
    
    def charge_game_file(self):
        print("in charge_game_file")
    
    def save_game_file(self):
        print("in save_config_file")

if __name__=="__main__":
    
    def first_window():
        
        PartieNormale_Button = tk.Button(master=fen,
                                        text = "Jouer à une partie standard",
                                        padx=10)
                                        #command = )
        PartieNormale_Button.grid(column=0, row=0) 
        
        ChargeConfig_Button = tk.Button(master=fen,
                                        text = "Configurer une partie",
                                        padx=10,
                                        command = configuration_window)
        ChargeConfig_Button.grid(column=1, row=0)
        
    
    def configuration_window():
        global fen
        
        fen.destroy()
        fen = tk.Tk(className = " Configuration de la Mine")
        
        Scale_DimPlateau = tk.Scale(master = fen,
                                    orient = "horizontal",
                                    label = "Dimension du plateau",
                                    from_ = 7, to = 21, resolution = 2,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        Scale_DimPlateau.grid(column=0, row=0)
        
        Scale_NbJoueur = tk.Scale(master = fen,
                                    orient = "horizontal",
                                    label = "Nombre de Joueurs",
                                    from_ = 2, to = 4, resolution = 1,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        Scale_NbJoueur.grid(column=1, row=0)
        
        Scale_NbFantomeOdM = tk.Scale(master = fen,
                                    orient = "horizontal",
                                    label = "Nombre de Fantômes sur l'ordre de mission",
                                    from_ = 1, to = 21, resolution = 1,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        Scale_NbFantomeOdM.grid(column=0, row=1, columnspan = 2)
        
        Scale_PtsPepite = tk.Scale(master = fen,
                                    orient = "horizontal",
                                    label = "Points pour 1 pépite d'or",
                                    from_ = 1, to = 100, resolution = 1,
                                    tickinterval = 10,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        Scale_PtsPepite.grid(column=0, row=2, columnspan = 2)
        
        Scale_PtsFantome = tk.Scale(master = fen,
                                    orient = "horizontal",
                                    label = "Points pour 1 fantôme",
                                    from_ = 1, to = 100, resolution = 1,
                                    tickinterval = 10,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        Scale_PtsFantome.grid(column=0, row=3, columnspan = 2)
        
        Scale_PtsFantomeOdM = tk.Scale(master = fen,
                                    orient = "horizontal",
                                    label = "Points pour 1 fantôme de l'ordre de mission",
                                    from_ = 1, to = 100, resolution = 1,
                                    tickinterval = 10,
                                    width = 20, length = 500,
                                    activebackground = "#105105105",
                                    relief = "sunken")
        Scale_PtsFantomeOdM.grid(column=0, row=4, columnspan = 2)
        
        
        scalers = [Scale_DimPlateau, Scale_NbJoueur, Scale_NbFantomeOdM,
                   Scale_PtsPepite, Scale_PtsFantome, Scale_PtsFantomeOdM]
        SaverCharger = Save_and_Charge(scalers)
        values = SaverCharger.read_file(_file_path = os.getcwd()+"/config.csv")
        values = [val.split(",")[1] for val in values]
        SaverCharger.setObjectValues(scalers, values)
        
        ChargeConfig_Button = tk.Button(master=fen,
                                        text = "Charger une configuration",
                                        padx=10,
                                        command = SaverCharger.charge_config_file)
        ChargeConfig_Button.grid(column=0, row=10)
        
        SaveConfig_Button = tk.Button(master=fen,
                                        text = "Sauvegarder une configuration",
                                        padx=10,
                                        command = SaverCharger.save_config_file)
        SaveConfig_Button.grid(column=1, row=10)
        
        fen.mainloop()
    
    
    
    fen = tk.Tk(className = " La Mine Hantée")
    
    first_window()
    
    fen.mainloop()
    