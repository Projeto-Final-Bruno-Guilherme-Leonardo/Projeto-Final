"""
Jogo Jetpack
Autores: Bruno Conte, Guilherme Aranha, Leonardo Alvarez
"""

import pygame
import sys

CINZA = (127, 127, 127)

surf_altura = 500
surf_largura = 700

pygame.init() # inicia o pygame

surf = pygame.display.set_mode([surf_largura, surf_altura]) # crição da superfície para o jogo (local para desenhar) # entre parenteses o tamanho da tela

try:
    imagem_jetpack = pygame.image.load('imagens/jetpack.png').convert_alpha()
    imagem_jetpack = pygame.transform.scale(imagem_jetpack, (100, 100))
except pygame.error:
    print('Erro ao tentar ler imagem: jetpack.png')
    sys.exit()
    

class Jetpack(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = imagem_jetpack
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 100
        self.speed = 0
        self.a = 0
        
    def update(self):
        self.speed += self.a
        self.rect.y += 1 * self.speed
        if self.rect.top + (1 * self.speed) < 0:
            self.rect.top = 0
            self.speed = 0
        if self.rect.bottom + (1 * self.speed) > surf_altura:
            self.rect.bottom = surf_altura
            self.speed = 0
        
    


jetpack = Jetpack()

sprites = pygame.sprite.Group()
sprites.add(jetpack)

def main():
    """Rotina principal do jogo"""
    
    clock = pygame.time.Clock()
    FPS = 30

    # Game Loop
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # terminado a aplicação pygame
                sys.exit() # sai pela rotima do sistema
                
            if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_SPACE:
                    jetpack.a = -1
                    print('A')
        # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_SPACE:
                    jetpack.a = 1
                    print('B')
                    
        sprites.update()
        
        surf.fill(CINZA) # preenche a tela
        #cores variam de 0 a 255 > 0 = preto
        sprites.draw(surf)

        pygame.display.flip() # faz a atualizacao da tela

if __name__ == "__main__":
    main()







