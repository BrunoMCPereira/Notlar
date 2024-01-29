import socket
import threading
import tkinter as tk
import ttkbootstrap as ttk
import xmlrpc.client

# Configurações iniciais do servidor
SERVER = socket.gethostbyname(socket.gethostname())
PORTA = 5050
MORADA = (SERVER, PORTA)
FORMATO = 'utf-8'
MESSAGEM_DESCONECTAR = "!DISCONNECTAR"

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
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Configuração de estilo e criação do campo de texto.
        self.style = ttk.Style()
        self.style.theme_use('superhero')
        self.text_area = tk.Text(self, wrap=tk.WORD, height=10, width=75)
        self.text_area.grid(row=0, column=0, padx=5, pady=5)
        # Inicialização do servidor e do balanceador de carga.
        self.server_log = ""
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((MORADA))
        self.ip_servicos = [f"http://{'server_ip'}:{'port'}", f"http://{'server_ip'}:{'port'}"]
        self.load_balancer = RoundRobinLoadBalancer(self.ip_servicos)
        self.inicializar_servidor()

    def on_closing(self):
        # Encerramento do servidor e da conexão.
        self.servidor.close()
        self.destroy()

    def log(self, mensagem):
        # Adiciona uma mensagem ao log do servidor.
        self.server_log += mensagem + "\n"
        self.atualizar_text_area()

    def inicializar_servidor(self):
        # Configuração e inicialização do servidor para ouvir conexões.
        self.servidor.listen()
        self.log(f'SERVIDOR INICIALIZADO em {SERVER}...')
        threading.Thread(target=self.aceitar_conexoes).start()

    def aceitar_conexoes(self):
        # Aceita conexões dos clientes e cria threads para lidar com elas.
        while True:
            conexao, morada = self.servidor.accept()
            self.log(f'CONEXAO COM IP: {morada} ...')
            tratamento = threading.Thread(target=self.processar_mensagem, args=(conexao,))
            tratamento.start()

    def processar_mensagem(self, conexao):
        # Processamento de mensagens recebidas dos clientes e repassando para o servidor de serviços.
        ligacao = True
        while ligacao:
            try:
                mensagem = conexao.recv(1024).decode(FORMATO)
                if mensagem == MESSAGEM_DESCONECTAR:
                    conexao.close()
                    ligacao = False
                else:
                    # Repassa a mensagem para o servidor de serviços selecionado pelo balanceador de carga
                    resposta = self.load_balancer.send_message(mensagem)
                    conexao.send(resposta.encode(FORMATO))  # Envia a resposta de volta ao cliente
            except Exception as e:
                self.log(f"Erro ao processar mensagem: {e}")
                break

    def atualizar_text_area(self):
        # Atualiza a área de texto com o log do servidor.
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.server_log)

class RoundRobinLoadBalancer:
    """ Balanceador de carga usando o algoritmo Round Robin. """
    def __init__(self, servers):
        # Inicialização com lista de servidores.
        self.servers = servers
        self.current_server_index = 0
        self.lock = threading.Lock()

    def get_server_proxy(self):
        # Retorna um proxy para o próximo servidor na lista.
        with self.lock:
            server_address = self.servers[self.current_server_index]
            self.current_server_index = (self.current_server_index + 1) % len(self.servers)
            return xmlrpc.client.ServerProxy(server_address)

    def send_message(self, message):
        # Envia uma mensagem para o servidor e recebe a resposta.
        try:
            server_proxy = self.get_server_proxy()
            response = server_proxy.process_string(message)
            return response
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return None


