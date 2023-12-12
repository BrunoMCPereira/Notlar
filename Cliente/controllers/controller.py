import socket
import json
import re
from models.conexao import Comunicacao as c

PORTA = 5050
FORMATO = 'utf-8'
MESSAGEM_DESCONECTAR = "!DISCONNECTAR"

class UtilizadorActivo:
    def __init__(self):
        self.mensagem = {
            'servidor': None,
            'nome': None,
            'username': None,
            'novo username': None,
            'password': None,
            'nova password': None,
            'nome': None,
            'instrucao': None,
            'notas': []
        }

    def dados_mensagem(self) -> dict:
        return self.mensagem


class Conexao:
    def __init__(self, dados: dict):
        self.dados = dados

    def binder(self) -> str:
        mapeamento_ip = {
            'utilizadores': 'localhost',  # Substituir pelos IPs desejados
            'notas': '192.168.1.18'
        }
        servidor = self.dados['servidor']
        ip_destino = mapeamento_ip[servidor]
        return ip_destino

    def enviar_mensagem(self, dados: dict) -> bool:
        conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = self.binder()
        conexao.connect(ip,PORTA)
        sessao = c.criar_sessao()
        mensagem = (dados['instrucao'],
                    [sessao,
                     dados['nome'],
                     dados['username'],
                     dados['novo username'],
                     dados['password'],
                     dados['nova password'],
                     dados['notas'],
                    ],)
        mensagem_str = str(mensagem)
        mensagem_encriptada = c.encriptar(mensagem_str)
        conexao.sendall(mensagem_encriptada.encode())
        while True:
            resposta_encriptada = conexao.recv()
            resposta_encriptada = resposta_encriptada.decode()
            resposta_recebida = c.desencriptar(resposta_encriptada)
            res = re.findall("^.*?({.*)$", resposta_recebida)
            if res:
                if dados['instrucao'] == "Criar_Utilizador":
                    conexao.sendall(MESSAGEM_DESCONECTAR.encode())
                    conexao.close()
                    return eval(res)
                if dados['instrucao'] == "Validar_Utilizador":
                    conexao.sendall(MESSAGEM_DESCONECTAR.encode())
                    conexao.close()
                    return eval(res)
                if dados['instrucao'] == "Eliminar Utilizador":
                    conexao.sendall(MESSAGEM_DESCONECTAR.encode())
                    conexao.close()
                    return eval(res)
        




