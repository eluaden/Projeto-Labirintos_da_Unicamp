import pickle
import os
# tem q ser chamado fora da pasta src**
def read_level_base(level_name) -> dict:
    #le os arquivos base de niveis
    file_path = os.path.join("database/level_base/",level_name + ".pkl")
    with open(file_path,"rb") as level:
        print(type(level))
        return pickle.load(level)

def save_user(usuario,nivel_1,nivel_2,nivel_3,nivel_4,nivel_5,nivel_6,nivel_7,nivel_8,nivel_9,nivel_10,ultimo_nivel,pontuacao) -> None:
    #salva o progresso do usuario
    file_path = os.path.join("database/users/",usuario + ".pkl")
    os.makedirs("database/users/", exist_ok=True) # cria o diretorio caso nao exista
    user = {
        "nome": usuario,
        "nivel_1": nivel_1,
        "nivel_2": nivel_2, 
        "nivel_3": nivel_3,
        "nivel_4": nivel_4,
        "nivel_5": nivel_5,
        "nivel_6": nivel_6,
        "nivel_7": nivel_7,
        "nivel_8": nivel_8,
        "nivel_9": nivel_9,
        "nivel_10": nivel_10,
        "ultimo_nivel": ultimo_nivel,
        "pontuacao": pontuacao
    }

    with open(file_path,"wb") as user_file:
        pickle.dump(user,user_file)


def read_user(usuario):
    file_path = os.path.join("database/users/",usuario + ".pkl")
    if os.path.exists(file_path):
        with open(file_path,"rb") as user_file:
            return pickle.load(user_file)
    else:
        return False
    
def read_pergunta(nivel):
    path = os.path.join("database/perguntas/", nivel + ".pkl")
    with open(path, "rb") as f:
        return pickle.load(f)




    