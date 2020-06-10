"""
Jogo Jetpack
Autores: Bruno Conte, Guilherme Aranha, Leonardo Alvarez
"""

import pygame    #importa todos os modulos que serao usados
import sys
import random
import shelve

pygame.init()    #inicia o pygame


surf_altura = 1000   #<-----------| altura da tela, recomendado: 900 |
surf_largura = int(surf_altura * 1.5)

def proporcao(a, b = 0):    #funcao que mantem a proporcao entre as sprites e o tamanho da tela
    if b == 0:
        return a * surf_altura / 100
    elif b == 'borda':
        return (a * surf_altura * 0.8 / 100) + (surf_altura / 10)
    else:
        return (int(a * surf_altura * 0.8 / 100), int(b * surf_altura * 0.8 / 100))

a_cima = -0.10  #aceleracao vertical quando aperta ESPAÇO
a_baixo = 0.08  #aceleracao vertical quando solta

surf = pygame.display.set_mode([surf_largura, surf_altura])     #cria a janela

font = pygame.font.SysFont(None, int(proporcao(6)))             #cria a fonte para os textos
fontScoreboard = pygame.font.SysFont(None, int(proporcao(8)))
fontScoreboard2 = pygame.font.SysFont(None, int(proporcao(2)))
fontAjuda = pygame.font.SysFont(None, int(proporcao(5)))

verde = (0, 170, 8)

coisa_imagens = []

game = 0    #o jogo começa desligado, ou seja, no menu
corrido = 0     #o caminho corrido comeca no 0

v_inicial = 1
v = v_inicial  #velocida dos obstaculos

ajudax_inicial = proporcao(150)
ajudax = ajudax_inicial

arquivo_score = shelve.open('arquivo_score')
try:
    score = arquivo_score['score']
except:
    score = []
arquivo_score.close()

clock = pygame.time.Clock()     #cria o FPS do jogo
FPS = 60

timer = 0   #cria o timer para criar os obstaculos
t_obstaculo_inicial = 100   #tempo ate aparecer o primeiro obstaculo
t_obstaculo = t_obstaculo_inicial

pygame.mixer.music.load('mixer/battleship.ogg')     #load a musica tema
pygame.mixer.music.set_volume(0.2)                  #abaixa o volume
pygame.mixer.music.play(-1)                         #começa a tocar a musica ciclicamente

coisas_info = [                                     #informações sobre como fazer o load das imagens dos obstaculos
        ('pedra', 20),                              #(nome do arquivo, dimensao da imagem)
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

try:        #load as imagens 
    imagem_menu = pygame.image.load('imagens/menu.png').convert()
    imagem_menu = pygame.transform.scale(imagem_menu, (surf_largura, surf_altura))
    
    imagem_scoreboardoff = pygame.image.load('imagens/scoreboardoff.png').convert_alpha()
    imagem_scoreboardoff = pygame.transform.scale(imagem_scoreboardoff, proporcao(60, 60))
    
    imagem_scoreboardon = pygame.image.load('imagens/scoreboardon.png').convert_alpha()
    imagem_scoreboardon = pygame.transform.scale(imagem_scoreboardon, proporcao(60, 60))
    
    imagem_corredor = pygame.image.load('imagens/corredor.png').convert_alpha()
    imagem_corredor = pygame.transform.scale(imagem_corredor, proporcao(40, 40))
    
    imagem_ajuda = pygame.image.load('imagens/ajuda.png').convert_alpha()
    imagem_ajuda = pygame.transform.scale(imagem_ajuda, proporcao(100, 100))
    
    imagem_chao = pygame.image.load('imagens/chao.png').convert()
    imagem_chao = pygame.transform.scale(imagem_chao, proporcao(375, 30))
    imagem_teto = pygame.transform.rotate(imagem_chao, 180)
    
    imagem_fundo = pygame.image.load('imagens/fundo.png').convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, proporcao(375, 125))
    
    imagem_jetpack = pygame.image.load('imagens/jetpack.png').convert_alpha()
    imagem_jetpack = pygame.transform.scale(imagem_jetpack, proporcao(10, 10))
    
    for nome, tamanho in coisas_info:       #load as imagens dos obstaculos
        imagem = pygame.image.load('imagens/' + nome + '.png').convert_alpha()
        imagem = pygame.transform.scale(imagem, proporcao(tamanho, tamanho))
        coisa_imagens.append(imagem)

except pygame.error:        #caso algum load falhe, print erro
    print('Erro ao tentar ler uma imagem')
    sys.exit()

class Cenario(pygame.sprite.Sprite):
    '''Sprites que são usadas apenas para o cenario, elas nao interagem com o player'''
    def __init__(self, grupo, imagem, paralaxe = 0):
        super().__init__(grupo)
        
        self.image = imagem
        self.rect = self.image.get_rect()
        self.paralaxe = paralaxe
    
    def update(self):       #anda o cenario para a esquerda
        self.rect.x -= int(proporcao(v)) - (self.paralaxe * (2/3) * int(proporcao(v)))  #se o cenario tiver paralaxe, ele anda mais devagar que o resto dos cenarios
        if self.rect.centerx < 0:
            self.rect.centerx = surf_largura
            

class Jetpack(pygame.sprite.Sprite):
    '''Sprite do player'''
    def __init__(self, grupo):
        super().__init__(grupo)
        
        self.image = imagem_jetpack
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = proporcao(10)
        self.rect.bottom = proporcao(100, 'borda')
        self.speed = 0                                      #velocidade vertical da jetpack
        self.a = 0                                          #aceleracao vertical da jetpack
        
    def update(self):
        self.speed += self.a
        self.rect.y += proporcao(self.speed)
        if self.rect.top + (1 * self.speed) < proporcao(0, 'borda'):        #nao permite que o player sair para cima da tela
            self.rect.top = proporcao(0, 'borda')
            self.speed = 0
        if self.rect.bottom + (1 * self.speed) > proporcao(100, 'borda'):   #nao permite que o player sair para baixo da tela
            self.rect.bottom = proporcao(100, 'borda')
            self.speed = 0
    
    def reset(self):                                                        #reseta o player para recomeçar o jogo
        self.rect.bottom = proporcao(100, 'borda')
        self.speed = 0  #velocidade vertical da jetpack
        self.a = 0  #aceleracao
        
            
class Coisa(pygame.sprite.Sprite):
    '''Sprite dos obstaculos, o player deve desviar delas'''
    def __init__(self, grupo):
        super().__init__(grupo)
        
        preso = random.sample([0,0,0,0,0,0,0,0,1,2], k=1)[0]            #randomiza a chance de ser um obstaculo no chao, no teto ou voando
        
        if preso == 0:      #obstaculo voando tem uma imagem em qualquer orientação
            self.image = pygame.transform.rotate(coisa_imagens[random.randint(0, len(coisa_imagens) -1)], random.randint(0,359))
        elif preso == 1:    #obstaculo no chao estao retos para cima
            self.image = coisa_imagens[random.randint(0, len(coisa_imagens) -1)]
        else:               #obstaculo no teto estao de ponta cabeca
            self.image = pygame.transform.rotate(coisa_imagens[random.randint(0, len(coisa_imagens) -1)], 180)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = surf_largura
        if preso == 2:      #obstaculo no chao é posicionado no chao
            self.rect.top = proporcao(0, 'borda')
        elif preso == 1:    #obstaculo no teto é posicionado no teto
            self.rect.bottom = proporcao(100, 'borda')
        else:               #obstaculo voando tem uma posicao aleatoria
            self.rect.y = random.randint(proporcao(0, 'borda'), proporcao(100, 'borda') - self.rect.height)
        
    def update(self):       #anda o obstaculo para a esquerda
        self.rect.x -= int(proporcao(v))
        if self.rect.right < 0:
            self.kill()
        
        


sprites = pygame.sprite.Group()     #cria os grupos de sprites
coisas = pygame.sprite.Group()
paredes = pygame.sprite.Group()
fundos = pygame.sprite.Group()

jetpack = Jetpack(sprites)      #cria a sprite do player

teto = Cenario(paredes, imagem_teto)    #cria as spritse do cenario
teto.rect.left = proporcao(0)
teto.rect.bottom = proporcao(0, 'borda')
chao = Cenario(paredes, imagem_chao)
chao.rect.left = proporcao(0)
chao.rect.top = proporcao(100, 'borda')
fundo = Cenario(fundos, imagem_fundo, paralaxe = True)
fundo.rect.left = proporcao(0)
fundo.rect.centery = proporcao(50, 'borda')




while True:     #loop principal da interface
    clock.tick(FPS)     #garante o FPS predeterminado
    
    for event in pygame.event.get():    #detecta os eventos do usuario
        if event.type == pygame.QUIT:
            pygame.quit()               #fecha o pygame
            sys.exit()                   #fecha o sistema
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jetpack.a = a_cima                          #acelera para cima 
            if event.key == pygame.K_RETURN and game == 0:
                game = 1                                    #inicia o jogo a partir do menu
            if event.key == pygame.K_e and game == 0:
                score = []
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                jetpack.a = a_baixo                         #acelera para baixo
    
    if game:    #se o jogo estiver ligado:  
        timer += 1
        if timer >= t_obstaculo: #Timer para criar obstaculos
            timer = 0
            t_obstaculo = random.randint(10, 40 + int(400/((v-0.9)*100)))   #cria aleatoriamente o tempo ate o proximo obstaculo aparecer, esse valor diminui conforme a velocidade almenta
            coisa = Coisa(sprites)
            coisas.add(coisa)
            
        v += 0.0001   #aumenta a velocidade dos obstaculos constantemente
        corrido += v * 0.05
        corredor = font.render(str(int(corrido)) + ' metros', True, verde)     #atualiza o contador da distancia percorrida
            
        surf.fill((255, 255, 255)) # preenche a tela
        #cores variam de 0 a 255 > 0 = preto
        fundos.draw(surf)
        if ajudax > 0:
            surf.blit(imagem_ajuda, (ajudax - imagem_ajuda.get_rect().size[0], (surf_altura/2) - (imagem_ajuda.get_rect().size[1]/2)))
            ajudax -= proporcao(v) * (1/2)
            textoAjuda = fontAjuda.render('Aperte [ESPAÇO] para voar', True, verde)
            surf.blit(textoAjuda, (ajudax - (imagem_ajuda.get_rect().size[0]/2) - (textoAjuda.get_rect().size[0]/2), (surf_altura/2) - (textoAjuda.get_rect().size[1]/2)))
        surf.blit(imagem_corredor, ((surf_largura/2) - (imagem_corredor.get_rect().size[0]/2), proporcao(10)))
        surf.blit(corredor, ((surf_largura/2) - (corredor.get_rect().size[0]/2), (imagem_corredor.get_rect().size[1]/2) - (corredor.get_rect().size[1]/2) + proporcao(10.4)))
        sprites.draw(surf)
        paredes.draw(surf)
        
        sprites.update()
        fundos.update()
        paredes.update()
            
        if pygame.sprite.spritecollide(jetpack, coisas, False, pygame.sprite.collide_mask):
            game = 0
            v = v_inicial
            t_obstaculo = t_obstaculo_inicial
            ajudax = ajudax_inicial
            
            score += [corrido]
            score.sort(reverse = 1)
            score = score[:5]
            arquivo_score = shelve.open('arquivo_score')
            arquivo_score['score'] = score
            arquivo_score.close()
            
            corrido = 0
            for i in coisas:
                i.kill()
            for i in paredes:
                i.rect.left = 0
            jetpack.reset()
            surf.fill((55, 55, 55)) # preenche a tela
        
    else:   #se o jogo estiver desligado, ou seja, no menu
#        score = [412, 1, 44, 2222, 2]
        surf.blit(imagem_menu, (0, 0))      #apresenta o Menu
        if len(score) == 0:
            surf.blit(imagem_scoreboardoff, ((surf_largura/2) - (imagem_scoreboardoff.get_rect().size[0]/2), (surf_altura/2) - (imagem_scoreboardoff.get_rect().size[1]/2) + proporcao(20))) 
        else:
            surf.blit(imagem_scoreboardon, ((surf_largura/2) - (imagem_scoreboardoff.get_rect().size[0]/2), (surf_altura/2) - (imagem_scoreboardoff.get_rect().size[1]/2) + proporcao(20))) 
            textoScoreboard = fontScoreboard.render('- Scoreboard -', True, verde)
            surf.blit(textoScoreboard, ((surf_largura/2) - (textoScoreboard.get_rect().size[0]/2), (surf_altura/2) - (textoScoreboard.get_rect().size[1]/2) + proporcao(4.5)))
            textoScoreboard2 = fontScoreboard2.render('Aperte [E] para apagar os scores', True, verde)
            surf.blit(textoScoreboard2, ((surf_largura/2) - (textoScoreboard2.get_rect().size[0]/2), (surf_altura/2) - (textoScoreboard2.get_rect().size[1]/2) + proporcao(40)))
            
            n = 0
            for i in score:
                if n == 0:
                    texto = font.render('> ' + str(int(i)) + ' metros <', True, verde)
                else:
                    texto = font.render(str(int(i)) + ' metros', True, verde)
                surf.blit(texto, ((surf_largura/2) - (texto.get_rect().size[0]/2), (surf_altura/2) - (texto.get_rect().size[1]/2) + proporcao(12) + (proporcao(6)*n)))
                n += 1
    
    pygame.display.flip() # faz a atualizacao da tela









