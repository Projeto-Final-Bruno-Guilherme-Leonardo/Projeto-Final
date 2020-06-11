#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jogo Jetpack
Autores: Bruno Conte, Guilherme Aranha, Leonardo Alvarez
"""

import pygame    # Importa todos os módulos que serão usados
import sys
import random
import shelve

pygame.init()    # Inicia o pygame

from config import surf_altura, surf_largura, proporcao, a_cima, a_baixo, surf, font, fontScoreboard, fontScoreboard2, fontAjuda, verde, game, corrido, v_inicial, v, ajudax_inicial, ajudax, score, clock, FPS, timer, t_obstaculo_inicial, t_obstaculo             #importa as configurações
from load_imagens import imagens                    #importa as imagens
from classes import Cenario, Jetpack, Coisa         #importa as classes

pygame.mixer.music.load('mixer/battleship.ogg')     # Load a música tema
pygame.mixer.music.set_volume(0.02)                 # Abaixa o volume da música tema
pygame.mixer.music.play(-1)                         # Começa a tocar a música ciclicamente

som_batida = pygame.mixer.Sound('mixer/batida.ogg') # Load som da batida

sprites = pygame.sprite.Group()         # Cria os grupos de sprites (player + obstáculos)
coisas = pygame.sprite.Group()          # (obstáculos)
paredes = pygame.sprite.Group()         # (cenário do chão e do teto)
fundos = pygame.sprite.Group()          # (cenário do fundo)

jetpack = Jetpack(sprites)              # Cria a sprite do player

teto = Cenario(paredes, imagens['teto'])    # Cria as sprites do cenário
teto.rect.left = proporcao(0)
teto.rect.bottom = proporcao(0, 'borda')
chao = Cenario(paredes, imagens['chao'])
chao.rect.left = proporcao(0)
chao.rect.top = proporcao(100, 'borda')
fundo = Cenario(fundos, imagens['fundo'], paralaxe = True)
fundo.rect.left = proporcao(0)
fundo.rect.centery = proporcao(50, 'borda')

while True:     # Loop principal da interface
    clock.tick(FPS)     # Garante o FPS do jogo predeterminado
    
    for event in pygame.event.get():    # Detecta os eventos do usuário
        if event.type == pygame.QUIT:
            pygame.quit()               # Fecha o pygame
            sys.exit()                  # Fecha o sistema
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:                     # [ESPAÇO] -> acelera para cima 
                jetpack.a = a_cima
            if event.key == pygame.K_RETURN and game == 0:      # [RETURN] -> inicia o jogo a partir do MENU
                game = 1
            if event.key == pygame.K_e and game == 0:           # [E] -> reseta os scores da scoreboard
                score = []
                arquivo_score = shelve.open('arquivo_score')
                arquivo_score['score'] = score
                arquivo_score.close()
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:                     # Soltar [ESPAÇO] -> acelera para baixo
                jetpack.a = a_baixo
    
    if game:                        # Se o jogo estiver ligado:  
        timer += 1
        if timer >= t_obstaculo:    # Timer para criar obstáculos
            timer = 0
            t_obstaculo = random.randint(10, 40 + int(400/((v-0.9)*100)))   # Cria aleatoriamente o tempo ate o próximo obstáculo aparecer, esse valor diminui conforme a velocidade aumenta
            coisa = Coisa(sprites)                                          # Cria a sprite do obstáculo
            coisas.add(coisa)
            
        v += 0.0001                                                             # Aumenta a velocidade dos obstáculos constantemente
        corrido += v * 0.05
        corredor = font.render(str(int(corrido)) + ' metros', True, verde)      # Atualiza o contador da distância percorrida
            
        surf.fill((255, 255, 255))  # Se por algum motivo a tela nao for inteira coberta pelo cenário, o fundo será preto
        
        fundos.draw(surf)           # Desenha a tela de fundo
        if ajudax > 0:              # Desenha a placa de ajuda se ela ainda não tiver saído da tela
            surf.blit(imagens['ajuda'], (ajudax - imagens['ajuda'].get_rect().size[0], (surf_altura/2) - (imagens['ajuda'].get_rect().size[1]/2)))
            textoAjuda = fontAjuda.render('Aperte [ESPAÇO] para voar', True, verde)
            surf.blit(textoAjuda, (ajudax - (imagens['ajuda'].get_rect().size[0]/2) - (textoAjuda.get_rect().size[0]/2), (surf_altura/2) - (textoAjuda.get_rect().size[1]/2)))
            ajudax -= proporcao(v) * (1/2)
        surf.blit(imagens['corredor'], ((surf_largura/2) - (imagens['corredor'].get_rect().size[0]/2), proporcao(10)))      # Desenha o mostrador dos metros percorridos
        surf.blit(corredor, ((surf_largura/2) - (corredor.get_rect().size[0]/2), (imagens['corredor'].get_rect().size[1]/2) - (corredor.get_rect().size[1]/2) + proporcao(10.4)))   #desenha o texto no mostrador
        sprites.draw(surf)          # Desenha o player e os obstáculos
        paredes.draw(surf)          # Desenha o chão e o teto
        
        sprites.update()            # Atualiza o player e os obstáculos
        fundos.update()             # Atualiza o fundo
        paredes.update()            # Atualiza o chão e o teto
            
        if pygame.sprite.spritecollide(jetpack, coisas, False, pygame.sprite.collide_mask):     # Se o player acertar um obstáculo, o jogo acaba e fica pronto para a próxima partida
            som_batida.play()                               # Toca o som da batida do player em um obstáculo
            game = 0                                        # Sai do jogo para o MENU
            v = v_inicial                                   # Reseta a velocidade dos obstáculos
            t_obstaculo = t_obstaculo_inicial               # Reseta o timer para criar obstáculos constantemente
            ajudax = ajudax_inicial                         # Reseta a posição da placa de ajuda
            for i in coisas:                                # Apaga os obstáculos
                i.kill()
            for i in paredes:                               # Reseta a posição do cenário
                i.rect.left = 0
            jetpack.reset()                                 # Reseta a posição, velocidade e aceleração do player
            
            score += [corrido]                              # Adiciona o score corrido a lista de scores no MENU
            score.sort(reverse = 1)                         # Ordena os scores
            score = score[:5]                               # Apaga todos os scores depois da quinta posição da tabela de scores
            arquivo_score = shelve.open('arquivo_score')    # Abre o arquivo que guarda os scores
            arquivo_score['score'] = score                  # Atualiza o arquivo dos scores
            arquivo_score.close()                           # Fecha o arquivo dos scores
            
            corrido = 0                                     # Reseta o marcador de metros percorridos
            
    else:                       # Se o jogo estiver desligado, ou seja, no MENU:
        surf.blit(imagens['menu'], (0, 0))      # Apresenta o MENU
        assert len(score) <= 5, 'Há mais de 5 scores na lista de scores: ' + str(score)     # Garante que não tem mais que 5 scores para serem mostrados na scoreboard
        if len(score) == 0:                 # Se não tiver nenhum score registrado, a scoreboard aparece fechada
            surf.blit(imagens['scoreboardoff'], ((surf_largura/2) - (imagens['scoreboardoff'].get_rect().size[0]/2), (surf_altura/2) - (imagens['scoreboardoff'].get_rect().size[1]/2) + proporcao(20))) 
        else:                               # Se tiverem scores registrados, a scoreboard aparece aberta e apresenta os scores
            surf.blit(imagens['scoreboardon'], ((surf_largura/2) - (imagens['scoreboardoff'].get_rect().size[0]/2), (surf_altura/2) - (imagens['scoreboardoff'].get_rect().size[1]/2) + proporcao(20))) 
            textoScoreboard = fontScoreboard.render('- Scoreboard -', True, verde)
            surf.blit(textoScoreboard, ((surf_largura/2) - (textoScoreboard.get_rect().size[0]/2), (surf_altura/2) - (textoScoreboard.get_rect().size[1]/2) + proporcao(4.5)))
            textoScoreboard2 = fontScoreboard2.render('Aperte [E] para apagar os scores', True, verde)
            surf.blit(textoScoreboard2, ((surf_largura/2) - (textoScoreboard2.get_rect().size[0]/2), (surf_altura/2) - (textoScoreboard2.get_rect().size[1]/2) + proporcao(40)))
            
            n = 0
            for i in score:     # Mostra cada um dos 5 primeiros scores
                if n == 0:
                    texto = font.render('> ' + str(int(i)) + ' metros <', True, verde)
                else:
                    texto = font.render(str(int(i)) + ' metros', True, verde)
                surf.blit(texto, ((surf_largura/2) - (texto.get_rect().size[0]/2), (surf_altura/2) - (texto.get_rect().size[1]/2) + proporcao(12) + (proporcao(6)*n)))
                n += 1
    
    pygame.display.flip()       # Atualiza a tela a cada repetição
