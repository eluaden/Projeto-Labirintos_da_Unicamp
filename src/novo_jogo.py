import pygame
import pygame.freetype
import os
from save import *
from level import Level

# Inicialize o Pygame
pygame.init()

# Obtenha as dimensões da tela do sistema
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Defina as dimensões da janela
LARGURA_JANELA, ALTURA_JANELA = 1200, 700

# Calcule a posição para centralizar a janela
pos_x = (screen_width - LARGURA_JANELA) // 2
pos_y = (screen_height - ALTURA_JANELA) // 2

# Defina a posição da janela
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{pos_x},{pos_y}"
print(f"SDL_VIDEO_WINDOW_POS = {os.environ['SDL_VIDEO_WINDOW_POS']}")

# Dimensões da tela
TELA = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption('Novo Jogo')

# Inicialize o mixer
pygame.mixer.init()

# Carregue e toque a música de fundo
pygame.mixer.music.load('assets/musica_inicial.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.3)

# Cores
WHITE = (0,0,0)
BLACK = (2, 0, 12)
GRAY = (248, 246, 246)
DARK_GRAY = (133, 133, 133)
ORANGE = (245, 189, 73)

# Fonte
pygame.font.init()
FONT = pygame.freetype.SysFont("Arial", 35, True)
FONT_BOTTON = pygame.freetype.SysFont("Arial", 20, True)
SMALL_FONT = pygame.freetype.SysFont("Arial", 20)

# Classe para o campo de entrada de texto
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface, _ = SMALL_FONT.render(self.text, GRAY)
        self.active = False
        self.offset = 0

    def handle_event(self, event):
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
        pass

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Função para desenhar o botão
def desenhar_botao(screen, text, rect, color):
    pygame.draw.rect(screen, color, rect)
    txt_surface, _ = FONT_BOTTON.render(text, WHITE)
    screen.blit(txt_surface, (rect.x + (rect.width - txt_surface.get_width()) // 2, rect.y + (rect.height - txt_surface.get_height()) // 2))

input_box = InputBox(475, 280, 250, 30)
button_rect = pygame.Rect(550, 350, 100, 40)
button_color = GRAY

def novo_jogo():
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
                    # Lógica após clicar no botão
                    save_user(input_box.text,None,None,None,None,None,None,None,None,None,None,1, 0)
                    level_1 = read_level_base("level_10")
                    pygame.mixer.music.pause() 
                    jogo = Level("level_10",level_1["maze"],level_1["items"],level_1["enemies"],level_1["time"],level_1["media"])
                    jogo.jogar()

        # Efeito de hover no botão
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            current_button_color = ORANGE
        else:
            current_button_color = GRAY

        input_box.update()

        TELA.fill(BLACK)
        FONT.render_to(TELA, (460, 200), "Nome do jogador", ORANGE)
        input_box.draw(TELA)
        desenhar_botao(TELA, "Enviar", button_rect, current_button_color)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()



