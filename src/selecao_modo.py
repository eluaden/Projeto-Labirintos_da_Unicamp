import pygame
from novo_jogo import novo_jogo

# Inicialização do Pygame
pygame.init()

# Defina as dimensões da janela
LARGURA_JANELA, ALTURA_JANELA = 1200, 700

# Defina a posição inicial da janela
POS_X, POS_Y = 100, 50  # Exemplo de posição (100 pixels à direita, 50 pixels abaixo do canto superior esquerdo)

# Crie a tela do Pygame com posição inicial definida
TELA = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA), 0, 32)
pygame.display.set_caption('Tela Inicial')


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

# Textos
titulo = fonte_titulo.render('Modo de jogo', True, cor_titulo)

# Posições dos textos e botões
largura_titulo, altura_titulo = fonte_titulo.size('Modo de jogo')
posicao_titulo = ((LARGURA_JANELA - largura_titulo) // 2, ALTURA_JANELA // 7 - altura_titulo // 2)

# Dimensões dos botões
largura_botao = 380
altura_botao = 380
margem_entre_botoes = 60

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

def modo_historia():
    novo_jogo('historia')

def modo_recorde():
    novo_jogo('recorde')
      
# Loop principal
def selecao_de_modo():

    rodando = True

    while rodando:
        # Preencher o fundo com a cor preta
        TELA.fill((0, 0, 0))

        # Desenhar texto do título
        TELA.blit(titulo, posicao_titulo)

        # Verificar hover e desenhar botões do menu com a cor adequada
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        posicao_opcao_modo_historia = (LARGURA_JANELA//4 + 75, ALTURA_JANELA * 5 // 8 - 30)
        posicao_opcao_modo_recorde = (LARGURA_JANELA//4 + largura_botao + margem_entre_botoes + 75,ALTURA_JANELA * 5 // 8 - 30)
        
        botao_historia = desenhar_botao('historia', posicao_opcao_modo_historia, hover=posicao_opcao_modo_historia[0] - largura_botao // 2 <= mouse_x <= posicao_opcao_modo_historia[0] + largura_botao // 2 and posicao_opcao_modo_historia[1] - altura_botao // 2 <= mouse_y <= posicao_opcao_modo_historia[1] + altura_botao // 2)
        botao_recorde = desenhar_botao('recorde', posicao_opcao_modo_recorde, hover=posicao_opcao_modo_recorde[0] - largura_botao // 2 <= mouse_x <= posicao_opcao_modo_recorde[0] + largura_botao // 2 and posicao_opcao_modo_recorde[1] - altura_botao // 2 <= mouse_y <= posicao_opcao_modo_recorde[1] + altura_botao // 2)
      

        # Verificar cliques nos botões
        if botao_historia.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            modo_historia()
            rodando = False  # Fecha o menu principal ao abrir o novo jogo

        if botao_recorde.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            print('recorde')
            modo_recorde()
            rodando = False  # Fecha o menu principal ao abrir o novo jogo


        # Atualizar a tela
        pygame.display.flip()

        # Verificar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

    # Liberar recursos
    pygame.quit()

if __name__ == "__main__":
    selecao_de_modo()


