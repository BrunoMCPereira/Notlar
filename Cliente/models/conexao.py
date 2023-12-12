import string
import random
import json

class Comunicacao:
    @staticmethod
    def criar_sessao() -> str:
        tamanho_string = 12
        letras = string.ascii_lowercase
        string_aleatoria = "".join(random.choice(letras) for _ in range(tamanho_string))
        return "s_" + string_aleatoria

    @staticmethod
    def cabecalho(sessao):
        return f"~m~{len(sessao)}~m~{sessao}"

    @staticmethod
    def construir_mensagem(func, param_list):
        return json.dumps({"m": func, "p": param_list}, separators=(",", ":"))

    @staticmethod
    def criar_mensagem(func, param_list):
        return Comunicacao.cabecalho(Comunicacao.construir_mensagem(func, param_list))

    @staticmethod
    def criar_identificador_nota():
        string_length = 10
        letras = string.ascii_lowercase
        id_nota = "".join(random.choice(letras) for _ in range(string_length))
        return "n_" + id_nota
    
    def criar_identificador_utilizador():
        string_length = 10
        letras = string.ascii_lowercase
        id_utilizador = "".join(random.choice(letras) for _ in range(string_length))
        return "u_" + id_utilizador
    
    @staticmethod
    def encriptar(texto):
        chave=5
        return "".join([chr(ord(algo) + chave) for algo in texto])
    
    @staticmethod
    def desencriptar(texto):
        chave=5
        return "".join([chr(ord(algo) - chave) for algo in texto])