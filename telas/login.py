import customtkinter as ctk
import sqlite3

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