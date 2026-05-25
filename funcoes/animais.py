import sqlite3
import customtkinter as ctk
from tkinter import messagebox, ttk
import time

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

# *********
# Cadastros
# *********

def novo_animal(self):
    cadastro = ctk.CTkToplevel()
    cadastro.geometry("650x500")
    cadastro.title("Novo Animal")
    cadastro.attributes("-topmost", True)
    cadastro.grab_set()
    cadastro.configure(fg_color=FUNDO)
    
    topo = ctk.CTkFrame(cadastro, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(cadastro, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)
    title = ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"), text="Cadastro de Animais")
    title.place(relx=0.5, rely=0.5, anchor="center")
    
    titulos = [
        ("Nome:", 20, 10),
        ("Brinco:", 300, 10),
        ("Lote:", 420, 10),
        ("Peso Atual:", 20, 70),
        ("Raça:", 160, 70),
        ("Origem:", 20, 130),
        ("Tipo:", 420, 130),
        ("Sexo:", 300, 130),
        ("Status:", 180, 130),
        ("Observações:", 20, 190),
        ("Dia Nasc.:", 300, 70),
        ("Mês Nasc.:", 420, 70),
        ("Ano Nasc.:", 540, 70)
    ]
    
    for nome, x, y in titulos:
        ctk.CTkLabel(resto, text=nome, text_color=TEXTO, fg_color="transparent", font=("Inter", 16, "bold")).place(x=x, y=y)
        
    campos = {}
    
    entradas = [
        (250, 20, 35, "Nome"),
        (75, 300, 35, "Brinco"),
        (75, 420, 35, "Lote"),
        (75, 20, 95, "Peso Atual"),
        (75, 160, 95, "Raça"),
        (150, 20, 155, "Origem"),
        (150, 20, 215, "Observações"),
    ]
    
    for largura, x, y, nome in entradas:
        entry = ctk.CTkEntry(resto, text_color=TEXTO, font=("Inter", 14), width=largura, fg_color="DarkGrey")
        entry.place(x=x, y=y)
        campos[nome] = entry

    data_nascimento = [
        (75, 300, 95, "Dia nasc"),
        (75, 420, 95, "Mes nasc"),
        (75, 540, 95, "Ano nasc")
    ]
    
    for largura, x, y, nome in data_nascimento:
        entry_data = ctk.CTkEntry(resto, text_color=TEXTO, font=("Inter", 14), width=largura, fg_color="DarkGrey")
        entry_data.place(x=x, y=y)
        campos[nome] = entry_data
    
    opcoes_selecionaveis = [
        ("Sexo", ["Macho", "Fêmea"], 180, 155),
        ("Tipo", ["Corte", "Leite"], 300, 155),
        ("Status", ["Ativo", "Tratamento", "Seca", "Prenha", "Abate"], 420, 155)
    ]
    
    for i, (nome, valores, x, y) in enumerate(opcoes_selecionaveis):
        opcoes_combo = ctk.CTkComboBox(resto, values=valores, width=100)
        opcoes_combo.place(x=x, y=y)
        campos[nome] = opcoes_combo
    
    ctk.CTkButton(resto, text_color="black", font=("Inter", 14), fg_color=BOTOES, hover_color=BOTOES_HOVER, text="Cadastrar",
                  command=lambda: cadastrar_animais(cadastro, campos, self)).place(relx=0.5, rely=0.9, anchor="center")


# *****
# Banco
# *****

def buscar_animais(event, instancia_tela):
    termo = instancia_tela.entrada_pesquisa.get()
    atualizar_tabela_animais(instancia_tela, termo)

def atualizar_tabela_animais(instancia_tela, termo=""):
    for item in instancia_tela.tabela.get_children():
        instancia_tela.tabela.delete(item)
    dados = buscar_animais_db(termo)
    for i, linha in enumerate(dados):
        cor = "par" if i % 2 == 0 else "impar"
        instancia_tela.tabela.insert("", "end", values=linha, tags=(cor,))

def buscar_animais_db(nome):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            id, brinco, nome, tipo, sexo,
            printf('%.2f KG', peso_atual) as peso_atual,
            strftime('%d/%m/%Y', data_nascimento) as data_nascimento,
            status, lote
        FROM animais
        WHERE nome LIKE ?
        AND ativo = 1
        ORDER BY CASE
            WHEN tipo = "Leite" THEN 1
            WHEN tipo = "Corte" THEN 2
        END, nome ASC
    """, (f'%{nome}%',))
    dados = cursor.fetchall()
    conn.close()
    return dados

def cadastrar_animais(cadastro, campos, instancia_tela):
    dados = {campo: entry.get().strip() for campo, entry in campos.items()}

    for campo in ["Nome", "Lote", "Peso Atual", "Raça", "Brinco"]:
        if dados[campo] == "":
            messagebox.showwarning("Aviso", f"O campo {campo} é obrigatório!")
            return

    try:
        peso = float(dados["Peso Atual"])
    except:
        messagebox.showerror("Erro", "Digite um peso válido!")
        return
    
    try:
        dia = dados["Dia nasc"].zfill(2)
        mes = dados["Mes nasc"].zfill(2)
        ano = dados["Ano nasc"]
        data_nascimento = f"{ano}-{mes}-{dia}"
    except:
        messagebox.showerror("Erro", "Preencha a data corretamente!")
        return
    
    try:
        with sqlite3.connect("banco.db") as conn:
            conn.cursor().execute("""
                INSERT INTO animais(nome, brinco, lote, peso_atual, data_nascimento,
                                    raca, origem, status, sexo, tipo, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (dados["Nome"], dados["Brinco"], dados["Lote"], peso, data_nascimento,
                  dados["Raça"], dados["Origem"], dados["Status"], dados["Sexo"],
                  dados["Tipo"], dados["Observações"]))
            conn.commit()
        messagebox.showinfo("Sucesso", "Animal cadastrado com sucesso!")
        atualizar_tabela_animais(instancia_tela, "")
        cadastro.destroy()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", f"Brinco {dados['Brinco']} já cadastrado!\nPor favor, coloque outro")

def animais_qnt():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) FROM animais WHERE ativo = 1")
    contador = cursor.fetchone()
    conn.close()
    return contador[0]

# ***********
# Informações
# ***********

def informacao_animal(self, dados_animais, instancia_tela):
    info = ctk.CTkToplevel(self)
    info.title("Informações do animal")
    info.geometry("520x560")
    info.attributes("-topmost", True)
    info.grab_set()
    info.configure(fg_color=FUNDO)
    
    topo = ctk.CTkFrame(info, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(info, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)
    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                 text="Informações do animal").place(relx=0.5, rely=0.5, anchor="center")
    
    titulos = [
        ("Nome:", 20, 10),
        ("Brinco:", 300, 10),
        ("Lote:", 420, 10),
        ("Peso Atual:", 20, 70),
        ("Data Nasc.:", 160, 70),
        ("Raça:", 300, 70),
        ("Status:", 20, 130),
        ("Sexo:", 160, 130),
        ("Tipo:", 300, 130),
        ("Origem:", 20, 190),
        ("Observações:", 20, 250)
    ]
    
    for titulo, x, y in titulos:
        ctk.CTkLabel(resto, text=titulo, text_color=TEXTO, fg_color="transparent",
                     font=("Inter", 16, "bold")).place(x=x, y=y)
    
    id_animal   = dados_animais[0]
    brinco      = dados_animais[1]
    nome        = dados_animais[2]
    tipo        = dados_animais[3]
    sexo        = dados_animais[4]
    raca        = dados_animais[5]
    data_nasc   = dados_animais[6]
    peso_atual  = dados_animais[7]
    lote        = dados_animais[8]
    status      = dados_animais[9]
    origem      = dados_animais[10]
    observacoes = dados_animais[11]

    # Labels atualizáveis (lote e status podem mudar)
    lote_label = ctk.CTkLabel(resto, text_color=TEXTO, font=("Inter", 14), fg_color="transparent", text=lote)
    lote_label.place(x=420, y=35)

    status_label = ctk.CTkLabel(resto, text_color=TEXTO, font=("Inter", 14), fg_color="transparent", text=status)
    status_label.place(x=20, y=155)

    # Demais informações fixas
    fixos = [
        (20, 35, nome),
        (300, 35, brinco),
        (20, 95, peso_atual),
        (160, 95, data_nasc),
        (300, 95, raca),
        (300, 155, tipo),
        (160, 155, sexo),
        (20, 215, origem),
        (20, 275, observacoes)
    ]
    for x, y, texto in fixos:
        ctk.CTkLabel(resto, text_color=TEXTO, font=("Inter", 14),
                     fg_color="transparent", text=texto).place(x=x, y=y)

    # ── Linha de botões de ação ──
    cor_acao = "#475569"
    botoes_acao = [
        ("Mudar Lote",    lambda: mudar_lote(info, id_animal, lote_label, instancia_tela)),
        ("Reg. Pesagem",  lambda: registrar_pesagem(info, id_animal, nome)),
        ("Reg. Vacina",   lambda: registrar_vacina(info, id_animal, nome)),
        ("Mudar Status",  lambda: mudar_status(info, id_animal, status_label, instancia_tela)),
    ]
    
    frame_superior = ctk.CTkFrame(resto, fg_color="transparent")
    frame_superior.place(relx=0.5, rely=0.74, anchor="center")
    frame_inferior = ctk.CTkFrame(resto, fg_color="transparent")
    frame_inferior.place(relx=0.5, rely=0.82, anchor="center")

    for texto, cmd in botoes_acao:
        ctk.CTkButton(frame_inferior, text=texto, text_color=TEXTO, font=("Inter", 12),
                        hover_color=cor_acao, width=108, fg_color="#7E8CA0",
                        command=cmd).pack(side="left", padx=4)
    
    btn_relvacinas = ctk.CTkButton(frame_superior, text="Rel. de Vacinas", text_color=TEXTO,
                                    font=("Inter", 12), fg_color="#7E8CA0", hover_color=cor_acao, 
                                    width=120, command= lambda: relatorio_vacinas(info, id_animal, nome))
    btn_relvacinas.pack(side="left", padx=4)
    
    btn_relpesagem = ctk.CTkButton(frame_superior, text="Rel. de Pesagem", text_color=TEXTO,
                                   font=("Inter", 12), fg_color="#7E8CA0", hover_color=cor_acao,
                                   width=120, command= lambda: relatorio_pesagens(info, id_animal, nome))
    btn_relpesagem.pack(side="left", padx=4)

    # ── Botão Concluído ──
    ctk.CTkButton(resto, text="Concluído", text_color=TEXTO, font=("Inter", 14),
                    fg_color="#7E8CA0", hover_color=cor_acao, width=130,
                    command=info.destroy).place(relx=0.5, rely=0.93, anchor="center")

    print(f"RELATÓRIO: Informação animal funcionando! Nome: {nome}. Brinco: {brinco}")

# **********
# Mudar Lote
# **********

def mudar_lote(pai, id_animal, lote_label, instancia_tela):
    modal = ctk.CTkToplevel(pai)
    modal.title("Mudar Lote")
    modal.geometry("300x260")
    modal.attributes("-topmost", True)
    modal.grab_set()
    modal.configure(fg_color=FUNDO)

    topo = ctk.CTkFrame(modal, fg_color=MENU_LATERAL, height=45, corner_radius=0)
    topo.pack(fill="x")
    ctk.CTkLabel(topo, text="Mudar Lote", text_color=TEXTO,
                font=("Inter", 16, "bold")).place(relx=0.5, rely=0.5, anchor="center")

    resto = ctk.CTkFrame(modal, fg_color="transparent", corner_radius=0)
    resto.pack(fill="both", expand=True)

    ctk.CTkLabel(resto, text="Selecione o novo lote:", text_color=TEXTO,
                font=("Inter", 14, "bold")).place(relx=0.5, y=25, anchor="center")

    conn = sqlite3.connect("banco.db")
    lotes = [r[0] for r in conn.execute(
        "SELECT DISTINCT lote FROM animais WHERE lote IS NOT NULL AND ativo = 1 ORDER BY lote"
    ).fetchall()]
    conn.close()

    combo = ctk.CTkComboBox(resto, values=lotes, width=180, font=("Inter", 14))
    combo.place(relx=0.5, y=70, anchor="center")

    def confirmar():
        novo = combo.get().strip()
        if not novo:
            messagebox.showwarning("Aviso", "Selecione um lote válido!")
            return
        try:
            with sqlite3.connect("banco.db") as conn:
                conn.execute("UPDATE animais SET lote = ? WHERE id = ?", (novo, id_animal))
                conn.commit()
            lote_label.configure(text=novo)
            atualizar_tabela_animais(instancia_tela, "")
            messagebox.showinfo("Sucesso", f"Lote alterado para {novo}!")
            modal.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível alterar o lote: {e}")

    ctk.CTkButton(resto, text="Confirmar", text_color=TEXTO, fg_color=BOTOES, hover_color=BOTOES_HOVER,
                  font=("Inter", 14), command=confirmar).place(relx=0.5, y=130, anchor="center")
    ctk.CTkButton(resto, text="Cancelar", text_color="white", fg_color="#64748B", hover_color=BOTOES_HOVER,
                  font=("Inter", 13), command=modal.destroy).place(relx=0.5, y=178, anchor="center")

# *****************
# Registrar Pesagem
# *****************

def registrar_pesagem(pai, id_animal, nome_animal):
    modal = ctk.CTkToplevel(pai)
    modal.title("Registrar Pesagem")
    modal.geometry("320x350")
    modal.attributes("-topmost", True)
    modal.grab_set()
    modal.configure(fg_color=FUNDO)

    topo = ctk.CTkFrame(modal, fg_color=MENU_LATERAL, height=45, corner_radius=0)
    topo.pack(fill="x")
    ctk.CTkLabel(topo, text="Registrar Pesagem", text_color=TEXTO,
                 font=("Inter", 16, "bold")).place(relx=0.5, rely=0.5, anchor="center")

    resto = ctk.CTkFrame(modal, fg_color="transparent", corner_radius=0)
    resto.pack(fill="both", expand=True)

    ctk.CTkLabel(resto, text=f"Animal: {nome_animal}", text_color=TEXTO,
                 font=("Inter", 13, "bold")).place(x=20, y=15)

    ctk.CTkLabel(resto, text="Peso (KG):", text_color=TEXTO,
                 font=("Inter", 14, "bold")).place(x=20, y=55)
    entry_peso = ctk.CTkEntry(resto, font=("Inter", 14), width=150, fg_color="DarkGrey", text_color=TEXTO)
    entry_peso.place(x=20, y=80)

    ctk.CTkLabel(resto, text="Data (DD/MM/AAAA):", text_color=TEXTO,
                 font=("Inter", 14, "bold")).place(x=20, y=115)
    entry_data = ctk.CTkEntry(resto, font=("Inter", 14), width=150, fg_color="DarkGrey", text_color=TEXTO)
    entry_data.insert(0, time.strftime("%d/%m/%Y"))
    entry_data.place(x=20, y=140)

    ctk.CTkLabel(resto, text="Observações:", text_color=TEXTO,
                 font=("Inter", 14, "bold")).place(x=20, y=175)
    entry_obs = ctk.CTkEntry(resto, font=("Inter", 14), width=270, fg_color="DarkGrey", text_color=TEXTO)
    entry_obs.place(x=20, y=198)

    def salvar():
        try:
            peso = float(entry_peso.get().strip().replace(",", "."))
        except:
            messagebox.showerror("Erro", "Digite um peso válido!")
            return

        data_raw = entry_data.get().strip()
        try:
            d, m, a = data_raw.split("/")
            data_db = f"{a}-{m.zfill(2)}-{d.zfill(2)}"
        except:
            messagebox.showerror("Erro", "Data inválida! Use DD/MM/AAAA.")
            return

        obs = entry_obs.get().strip()

        try:
            with sqlite3.connect("banco.db") as conn:
                conn.execute("""
                    INSERT INTO pesagens (animal_id, data_pesagem, peso, observacoes)
                    VALUES (?, ?, ?, ?)
                """, (id_animal, data_db, peso, obs))
                # Atualiza peso_atual do animal
                conn.execute("UPDATE animais SET peso_atual = ? WHERE id = ?", (peso, id_animal))
                conn.commit()
            messagebox.showinfo("Sucesso", f"Pesagem de {peso} KG registrada!")
            modal.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar pesagem: {e}")

    ctk.CTkButton(resto, text="Salvar", text_color="white", fg_color=BOTOES, hover_color=BOTOES_HOVER,
                  font=("Inter", 14), command=salvar).place(relx=0.5, rely=0.93, anchor="center")

def relatorio_pesagens(info, id_animal, nome_animal):
    pesagens = ctk.CTkToplevel(info)
    pesagens.geometry("520x560")
    pesagens.attributes("-topmost", True)
    pesagens.grab_set()
    pesagens.configure(fg_color=FUNDO)
    
    topo = ctk.CTkFrame(pesagens, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(pesagens, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)
    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                    text="Relatório de Pesagens").place(relx=0.5, rely=0.5, anchor="center")
    
    nome_label = ctk.CTkLabel(resto, text_color=TEXTO, font=("Inter", 14, "bold"), text=f"Nome do animal: {nome_animal}")
    nome_label.place(x=25, y=-2)
    
    estilo = ttk.Style()
    estilo.theme_use("clam")

    
    colunas = ("id", "data_pesagem", "peso", "observacoes")
    tabela = ttk.Treeview(resto, columns=colunas, show="headings")
    
    tabela.tag_configure("par", background=LINHA_PAR)
    tabela.tag_configure("impar", background=LINHA_IMPAR)
    
    tabela.heading("id", text="ID")
    tabela.heading("data_pesagem", text="Data Pesagem")
    tabela.heading("peso", text="Peso")
    tabela.heading("observacoes", text="Observações")

        
    tabela.column("id", width=40, anchor="center", stretch=False)
    tabela.column("data_pesagem", width=175, minwidth=150, anchor="center")
    tabela.column("peso", width=75, anchor="center")
    tabela.column("observacoes", width=100, anchor="center")
    
    def atualizar_tabela_vacinas(instancia_tela):
        for item in tabela.get_children():
            tabela.delete(item)
        dados = buscar_vacinas_db()
        for i, linha in enumerate(dados):
            cor = "par" if i % 2 == 0 else "impar"
            tabela.insert("", "end", values=linha, tags=(cor,))

    def buscar_vacinas_db():
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                id,
                strftime('%d/%m/%Y', data_pesagem) as data_pesagem,
                printf('%.2f KG', peso) as peso,
                observacoes
            FROM pesagens
            WHERE animal_id = ?
            ORDER BY data_pesagem DESC""", (id_animal,))
        dados = cursor.fetchall()
        conn.close()
        return dados
    
    atualizar_tabela_vacinas(tabela)
    
    tabela.pack(fill="both", expand=True, padx=25, pady=20)

# ****************
# Registrar Vacina
# ****************

def registrar_vacina(pai, id_animal, nome_animal):
    modal = ctk.CTkToplevel(pai)
    modal.title("Registrar Vacina")
    modal.geometry("340x420")
    modal.attributes("-topmost", True)
    modal.grab_set()
    modal.configure(fg_color=FUNDO)

    topo = ctk.CTkFrame(modal, fg_color=MENU_LATERAL, height=45, corner_radius=0)
    topo.pack(fill="x")
    ctk.CTkLabel(topo, text="Registrar Vacina", text_color=TEXTO,
                    font=("Inter", 16, "bold")).place(relx=0.5, rely=0.5, anchor="center")

    resto = ctk.CTkFrame(modal, fg_color="transparent", corner_radius=0)
    resto.pack(fill="both", expand=True)

    ctk.CTkLabel(resto, text=f"Animal: {nome_animal}", text_color=TEXTO,
                    font=("Inter", 13, "bold")).place(x=20, y=15)

    campos_vacina = [
        ("Vacina:",               "Vacina",        20,  55,  280),
        ("Responsável:",          "Responsavel",   20, 115,  200),
        ("Data Aplicação (DD/MM/AAAA):", "DataAplicacao", 20, 175, 150),
        ("Próxima Dose (DD/MM/AAAA):",   "ProximaDose",   20, 235, 150),
        ("Observações:", "Obs", 20, 295, 150)
    ]

    campos = {}
    for label, chave, x, y, larg in campos_vacina:
        ctk.CTkLabel(resto, text=label, text_color=TEXTO,
                        font=("Inter", 13, "bold")).place(x=x, y=y - 20)
        entry = ctk.CTkEntry(resto, font=("Inter", 13), width=larg,
                                fg_color="DarkGrey", text_color=TEXTO)
        entry.place(x=x, y=y)
        campos[chave] = entry

    campos["DataAplicacao"].insert(0, time.strftime("%d/%m/%Y"))

    def salvar(nome_animal):
        vacina       = campos["Vacina"].get().strip()
        responsavel  = campos["Responsavel"].get().strip()
        data_raw     = campos["DataAplicacao"].get().strip()
        proxima_raw  = campos["ProximaDose"].get().strip()
        obs          = campos["Obs"].get().strip()

        if not vacina:
            messagebox.showwarning("Aviso", "O nome da vacina é obrigatório!")
            return
        
        if not data_raw:
            messagebox.showwarning("Aviso", "A data da vacinação é obrigatória")
            return

        def converter_data(texto):
            try:
                d, m, a = texto.split("/")
                return f"{a}-{m.zfill(2)}-{d.zfill(2)}"
            except:
                return None

        data_db    = converter_data(data_raw)
        proxima_db = converter_data(proxima_raw) if proxima_raw else None

        if not data_db:
            messagebox.showerror("Erro", "Data de aplicação inválida! Use DD/MM/AAAA.")
            return

        try:
            with sqlite3.connect("banco.db") as conn:
                conn.execute("""
                    INSERT INTO vacinas (animal_id, vacina, data_aplicacao, proxima_dose, responsavel, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (id_animal, vacina, data_db, proxima_db, responsavel, obs))
                conn.commit()
            messagebox.showinfo("Sucesso", f"Vacina '{vacina}' registrada!")
            print(f"Vacina {vacina} aplicada no animal: {nome_animal}")
            modal.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar vacina: {e}")

    ctk.CTkButton(resto, text="Salvar", text_color=TEXTO, fg_color=BOTOES, hover_color=BOTOES_HOVER,
                    font=("Inter", 14), command=lambda:salvar(nome_animal)).place(relx=0.5, rely=0.94, anchor="center")

def relatorio_vacinas(info, id_animal, nome_animal):
    vacinas = ctk.CTkToplevel(info)
    vacinas.geometry("800x560")
    vacinas.attributes("-topmost", True)
    vacinas.grab_set()
    vacinas.configure(fg_color=FUNDO)
    
    topo = ctk.CTkFrame(vacinas, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(vacinas, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)
    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                    text="Relatório de Vacinas").place(relx=0.5, rely=0.5, anchor="center")
    
    nome_label = ctk.CTkLabel(resto, text_color=TEXTO, font=("Inter", 14, "bold"), text=f"Nome do animal: {nome_animal}")
    nome_label.place(x=25, y=-2)
    
    estilo = ttk.Style()
    estilo.theme_use("clam")

    
    colunas = ("id", "vacina", "data_aplicacao", "proxima", "responsavel", "observacoes")
    tabela = ttk.Treeview(resto, columns=colunas, show="headings")
    
    tabela.tag_configure("par", background=LINHA_PAR)
    tabela.tag_configure("impar", background=LINHA_IMPAR)
    
    tabela.heading("id", text="ID")
    tabela.heading("vacina", text="Vacina")
    tabela.heading("data_aplicacao", text="Data Aplicação")
    tabela.heading("proxima", text="Data da Próxima")
    tabela.heading("responsavel", text="Responsável")
    tabela.heading("observacoes", text="Observacoes")
        
    tabela.column("id", width=40, anchor="center", stretch=False)
    tabela.column("vacina", width=175, minwidth=150, anchor="center")
    tabela.column("data_aplicacao", width=75, anchor="center")
    tabela.column("proxima", width=75, minwidth=150, anchor="center")
    tabela.column("responsavel", width=75, anchor="center")
    tabela.column("observacoes", width=100, anchor="center")
    
    def atualizar_tabela_vacinas(instancia_tela):
        for item in tabela.get_children():
            tabela.delete(item)
        dados = buscar_vacinas_db()
        for i, linha in enumerate(dados):
            cor = "par" if i % 2 == 0 else "impar"
            tabela.insert("", "end", values=linha, tags=(cor,))

    def buscar_vacinas_db():
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                id,
                vacina,
                strftime('%d/%m/%Y', data_aplicacao) as data_aplicacao,
                strftime('%d/%m/%Y', proxima_dose) as proxima_dose,
                responsavel,
                observacoes
            FROM vacinas
            WHERE animal_id = ?
            ORDER BY data_aplicacao DESC""", (id_animal,))
        dados = cursor.fetchall()
        conn.close()
        return dados
    
    atualizar_tabela_vacinas(tabela)
    
    tabela.pack(fill="both", expand=True, padx=25, pady=20)

# *************
# Mudar Status
# *************

def mudar_status(pai, id_animal, status_label, instancia_tela):
    modal = ctk.CTkToplevel(pai)
    modal.title("Mudar Status")
    modal.geometry("300x250")
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

    status_opcoes = ["Ativo", "Tratamento", "Seca", "Prenha", "Abate"]
    combo = ctk.CTkComboBox(resto, values=status_opcoes, width=180, font=("Inter", 14))
    combo.set(status_label.cget("text"))
    combo.place(relx=0.5, y=70, anchor="center")

    def confirmar():
        novo = combo.get().strip()
        if not novo:
            messagebox.showwarning("Aviso", "Selecione um status válido!")
            return
        try:
            with sqlite3.connect("banco.db") as conn:
                conn.execute("UPDATE animais SET status = ? WHERE id = ?", (novo, id_animal))
                conn.commit()
            status_label.configure(text=novo)
            atualizar_tabela_animais(instancia_tela, "")
            messagebox.showinfo("Sucesso", f"Status alterado para '{novo}'!")
            modal.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível alterar o status: {e}")

    ctk.CTkButton(resto, text="Confirmar", text_color=TEXTO, fg_color=BOTOES,
                    font=("Inter", 14), command=confirmar).place(relx=0.5, y=130, anchor="center")
    ctk.CTkButton(resto, text="Cancelar", text_color=TEXTO, fg_color="#64748B",
                    font=("Inter", 13), command=modal.destroy).place(relx=0.5, y=178, anchor="center")
