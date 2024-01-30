import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from pathlib import Path
from ttkbootstrap.toast import ToastNotification
from controllers.controller import UtilizadorActivo as u
from controllers.controller import ConexaoControlador as c

utilizador_ativo = None
user_ativo = None

PATH = Path(__file__).absolute().parent

class Notlar(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # Use o estilo ttkbootstrap
        style = Style(theme='superhero')
        style.configure('.', font=('Helvetica', 10))  # Ajuste a fonte conforme necessário

        self.controlador = Controlador(self)
        self.control_frame = ControlFrame(self.controlador)
        self.control_frame.pack()

        # Mostra a página inicial
        self.controlador.mostrar_pagina(MenuInicial)

        self.mainloop()

class ControlFrame(ttk.Frame):
    def __init__(self, controlador):
        super().__init__(controlador.aplicacao)

        self.frames = {}
        for F in (MenuInicial, MenuRegisto, MenuLogin, MenuAlterações, MenuNotas, MenuAlterarUsername, MenuAlterarPassword):
            frame = F(controlador)
            self.frames[F] = frame

        self.show_frame(MenuInicial)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MenuInicial(ttk.Frame):
    def __init__(self, controlador):
        super().__init__(controlador.aplicacao)
        self.controlador = controlador

        # Logo
        logo = ttk.PhotoImage(file= PATH /'notebook-64.png')
        logo_label = ttk.Label(self, image=logo)
        logo_label.image = logo  # Garante que a imagem não é coletada pelo garbage collector
        logo_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        # Título da App
        titulo_label = ttk.Label(self, text="Notlar", font=('Bradley Hand ITC', 36, 'bold'))
        titulo_label.grid(row=1, column=1, sticky="w", padx=10, pady=40)

        # Frase
        frase_label = ttk.Label(self, text="O seu Bloco de Notas Virtual", font=('Comic Sans MS', 16))
        frase_label.grid(row=1, column=2, sticky="e", padx=10, pady=40)

        # Botões
        btn_registo = ttk.Button(self, text="Registo", command=lambda: self.controlador.mostrar_pagina(MenuRegisto), style='light-outline.TButton')
        btn_login = ttk.Button(self, text="Login", command=lambda: self.controlador.mostrar_pagina(MenuValidacao), style='success-outline.TButton')
        btn_sair = ttk.Button(self, text="Sair", command=self.controlador.aplicacao.destroy, style='danger-outline.TButton')

        btn_registo.grid(row=40, column=5, padx=10, pady=10)
        btn_login.grid(row=40, column=6, padx=10, pady=10)
        btn_sair.grid(row=45, column=6, padx=10, pady=10)

        # Rótulo "Escolha uma das opções"
        escolha_label = ttk.Label(self, text="Escolha a sua opção", font=('Bradley Hand ITC', 16, 'bold'))
        escolha_label.grid(row=38, column=5, columnspan=3, pady=(175, 5))

class MenuRegisto(ttk.Frame):
    def __init__(self, controlador):
        super().__init__(controlador.aplicacao)
        self.controlador = controlador

        # Logo e Título da App
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="NW")

        logo = ttk.PhotoImage(file=PATH / 'notebook-64.png')
        logo_label = ttk.Label(top_frame, image=logo)
        logo_label.image = logo
        logo_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        titulo_label = ttk.Label(top_frame, text="Notlar", font=('Bradley Hand ITC', 36, 'bold'))
        titulo_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        # Rótulos e entradas para obter Nome, Username e Password
        input_frame = ttk.Frame(self)
        input_frame.grid(row=1, column=0, columnspan=2)

        ttk.Label(input_frame, text="Nome:").pack(pady=5)
        self.entry_nome = ttk.Entry(input_frame)
        self.entry_nome.pack(pady=5)

        ttk.Label(input_frame, text="Username:").pack(pady=5)
        self.entry_username = ttk.Entry(input_frame)
        self.entry_username.pack(pady=5)

        ttk.Label(input_frame, text="Password:").pack(pady=5)
        self.entry_password = ttk.Entry(input_frame, show="*")  # Utilizando show="*" para esconder a password
        self.entry_password.pack(pady=5)
        
        ttk.Label(input_frame, text="Confirmar Password:").pack(pady=5)
        self.entry_confirm_password = ttk.Entry(input_frame, show="*")  # Utilizando show="*" para esconder a password
        self.entry_confirm_password.pack(pady=5)

        # Botão para submeter o registo
        btn_registar = ttk.Button(self, text="Registar", style='success-outline.TButton', command=self.validar_registo)
        btn_registar.grid(row=2, column=0, columnspan=2, pady=10)

        # Botão para voltar ao Menu Inicial
        btn_voltar = ttk.Button(self, text="Voltar ao Menu Inicial", style='secondary-outline.TButton', command=lambda: self.controlador.mostrar_pagina(MenuInicial))
        btn_voltar.grid(row=3, column=0, columnspan=2, pady=10)

    def validar_registo(self):
        senha = self.entry_password.get()
        confirmar_senha = self.entry_confirm_password.get()
        if senha == confirmar_senha:
            dados = u()
            dados.mensagem['instrução'] = 'Criar Utilizador'
            dados.mensagem['nome'] = f'{self.entry_nome.get()}'
            dados.mensagem['username'] = f'{self.entry_username.get()}'
            dados.mensagem['password'] = f'{self.entry_password.get()}'
            mensagem = str(dados.mensagem)
            mensagem_c = c.encriptar_cliente(mensagem)
            conexao = c()
            if (conexao.tratamento_mensagem(mensagem_c) == True):
                # Notificação de sucesso
                toast = ToastNotification(
                    title="Registo Bem-sucedido", 
                    message="O utilizador foi registado com sucesso!",
                    position=(400, 300, "ne"),
                    duration=5000,
                bootstyle=SUCCESS
                )
                toast.show_toast()
                self.controlador.mostrar_pagina(MenuInicial)
        else:
            # Notificação de erro
            toast = ToastNotification(
                title="Erro no Registo",
                message="As senhas não coincidem. Por favor, tente novamente.",
                position=(400, 300, "ne"),
                duration=5000,
                bootstyle=DANGER
            )
            toast.show_toast()
            # Limpar campos de senha
            self.entry_password.delete(0, tk.END)
            self.entry_confirm_password.delete(0, tk.END)

class MenuValidacao(ttk.Frame):
    def __init__(self, controlador):
        super().__init__(controlador.aplicacao)
        self.controlador = controlador

        # Logo e Título da App
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="NW")

        logo = ttk.PhotoImage(file=PATH / 'notebook-64.png')
        logo_label = ttk.Label(top_frame, image=logo)
        logo_label.image = logo
        logo_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        titulo_label = ttk.Label(top_frame, text="Notlar", font=('Bradley Hand ITC', 36, 'bold'))
        titulo_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        # Rótulos e entradas para obter Username e Password
        input_frame = ttk.Frame(self)
        input_frame.grid(row=1, column=0, columnspan=2)

        ttk.Label(input_frame, text="Username:").pack(pady=5)
        self.entry_username = ttk.Entry(input_frame)
        self.entry_username.pack(pady=5)

        ttk.Label(input_frame, text="Password:").pack(pady=5)
        self.entry_password = ttk.Entry(input_frame, show="*")  # Utilizando show="*" para esconder a password
        self.entry_password.pack(pady=5)

        # Botão para validar os dados
        btn_validar = ttk.Button(self, text="Validar", style='success-outline.TButton', command=self.validar)
        btn_validar.grid(row=2, column=0, columnspan=2, pady=10)

        # Botão para voltar ao Menu Inicial
        btn_voltar = ttk.Button(self, text="Voltar ao Menu Inicial", style='secondary-outline.TButton', command=lambda: self.controlador.mostrar_pagina(MenuInicial))
        btn_voltar.grid(row=3, column=0, columnspan=2, pady=10)

    def validar(self):
        dados = u()
        dados.mensagem['servidor'] = 'utilizadores'
        dados.mensagem['instrucao'] = 'Validar Utilizador'
        dados.mensagem['username'] = f'{self.entry_username.get()}'
        dados.mensagem['password'] = f'{self.entry_password.get()}'
        mensagem = str(dados.dados_mensagem())
        conexao = c()
        if (conexao.tratamento_mensagem(mensagem) == True):
            global utilizador_ativo
            global user_ativo
            utilizador_ativo = dados.mensagem['nome']
            user_ativo = dados.mensagem['username']
            self.mostrar_toast_sucesso()
            self.controlador.mostrar_pagina(MenuLogin)
        else:
            self.mostrar_toast_erro()
            self.limpar_campos()

    def mostrar_toast_sucesso(self):
        # Notificação de Sucesso no Login
        toast = ToastNotification(
            title="Acesso Validado",
            message="Acesso Correcto. Disponha das suas opções",
            position=(400, 300, "ne"),
            alert=True,
            duration=1000,
            bootstyle=SUCCESS
        )
        toast.show_toast()
        
    def mostrar_toast_erro(self):
        # Notificação de Erro
        toast = ToastNotification(
            title="Erro de Validação",
            message="Os dados fornecidos são inválidos. Por favor, tente novamente.",
            position=(400, 300, "ne"),
            alert=True,
            duration=3000,
            bootstyle=WARNING
        )
        toast.show_toast()

    def limpar_campos(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

class MenuLogin(ttk.Frame):
    def __init__(self, controlador):
        super().__init__(controlador.aplicacao)
        self.controlador = controlador

        # Logo e Título da App
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=10)

        logo = ttk.PhotoImage(file=PATH / 'notebook-64.png')
        logo_label = ttk.Label(top_frame, image=logo)
        logo_label.image = logo
        logo_label.grid(row=1, column=0, padx=10, pady=10)

        titulo_label = ttk.Label(top_frame, text="Notlar", font=('Bradley Hand ITC', 36, 'bold'))
        titulo_label.grid(row=1, column=1, padx=10, pady=40)

        # Mensagem de boas-vindas
        mensagem_boas_vindas = ttk.Label(self, text=f"Bem-vindo, {utilizador_ativo}", font=('Arial', 16))
        mensagem_boas_vindas.grid(row=1, column=1, columnspan=2, pady=10)

        # Novo frame para os botões de acção
        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(row=6, column=3, columnspan=2)

        btn_consultar_notas = ttk.Button(buttons_frame, text="As suas Notas", style='success-outline.TButton',command=lambda: self.controlador.mostrar_pagina(MenuNotas))
        btn_consultar_notas.pack(pady=20)

        btn_alterar_dados = ttk.Button(buttons_frame, text="Alterar dados de Registo", style='info-outline.TButton',command=lambda: self.controlador.mostrar_pagina(MenuAlterações))
        btn_alterar_dados.pack(pady=10)

        # Novo frame para os botões de retorno
        buttonsr_frame = ttk.Frame(self)
        buttonsr_frame.grid(row=20, column=4, columnspan=2, pady=20)

        btn_voltar = ttk.Button(buttonsr_frame, text="Sign out", style='danger-outline.TButton',command=lambda: self.controlador.mostrar_pagina(MenuInicial))
        btn_voltar.pack(side='left', padx=10, pady=30)

        btn_sair = ttk.Button(buttonsr_frame, text="Sair", style='secondary-outline.TButton',command=self.controlador.aplicacao.destroy)
        btn_sair.pack(side='left', padx=10)

        # Mensagem para escolher a opção
        mensagem_escolher_opcao = ttk.Label(self, text="Escolha a sua opção:", font=('Bradley Hand ITC', 16, 'bold'))
        mensagem_escolher_opcao.grid(row=4, column=0, columnspan=2, pady=10)

class MenuAlterações(ttk.Frame):
    def __init__(self, controlador):
        super().__init__(controlador.aplicacao)
        self.controlador = controlador

        # Logo e Título da App
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=10)

        logo = ttk.PhotoImage(file=PATH / 'notebook-64.png')
        logo_label = ttk.Label(top_frame, image=logo)
        logo_label.image = logo
        logo_label.grid(row=1, column=0, padx=10, pady=10)

        titulo_label = ttk.Label(top_frame, text="Notlar", font=('Bradley Hand ITC', 36, 'bold'))
        titulo_label.grid(row=1, column=1, padx=10, pady=40)

        # Novo frame para os botões de acção
        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(row=4, column=3, columnspan=2, padx = 10)

        btn_consultar_notas = ttk.Button(buttons_frame, text="Alterar Username", style='success-outline.TButton',command=lambda: self.controlador.mostrar_pagina(MenuAlterarUsername))
        btn_consultar_notas.pack(pady=20)

        btn_alterar_dados = ttk.Button(buttons_frame, text="Alterar Password", style='info-outline.TButton',command=lambda: self.controlador.mostrar_pagina(MenuAlterarPassword))
        btn_alterar_dados.pack(pady=10)

        # Novo frame para os botões de retorno
        buttonsr_frame = ttk.Frame(self)
        buttonsr_frame.grid(row=20, column=4, columnspan=5, pady=20)
        
        btn_voltar = ttk.Button(buttonsr_frame, text="Voltar ao Menu Anterior", style='light-outline.TButton',command=lambda: self.controlador.mostrar_pagina(MenuLogin))
        btn_voltar.pack(side='left', padx=10, pady=30)

        btn_voltar = ttk.Button(buttonsr_frame, text="Sign out", style='danger-outline.TButton',command=lambda: self.controlador.mostrar_pagina(MenuInicial))
        btn_voltar.pack(side='left', padx=10)

        btn_sair = ttk.Button(buttonsr_frame, text="Sair", style='secondary-outline.TButton',command=self.controlador.aplicacao.destroy)
        btn_sair.pack(side='left', padx=10)

        # Mensagem para escolher a opção
        mensagem_escolher_opcao = ttk.Label(self, text="Escolha a sua opção:", font=('Bradley Hand ITC', 16, 'bold'))
        mensagem_escolher_opcao.grid(row=4, column=0, columnspan=2, pady=10, padx = 5)

class MenuNotas(ttk.Frame):
    def __init__(self, controlador):
        super().__init__(controlador.aplicacao)
        self.controlador = controlador

        self.id_notas =[]
        dados = u()
        dados.mensagem['instrução'] = 'Mostrar Notas'
        dados.mensagem['username'] = user_ativo
        mensagem = str(dados.mensagem)
        mensagem_c = c.encriptar_cliente(mensagem)
        conexao = c()
        dic = conexao.tratamento_mensagem(mensagem_c)
        notas = dic['notas']

        self.total_n = len(notas)

        # Logo e Título da App
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="NW")

        logo = ttk.PhotoImage(file=PATH / 'notebook-64.png')
        logo_label = ttk.Label(top_frame, image=logo)
        logo_label.image = logo
        logo_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        titulo_label = ttk.Label(top_frame, text="Notlar", font=('Bradley Hand ITC', 36, 'bold'))
        titulo_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        #Criação do notebook tem de ir para 
        # Criação do Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, columnspan=20, sticky="NESW", padx=1, pady=1)

        # Itera sobre a lista de notas e adiciona cada par de notas ao Notebook
        for i in range(0, len(notas), 3):
            id_nota = notas[i]
            titulo_nota = notas[i + 1]
            conteudo_nota = notas[i + 2]

            frame_nota = ttk.Frame(self.notebook)
            self.notebook.add(frame_nota, text=titulo_nota)

            # Adicione widgets para exibir a nota dentro do frame_nota
            entry_titulo = ttk.Entry(frame_nota, font=('Arial', 14, 'bold'), justify='center', width=30)
            entry_titulo.insert(0, titulo_nota)
            entry_titulo.grid(row=0, column=0, columnspan=50, padx=5, pady=5)

            text_nota = tk.Text(frame_nota, wrap=tk.WORD, height=10, width=125)
            text_nota.insert(tk.END, conteudo_nota)
            text_nota.grid(row=1, column=0,columnspan=50, padx=5, pady=5)

            btn_guardar_nota = ttk.Button(frame_nota, text="Eliminar Nota",style='secondary-outline.TButton', command=lambda i=id_nota : self.eliminar_nota(i))
            btn_guardar_nota.grid(row=2, column=0, pady=1)
            
            btn_nova_nota = ttk.Button(frame_nota, text="Guardar Nota", style='warning-outline.TButton',command=self.adicionar_nova_nota)
            btn_nova_nota.grid(row=2, column=24, sticky='E')
            # Botão para adicionar nova nota
            
            btn_nova_nota = ttk.Button(frame_nota, text="Criar nova Nota", style='success-outline.TButton',command=self.adicionar_nova_nota)
            btn_nova_nota.grid(row=2, column=48, sticky='E')
            
            

       # Novo frame para os botões de retorno
        buttonsr_frame = ttk.Frame(self)
        buttonsr_frame.grid(row=20, column=0, columnspan=5, pady=5)
        
        btn_voltar = ttk.Button(buttonsr_frame, text="Voltar ao Menu Anterior", style='light-outline.TButton',command=lambda: self.controlador.mostrar_pagina(MenuLogin))
        btn_voltar.pack(side='left', padx=10, pady=30)

        btn_voltar = ttk.Button(buttonsr_frame, text="Sign out", style='danger-outline.TButton',command=lambda: self.controlador.mostrar_pagina(MenuInicial))
        btn_voltar.pack(side='left', padx=10)

        btn_sair = ttk.Button(buttonsr_frame, text="Sair", style='secondary-outline.TButton',command=self.controlador.aplicacao.destroy)
        btn_sair.pack(side='left', padx=10)



        # Configurar para que a coluna e a linha se expandam conforme o redimensionamento da janela
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Botão para adicionar nova nota
        

    def adicionar_nova_nota(self):
        id_nota = self.total_n + 1
        # Cria uma nova aba no notebook para a nova nota
        frame_nova_nota = ttk.Frame(self.notebook)
        self.notebook.add(frame_nova_nota, text="Nova Nota")
        self.notebook.select(frame_nova_nota)

        # Adiciona widgets para a nova nota
        entry_titulo_nova_nota = ttk.Entry(frame_nova_nota, font=('Arial', 14, 'bold'), justify='center', width=30)
        entry_titulo_nova_nota.grid(row=0, column=0, columnspan=50, padx=5, pady=5)
        id_nota = self.id_notas

        text_nova_nota = tk.Text(frame_nova_nota, wrap=tk.WORD, height=10, width=125)
        text_nova_nota.grid(row=1, column=0, columnspan=50, padx=5, pady=5)

        btn_guardar_nova_nota = ttk.Button(frame_nova_nota, text="Eliminar Nota", style='secondary-outline.TButton',
                                           command=lambda i=id_nota : self.eliminar_nota(i))
        btn_guardar_nova_nota.grid(row=2, column=0, pady=1)
        
        btn_nova_nota = ttk.Button(frame_nova_nota, text="Guardar Nota", style='warning-outline.TButton',command=lambda i=id_nota, t=text_nova_nota, e=entry_titulo_nova_nota : self.guardar_nova_nota(i,t,e))
        btn_nova_nota.grid(row=2, column=24, sticky='E')
        
        btn_nova_nota = ttk.Button(frame_nova_nota, text="Criar nova Nota", style='success-outline.TButton',command=lambda t=text_nova_nota, e=entry_titulo_nova_nota : self.adicionar_nova_nota(t,e))
        btn_nova_nota.grid(row=2, column=48, sticky='E')

    def guardar_nova_nota(self, id_nota, text_widget, entry_widget):
        # Obtenha o conteúdo e o título da nova nota
        conteudo_nova_nota = text_widget.get("1.0", tk.END)
        titulo_nova_nota = entry_widget.get()
        id_n = id_nota
        nota = [id_n,titulo_nova_nota,conteudo_nova_nota]
        dados = u()
        dados.mensagem['instrução'] = 'Guardar Nota'
        dados.mensagem['username'] = user_ativo
        dados.mensagem['notas'] = nota
        mensagem = str(dados.mensagem)
        mensagem_c = c.encriptar_cliente(mensagem)
        conexao = c()
        if (conexao.tratamento_mensagem(mensagem_c) == True):
                # Notificação de sucesso
                toast = ToastNotification(
                    title="Nota Guardada", 
                    message="A nota foi arquivada com sucesso!",
                    position=(400, 300, "ne"),
                    duration=5000,
                bootstyle=SUCCESS
                )
                toast.show_toast()
                self.controlador.mostrar_pagina(MenuNotas)
        else:
            # Notificação de erro
            toast = ToastNotification(
                title="Erro no processamento",
                message="Por favor, tente novamente.",
                position=(400, 300, "ne"),
                duration=5000,
                bootstyle=DANGER
            )
            toast.show_toast()
            
            
            
            
    def eliminar_nota(self, id_nota):
        # Obtenha o conteúdo e o título da nova nota
        id_n = id_nota
        nota = [str(id_n)]
        dados = u()
        dados.mensagem['instrução'] = 'Eliminar Nota'
        dados.mensagem['username'] = user_ativo
        dados.mensagem['notas'] = nota
        mensagem = str(dados.mensagem)
        mensagem_c = c.encriptar_cliente(mensagem)
        conexao = c()
        if (conexao.tratamento_mensagem(mensagem_c) == True):
                # Notificação de sucesso
                toast = ToastNotification(
                    title="Nota Eliminada", 
                    message="A nota foi eliminada com sucesso!",
                    position=(400, 300, "ne"),
                    duration=5000,
                bootstyle=SUCCESS
                )
                toast.show_toast()
                self.controlador.mostrar_pagina(MenuNotas)
        else:
            # Notificação de erro
            toast = ToastNotification(
                title="Erro no processamento",
                message="Por favor, tente novamente.",
                position=(400, 300, "ne"),
                duration=5000,
                bootstyle=DANGER
            )
            toast.show_toast()

class MenuAlterarUsername(ttk.Frame):
    def __init__(self, controlador):
        super().__init__(controlador.aplicacao)
        self.controlador = controlador

        # Logo e Título da App
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="NW")

        logo = ttk.PhotoImage(file=PATH / 'notebook-64.png')
        logo_label = ttk.Label(top_frame, image=logo)
        logo_label.image = logo
        logo_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        titulo_label = ttk.Label(top_frame, text="Notlar", font=('Bradley Hand ITC', 36, 'bold'))
        titulo_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        # Rótulos e entradas para obter Nome, Username e Password
        input_frame = ttk.Frame(self)
        input_frame.grid(row=1, column=0, columnspan=2)

        ttk.Label(input_frame, text="Username Atual:").pack(pady=5)
        self.entry_nome = ttk.Entry(input_frame)
        self.entry_nome.pack(pady=5)

        ttk.Label(input_frame, text="Novo Username:").pack(pady=5)
        self.entry_username = ttk.Entry(input_frame,  show="*")
        self.entry_username.pack(pady=5)

        ttk.Label(input_frame, text="Password:").pack(pady=5)
        self.entry_confirm_password = ttk.Entry(input_frame, show="*")  # Utilizando show="*" para esconder a password
        self.entry_confirm_password.pack(pady=10)

        # Botão para submeter o registo
        btn_registar = ttk.Button(self, text="Alterar Username", style='success-outline.TButton', command=self.validar_registo)
        btn_registar.grid(row=2, column=0, columnspan=2, pady=10)

        # Botão para voltar ao Menu Inicial
        btn_voltar = ttk.Button(self, text="Voltar ao Menu Anterior", style='secondary-outline.TButton', command=lambda: self.controlador.mostrar_pagina(MenuAlterações))
        btn_voltar.grid(row=3, column=0, columnspan=2, pady=10)

    def validar_registo(self):
        senha = self.entry_password.get()
        confirmar_senha = self.entry_confirm_password.get()
        if senha == confirmar_senha:
            dados = u()
            dados.mensagem['instrução'] = 'Validar Registo'
            dados.mensagem['nome'] = f'{self.entry_nome.get()}'
            dados.mensagem['username'] = f'{self.entry_username.get()}'
            dados.mensagem['password'] = f'{self.entry_password.get()}'
            mensagem = str(dados.mensagem)
            mensagem_c = c.encriptar_cliente(mensagem)
            conexao = c()
            if (conexao.tratamento_mensagem(mensagem_c) == True):
                # Notificação de sucesso
                toast = ToastNotification(
                    title="Registo Bem-sucedido", 
                    message="O utilizador foi registado com sucesso!",
                    position=(400, 300, "ne"),
                    duration=5000,
                bootstyle=SUCCESS
                )
                toast.show_toast()
                self.controlador.mostrar_pagina(MenuInicial)
        else:
            # Notificação de erro
            toast = ToastNotification(
                title="Erro no Registo",
                message="As senhas não coincidem. Por favor, tente novamente.",
                position=(400, 300, "ne"),
                duration=5000,
                bootstyle=DANGER
            )
            toast.show_toast()
            # Limpar campos de senha
            self.entry_password.delete(0, tk.END)
            self.entry_confirm_password.delete(0, tk.END)

class MenuAlterarPassword(ttk.Frame):
    def __init__(self, controlador):
        super().__init__(controlador.aplicacao)
        self.controlador = controlador

        # Logo e Título da App
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="NW")

        logo = ttk.PhotoImage(file=PATH / 'notebook-64.png')
        logo_label = ttk.Label(top_frame, image=logo)
        logo_label.image = logo
        logo_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        titulo_label = ttk.Label(top_frame, text="Notlar", font=('Bradley Hand ITC', 36, 'bold'))
        titulo_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        # Rótulos e entradas para obter Nome, Username e Password
        input_frame = ttk.Frame(self)
        input_frame.grid(row=1, column=0, columnspan=2)

        ttk.Label(input_frame, text="Username:").pack(pady=5)
        self.entry_nome = ttk.Entry(input_frame)
        self.entry_nome.pack(pady=5)

        ttk.Label(input_frame, text="Password:").pack(pady=5)
        self.entry_username = ttk.Entry(input_frame,  show="*")
        self.entry_username.pack(pady=5)

        ttk.Label(input_frame, text="Nova Password:").pack(pady=5)
        self.entry_password = ttk.Entry(input_frame, show="*")  # Utilizando show="*" para esconder a password
        self.entry_password.pack(pady=5)
        
        ttk.Label(input_frame, text="Confirmar Nova Password:").pack(pady=5)
        self.entry_confirm_password = ttk.Entry(input_frame, show="*")  # Utilizando show="*" para esconder a password
        self.entry_confirm_password.pack(pady=5)

        # Botão para submeter o registo
        btn_registar = ttk.Button(self, text="Alterar Password", style='success-outline.TButton', command=self.validar_registo)
        btn_registar.grid(row=2, column=0, columnspan=2, pady=10)

        # Botão para voltar ao Menu Inicial
        btn_voltar = ttk.Button(self, text="Voltar ao Menu Anterior", style='secondary-outline.TButton', command=lambda: self.controlador.mostrar_pagina(MenuAlterações))
        btn_voltar.grid(row=3, column=0, columnspan=2, pady=10)

    def validar_registo(self):
        senha = self.entry_password.get()
        confirmar_senha = self.entry_confirm_password.get()

        if senha == confirmar_senha:
            mensagem = c.criar_mensagem()
            mensagem['Servidor'] = 'utilizadores'
            mensagem['instrução'] = 'Criar_Utilizador'
            mensagem['Nome'] = f'{self.entry_nome.get()}'
            mensagem['Username'] = f'{self.entry_username.get()}'
            mensagem['Password'] = f'{senha}'
            c.mensagens_user(c.comunicacao(mensagem))

            # Notificação de sucesso
            toast = ToastNotification(
                title="Registo Bem-sucedido",
                message="O utilizador foi registado com sucesso!",
                position=(400, 300, "ne"),
                duration=3000,
                bootstyle=SUCCESS
            )
            toast.show_toast()

            # Limpar campos
            self.entry_nome.delete(0, tk.END)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_confirm_password.delete(0, tk.END)
        else:
            # Notificação de erro
            toast = ToastNotification(
                title="Erro no Registo",
                message="As senhas não coincidem. Por favor, tente novamente.",
                position=(400, 300, "ne"),
                duration=3000,
                bootstyle=DANGER
            )
            toast.show_toast()
            # Limpar campos de senha
            self.entry_password.delete(0, tk.END)
            self.entry_confirm_password.delete(0, tk.END)

class Controlador:
    def __init__(self, aplicacao):
        self.aplicacao = aplicacao
        self.frames = {}

    def mostrar_pagina(self, page_class):
        frame = self.frames.get(page_class)
        if not frame:
            frame = page_class(self)
            self.frames[page_class] = frame
        for other_page_class in self.frames:
            if other_page_class != page_class:
                self.frames[other_page_class].pack_forget()
        frame.pack()

