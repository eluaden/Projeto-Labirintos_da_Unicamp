class Item:
    def __init__(self, posicao, on_inv=False) -> None:
        self._pos = posicao
        self._on_inv = on_inv  # verifica se está no inventário do jogador
    
    def special_action(self,player):
        pass

    @property
    def position(self):
        return self._pos
    
    @position.setter
    def position(self, pos):
        self._pos = pos


class Clock(Item):
    def __init__(self, posicao,on_inv = False) -> None:
        super().__init__(posicao,on_inv)
    
    def special_action(self, player):
        # adiciona 5 segundos no temporizador do jogador
        player.tempo_restante += 5
    
    @property
    def position(self):
        return self._pos


class Bomb(Item):
    def init(self, posicao,on_inv = False) -> None:
        super().init(posicao,on_inv)

    @property
    def on_inv(self):
        return self._on_inv

    @on_inv.setter
    def on_inv(self, value):
        self._on_inv = value

    def special_action(self, player):
        if not self._on_inv:
            raise Exception("Bomba acionada sem estar no inventário de um jogador!!")

        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        print(f"Explodindo bomba na posição {player.posicao_atual}")

        for direction in directions:
            new_x = player.posicao_atual[0] + direction[0]
            new_y = player.posicao_atual[1] + direction[1]

            print(f"Tentando explodir na direção {direction} -> nova posição: ({new_x}, {new_y})")

            # Certifique-se de que a posição nova esteja dentro dos limites do labirinto e não é uma parede da borda
            if (1 <= new_x < len(player.labirinto_atual[0]) - 1) and (1 <= new_y < len(player.labirinto_atual) - 1):
                print(f"Posição ({new_x}, {new_y}) está dentro dos limites do labirinto e não é uma borda")
                # Verifica se há uma parede na posição nova
                if player.labirinto_atual[new_y][new_x] == 1:
                    print(f"Explodindo parede na posição ({new_x}, {new_y})")
                    player.labirinto_atual[new_y][new_x] = 0
                else:
                    print(f"Nenhuma parede para explodir na posição ({new_x}, {new_y})")
            else:
                print(f"Posição ({new_x}, {new_y}) está fora dos limites do labirinto ou é uma borda")

class Book(Item):
    def __init__(self, posicao,on_inv = False) -> None:
        super().__init__(posicao,on_inv)
    
    def special_action(self, player):
        # aumenta a nota do jogador
        player.nota += 1
        print("teste")

    @property
    def position(self):
        return self._pos
    


        
        
    

        