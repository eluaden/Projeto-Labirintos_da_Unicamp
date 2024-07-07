import pygame
# Inicialização do Pygame
pygame.init()

# Defina as dimensões da janela
LARGURA_JANELA, ALTURA_JANELA = 1200, 700

# Caminho para o arquivo de fonte
caminho_fonte = 'assets/ARCADE_N.TTF'

# Fontes e cores
fonte_titulo = pygame.font.Font(caminho_fonte, 50)
fonte_texto = pygame.font.Font(None, 24)
fonte_botao = pygame.font.Font(caminho_fonte, 30)

cor_texto_normal = (217, 220, 214)  # Branco
cor_texto_hover = (245, 189, 73)   # Vermelho para o hover
cor_fundo_texto = (2, 0, 12)         # Preto
cor_titulo = (245, 189, 73)

# Cores dos botões
cor_botao_normal = (11, 32, 39)
cor_botao_hover = (7, 19, 24)

# Texto das informações
texto_informacoes = (
    """
    "Os Labirintos da Unicamp" é um jogo desenvolvido em Python, inspirado no jogo "Laberinto del Saber". O objetivo do jogador é completar 
    diferentes labirintos, coletar pontos e interagir com professores dentro de um tempo limite. O jogador deve acumular NOTA suficiente para 
    avançar para o próximo labirinto, enquanto deve responder as perguntas dos professores que se movimentam pelo labirinto. O jogo possui 
    vários níveis e funcionalidades, incluindo salvamento e carregamento, tabela de pontuação, Nível extra(que é ilimitado) e muito mais."""
    '\nRegras:\n'
    '- Obter pontos através de perguntas de professores, e livros\n'
    '- Utilizar desses pontos pra passar de ano(Férias)\n'
    '- Usar as bombas para explodir paredes\n'
    '- Fazer tudo isso sem o tempo estourar!\n\n'
    'Todas as artes do jogo, ou pelo menos a maioria foi feita por nós,'
    'incluindo também a musica.\n'
    'Gostariamos de agradecer ao professor e aos peds pelo ótimo semestre.\n'
    'Enjoy the GAME!\n'
    'Assinado: Rafael Feltrin 276246 e Lucas Guimarães 195948'
)

# Função para desenhar botões
def desenhar_botao(tela, texto, posicao, hover=False):
    """Função principal que desenha o botão na tela"""
    largura_botao = 50
    altura_botao = 50
    if hover:
        cor_botao = cor_botao_hover
    else:
        cor_botao = cor_botao_normal
    
    botao_rect = pygame.Rect(0, 0, largura_botao, altura_botao)
    botao_rect.center = posicao
    pygame.draw.rect(tela, cor_botao, botao_rect, border_radius=10)
    texto_renderizado = fonte_botao.render(texto, True, cor_texto_normal)
    texto_rect = texto_renderizado.get_rect(center=botao_rect.center)
    tela.blit(texto_renderizado, texto_rect)
    return botao_rect

def informacoes():
    """Função princial da tela de informações"""
    tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
    pygame.display.set_caption('Informações')
    
    # Título
    titulo = fonte_titulo.render('Informacoes', True, cor_titulo)
    largura_titulo, altura_titulo = titulo.get_size()
    posicao_titulo = ((LARGURA_JANELA - largura_titulo) // 2, ALTURA_JANELA // 8 - altura_titulo // 2)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        tela.fill(cor_fundo_texto)
        
        # Desenhar o título
        tela.blit(titulo, posicao_titulo)
        
        # Desenhar o texto das informações
        linhas = texto_informacoes.split('\n')
        for i, linha in enumerate(linhas):
            linha_renderizada = fonte_texto.render(linha, True, cor_texto_normal)
            tela.blit(linha_renderizada, (50, 150 + i * 35))
        
        # Desenhar botão Voltar
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_voltar = desenhar_botao(tela, 'X', (100, ALTURA_JANELA // 8 - altura_titulo // 2), hover=False)
        if botao_voltar.collidepoint(mouse_x, mouse_y):
            botao_voltar = desenhar_botao(tela, 'X', (100, ALTURA_JANELA // 8 - altura_titulo // 2), hover=True)
            if pygame.mouse.get_pressed()[0]:
                rodando = False
                from main import main
                main()
                

        pygame.display.flip()

if __name__ == "__main__":
    informacoes()
