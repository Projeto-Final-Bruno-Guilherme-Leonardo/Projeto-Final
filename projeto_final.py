"""
Jogo Jetpack
Autores: Bruno Conte, Guilherme Aranha, Leonardo Alvarez
"""

import pygame    # Importa todos os módulos que serão usados
import sys
import random
import shelve

pygame.init()    # Inicia o pygame

surf_altura = 800   #<-----------| Altura da tela, recomendado: 800 | (AJUSTE PARA O TAMANHO DA SUA TELA)
surf_largura = int(surf_altura * 1.5)   # Largura em função da altura da janela

def proporcao(a, b = 0):    # Função que mantém a proporção entre as sprites e o tamanho da tela
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

pygame.mixer.music.load('mixer/battleship.ogg')     # Load a música tema
pygame.mixer.music.set_volume(0.02)                 # Abaixa o volume da música tema
pygame.mixer.music.play(-1)                         # Começa a tocar a música ciclicamente

som_batida = pygame.mixer.Sound('mixer/batida.ogg') # Load som da batida

coisa_imagens = []                                  # Lista que guarda as possíveis imagens para os obstáculos

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
    
    for nome, tamanho in coisas_info:       # Load as imagens dos obstáculos
        imagem = pygame.image.load('imagens/' + nome + '.png').convert_alpha()
        imagem = pygame.transform.scale(imagem, proporcao(tamanho, tamanho))
        coisa_imagens.append(imagem)

except pygame.error:        # Caso algum load falhe, print ERRO
    print('Erro ao tentar ler uma imagem')
    sys.exit()

class Cenario(pygame.sprite.Sprite):
    '''Sprites que são usadas apenas para o cenario, elas nao interagem com o player'''
    def __init__(self, grupo, imagem, paralaxe = 0):
        super().__init__(grupo)
        
        self.image = imagem
        self.rect = self.image.get_rect()
        self.paralaxe = paralaxe
    
    def update(self):       # Anda o cenário para a esquerda
        self.rect.x -= int(proporcao(v)) - (self.paralaxe * (2/3) * int(proporcao(v)))  # Se o cenario tiver paralaxe, ele anda mais devagar que o resto dos cenarios
        if self.rect.centerx < 0:       # Os cenários apresentam um fundo sem fim, sempre andando para a esquerda
            self.rect.centerx = surf_largura
            

class Jetpack(pygame.sprite.Sprite):
    '''Sprite do player, move-se verticalmente para desviar dos obstaculos'''
    def __init__(self, grupo):
        super().__init__(grupo)
        
        self.image = imagem_jetpack
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = proporcao(10)
        self.rect.bottom = proporcao(100, 'borda')
        self.speed = 0                                      # Velocidade vertical do player
        self.a = 0                                          # Aceleração vertical do player
        
    def update(self):
        self.speed += self.a
        self.rect.y += proporcao(self.speed)
        if self.rect.top + (1 * self.speed) < proporcao(0, 'borda'):        # Não permite que o player sair para cima da tela
            self.rect.top = proporcao(0, 'borda')
            self.speed = 0
        if self.rect.bottom + (1 * self.speed) > proporcao(100, 'borda'):   # Não permite que o player sair para baixo da tela
            self.rect.bottom = proporcao(100, 'borda')
            self.speed = 0
    
    def reset(self):                                                        # Reseta o player para recomeçar o jogo
        self.rect.bottom = proporcao(100, 'borda')
        self.speed = 0  # Velocidade vertical do player
        self.a = 0  # Aceleração vertical do player
        
            
class Coisa(pygame.sprite.Sprite):
    '''Sprite dos obstaculos, o player deve desviar delas enquanto elas passam da direita para a esquerda'''
    def __init__(self, grupo):
        super().__init__(grupo)
        
        preso = random.sample([0,0,0,0,0,0,0,0,1,2], k=1)[0]            # Randomiza a chance de ser um obstáculo no chão, no teto ou voando
        
        if preso == 0:      # Obstáculos voando tem uma imagem em qualquer orientação
            self.image = pygame.transform.rotate(coisa_imagens[random.randint(0, len(coisa_imagens) -1)], random.randint(0,359))
        elif preso == 1:    # Obstáculos no chão ficam perpendiculares ao chão
            self.image = coisa_imagens[random.randint(0, len(coisa_imagens) -1)]
        else:               # Obstáculos no teto ficam perpendiculares ao teto
            self.image = pygame.transform.rotate(coisa_imagens[random.randint(0, len(coisa_imagens) -1)], 180)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = surf_largura
        if preso == 2:      # Obstáculos no chão são posicionados no chão
            self.rect.top = proporcao(0, 'borda')
        elif preso == 1:    # Obstáculos no teto são posicionados no teto
            self.rect.bottom = proporcao(100, 'borda')
        else:               # Obstáculos voando tem uma posição aleatória
            self.rect.y = random.randint(proporcao(0, 'borda'), proporcao(100, 'borda') - self.rect.height)
        
    def update(self):       # Anda o obstáculo para a esquerda junto do fundo da tela do jogo
        self.rect.x -= int(proporcao(v))
        if self.rect.right < 0:
            self.kill()
        
        


sprites = pygame.sprite.Group()         # Cria os grupos de sprites (player + obstáculos)
coisas = pygame.sprite.Group()          # (obstáculos)
paredes = pygame.sprite.Group()         # (cenário do chão e do teto)
fundos = pygame.sprite.Group()          # (cenário do fundo)

jetpack = Jetpack(sprites)              # Cria a sprite do player

teto = Cenario(paredes, imagem_teto)    # Cria as sprites do cenário
teto.rect.left = proporcao(0)
teto.rect.bottom = proporcao(0, 'borda')
chao = Cenario(paredes, imagem_chao)
chao.rect.left = proporcao(0)
chao.rect.top = proporcao(100, 'borda')
fundo = Cenario(fundos, imagem_fundo, paralaxe = True)
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
            surf.blit(imagem_ajuda, (ajudax - imagem_ajuda.get_rect().size[0], (surf_altura/2) - (imagem_ajuda.get_rect().size[1]/2)))
            textoAjuda = fontAjuda.render('Aperte [ESPAÇO] para voar', True, verde)
            surf.blit(textoAjuda, (ajudax - (imagem_ajuda.get_rect().size[0]/2) - (textoAjuda.get_rect().size[0]/2), (surf_altura/2) - (textoAjuda.get_rect().size[1]/2)))
            ajudax -= proporcao(v) * (1/2)
        surf.blit(imagem_corredor, ((surf_largura/2) - (imagem_corredor.get_rect().size[0]/2), proporcao(10)))      # Desenha o mostrador dos metros percorridos
        surf.blit(corredor, ((surf_largura/2) - (corredor.get_rect().size[0]/2), (imagem_corredor.get_rect().size[1]/2) - (corredor.get_rect().size[1]/2) + proporcao(10.4)))   #desenha o texto no mostrador
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
        surf.blit(imagem_menu, (0, 0))      # Apresenta o MENU
        assert len(score) <= 5, 'Há mais de 5 scores na lista de scores: ' + str(score)     # Garante que não tem mais que 5 scores para serem mostrados na scoreboard
        if len(score) == 0:                 # Se não tiver nenhum score registrado, a scoreboard aparece fechada
            surf.blit(imagem_scoreboardoff, ((surf_largura/2) - (imagem_scoreboardoff.get_rect().size[0]/2), (surf_altura/2) - (imagem_scoreboardoff.get_rect().size[1]/2) + proporcao(20))) 
        else:                               # Se tiverem scores registrados, a scoreboard aparece aberta e apresenta os scores
            surf.blit(imagem_scoreboardon, ((surf_largura/2) - (imagem_scoreboardoff.get_rect().size[0]/2), (surf_altura/2) - (imagem_scoreboardoff.get_rect().size[1]/2) + proporcao(20))) 
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




