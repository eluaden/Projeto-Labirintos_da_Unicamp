import pygame
import random
from jogador import Jogador
from moderador import Moderador
from Inimigos import Teacher, Statue
from itens import Clock, Bomb
from niveis import level_1

# Configurações do Pygame
pygame.init()
LARGURA_JANELA, ALTURA_JANELA = 1000, 800
TELA = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption('Os Labirintos da Unicamp')
FPS = 30

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

# Dimensões do labirinto
TAMANHO_CELULA = 40

class Jogo:
    def __init__(self):
        self.labirinto = level_1
        self.jogador = Jogador(nome="Player1", vidas=5, pontos_total=0, labirinto_atual=self.labirinto, posicao_atual=[1, 1], tempo_restante=100)
        self.professores = [Teacher(nome="Prof1", position=(2, 2))]
        self.estatuas = [Statue(nome="Statue1", position=(3, 3))]
        self.itens = self.gerar_itens_aleatorios()
        self.moderador = Moderador(self)
        self.clock = pygame.time.Clock()
        self.ultimo_tempo = pygame.time.get_ticks()  # Para rastrear o tempo
        

    def gerar_itens_aleatorios(self):
        
        itens = {"relogio": [], "bombas": [], "pontos": []}
        for _ in range(5):  # Número de cada item a ser gerado
            posicao_relogio = self.posicao_aleatoria()
            posicao_bomba = self.posicao_aleatoria()
            posicao_pontos = self.posicao_aleatoria()

            # Criando instâncias de itens específicos
            relogio = Clock(posicao_relogio)
            bomba = Bomb(posicao_bomba)

            # Adicionando as instâncias à lista de itens
            itens["relogio"].append(relogio)
            itens["bombas"].append(bomba)
            itens["pontos"].append(posicao_pontos)  # Mantendo a posição para desenho
            
        print(f"Esses são os itens:  {itens}")
        return itens
    
    def posicao_aleatoria(self):
        while True:
            x = random.randint(1, len(self.labirinto[0]) - 2)
            y = random.randint(1, len(self.labirinto) - 2)
            if self.labirinto[y][x] == 0:
                return (x, y)

    def desenhar_labirinto(self):
        for y, linha in enumerate(self.labirinto):
            for x, celula in enumerate(linha):
                cor = BRANCO if celula == 0 else PRETO
                pygame.draw.rect(TELA, cor, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    def desenhar_jogador(self):
        x, y = self.jogador.posicao_atual
        pygame.draw.rect(TELA, AZUL, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    def desenhar_inimigos(self):
        for professor in self.professores:
            x, y = professor.position
            pygame.draw.rect(TELA, VERMELHO, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
        for estatua in self.estatuas:
            x, y = estatua.position
            pygame.draw.rect(TELA, VERDE, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    def desenhar_itens(self):
        for tipo_item, itens in self.itens.items():
            cor = AMARELO if tipo_item == 'pontos' else VERDE if tipo_item == 'relogio' else VERMELHO
            if tipo_item in ['relogio', 'bombas']:
                for item in itens:
                    x, y = item.position  # Acessa a posição do item
                    pygame.draw.rect(TELA, cor, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
            else:
                for posicao in itens:
                    x, y = posicao
                    pygame.draw.rect(TELA, cor, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
    
    def desenhar_informacoes(self):
        fonte = pygame.font.SysFont(None, 36)
        texto_vidas = fonte.render(f'Vidas: {self.jogador.vidas}', True, BRANCO)
        texto_tempo = fonte.render(f'Tempo: {self.jogador.tempo_restante}', True, BRANCO)
        texto_bombas = fonte.render(f'Bombas: {self.jogador.inventario["bombas"]}', True, BRANCO)
        
        TELA.blit(texto_vidas, (700, 40))
        TELA.blit(texto_tempo, (700, 60))
        TELA.blit(texto_bombas, (700, 80))
        
    def atualizar_tempo(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tempo >= 1000:  # 1000 milissegundos = 1 segundo
            self.jogador.tempo_restante -= 1
            self.ultimo_tempo = agora
            print(f"vidas:{self.jogador.vidas}, tempo:{self.jogador.tempo_restante}")
            print(f"Inventario: {self.jogador.inventario}")
            if self.jogador.tempo_restante <= 0:
                print("Fim de jogo!")
                pygame.quit()
                quit()

    def atualizar_jogo(self):
        self.moderador.verificar_colisao(self.jogador)
    
        # Verifique colisão com bombas
        #print(f"Esses são os itenssss:  {self.itens}")
        for bomba in self.itens["bombas"]:
            #print(bomba.position)
            if tuple(self.jogador.posicao_atual) == bomba.position and not bomba._on_inv:
                self.jogador.inventario["bombas"] += 1  # Adiciona a bomba ao inventário do jogador
                self.itens["bombas"].remove(bomba)  # Remove a bomba da lista de itens
        
        for relogio in self.itens["relogio"]:
            #print(bomba.position)
            if tuple(self.jogador.posicao_atual) == relogio.position:
                relogio.special_action(self.jogador)  # Adiciona a bomba ao inventário do jogador
                self.itens["relogio"].remove(relogio)  # Remove a bomba da lista de itens

    def jogar(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT:
                        self.jogador.mover('esquerda')
                    elif evento.key == pygame.K_RIGHT:
                        self.jogador.mover('direita')
                    elif evento.key == pygame.K_UP:
                        self.jogador.mover('cima')
                    elif evento.key == pygame.K_DOWN:
                        self.jogador.mover('baixo')

            self.atualizar_tempo()
            self.atualizar_jogo()

            # Atualize o jogador (incluindo a animação)
            self.jogador.update()

            TELA.fill(PRETO)
            self.desenhar_labirinto()
            self.desenhar_inimigos()
            self.desenhar_itens()
            
            # Desenhe informações na tela
            self.desenhar_informacoes()
            # Desenhe o jogador na sua posição atual
            TELA.blit(self.jogador.image, self.jogador.rect)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.jogar()


