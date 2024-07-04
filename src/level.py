import pygame
import random
from jogador import Jogador
from moderador import Moderador
from inimigos import Teacher, Statue
from itens import Clock, Bomb, Book
from save import *
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
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)

# Dimensões do labirinto
TAMANHO_CELULA = 40

class Level:
    def __init__(self,nome,labirinto,itens,inimigos,tempo,media):
        self.nome = nome
        self.labirinto = labirinto

        if verify_save(self.nome):
            level = read_level_progress(self.nome)
            self.labirinto = level["maze"]
            self.professores = level["enemies"]["teachers"]
            self.itens = level["items"]
            self.posicoes_ocupadas = level["posicoes_ocupadas"]

            if level["player"]:
                self.jogador = level["player"]
            else:
                self.jogador = Jogador(nome="Player1",nota = 0, pontos_total=0, labirinto_atual=self.labirinto, posicao_atual=[1, 1], tempo_restante= tempo)
        
        self.posicoes_ocupadas = [] # posicoes do jogo que ja estao ocupadas, seja por item, seja por inimigo, seja por jogador
        self.professores = self.gerar_inimigos_aleatorios(inimigos["teachers"])
        self.itens = self.gerar_itens_aleatorios(itens["bombs"],itens["clocks"],itens["books"])
        self.moderador = Moderador(self)
        self.clock = pygame.time.Clock()
        self.ultimo_tempo = pygame.time.get_ticks()  # Para rastrear o tempo
        self.media = media
        self.saida = next(((y,x) for x in range(len(self.labirinto)) for y in range(len(self.labirinto[0])) if self.labirinto[x][y] == 3), None)
        print(f"Essa é a saída: {self.saida}")

        
            



        

    def gerar_itens_aleatorios(self,n_bomb,n_rel,n_liv):
        
        itens = {"relogios": [], "bombas": [], "livros": []}
        for _ in range(n_rel):  # Número de cada item a ser gerado
            posicao_relogio = self.posicao_aleatoria()

            # Criando instâncias de itens específicos
            relogio = Clock(posicao_relogio)

            # Adicionando as instâncias à lista de itens
            itens["relogios"].append(relogio)
        for _ in range(n_bomb):  
            posicao_bomba = self.posicao_aleatoria()
            bomba = Bomb(posicao_bomba)
            itens["bombas"].append(bomba)
        for _ in range(n_liv):
            posicao_livro = self.posicao_aleatoria()
            livro = Book(posicao_livro)
            itens["livros"].append(livro)

            
        print(f"Esses são os itens:  {itens}")
        return itens
    
    def gerar_inimigos_aleatorios(self,n_prof):
        professores = []
        for _ in range(n_prof):
            posicao_prof = self.posicao_aleatoria()
            professor = Teacher("prof",posicao_prof)
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

                pygame.draw.rect(TELA, cor, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    def desenhar_jogador(self):
        x, y = self.jogador.posicao_atual
        pygame.draw.rect(TELA, AZUL, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    def desenhar_inimigos(self,estatua = None):
        for professor in self.professores:
            x, y = professor.position
            pygame.draw.rect(TELA, VERMELHO, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
        if estatua:
            x, y = estatua.position
            pygame.draw.rect(TELA, VERMELHO, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))    

    def desenhar_itens(self):
        for tipo_item, itens in self.itens.items():
            cor = AMARELO if tipo_item == 'livros' else VERDE if tipo_item == 'relogios' else VERMELHO
            if tipo_item in ['relogios', 'bombas','livros']:
                for item in itens:
                    x, y = item.position  # Acessa a posição do item
                    pygame.draw.rect(TELA, cor, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
            
    
    def desenhar_informacoes(self):
        fonte = pygame.font.SysFont(None, 36)
        texto_nota = fonte.render(f'nota: {self.jogador.nota}', True, BRANCO)
        texto_tempo = fonte.render(f'Tempo: {self.jogador.tempo_restante}', True, BRANCO)
        texto_bombas = fonte.render(f'Bombas: {len(self.jogador.inventario["bombas"])}', True, BRANCO)
        
        TELA.blit(texto_nota, (700, 40))
        TELA.blit(texto_tempo, (700, 60))
        TELA.blit(texto_bombas, (700, 80))
        
    def atualizacao_por_segundo(self): #coisas que ocorrem na tela a cada segundo
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tempo >= 1000:  # 1000 milissegundos = 1 segundo
            self.jogador.tempo_restante -= 1
            self.ultimo_tempo = agora
            print(f"nota:{self.jogador.nota}, tempo:{self.jogador.tempo_restante}")
            print(f"Inventario: {self.jogador.inventario}")

            for professor in self.professores: # atualiza posição dos professores
                professor.wander(self.labirinto)

            if self.jogador.tempo_restante <= 0:
                print("Seu tempo acabou!")
                self.moderador.perdeu()
                pygame.quit()
                quit()

    def verificar_colisoes(self):
        # Verifique colisão com bombas
        #print(f"Esses são os itens:  {self.itens}")
        for bomba in self.itens["bombas"]:
            #print(bomba.position)
            if tuple(self.jogador.posicao_atual) == bomba.position and not bomba._on_inv:
                self.jogador.inventario["bombas"].append(bomba)
                bomba.on_inv = True  # Adiciona a bomba ao inventário do jogador
                self.itens["bombas"].remove(bomba)  # Remove a bomba da lista de itens
        
        for relogio in self.itens["relogios"]:
            
            if tuple(self.jogador.posicao_atual) == relogio.position:
                relogio.special_action(self.jogador)  
                self.itens["relogios"].remove(relogio)  
        
        for livro in self.itens["livros"]:
            if tuple(self.jogador.posicao_atual) == livro.position:
                livro.special_action(self.jogador) # Adiciona a bomba ao inventário do jogador
                self.itens["livros"].remove(livro)  # Remove a bomba da lista de itens

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




