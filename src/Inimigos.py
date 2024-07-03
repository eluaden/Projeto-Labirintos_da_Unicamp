from random import randint

class Inimigo: # classe base para inimigos,trata apenas da movimentação dele
    def __init__(self,nome,position) -> None:
        self._nome = nome
        self._pos = position
    
    def wander(self,maze):
        moves = [(0,1),(0,-1),(1,0),(-1,0)]
        pss_moves = []
        for move in moves:
            new_x = move[0] + self._pos[0]
            new_y = move[1] + self._pos[1]

            if new_x < len(maze) and new_x >= 0 and new_y < len(maze[0]) and new_y >= 0:
                if maze[new_x][new_y] == 0:
                    pss_moves.append(move)                                   
        move = pss_moves[randint(0,len(pss_moves)-1)]
        self._pos = (self._pos[0] + move[0], self._pos[1] + move[1])
 
class Professor(Inimigo):
    def __init__(self, nome, position) -> None:
        super().__init__(nome, position)
    
    def wander(self, maze):
        return super().wander(maze)
    
    def ask(self):
        pass



