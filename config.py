#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jogo Jetpack
Autores: Bruno Conte, Guilherme Aranha, Leonardo Alvarez
"""

import pygame
import shelve

surf_altura = 800   #<-----------| Altura da tela, recomendado: 800 | (AJUSTE PARA O TAMANHO DA SUA TELA)
surf_largura = int(surf_altura * 1.5)   # Largura em função da altura da janela

def proporcao(a, b = 0):
    '''Função que mantém a proporção entre as sprites e o tamanho da tela'''
    if b == 0:
        return a * surf_altura / 100
    elif b == 'borda':
        return (a * surf_altura * 0.8 / 100) + (surf_altura / 10)
    else:
        return (int(a * surf_altura * 0.8 / 100), int(b * surf_altura * 0.8 / 100))

a_cima = -0.10  # Aceleração vertical quando aperta [ESPAÇO]
a_baixo = 0.08  # Aceleração vertical quando solta  [ESPAÇO]

surf = pygame.display.set_mode([surf_largura, surf_altura])     # Cria a janela do jogo

font = pygame.font.SysFont(None, int(proporcao(6)))             # Cria as fontes para os textos dentro do jogo
fontScoreboard = pygame.font.SysFont(None, int(proporcao(8)))
fontScoreboard2 = pygame.font.SysFont(None, int(proporcao(2)))
fontAjuda = pygame.font.SysFont(None, int(proporcao(5)))

verde = (0, 170, 8)     # Cor verde que vai ser usada no mostrador de metros corridos, na placa de ajuda e no scoreboard

game = 0        # O jogo começa desligado, ou seja, no MENU
corrido = 0     # O caminho corrido comeca em 0

v_inicial = 1   # Velocidade inicial dos obstáculos
v = v_inicial

ajudax_inicial = proporcao(150)     # Posição inicial da placa de ajuda
ajudax = ajudax_inicial

arquivo_score = shelve.open('arquivo_score')        # Abre o arquivo que guarda os scores
try:
    score = arquivo_score['score']                  # Caso exista um arquivo
except:
    score = []
    print('asdfasdfasdf')
arquivo_score.close()

clock = pygame.time.Clock()     # Cria o FPS do jogo
FPS = 60

timer = 0   # Cria o timer para criar os obstáculos constantemente
t_obstaculo_inicial = 100   # Tempo até aparecer o primeiro obstáculo no jogo
t_obstaculo = t_obstaculo_inicial

