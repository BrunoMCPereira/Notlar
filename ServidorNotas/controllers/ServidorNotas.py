import socket
import mysql.connector
import threading
import tkinter as tk
import ttkbootstrap as ttk
import json

SERVER = socket.gethostbyname(socket.gethostname())
PORTA = 5050
MORADA = (SERVER, PORTA)
FORMATO = 'utf-8'
MESSAGEM_DESCONECTAR = "!DISCONNECTAR"

class PromptServidor(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.comand_prompt()

    def comand_prompt(self):
        self.style = ttk.Style()
        self.style.theme_use('superhero')

        self.text_area = tk.Text(self, wrap=tk.WORD, height=10, width=75)
        self.text_area.grid(row=0, column=0, padx=5, pady=5)

        self.after(100, self.atualizar_texto)

    def atualizar_texto(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, prompt_servidor)
        self.after(100, self.atualizar_texto)

class ServidorNotas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Servidor Notas Notlar")
        self.geometry("475x175")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.style = ttk.Style()
        self.style.theme_use('superhero')

        self.text_area = tk.Text(self, wrap=tk.WORD, height=10, width=75)
        self.text_area.grid(row=0, column=0, padx=5, pady=5)

        self.server_log = ""

        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((MORADA))

        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="Sistemas_Distribuidos",
            password="Base_Dados_Notas",
            db="notlar"
        )

        self.cursor = self.conn.cursor()
        
        self.dados = {

            'username': None,
            'username_id': None,
            'nota': None,
            'nova nota': None,
            'instrucao': None,
        }
            

        self.inicializar_servidor()
        
        self.dados = {

            'username': None,
            'username_id': None,
            'nota': None,
            'nova nota': None,
            'instrucao': None,
        }

    def on_closing(self):
        self.servidor.close()
        self.conn.close()
        self.destroy()

    def inicializar_servidor(self):
        self.servidor.listen()
        self.log("SERVIDOR INICIALIZADO...")

        threading.Thread(target=self.aceitar_conexoes).start()
        self.after(100, self.atualizar_text_area)

    def aceitar_conexoes(self):
        while True:
            conexao, morada = self.servidor.accept()
            self.log(f'CONEXAO COM IP: {morada} ...')
            tratamento = threading.Thread(target=self.processar_mensagem, args=(conexao,))
            tratamento.start()

    def processar_mensagem(self, conexao):
        ligacao = True
        while ligacao:
            mensagem = conexao.recv(1024).decode('utf-8')
            if mensagem == "!DISCONNECTAR":
                conexao.close()
                ligacao = False
        #Melhoria deste tratamento
        mensagem = mensagem.replace("}", "")
        self.log("\nSERVIÇO REQUERIDO\n")
        mensagem = mensagem.replace("{", "")
        mensagem = mensagem.replace("]", "")
        mensagem_nt = mensagem.split("[")
        mensagem_nt: str = mensagem_nt[1]
        mensagem_nt = mensagem_nt.replace("'", "")
        mensagem_nt: list[str] = mensagem_nt.split(",")
        for i in range(len(mensagem_nt)):
            mensagem_nt[i] = mensagem_nt[i].replace(" ", "", 1)
        dados['notas'] = mensagem_nt
        mensagem = mensagem.replace("'", "")
        mensagem = mensagem.replace("[", "")
        mensagem = mensagem.replace(" ", "")
        mensagem = mensagem.split(",")
        dados_transmitidos = []
        for i in range(len(mensagem)):
            mensagem[i] = mensagem[i].split(":")
            dados_transmitidos.append(mensagem[i])
        username = dados_transmitidos[0]
        dados['username'] = username[1]
        password = dados_transmitidos[1]
        dados['password'] = password[1]
        nome = dados_transmitidos[2]
        dados['nome'] = nome[1]
        instrucao = dados_transmitidos[3]
        dados['instrução'] = instrucao[1]

        # Estrutura a alterar por funções
        if dados['instrução'] == 'Criar_Nota':
            self.criar_nota(dados['nome'], dados['username'], dados['password'])
            conexao.sendall(self.mostrar_notas(dados['username']))
        elif dados['instrução'] == 'Alterar_Nota':
            self.guardar_nota(dados['username'], dados['password'])
            conexao.sendall(self.mostrar_notas(dados['username']))
        elif dados['instrução'] == 'Eliminar_Nota':
            self.eliminar_nota(dados['username'])
            conexao.sendall(self.mostrar_notas(dados['username']))
        elif dados['instrução'] == 'Mostrar_Notas':
            conexao.sendall(self.mostrar_notas(dados['username']))

    def criar_nota(self, titulo, nota, id_utilizador):
        query = "INSERT INTO notas (titulo_nota, nota, ID_Utilizador) VALUES (%s, %s, %s)"
        values = (titulo, nota, id_utilizador)
        self.cursor.execute(query, values)
        self.conn.commit()

    def guardar_nota(self, novo_titulo, nova_nota):
        query = "UPDATE notas SET titulo_nota = %s, nota = %s WHERE ID = %s"
        values = (novo_titulo, nova_nota)
        self.cursor.execute(query, values)
        self.conn.commit()

    def eliminar_nota(self, nota_id):
        query = "DELETE FROM notas WHERE ID = %s"
        values = (nota_id,)
        self.cursor.execute(query, values)
        self.conn.commit()

    def mostrar_notas(self, id_utilizador):
        query = "SELECT titulo_nota, nota FROM notas WHERE ID_Utilizador = %s"
        values = (id_utilizador,)
        self.cursor.execute(query, values)
        notas = self.cursor.fetchall()
        return str(notas)

    def log(self, mensagem):
        self.server_log += mensagem + "\n"

    def atualizar_text_area(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.server_log)
        self.after(100, self.atualizar_text_area)

