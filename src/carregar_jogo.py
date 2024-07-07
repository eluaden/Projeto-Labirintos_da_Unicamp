import pygame
import os
from save import *
from level import Level
from nivel_extra import nivel_extra

# Configurações do Pygame
pygame.init()
LARGURA_JANELA, ALTURA_JANELA = 1200, 700
TELA = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption('Tela de Seleção de Fases')

# Cores
COR_FUNDO = (2, 0, 12)  # Preto
"""
COR_QUADRADO = (217, 220, 214)  # Cinza para quadrados
COR_QUADRADO_HOVER = (245, 189, 73)  # Cinza claro para hover
"""
COR_QUADRADO = (255, 254, 227) # Cinza para quadrados
COR_QUADRADO_HOVER = (245, 189, 73)  # Cinza claro para hover

COR_TITULO = (245, 189, 73)  # Branco para o título

# Dimensões e posição dos quadrados
NUMERO_COLUNAS = 5
NUMERO_LINHAS = 2
TAMANHO_QUADRADO = 100
ESPACO_ENTRE_QUADRADOS = 20
margem_esquerda = (LARGURA_JANELA - (NUMERO_COLUNAS * (TAMANHO_QUADRADO + ESPACO_ENTRE_QUADRADOS))) // 2
margem_topo = (ALTURA_JANELA - (NUMERO_LINHAS * (TAMANHO_QUADRADO + ESPACO_ENTRE_QUADRADOS))) // 2

# Carregar imagem do cadeado com transparência
cadeado_img = pygame.image.load(os.path.join('assets/', 'cadeado.png')).convert_alpha()
# Redimensionar a imagem usando interpolação suave
cadeado_img = pygame.transform.smoothscale(cadeado_img, (TAMANHO_QUADRADO - 40, TAMANHO_QUADRADO - 40))

FONT_BOTTON = pygame.freetype.SysFont("Arial", 20, True)

caminho_fonte = 'assets/ARCADE_N.TTF'

FONT_TITULO = pygame.font.Font(caminho_fonte, 35)
# Função para desenhar os quadrados na tela
def desenhar_tela(nome_usuario):
    TELA.fill(COR_FUNDO)
    
    # Desenhar título
    fonte_titulo = pygame.font.SysFont(None, 60)
    titulo = FONT_TITULO.render('Escolha uma Fase', True, COR_TITULO)
    largura_titulo, altura_titulo = fonte_titulo.size('Escolha uma Fase')
    posicao_titulo = (((LARGURA_JANELA - largura_titulo) // 2) - 100 , margem_topo // 2 - altura_titulo // 2)
    TELA.blit(titulo, posicao_titulo)
    
    for linha in range(NUMERO_LINHAS):
        for coluna in range(NUMERO_COLUNAS):
            x = margem_esquerda + coluna * (TAMANHO_QUADRADO + ESPACO_ENTRE_QUADRADOS)
            y = margem_topo + linha * (TAMANHO_QUADRADO + ESPACO_ENTRE_QUADRADOS)
            rect = pygame.Rect(x, y, TAMANHO_QUADRADO, TAMANHO_QUADRADO)
            cor = COR_QUADRADO_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else COR_QUADRADO
            pygame.draw.rect(TELA, cor, rect)
            # Exemplo: número da fase ou cadeado (simbolizado por um retângulo preto)
            fase = linha * NUMERO_COLUNAS + coluna + 1
            if fase <= read_user(nome_usuario)['ultimo_nivel']:  # Exemplo: Liberar as 5 primeiras fases
                texto = pygame.font.SysFont(None, 36).render(str(fase), True, (0, 0, 0))
                largura_texto, altura_texto = texto.get_size()
                TELA.blit(texto, (x + (TAMANHO_QUADRADO - largura_texto) // 2, y + (TAMANHO_QUADRADO - altura_texto) // 2))
            else:
                TELA.blit(cadeado_img, (x + 20, y + 20))  # Desenhar cadeado sobre quadrados não liberados

# Loop principal

# Função para desenhar o botão
def desenhar_botao(screen, text, rect, color):
    pygame.draw.rect(screen, color, rect)
    txt_surface, _ = FONT_BOTTON.render(text, (0,0,0))
    screen.blit(txt_surface, (rect.x + (rect.width - txt_surface.get_width()) // 2, rect.y + (rect.height - txt_surface.get_height()) // 2))

retornar_button_rect = pygame.Rect(50, 600, 120, 40)
nivel_extra_button_rect = pygame.Rect(1030, 600, 120, 40)


def carregar_jogo(nome_usuario):
    rodando = True

    usuario = read_user(nome_usuario)
    fase = usuario['ultimo_nivel']
    print(nome_usuario)
    print(usuario)
    
    print(f"fase: {fase}")
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                for linha in range(NUMERO_LINHAS):
                    for coluna in range(NUMERO_COLUNAS):
                        x_quad = margem_esquerda + coluna * (TAMANHO_QUADRADO + ESPACO_ENTRE_QUADRADOS)
                        y_quad = margem_topo + linha * (TAMANHO_QUADRADO + ESPACO_ENTRE_QUADRADOS)
                        rect = pygame.Rect(x_quad, y_quad, TAMANHO_QUADRADO, TAMANHO_QUADRADO)
                        if rect.collidepoint(x, y):
                            fase_selecionada = linha * NUMERO_COLUNAS + coluna + 1
                            print(f"Clicou na fase {fase_selecionada}")
                            # Implemente aqui a ação desejada ao clicar (abrir fase, mostrar informações, etc.)
                            if fase >= 1 and fase_selecionada == 1:
                                print('entrouuu')
                                level_1 = read_level_base("level_1")
                                jogo = Level("nivel_1",nome_usuario,level_1["maze"],level_1["items"],level_1["enemies"],level_1["time"],level_1["media"],usuario["nivel_1"])
                                jogo.jogar()
                            if fase >= 2 and fase_selecionada == 2:
                                print('entrouuu')
                                level_2 = read_level_base("level_2")
                                jogo = Level("nivel_2",nome_usuario,level_2["maze"],level_2["items"],level_2["enemies"],level_2["time"],level_2["media"],usuario["nivel_2"])
                                jogo.jogar()
                            if fase >= 3 and fase_selecionada == 3:
                                print('entrouuu')
                                level_3 = read_level_base("level_3")
                                jogo = Level("nivel_3",nome_usuario,level_3["maze"],level_3["items"],level_3["enemies"],level_3["time"],level_3["media"],usuario["nivel_3"])
                                jogo.jogar()
                            if fase >= 4 and fase_selecionada == 4:
                                print('entrouuu')
                                level_4 = read_level_base("level_4")
                                jogo = Level("nivel_4",nome_usuario,level_4["maze"],level_4["items"],level_4["enemies"],level_4["time"],level_4["media"],usuario["nivel_4"])
                                jogo.jogar()
                            if fase >= 5 and fase_selecionada == 5:
                                print('entrouuu')
                                level_5 = read_level_base("level_5")
                                jogo = Level("nivel_5",nome_usuario,level_5["maze"],level_5["items"],level_5["enemies"],level_5["time"],level_5["media"],usuario["nivel_5"])
                                jogo.jogar()
                            if fase >= 6 and fase_selecionada == 6:
                                print('entrouuu')
                                level_6 = read_level_base("level_6")
                                jogo = Level("nivel_6",nome_usuario,level_6["maze"],level_6["items"],level_6["enemies"],level_6["time"],level_6["media"],usuario["nivel_6"])
                                jogo.jogar()
                            if fase >= 7 and fase_selecionada == 7:
                                print('entrouuu')
                                level_7 = read_level_base("level_7")
                                jogo = Level("nivel_7",nome_usuario,level_7["maze"],level_7["items"],level_7["enemies"],level_7["time"],level_7["media"],usuario["nivel_7"])
                                jogo.jogar()
                            if fase >= 8 and fase_selecionada == 8:
                                print('entrouuu')
                                level_8 = read_level_base("level_8")
                                jogo = Level("nivel_8",nome_usuario,level_8["maze"],level_8["items"],level_8["enemies"],level_8["time"],level_8["media"],usuario["nivel_8"])
                                jogo.jogar()
                            if fase >= 9 and fase_selecionada == 9:
                                print('entrouuu')
                                level_9 = read_level_base("level_9")
                                jogo = Level("nivel_9",nome_usuario,level_9["maze"],level_9["items"],level_9["enemies"],level_9["time"],level_9["media"],usuario["nivel_9"])
                                jogo.jogar()
                            if fase >= 10 and fase_selecionada == 10:
                                print('entrouuu')
                                level_10 = read_level_base("level_10")
                                jogo = Level("nivel_10",nome_usuario,level_10["maze"],level_10["items"],level_10["enemies"],level_10["time"],level_10["media"],usuario["nivel_10"])
                                jogo.jogar()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if retornar_button_rect.collidepoint(evento.pos):
                    from main import main
                    main()
                    print(f"Nome do jogador")
                if nivel_extra_button_rect.collidepoint(evento.pos):
                    nivel_extra(nome_usuario,usuario)

        desenhar_tela(nome_usuario)

        # Efeito de hover no botão
        if retornar_button_rect.collidepoint(pygame.mouse.get_pos()):
            current_button_color = (245, 189, 73)
        else:
            current_button_color = (248, 246, 246)

        desenhar_botao(TELA, "Retornar", retornar_button_rect, current_button_color)
        #efeito de hover no botão nivel extra
        if nivel_extra_button_rect.collidepoint(pygame.mouse.get_pos()):
            current_button_color = (224, 169, 58)
        else:
            current_button_color = (245, 189, 73)

        desenhar_botao(TELA, "Nivel Extra", nivel_extra_button_rect, current_button_color)

        
        
        
        
        pygame.display.flip()

    # Finaliza o Pygame
    pygame.quit()


if __name__ == "__main__":
    carregar_jogo()


