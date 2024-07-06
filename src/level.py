import pygame
import random
from jogador import Jogador
from inimigos import Teacher,Statue
from itens import Clock, Bomb, Book
from save import *
import random


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
LARANJA = (245, 189, 73)
ESCOLHA = (219, 58, 52)

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
        imagem_parede = pygame.image.load('assets/parede.png')
        imagem_chao = pygame.image.load('assets/chao.png')
        imagem_saida = pygame.image.load('assets/saida.png')
        imagem_entrada = pygame.image.load('assets/entrada.png')
        imagem_entrada = pygame.transform.scale(imagem_entrada, (TAMANHO_CELULA, TAMANHO_CELULA))
        imagem_saida = pygame.transform.scale(imagem_saida, (TAMANHO_CELULA, TAMANHO_CELULA))
        imagem_chao = pygame.transform.scale(imagem_chao, (TAMANHO_CELULA, TAMANHO_CELULA))
        imagem_parede = pygame.transform.scale(imagem_parede, (TAMANHO_CELULA, TAMANHO_CELULA))
        for y, linha in enumerate(self.labirinto):
            for x, celula in enumerate(linha):
                if celula == 1:
                    TELA.blit(imagem_parede, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y))
                elif celula == 0:
                    TELA.blit(imagem_chao, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y))
                elif celula == 3:
                    TELA.blit(imagem_saida, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y))
                elif celula == 2:
                    TELA.blit(imagem_entrada, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y))
        
        # Desenhar a primeira fileira sempre preta
        


    def desenhar_jogador(self):
        jogador_img = pygame.image.load('assets/jogador.png')

        x, y = self.jogador.posicao_atual
        TELA.blit(jogador_img, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y))

    def desenhar_inimigos(self):
        professor_img = pygame.image.load('assets/professor.png')
        estatua_img = pygame.image.load('assets/estatua.png')

        for professor in self.professores:
            x, y = professor.position
            TELA.blit(professor_img, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y))
        if self.estatua:
            x, y = self.estatua.position
            TELA.blit(estatua_img, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y))

    def desenhar_itens(self):
        # Carregar as imagens dos itens
        imagem_livro = pygame.image.load('assets/livro.png')
        imagem_relogio = pygame.image.load('assets/relogio.png')
        imagem_bomba = pygame.image.load('assets/bomba.png')

        # Redimensionar as imagens para o tamanho desejado (opcional)
        imagem_livro = pygame.transform.scale(imagem_livro, (TAMANHO_CELULA, TAMANHO_CELULA))
        imagem_relogio = pygame.transform.scale(imagem_relogio, (TAMANHO_CELULA, TAMANHO_CELULA))
        imagem_bomba = pygame.transform.scale(imagem_bomba, (TAMANHO_CELULA, TAMANHO_CELULA))

        for tipo_item, itens in self.itens.items():
            cor = AMARELO if tipo_item == 'livros' else VERDE if tipo_item == 'relogios' else VERMELHO
            for item in itens:
                x, y = item.position
                if tipo_item == "bombas":
                    TELA.blit(imagem_bomba, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y))
                elif tipo_item == "relogios":
                    TELA.blit(imagem_relogio, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y))
                elif tipo_item == "livros":
                    TELA.blit(imagem_livro, ((x * TAMANHO_CELULA) - self.camera_x, INFO_HEIGHT + (y * TAMANHO_CELULA) - self.camera_y))

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
        

    def popup_pergunta(self, pergunta):
        largura, altura = 400, 300
        x_popup = (LARGURA_JANELA - largura) // 2
        y_popup = (ALTURA_JANELA - altura) // 2

        # Escolha aleatória da posição da resposta errada
        resposta_posicao = random.choice([True, False])

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if resposta_posicao:
                        # Verifica clique na resposta errada (à esquerda)
                        if x_popup + 50 <= x <= x_popup + 150 and y_popup + altura - 100 <= y <= y_popup + altura - 50:
                            return False
                        # Verifica clique na resposta certa (à direita)
                        elif x_popup + 250 <= x <= x_popup + 350 and y_popup + altura - 100 <= y <= y_popup + altura - 50:
                            return True
                    else:
                        # Verifica clique na resposta errada (à direita)
                        if x_popup + 250 <= x <= x_popup + 350 and y_popup + altura - 100 <= y <= y_popup + altura - 50:
                            return False
                        # Verifica clique na resposta certa (à esquerda)
                        elif x_popup + 50 <= x <= x_popup + 150 and y_popup + altura - 100 <= y <= y_popup + altura - 50:
                            return True

            TELA.fill(PRETO)
            pygame.draw.rect(TELA, LARANJA, (x_popup, y_popup, largura, altura))
            pygame.draw.rect(TELA, BRANCO, (x_popup, y_popup, largura, altura), 5)
            fonte = pygame.font.SysFont(None, 36)
            texto = fonte.render(pergunta["pergunta"], True, BRANCO)
            texto_rect = texto.get_rect(center=(x_popup + largura // 2, y_popup + 50))
            TELA.blit(texto, texto_rect)

            # Definindo coordenadas com base na escolha aleatória
            if resposta_posicao:
                pygame.draw.rect(TELA, ESCOLHA, (x_popup + 50, y_popup + altura - 100, 100, 50))
                pygame.draw.rect(TELA, BRANCO, (x_popup + 50, y_popup + altura - 100, 100, 50), 3)
                texto = fonte.render(str(pergunta["resposta_errada"]), True, BRANCO)
                texto_rect = texto.get_rect(center=(x_popup + 100, y_popup + altura - 75))
                TELA.blit(texto, texto_rect)

                pygame.draw.rect(TELA, ESCOLHA, (x_popup + 250, y_popup + altura - 100, 100, 50))
                pygame.draw.rect(TELA, BRANCO, (x_popup + 250, y_popup + altura - 100, 100, 50), 3)
                texto = fonte.render(str(pergunta["resposta_certa"]), True, BRANCO)
                texto_rect = texto.get_rect(center=(x_popup + 300, y_popup + altura - 75))
                TELA.blit(texto, texto_rect)
            else:
                pygame.draw.rect(TELA, ESCOLHA, (x_popup + 50, y_popup + altura - 100, 100, 50))
                pygame.draw.rect(TELA, BRANCO, (x_popup + 50, y_popup + altura - 100, 100, 50), 3)
                texto = fonte.render(str(pergunta["resposta_certa"]), True, BRANCO)
                texto_rect = texto.get_rect(center=(x_popup + 100, y_popup + altura - 75))
                TELA.blit(texto, texto_rect)

                pygame.draw.rect(TELA, ESCOLHA, (x_popup + 250, y_popup + altura - 100, 100, 50))
                pygame.draw.rect(TELA, BRANCO, (x_popup + 250, y_popup + altura - 100, 100, 50), 3)
                texto = fonte.render(str(pergunta["resposta_errada"]), True, BRANCO)
                texto_rect = texto.get_rect(center=(x_popup + 300, y_popup + altura - 75))
                TELA.blit(texto, texto_rect)

            self.atualizacao_por_segundo()
            self.desenhar_informacoes()

            pygame.display.flip()
    """
    def popup_pergunta(self, pergunta):
        largura,altura = 400,300
        x_popup = (LARGURA_JANELA - largura) // 2
        y_popup = (ALTURA_JANELA - altura) // 2
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # Verifica se o clique foi dentro do retângulo "Sim"
                    if x_popup + 50 <= x <= x_popup + 150 and y_popup + altura - 100 <= y <= y_popup + altura - 50:
                        
                        return False
                    # Verifica se o clique foi dentro do retângulo "Não"
                    elif x_popup + 250 <= x <= x_popup + 350 and y_popup + altura - 100 <= y <= y_popup + altura - 50:
                        
                        return True

            TELA.fill(PRETO)
            pygame.draw.rect(TELA, LARANJA, (x_popup, y_popup, largura, altura))
            pygame.draw.rect(TELA, BRANCO, (x_popup, y_popup, largura, altura), 5)
            fonte = pygame.font.SysFont(None, 36)
            texto = fonte.render(pergunta["pergunta"], True, BRANCO)
            texto_rect = texto.get_rect(center=(x_popup + largura // 2, y_popup + 50))
            TELA.blit(texto, texto_rect)

            pygame.draw.rect(TELA, VERDE, (x_popup + 50, y_popup + altura - 100, 100, 50))
            pygame.draw.rect(TELA, BRANCO, (x_popup + 50, y_popup + altura - 100, 100, 50), 3)
            fonte = pygame.font.SysFont(None, 36)
            texto = fonte.render(str(pergunta["resposta_errada"]), True, BRANCO)
            texto_rect = texto.get_rect(center=(x_popup + 100, y_popup + altura - 75))
            TELA.blit(texto, texto_rect)

            pygame.draw.rect(TELA, VERMELHO, (x_popup + 250, y_popup + altura - 100, 100, 50))
            pygame.draw.rect(TELA, BRANCO, (x_popup + 250, y_popup + altura - 100, 100, 50), 3)
            texto = fonte.render(str(pergunta["resposta_certa"]), True, BRANCO)
            texto_rect = texto.get_rect(center=(x_popup + 300, y_popup + altura - 75))
            TELA.blit(texto, texto_rect)


            
            self.atualizacao_por_segundo()
            self.desenhar_informacoes()

            pygame.display.flip()
    """
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
                self.popup_final(False)
                self.perdeu()
                pygame.quit()
                quit()


    def popup_final(self, vitoria):
        largura,altura = 400,300
        x_popup = (LARGURA_JANELA - largura) // 2
        y_popup = (ALTURA_JANELA - altura) // 2

        start_time = pygame.time.get_ticks()

       

        user = read_user(self.jogador.nome)



        while pygame.time.get_ticks() - start_time < 4000:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            TELA.fill(PRETO)
            pygame.draw.rect(TELA, LARANJA, (x_popup, y_popup, largura, altura))
            pygame.draw.rect(TELA, BRANCO, (x_popup, y_popup, largura, altura), 5)
            fonte = pygame.font.SysFont(None, 36)
            if vitoria:
                pontuacao = self.jogador.nota * 30 + self.jogador.tempo_restante * 10

                if int(self.nome[6]) >= user["ultimo_nivel"]:
                    p_t = user["pontuacao"] + pontuacao
                else:
                    p_t = user["pontuacao"]

                texto = fonte.render("Você passou de ano!", True, BRANCO)

            else:
                pontuacao = ((10 - int(self.nome[6])) * 30)
                if int(self.nome[6]) >= user["ultimo_nivel"]:
                    p_t = user["pontuacao"] - pontuacao
                else:
                    p_t = user["pontuacao"]

                texto = fonte.render("Você reprovou", True, BRANCO)

            pontos = fonte.render(f"Pontos na fase: {pontuacao}", True, BRANCO)
            pontos_totais = fonte.render(f"Pontos totais: {p_t}", True, BRANCO)   

            texto_rect = texto.get_rect(center=(x_popup + largura // 2, y_popup + 50))

            pontos_rect = pontos.get_rect(center=(x_popup + largura // 2, y_popup + 80))

            totais_rect = pontos_totais.get_rect(center=(x_popup + largura // 2, y_popup + 110))
            TELA.blit(texto, texto_rect)
            TELA.blit(pontos, pontos_rect)
            TELA.blit(pontos_totais, totais_rect)

            pygame.display.flip()


    def venceu(self):
        pontuacao = self.jogador.nota * 30 + self.jogador.tempo_restante * 10
        print(pontuacao)

        user = read_user(self.jogador.nome)
        if user["ultimo_nivel"] != 10 and (user["ultimo_nivel"] <= int(self.nome[6])):
            user["ultimo_nivel"] += 1 
        
        if int(self.nome[6]) == 0:
            user["pontuacao"] += pontuacao
        else:
            if int(self.nome[6]) > user["ultimo_nivel"] or int(user["ultimo_nivel"]) <= 2:
                user["pontuacao"] += pontuacao
    
            
        print("prr",user)

        save_user(user["nome"],None,None,None,None,None,None,None,None,None,None,user["ultimo_nivel"],user["pontuacao"])

        from carregar_jogo import carregar_jogo
        carregar_jogo(self.jogador.nome)

    def perdeu(self):
        estatua = Statue(self.jogador.nome,self.jogador.posicao_atual)
        pontuacao = self.jogador.nota * 30 + self.jogador.tempo_restante * 10
        user = read_user(self.jogador.nome)

        user["pontuacao"] -= pontuacao
        user[self.nome] = estatua
        save_user(user["nome"],user["nivel_1"],user["nivel_2"],user["nivel_3"],user["nivel_4"],user["nivel_5"],\
                  user["nivel_6"],user["nivel_7"],user["nivel_8"],user["nivel_9"],user["nivel_10"],user["ultimo_nivel"],user["pontuacao"])
        
        from carregar_jogo import carregar_jogo
        carregar_jogo(self.jogador.nome)


    def popup_insuficiente(self):
        largura,altura = 400,300
        x_popup = (LARGURA_JANELA - largura) // 2
        y_popup = (ALTURA_JANELA - altura) // 2

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
        TELA.fill(PRETO)
        pygame.draw.rect(TELA, LARANJA, (x_popup, y_popup, largura, altura))
        pygame.draw.rect(TELA, BRANCO, (x_popup, y_popup, largura, altura), 5)
        fonte = pygame.font.SysFont(None, 36)
        
        texto = fonte.render("Nota Insufuciente!", True, BRANCO)

        totais_rect = texto.get_rect(center=(x_popup + largura // 2, y_popup + 110))
        TELA.blit(texto, totais_rect)

        pygame.display.flip()

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
                self.popup_final(True)
                self.venceu()
                pygame.quit()
                quit()
            else:
                self.popup_insuficiente()
        
        for professor in self.professores:
            if abs(self.jogador.posicao_atual[0] - professor.position[0]) + abs(self.jogador.posicao_atual[1] - professor.position[1]) <= 1:
                pergunta = professor.ask(self.nome)
                if self.popup_pergunta(pergunta):
                    self.jogador.nota += 1
                    self.professores.remove(professor)
                else:
                    self.jogador.nota -= 1

        if self.estatua:
            if self.jogador.posicao_atual == self.estatua.position:
                pergunta = self.estatua.ask(self.nome)
                if self.popup_pergunta(pergunta):
                    self.jogador.nota += 1
                    self.jogador.tempo_restante += 3
                    self.estatua = None
                else:
                    self.estatua = None
                    self.jogador.tempo_restante -= 3


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






