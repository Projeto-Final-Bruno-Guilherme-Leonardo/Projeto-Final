"""
Jogo Jetpack
Autores: Bruno Conte, Guilherme Aranha, Leonardo Alvarez
"""

import pygame
import sys
import random

surf_altura = 600
surf_largura = int(surf_altura * 1.5)

a_cima = -3
a_baixo = 2.25

pygame.init() # inicia o pygame

surf = pygame.display.set_mode([surf_largura, surf_altura]) # crição da superfície para o jogo (local para desenhar) # entre parenteses o tamanho da tela

coisa_imagens = []

game = 0    #o jogo começa desligado, no menu

v_inicial = 10
v = v_inicial  #velocida dos obstaculos

def proporcao(a, b):
    return (int(a * surf_altura / 100), int(b * surf_altura / 100))

try:
    imagem_jetpack = pygame.image.load('imagens/jetpack.png').convert_alpha()
    imagem_jetpack = pygame.transform.scale(imagem_jetpack, proporcao(10, 10))
    
    coisa_imagens.append(pygame.image.load('imagens/pedra.png').convert_alpha())
    coisa_imagens[-1] = pygame.transform.scale(coisa_imagens[-1], proporcao(10, 10))
    
    coisa_imagens.append(pygame.image.load('imagens/laser.png').convert_alpha())
    coisa_imagens[-1] = pygame.transform.scale(coisa_imagens[-1], proporcao(20, 20))
    
except pygame.error:
    print('Erro ao tentar ler uma imagem')
    sys.exit()
    

class Jetpack(pygame.sprite.Sprite):
    def __init__(self, grupo):
        super().__init__(grupo)
        
        self.image = imagem_jetpack
        self.rect = self.image.get_rect()
        self.rect.left = 100
        self.rect.bottom = surf_altura
        self.speed = 0  #velocidade vertical da jetpack
        self.a = 1  #aceleracao
        
    def update(self):
        self.speed += self.a
        self.rect.y += self.speed
        if self.rect.top + (1 * self.speed) < 0:
            self.rect.top = 0
            self.speed = 0
        if self.rect.bottom + (1 * self.speed) > surf_altura:
            self.rect.bottom = surf_altura
            self.speed = 0
    
    def reset(self):
        self.rect.left = 100
        self.rect.bottom = surf_altura
        self.speed = 0  #velocidade vertical da jetpack
        self.a = 1  #aceleracao
        
            
class Coisa(pygame.sprite.Sprite):
    def __init__(self, grupo):
        super().__init__(grupo)
        
        self.image = coisa_imagens[random.randint(0, len(coisa_imagens) -1)]
        self.rect = self.image.get_rect()
        self.rect.left = surf_largura
        self.rect.y = random.randint(0, surf_altura - self.rect.height)
        
    def update(self):
        self.rect.x -= v
        if self.rect.right < 0:
            self.kill()
        
        


sprites = pygame.sprite.Group()
coisas = pygame.sprite.Group()

jetpack = Jetpack(sprites)


def main():
    global game
    global v
    
    clock = pygame.time.Clock()
    FPS = 30
    
    timer = 0

    # Game Loop
    while True:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   #fecha o pygame
                sys.exit()      #fecha o sistema
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jetpack.a = a_cima
                if event.key == pygame.K_RETURN and game == 0:
                    game = 1
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    jetpack.a = a_baixo
        
        if game:    #se o jogo estiver ligado:  
            timer += 1
            if timer == 30:
                timer = 0
                coisa = Coisa(sprites)
                coisas.add(coisa)
                
            v += 0.01   #almenta a velocidade dos obstaculos constantemente
                
            surf.fill((255, 255, 255)) # preenche a tela
            #cores variam de 0 a 255 > 0 = preto
            sprites.draw(surf)
            
            sprites.update()
                
            if pygame.sprite.spritecollide(jetpack, coisas, 0):
                game = 0
                v = v_inicial
                for i in coisas:
                    i.kill()
                jetpack.reset()
                surf.fill((55, 55, 55)) # preenche a tela
            
        else:   #se o jogo estiver desligado, no menu
            
            surf.fill((55, 55, 55)) # preenche a tela

        
        pygame.display.flip() # faz a atualizacao da tela


main()

print('aaaaa')











