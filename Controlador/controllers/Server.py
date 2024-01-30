import socket
import threading
import tkinter as tk
import ttkbootstrap as ttk


# Configurações iniciais do Controlador
SERVER = socket.gethostbyname(socket.gethostname())
PORTA = 5050
MORADA = (SERVER, PORTA)
MESSAGEM_DESCONECTAR = "!DISCONNECTAR"
FORMATO = 'utf-8'

class PromptServidor(ttk.Frame):
    """ Interface gráfica para o servidor. """
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.comand_prompt()


    def comand_prompt(self):
        # Configuração de estilo e criação do campo de texto.
        self.style = ttk.Style()
        self.style.theme_use('superhero')
        self.text_area = tk.Text(self, wrap=tk.WORD, height=10, width=75)
        self.text_area.grid(row=0, column=0, padx=5, pady=5)
        self.atualizar_text_area()


    def atualizar_text_area(self):
        # Atualiza o texto exibido na interface gráfica.
        # Aqui, você pode adicionar lógica para atualizar o texto com informações do servidor.
        self.after(100, self.atualizar_text_area)


class ControladorPrincipal(tk.Tk):
    """ Classe principal do servidor. """
    def __init__(self):
        super().__init__()
        # Configuração da janela principal.
        self.title("Controlador Principal Notlar")
        self.geometry("475x175")
        self.protocol("WM_DELETE_WINDOW", self.ao_fechar)
        # Configuração de estilo e criação do campo de texto.
        self.style = ttk.Style()
        self.style.theme_use('superhero')
        self.text_area = tk.Text(self, wrap=tk.WORD, height=10, width=75)
        self.text_area.grid(row=0, column=0, padx=5, pady=5)
        
        # Inicialização do servidor e do balanceador de carga.
        self.ecra = ""
        self.controlador = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria o socket do Controlador
        self.controlador.bind((MORADA)) #Liga o IP e a Porta ao socket
        
        # Parametrização dos Servidores de Serviços
        self.ip_servicos = [f"http://{'192.168.1.202'}:{5030}"] # adicionar servidores de serviços: , f"http://{'server_ip'}:{'port'}"
        self.ip_actual = 0
        
        # inicia o Servidor do Controlador
        self.inicializar_servidor()

        self.servicos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def ao_fechar(self):
        # Encerramento do servidor e da conexão.
        self.controlador.close()
        self.destroy()


    def emi(self, mensagem):
        # Adiciona uma mensagem ao emi do servidor.
        self.ecra += mensagem + "\n"
        self.atualizar_text_area()


    def inicializar_servidor(self):
        # Configuração e inicialização do servidor para ouvir conexões.
        self.controlador.listen()
        self.emi(f'SERVIDOR INICIALIZADO em {SERVER}...')
        threading.Thread(target=self.aceitar_conexoes).start()


    def aceitar_conexoes(self):
        # Aceita conexões dos clientes e cria threads para lidar com elas.
        while True:
            conexao, morada = self.controlador.accept()
            self.emi(f'CONEXAO COM IP: {morada} ...')
            self.processar_mensagem(conexao)
            


    def processar_mensagem(self, conexao):
        # Processamento de mensagens recebidas dos clientes e repassando para o servidor de serviços.
        ligacao = True
        while ligacao:
            try:
                mensagem_enc = conexao.recv(2048)
                mensagem: str = mensagem_enc.decode(FORMATO)
                mensagem_d = self.desencriptar_cliente(mensagem)
                if mensagem_d == MESSAGEM_DESCONECTAR:
                    conexao.close()
                    ligacao = False
                else:
                    self.servicos = self.prox_serv() # activação do servidor de serviços por Round Robin
                    self.servicos.send(mensagem_enc) # Envio de Mensagem ao Servidor
                    self.emi(f'Solicitado serviço ao Servidor de Serviços')
                    resposta_enc = self.servicos.recv(2048) # Recepção de Mensagem
                    conexao.send(resposta_enc)  # Envia a resposta de volta ao cliente
                    self.servicos.close() # Fecho de Servidor de Serviços
                    conexao.close() # Fecho de Servidor de Cliente
                    ligacao = False
            except Exception as e:
                self.emi(f"Erro ao processar mensagem: {e}")
                break


    def atualizar_text_area(self):
        # Atualiza a área de texto com o emi do servidor.
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.ecra)

    @staticmethod
    def encriptar_cliente(texto: str) -> str:
        chave = 5
        return "".join([chr(ord(algo) + chave) for algo in texto])

    @staticmethod
    def desencriptar_cliente(texto: str) -> str:
        chave = 5
        return "".join([chr(ord(algo) - chave) for algo in texto])
    """ Balanceador de carga usando o algoritmo Round Robin. """


    def prox_serv(self):
        # Retorna o próximo servidor na lista.
        serv_dest = self.ip_servicos[self.ip_actual]
        ip, porta = serv_dest.replace('http://','').split(':')
        self.ip_actual = (self.ip_actual + 1) % len(self.ip_servicos)
        servidor_servicos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_servicos.connect((ip, int(porta)))
        return servidor_servicos