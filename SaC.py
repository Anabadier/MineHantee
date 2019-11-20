# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:28:20 2019

@author: eliot
"""

from tkinter import filedialog as tkfd

 
class Save_and_Charge(object):
    def __init__(self, _scalers, _ref_launcher):
        self.scalers = _scalers
        self.ref_launcher = _ref_launcher
    
    def setScalersValues(self, _list_values):
        l = len(_list_values)
        try:
            self.scalers[0].config(state="normal")
            self.scalers[0].delete(0,'end')
            self.scalers[0].insert(1,_list_values[0])
            self.scalers[0].config(state="readonly")
            for k in range(1,l):
                self.scalers[k].set(_list_values[k])
            self.ref_launcher.update_nb_fantome_max()
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
            self.setScalersValues(values)
    
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
    