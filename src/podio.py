import pygame
import sys
from save import read_all_users
from main import main  # Importar a função principal da tela inicial

# Inicializa o Pygame
pygame.init()

# Dimensões da janela
LARGURA_JANELA, ALTURA_JANELA = 1200, 700

# Configurações de tela
screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Classificação")

# Cores
black = (217, 220, 214)
white = (0, 0, 0)
gold = (255, 215, 0)
silver = (192, 192, 192)
bronze = (205, 127, 50)
laranja = (255, 165, 0)

# Fonte
title_font = pygame.font.SysFont('Arial', 50)
header_font = pygame.font.SysFont('Arial', 40)
default_font = pygame.font.SysFont('Arial', 30)
highlight_font = pygame.font.SysFont('Arial', 35)

# Cores dos botões
cor_botao_normal = (11, 32, 39)
cor_botao_hover = (7, 19, 24)

fonte_botao = pygame.font.Font('assets/ARCADE_N.TTF', 30)

cor_texto_normal = (217, 220, 214)  # Branco

# Função para desenhar o texto centralizado
def draw_text(text, font, color, surface, x, y):
    """
    Desenha o texto centralizado na superfície especificada.

    Args:
        text (str): Texto a ser desenhado.
        font (pygame.font.Font): Fonte do texto.
        color (tuple): Cor do texto.
        surface (pygame.Surface): Superfície onde o texto será desenhado.
        x (int): Coordenada x do centro do texto.
        y (int): Coordenada y do centro do texto.
    """
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Função para desenhar o botão
def desenhar_botao(tela, texto, posicao, hover=False):
    """
    Desenha um botão na tela com efeito de hover.

    Args:
        tela (pygame.Surface): Superfície onde o botão será desenhado.
        texto (str): Texto do botão.
        posicao (tuple): Coordenadas x, y do centro do botão.
        hover (bool): Indica se o efeito de hover está ativo.
    
    Returns:
        pygame.Rect: Retângulo do botão.
    """
    largura_botao = 50
    altura_botao = 50
    cor_botao = cor_botao_hover if hover else cor_botao_normal
    botao_rect = pygame.Rect(0, 0, largura_botao, altura_botao)
    botao_rect.center = posicao
    pygame.draw.rect(tela, cor_botao, botao_rect, border_radius=10)
    texto_renderizado = fonte_botao.render(texto, True, cor_texto_normal)
    texto_rect = texto_renderizado.get_rect(center=botao_rect.center)
    tela.blit(texto_renderizado, texto_rect)
    return botao_rect

# Função principal da tela de classificação
def classificacao():
    """
    Exibe a tela de classificação dos jogadores.
    """
    players_scores = read_all_users()
    print("podio", players_scores)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fundo branco
        screen.fill(white)

        # Título
        draw_text('Classificação', title_font, black, screen, screen_width // 2, 50)

        # Ordenar jogadores por pontuação (decrescente)
        sorted_players = sorted(players_scores.items(), key=lambda item: item[1], reverse=True)

        # Hover no botão
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_voltar = desenhar_botao(screen, 'X', (100, ALTURA_JANELA // 8 // 2), hover=False)
        if botao_voltar.collidepoint(mouse_x, mouse_y):
            botao_voltar = desenhar_botao(screen, 'X', (100, ALTURA_JANELA // 8 // 2), hover=True)
            if pygame.mouse.get_pressed()[0]:
                running = False
                main()

        # Desenhar a tabela de classificação
        y_offset = 150
        for i, (player, score) in enumerate(sorted_players):
            if i == 0:
                draw_text(f"{i + 1}. {player}: {score}", highlight_font, gold, screen, screen_width // 2, y_offset)
            elif i == 1:
                draw_text(f"{i + 1}. {player}: {score}", highlight_font, silver, screen, screen_width // 2, y_offset)
            elif i == 2:
                draw_text(f"{i + 1}. {player}: {score}", highlight_font, bronze, screen, screen_width // 2, y_offset)
            else:
                draw_text(f"{i + 1}. {player}: {score}", default_font, black, screen, screen_width // 2, y_offset)
            y_offset += 50

        # Atualizar a tela
        pygame.display.flip()
