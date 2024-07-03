from random import randint

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
    
    def die(self,enemies):
        if self in enemies:
            enemies.remove(self)
        
 
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
    
    def wander(self, maze):
        return super().wander(maze)
    
    def ask(self):
        pass

    def die(self, enemies):
        return super().die(enemies)
    
    
    
class Statue(Enemy):
    def __init__(self, nome, position) -> None:
        super().__init__(nome, position)

    @property
    def position(self):
        return self._pos
    @property
    def nome(self):
        return self._nome
    
    def wander(self, maze):
        pass # esse tipo de Enemy não anda 
    
    def ask(self):
        pass
    
    def die(self, enemies):
        return super().die(enemies)


