# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:23:42 2019

@author: anael
"""

import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
CIEL = 0, 200, 255
RED = 255, 0, 0
ORANGE = 255, 100, 0
GREEN = 0, 255, 0


class Button:
    '''Ajout d'un bouton avec un texte sur img
    Astuce: ajouter des espaces dans les textes pour avoir une même largeur
    de boutons
    dx, dy décalage du bouton par rapport au centre
    action si click
    Texte noir
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
        self.rect = pygame.draw.rect(self.fond, self.color, self.textpos)
        self.fond.blit(self.title, self.textpos)

    def update_button(self, fond, action=None):
        self.fond = fond
        mouse_xy = pygame.mouse.get_pos()
        over = self.rect.collidepoint(mouse_xy)
        if over:
            action()
            if self.color == RED:
                self.color = GREEN
                self.state = True
            elif self.color == GREEN:
                # sauf les + et -, pour que ce soit toujours vert
                if len(self.text) > 5:  # 5 char avec les espaces
                    self.color = RED
                self.state = False
        # à la bonne couleur
        self.rect = pygame.draw.rect(self.fond, self.color, self.textpos)
        self.fond.blit(self.title, self.textpos)

    def display_button(self, fond):
        self.fond = fond
        self.rect = pygame.draw.rect(self.fond, self.color, self.textpos)
        self.fond.blit(self.title, self.textpos)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480))
        self.level = 1
        self.loop = True

        # Définition de la police
        self.big = pygame.font.SysFont('freesans', 48)
        self.small = pygame.font.SysFont('freesans', 36)

        self.create_fond()
        self.create_button()

    def update_textes(self):
        self.textes = [ ["Buggy Server", ORANGE, self.big, 0, 50],
                        ["Level", BLACK, self.small, 0, 150],
                        [str(self.level), BLACK, self.small, 0, 200]]

    def create_fond(self):
        # Image de la taille de la fenêtre
        self.fond = pygame.Surface(self.screen.get_size())
        # En bleu
        self.fond.fill(CIEL)

    def create_button(self):
        self.reset_button = Button(self.fond, "   Reset   ", RED, self.small, 0, 300)
        self.start_button = Button(self.fond, "   Start   ", RED, self.small, 0, 360)
        self.quit_button  = Button(self.fond, "   Quit   ", RED, self.small, 0, 420)
        self.moins_button = Button(self.fond, "  -  ", GREEN, self.small, -100, 200)
        self.plus_button  = Button(self.fond, "  +  ", GREEN, self.small, 100, 200)

    def display_text(self, text, color, font, dx, dy):
        '''Ajout d'un texte sur fond. Décalage dx, dy par rapport au centre.
        '''
        mytext = font.render(text, True, color)  # True pour antialiasing
        textpos = mytext.get_rect()
        textpos.centerx = self.fond.get_rect().centerx + dx
        textpos.centery = dy
        self.fond.blit(mytext, textpos)

    def plus(self):
        self.level += 1
        if self.level == 6: self.level = 5

    def moins(self):
        self.level += -1
        if self.level == 0: self.level = 1

    def infinite_loop(self):
        while self.loop:
            self.create_fond()

            # Boutons
            self.reset_button.display_button(self.fond)
            self.start_button.display_button(self.fond)
            self.quit_button.display_button(self.fond)
            self.moins_button.display_button(self.fond)
            self.plus_button.display_button(self.fond)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_button.update_button(self.fond, action=reset)
                    self.start_button.update_button(self.fond, action=start)
                    self.quit_button.update_button(self.fond, action=gamequit)
                    self.moins_button.update_button(self.fond, action=self.moins)
                    self.plus_button.update_button(self.fond, action=self.plus)

            self.update_textes()
            for text in self.textes:
                self.display_text(text[0], text[1], text[2],
                                        text[3], text[4])

            # Ajout du fond dans la fenêtre
            self.screen.blit(self.fond, (0, 0))
            # Actualisation de l'affichage
            pygame.display.update()
            # 10 fps
            clock.tick(10)


def reset():
    print("reset")

def start():
    print("start")

def gamequit():
    print("Quit")
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    game = Game()
    game.infinite_loop()