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
            'nome': None,
            'username': None,
            'novo username': None,
            'password': None,
            'nova password': None,
            'instrucao': None,
            'notas': []
        }

    def dados_mensagem(self) -> dict:
        return self.mensagem




