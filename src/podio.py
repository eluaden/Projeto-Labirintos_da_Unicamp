import pygame
import sys
from save import *
# Inicializa o Pygame
pygame.init()

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

#botao
botao_retornar_rect = pygame.Rect(50, 50, 200, 100)

# Dados dos jogadores (exemplo)


# Função para desenhar o texto centralizado
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)



# Loop principal
def classificacao():

    players_scores = read_all_users()
    print("podio",players_scores)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_retornar_rect.collidepoint(event.pos):
                    from tela_inicial import main
                    main()
                    break

        # Fundo branco
        screen.fill(white)

        # Título
        draw_text('Classificação', title_font, black, screen, screen_width // 2, 50)

        # Ordenar jogadores por pontuação (decrescente)
        sorted_players = sorted(players_scores.items(), key=lambda item: item[1], reverse=True)


        #hover no botao
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if botao_retornar_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, laranja, botao_retornar_rect, 2)
            cor_botao_retornar = laranja
            
        else:
            pygame.draw.rect(screen, black, botao_retornar_rect, 1)
            cor_botao_retornar =  black
                #desenhar botao de retornar

        pygame.draw.rect(screen, white, botao_retornar_rect)
        txt_surface = default_font.render('Retornar', True, cor_botao_retornar)
        screen.blit(txt_surface, (botao_retornar_rect.x + (botao_retornar_rect.width - txt_surface.get_width()) // 2, botao_retornar_rect.y + (botao_retornar_rect.height - txt_surface.get_height()) // 2))


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


