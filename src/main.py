from level import Level
from save import *

if __name__ == "__main__":
    level_teste = read_level_base("level_1")

    jogo = Level("level_1",level_teste["maze"],level_teste["items"],level_teste["enemies"],level_teste["time"],level_teste["media"])
    jogo.jogar()