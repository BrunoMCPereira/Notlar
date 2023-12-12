import socket
import json
import mysql.connector
import threading
import tkinter as tk
import ttkbootstrap as ttk
from models.criptografia import Criptografia as c

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
        self.text_area.insert(tk.END, self.comand_prompt)
        self.after(10000, self.atualizar_texto)

class ServidorUtilizadores(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Servidor Utilizadores")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.interface = PromptServidor(self)

        self.style = ttk.Style()
        self.style.theme_use('superhero')

        self.prompt_servidor = ""

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

        self.inicializar_servidor()
        
        self.dados = {

            'nome': None,
            'username': None,
            'novo_username': None,
            'password': None,
            'nova password': None,
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
            tratamento = threading.Thread(target=self.processar_mensagem, args=(conexao, morada))
            tratamento.start()

    def processar_mensagem(self, conexao, morada):
        ligacao = True
        while ligacao:
            mensagem_encriptada = conexao.recv().decode()
            mensagem = c.desencriptar_cliente(mensagem_encriptada)
            if mensagem:
                if mensagem == MESSAGEM_DESCONECTAR:
                    conexao.close()
                    ligacao = False
                else:
                    json_res = json.loads(res[0])
                    self.dados['nome'] = json_res["dd"][1]
                    self.dados['username'] = json_res["dd"][2]
                    self.dados['novo_username'] = json_res["dd"][3]
                    self.dados['password'] = json_res["dd"][4]
                    self.dados['nova password'] = json_res["dd"][5]
                    self.dados['instrucao'] = json_res["dd"][6]
                    self.log("\nSERVIÇO REQUERIDO\n")
                    if self.dados['instrução'] == 'Criar_Utilizador':
                        resposta = self.criar_utilizador(self.dados['nome'], self.dados['username'], self.dados['password'])
                        resposta_encriptada = c.encriptar_cliente(resposta)
                        resposta_cliente = resposta_encriptada.encode()
                        conexao.sendall(resposta_cliente)
                        print(f'\nRESPOSTA ENVIADA a IP:{morada} \n')
                    elif self.dados['instrução'] == 'Alterar_Password':
                        resposta = self.alterar_password(self.dados['username'], self.dados['password'])
                        resposta_encriptada = c.encriptar_cliente(resposta)
                        resposta_cliente = resposta_encriptada.encode()
                        conexao.sendall(resposta_cliente)
                        print(f'\nRESPOSTA ENVIADA a IP:{morada} \n')
                    elif self.dados['instrução'] == 'Eliminar_Registo':
                        resposta = self.eliminar_registo(self.dados['username'])
                        resposta_encriptada = c.encriptar_cliente(resposta)
                        resposta_cliente = resposta_encriptada.encode()
                        conexao.sendall(resposta_cliente)
                        print(f'\nRESPOSTA ENVIADA a IP:{morada} \n')

    def criar_utilizador(self, nome, username, password) -> bool:
        nome = c.encriptar_base_dados(nome)
        username = c.encriptar_base_dados(username)
        password = c.encriptar_base_dados(password)
        query = "INSERT INTO utilizadores (Nome, Username, Password) VALUES (%s, %s, %s)"
        values = (nome, username, password)
        self.cursor.execute(query, values)
        self.conn.commit()
        return True

    def alterar_password(self, username, new_password) -> bool:
        username = c.encriptar_base_dados(username)
        new_password = c.encriptar_base_dados(new_password)
        query = "UPDATE utilizadores SET Password = %s WHERE Username = %s"
        values = (new_password, username)
        self.cursor.execute(query, values)
        self.conn.commit()
        return True

    def eliminar_registo(self, username) -> bool:
        username = c.encriptar_base_dados(username)
        query = "DELETE FROM utilizadores WHERE Username = %s"
        values = (username,)
        self.cursor.execute(query, values)
        self.conn.commit()
        return True
    
    def validar_utilizador(self, username, password) -> bool:
        username = c.encriptar_base_dados(username)
        password = c.encriptar_base_dados(password)
        values = (password, username)
        query = "SELECT * FROM utilizadores WHERE username = %s AND password = %s"
        self.cursor.execute(query, values)
        usuario = self.cursor.fetchone()
        if usuario is None:
            return False
        else:
            return True

    def log(self, mensagem):
        self.prompt_servidor += mensagem + "\n"

    def atualizar_text_area(self):
        self.interface.text_area.delete(1.0, tk.END)
        self.interface.text_area.insert(tk.END, self.prompt_servidor)
        self.after(100, self.atualizar_text_area)



