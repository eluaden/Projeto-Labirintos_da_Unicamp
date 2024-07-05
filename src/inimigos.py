from random import randint
from save import read_pergunta

class Enemy: # classe base para Enemys,trata apenas da movimentação dele
    def __init__(self,nome,position) -> None:
        self._nome = nome
        self._pos = position
        self._health = None
    
    @property
    def position(self):
        return self._pos
    @property
    def nome(self):
        return self._nome

 
class Teacher(Enemy):
    def __init__(self, nome, position) -> None:
        super().__init__(nome, position)
        self._health = 3

    @property
    def position(self):
        return self._pos
    @property
    def nome(self):
        return self._nome
    
    def wander(self,maze):

        moves = [(0,1),(0,-1),(1,0),(-1,0)]
        pss_moves = []
        for move in moves:
            new_x = move[0] + self._pos[0]
            new_y = move[1] + self._pos[1]

            if new_x < len(maze) and new_x >= 0 and new_y < len(maze[0]) and new_y >= 0:
                if maze[new_y][new_x] == 0:
                    pss_moves.append(move)   
        if pss_moves:                                
            move = pss_moves[randint(0,len(pss_moves)-1)]
        else: move = (0,0)
        self._pos = (self._pos[0] + move[0], self._pos[1] + move[1])
    
    def ask(self,nivel):
        perguntas = read_pergunta(nivel)
        pergunta = perguntas[randint(0,len(perguntas)-1)]
        return pergunta

    
    
    
class Statue(Enemy):
    def __init__(self, nome, position) -> None:
        super().__init__(nome, position)

    @property
    def position(self):
        return self._pos
    @property
    def nome(self):
        return self._nome
    
    def ask(self):
        perguntas = read_pergunta(nivel)
        pergunta = perguntas[randint(0,len(perguntas)-1)]
        return pergunta
    

