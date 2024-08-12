import pygame
import pygame.freetype
import os
from save import *
from carregar_jogo import carregar_jogo
from nivel_extra import nivel_extra

caminho_fonte = 'assets/ARCADE_N.TTF'

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da janela
LARGURA_JANELA, ALTURA_JANELA = 1200, 700

# Defina a posição inicial da janela
POS_X, POS_Y = 100, 50  # Exemplo de posição (100 pixels à direita, 50 pixels abaixo do canto superior esquerdo)

# Crie a tela do Pygame com posição inicial definida
TELA = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA), 0, 32)
pygame.display.set_caption('Novo Jogo')

# Inicialize o mixer
pygame.mixer.init()

# Carregue e toque a música de fundo
pygame.mixer.music.load('assets/musica_inicial.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.3)

# Cores
WHITE = (0, 0, 0)
BLACK = (2, 0, 12)
GRAY = (248, 246, 246)
DARK_GRAY = (133, 133, 133)
ORANGE = (245, 189, 73)

# Fonte
pygame.font.init()
FONT_TITULO = pygame.font.Font(caminho_fonte, 25)
FONT = FONT_TITULO.render('Nome do jogador', True, ORANGE)
FONT_BOTTON = pygame.freetype.SysFont("Arial", 20, True)
SMALL_FONT = pygame.freetype.SysFont("Arial", 20)

# Classe para o campo de entrada de texto
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        """
        Inicializa a caixa de entrada.

        Args:
            x (int): Coordenada x da caixa de entrada.
            y (int): Coordenada y da caixa de entrada.
            w (int): Largura da caixa de entrada.
            h (int): Altura da caixa de entrada.
            text (str): Texto inicial na caixa de entrada.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface, _ = SMALL_FONT.render(self.text, GRAY)
        self.active = False
        self.offset = 0

    def handle_event(self, event):
        """
        Lida com eventos do Pygame relacionados à caixa de entrada.
        Para saber se a caixa está ativa, e assim capturar o que vai ser escrito
        Args:
            event (pygame.event.Event): Evento do Pygame.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = ORANGE if self.active else GRAY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface, _ = SMALL_FONT.render(self.text[self.offset:], GRAY)
                # Verifica se o texto excede a largura da caixa
                while self.txt_surface.get_width() > self.rect.w - 10:
                    self.offset += 1
                    self.txt_surface, _ = SMALL_FONT.render(self.text[self.offset:], GRAY)

    def update(self):
        """
        Atualiza o estado da caixa de entrada. (Atualmente vazio)
        """
        pass

    def draw(self, screen):
        """
        Desenha a caixa de entrada na tela.

        Args:
            screen (pygame.Surface): Superfície onde a caixa de entrada será desenhada.
        """
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Função para desenhar o botão
def desenhar_botao(screen, text, rect, color):
    """
    Desenha um botão na tela.

    Args:
        screen (pygame.Surface): Superfície onde o botão será desenhado.
        text (str): Texto do botão.
        rect (pygame.Rect): Retângulo do botão.
        color (tuple): Cor do botão.
    """
    pygame.draw.rect(screen, color, rect)
    txt_surface, _ = FONT_BOTTON.render(text, WHITE)
    screen.blit(txt_surface, (rect.x + (rect.width - txt_surface.get_width()) // 2, rect.y + (rect.height - txt_surface.get_height()) // 2))

# Definindo posições e tamanho do box e do botão
input_box = InputBox(475, 280, 250, 30)
button_rect = pygame.Rect(550, 350, 100, 40)
button_color = GRAY

# Função principal
def novo_jogo(modo : str = "historia"):
    """
    Função principal que inicializa e executa o loop do jogo.
    """
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            input_box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print(f"Nome do jogador: {input_box.text}")

                    if not read_user(input_box.text):
                        save_user(input_box.text, None, None, None, None, None, None, None, None, None, None, 1, 0)
                    if modo == "historia":
                        carregar_jogo(input_box.text)
                    else:
                        nivel_extra(input_box.text)

        # Efeito de hover no botão
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            current_button_color = ORANGE
        else:
            current_button_color = GRAY

        input_box.update()

        TELA.fill(BLACK)
        TELA.blit(FONT, (430, 200))

        input_box.draw(TELA)
        desenhar_botao(TELA, "Enviar", button_rect, current_button_color)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    novo_jogo()
