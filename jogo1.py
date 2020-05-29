#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 14:28:04 2020

@author: guilhermearanha
"""
import pygame
import random
import time

pygame.init()
pygame.key.set_repeat(0)
pygame.mixer.init()

WIDTH = 400
HEIGHT = 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Guerreiro Yo')

teclasDic = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'z': pygame.K_z, 'x': pygame.K_x, 'p': pygame.K_p, 'esc': 27}
teclas = {'up': 0, 'down': 0, 'left': 0, 'right': 0, 'z': 0, 'x': 0, 'p': 0, 'esc':0}

def updateTeclas():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            for k in teclasDic:
                if event.key == teclasDic[k]:
                    teclas[k] = 1
        if event.type == pygame.KEYUP:
            for k in teclasDic:
                if event.key == teclasDic[k]:
                    teclas[k] = 0
        if event.type == pygame.QUIT:
                pygame.quit()
                
                
            

x = 0
while 1:
    updateTeclas()
    if teclas['up'] == 1:
        x += 1
    if teclas['down'] == 1:
        x -= 1
    print(x)
    window.fill((225, 225, 225))
    pygame.display.update()
    
    time.sleep(0.01)
    






