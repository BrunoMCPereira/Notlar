import string
import random
import json
import xmlrpc.client
import socket
import json
from controllers.controller import UtilizadorActivo  # Importando a classe UtilizadorActivo

PORTA = 5050
IP_SERVIDOR = "endereço_ip_do_servidor"  # Substitua pelo IP real do servidor
FORMATO = 'utf-8'

class ConexaoControlador:
    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((IP_SERVIDOR, PORTA))

    def encriptar_cliente(texto: str) -> str:
        chave = 5
        return "".join([chr(ord(algo) + chave) for algo in texto])
    
    def desencriptar_cliente(texto: str) -> str:
        chave=5
        return "".join([chr(ord(algo) - chave) for algo in texto])

    def tratamento_mensagem(self, mensagem):
        """ Envia uma mensagem encriptada para o servidor e aguarda a resposta. """
        mensagem_encriptada = self.encriptar_cliente(mensagem)
        self.cliente.send(mensagem_encriptada.encode(FORMATO))
        resposta_enc = self.cliente.recv(2048).decode(FORMATO)
        resposta = self.desencriptar_cliente(resposta_enc)
        return resposta

    def fechar_conexao(self):
        self.cliente.close()