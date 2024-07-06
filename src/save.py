import pickle
import os
# todos tem q ser chamados fora da pasta src**

#le o as infos padrao de um nivel
def read_level_base(level_name) -> dict:
    #le os arquivos base de niveis
    file_path = os.path.join("database/level_base/",level_name + ".pkl")
    with open(file_path,"rb") as level:
        return pickle.load(level)

#para salvar um novo usuario no database, com progresso passado por parametros
def save_user(usuario,nivel_1,nivel_2,nivel_3,nivel_4,nivel_5,nivel_6,nivel_7,nivel_8,nivel_9,nivel_10,ultimo_nivel,pontuacao) -> None:

    file_path_user = os.path.join("database/users/",usuario + ".pkl")
    file_path_all_users = os.path.join("database/users/all_users.pkl")

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
    print("pru",user)


    if os.path.exists(file_path_all_users):
        with open(file_path_all_users,"rb+") as all_users_file:
            all_users = pickle.load(all_users_file)
            all_users_file.seek(0)
            print("all_users", all_users)
            all_users[usuario] = user["pontuacao"]
            print("all_users", all_users)
            pickle.dump(all_users, all_users_file)
    else:
        with open(file_path_all_users,"wb") as all_users_file:
            all_users = {}
            all_users[usuario] = user["pontuacao"]
            print("all_users", all_users)
            pickle.dump(all_users, all_users_file)

        
    with open(file_path_user,"wb") as user_file:
        
        pickle.dump(user,user_file)


#para ler um usuario do database
def read_user(usuario):
    file_path = os.path.join("database/users/",usuario + ".pkl")
    if os.path.exists(file_path):
        with open(file_path,"rb") as user_file:
            return pickle.load(user_file)
    else:
        return False
    
# para ler alguma pergunta do database
def read_pergunta(nivel):
    path = os.path.join("database/perguntas/", nivel + ".pkl")
    with open(path, "rb") as f:
        return pickle.load(f)


def read_all_users():
    file_path_all_users = os.path.join("database/users/all_users.pkl")
    if not os.path.exists(file_path_all_users):
        return {}
    with open(file_path_all_users, "rb") as all_users_file:
        all_users = pickle.load(all_users_file)
        print("reading", all_users)
        return all_users  




    