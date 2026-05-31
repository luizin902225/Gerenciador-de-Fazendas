import sqlite3
import customtkinter as ctk
from tkinter import ttk, messagebox
from funcoes.animais import animais_qnt
from funcoes.estoque import estoque_qnt
from funcoes.funcionarios import funcionarios_qnt
from funcoes.maquinas import maquinas_qnt
from Telas.Secundarias.Lotes import qnt_lotes

# Paleta de Cores
FUNDO = "#F8FAFC"              # Fundo geral
MENU_LATERAL = "#E2E8F0"       # Sidebar
TOPO = "#FFFFFF"               # Barra superior
CARDS = "#FFFFFF"              # Cards
CARD_HOVER = "#F1F5F9"
TABELAS = "#FFFFFF"
LINHA_PAR = "#F8FAFC"
LINHA_IMPAR = "#EEF2F7"
HOVER_TABELA = "#DBEAFE"
BOTOES = "#2563EB"             # Azul principal
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

class PerfildaFazenda(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color=FUNDO)
        self.controller = controller
        self.conn = controller.conn
        self.configure(fg_color="transparent")
        
        topo = ctk.CTkFrame(self, fg_color=MENU_LATERAL, corner_radius=0, height=75)
        topo.pack(fill="x")
        meio = ctk.CTkFrame(self, fg_color=FUNDO, corner_radius=0)
        meio.pack(fill="both", expand=True)
        
        # Titulo
        
        titulo_pagina = ctk.CTkLabel(topo, text="Perfil da Fazenda", fg_color="transparent", font=("Inter", 20, "bold"), text_color=TEXTO)
        titulo_pagina.place(anchor="center", relx=0.5, rely=0.5)
        
        # Labels de Dados Simples
        frame_botoes = ctk.CTkFrame(meio, fg_color="transparent")
        frame_botoes.pack(side="top", fill="x")
        
        animais = ctk.CTkFrame(frame_botoes, fg_color="DarkGray", height=100, width=200)
        animais.pack(side="left", padx=10, pady=10)
        
        funcionarios = ctk.CTkFrame(frame_botoes, fg_color="DarkGray", height=100, width=200)
        funcionarios.pack(side="left", padx=10, pady=10)
        
        maquinas = ctk.CTkFrame(frame_botoes, fg_color="DarkGray", height=100, width=200)
        maquinas.pack(side="left", padx=10, pady=10)
        
        produtos = ctk.CTkFrame(frame_botoes, fg_color="DarkGray", height=100, width=200)
        produtos.pack(side="left", padx=10, pady=10)
        
        lotes = ctk.CTkFrame(frame_botoes, fg_color="DarkGray", height=100, width=200)
        lotes.pack(side="left", padx=10, pady=10)
        
        # Labels dentro dos frames
        
        qnt_animais = animais_qnt()
        qnt_estoque = estoque_qnt()
        qnt_funcionarios = funcionarios_qnt()
        qnt_maquinas = maquinas_qnt()
        qnt_lote = qnt_lotes()
        
        # Animais
    
        ctk.CTkLabel(animais, text=f"{qnt_animais}", font=("Inter", 40, "bold"), text_color="black").place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(animais, text="Quantidade de animais", font=("Inter", 15), text_color=TEXTO).place(relx=0.5, rely=0.85, anchor="center")
        
        # Estoque 
        
        ctk.CTkLabel(produtos, text=f"{qnt_estoque}", font=("Inter", 40, "bold"), text_color="black").place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(produtos, text="Quantidade de produtos", font=("Inter", 15), text_color=TEXTO).place(relx=0.5, rely=0.85, anchor="center")
        
        # Funcionários 
        
        ctk.CTkLabel(funcionarios, text=f"{qnt_funcionarios}", font=("Inter", 40, "bold"), text_color="black").place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(funcionarios, text="Quantidade de funcionários", font=("Inter", 15), text_color=TEXTO).place(relx=0.5, rely=0.85, anchor="center")

        # Máquinas
        
        ctk.CTkLabel(maquinas, text=f"{qnt_maquinas}", font=("Inter", 40, "bold"), text_color="black").place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(maquinas, text="Quantidade de máquinas", font=("Inter", 15), text_color=TEXTO).place(relx=0.5, rely=0.85, anchor="center")
        
        # Lotes
        
        ctk.CTkLabel(lotes, text=f"{qnt_lote}", font=("Inter", 40, "bold"), text_color="black").place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(lotes, text="Quantidade de lotes", font=("Inter", 15), text_color=TEXTO).place(relx=0.5, rely=0.85, anchor="center")
        
        titulos = [
            ("Nome da Fazenda:", 20, 150),
            ("Dono da Fazenda:", 20, 200),
            ("Data de Fundação:", 20, 250),
            ("Tamanho:", 20, 300),
            ("Endereço:", 20, 350)
        ]
        
        for nome, x, y in titulos:
            ctk.CTkLabel(meio, text=nome, font=("Inter", 18, "bold"), text_color="black").place(x=x, y=y)
        
        dados = self.dados_fazenda()
        
        nome_fazenda = dados[0]
        tamanho = dados[1]
        endereco = dados[2]
        data_fundacao = dados[3]
        dono = dados[4]
        
        dados = [
            (f"{nome_fazenda}", 190, 150),
            (f"{dono}", 180, 200),
            (f"{data_fundacao}", 190, 250),
            (f"{tamanho}", 120, 300),
            (f"{endereco}", 120, 350)
        ]
        
        for nome, x, y in dados:
            ctk.CTkLabel(meio, text=nome, font=("Inter", 18), text_color="black").place(x=x, y=y)
    
    def dados_fazenda(self):
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT nome_fazenda, printf('%.0f Hectares', tamanho) as tamanho, endereco, data_fundacao, dono FROM fazenda")
        dados = cursor.fetchone()
        
        conn.close()
        return dados
        