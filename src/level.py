import pygame
import random
from jogador import Jogador
from inimigos import Teacher
from itens import Clock, Bomb, Book

# Configurações do Pygame
pygame.init()
LARGURA_JANELA, ALTURA_JANELA = 1200, 700  # Ajustado para as novas dimensões da tela
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
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)

# Dimensões do labirinto
TAMANHO_CELULA = 70
INFO_HEIGHT = 50  # Altura da área de informações

class Level:
    def __init__(self, nome, nome_usr, labirinto, itens, inimigos, tempo, media, estatua=None):
        self.nome = nome
        self.labirinto = labirinto
        self.posicoes_ocupadas = []
        self.professores = self.gerar_inimigos(inimigos["teachers"])
        self.itens = self.gerar_itens_aleatorios(itens["bombs"], itens["clocks"], itens["books"])
        self.clock = pygame.time.Clock()
        self.ultimo_tempo = pygame.time.get_ticks()
        self.media = media
        self.estatua = estatua
        self.saida = next(((y, x) for x in range(len(self.labirinto)) for y in range(len(self.labirinto[0])) if self.labirinto[x][y] == 3), None)
        self.jogador = Jogador(nome=nome_usr, nota=0, pontos_total=0, labirinto_atual=self.labirinto, posicao_atual=[1, 1], tempo_restante=tempo)

        # Dimensões do labirinto em pixels
        self.largura_labirinto = len(self.labirinto[0]) * TAMANHO_CELULA
        self.altura_labirinto = len(self.labirinto) * TAMANHO_CELULA

        # Ajuste para a câmera
        self.camera_x = 0
        self.camera_y = 0

    def gerar_itens_aleatorios(self, n_bomb, n_rel, n_liv):
        itens = {"relogios": [], "bombas": [], "livros": []}
        for _ in range(n_rel):
            posicao_relogio = self.posicao_aleatoria()
            relogio = Clock(posicao_relogio)
            itens["relogios"].append(relogio)
        for _ in range(n_bomb):
            posicao_bomba = self.posicao_aleatoria()
            bomba = Bomb(posicao_bomba)
            itens["bombas"].append(bomba)
        for _ in range(n_liv):
            posicao_livro = self.posicao_aleatoria()
            livro = Book(posicao_livro)
            itens["livros"].append(livro)
        return itens

    def gerar_inimigos(self, n_prof):
        professores = []
        for _ in range(n_prof):
            posicao_prof = self.posicao_aleatoria()
            professor = Teacher("prof", posicao_prof)
            professores.append(professor)
        return professores

    def posicao_aleatoria(self):
        while True:
            x = random.randint(1, len(self.labirinto[0]) - 2)
            y = random.randint(1, len(self.labirinto) - 2)
            if self.labirinto[y][x] == 0 and (x, y) not in self.posicoes_ocupadas:
                self.posicoes_ocupadas.append((x, y))
                return (x, y)

    def desenhar_labirinto(self):
        for y, linha in enumerate(self.labirinto):
            for x, celula in enumerate(linha):
                cor = BRANCO if celula == 0 else LARANJA if celula == 2 else ROXO if celula == 3 else PRETO
                pygame.draw.rect(TELA, cor, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y, TAMANHO_CELULA, TAMANHO_CELULA))
        
        # Desenhar a primeira fileira sempre preta
        for x in range(len(self.labirinto[0])):
            pygame.draw.rect(TELA, PRETO, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT - self.camera_y, TAMANHO_CELULA, TAMANHO_CELULA))


    def desenhar_jogador(self):
        x, y = self.jogador.posicao_atual
        pygame.draw.rect(TELA, AZUL, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y, TAMANHO_CELULA, TAMANHO_CELULA))

    def desenhar_inimigos(self):
        for professor in self.professores:
            x, y = professor.position
            pygame.draw.rect(TELA, VERMELHO, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y, TAMANHO_CELULA, TAMANHO_CELULA))
        if self.estatua:
            x, y = self.estatua.position
            pygame.draw.rect(TELA, VERMELHO, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y, TAMANHO_CELULA, TAMANHO_CELULA))

    def desenhar_itens(self):
        for tipo_item, itens in self.itens.items():
            cor = AMARELO if tipo_item == 'livros' else VERDE if tipo_item == 'relogios' else VERMELHO
            for item in itens:
                x, y = item.position
                pygame.draw.rect(TELA, cor, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y, TAMANHO_CELULA, TAMANHO_CELULA))

    def desenhar_informacoes(self):
        fonte = pygame.font.SysFont(None, 36)
        texto_nome = fonte.render(f'Nome: {self.jogador.nome}', True, BRANCO)
        texto_nota = fonte.render(f'Nota: {self.jogador.nota}', True, BRANCO)
        texto_tempo = fonte.render(f'Tempo: {self.jogador.tempo_restante}', True, BRANCO)
        texto_bombas = fonte.render(f'Bombas: {len(self.jogador.inventario["bombas"])}', True, BRANCO)

        for x in range(0, 1201, 50):  # Começa do 0, vai até 1200 com passo de 50
            pygame.draw.rect(TELA, PRETO, (x, 0, 50, 50))

        TELA.blit(texto_nome, (20, 10))
        TELA.blit(texto_nota, (300, 10))
        TELA.blit(texto_tempo, (500, 10))
        TELA.blit(texto_bombas, (700, 10))
        

    def atualizar_camera(self):
        jogador_x, jogador_y = self.jogador.posicao_atual

        # Calcula a posição desejada da câmera
        target_camera_x = jogador_x * TAMANHO_CELULA - LARGURA_JANELA // 2
        target_camera_y = jogador_y * TAMANHO_CELULA - (ALTURA_JANELA - INFO_HEIGHT) // 2

        # Interpolação suave para suavizar o movimento da câmera
        self.camera_x += (target_camera_x - self.camera_x) * 0.1
        self.camera_y += (target_camera_y - self.camera_y) * 0.1

        # Limita o deslocamento da câmera para que não mostre áreas fora do labirinto
        self.camera_x = max(0, min(self.camera_x, self.largura_labirinto - LARGURA_JANELA))
        self.camera_y = max(0, min(self.camera_y, self.altura_labirinto - ALTURA_JANELA + INFO_HEIGHT))

    def atualizacao_por_segundo(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tempo >= 1000:
            self.jogador.tempo_restante -= 1
            self.ultimo_tempo = agora
            print(f"Nota: {self.jogador.nota}, Tempo: {self.jogador.tempo_restante}")

            for professor in self.professores:
                professor.wander(self.labirinto)

            if self.jogador.tempo_restante <= 0:
                print("Seu tempo acabou!")
                pygame.quit()
                quit()

    def verificar_colisoes(self):
        for bomba in self.itens["bombas"]:
            if tuple(self.jogador.posicao_atual) == bomba.position and not bomba.on_inv:
                self.jogador.inventario["bombas"].append(bomba)
                bomba.on_inv = True
                self.itens["bombas"].remove(bomba)

        for relogio in self.itens["relogios"]:
            if tuple(self.jogador.posicao_atual) == relogio.position:
                relogio.special_action(self.jogador)
                self.itens["relogios"].remove(relogio)

        for livro in self.itens["livros"]:
            if tuple(self.jogador.posicao_atual) == livro.position:
                livro.special_action(self.jogador)
                self.itens["livros"].remove(livro)

        if tuple(self.jogador.posicao_atual) == self.saida:
            if self.jogador.nota >= self.media:
                print("Você passou de ano!")
                pygame.quit()
                quit()
            else:
                print("Faltam pontos para passar de ano!")

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
                    elif evento.key == pygame.K_SPACE and len(self.jogador.inventario["bombas"]) > 0:
                        bomba = self.jogador.inventario["bombas"].pop()
                        bomba.special_action(self.jogador)

            self.atualizacao_por_segundo()
            self.verificar_colisoes()
            self.atualizar_camera()

            TELA.fill(PRETO)
            self.desenhar_labirinto()
            self.desenhar_inimigos()
            self.desenhar_itens()
            self.desenhar_informacoes()
            self.desenhar_jogador()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()






