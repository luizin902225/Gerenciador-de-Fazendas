import customtkinter as ctk
import sqlite3
import time
from telas.MenuAnimais import MenuAnimais
from telas.MenuMaquinas import MenuMaquinas
from telas.MenuEstoque import MenuEstoque
from telas.MenuFuncionarios import MenuFuncionarios
from funcoes.animais import *
from funcoes.maquinas import *
from funcoes.estoque import *
from funcoes.funcionarios import *


data = time.strftime("%d/%m/%Y")

# ====

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

# ======

class App(ctk.CTk):
    def __init__(self, conn):
        super().__init__()
        self.title("Gerenciamento de Fazenda - v0.1")
        self.geometry("1300x800")
        self.configure(fg_color=FUNDO)
        self.conn = conn
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        

        self.lateral = ctk.CTkFrame(self, fg_color=MENU_LATERAL, corner_radius=0)
        self.lateral.grid(row=0, column=0, sticky="nsew")
        self.lateral.grid_propagate(False)
        self.configurar_menu_lateral()
        
        lateral_frame = ctk.CTkFrame(self, fg_color=MENU_LATERAL, corner_radius=0, height=10, width=200)
        lateral_frame.place(x=0, y=830)
        
        self.meio = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0, border_width=0)
        self.meio.grid(row=0, column=1, sticky="nsew")
        self.meio.grid_rowconfigure(0, weight=1)      
        self.meio.grid_columnconfigure(0, weight=1)  
        
        self.frames = {}
        for F in (MenuIniciar, MenuAnimais, MenuMaquinas, MenuEstoque, MenuFuncionarios):
            frame = F(self.meio, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela(MenuIniciar)
        
    def configurar_menu_lateral(self):
        lateral_titulo = ctk.CTkFrame(self.lateral, fg_color="transparent", height=50, corner_radius=0)
        lateral_titulo.pack(fill="x")
            
        titulo = ctk.CTkLabel(lateral_titulo, text=" MENU\n PRINCIPAL", font=("Inter", 19, "bold"), text_color=TEXTO, fg_color="transparent", bg_color="transparent")
        titulo.pack(side="left", padx=38, pady=20, anchor="center")

        lateral_botoes = ctk.CTkFrame(self.lateral, fg_color="transparent", corner_radius=0)
        lateral_botoes.pack(pady=10)
            
        botoes = [
            ("Menu Principal", lambda: self.mostrar_tela(MenuIniciar), MENU_LATERAL, "w"),
            ("Animais", lambda: self.mostrar_tela(MenuAnimais), MENU_LATERAL, "w"),
            ("Máquinas", lambda: self.mostrar_tela(MenuMaquinas), MENU_LATERAL, "w"),
            ("Estoque", lambda: self.mostrar_tela(MenuEstoque), MENU_LATERAL, "w"),
            ("Funcionários", lambda: self.mostrar_tela(MenuFuncionarios), MENU_LATERAL, "w"),
            ("Plantações", lambda: print("Plantações"), MENU_LATERAL, "w"),
            ("Produtores Rurais", lambda: print("Produtores"), MENU_LATERAL, "w"),
            ("Sair", lambda: self.destroy(), BOTAO_ERRO, "center")
        ]
            
        for texto, comando, cor, lado in botoes:
            btn = ctk.CTkButton(lateral_botoes,
                                font=("Inter", 17, "bold"),
                                text=texto,
                                width=70,
                                height=50,
                                fg_color=cor,
                                hover_color=SCROLLBAR,
                                text_color=TEXTO,
                                command=comando,
                                anchor=lado)
            btn.pack(padx=10, pady=10, fill="x") 
            
        marcacao_data = ctk.CTkLabel(self.lateral, text=f"{data}", font=("Inter", 18, "bold"), bg_color="transparent", text_color=TEXTO)
        marcacao_data.pack(side="bottom", pady=15)    
        
        print('RELATÓRIO: Menu Lateral funcionando corretamente.')
    
    def mostrar_tela(self, tela):
        frame = self.frames[tela]
        frame.tkraise()

class MenuIniciar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0)
        self.controller = controller
        self.conn = controller.conn
        self.configure(fg_color="#D3D3D3")
        
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        titulo_central = ctk.CTkLabel(self, text="GERENCIAMENTO DA FAZENDA\n v0.1", font=("Segoe UI", 50, "bold"), text_color=TEXTO, fg_color="transparent")
        titulo_central.place(relx=0.5, rely=0.5, anchor="center")
        print('RELATÓRIO: Tela inicial funcionando.')
        
        # Relatório
        
        rel_animais = ctk.CTkFrame(self, fg_color="white", height=100, width=150)
        rel_animais.pack(padx=20, pady=20, side="top", anchor="nw")
        
        quantidade_animais = animais_qnt()
        
        label_rel = ctk.CTkLabel(rel_animais, text_color=TEXTO, text=f"Quantidade\nanimais:\n{quantidade_animais}", font=("Inter", 24, "bold"))
        label_rel.place(relx=0.5, rely=0.5, anchor="center")
        
        rel_animais = ctk.CTkFrame(self, fg_color="white", height=100, width=150)
        rel_animais.pack(padx=20, pady=20, side="top", anchor="nw")
        
        quantidade_maquinas = maquinas_qnt()
        
        label_rel = ctk.CTkLabel(rel_animais, text_color=TEXTO, text=f"Quantidade\nmaquinas:\n{quantidade_maquinas}", font=("Inter", 24, "bold"))
        label_rel.place(relx=0.5, rely=0.5, anchor="center")