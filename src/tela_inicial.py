import pygame
import cv2
import os
from novo_jogo import novo_jogo
from informacoes import informacoes
# Inicialização do Pygame
pygame.init()

# Defina as dimensões da janela
LARGURA_JANELA, ALTURA_JANELA = 1200, 700

# Defina a posição inicial da janela
POS_X, POS_Y = 100, 50  # Exemplo de posição (100 pixels à direita, 50 pixels abaixo do canto superior esquerdo)

# Crie a tela do Pygame com posição inicial definida
TELA = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA), 0, 32)
pygame.display.set_caption('Tela Inicial')

# Inicialize o mixer
pygame.mixer.init()

# Carregue e toque a música de fundo
pygame.mixer.music.load('assets/musica_inicial.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.3)

# Carregar o vídeo com OpenCV
video = cv2.VideoCapture('assets/video_labirinto6.mp4')

# Caminho para o arquivo de fonte
caminho_fonte = 'assets/ARCADE_N.TTF'

# Fontes e cores
fonte_titulo = pygame.font.Font(caminho_fonte, 70)
fonte_opcoes = pygame.font.Font(caminho_fonte, 30)
cor_texto_normal = (217, 220, 214)  # Branco
cor_texto_hover = (245, 189, 73)   # Vermelho para o hover
cor_fundo_texto = (0, 0, 0)         # Preto
cor_titulo = (245, 189, 73)

# Cores dos botões
cor_botao_normal = (11, 32, 39)
cor_botao_hover = (7, 19, 24)

"""
antes
# Cores dos botões
cor_botao_normal = (0, 41, 168)
cor_botao_hover = (0, 30, 122)
"""

# Textos
titulo = fonte_titulo.render('O Labirinto', True, cor_titulo)

# Posições dos textos e botões
largura_titulo, altura_titulo = fonte_titulo.size('O Labirinto')
posicao_titulo = ((LARGURA_JANELA - largura_titulo) // 2, ALTURA_JANELA // 4 - altura_titulo // 2)

# Dimensões dos botões
largura_botao = 380
altura_botao = 70
margem_entre_botoes = 30

# Função para desenhar botões
def desenhar_botao(texto, posicao, hover=False):
    if hover:
        cor_botao = cor_botao_hover
        cor_texto = cor_texto_hover
    else:
        cor_botao = cor_botao_normal
        cor_texto = cor_texto_normal
    
    botao_rect = pygame.Rect(0, 0, largura_botao, altura_botao)
    botao_rect.center = posicao
    pygame.draw.rect(TELA, cor_botao, botao_rect, border_radius=10)
    texto_renderizado = fonte_opcoes.render(texto, True, cor_texto_normal)
    texto_rect = texto_renderizado.get_rect(center=botao_rect.center)
    TELA.blit(texto_renderizado, texto_rect)
    return botao_rect

# Funções de callback para os botões
def abrir_novo_jogo():
    novo_jogo()

def podio():
    from podio import classificacao
    classificacao()

def abrir_informacoes():
    informacoes()

"""
def tela_infos():
    texto = 'O Labirinto é um jogo educativo desenvolvido por alunos\ndo curso de Ciência de Computação da Universidade Estadual de Campinas,\npara o projeto 3 da disciplina de algoritimos e programação de computadores. \nSim, acabamos de entrar na faculdade e ja estamos fazendo um JOGO!!\nRegras: \n-Obter pontos através de perguntas de professores, e livros\n-Utilizar desses pontos pra passar de ano(Férias)\n-Usar as bombas para explodir paredes\n-Fazer tudo isso sem o tempo estourar!\n \nTodas as artes do jogo, ou pelo menos a maioria foi feita por nós,\n incluindo também a musica.\n Gostariamos de agradecer ao professor e aos peds pelo ótimo semestre. \n(E ao chat GPT por ensinar pygames do zero pra gente).\n Enjoy the GAME! \n Assinado: Rafael Feltrin () e Lucas Guimarães 195948'

    botao_voltar = fonte_opcoes.render('Voltar', True, cor_texto_normal)
    botao_voltar_rect = botao_voltar.get_rect(center=(LARGURA_JANELA // 2, ALTURA_JANELA * 9 // 10))
    
    cor_rect = cor_texto_normal
    while True:
        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if botao_voltar_rect.collidepoint(mouse_x, mouse_y):
                cor_rect = cor_texto_hover
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            else:
                cor_rect = cor_texto_normal
                   
        TELA.fill(cor_fundo_texto)
  
        # Quebrando texto
        lines = texto.split('\n')
        for i, line in enumerate(lines):
            line = fonte_opcoes.render(line, True, cor_texto_normal)
            line_rect = line.get_rect(center=(LARGURA_JANELA // 2, ALTURA_JANELA // 15 + i * 35))
            TELA.blit(line, line_rect)

        botao_voltar = fonte_opcoes.render('Voltar', True, cor_fundo_texto)
        pygame.draw.rect(TELA, cor_rect, botao_voltar_rect)
        TELA.blit(botao_voltar, botao_voltar_rect)
        pygame.display.flip()
"""
        
# Loop principal
def main():
    video = cv2.VideoCapture('assets/video_labirinto6.mp4')
    rodando = True
    ultimo_frame = None  # Para armazenar o último frame do vídeo
    while rodando:
        ret, frame = video.read()
        if not ret:
            video.release()
            video = cv2.VideoCapture('assets/video_labirinto6.mp4')  # Reinicia o vídeo ao chegar ao fim
            continue

        # Redimensionar o quadro do vídeo para as dimensões da tela
        frame = cv2.resize(frame, (LARGURA_JANELA, ALTURA_JANELA))

        # Converter de BGR para RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Converter para formato do pygame
        frame_pygame = pygame.image.frombuffer(frame_rgb.flatten(), (LARGURA_JANELA, ALTURA_JANELA), 'RGB')

        # Desenhar o vídeo como fundo da tela
        TELA.blit(frame_pygame, (0, 0))

        # Salvar o último frame para exibir quando o vídeo terminar
        ultimo_frame = frame_pygame

        # Desenhar texto do título
        TELA.blit(titulo, posicao_titulo)

        # Verificar hover e desenhar botões do menu com a cor adequada
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        posicao_opcao_novo_jogo = (LARGURA_JANELA // 2, ALTURA_JANELA * 3 // 4 - altura_botao - margem_entre_botoes)
        posicao_opcao_podio = (LARGURA_JANELA // 2, ALTURA_JANELA * 3 // 4)
        posicao_opcao_informacoes = (LARGURA_JANELA // 2, ALTURA_JANELA * 3 // 4 + altura_botao + margem_entre_botoes)
        
        botao_novo_jogo = desenhar_botao('Jogar', posicao_opcao_novo_jogo, hover=posicao_opcao_novo_jogo[0] - largura_botao // 2 <= mouse_x <= posicao_opcao_novo_jogo[0] + largura_botao // 2 and posicao_opcao_novo_jogo[1] - altura_botao // 2 <= mouse_y <= posicao_opcao_novo_jogo[1] + altura_botao // 2)
        botao_podio = desenhar_botao('Podio', posicao_opcao_podio, hover=posicao_opcao_podio[0] - largura_botao // 2 <= mouse_x <= posicao_opcao_podio[0] + largura_botao // 2 and posicao_opcao_podio[1] - altura_botao // 2 <= mouse_y <= posicao_opcao_podio[1] + altura_botao // 2)
        botao_informacoes = desenhar_botao('Informacoes', posicao_opcao_informacoes, hover=posicao_opcao_informacoes[0] - largura_botao // 2 <= mouse_x <= posicao_opcao_informacoes[0] + largura_botao // 2 and posicao_opcao_informacoes[1] - altura_botao // 2 <= mouse_y <= posicao_opcao_informacoes[1] + altura_botao // 2)

        # Verificar cliques nos botões
        if botao_novo_jogo.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            abrir_novo_jogo()
            rodando = False  # Fecha o menu principal ao abrir o novo jogo

        if botao_podio.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            podio()
            rodando = False  # Fecha o menu principal ao abrir o novo jogo

        if botao_informacoes.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            abrir_informacoes()
            rodando = False

        # Atualizar a tela
        pygame.display.flip()

        # Verificar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

    # Desenhar o último frame do vídeo após ele terminar
    if ultimo_frame is not None:
        TELA.blit(ultimo_frame, (0, 0))
        pygame.display.flip()

    # Liberar recursos
    pygame.quit()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()




