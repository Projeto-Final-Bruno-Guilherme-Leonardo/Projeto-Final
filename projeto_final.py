"""
Jogo Jetpack
Autores: Bruno Conte, Guilherme Aranha, Leonardo Alvarez
"""

import pygame
import sys
import random

surf_altura = 500
surf_largura = 700

pygame.init() # inicia o pygame

surf = pygame.display.set_mode([surf_largura, surf_altura]) # crição da superfície para o jogo (local para desenhar) # entre parenteses o tamanho da tela

coisa_imagens = []

v = 10

try:
    imagem_jetpack = pygame.image.load('imagens/jetpack.png').convert_alpha()
    imagem_jetpack = pygame.transform.scale(imagem_jetpack, (100, 100))
    
    coisa_imagens.append(pygame.image.load('imagens/pedra.png').convert_alpha())
    coisa_imagens[-1] = pygame.transform.scale(coisa_imagens[-1], (50, 50))
    
    coisa_imagens.append(pygame.image.load('imagens/laser.png').convert_alpha())
    coisa_imagens[-1] = pygame.transform.scale(coisa_imagens[-1], (100, 100))
    
except pygame.error:
    print('Erro ao tentar ler uma imagem')
    sys.exit()
    

class Jetpack(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = imagem_jetpack
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 100
        self.speed = 0
        self.a = 0  #aceleracao
        
    def update(self):
        self.speed += self.a
        self.rect.y += 1 * self.speed
        if self.rect.top + (1 * self.speed) < 0:
            self.rect.top = 0
            self.speed = 0
        if self.rect.bottom + (1 * self.speed) > surf_altura:
            self.rect.bottom = surf_altura
            self.speed = 0
            
class Coisa(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = coisa_imagens[random.randint(0, len(coisa_imagens) -1)]
        self.rect = self.image.get_rect()
        self.rect.left = surf_largura
        self.rect.y = random.randint(0, surf_altura - self.rect.height)
        
    def update(self):
        self.rect.x -= v
        if self.rect.right < 0:
            self.kill()
        
        
    


jetpack = Jetpack()

sprites = pygame.sprite.Group()
sprites.add(jetpack)

def main():
    
    clock = pygame.time.Clock()
    FPS = 30
    
    timer = 0

    # Game Loop
    while True:
        clock.tick(FPS)
        timer += 1
        
        if timer == 100:
            timer = 0
            coisa = Coisa()
            sprites.add(coisa)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # terminado a aplicação pygame
                sys.exit() # sai pela rotima do sistema
                
            if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_SPACE:
                    jetpack.a = -1
        # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_SPACE:
                    jetpack.a = 1
                    
        sprites.update()
        
        surf.fill((255, 255, 255)) # preenche a tela
        #cores variam de 0 a 255 > 0 = preto
        sprites.draw(surf)

        pygame.display.flip() # faz a atualizacao da tela



main()







