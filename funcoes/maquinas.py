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