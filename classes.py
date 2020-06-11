#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jogo Jetpack
Autores: Bruno Conte, Guilherme Aranha, Leonardo Alvarez
"""

import pygame
import random

from config import surf_largura, proporcao, v
from load_imagens import imagens

class Cenario(pygame.sprite.Sprite):
    '''Sprites que são usadas apenas para o cenario, elas nao interagem com o player'''
    def __init__(self, grupo, imagem, paralaxe = 0):
        super().__init__(grupo)
        
        self.image = imagem
        self.rect = self.image.get_rect()
        self.paralaxe = paralaxe
    
    def update(self):       # Anda o cenário para a esquerda
        self.rect.x -= int(proporcao(v)) - (self.paralaxe * (2/3) * int(proporcao(v)))  # Se o cenario tiver paralaxe, ele anda mais devagar que o resto dos cenarios
        if self.rect.centerx < 0:       # Os cenários apresentam um fundo sem fim, sempre andando para a esquerda
            self.rect.centerx = surf_largura
            

class Jetpack(pygame.sprite.Sprite):
    '''Sprite do player, move-se verticalmente para desviar dos obstaculos'''
    def __init__(self, grupo):
        super().__init__(grupo)
        
        self.image = imagens['jetpack']
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = proporcao(10)
        self.rect.bottom = proporcao(100, 'borda')
        self.speed = 0                                      # Velocidade vertical do player
        self.a = 0                                          # Aceleração vertical do player
        
    def update(self):
        self.speed += self.a
        self.rect.y += proporcao(self.speed)
        if self.rect.top + (1 * self.speed) < proporcao(0, 'borda'):        # Não permite que o player sair para cima da tela
            self.rect.top = proporcao(0, 'borda')
            self.speed = 0
        if self.rect.bottom + (1 * self.speed) > proporcao(100, 'borda'):   # Não permite que o player sair para baixo da tela
            self.rect.bottom = proporcao(100, 'borda')
            self.speed = 0
    
    def reset(self):                                                        # Reseta o player para recomeçar o jogo
        self.rect.bottom = proporcao(100, 'borda')
        self.speed = 0  # Velocidade vertical do player
        self.a = 0  # Aceleração vertical do player
        
            
class Coisa(pygame.sprite.Sprite):
    '''Sprite dos obstaculos, o player deve desviar delas enquanto elas passam da direita para a esquerda'''
    def __init__(self, grupo):
        super().__init__(grupo)
        
        preso = random.sample([0,0,0,0,0,0,0,0,1,2], k=1)[0]            # Randomiza a chance de ser um obstáculo no chão, no teto ou voando
        
        if preso == 0:      # Obstáculos voando tem uma imagem em qualquer orientação
            self.image = pygame.transform.rotate(imagens['coisas'][random.randint(0, len(imagens['coisas']) -1)], random.randint(0,359))
        elif preso == 1:    # Obstáculos no chão ficam perpendiculares ao chão
            self.image = imagens['coisas'][random.randint(0, len(imagens['coisas']) -1)]
        else:               # Obstáculos no teto ficam perpendiculares ao teto
            self.image = pygame.transform.rotate(imagens['coisas'][random.randint(0, len(imagens['coisas']) -1)], 180)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = surf_largura
        if preso == 2:      # Obstáculos no chão são posicionados no chão
            self.rect.top = proporcao(0, 'borda')
        elif preso == 1:    # Obstáculos no teto são posicionados no teto
            self.rect.bottom = proporcao(100, 'borda')
        else:               # Obstáculos voando tem uma posição aleatória
            self.rect.y = random.randint(proporcao(0, 'borda'), proporcao(100, 'borda') - self.rect.height)
        
    def update(self):       # Anda o obstáculo para a esquerda junto do fundo da tela do jogo
        self.rect.x -= int(proporcao(v))
        if self.rect.right < 0:
            self.kill()