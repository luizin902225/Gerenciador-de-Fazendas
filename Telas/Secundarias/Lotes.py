import sqlite3
import customtkinter as ctk
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


def cadastro_lotes(self):
    lotes = ctk.CTkToplevel(self)
    lotes.title("Cadastro de Lotes")
    lotes.geometry("450x340")
    lotes.attributes("-topmost", True)
    lotes.grab_set()
    lotes.iconbitmap("image.ico")
    
    topo = ctk.CTkFrame(lotes, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(lotes, corner_radius=0, fg_color="white")
    resto.pack(fill="both", expand=True)
    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                    text="Cadastro de Lotes").place(relx=0.5, rely=0.5, anchor="center")
    
    titulos = [
        ("Nome:", 20, 20),
        ("Tamanho (hectares):", 230, 20),
        ("Localização:", 20, 100),
        ("Descrição:", 230, 100)
    ]
    
    for nome, x, y in titulos:
        ctk.CTkLabel(resto, text=nome, text_color=TEXTO, font=("Inter", 16, "bold")).place(x=x, y=y)
    
    entrada_nome = ctk.CTkEntry(resto, width=150, text_color="white")
    entrada_nome.place(x=20, y=50)
    entrada_tamanho = ctk.CTkEntry(resto, width=150, text_color="white")
    entrada_tamanho.place(x=230, y=50)
    entrada_localizacao = ctk.CTkEntry(resto, width=150, text_color="white")
    entrada_localizacao.place(x=20, y=130)
    entrada_descricao = ctk.CTkEntry(resto, width=150, text_color="white")
    entrada_descricao.place(x=230, y=130)
    
    btn_cadastrar = ctk.CTkButton(resto, text="Cadastrar", text_color="black",
                                    fg_color=BOTOES, hover_color=BOTOES_HOVER, command= lambda: salvar(lotes, entrada_nome, entrada_descricao, entrada_localizacao, entrada_tamanho))
    btn_cadastrar.place(relx=0.5, rely=0.9, anchor="center")
    
    print("RELATÓRIO: Tela de Cadastro de Lote carregado.")
    

def salvar(lote, nome_entrada, descricao_entrada, local_entrada, tamanho_entrada):
    
    nome = nome_entrada.get()
    tamanho = tamanho_entrada.get()
    local = local_entrada.get()
    descricao = descricao_entrada.get()
    
    try:
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        
        cursor.execute("""INSERT INTO lote(nome, tamanho, localizacao, descricao) 
                        VALUES(?, ?, ?, ?)""", (nome, tamanho, local, descricao))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", f"Lote {nome}, cadastrado com sucesso!")
        print(f"Lote {nome}, cadastrado com sucesso!")
        lote.destroy()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro: {str(e)}, contate o suporte")