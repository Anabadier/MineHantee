# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:28:20 2019

@author: eliot
"""
import os
from tkinter import filedialog as tkfd

 
class Save_and_Charge(object):
    def __init__(self, _scalers = None, _ref_launcher = None):
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
        file_path = tkfd.askopenfilename(filetypes = [('CSV Files', '*.csv')])
        
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
                file.write("dim_plateau," + str(values[0].strip())+ "\n" +
                           "nb_joueur," + str(values[1])+ "\n" +
                           "nb_joueur_IA," + str(values[2])+ "\n" +
                           "nb_fantome," + str(values[3])+ "\n" +
                           "nb_fantome_OdM," + str(values[4])+ "\n" +
                           "nb_pepite," + str(values[5])+ "\n" +
                           "pts_pepite," + str(values[6])+ "\n" +
                           "pts_fantome," + str(values[7])+ "\n" +
                           "pts_fantome_OdM," + str(values[8]))
                file.close()
                print("Le fichier a bien été sauvegardé")
                
            except IndexError:
                print("Une erreur de valeur est survenue lors de la sauvegarde de fichier.")
                file.close()
    
    def log_plateau(self, _plateau, _overwrite = False):
        
        if (not os.path.exists(os.getcwd()+"/"+"log_plateau_last_game.txt")):
            file_object = open(os.getcwd()+"/"+"log_plateau_last_game.txt", 'w')
        else:
            if (_overwrite):
                file_object = open(os.getcwd()+"/"+"log_plateau_last_game.txt", 'w')
            else:
                file_object = open(os.getcwd()+"/"+"log_plateau_last_game.txt", 'a')
        
        file_object.write("******\n")
        dim = _plateau.labyrinthe_detail.shape
        c = 0
        for i in range(dim[0]):
            _str = ""
            for j in range(dim[1]):
                _str += "{0}_{1}_{2}_{3},".format(c,
                        _plateau.labyrinthe_detail[i,j].nom,
                        _plateau.labyrinthe_detail[i,j].position_D,
                        _plateau.labyrinthe_detail[i,j].position_G)
                c+=1
            file_object.write(_str[:-1]+"\n")
        
            
        file_object.close()
        
        
    def charge_game_file(self):
        print("in charge_game_file")
    
    def save_game_file(self):
        print("in save_config_file")
    