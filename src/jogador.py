class Jogador:
    def _init_(self, nome: str, vidas: int, pontos_total: int, labirinto_atual: int, posicao_atual: list, tempo_restante:int) -> None:
        self._nome = nome
        self._vidas = vidas
        self._pontos_total = pontos_total
        self._inventario = {"bombas":0}
        self._labirinto_atual = labirinto_atual
        self._posicao_atual = posicao_atual.copy()
        self._tempo_restante = tempo_restante
    
    @property
    def nome(self):
        return self._nome

    @property
    def vidas(self):
        return self._vidas

    @vidas.setter
    def vidas(self, value):
        if 0 <= value <= 5:
            self._vidas = value
        else:
            print("Número inválido de vidas. Deve estar entre 0 e 5.")
    
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
        return self.tempo_restante

    @tempo_restante.setter
    def tempo_restante(self, value):
        self._tempo_restante = value    
        
        
    def mover(self,direcao:str):
        match direcao:
            case 'direita':
                self._posicao_atual[0] += 1
            case 'esquerda':
                self._posicao_atual[0] -= 1
            case 'cima':
                self._posicao_atual[1] += 1
            case 'baixo':
                self._posicao_atual[1] -= 1
            case _:
                print("Direção inválida")
                
                
    def aumentar_vida(self):
        if self.vidas < 5:
            self.vidas += 1
        else:
            print("O jogador já tem o máximo de vidas (5).")

    def diminuir_vida(self):
        if self.vidas > 0:
            self.vidas -= 1
        else:
            print("O jogador já está sem vidas.")
            
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
              vidas restantes: {self._vidas}
              pontos: {self._pontos_total}
              labirinto atual: {self._labirinto_atual}
    """)