from level import *
from inimigos import *  
 
class Moderador:
    def __init__(self,level) -> None:
        self._level = level
        pass

    def perdeu(self):
        print("voce perdeu!!")
        estatua = Statue(self._level.jogador.nome,self._level.jogador.posicao_atual)
        self._level.enemies["statue"] = estatua
        save_level_progress(self._level.nome,self._level.maze,self._level.enemies,self._level.items,self._level.posicoes_ocupadas,player=None,)
        pygame.quit()
        quit()
        
