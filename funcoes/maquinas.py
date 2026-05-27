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

def maquinas_qnt():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) FROM maquinas")
    contador = cursor.fetchone()
    conn.close()
    return contador[0]

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

def informacao_maquina(self, dados_maquinas, instancia_tela):
    info = ctk.CTkToplevel(self)
    info.title("Informações da Máquina")
    info.geometry("450x450")
    info.attributes("-topmost", True)
    info.grab_set()
    info.configure(fg_color=FUNDO)
    
    topo = ctk.CTkFrame(info, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(info, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)
    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                 text="Informações da Máquina").place(relx=0.5, rely=0.5, anchor="center")
    
    titulos = [
        ("Nome:",         20,  10),
        ("Placa:",        300, 10),
        ("Fabricante:",   20,  70),
        ("Modelo:",       160, 70),
        ("Horas de Uso:", 300, 70),
        ("Tipo:",         20,  130),
        ("Status:",       220, 130),
        ("Observações:",  20,  190),
        ("Ano:",          220, 190),
    ]
    
    for titulo, x, y in titulos:
        ctk.CTkLabel(resto, text=titulo, text_color=TEXTO, fg_color="transparent",
                     font=("Inter", 16, "bold")).place(x=x, y=y)
    
    id_maquina = dados_maquinas[0]
    nome_maquina       = dados_maquinas[1]
    tipo       = dados_maquinas[2]
    modelo     = dados_maquinas[3]
    fabricante = dados_maquinas[4]
    ano        = dados_maquinas[5]
    placa      = dados_maquinas[6]
    horasdeuso = dados_maquinas[7]
    status     = dados_maquinas[8]
    obs        = dados_maquinas[9]
    
    # Label atualizável
    status_label = ctk.CTkLabel(resto, text_color=TEXTO, font=("Inter", 14),
                                fg_color="transparent", text=status)
    status_label.place(x=220, y=155)

    # Demais informações fixas
    fixos = [
        (20,  35,  nome_maquina),
        (300, 35,  placa),
        (20,  95,  fabricante),
        (160, 95,  modelo),
        (300, 95,  str(horasdeuso)),
        (20,  155, tipo),
        (20,  215, str(obs)),
        (220, 215, str(ano)),        
    ]
    for x, y, texto in fixos:
        ctk.CTkLabel(resto, text_color=TEXTO, font=("Inter", 14),
                     fg_color="transparent", text=texto).place(x=x, y=y)

    frame_inferior = ctk.CTkFrame(resto, fg_color="transparent")
    frame_inferior.place(relx=0.5, rely=0.8, anchor="center")
    
    cor_acao = "#475569"
    
    btns = [
        ("Relatório Manut.", lambda: relatorio_manutencao(info, id_maquina, nome_maquina)),
        ("Registrar Manut.", lambda: registrar_manutencao(info, id_maquina, nome_maquina)),
        ("Status", lambda: status_maquina(info, id_maquina, status_label, instancia_tela))
    ]
    for nome, comando in btns:
        btn = ctk.CTkButton(frame_inferior, text=nome, command= comando, font=("Inter", 14), fg_color=cor_acao)
        btn.pack(side="left", padx=4)
        
    # ── Botão Concluído ──
    ctk.CTkButton(resto, text="Concluído", text_color=TEXTO, font=("Inter", 14),
                    fg_color="#7E8CA0", hover_color=cor_acao, width=130,
                    command=info.destroy).place(relx=0.5, rely=0.93, anchor="center")

    print(f"RELATÓRIO: Informação máquinas funcionando!")
    

    # Função que registra uma manutenção
def registrar_manutencao(pai, id_maquina, nome_maquina):
    modal = ctk.CTkToplevel(pai)
    modal.title("Registrar Vacina")
    modal.geometry("340x550")
    modal.attributes("-topmost", True)
    modal.grab_set()
    modal.configure(fg_color=FUNDO)

    topo = ctk.CTkFrame(modal, fg_color=MENU_LATERAL, height=45, corner_radius=0)
    topo.pack(fill="x")
    ctk.CTkLabel(topo, text="Registrar Manutenção", text_color=TEXTO,
                    font=("Inter", 16, "bold")).place(relx=0.5, rely=0.5, anchor="center")

    resto = ctk.CTkFrame(modal, fg_color="transparent", corner_radius=0)
    resto.pack(fill="both", expand=True)

    ctk.CTkLabel(resto, text=f"Máquina: {nome_maquina}", text_color=TEXTO,
                    font=("Inter", 13, "bold")).place(x=20, y=15)

    campos_vacina = [
        ("Tipo da Manutenção ( Preventiva ou Corretiva ):", "Tipo", 20,  55,  300),
        ("Responsável:", "Responsavel", 20, 115,  200),
        ("Data da Manutenção (DD/MM/AAAA):", "DataManutencao", 20, 175, 150),
        ("Próxima Manutenção (DD/MM/AAAA):", "ProximaManutencao",   20, 235, 150)
    ]

    campos = {}
    for label, chave, x, y, larg in campos_vacina:
        ctk.CTkLabel(resto, text=label, text_color=TEXTO,
                        font=("Inter", 13, "bold")).place(x=x, y=y - 20)
        entry = ctk.CTkEntry(resto, font=("Inter", 13), width=larg,
                                fg_color="DarkGrey", text_color=TEXTO)
        entry.place(x=x, y=y)
        campos[chave] = entry
        
    ctk.CTkLabel(resto, font=("Inter", 13, "bold"), text_color=TEXTO, text="Descrição").place(x=20, y=275)
    desc = ctk.CTkTextbox(resto, font=("Inter", 13), fg_color="DarkGrey", text_color=TEXTO,
                            width=300, height=150)
    desc.place(x=20, y=295)
    campos["Descricao"] = desc
    campos["DataManutencao"].insert(0, time.strftime("%d/%m/%Y"))

    def salvar(nome_maquina):
        tipo       = campos["Tipo"].get().strip()
        responsavel  = campos["Responsavel"].get().strip()
        data_raw     = campos["DataManutencao"].get().strip()
        proxima_raw  = campos["ProximaManutencao"].get().strip()
        descricao    = campos["Descricao"].get("1.0", "end").strip()

        if not tipo:
            messagebox.showwarning("Aviso", "O tipo da manutenção é obrigatório!")
            return
        
        if not data_raw:
            messagebox.showwarning("Aviso", "A data da manutenção é obrigatória")
            return

        def converter_data(texto):
            try:
                d, m, a = texto.split("/")
                return f"{a}-{m.zfill(2)}-{d.zfill(2)}"
            except:
                return None

        data_db    = converter_data(data_raw)
        proxima_db = converter_data(proxima_raw) if proxima_raw else "Sem data certa"

        if not data_db:
            messagebox.showerror("Erro", "Data de manutenção inválida! Use DD/MM/AAAA.")
            return

        try:
            with sqlite3.connect("banco.db") as conn:
                conn.execute("""
                    INSERT INTO manutencoes (maquina_id, tipo_manutencao, data_manutencao, proxima_manutencao, descricao, responsavel)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (id_maquina, tipo, data_db, proxima_db, descricao, responsavel))
                conn.commit()
            messagebox.showinfo("Sucesso", f"Manutencção {tipo} registrada!")
            print(f"RELATÓRIO: Manutenção {tipo} realizada!")
            modal.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar manutenção: {e}")

    ctk.CTkButton(resto, text="Salvar", text_color=TEXTO, fg_color=BOTOES, hover_color=BOTOES_HOVER,
                    font=("Inter", 14), command=lambda:salvar(nome_maquina)).place(relx=0.5, rely=0.94, anchor="center")


    # Função que mostra os relatórios de uma função
def relatorio_manutencao(info, id_maquina, nome_maquina):
    manutencoes = ctk.CTkToplevel(info)
    manutencoes.geometry("800x560")
    manutencoes.attributes("-topmost", True)
    manutencoes.grab_set()
    manutencoes.configure(fg_color=FUNDO)
    
    topo = ctk.CTkFrame(manutencoes, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    meio = ctk.CTkFrame(manutencoes, corner_radius=0, fg_color="transparent", height=40)
    meio.pack(fill="x")
    resto = ctk.CTkFrame(manutencoes, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)
    
    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                    text="Relatório de Manutenções").place(relx=0.5, rely=0.5, anchor="center")
    
    nome_label = ctk.CTkLabel(meio, text_color=TEXTO, font=("Inter", 14, "bold"), text=f"Nome da máquina: {nome_maquina}")
    nome_label.pack(padx=20, side="left", pady=10)
    
    #btn_info = ctk.CTkButton(meio, text_color=TEXTO, font=("Inter", 14, "bold"), text="Informações")
    #btn_info.pack(side="left", padx=10)
    
    estilo = ttk.Style()
    estilo.theme_use("clam")
    
    colunas = ("id", "tipo", "data_man", "proxima_man", "responsavel", "descricao")
    tabela = ttk.Treeview(resto, columns=colunas, show="headings")
    
    tabela.tag_configure("par", background=LINHA_PAR)
    tabela.tag_configure("impar", background=LINHA_IMPAR)
    
    tabela.heading("id", text="ID")
    tabela.heading("tipo", text="Tipo")
    tabela.heading("data_man", text="Data Manutenção")
    tabela.heading("proxima_man", text="Data da Próxima")
    tabela.heading("responsavel", text="Responsável")
    tabela.heading("descricao", text="Descrição")
        
    tabela.column("id", width=40, anchor="center", stretch=False)
    tabela.column("tipo", width=75, minwidth=150, anchor="center")
    tabela.column("data_man", width=75, anchor="center")
    tabela.column("proxima_man", width=75, minwidth=150, anchor="center")
    tabela.column("responsavel", width=75, anchor="center")
    tabela.column("descricao", width=175, anchor="center")
    
    def atualizar_tabela_maquinas(instancia_tela):
        for item in tabela.get_children():
            tabela.delete(item)
        dados = buscar_manutencao_db()
        for i, linha in enumerate(dados):
            cor = "par" if i % 2 == 0 else "impar"
            tabela.insert("", "end", values=linha, tags=(cor,))

    def buscar_manutencao_db():
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                id,
                tipo_manutencao,
                data_manutencao,
                proxima_manutencao,
                responsavel,
                descricao
            FROM manutencoes
            WHERE maquina_id = ?
            ORDER BY data_manutencao DESC""", (id_maquina,))
        dados = cursor.fetchall()
        conn.close()
        return dados
    
    atualizar_tabela_maquinas(tabela)
    
    tabela.pack(fill="both", expand=True, padx=25, pady=20)

def status_maquina(pai, id_animal, lote_label, instancia_tela): # Função que muda o status da maquina ( Ativa, Manutenção, Encostada )
    modal = ctk.CTkToplevel(pai)
    modal.title("Mudar Status")
    modal.geometry("300x260")
    modal.attributes("-topmost", True)
    modal.grab_set()
    modal.configure(fg_color=FUNDO)

    topo = ctk.CTkFrame(modal, fg_color=MENU_LATERAL, height=45, corner_radius=0)
    topo.pack(fill="x")
    ctk.CTkLabel(topo, text="Mudar Status", text_color=TEXTO,
                font=("Inter", 16, "bold")).place(relx=0.5, rely=0.5, anchor="center")

    resto = ctk.CTkFrame(modal, fg_color="transparent", corner_radius=0)
    resto.pack(fill="both", expand=True)

    ctk.CTkLabel(resto, text="Selecione o novo status:", text_color=TEXTO,
                font=("Inter", 14, "bold")).place(relx=0.5, y=25, anchor="center")

    conn = sqlite3.connect("banco.db")
    lotes = [r[0] for r in conn.execute(
        "SELECT DISTINCT status FROM maquinas ORDER BY status"
    ).fetchall()]
    conn.close()

    combo = ctk.CTkComboBox(resto, values=lotes, width=180, font=("Inter", 14))
    combo.place(relx=0.5, y=70, anchor="center")

    def confirmar():
        novo = combo.get().strip()
        if not novo:
            messagebox.showwarning("Aviso", "Selecione um status válido!")
            return
        try:
            with sqlite3.connect("banco.db") as conn:
                conn.execute("UPDATE maquinas SET status = ? WHERE id = ?", (novo, id_animal))
                conn.commit()
            lote_label.configure(text=novo)
            atualizar_tabela_maquinas(instancia_tela, "")
            messagebox.showinfo("Sucesso", f"Status alterado para {novo}!")
            modal.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível alterar o status: {e}")

    ctk.CTkButton(resto, text="Confirmar", text_color=TEXTO, fg_color=BOTOES, hover_color=BOTOES_HOVER,
                  font=("Inter", 14), command=confirmar).place(relx=0.5, y=130, anchor="center")
    ctk.CTkButton(resto, text="Cancelar", text_color="white", fg_color="#64748B", hover_color=BOTOES_HOVER,
                  font=("Inter", 13), command=modal.destroy).place(relx=0.5, y=178, anchor="center")
