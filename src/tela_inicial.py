import pygame
import cv2
import subprocess
import ctypes
# Inicialize o Pygame
pygame.init()

# Defina as dimensões da janela
LARGURA_JANELA, ALTURA_JANELA = 1200, 700

# Dimensões da tela
TELA = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption('Novo Jogo')

# Obtenha a resolução da tela
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

print(screen_width)
print(screen_height)

# Calcule a posição para centralizar a janela
pos_x = (screen_width - LARGURA_JANELA) // 2
pos_y = (screen_height - ALTURA_JANELA) // 2

# Use ctypes para mover a janela para a posição desejada
window = pygame.display.get_wm_info()['window']
ctypes.windll.user32.SetWindowPos(window, 0, pos_x, pos_y, 0, 0, 0x0001)

# Inicialize o mixer
pygame.mixer.init()

# Carregue e toque a música de fundo
pygame.mixer.music.load('assets/musica_inicial.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.3)

# Carregar o vídeo com OpenCV
video = cv2.VideoCapture('assets/video_labirinto6.mp4')

# Fontes e cores 141, 8, 1
fonte_titulo = pygame.font.Font(None, 80)
fonte_opcoes = pygame.font.Font(None, 36)
cor_texto_normal = (217, 220, 214)  # Branco
cor_texto_hover = (245, 189, 73)   # vermelho para o hover
cor_fundo_texto = (0, 0, 0)         # Preto
cor_titulo = (245, 189, 73)

# Textos
titulo = fonte_titulo.render('O Labirinto', True, cor_titulo)
opcao_novo_jogo = fonte_opcoes.render('Novo Jogo', True, cor_texto_normal)
opcao_carregar_jogo = fonte_opcoes.render('Carregar Jogo', True, cor_texto_normal)
opcao_informacoes = fonte_opcoes.render('Informações', True, cor_texto_normal)

# Posições dos textos
largura_titulo, altura_titulo = fonte_titulo.size('O Labirinto')
largura_opcoes, altura_opcoes = fonte_opcoes.size('Novo Jogo')

posicao_titulo = ((LARGURA_JANELA - largura_titulo) // 2, ALTURA_JANELA // 4 - altura_titulo // 2)
posicao_opcao_novo_jogo = ((LARGURA_JANELA - largura_opcoes) // 2, ALTURA_JANELA * 3 // 4 - altura_opcoes // 2)
posicao_opcao_carregar_jogo = ((LARGURA_JANELA - largura_opcoes) // 2, ALTURA_JANELA * 3 // 4 + 50 - altura_opcoes // 2)
posicao_opcao_informacoes = ((LARGURA_JANELA - largura_opcoes) // 2, ALTURA_JANELA * 3 // 4 + 100 - altura_opcoes // 2)

# Função para abrir um novo jogo
def abrir_novo_jogo():
    subprocess.Popen(['python', 'src/novo_jogo.py'])

def carregar_jogo():
    subprocess.Popen(['python', 'src/carregar_jogo.py'])

# Loop principal
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

    # Verificar hover e desenhar opções do menu com a cor adequada
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Verificar hover sobre "Novo Jogo"
    if posicao_opcao_novo_jogo[0] <= mouse_x <= posicao_opcao_novo_jogo[0] + largura_opcoes and \
       posicao_opcao_novo_jogo[1] <= mouse_y <= posicao_opcao_novo_jogo[1] + altura_opcoes:
        opcao_novo_jogo = fonte_opcoes.render('Novo Jogo', True, cor_texto_hover)
        if pygame.mouse.get_pressed()[0]:  # Verifica se clicou com o botão esquerdo do mouse
            abrir_novo_jogo()
            rodando = False  # Fecha o menu principal ao abrir o novo jogo
    else:
        opcao_novo_jogo = fonte_opcoes.render('Novo Jogo', True, cor_texto_normal)
    
    # Verificar hover sobre "Carregar Jogo"
    if posicao_opcao_carregar_jogo[0] <= mouse_x <= posicao_opcao_carregar_jogo[0] + largura_opcoes and \
       posicao_opcao_carregar_jogo[1] <= mouse_y <= posicao_opcao_carregar_jogo[1] + altura_opcoes:
        opcao_carregar_jogo = fonte_opcoes.render('Carregar Jogo', True, cor_texto_hover)
        if pygame.mouse.get_pressed()[0]:  # Verifica se clicou com o botão esquerdo do mouse
            carregar_jogo()
            rodando = False  # Fecha o menu principal ao abrir o novo jogo
    else:
        opcao_carregar_jogo = fonte_opcoes.render('Carregar Jogo', True, cor_texto_normal)
    
    # Verificar hover sobre "Informações"
    if posicao_opcao_informacoes[0] <= mouse_x <= posicao_opcao_informacoes[0] + largura_opcoes and \
       posicao_opcao_informacoes[1] <= mouse_y <= posicao_opcao_informacoes[1] + altura_opcoes:
        opcao_informacoes = fonte_opcoes.render('Informações', True, cor_texto_hover)
    else:
        opcao_informacoes = fonte_opcoes.render('Informações', True, cor_texto_normal)

    # Desenhar as opções do menu atualizadas
    TELA.blit(opcao_novo_jogo, posicao_opcao_novo_jogo)
    TELA.blit(opcao_carregar_jogo, posicao_opcao_carregar_jogo)
    TELA.blit(opcao_informacoes, posicao_opcao_informacoes)

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







