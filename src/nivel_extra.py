from gera_labirintos import create_maze
from level import Level
from random import randint


def nivel_extra(nome_usuario,usuario):

    maze_x = ((randint(18,54)) //2) * 2 + 1
    maze_y = ((randint(18,54)) //2) * 2 + 1
    maze = create_maze(maze_x,maze_y)

    itens = {"bombs":(maze_x//5) -1,"clocks": (maze_y//4) + 1, "books": maze_x//5}
    inimigos = {"teachers": (maze_y//5)}
    time = 60 + ((maze_x * maze_y) - 800)
    media = time % 10

    

    nivel = Level("nivel_0",nome_usuario,maze,itens,inimigos,time,media)
    nivel.jogar()

