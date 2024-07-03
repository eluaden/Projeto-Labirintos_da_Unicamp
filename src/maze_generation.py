from random import choice,randint

def generate_maze(pos, maze, visited= None):
    # funçao recursiva que "cava" buracos em um grid, gerando assim um labirinto aleatorio com ajuda de uma funçao de escolha
    if visited == None:
        visited = []

    moves = [(2, 0), (-2, 0), (0, 2), (0, -2)]

    visited.append(pos)

    pss_moves = []
    for move in moves:
        new_x = pos[0] + move[0]
        new_y = pos[1] + move[1]

        if (new_x < len(maze) and new_x >= 0) and (new_y < len(maze[0]) and new_y >= 0) and (new_x,new_y) not in visited:
            pss_moves.append(move)

    while pss_moves:
        move = choice(pss_moves)           
        new_x = pos[0] + move[0]
        new_y = pos[1] + move[1]
        
        #linkando as partes em branco
        if move == (2, 0):
            maze[new_x - 1][new_y] = 0
        elif move == (-2, 0):
            maze[new_x + 1][new_y] = 0
        elif move == (0, 2):
            maze[new_x][new_y - 1] = 0
        elif move == (0, -2):
            maze[new_x][new_y + 1] = 0
        generate_maze((new_x,new_y),maze,visited)

        #atualizando movimentos possiveis levando em conta a recursao
        pss_moves = [move for move in moves if 
                     (0 <= pos[0] + move[0] < len(maze)) and 
                     (0 <= pos[1] + move[1] < len(maze[0])) and 
                     (pos[0] + move[0], pos[1] + move[1]) not in visited]

    return visited

def create_maze(size_x,size_y,start = None,exit = None) -> list:
    # ao gerar labirintos, tente evitar tamanhos pares, por causa da logica que eu escolhi 
    # pra fazer o algoritimo ele gera um labirinto meio quebrado quando com numeros pares
    maze = [[1]*size_x for _ in range(size_y)]
    for i in range(1,len(maze) -1,2):
        for j in range(1,len(maze[i]) -1,2):
            maze[i][j] = 0

    if start == None:        
        pass # faltando completar essa parte
    
    if exit == None:        
        pass # e essa
        

    generate_maze(start,maze)

    maze[start[0]][start[1]] = 2
    maze[exit[0]][exit[1]] = 3

    return maze

def print_maze(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                print("#", end= " ")
            elif maze[i][j] == 2:
                print("E", end= " ")
            elif maze[i][j] == 3:
                print("S", end= " ")
            else:
                print(" ", end= " ")

        print()

maze = create_maze(41,41,(1,1),(7,7))


print_maze(maze)