import pygame.sprite

class Jogador(pygame.sprite.Sprite):
    
    def __init__(self, nome: str, nota: int, pontos_total: int, labirinto_atual, posicao_atual: list, tempo_restante: int):
        super().__init__()
        self._nome = nome
        self._nota = nota
        self._pontos_total = pontos_total
        self._inventario = {"bombas": []}
        self._labirinto_atual = labirinto_atual
        self._posicao_atual = posicao_atual.copy()
        self._tempo_restante = tempo_restante

        # Carregar o sprite sheet
        sprite_sheet = pygame.image.load('assets/teste7.png').convert_alpha()

        # Configurações de sprites
        self.SPRITE_WIDTH = sprite_sheet.get_width() // 3
        self.SPRITE_HEIGHT = sprite_sheet.get_height() // 4

        # Função para dividir o sprite sheet
        def load_sprites(sheet, num_frames, row):
            sprites = []
            for i in range(num_frames):
                frame = sheet.subsurface(pygame.Rect(i * self.SPRITE_WIDTH, row * self.SPRITE_HEIGHT, self.SPRITE_WIDTH, self.SPRITE_HEIGHT))
                sprites.append(frame)
            return sprites

        # Carregar os sprites para cada direção
        self.sprites_up = load_sprites(sprite_sheet, 3, 3)
        self.sprites_left = load_sprites(sprite_sheet, 3, 1)
        self.sprites_right = load_sprites(sprite_sheet, 3, 2)
        self.sprites_down = load_sprites(sprite_sheet, 3, 0)

        # Dicionário para armazenar as listas de sprites
        self.sprites = {
            'cima': self.sprites_up,
            'esquerda': self.sprites_left,
            'direita': self.sprites_right,
            'baixo': self.sprites_down
        }

        # Configurações iniciais
        self.direcao = 'baixo'
        self.animacao_index = 0
        self.image = self.sprites[self.direcao][self.animacao_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self._posicao_atual[0] * 40, self._posicao_atual[1] * 40)
        self.velocidade = 40  # Ajuste conforme a necessidade


    def mover(self, direcao):
        self.direcao = direcao
        x, y = self.posicao_atual

        # Determina a nova posição de destino com base na direção
        if direcao == 'esquerda':
            nova_posicao = [x - 1, y]
        elif direcao == 'direita':
            nova_posicao = [x + 1, y]
        elif direcao == 'cima':
            nova_posicao = [x, y - 1]
        elif direcao == 'baixo':
            nova_posicao = [x, y + 1]

        nova_pos_x, nova_pos_y = nova_posicao

        # Verifica se a nova posição está dentro dos limites do labirinto e não colide com uma parede
        if 0 <= nova_pos_x < len(self.labirinto_atual[0]) and 0 <= nova_pos_y < len(self.labirinto_atual):
            if self.labirinto_atual[nova_pos_y][nova_pos_x] != 1:
                # Atualiza a posição do jogador
                self.posicao_atual = nova_posicao

        print(self.direcao)
        # Atualiza a animação do sprite
        self.animacao_index = (self.animacao_index + 1) % len(self.sprites[self.direcao])
        self.image = self.sprites[self.direcao][self.animacao_index]

           
    @property
    def nome(self):
        return self._nome

    @property
    def nota(self):
        return self._nota

    @nota.setter
    def nota(self, value):
        if 0 <= value <= 10:
            self._nota = value
        else:
            print("Número inválido de nota. Deve estar entre 0 e 10.")
    
    @property
    def pontos_total(self):
        return self._pontos_total

    @pontos_total.setter
    def pontos_total(self, value):
        self._pontos_total = value
    
    @property
    def inventario(self):
        return self._inventario

    @inventario.setter
    def inventario(self, value):
        self._inventario = value
    
    @property
    def labirinto_atual(self):
        return self._labirinto_atual
    
    @labirinto_atual.setter
    def labirinto_atual(self, value):
        self.labirinto_atual = value

    @property
    def posicao_atual(self):
        return self._posicao_atual.copy()
    
    @posicao_atual.setter
    def posicao_atual(self, value):
        self._posicao_atual = value.copy()
        
    
    @property
    def tempo_restante(self):
        return self._tempo_restante

    @tempo_restante.setter
    def tempo_restante(self, value):
        self._tempo_restante = value    
        
    """
    def mover(self, direcao):
        x, y = self.posicao_atual
        nova_posicao = [x, y]

        if direcao == 'esquerda':
            nova_posicao = [x - 1, y]
        elif direcao == 'direita':
            nova_posicao = [x + 1, y]
        elif direcao == 'cima':
            nova_posicao = [x, y - 1]
        elif direcao == 'baixo':
            nova_posicao = [x, y + 1]

        # Verificar se a nova posição é válida no labirinto
        if self.labirinto_atual[nova_posicao[1]][nova_posicao[0]] != 1:
            self.posicao_atual = nova_posicao
    """             
                
    def aumentar_vida(self):
        if self.nota < 10:
            self.nota += 1
        else:
            print("O jogador já tem o máximo de nota (10).")

    def diminuir_vida(self):
        if self.nota > 0:
            self.nota -= 1
        else:
            print("O jogador já está sem nota.")
            
    def incrementar_pontos(self,pontos:int):
        self._pontos_total += pontos
        
    def usar_bomba(self):
        if self._inventario["bombas"] > 0:
            self._inventario["bombas"] -= 1
            return True
        else:
            return False
        
    def pegar_item(self,item):
        if item in self._inventario.keys():
            self._inventario[item] += 1
        else:
            self._inventario[item] = 1
            
    def status(self):
        print(f"""
              nota restantes: {self._nota}
              pontos: {self._pontos_total}
              labirinto atual: {self._labirinto_atual}
    """)