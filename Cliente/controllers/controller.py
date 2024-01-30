import socket
import ast


PORTA = 5050
IP_CONTROLADOR = "192.168.1.204"  # Substitua pelo IP real do servidor Controlador
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
            'instrução': None,
            'notas': []
        }

    def dados_mensagem(self) -> dict:
        return self.mensagem

class ConexaoControlador:
    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((IP_CONTROLADOR, PORTA))

    @staticmethod
    def encriptar_cliente(texto: str) -> str:
        chave = 5
        return "".join([chr(ord(algo) + chave) for algo in texto])

    @staticmethod
    def desencriptar_cliente(texto: str) -> str:
        chave = 5
        return "".join([chr(ord(algo) - chave) for algo in texto])

    def tratamento_mensagem(self, mensagem):
        self.cliente.send(mensagem.encode(FORMATO))
        resposta_enc_c = self.cliente.recv(2048)
        resposta_enc = resposta_enc_c.decode(FORMATO)
        resposta: str = self.desencriptar_cliente(resposta_enc)
        if resposta not in ['True', 'False']:
            dados: dict = ast.literal_eval(resposta)
            return dados
        else:
            resul : bool = bool(resposta)
            return resul

    def fechar_conexao(self):
        # Enviar mensagem de desconexão antes de fechar a conexão
        mensagem_desconexao = ConexaoControlador.encriptar_cliente(MESSAGEM_DESCONECTAR)
        self.cliente.send(mensagem_desconexao.encode(FORMATO))
        self.cliente.close()


    def obter_notas(self, mensagem):
        self.cliente.send(mensagem.encode(FORMATO))
        resposta_enc_c = self.cliente.recv(2048)
        resposta_enc = resposta_enc_c.decode(FORMATO)
        resposta: str = self.desencriptar_cliente(resposta_enc)