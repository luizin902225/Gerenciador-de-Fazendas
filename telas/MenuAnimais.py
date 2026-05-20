import sqlite3
import customtkinter as ctk
from tkinter import ttk, messagebox
from funcoes.animais import novo_animal, atualizar_tabela_animais, buscar_animais, informacao_animal
# Paleta de Cores
FUNDO = "#F5F7FA"
MENU_LATERAL = "#1E293B"
BOTOES = "#2563EB"
CARDS = "#FFFFFF"
TABELAS = "#FFFFFF"
HOVER_TABELA = "#EFF6FF"
TEXTO = "black"

class MenuAnimais(ctk.CTkFrame):
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
        
        titulo_pagina = ctk.CTkLabel(topo, text="Gerenciador de Animais", fg_color="transparent", font=("Inter", 20, "bold"), text_color="white")
        titulo_pagina.place(anchor="center", relx=0.5, rely=0.5)
        
        # Topo Pesquisa
        pesquisa_titulo = ctk.CTkLabel(topo_pesquisa, font=("Inter", 14, "bold"), text_color="black", text="Pesquisar:")
        pesquisa_titulo.place(x=20, y=-5)
        self.entrada_pesquisa = ctk.CTkEntry(topo_pesquisa, font=("Inter", 15), width=250, fg_color="white", text_color="black", border_color="black")
        self.entrada_pesquisa.pack(padx=20, pady=15, side="left")
        
        self.entrada_pesquisa.bind("<Return>", lambda e: buscar_animais(e, self))
        self.entrada_pesquisa.bind("<KeyRelease>", lambda e: buscar_animais(e, self))
        
        botoes = [
            ("Pesquisar", lambda: buscar_animais(None, self)),
            ("Cadastrar", lambda: novo_animal(self)),
            ("Informações", lambda: self.abrir_informacoes_animais()),
            ("Excluir", lambda: self.deletar_animal())
        ]
        
        for texto, comando in botoes:
            btn = ctk.CTkButton(topo_pesquisa, font=("Inter", 12), text=texto, text_color="black", fg_color=BOTOES, command=comando, width=75)
            btn.pack(padx=6, pady=10, side="left")
        
        # Tabela
        estilo = ttk.Style()
        estilo.theme_use("clam")

        
        colunas = ("id", "brinco", "nome", "tipo", "sexo", "peso", "data_nasc", "status", "lote")
        self.tabela = ttk.Treeview(meio, columns=colunas, show="headings")
        
        self.tabela.tag_configure("par", background="#F2F2F2")
        self.tabela.tag_configure("impar", background="white")
        
        self.tabela.heading("id", text="ID")
        self.tabela.heading("brinco", text="Brinco")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("tipo", text="Tipo")
        self.tabela.heading("sexo", text="Sexo")
        self.tabela.heading("peso", text="Peso Atual")
        self.tabela.heading("data_nasc", text="Data de Nascimento")
        self.tabela.heading("status", text="Status")
        self.tabela.heading("lote", text="Lote")
        
        self.tabela.column("id", width=40, anchor="center", stretch=False)
        self.tabela.column("brinco", width=50, anchor="center", stretch=False)
        self.tabela.column("nome", width=200, minwidth=150, anchor="center")
        self.tabela.column("tipo", width=75, anchor="center")
        self.tabela.column("sexo", width=75, minwidth=150, anchor="center")
        self.tabela.column("peso", width=75, anchor="center")
        self.tabela.column("data_nasc", width=100, anchor="center")
        self.tabela.column("status", width=100, anchor="center")
        self.tabela.column("lote", width=100, anchor="center")
        
        atualizar_tabela_animais(self, "")
        
        self.tabela.pack(fill="both", expand=True, padx=25, pady=20)
    
    def abrir_informacoes_animais(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione algum animal para ver as informações!")
            return
        
        dados_animal = self.tabela.item(selecao[0])['values']
        id_animal = dados_animal[0]
        
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT 
                        id, 
                        brinco,
                        nome,
                        tipo,
                        sexo,
                        raca,
                        strftime('%d/%m/%Y', data_nascimento) as data_nascimento,
                        printf('%.2f KG', peso_atual) as peso_atual,
                        lote,
                        status,
                        origem,
                        observacoes
                        FROM animais WHERE id=?""", (id_animal,))
        dados_animal = cursor.fetchone()
        
        conn.close()
        
        if dados_animal is None:
            messagebox.showinfo("Aviso", "Animal não encontrado!")
            return
    
        informacao_animal(self, dados_animal, self)
    
    def deletar_animal(self):
        selecao = self.tabela.selection()
        
        if not selecao:
            messagebox.showwarning("Aviso", "Por favor, selecione um animal para excluir")
            return

        valores = self.tabela.item(selecao)['values']
        id_animal  = valores[0]
        brinco = valores[1]
        nome = valores[2]
        
        confirmar = messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente deletar o produto:\n{nome}?")
        
        if confirmar:
            try:
                cursor = self.conn.cursor()
                cursor.execute("UPDATE animais SET ativo = 0 WHERE id = ?", (id_animal,))
                self.conn.commit()
                
                #  Remove da interface e avisa o usuário
                self.tabela.delete(selecao)
                messagebox.showinfo("Sucesso", f"Produto removido com sucesso!\n{nome}")
                print(f'Brinco: {brinco}. Nome: {nome}.\n Excluído do banco com sucesso!')
                
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível deletar do banco de dados: {e}")
                