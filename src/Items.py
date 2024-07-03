class Item:
    def __init__(self,posicao,on_inv = False) -> None:
        self._pos = posicao
        self._on_inv = on_inv # verifica se esta no inventario do jogador
    
    def special_action(self):
        pass

    @property
    def position(self,pos):
        self._pos = pos

    @position.setter
    def position(self,pos):
        self._pos = pos

class Clock(Item):
    def __init__(self, posicao) -> None:
        super().__init__(posicao)
    
    def special_action(self,player):
        #adiciona 5 segundos no temporizador do jogador
        player.tempo_restante += 5
    
    @property
    def position(self,pos):
        self._pos = pos

    @position.setter
    def position(self,pos):
        self._pos = pos
        

class Bomb(Item):
    def __init__(self, posicao) -> None:
        super().__init__(posicao)

    def special_action(self,player):
        if not self._on_inv:
            raise Exception("bomba acionada sem estra no inventário de um jogador!!")

        directions = [(0,1),(0,-1),(-1,0),(1,0)]

        for direction in directions:
            new_x = player.posicao_atual[0] + direction[0]
            new_y = player.posicao_atual[1] + direction[1]

            if (new_x < len(player.labirinto_atual) and new_x >= 0) and \
               (new_y < len(player.labirinto_atual[0]) and new_y >= 0):
                
                player.labirinto_atual[new_x][new_y] = 0
    


        
        
    

        