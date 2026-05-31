import customtkinter as ctk
import sqlite3
import hashlib
from tkinter import messagebox
from Telas.Menus.Iniciar import App

# Paleta de Cores
FUNDO_LOGIN = "#0F172A"
CARD_LOGIN = "#1E293B"
INPUT_LOGIN = "#334155"
BOTAO_LOGIN = "#2563EB"
BOTAO_HOVER = "#1D4ED8"
TEXTO_LOGIN = "#F8FAFC"
PLACEHOLDER = "#CBD5E1"
BORDA_INPUT = "#475569"
DESTAQUE = "#38BDF8"
ERRO = "#EF4444"
SUCESSO = "#22C55E"

def hash_senha(senha: str) -> str:
    """Retorna o SHA-256 da senha em hexadecimal."""
    return hashlib.sha256(senha.encode()).hexdigest()

class Login(ctk.CTk):
    def __init__(self, conn):
        super().__init__()
        self.title("Área de Login")
        self.geometry("380x470")
        self.configure(fg_color=FUNDO_LOGIN)
        self.conn = conn

        card_fundo = ctk.CTkFrame(self, fg_color=CARD_LOGIN, corner_radius=18)
        card_fundo.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.9)

        ctk.CTkLabel(card_fundo, text="Área de Login", font=("Inter", 22, "bold"),
                     text_color=TEXTO_LOGIN).place(relx=0.5, y=30, anchor="center")

        ctk.CTkLabel(card_fundo, text="Usuário", font=("Inter", 22, "bold"),
                     text_color=TEXTO_LOGIN).place(relx=0.5, y=100, anchor="center")

        self.login_user_entrada = ctk.CTkEntry(
            card_fundo, placeholder_text="Usuário",
            placeholder_text_color=PLACEHOLDER, font=("Inter", 15), text_color=TEXTO_LOGIN
        )
        self.login_user_entrada.place(relx=0.5, y=130, anchor="center")

        ctk.CTkLabel(card_fundo, text="Senha", font=("Inter", 22, "bold"),
                     text_color=TEXTO_LOGIN).place(relx=0.5, y=200, anchor="center")

        self.login_senha_entrada = ctk.CTkEntry(
            card_fundo, placeholder_text="Senha", show="*",
            placeholder_text_color=PLACEHOLDER, font=("Inter", 15), text_color=TEXTO_LOGIN
        )
        self.login_senha_entrada.place(relx=0.5, y=230, anchor="center")

        # Enter para logar
        self.login_senha_entrada.bind("<Return>", lambda e: self.verificar_login())

        ctk.CTkButton(card_fundo, text="Entrar", text_color=TEXTO_LOGIN,
                      fg_color=BOTAO_LOGIN, hover_color=BOTAO_HOVER,
                      command=self.verificar_login
                      ).place(relx=0.5, y=300, anchor="center")

        ctk.CTkButton(card_fundo, text="Cancelar", text_color=TEXTO_LOGIN,
                      fg_color=BOTAO_LOGIN, hover_color=BOTAO_HOVER,
                      command=self.destroy
                      ).place(relx=0.5, y=350, anchor="center")

    def verificar_login(self):
        login    = self.login_user_entrada.get().strip()
        password = self.login_senha_entrada.get().strip()

        if not login or not password:
            messagebox.showwarning("Aviso", "Preencha usuário e senha!")
            return

        senha_hash = hash_senha(password)

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, nome, nivel_acesso
            FROM usuarios
            WHERE usuario = ?
            AND senha = ?
            AND ativo = 1
        """, (login, senha_hash))
        resultado = cursor.fetchone()

        if resultado:
            id_usuario, nome_usuario, nivel_acesso = resultado
            print(f"RELATÓRIO: Login realizado — usuário '{nome_usuario}' | nível '{nivel_acesso}'")
            messagebox.showinfo("Sucesso", f"Bem-vindo, {nome_usuario}!")
            self.destroy()
            app = App(self.conn, nivel_acesso=nivel_acesso, nome_usuario=nome_usuario)
            app.mainloop()
        else:
            # Tenta sem hash (compatibilidade com senhas antigas em texto puro)
            cursor.execute("""
                SELECT id, nome, nivel_acesso
                FROM usuarios
                WHERE usuario = ?
                AND senha = ?
                AND ativo = 1
            """, (login, password))
            resultado = cursor.fetchone()

            if resultado:
                id_usuario, nome_usuario, nivel_acesso = resultado
                # Atualiza automaticamente para hash
                cursor.execute(
                    "UPDATE usuarios SET senha = ? WHERE id = ?",
                    (senha_hash, id_usuario)
                )
                self.conn.commit()
                print(f"RELATÓRIO: Senha de '{nome_usuario}' migrada para hash automaticamente.")
                messagebox.showinfo("Sucesso", f"Bem-vindo, {nome_usuario}!")
                self.destroy()
                app = App(self.conn, nivel_acesso=nivel_acesso, nome_usuario=nome_usuario)
                app.mainloop()
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos!")