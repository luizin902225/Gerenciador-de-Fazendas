import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import time
from tkinter import ttk, messagebox

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

# Procurar no banco =>
def buscar_maquinas(event, instancia_tela):
    termo = instancia_tela.entrada_pesquisa.get()
    atualizar_tabela_maquinas(instancia_tela, termo)

def atualizar_tabela_maquinas(instancia_tela, termo=""):
    for item in instancia_tela.tabela.get_children():
        instancia_tela.tabela.delete(item)
    dados = buscar_maquinas_db(termo)
    for i, linha in enumerate(dados):
        cor = "par" if i % 2 == 0 else "impar"
        instancia_tela.tabela.insert("", "end", values=linha, tags=(cor,))

def buscar_maquinas_db(nome):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            id, nome, tipo, status, modelo, fabricante,
            ano, placa, horas_uso
        FROM maquinas
        WHERE nome LIKE ?
        ORDER BY CASE
            WHEN status = "ativo" THEN 1
            ELSE 2
        END, nome ASC
    """, (f'%{nome}%',))
    dados = cursor.fetchall()
    conn.close()
    return dados

def novo_maquina(self): # Cria a Janela de cadastro de maquinas
    cadastro = ctk.CTkToplevel()
    cadastro.geometry("450x400")
    cadastro.title("Nova Máquina")
    cadastro.attributes("-topmost", True)
    cadastro.configure(fg_color=FUNDO)
    
    topo = ctk.CTkFrame(cadastro, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(cadastro, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)
    title = ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"), text="Cadastro de Maquinas")
    title.place(relx=0.5, rely=0.5, anchor="center")
    
    titulos = [ # Lista de titulos
        ("Nome:", 20, 10),
        ("Placa:", 300, 10),
        ("Horas de Uso:", 300, 70),
        ("Fabricante:", 20, 70),
        ("Modelo:", 160, 70),
        ("Tipo:", 20, 130),
        ("Status:", 180, 130),
        ("Observações:", 20, 190),
        ("Ano", 220,190)
    ]
    
    for nome, x, y in titulos: # Cria os titulos na janela
        ctk.CTkLabel(resto, text=nome, text_color=TEXTO, fg_color="transparent", font=("Inter", 16, "bold")).place(x=x, y=y)
        
    campos = {}
    
    entradas = [ # lista de entradas
        (250, 20, 35, "Nome"),
        (75, 300, 35, "Placa"),
        (75, 300, 95, "HorasUso"),
        (75, 20, 95, "Fabricante"),
        (75, 160, 95, "Modelo"),
        (150, 20, 155, "Tipo"),
        (180, 20, 215, "Observacoes"),
        (75, 220, 215, "Ano")
    ]
    
    for largura, x, y, nome in entradas: # Cria as entradas na janela
        entry = ctk.CTkEntry(resto, text_color=TEXTO, font=("Inter", 14), width=largura, fg_color="DarkGrey")
        entry.place(x=x, y=y)
        campos[nome] = entry
    
    opcoes_selecionaveis = [
        ("Status", ["Ativo", "Manutenção", "Encostado"], 200, 155)
    ]
    
    for i, (nome, valores, x, y) in enumerate(opcoes_selecionaveis):
        opcoes_combo = ctk.CTkComboBox(resto, values=valores, width=100)
        opcoes_combo.place(x=x, y=y)
        campos[nome] = opcoes_combo
    
    # Botão cadastro que chama a função de cadastro
    ctk.CTkButton(resto, text_color="black", font=("Inter", 14), fg_color=BOTOES, hover_color=BOTOES_HOVER, text="Cadastrar",
                    command=lambda: cadastrar_maquina(cadastro, campos, self)).place(relx=0.5, rely=0.9, anchor="center")

def cadastrar_maquina(cadastro, campos, instancia_tela): # Função que cadastra a máquina
    dados = {campo: entry.get().strip() for campo, entry in campos.items()}

    for campo in ["Nome", "Placa", "Fabricante", "Status"]: # Transforma esses campos em obrigatório
        if dados[campo] == "":
            messagebox.showwarning("Aviso", f"O campo {campo} é obrigatório!")
            return
    
    #Adicona as entrada no banco
    with sqlite3.connect("banco.db") as conn:
        conn.cursor().execute("""
            INSERT INTO maquinas(nome, tipo, modelo, fabricante, ano, placa, 
                                horas_uso, status, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (dados["Nome"], dados["Tipo"], dados["Modelo"], dados["Fabricante"], dados["Ano"],
                dados["Placa"], dados["HorasUso"], dados["Status"], dados["Observacoes"]))
        conn.commit()
    messagebox.showinfo("Sucesso", "Maquina cadastrado com sucesso!")
    print(f"Maquina cadastrada com sucesso!") # Dá o log de sucesso
    atualizar_tabela_maquinas(instancia_tela, "")
    cadastro.destroy()
