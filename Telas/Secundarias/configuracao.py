import sqlite3
import customtkinter as ctk
from tkinter import ttk, messagebox

# Paleta de Cores
FUNDO = "#F8FAFC"
MENU_LATERAL = "#E2E8F0"
TOPO = "#FFFFFF"
CARDS = "#FFFFFF"
CARD_HOVER = "#F1F5F9"
TABELAS = "#FFFFFF"
LINHA_PAR = "#F8FAFC"
LINHA_IMPAR = "#EEF2F7"
HOVER_TABELA = "#DBEAFE"
BOTOES = "#2563EB"
BOTOES_HOVER = "#1D4ED8"
BOTAO_SUCESSO = "#16A34A"
BOTAO_SUCESSO_HOVER = "#15803D"
BOTAO_ALERTA = "#D97706"
BOTAO_ALERTA_HOVER = "#B45309"
BOTAO_ERRO = "#DC2626"
BOTAO_ERRO_HOVER = "#B91C1C"
INPUT = "#FFFFFF"
INPUT_BORDA = "#CBD5E1"
INPUT_FOCUS = "#93C5FD"
TEXTO = "#0F172A"
TEXTO_SECUNDARIO = "#475569"
TEXTO_PLACEHOLDER = "#94A3B8"
DIVISORIA = "#E2E8F0"
SUCESSO = "#22C55E"
ERRO = "#EF4444"
AVISO = "#F59E0B"
SCROLLBAR = "#CBD5E1"

def configuracoes(self):
    config = ctk.CTkToplevel(self)
    config.title("Configurações")
    config.geometry("600x450")
    config.attributes("-topmost", True)
    config.grab_set()
    config.iconbitmap("imagens/icone_configuracoes.png")
    
    topo = ctk.CTkFrame(config, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(config, corner_radius=0, fg_color="white")
    resto.pack(fill="both", expand=True)
    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                    text="Configurações").place(relx=0.5, rely=0.5, anchor="center")
    
    
    print("RELATÓRIO: Tela de Configurações carregado.")
    
