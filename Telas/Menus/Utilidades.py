import sqlite3
import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image

from Telas.Secundarias.configuracao import configuracoes
from Telas.Secundarias.Lotes import cadastro_lotes
from Telas.Secundarias.usuario import cadastro_usuarios
from Telas.Secundarias.fazendeiros import produtor_rural

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

class Utilidades(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color=FUNDO)
        self.controller = controller
        self.conn = controller.conn
        self.configure(fg_color="transparent")
        
        topo = ctk.CTkFrame(self, fg_color=MENU_LATERAL, corner_radius=0, height=75)
        topo.pack(fill="x")
        meio = ctk.CTkFrame(self, fg_color=FUNDO, corner_radius=0)
        meio.pack(fill="both", expand=True)
        
        titulo_pagina = ctk.CTkLabel(topo, text="Utilidades", fg_color="transparent", font=("Inter", 20, "bold"), text_color=TEXTO)
        titulo_pagina.place(anchor="center", relx=0.5, rely=0.5)
        
        # Ícones
        icone_configuração = ctk.CTkImage(
            light_image=Image.open("imagens/icone_configuracoes.png"), size=(100, 100))
        icone_fazendeiro = ctk.CTkImage(
            light_image=Image.open("imagens/icone_fazendeiro.png"), size=(100, 100))
        icone_pessoal = ctk.CTkImage(
            light_image=Image.open("imagens/icone_pessoal.png"), size=(100, 100))
        icone_lote = ctk.CTkImage(
            light_image=Image.open("imagens/icone_lote.png"), size=(100, 100))

        frame_bts = ctk.CTkFrame(self, fg_color="transparent")
        frame_bts.pack(anchor="center", expand=True)

        btn_inicio = [
            ("Configurações", icone_configuração, lambda: configuracoes(self)),
            ("Pessoal",       icone_pessoal,      lambda: cadastro_usuarios(self)),
            ("Fazendeiros",   icone_fazendeiro,   lambda: produtor_rural(self)),
            ("Lote",          icone_lote,         lambda: cadastro_lotes(self)),
        ]

        for nome, foto, comando in btn_inicio:
            ctk.CTkButton(frame_bts, fg_color="transparent", text_color=TEXTO,
                          text=nome, image=foto, font=("Inter", 14, "bold"),
                          compound="top", command=comando,
                          hover_color=TEXTO_PLACEHOLDER
                          ).pack(side="left", padx=5)

        ctk.CTkLabel(self, text_color="black",
                     text="Suporte: (38) 99995-4195 - luizhf2018@gmail.com",
                     font=("Inter", 13, "bold")
                     ).place(anchor="center", relx=0.5, rely=0.94)