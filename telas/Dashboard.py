import customtkinter as ctk
import sqlite3
import time
from telas.MenuAnimais import MenuAnimais
from funcoes.animais import *

data = time.strftime("%d/%m/%Y")

# Paleta de Cores
FUNDO = "#F5F7FA"
MENU_LATERAL = "#1E293B"
BOTOES = "#2563EB"
CARDS = "#FFFFFF"
TABELAS = "#FFFFFF"
HOVER_TABELA = "#EFF6FF"
TEXTO = "black"

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
        self.configurar_topo()
        
        lateral_frame = ctk.CTkFrame(self, fg_color=MENU_LATERAL, corner_radius=0, height=10, width=200)
        lateral_frame.place(x=0, y=830)
        
        self.meio = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0, border_width=0)
        self.meio.grid(row=0, column=1, sticky="nsew")
        self.meio.grid_rowconfigure(0, weight=1)      
        self.meio.grid_columnconfigure(0, weight=1)  
        
        self.frames = {}
        for F in (MenuIniciar, MenuAnimais):
            frame = F(self.meio, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela(MenuIniciar)
        
    def configurar_topo(self):
        lateral_titulo = ctk.CTkFrame(self.lateral, fg_color="transparent", height=50, corner_radius=0)
        lateral_titulo.pack(fill="x")
            
        titulo = ctk.CTkLabel(lateral_titulo, text=" MENU\n PRINCIPAL", font=("Inter", 19, "bold"), text_color="white", fg_color="transparent", bg_color="transparent")
        titulo.pack(side="left", padx=38, pady=20, anchor="center")

        lateral_botoes = ctk.CTkFrame(self.lateral, fg_color="transparent", corner_radius=0)
        lateral_botoes.pack(pady=10)
            
        botoes = [
            ("Menu Principal", lambda: self.mostrar_tela(MenuIniciar), MENU_LATERAL, "w"),
            ("Animais", lambda: self.mostrar_tela(MenuAnimais), MENU_LATERAL, "w"),
            ("Máquinas", lambda: print('Máquinas'), MENU_LATERAL, "w"),
            ("Funcionários", lambda: print("Funcionários"), MENU_LATERAL, "w"),
            ("Estoque", lambda: print("Estoque"), MENU_LATERAL, "w"),
            ("Plantações", lambda: print("Plantações"), MENU_LATERAL, "w"),
            ("Sair", lambda: self.destroy(), "red", "center")
        ]
            
        for texto, comando, cor, lado in botoes:
            btn = ctk.CTkButton(lateral_botoes,
                                font=("Inter", 17, "bold"),
                                text=texto,
                                width=70,
                                height=50,
                                fg_color=cor,
                                hover_color=BOTOES,
                                text_color="white",
                                command=comando,
                                anchor=lado)
            btn.pack(padx=10, pady=10, fill="x") 
            
        marcacao_data = ctk.CTkLabel(self.lateral, text=f"{data}", font=("Inter", 18, "bold"), bg_color="transparent", text_color="white")
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
        
        label_rel = ctk.CTkLabel(rel_animais, text_color="black", text=f"Quantidade\nanimais:\n{quantidade_animais}", font=("Inter", 24, "bold"))
        label_rel.place(relx=0.5, rely=0.5, anchor="center")