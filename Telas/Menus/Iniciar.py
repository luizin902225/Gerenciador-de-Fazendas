import customtkinter as ctk
import sqlite3
import time
from PIL import Image

from Telas.Menus.MenuAnimais import MenuAnimais
from Telas.Menus.MenuMaquinas import MenuMaquinas
from Telas.Menus.MenuEstoque import MenuEstoque
from Telas.Menus.MenuFuncionarios import MenuFuncionarios
from Telas.Menus.PerfilFazenda import PerfildaFazenda
from funcoes.animais import *
from funcoes.maquinas import *
from funcoes.estoque import *
from funcoes.funcionarios import *
from Telas.Secundarias.Lotes import cadastro_lotes
from Telas.Secundarias.configuracao import configuracoes
from Telas.Menus.Utilidades import Utilidades

data = time.strftime("%d/%m/%Y")

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

# ==========================================
# Mapa de permissões por nível de acesso
# Adicione ou remova telas conforme necessário
# ==========================================
PERMISSOES = {
    "admin": [
        MenuAnimais,
        MenuMaquinas,
        MenuEstoque,
        MenuFuncionarios,
        PerfildaFazenda,
        Utilidades
    ],
    "gerente": [
        MenuAnimais,
        MenuMaquinas,
        MenuEstoque,
        MenuFuncionarios,
        PerfildaFazenda,
    ],
    "operador": [
        MenuAnimais,
        MenuEstoque,
        MenuMaquinas,
        PerfildaFazenda
    ],
}

# Rótulos dos botões da sidebar para cada tela
ROTULOS_TELAS = {
    MenuAnimais:      "Animais",
    MenuMaquinas:     "Máquinas",
    MenuEstoque:      "Estoque",
    MenuFuncionarios: "Funcionários",
    PerfildaFazenda:  "Fazenda",
}


class App(ctk.CTk):
    def __init__(self, conn, nivel_acesso="operador", nome_usuario=""):
        super().__init__()
        self.title("Gerenciamento de Fazenda - v1.0")
        self.geometry("1300x800")
        self.configure(fg_color=FUNDO)
        self.conn = conn
        self.nivel_acesso  = nivel_acesso
        self.nome_usuario  = nome_usuario
        self.iconbitmap("image.ico")

        # Telas permitidas para este nível
        self.telas_permitidas = PERMISSOES.get(nivel_acesso, [MenuAnimais, MenuEstoque])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.lateral = ctk.CTkFrame(self, fg_color=MENU_LATERAL, corner_radius=0)
        self.lateral.grid(row=0, column=0, sticky="nsew")
        self.lateral.grid_propagate(False)
        self.configurar_menu_lateral()

        ctk.CTkFrame(self, fg_color=MENU_LATERAL, corner_radius=0,
                     height=10, width=200).place(x=0, y=830)

        self.meio = ctk.CTkFrame(self, fg_color="transparent",
                                 corner_radius=0, border_width=0)
        self.meio.grid(row=0, column=1, sticky="nsew")
        self.meio.grid_rowconfigure(0, weight=1)
        self.meio.grid_columnconfigure(0, weight=1)

        # Carrega MenuIniciar + somente as telas permitidas
        self.frames = {}
        for F in [MenuIniciar] + self.telas_permitidas:
            frame = F(self.meio, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela(MenuIniciar)

    def configurar_menu_lateral(self):
        # Cabeçalho
        lateral_titulo = ctk.CTkFrame(self.lateral, fg_color="transparent",
                                      height=50, corner_radius=0)
        lateral_titulo.pack(fill="x")
        ctk.CTkLabel(lateral_titulo, text=" MENU\n PRINCIPAL",
                     font=("Inter", 19, "bold"), text_color=TEXTO,
                     fg_color="transparent", bg_color="transparent"
                     ).pack(side="left", padx=38, pady=20, anchor="center")

        # Badge de nível do usuário
        cores_nivel = {
            "admin":    ("#2563EB", "white"),
            "gerente":  ("#D97706", "white"),
            "operador": ("#16A34A", "white"),
        }
        cor_bg, cor_txt = cores_nivel.get(self.nivel_acesso, ("#475569", "white"))
        badge_frame = ctk.CTkFrame(self.lateral, fg_color=cor_bg, corner_radius=8, height=28)
        badge_frame.pack(fill="x", padx=16, pady=(0, 6))
        badge_frame.pack_propagate(False)
        ctk.CTkLabel(badge_frame,
                     text=f"  {self.nome_usuario}  •  {self.nivel_acesso.upper()}  ",
                     font=("Inter", 11, "bold"), text_color=cor_txt,
                     fg_color="transparent"
                     ).place(relx=0.5, rely=0.5, anchor="center")

        lateral_botoes = ctk.CTkFrame(self.lateral, fg_color="transparent", corner_radius=0)
        lateral_botoes.pack(pady=6)

        # Botão fixo: Menu Principal
        ctk.CTkButton(lateral_botoes, font=("Inter", 17, "bold"),
                      text="Menu Principal", width=70, height=50,
                      fg_color=MENU_LATERAL, hover_color=SCROLLBAR,
                      text_color=TEXTO, anchor="w",
                      command=lambda: self.mostrar_tela(MenuIniciar)
                      ).pack(padx=10, pady=6, fill="x")

        # Botões das telas permitidas
        for tela in self.telas_permitidas:
            rotulo = ROTULOS_TELAS.get(tela, str(tela.__name__))
            ctk.CTkButton(lateral_botoes, font=("Inter", 17, "bold"),
                          text=rotulo, width=70, height=50,
                          fg_color=MENU_LATERAL, hover_color=SCROLLBAR,
                          text_color=TEXTO, anchor="w",
                          command=lambda t=tela: self.mostrar_tela(t)
                          ).pack(padx=10, pady=6, fill="x")

        # Botão Sair (sempre visível)
        ctk.CTkButton(lateral_botoes, font=("Inter", 17, "bold"),
                      text="Sair", width=70, height=50,
                      fg_color=BOTAO_ERRO, hover_color=BOTAO_ERRO_HOVER,
                      text_color="white", anchor="center",
                      command=self.destroy
                      ).pack(padx=10, pady=16, fill="x")

        ctk.CTkLabel(self.lateral, text=data, font=("Inter", 18, "bold"),
                     bg_color="transparent", text_color=TEXTO
                     ).pack(side="bottom", pady=15)

        print(f"RELATÓRIO: Menu Lateral carregado — nível '{self.nivel_acesso}'.")

    def mostrar_tela(self, tela):
        if tela not in self.frames:
            from tkinter import messagebox
            messagebox.showwarning("Acesso Negado",
                                   "Você não tem permissão para acessar esta tela.")
            return
        self.frames[tela].tkraise()


class MenuIniciar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0)
        self.controller = controller
        self.conn = controller.conn
        self.configure(fg_color="transparent")

        ctk.CTkLabel(self, text="GERENCIAMENTO DA FAZENDA\n v1.0",
                     font=("Segoe UI", 50, "bold"), text_color=TEXTO,
                     fg_color="transparent"
                     ).place(relx=0.5, y=80, anchor="center")

        ctk.CTkLabel(self, text_color="black",
                     text="Suporte: (38) 99995-4195 - luizhf2018@gmail.com",
                     font=("Inter", 13, "bold")
                     ).place(anchor="center", relx=0.5, rely=0.94)

        print("RELATÓRIO: Tela Inicial funcionando.")