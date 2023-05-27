import pygame
import random
from sprites import sprites, click_som, toggle_som
from chicken import *
global jogador
class TelaInicial():
    def __init__(self, tela):
        self.tela = tela
        self.fonte  = pygame.font.Font('assets/MinecraftTen-VGORe.ttf', 30)
        self.fundo = sprites['inicio']
        self.botaoPlay = pygame.Rect(55, 405, 425, 40)
        self.botaoRanking = pygame.Rect(55, 460, 425, 40)
        self.botaoSair = pygame.Rect(275, 585, 210, 40)
        self.botaoOptions = pygame.Rect(55, 585, 210, 40)
        self.play = False
        self.options = False
        self.ranking = False
        self.caixaTexto = CaixaTexto(self.fonte, tela)
    def desenha(self):
        self.tela.fill((255, 255, 255))
        self.tela.blit(self.fundo, (0, 0))
        self.caixaTexto.desenha()
        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            self.caixaTexto.escreve(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
                mouse_x, mouse_y = event.pos
                if self.botaoPlay.collidepoint(mouse_x, mouse_y):
                    self.play = True
                    click_som.play()
                elif self.botaoRanking.collidepoint(mouse_x, mouse_y):
                    self.ranking = True
                    click_som.play()
                elif self.botaoOptions.collidepoint(mouse_x, mouse_y):
                    self.options = True
                    click_som.play()
                elif self.botaoSair.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    return False
        return True
    def troca_tela(self):
        if self.play:
            return TelaJogo(self.tela, self.caixaTexto.texto)
        elif self.ranking:
            return TelaRanking(self.tela)
        elif self.options:
            return TelaOptions(self.tela)
        else:
            return self
        
class TelaJogo:
    def __init__(self, tela, nome='',opcoes= None):
        self.opcoes = opcoes
        if self.opcoes == None: 
            self.opcoes = {'Vidas': 1,'Velocidade': 2, 'NBarcos': 3, 'NMinecarts': 3, 'VB': 4, 'VM': 4, 'Efeitos': True, 'Musica': True}
        self.frame = 0
        self.tela = tela
        self.y = 0
        self.clock = pygame.time.Clock()
        self.player = Player(self.opcoes['Velocidade'], self.opcoes['Vidas'])
        self.fonte  = pygame.font.Font(None, 36)
        self.nome = nome
        self.velocidade = self.opcoes['Velocidade']
        print(self.velocidade)
        for i in range(17):
            self.nova_fileira(y=800-(i*50))
    def nova_fileira(self, y=0):
        block = random.choice(['grama', 'agua', 'trilho', 'grama', 'trilho', 'grama'])
        if y > 500 and y <850:
            block = 'grama'
        direcao = random.choice([1, -1])
        speedbarco = random.randint(self.opcoes['VB'], self.opcoes['VB']+3)
        speedcart = random.randint(self.opcoes['VM'], self.opcoes['VM']+3)

        temBarco = False
        for i in range(10):
            if block == 'grama':Grama(i * 50 + 25, y, self.player)
            elif block == 'agua':Agua(i * 50 + 25, y, self.player)
            elif block == 'trilho':Trilho(i * 50 + 25, y, self.player)
            if block == 'agua' and random.randint(0, (10-self.opcoes['NBarcos'])) == 0:
                Barco(i * 50 + 25, y, self.player, speedbarco, direcao)
                temBarco = True
            elif not temBarco and i == 9 and block == 'agua':
                Barco(i * 50 + 25, y, self.player, speedbarco, direcao)
            if block == 'trilho' and random.randint(0, (10-self.opcoes['NMinecarts'])) == 0:Minecart(i * 50 + 25, y, self.player, speedcart, direcao)
    def salvar_highscore(self):
        if self.nome != '' and self.nome != 'escreva seu nome':
            string = '\n'+self.nome+','+str(self.player.score)
            with open('assets/scores.csv', 'a') as f:
                f.write(string)
                print(string)
    def update(self):
        if self.y >= int(50/self.player.velocidade): # Gerar uma nova fileira em cima
            self.nova_fileira()
            self.y = 0
        self.y += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        self.player.update()
        self.clock.tick(30)
        return True
    
    def desenha(self):
        self.tela.fill((255, 255, 255))
        for i in self.player.blocos:
            self.tela.blit(i.image, i.rect)
        for i in self.player.obstaculos:
            self.tela.blit(i.image, i.rect)
        self.tela.blit(self.player.image, self.player.rect)
        t = "pontuacao: " + str(self.player.score)
        texto = self.fonte.render(t, True, (255, 255, 255))
        self.tela.blit(texto, (300, 10))
        pygame.display.update()
    
    def troca_tela(self):
        if self.player.checarMorte():
            self.salvar_highscore()
            return TelaInicial(self.tela)
        else:
            return self
class TelaRanking():
    def __init__(self, tela):
        self.ranking = {}
        self.tela = tela
        self.fundo = sprites['ranking']
        with open('assets/scores.csv', 'r') as scores:
            for line in scores:
                nome, score = line.split(',')
                self.ranking[nome] = int(score)
        self.ranking = sorted(self.ranking.items(), key=lambda x: x[1], reverse=True)
        self.fonte  = pygame.font.Font('assets/MinecraftTen-VGORe.ttf', 30)
        self.botaoSair = pygame.Rect(0, 0, 100, 50)
        self.voltar = False
    def desenha(self):
        self.tela.fill((0, 0, 0))
        self.tela.blit(self.fundo, (0,0))
        texto1 = self.fonte.render('voltar', True, (255, 255, 255))
        self.tela.blit(texto1, (0, 0))
        for i in range(len(self.ranking)):
            nome, score = self.ranking[i]
            texto = self.fonte.render(str(i+1)+'. '+nome+' - '+str(score), True, (255, 255, 255))
            self.tela.blit(texto, (100, 100+i*50))
        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.botaoSair.collidepoint(event.pos) or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE): # Left mouse button click
                self.voltar = True
                click_som.play()
        return True
    def troca_tela(self):
        if self.voltar:
            return TelaInicial(self.tela)
        else:
            return self
class TelaOptions():
    def __init__(self, tela):
        self.tela, self.fundo, self.fonte, self.voltar, self.play = tela, sprites['ranking'], pygame.font.Font('assets/MinecraftTen-VGORe.ttf', 30), False, False
        self.botoes = {name: sprites[name].get_rect() for name in ['botaoVoltar', 'botaoJogar', 'botaoVelocidade', 'botaoMusica', 'botaoEfeitos', 'botaoNBarcos', 'botaoNMinecarts', 'botaoVidas', 'botaoVB', 'botaoVM']}
        self.opcoes = {'Vidas': 1,'Velocidade': 2, 'NBarcos': 3, 'NMinecarts': 3, 'VB': 2, 'VM': 2, 'Efeitos': True, 'Musica': True}

        #posiciona botoes
        for x, y, name in [(250, 300, 'botaoNBarcos'), (250, 350, 'botaoNMinecarts'), (250, 250, 'botaoVelocidade'), (150, 500, 'botaoEfeitos'), (350, 500, 'botaoMusica'), (250, 400, 'botaoVB'), (250, 450, 'botaoVM'), (400, 640, 'botaoVoltar'), (250, 130, 'botaoJogar'), (250, 200, 'botaoVidas')]:
            for n in (name if isinstance(name, list) else [name]):
                self.botoes[n].centerx, self.botoes[n].centery = x, y
    def desenha(self):
        self.tela.fill((0,0,0))
        self.tela.blit(self.fundo, (0,0))
        [self.tela.blit(sprites[name], self.botoes[name]) for name in self.botoes.keys()]
        for i in range(6):
            texto = self.fonte.render(str(list(self.opcoes.values())[i]), True, (210, 210, 210))
            self.tela.blit(texto, (400, 187+i*50))
        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name in self.botoes.keys():
                    if self.botoes[name].collidepoint(event.pos):
                        if name in ['botaoVelocidade', 'botaoNBarcos', 'botaoNMinecarts', 'botaoVidas', 'botaoVB', 'botaoVM']:
                            click_som.play()
                            self.opcoes[name[5:]] = self.opcoes[name[5:]] % 9 + 1
                        elif name in ['botaoMusica', 'botaoEfeitos']:
                            toggle_som()
                            click_som.play()
                            
                        elif name == 'botaoVoltar': self.voltar = True, click_som.play()
                        elif name == 'botaoJogar': self.play = True, click_som.play()
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.voltar = True
        return True
    def troca_tela(self):
        if self.voltar:
            return TelaInicial(self.tela)
        elif self.play:
            return TelaJogo(self.tela, opcoes = self.opcoes)
        else:
            return self