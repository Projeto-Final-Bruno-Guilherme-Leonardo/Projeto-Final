#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jogo Jetpack
Autores: Bruno Conte, Guilherme Aranha, Leonardo Alvarez
"""

import pygame
import sys

from config import surf_altura, surf_largura, proporcao

imagens = {'coisas': []}                            # Dicionário que guarda todas as imagens

coisas_info = [                                     # Informações sobre como fazer o load das imagens dos obstáculos
        ('pedra', 20),                              # (nome do arquivo, dimensão da imagem)
        ('spike', 10),
        ('barril vermelho', 15),
        ('barril verde', 15),
        ('caixa', 20),
        ('disco', 20),
        ('bloco', 25),
        ('cactus', 15),
        ('caixa 2', 20),
        ('gelo', 25),
        ('lapide', 10),
        ('placa', 20)
        ]

try:            # Load as imagens
    imagens['menu'] = pygame.image.load('imagens/menu.png').convert()
    imagens['menu'] = pygame.transform.scale(imagens['menu'], (surf_largura, surf_altura))
    
    imagens['scoreboardoff'] = pygame.image.load('imagens/scoreboardoff.png').convert_alpha()
    imagens['scoreboardoff'] = pygame.transform.scale(imagens['scoreboardoff'], proporcao(60, 60))
    
    imagens['scoreboardon'] = pygame.image.load('imagens/scoreboardon.png').convert_alpha()
    imagens['scoreboardon'] = pygame.transform.scale(imagens['scoreboardon'], proporcao(60, 60))
    
    imagens['corredor'] = pygame.image.load('imagens/corredor.png').convert_alpha()
    imagens['corredor'] = pygame.transform.scale(imagens['corredor'], proporcao(40, 40))
    
    imagens['ajuda'] = pygame.image.load('imagens/ajuda.png').convert_alpha()
    imagens['ajuda'] = pygame.transform.scale(imagens['ajuda'], proporcao(100, 100))
    
    imagens['chao'] = pygame.image.load('imagens/chao.png').convert()
    imagens['chao'] = pygame.transform.scale(imagens['chao'], proporcao(375, 30))
    imagens['teto'] = pygame.transform.rotate(imagens['chao'], 180)
    
    imagens['fundo'] = pygame.image.load('imagens/fundo.png').convert()
    imagens['fundo'] = pygame.transform.scale(imagens['fundo'], proporcao(375, 125))
    
    imagens['jetpack'] = pygame.image.load('imagens/jetpack.png').convert_alpha()
    imagens['jetpack'] = pygame.transform.scale(imagens['jetpack'], proporcao(10, 10))
    
    for nome, tamanho in coisas_info:       # Load as imagens dos obstáculos
        imagem = pygame.image.load('imagens/' + nome + '.png').convert_alpha()
        imagem = pygame.transform.scale(imagem, proporcao(tamanho, tamanho))
        imagens['coisas'].append(imagem)

except pygame.error:        # Caso algum load falhe, print ERRO
    print('Erro ao tentar ler uma imagem')
    sys.exit()