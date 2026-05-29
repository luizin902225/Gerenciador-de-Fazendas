import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from Telas.Menus.Iniciar import App
# Paleta de Cores

FUNDO_LOGIN = "#0F172A"          # Fundo principal escuro
CARD_LOGIN = "#1E293B"           # Card do login
INPUT_LOGIN = "#334155"          # Campos
BOTAO_LOGIN = "#2563EB"          # Azul principal
BOTAO_HOVER = "#1D4ED8"          # Hover do botão
TEXTO_LOGIN = "#F8FAFC"          # Texto branco suave
PLACEHOLDER = "#CBD5E1"          # Placeholder
BORDA_INPUT = "#475569"          # Bordas sutis
DESTAQUE = "#38BDF8"             # Azul claro destaque
ERRO = "#EF4444"                 # Vermelho erro
SUCESSO = "#22C55E"              # Verde sucesso

class Login(ctk.CTk):
    def __init__(self, conn):
        super().__init__()
        self.title("Área de Login")
        self.geometry("380x470")
        self.configure(fg_color=FUNDO_LOGIN)
        self.conn = conn
        
        card_fundo = ctk.CTkFrame(self, fg_color=CARD_LOGIN, corner_radius=18)
        card_fundo.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.9)
        
        title = ctk.CTkLabel(card_fundo, text="Área de Login", font=("Inter", 22, "bold"), text_color=TEXTO_LOGIN)
        title.place(relx=0.5, y=30, anchor="center")
        
        login_user_label = ctk.CTkLabel(card_fundo, text="Usuário", font=("Inter", 22, "bold"), text_color=TEXTO_LOGIN)
        login_user_label.place(relx=0.5, y=100, anchor="center")
        
        self.login_user_entrada = ctk.CTkEntry(card_fundo, placeholder_text="Usuário", placeholder_text_color=PLACEHOLDER, font=("Inter", 15), text_color=TEXTO_LOGIN)
        self.login_user_entrada.place(relx=0.5, y=130, anchor="center")
        
        login_senha_label = ctk.CTkLabel(card_fundo, text="Senha", font=("Inter", 22, "bold"), text_color=TEXTO_LOGIN)
        login_senha_label.place(relx=0.5, y=200, anchor="center")
        
        self.login_senha_entrada = ctk.CTkEntry(card_fundo, placeholder_text="Senha", placeholder_text_color=PLACEHOLDER, font=("Inter", 15), text_color=TEXTO_LOGIN)
        self.login_senha_entrada.place(relx=0.5, y=230, anchor="center")
        
        btn_login = ctk.CTkButton(card_fundo, text="Entrar", text_color=TEXTO_LOGIN,
                                    fg_color=BOTAO_LOGIN, hover_color=BOTAO_HOVER,
                                    command= self.verificar_login)
        btn_login.place(relx=0.5, y=300, anchor="center")
        
        btn_cancelar = ctk.CTkButton(card_fundo, text="Cancelar", text_color=TEXTO_LOGIN,
                                        fg_color=BOTAO_LOGIN, hover_color=BOTAO_HOVER,
                                        command= lambda: self.destroy())
        btn_cancelar.place(relx=0.5, y=350, anchor="center")
    
    def verificar_login(self):
        login = self.login_user_entrada.get()
        password = self.login_senha_entrada.get()
        
        if login == "" or password == "":
            messagebox.showwarning("Aviso", "Preencha usuário e senha!")
            
            return

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE usuario = ?
            AND senha = ?
        """, (login, password))
        resultado = cursor.fetchone()
        self.conn.close()
        
        if resultado:
            messagebox.showinfo("Sucesso", "Login realizado!")
            self.destroy()
            app = App(self.conn)
            app.mainloop()

        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")
            return
