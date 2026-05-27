import sqlite3
import customtkinter as ctk
from tkinter import ttk, messagebox
from funcoes.funcionarios import (
    novo_funcionario, atualizar_tabela_funcionarios,
    buscar_funcionarios, informacao_funcionario
)

# Paleta de Cores
FUNDO = "#F8FAFC"
MENU_LATERAL = "#E2E8F0"
LINHA_PAR = "#F8FAFC"
LINHA_IMPAR = "#EEF2F7"
BOTOES = "#2563EB"
BOTOES_HOVER = "#1D4ED8"
BOTAO_ERRO = "#DC2626"
BOTAO_ERRO_HOVER = "#B91C1C"
TEXTO = "#0F172A"
SCROLLBAR = "#CBD5E1"


class MenuFuncionarios(ctk.CTkFrame):
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
        ctk.CTkLabel(topo, text="Gerenciador de Funcionários", fg_color="transparent",
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
        self.entrada_pesquisa.bind("<Return>",     lambda e: buscar_funcionarios(e, self))
        self.entrada_pesquisa.bind("<KeyRelease>", lambda e: buscar_funcionarios(e, self))

        # Botões
        botoes = [
            ("Pesquisar",   lambda: buscar_funcionarios(None, self)),
            ("Cadastrar",   lambda: novo_funcionario(self)),
            ("Informações", lambda: self.abrir_informacoes()),
            ("Excluir",     lambda: self.deletar_funcionario()),
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

        colunas = ("id", "nome", "cpf", "cargo", "telefone", "data_admissao")
        self.tabela = ttk.Treeview(meio, columns=colunas, show="headings")

        self.tabela.tag_configure("par",   background=LINHA_PAR)
        self.tabela.tag_configure("impar", background=LINHA_IMPAR)

        self.tabela.heading("id",           text="ID")
        self.tabela.heading("nome",         text="Nome")
        self.tabela.heading("cpf",          text="CPF")
        self.tabela.heading("cargo",        text="Cargo")
        self.tabela.heading("telefone",     text="Telefone")
        self.tabela.heading("data_admissao", text="Data Admissão")

        self.tabela.column("id",            width=40,  anchor="center", stretch=False)
        self.tabela.column("nome",          width=250, anchor="center")
        self.tabela.column("cpf",           width=120, anchor="center")
        self.tabela.column("cargo",         width=150, anchor="center")
        self.tabela.column("telefone",      width=120, anchor="center")
        self.tabela.column("data_admissao", width=120, anchor="center")

        atualizar_tabela_funcionarios(self, "")

        self.tabela.pack(fill="both", expand=True, padx=20, pady=10)

        print("RELATÓRIO: Tela de Funcionários carregada.")

    def abrir_informacoes(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um funcionário para ver as informações!")
            return

        dados_tabela = self.tabela.item(selecao[0])['values']
        id_func = dados_tabela[0]

        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                id, nome, cpf, cargo, telefone, endereco,
                strftime('%d/%m/%Y', data_admissao) as data_admissao,
                observacoes
            FROM funcionarios WHERE id = ?
        """, (id_func,))
        dados_func = cursor.fetchone()
        conn.close()

        if dados_func is None:
            messagebox.showinfo("Aviso", "Funcionário não encontrado!")
            return

        informacao_funcionario(self, dados_func, self)

    def deletar_funcionario(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um funcionário para excluir!")
            return

        valores = self.tabela.item(selecao)['values']
        id_func = valores[0]
        nome    = valores[1]

        confirmar = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja realmente excluir o funcionário:\n{nome}?"
        )

        if confirmar:
            try:
                cursor = self.conn.cursor()
                cursor.execute("UPDATE funcionarios SET ativo = 0 WHERE id = ?", (id_func,))
                self.conn.commit()
                self.tabela.delete(selecao)
                messagebox.showinfo("Sucesso", f"Funcionário removido com sucesso!\n{nome}")
                print(f"RELATÓRIO: Funcionário '{nome}' desativado.")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir: {e}")