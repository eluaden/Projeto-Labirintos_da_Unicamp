import pickle
import os
# tem q ser chamado fora da pasta src***
def save_level(level_name,maze,enemies,items,player): 
    
    file_path = os.path.join("level/",level_name + ".pkl")
    os.makedirs("level/", exist_ok=True) # cria o diretorio caso nao exista

    with open(file_path,"wb") as save:
        level = {
        "maze": maze,
        "enemies": enemies,
        "items": items,
        "player": player
        }

        pickle.dump(level,save)

def read_level(level_name) -> dict:
    file_path = os.path.join("level/",level_name + ".pkl")
    with open(file_path,"rb") as level:
        return pickle.load(level)



save_level("teste",[],[],[],[])