import socket
import mysql.connector
import threading
import tkinter as tk
import ttkbootstrap as ttk
import ast

SERVER = socket.gethostbyname(socket.gethostname())  # Obtem o IP do Servidor de Serviços
PORTA_S = 5030
MORADA_S = (SERVER, PORTA_S)
FORMATO = "utf-8"

class PromptServidor(ttk.Frame):
    def __init__(self, master, server_log_var):
        super().__init__(master)
        self.server_log_var = server_log_var
        self.grid(row=0, column=0, sticky="nsew")
        self.comand_prompt()

    def comand_prompt(self):
        self.style = ttk.Style()
        self.style.theme_use('superhero')
        self.text_area = tk.Text(self, wrap=tk.WORD, height=10, width=75)
        self.text_area.grid(row=0, column=0, padx=5, pady=5)
        self.atualizar_text_area()

    def atualizar_text_area(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.server_log_var.get())
        self.after(100, self.atualizar_text_area)

class ServidorServicos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Servidor de Serviços")
        self.geometry("475x175")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.style = ttk.Style()
        self.style.theme_use('superhero')

        self.server_log = tk.StringVar()
        self.interface = PromptServidor(self, self.server_log)

        self.conn = mysql.connector.connect(
            host="192.168.1.5",
            port=3306,
            user="Sistemas_Distribuidos",
            password="Base_Dados_Notas",
            db="notlar"
        )
        self.cursor = self.conn.cursor()
        self.controlador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.controlador.bind(MORADA_S)

        self.inicializar_servidor()

    def on_closing(self):
        self.controlador.close()
        self.conn.close()
        self.destroy()

    def log(self, mensagem):
        current_log = self.server_log.get()
        self.server_log.set(current_log + mensagem + "\n")

    def inicializar_servidor(self):
        self.controlador.listen()
        self.log(f'SERVIDOR INICIALIZADO em {SERVER}...')
        threading.Thread(target=self.aceitar_conexoes).start()

    def aceitar_conexoes(self):
        while True:
            conexao, morada = self.controlador.accept()
            self.log(f'CONEXAO COM IP: {morada} ...')
            threading.Thread(target=self.processar_mensagem, args=(conexao,)).start()

    def processar_desc_mensagem(self, mensagem_encriptada):
        mensagem = self.desencriptar(mensagem_encriptada)
        mensagem_d = ast.literal_eval(mensagem)
        return mensagem_d


    def processar_enc_mensagem(self, mensagem_encriptada):
        mensagem = self.encriptar(mensagem_encriptada)
        return mensagem

    def processar_mensagem(self, conexao):
        mensagem_encriptada = conexao.recv(2048)
        mensagem: str = mensagem_encriptada.decode("utf-8")
        mensagem_d: str = self.desencriptar(mensagem)
        mensagem : dict = ast.literal_eval(mensagem_d)
        instrucao = mensagem['instrução']
        if instrucao == 'Criar Utilizador':
            self.log(f'Solicitado criação de utilizador')
            resposta = self.criar_utilizador(mensagem)
            resposta_encriptada = self.encriptar(str(resposta))

            conexao.send(resposta_encriptada.encode(FORMATO))
            self.log(f'RESPOSTA ENVIADA a Controlador Principal ')
        elif instrucao == 'Alterar Password':
            self.log(f'Solicitado alteração de Password')
            resposta = self.alterar_password(mensagem)
            resposta_encriptada = self.encriptar(str(resposta))
            conexao.send(resposta_encriptada.encode(FORMATO))
            self.log(f'RESPOSTA ENVIADA a Controlador Principal')
        elif instrucao == 'Alterar Username':
            self.log(f'Solicitado alteração de Username')
            resposta = self.alterar_username(mensagem)
            resposta_encriptada = self.encriptar(str(resposta))
            conexao.send(resposta_encriptada.encode(FORMATO))
            self.log(f'RESPOSTA ENVIADA a Controlador Principal')
        elif instrucao == 'Eliminar Registo':
            self.log(f'Solicitado eliminação de utilizador')
            resposta = self.eliminar_registo(mensagem)
            resposta_encriptada = self.encriptar(str(resposta))
            conexao.send(resposta_encriptada.encode(FORMATO))
            self.log(f'RESPOSTA ENVIADA a Controlador Principal')
        elif instrucao == 'Validar Utilizador':
            self.log(f'Solicitado Validação de Utilizador')
            resposta = self.validar_utilizador(mensagem)
            resposta_encriptada = self.encriptar(str(resposta))
            conexao.send(resposta_encriptada.encode(FORMATO))
            self.log(f'RESPOSTA ENVIADA a Controlador Principal')
        elif instrucao == 'Criar Nota':
            self.log(f'Solicitado criação de nota')
            resposta = self.criar_nota(mensagem)
            resposta_encriptada = self.encriptar(str(resposta))
            conexao.send(resposta_encriptada.encode(FORMATO))
            self.log(f'RESPOSTA ENVIADA a Controlador Principal')
        elif instrucao == 'Guardar Nota':
            self.log(f'Solicitado arquivo de nota')
            resposta = self.guardar_nota(mensagem)
            resposta_encriptada = self.encriptar(str(resposta))
            conexao.send(resposta_encriptada.encode(FORMATO))
            self.log(f'RESPOSTA ENVIADA a Controlador Principal')
        elif instrucao == 'Eliminar Nota':
            self.log(f'Solicitado eliminação de nota')
            resposta = self.eliminar_nota(mensagem)
            resposta_encriptada = self.encriptar(str(resposta))
            conexao.send(resposta_encriptada.encode(FORMATO))
            self.log(f'RESPOSTA ENVIADA a Controlador Principal')
        elif instrucao == 'Mostrar Notas':
            self.log(f'Solicitada a disponibilização de notas')
            resposta : dict = self.mostrar_notas(mensagem)
            self.log(f'{resposta}')
            mensagem = str(resposta)
            mensagem_enc = self.encriptar(mensagem)
            mennsagem_cod = mensagem_enc.encode(FORMATO)
            conexao.send(mennsagem_cod)
            self.log(f'\nRESPOSTA ENVIADA a Controlador Principal \n')

    def criar_utilizador(self, mensagem) -> bool:
        nome_db = mensagem['nome']
        nome = self.encriptar(nome_db)
        username_db = mensagem['username']
        username = self.encriptar(username_db)
        password_db = mensagem['password']
        password = self.encriptar(password_db)
        query = "INSERT INTO utilizador (nome, username, password) VALUES (%s, %s, %s)"
        values = (nome, username, password)
        self.cursor.execute(query, values)
        self.conn.commit()
        self.log(f'Criado utilizador')
        return True

    def alterar_password(self, mensagem) -> bool:
        valida = bool(self.validar_utilizador(mensagem))
        self.log(f'{valida}')
        if (valida == True):
            username_db = mensagem['username']
            username = self.encriptar(username_db)
            n_password_db = mensagem['nova password']
            n_password = self.encriptar(n_password_db)
            query = "UPDATE utilizador SET password = %s WHERE username = %s"
            values = (n_password, username)
            self.cursor.execute(query, values)
            self.conn.commit()
            self.log(f'Alterada Password')
            return True
        else:
            return False
        
    def alterar_username(self, mensagem) -> bool:
        valida = bool(self.validar_utilizador(mensagem))
        self.log(f'{valida}')
        if (valida == True):
            username_db = mensagem['username']
            username = self.encriptar(username_db)
            n_username_db = mensagem['novo username']
            n_username = self.encriptar(n_username_db)
            query = "UPDATE utilizador SET username = %s WHERE username = %s"
            values = (n_username, username)
            self.cursor.execute(query, values)
            self.conn.commit()
            self.log(f'Alterado Username')
            return True
        else:
            return False

    def eliminar_registo(self,mensagem) -> bool:
        if (self.validar_utilizador(mensagem) == True):
            username_db = mensagem['username']
            username = self.encriptar(username_db)
            query = "DELETE FROM utilizador WHERE username = %s"
            values = (username,)
            self.cursor.execute(query, values)
            self.conn.commit()
            self.log(f'Eliminado Utilizador')
            return True

    def validar_utilizador(self,mensagem) -> bool:
        username_db = mensagem['username']
        username = self.encriptar(username_db)
        password_db = mensagem['password']
        password = self.encriptar(password_db)
        values = (username,password)
        query = "SELECT * FROM utilizador WHERE username = %s AND password = %s"
        self.cursor.execute(query, values)
        usuario = self.cursor.fetchone()
        return usuario is not None

    def criar_nota(self, mensagem):
        username_db = mensagem['username']
        username = self.encriptar(username_db)
        values = (username,)
        query = "SELECT id FROM utilizadores WHERE username = %s"
        self.cursor.execute(query, values)
        id_utilizador = self.cursor.fetchone()
        notas_db = mensagem['notas']
        titulo_db = notas_db[1]
        nota_db = notas_db[2]
        titulo = self.encriptar(titulo_db)
        nota = self.encriptar(nota_db)
        query = "INSERT INTO notas (titulo, nota, id_utilizador) VALUES (%s, %s, %s)"
        values = (titulo, nota, id_utilizador)
        self.cursor.execute(query, values)
        self.conn.commit()
        self.log(f'Criada Nota')

    def guardar_nota(self, mensagem):
        username_db = mensagem['username']
        username = self.encriptar(username_db)
        values = (username,)
        query = "SELECT id FROM utilizadores WHERE username = %s"
        self.cursor.execute(query, values)
        id_utilizador = self.cursor.fetchone()
        nota_db = mensagem['notas']
        nota_id = nota_db[0]
        nota_titulo = nota_db[1]
        nota_nota = nota_db[2]
        titulo = self.encriptar(nota_titulo)
        nota = self.encriptar(nota_nota)
        query = "UPDATE notas SET titulo = %s, nota = %s, id_utilizador = %s, WHERE id = %s"
        values = (titulo, nota, id_utilizador, nota_id)
        self.cursor.execute(query, values)
        self.conn.commit()
        self.log(f'Nota Guardada')

    def eliminar_nota(self, mensagem):
        nota_db = mensagem['notas']
        nota_id = nota_db[0]
        query = "DELETE FROM notas WHERE id = %s"
        values = (nota_id,)
        self.cursor.execute(query, values)
        self.conn.commit()
        self.log(f'Nota Eliminada')

    def mostrar_notas(self,mensagem):
        username_db = mensagem['username']
        username = self.encriptar(username_db)
        values = (username,)
        query = "SELECT id FROM utilizadores WHERE username = %s"
        self.cursor.execute(query, values)
        id_utilizador = self.cursor.fetchone()
        notas = []
        query = "SELECT id, titulo, nota FROM nota WHERE id_utilizador = %s"
        values = (id_utilizador,)
        self.cursor.execute(query, values)
        notas_e = self.cursor.fetchall()
        for i in range (0,len(notas_e),3):
            notas.append(i) # id
            notas.append(self.desencriptar(i+1)) # titulo
            notas.append(self.desencriptar(i+3)) # nota
        mensagem['notas'] = notas
        self.log(f'Notas disponibilizadas')
        return mensagem

    def log(self, mensagem):
        # Obtém a informação atual, adiciona a nova mensagem e atualiza o ecrã
        current_log = self.server_log.get()
        updated_log = current_log + mensagem + "\n"
        self.server_log.set(updated_log)

    def atualizar_text_area(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.server_log)

    def encriptar(self, texto: str) -> str:
        chave=5
        return "".join([chr(ord(algo) + chave) for algo in texto])

    def desencriptar(self, texto) -> str:
        chave=5
        return "".join([chr(ord(algo) - chave) for algo in texto])