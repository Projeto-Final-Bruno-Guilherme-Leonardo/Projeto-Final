"""
Jogo Jetpack
Autores: Bruno Conte, Guilherme Aranha, Leonardo Alvarez
"""

import pygame    # Importa todos os módulos que serão usados do pygame
import sys
import random

pygame.init()    # Inicia o pygame

font = pygame.font.SysFont(None, 48)

surf_altura = 900   #<-----------| Altura da tela, recomendado: 900 |
surf_largura = int(surf_altura * 1.5)

def proporcao(a, b = 0):    # Função que mantém a proporção entre as sprites e o tamanho da tela
    if b == 0:
        return a * surf_altura / 100
    elif b == 'borda':
        return (a * surf_altura * 0.8 / 100) + (surf_altura / 10)
    else:
        return (int(a * surf_altura * 0.8 / 100), int(b * surf_altura * 0.8 / 100))

a_cima = -0.15  # Aceleração vertical quando aperta ESPAÇO
a_baixo = 0.12  # Aceleração vertical quando solta o ESPAÇO

surf = pygame.display.set_mode([surf_largura, surf_altura]) # Cria a janela do jogo

coisa_imagens = []

game = 0    # O jogo começa desligado, ou seja, no MENU
corrido = 0     # O caminho corrido começa em 0

v_inicial = 1
v = v_inicial  # Velocidade dos obstáculos

try:
    imagem_menu = pygame.image.load('imagens/menu.png').convert()
    imagem_menu = pygame.transform.scale(imagem_menu, (surf_largura, surf_altura))
    
    imagem_chao = pygame.image.load('imagens/chao.png').convert()
    imagem_chao = pygame.transform.scale(imagem_chao, proporcao(375, 30))
    imagem_teto = pygame.transform.rotate(imagem_chao, 180)
    
    imagem_fundo = pygame.image.load('imagens/fundo.png').convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, proporcao(375, 125))
    
    imagem_jetpack = pygame.image.load('imagens/jetpack.png').convert_alpha()
    imagem_jetpack = pygame.transform.scale(imagem_jetpack, proporcao(10, 10))
    
    coisa_imagens.append(pygame.image.load('imagens/pedra.png').convert_alpha())
    coisa_imagens[-1] = pygame.transform.scale(coisa_imagens[-1], proporcao(20, 20))
    
    coisa_imagens.append(pygame.image.load('imagens/laser.png').convert_alpha())
    coisa_imagens[-1] = pygame.transform.scale(coisa_imagens[-1], proporcao(30, 30))
    
    coisa_imagens.append(pygame.image.load('imagens/spike.png').convert_alpha())
    coisa_imagens[-1] = pygame.transform.scale(coisa_imagens[-1], proporcao(10, 10))
    
except pygame.error:
    print('Erro ao tentar ler uma imagem')
    sys.exit()

class Cenario(pygame.sprite.Sprite):    # Sprite que serve como cenário
    def __init__(self, grupo, imagem):
        super().__init__(grupo)
        
        self.image = imagem
        self.rect = self.image.get_rect()
    
    def update(self):
        self.rect.x -= int(proporcao(v))
        if self.rect.centerx < 0:
            self.rect.centerx = surf_largura
            

class Jetpack(pygame.sprite.Sprite):    # Sprite que mostra o player
    def __init__(self, grupo):
        super().__init__(grupo)
        
        self.image = imagem_jetpack
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = proporcao(10)
        self.rect.bottom = proporcao(100, 'borda')
        self.speed = 0  # Velocidade vertical do player
        self.a = 0  # Aceleração vertical do player
        
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
        self.speed = 0  # Velocidade vertical do player
        self.a = 0  # Aceleração vertical do player
        
            
class Coisa(pygame.sprite.Sprite):      # Sprite que serve como obstáculo
    def __init__(self, grupo):
        super().__init__(grupo)
        
        self.image = pygame.transform.rotate(coisa_imagens[random.randint(0, len(coisa_imagens) -1)], random.randint(0,359))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = surf_largura
        if random.randint(0,4) == 0:
            if random.randint(0,1) == 0:
                self.rect.top = proporcao(0, 'borda')
            else:
                self.rect.bottom = proporcao(100, 'borda')
        else:
            self.rect.y = random.randint(proporcao(0, 'borda'), proporcao(100, 'borda') - self.rect.height)
        
    def update(self):
        self.rect.x -= int(proporcao(v))
        if self.rect.right < 0:
            self.kill()
        
        


sprites = pygame.sprite.Group()     # Cria os grupos de sprites
coisas = pygame.sprite.Group()
paredes = pygame.sprite.Group()
fundos = pygame.sprite.Group()

jetpack = Jetpack(sprites)      # Cria a sprite do player

teto = Cenario(paredes, imagem_teto)    # Cria as sprites do cenário
teto.rect.left = proporcao(0)
teto.rect.bottom = proporcao(0, 'borda')
chao = Cenario(paredes, imagem_chao)
chao.rect.left = proporcao(0)
chao.rect.top = proporcao(100, 'borda')
fundo = Cenario(fundos, imagem_fundo)
fundo.rect.left = proporcao(0)
fundo.rect.centery = proporcao(50, 'borda')




clock = pygame.time.Clock()
FPS = 60

timer = 0
t_obstaculo = 100

while True:     # Loop principal da interface
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()   # Fecha o pygame
            sys.exit()      # Fecha o sistema
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jetpack.a = a_cima
            if event.key == pygame.K_RETURN and game == 0:
                game = 1
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                jetpack.a = a_baixo
    
    if game:    # Se o jogo estiver ligado:  
        timer += 1
        if timer == t_obstaculo: # Timer para criar obstáculos constantemente
            timer = 0
            t_obstaculo = random.randint(20, 100)
            coisa = Coisa(sprites)
            coisas.add(coisa)
            
        v += 0.001   # Aumenta a velocidade dos obstáculos constantemente
        corrido += v * 0.05
        corredor = font.render(str(int(corrido)) + ' metros', True, (200, 200, 0))     
            
        surf.fill((255, 255, 255)) # Preenche a tela
        # Cores variam de 0 a 255 > 0 = preto
        fundos.draw(surf)
        sprites.draw(surf)
        paredes.draw(surf)
        surf.blit(corredor, (10, 10))
        
        sprites.update()
        fundos.update()
        paredes.update()
        
#        for i in sprites:
#            print('sprite: ' + str(i.rect.left))
#        for i in fundos:
#            print('fundos: ' + str(i.rect.left))
#        print('v: ' + str(v))
            
            
        if pygame.sprite.spritecollide(jetpack, coisas, False, pygame.sprite.collide_mask):
            game = 0
            v = v_inicial
            t_obstaculo = 50
            corrido = 0
            for i in coisas:
                i.kill()
            for i in paredes:
                i.rect.left = 0
            jetpack.reset()
            surf.fill((55, 55, 55)) # Preenche a tela
        
    else:   # Se o jogo estiver desligado, ou seja, no MENU
        
        surf.blit(imagem_menu, (0, 0)) # Apresenta o MENU

    
    pygame.display.flip() # Faz a atualização da tela









