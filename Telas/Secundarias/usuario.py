import sqlite3
import customtkinter as ctk
import hashlib

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

def cadastro_usuarios(self):
    usuarios = ctk.CTkToplevel(self)
    usuarios.title("Cadastro de Usuário")
    usuarios.geometry("600x560")
    usuarios.attributes("-topmost", True)
    usuarios.grab_set()
    usuarios.iconbitmap("image.ico")
    
    topo = ctk.CTkFrame(usuarios, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(usuarios, corner_radius=0, fg_color="white")
    resto.pack(fill="both", expand=True)
    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                    text="Cadastro de Usuarios").place(relx=0.5, rely=0.5, anchor="center")
    
    titulos = [
        ("Nome:", 20, 20),
        ("Usuario:", 20, 100),
        ("Senha:", 20, 180),
        ("Cargo:", 20, 260),
        ("Nivel Acesso:", 20, 340)
    ]
    
    for nome, x, y in titulos:
        ctk.CTkLabel(resto, text=nome, text_color=TEXTO, font=("Inter", 16, "bold")).place(x=x, y=y)
    
    entrada_nome = ctk.CTkEntry(resto, width=170, text_color="white")
    entrada_nome.place(x=20, y=50)
    entrada_usuario = ctk.CTkEntry(resto, width=170, text_color="white")
    entrada_usuario.place(x=20, y=130)
    entrada_senha = ctk.CTkEntry(resto, width=170, text_color="white")
    entrada_senha.place(x=20, y=210)
    entrada_cargo = ctk.CTkEntry(resto, width=170, text_color="white")
    entrada_cargo.place(x=20, y=290)
    entrada_nivelacesso = ctk.CTkEntry(resto, width=170, text_color="white")
    entrada_nivelacesso.place(x=20, y=370)
    
    btn_cadastrar = ctk.CTkButton(resto, text="Cadastrar", text_color="black",
                                    fg_color=BOTOES, hover_color=BOTOES_HOVER, 
                                    command= lambda: salvar(usuarios, entrada_nome, entrada_usuario, entrada_senha, entrada_cargo, entrada_nivelacesso))
    btn_cadastrar.place(relx=0.35, rely=0.9, anchor="center")
    
    btn_excluir = ctk.CTkButton(resto, text="Excluir", text_color="black",
                                fg_color=BOTOES, hover_color=BOTOES_HOVER,
                                command= lambda: deletar_item(self))
    btn_excluir.place(relx=0.7, rely=0.9, anchor="center")
    
    estilo = ttk.Style()
    estilo.theme_use("clam")
        
    colunas = ("id", "nome", "usuario", "nivel")
    self.tabela = ttk.Treeview(resto, columns=colunas, show="headings")
        
    self.tabela.tag_configure("par", background=LINHA_PAR)
    self.tabela.tag_configure("impar", background=LINHA_IMPAR)
        
    self.tabela.heading("id", text="ID")
    self.tabela.heading("nome", text="Nome")
    self.tabela.heading("usuario", text="Usuário")
    self.tabela.heading("nivel", text="Acesso")
        
    self.tabela.column("id", width=40, anchor="center", stretch=False)
    self.tabela.column("nome", width=120, anchor="center", stretch=False)
    self.tabela.column("usuario", width=80, anchor="center")
    self.tabela.column("nivel", width=80, anchor="center")
    
    self.tabela.place(x=250, y=30)
    
    atualizar_tabela_usuarios(self, "")
    
    print("RELATÓRIO: Tela de Cadastro de Usuário carregado.")
    

def atualizar_tabela_usuarios(instancia_tela, termo=""): # Atualiza a tabela com os dados do banco de dados
    for item in instancia_tela.tabela.get_children():
        instancia_tela.tabela.delete(item)
    dados = buscar_usuarios(termo)
    for i, linha in enumerate(dados):
        cor = "par" if i % 2 == 0 else "impar"
        instancia_tela.tabela.insert("", "end", values=linha, tags=(cor,))

def buscar_usuarios(nome): # Busca os usuarios no banco de dados
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        id, nome, usuario, nivel_acesso
    FROM usuarios
    ORDER BY CASE
        WHEN nivel_acesso = 'admin' THEN 1
        WHEN nivel_acesso = 'gerente' THEN 2
        WHEN nivel_acesso = 'operador' THEN 3
    END
""")
    dados = cursor.fetchall()
    conn.close()
    return dados

def salvar(janela, nome_entrada, usuario_entrada, senha_entrada, cargo_entrada, nivelacesso_entrada):
    
    nome = nome_entrada.get()
    usuario = usuario_entrada.get()
    senha = senha_entrada.get()
    cargo = cargo_entrada.get()
    nivel = nivelacesso_entrada.get()
    
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    
    try:
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        
        cursor.execute("""INSERT INTO usuarios(nome, usuario, senha, cargo, nivel_acesso) 
                        VALUES(?, ?, ?, ?, ?)""", (nome, usuario, senha_hash, cargo, nivel))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", f"Usuário {nome}, cadastrado com sucesso!")
        print(f"Usuário {nome}, cadastrado com sucesso!")
        janela.destroy()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro: {str(e)} \nContate o suporte")
        print(f"Erro {e}.")

def deletar_item(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir!")
            return

        valores = self.tabela.item(selecao)['values']
        id_usuario = valores[0]
        nome    = valores[1]

        confirmar = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja realmente excluir o usuario:\n{nome}?"
        )

        if confirmar:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
                self.conn.commit()
                self.tabela.delete(selecao)
                messagebox.showinfo("Sucesso", f"Usuário removido com sucesso!\n{nome}")
                print(f"RELATÓRIO: Usuário '{nome}' excluído do banco.")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir: {e}.\nContate o suporte")