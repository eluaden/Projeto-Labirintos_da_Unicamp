import pickle
import os
# tem q ser chamado fora da pasta src**
def read_level_base(level_name) -> dict:
    #le os arquivos base de niveis
    file_path = os.path.join("database/level_base/",level_name + ".pkl")
    with open(file_path,"rb") as level:
        print(type(level))
        return pickle.load(level)
    
def read_level_progress(level_name) -> dict:
    #le os arquivos de progresso de niveis
    file_path = os.path.join("database/level_progress/",level_name + ".pkl")
    with open(file_path,"rb") as level:
        return pickle.load(level)
    
def save_level_progress(level_name,maze,enemies,items,player):
    #salva progresso de arquivos niveis, 
    file_path = os.path.join("database/level_progress/",level_name + ".pkl")
    os.makedirs("database/level_progress/", exist_ok=True) # cria o diretorio caso nao exista

    with open(file_path,"wb") as save:
        level = {
        "maze": maze,
        "enemies": enemies,
        "items": items,
        "player": player
        }

        pickle.dump(level,save)
