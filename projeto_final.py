"""
Jogo Jetpack
Autores: Bruno Conte, Guilherme Aranha, Leonardo Alvarez
"""

import pygame
import sys
import random

pygame.init() # inicia o pygame

font = pygame.font.SysFont(None, 48)

surf_altura = 900
surf_largura = int(surf_altura * 1.5)

def proporcao(a, b = 0):
    if b == 0:
        return a * surf_altura / 100
    elif b == 'borda':
        return (a * surf_altura * 0.8 / 100) + (surf_altura / 10)
    else:
        return (int(a * surf_altura * 0.8 / 100), int(b * surf_altura * 0.8 / 100))

a_cima = -0.3
a_baixo = 0.25

surf = pygame.display.set_mode([surf_largura, surf_altura]) # crição da superfície para o jogo (local para desenhar) # entre parenteses o tamanho da tela

coisa_imagens = []

game = 0    #o jogo começa desligado, no menu
corrido = 0

v_inicial = 2
v = v_inicial  #velocida dos obstaculos

try:
    imagem_chao = pygame.image.load('imagens/chao.png').convert_alpha()
    imagem_chao = pygame.transform.scale(imagem_chao, proporcao(188, 40))
    imagem_teto = pygame.transform.rotate(imagem_chao, 180)
    
    imagem_fundo = pygame.image.load('imagens/fundo.png').convert_alpha()
    imagem_fundo = pygame.transform.scale(imagem_fundo, proporcao(240, 80))
    
    imagem_jetpack = pygame.image.load('imagens/jetpack.png').convert_alpha()
    imagem_jetpack = pygame.transform.scale(imagem_jetpack, proporcao(10, 10))
    
    coisa_imagens.append(pygame.image.load('imagens/pedra.png').convert_alpha())
    coisa_imagens[-1] = pygame.transform.scale(coisa_imagens[-1], proporcao(20, 20))
    
    coisa_imagens.append(pygame.image.load('imagens/laser.png').convert_alpha())
    coisa_imagens[-1] = pygame.transform.scale(coisa_imagens[-1], proporcao(30, 30))
    
except pygame.error:
    print('Erro ao tentar ler uma imagem')
    sys.exit()

class Cenario(pygame.sprite.Sprite):
    def __init__(self, grupo, imagem):
        super().__init__(grupo)
        
        self.image = imagem
        self.rect = self.image.get_rect()

class Jetpack(pygame.sprite.Sprite):
    def __init__(self, grupo):
        super().__init__(grupo)
        
        self.image = imagem_jetpack
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = proporcao(10)
        self.rect.bottom = proporcao(100, 'borda')
        self.speed = 0  #velocidade vertical da jetpack
        self.a = 0  #aceleracao
        
    def update(self):
        self.speed += self.a
        self.rect.y += proporcao(self.speed)
        if self.rect.top + (1 * self.speed) < proporcao(0, 'borda'):
            self.rect.top = proporcao(0, 'borda')
            self.speed = 0
        if self.rect.bottom + (1 * self.speed) > proporcao(100, 'borda'):
            self.rect.bottom = proporcao(100, 'borda')
            self.speed = 0
    
    def reset(self):
        self.rect.bottom = proporcao(100, 'borda')
        self.speed = 0  #velocidade vertical da jetpack
        self.a = 0  #aceleracao
        
            
class Coisa(pygame.sprite.Sprite):
    def __init__(self, grupo):
        super().__init__(grupo)
        
        self.image = pygame.transform.rotate(coisa_imagens[random.randint(0, len(coisa_imagens) -1)], random.randint(0,359))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = surf_largura
        if random.randint(0,4) == 0:
            print('aaa')
            if random.randint(0,1) == 0:
                self.rect.top = proporcao(0, 'borda')
            else:
                self.rect.bottom = proporcao(100, 'borda')
        else:
            self.rect.y = random.randint(proporcao(0, 'borda'), proporcao(100, 'borda') - self.rect.height)
        
    def update(self):
        self.rect.x -= proporcao(v)
        if self.rect.right < 0:
            self.kill()
        
        


sprites = pygame.sprite.Group()
coisas = pygame.sprite.Group()
paredes = pygame.sprite.Group()
fundos = pygame.sprite.Group()

jetpack = Jetpack(sprites)

teto = Cenario(paredes, imagem_teto)
teto.rect.left = proporcao(0)
teto.rect.bottom = proporcao(0, 'borda')
chao = Cenario(paredes, imagem_chao)
chao.rect.left = proporcao(0)
chao.rect.top = proporcao(100, 'borda')
fundo = Cenario(fundos, imagem_fundo)

def main():
    global game
    global v
    global corrido
    
    clock = pygame.time.Clock()
    FPS = 30
    
    timer = 0
    t_obstaculo = 50

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
            if timer == t_obstaculo: #Timer para criar obstaculos
                timer = 0
                t_obstaculo = random.randint(10, 50)
                coisa = Coisa(sprites)
                coisas.add(coisa)
                
            v += 0.001   #aumenta a velocidade dos obstaculos constantemente
            corrido += v * 0.1
            corredor = font.render(str(int(corrido)) + ' metros', True, (200, 200, 0))     
                
            surf.fill((255, 255, 255)) # preenche a tela
            #cores variam de 0 a 255 > 0 = preto
            sprites.draw(surf)
            paredes.draw(surf)
            surf.blit(corredor, (10, 10))
            
            sprites.update()
                
            if pygame.sprite.spritecollide(jetpack, coisas, False, pygame.sprite.collide_mask):
                game = 0
                v = v_inicial
                t_obstaculo = 50
                corrido = 0
                for i in coisas:
                    i.kill()
                jetpack.reset()
                surf.fill((55, 55, 55)) # preenche a tela
            
        else:   #se o jogo estiver desligado, no menu
            
            surf.fill((55, 55, 55)) # preenche a tela

        
        pygame.display.flip() # faz a atualizacao da tela

main()

print('aaaaa')











