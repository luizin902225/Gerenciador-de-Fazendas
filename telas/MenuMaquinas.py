import sqlite3
import customtkinter as ctk
from tkinter import ttk, messagebox
from funcoes.maquinas import atualizar_tabela_maquinas, buscar_maquinas, novo_maquina, informacao_maquina

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

class MenuMaquinas(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color=FUNDO)
        self.controller = controller
        self.conn = controller.conn
        self.configure(fg_color="transparent")
        
        topo = ctk.CTkFrame(self, fg_color=MENU_LATERAL, corner_radius=0, height=75)
        topo.pack(fill="x")
        topo_pesquisa = ctk.CTkFrame(self, fg_color=FUNDO, corner_radius=0, height=50)
        topo_pesquisa.pack(fill="x")
        meio = ctk.CTkFrame(self, fg_color=FUNDO, corner_radius=0)
        meio.pack(fill="both", expand=True)
        
        # Titulo
        
        titulo_pagina = ctk.CTkLabel(topo, text="Gerenciador de Máquinas", fg_color="transparent", font=("Inter", 20, "bold"), text_color=TEXTO)
        titulo_pagina.place(anchor="center", relx=0.5, rely=0.5)
        
        # Topo Pesquisa
        pesquisa_titulo = ctk.CTkLabel(topo_pesquisa, font=("Inter", 14, "bold"), text_color=TEXTO, text="Pesquisar:")
        pesquisa_titulo.place(x=22, y=-2)
        self.entrada_pesquisa = ctk.CTkEntry(topo_pesquisa, font=("Inter", 15), width=250, fg_color="white", text_color=TEXTO, border_color="black")
        self.entrada_pesquisa.pack(padx=20, pady=25, side="left")
        
        botoes = [
            ("Pesquisar", lambda: buscar_maquinas(None, self)), 
            ("Cadastrar", lambda: novo_maquina(self)),
            ("Informações", lambda: self.abrir_informacoes_maquinas()),
            ("Excluir", lambda: self.deletar_maquina())
        ]
        
        for texto, comando in botoes:
            btn = ctk.CTkButton(topo_pesquisa, font=("Inter", 12), text=texto, text_color=TEXTO, fg_color=BOTOES, hover_color=BOTOES_HOVER, command=comando, width=75)
            btn.pack(padx=6, pady=10, side="left")
        
        self.entrada_pesquisa.bind("<Return>", lambda e: buscar_maquinas(e, self))
        self.entrada_pesquisa.bind("<KeyRelease>", lambda e: buscar_maquinas(e, self))
        
        style = ttk.Style()
        style.theme_use("clam")
        
        colunas = ("id", "nome", "tipo", "status", "modelo", "fabricante", "ano", "placa", "horas_uso")
        self.tabela = ttk.Treeview(meio, columns=colunas, show="headings")
        
        self.tabela.tag_configure("par", background=LINHA_PAR)
        self.tabela.tag_configure("impar", background=LINHA_IMPAR)
        
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("tipo", text="Tipo")
        self.tabela.heading("status", text="Status")
        self.tabela.heading("modelo", text="Modelo")
        self.tabela.heading("fabricante", text="Fabricante")
        self.tabela.heading("ano", text="Ano")
        self.tabela.heading("placa", text="Placa")
        self.tabela.heading("horas_uso", text="Horas Uso")
        
        self.tabela.column("id", width=40, anchor="center", stretch=False)
        self.tabela.column("nome", width=200, minwidth=150, anchor="center")
        self.tabela.column("tipo", width=75, anchor="center")
        self.tabela.column("status", width=75, anchor="center")
        self.tabela.column("modelo", width=75, minwidth=150, anchor="center")
        self.tabela.column("fabricante", width=75, anchor="center")
        self.tabela.column("ano", width=100, anchor="center")
        self.tabela.column("placa", width=100, anchor="center")
        self.tabela.column("horas_uso", width=100, anchor="center")
        
        atualizar_tabela_maquinas(self, "")
        
        self.tabela.pack(fill="both", expand=True, padx=20, pady=10)
        
    def abrir_informacoes_maquinas(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione alguma maquina para ver as informações!")
            return
        
        dados_maquinas = self.tabela.item(selecao[0])['values']
        id_maquinas = dados_maquinas[0]
        
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT 
                        id,
                        nome,
                        tipo,
                        modelo,
                        fabricante,
                        ano,
                        placa,
                        horas_uso,
                        status,
                        observacoes
                        FROM maquinas WHERE id=?""", (id_maquinas,))
        dados_maquina = cursor.fetchone()
        
        conn.close()
        
        if dados_maquina is None:
            messagebox.showinfo("Aviso", "Maquina não encontrada!")
            return
    
        informacao_maquina(self, dados_maquina, self)
    
    def deletar_maquina(self): # Função que deleta uma maquina 
        selecao = self.tabela.selection()
        
        if not selecao:
            messagebox.showwarning("Aviso", "Por favor, selecione uma maquina para excluir")
            return

        valores = self.tabela.item(selecao)['values']
        id_maquina  = valores[0]
        nome = valores[1]
        
        confirmar = messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente deletar a maquina:\n{nome}?")
        
        if confirmar:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM maquinas WHERE id=?", (id_maquina,))
                self.conn.commit()
                
                #  Remove da interface e avisa o usuário
                self.tabela.delete(selecao)
                messagebox.showinfo("Sucesso", f"Máquina removido com sucesso!\n{nome}")
                print(f'Nome: {nome}.\n Excluído do banco com sucesso!')
                
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível deletar do banco de dados: {e}")
                