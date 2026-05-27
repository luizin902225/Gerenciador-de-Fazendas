import sqlite3
import customtkinter as ctk
from tkinter import ttk, messagebox
from funcoes.estoque import (
    novo_item_estoque, atualizar_tabela_estoque, buscar_estoque,
    informacao_item_estoque
)

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


class MenuEstoque(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color=FUNDO)
        self.controller = controller
        self.conn = controller.conn
        self.configure(fg_color="transparent")

        # Frames principais
        topo = ctk.CTkFrame(self, fg_color=MENU_LATERAL, corner_radius=0, height=75)
        topo.pack(fill="x")
        topo_pesquisa = ctk.CTkFrame(self, fg_color=FUNDO, corner_radius=0, height=50)
        topo_pesquisa.pack(fill="x")
        meio = ctk.CTkFrame(self, fg_color=FUNDO, corner_radius=0)
        meio.pack(fill="both", expand=True)

        # Título
        ctk.CTkLabel(topo, text="Gerenciador de Estoque", fg_color="transparent",
                     font=("Inter", 20, "bold"), text_color=TEXTO
                     ).place(anchor="center", relx=0.5, rely=0.5)

        # Barra de pesquisa
        ctk.CTkLabel(topo_pesquisa, font=("Inter", 14, "bold"), text_color=TEXTO,
                     text="Pesquisar:").place(x=22, y=-2)

        self.entrada_pesquisa = ctk.CTkEntry(
            topo_pesquisa, font=("Inter", 15), width=250,
            fg_color="white", text_color=TEXTO, border_color="black"
        )
        self.entrada_pesquisa.pack(padx=20, pady=25, side="left")
        self.entrada_pesquisa.bind("<Return>",     lambda e: buscar_estoque(e, self))
        self.entrada_pesquisa.bind("<KeyRelease>", lambda e: buscar_estoque(e, self))

        # Botões
        botoes = [
            ("Pesquisar",   lambda: buscar_estoque(None, self)),
            ("Cadastrar",   lambda: novo_item_estoque(self)),
            ("Informações", lambda: self.abrir_informacoes()),
            ("Excluir",     lambda: self.deletar_item()),
        ]
        for texto, comando in botoes:
            ctk.CTkButton(
                topo_pesquisa, font=("Inter", 12), text=texto,
                text_color=TEXTO, fg_color=BOTOES, hover_color=BOTOES_HOVER,
                command=comando, width=75
            ).pack(padx=6, pady=10, side="left")

        # Tabela
        estilo = ttk.Style()
        estilo.theme_use("clam")

        colunas = ("id", "nome", "categoria", "quantidade", "minimo", "unidade", "localizacao", "observacoes")
        self.tabela = ttk.Treeview(meio, columns=colunas, show="headings")

        self.tabela.tag_configure("par",   background=LINHA_PAR)
        self.tabela.tag_configure("impar", background=LINHA_IMPAR)
        self.tabela.tag_configure("baixo", background="#FEE2E2")  # vermelho claro = abaixo do mínimo

        self.tabela.heading("id",           text="ID")
        self.tabela.heading("nome",         text="Nome")
        self.tabela.heading("categoria",    text="Categoria")
        self.tabela.heading("quantidade",   text="Quantidade")
        self.tabela.heading("minimo",       text="Mínimo")
        self.tabela.heading("unidade",      text="Unidade")
        self.tabela.heading("localizacao",  text="Localização")
        self.tabela.heading("observacoes",  text="Observações")

        self.tabela.column("id",          width=40,  anchor="center", stretch=False)
        self.tabela.column("nome",        width=200, anchor="center")
        self.tabela.column("categoria",   width=120, anchor="center")
        self.tabela.column("quantidade",  width=90,  anchor="center")
        self.tabela.column("minimo",      width=80,  anchor="center")
        self.tabela.column("unidade",     width=75,  anchor="center")
        self.tabela.column("localizacao", width=130, anchor="center")
        self.tabela.column("observacoes", width=200, anchor="center")

        atualizar_tabela_estoque(self, "")

        self.tabela.pack(fill="both", expand=True, padx=20, pady=10)

        print("RELATÓRIO: Tela de Estoque carregada.")

    def abrir_informacoes(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um item para ver as informações!")
            return

        dados_tabela = self.tabela.item(selecao[0])['values']
        id_item = dados_tabela[0]

        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, categoria, quantidade, estoque_minimo, unidade, localizacao, observacoes
            FROM estoque WHERE id = ?
        """, (id_item,))
        dados_item = cursor.fetchone()
        conn.close()

        if dados_item is None:
            messagebox.showinfo("Aviso", "Item não encontrado!")
            return

        informacao_item_estoque(self, dados_item, self)

    def deletar_item(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um item para excluir!")
            return

        valores = self.tabela.item(selecao)['values']
        id_item = valores[0]
        nome    = valores[1]

        confirmar = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja realmente excluir o item:\n{nome}?"
        )

        if confirmar:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM estoque WHERE id = ?", (id_item,))
                self.conn.commit()
                self.tabela.delete(selecao)
                messagebox.showinfo("Sucesso", f"Item removido com sucesso!\n{nome}")
                print(f"RELATÓRIO: Item '{nome}' excluído do banco.")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir: {e}")