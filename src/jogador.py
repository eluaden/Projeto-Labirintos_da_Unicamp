import pygame.sprite

class Jogador(pygame.sprite.Sprite):
    def __init__(self, nome: str, nota: int, pontos_total: int, labirinto_atual, posicao_atual: list, tempo_restante:int):
        self._nome = nome
        self._nota = nota
        self._pontos_total = pontos_total
        self._inventario = {"bombas":[]}
        self._labirinto_atual = labirinto_atual
        self._posicao_atual = posicao_atual.copy()
        self._tempo_restante = tempo_restante

        # Carregue as imagens para a animação do jogador
        self.imagens = [
            pygame.image.load('assets/attack_1.png').convert_alpha(),
            pygame.image.load('assets/attack_2.png').convert_alpha(),
            pygame.image.load('assets/attack_3.png').convert_alpha(),
            pygame.image.load('assets/attack_4.png').convert_alpha(),
            pygame.image.load('assets/attack_5.png').convert_alpha(),
            pygame.image.load('assets/attack_6.png').convert_alpha(),
            pygame.image.load('assets/attack_7.png').convert_alpha(),
            pygame.image.load('assets/attack_8.png').convert_alpha(),
            pygame.image.load('assets/attack_9.png').convert_alpha(),
            
            # Adicione mais imagens conforme necessário para a animação
        ]
        
        self.image_index = 0  # Índice atual da imagem de animação
        self.image = self.imagens[self.image_index]  # Imagem atual do jogador
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (posicao_atual[0]*20, posicao_atual[1]*20)
        
    def update(self):
        # Atualize a imagem do jogador para a próxima na animação
        self.image_index += 0.25
        if self.image_index >= len(self.imagens):
            self.image_index = 0
        self.image = self.imagens[int(self.image_index)]
        
        # Atualize a posição do retângulo do jogador
        self.rect.topleft = (self.posicao_atual[0]*40, self.posicao_atual[1]*40)  # Ajuste conforme necessário
           
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