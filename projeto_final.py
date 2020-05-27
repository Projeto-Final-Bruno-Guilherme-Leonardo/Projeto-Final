"""
Jogo Jetpack
Autores: Bruno Conte, Guilherme Aranha, Leonardo Alvarez
"""

import pygame
import sys
import os

CINZA = (127, 127, 127)

def main():
    """Rotina principal do jogo"""

    pygame.init() # inicia o pygame

    surf = pygame.display.set_mode([400, 400]) # crição da superfície para o jogo (local para desenhar) # entre parenteses o tamanho da tela

    arquivo = os.path.join('imagens', 'personagem.png') # pega a imagem da pasta

    try:
        imagem = pygame.image.load(arquivo)
    except pygame.error:
        print('Erro ao tentar ler imagem: imagem.png')
        sys.exit()

    posicao = 0

    clock = pygame.time.Clock() # objeto para controle das atualizações de imagens

    # Game Loop
    while True:
        delta_time = clock.tick(60) # garante um fps máximo de 60Hz

        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit() # terminado a aplicação pygame
                sys.exit() # sai pela rotima do sistema
        
        surf.fill(CINZA) # preenche a tela
        #cores variam de 0 a 255 > 0 = preto

        posicao += 0.2 * delta_time

        surf.blit(imagem, [posicao, 0]) # eixos x e y dentro dos []

        pygame.draw.circle(surf, [0, 0, 255], [200,200], 50) # desenha o circulo

        pygame.display.flip() # faz a atualizacao da tela

if __name__ == "__main__":
    main()