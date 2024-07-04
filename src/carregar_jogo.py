import pygame
import os

# Configurações do Pygame
pygame.init()
LARGURA_JANELA, ALTURA_JANELA = 1000, 700
TELA = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption('Tela de Seleção de Fases')

# Cores
COR_FUNDO = (50, 48, 49)  # Branco
COR_QUADRADO = (217, 220, 214)  # Cinza para quadrados
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
cadeado_img = pygame.image.load(os.path.join('animation-master/', 'cadeado.png')).convert_alpha()
# Redimensionar a imagem usando interpolação suave
cadeado_img = pygame.transform.smoothscale(cadeado_img, (TAMANHO_QUADRADO - 40, TAMANHO_QUADRADO - 40))

# Função para desenhar os quadrados na tela
def desenhar_tela():
    TELA.fill(COR_FUNDO)
    
    # Desenhar título
    fonte_titulo = pygame.font.SysFont(None, 60)
    titulo = fonte_titulo.render('Escolha uma Fase', True, COR_TITULO)
    largura_titulo, altura_titulo = fonte_titulo.size('Escolha uma Fase')
    posicao_titulo = ((LARGURA_JANELA - largura_titulo) // 2, margem_topo // 2 - altura_titulo // 2)
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
            if fase <= 3:  # Exemplo: Liberar as 5 primeiras fases
                texto = pygame.font.SysFont(None, 36).render(str(fase), True, (0, 0, 0))
                largura_texto, altura_texto = texto.get_size()
                TELA.blit(texto, (x + (TAMANHO_QUADRADO - largura_texto) // 2, y + (TAMANHO_QUADRADO - altura_texto) // 2))
            else:
                TELA.blit(cadeado_img, (x + 20, y + 20))  # Desenhar cadeado sobre quadrados não liberados

# Loop principal
rodando = True
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

    desenhar_tela()
    pygame.display.flip()

# Finaliza o Pygame
pygame.quit()



