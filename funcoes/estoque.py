import sqlite3
import customtkinter as ctk
from tkinter import messagebox, ttk
import time

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

# *********
# Contagem
# *********

def estoque_qnt():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) FROM estoque")
    contador = cursor.fetchone()
    conn.close()
    return contador[0]

# *********
# Banco
# *********

def buscar_estoque(event, instancia_tela):
    termo = instancia_tela.entrada_pesquisa.get()
    atualizar_tabela_estoque(instancia_tela, termo)

def atualizar_tabela_estoque(instancia_tela, termo=""):
    for item in instancia_tela.tabela.get_children():
        instancia_tela.tabela.delete(item)
    dados = buscar_estoque_db(termo)
    for i, linha in enumerate(dados):
        cor = "par" if i % 2 == 0 else "impar"
        # Marca em vermelho itens abaixo do estoque mínimo
        tags = (cor,)
        if linha[4] is not None and linha[3] is not None:
            if float(linha[3]) <= float(linha[4]):
                tags = ("baixo",)
        instancia_tela.tabela.insert("", "end", values=linha, tags=tags)

def buscar_estoque_db(nome):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            id, nome, categoria, quantidade, estoque_minimo, unidade, localizacao, observacoes
        FROM estoque
        WHERE nome LIKE ?
        ORDER BY categoria ASC, nome ASC
    """, (f'%{nome}%',))
    dados = cursor.fetchall()
    conn.close()
    return dados

# *********
# Cadastro
# *********

def novo_item_estoque(self):
    cadastro = ctk.CTkToplevel()
    cadastro.geometry("500x400")
    cadastro.title("Novo Item no Estoque")
    cadastro.attributes("-topmost", True)
    cadastro.grab_set()
    cadastro.configure(fg_color=FUNDO)

    topo = ctk.CTkFrame(cadastro, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(cadastro, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)
    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                 text="Cadastro de Item").place(relx=0.5, rely=0.5, anchor="center")

    titulos = [
        ("Nome:",             20,  10),
        ("Categoria:",        20,  70),
        ("Unidade:",         220,  70),
        ("Quantidade:",       20, 130),
        ("Estoque Mínimo:",  180, 130),
        ("Localização:",      20, 190),
        ("Observações:",      20, 250),
    ]
    for nome, x, y in titulos:
        ctk.CTkLabel(resto, text=nome, text_color=TEXTO, fg_color="transparent",
                     font=("Inter", 16, "bold")).place(x=x, y=y)

    campos = {}

    entradas = [
        (440, 20,  35, "Nome"),
        (180, 20,  95, "Categoria"),
        (100, 220, 95, "Unidade"),
        (120, 20, 155, "Quantidade"),
        (120, 180, 155, "EstoqueMinimo"),
        (440, 20, 215, "Localizacao"),
        (440, 20, 275, "Observacoes"),
    ]
    for largura, x, y, nome in entradas:
        entry = ctk.CTkEntry(resto, text_color=TEXTO, font=("Inter", 14),
                             width=largura, fg_color="DarkGrey")
        entry.place(x=x, y=y)
        campos[nome] = entry

    ctk.CTkButton(resto, text_color="black", font=("Inter", 14),
                  fg_color=BOTOES, hover_color=BOTOES_HOVER, text="Cadastrar",
                  command=lambda: cadastrar_item_estoque(cadastro, campos, self)
                  ).place(relx=0.5, rely=0.93, anchor="center")


def cadastrar_item_estoque(cadastro, campos, instancia_tela):
    dados = {campo: entry.get().strip() for campo, entry in campos.items()}

    for campo in ["Nome", "Categoria", "Unidade"]:
        if dados[campo] == "":
            messagebox.showwarning("Aviso", f"O campo {campo} é obrigatório!")
            return

    try:
        quantidade = float(dados["Quantidade"]) if dados["Quantidade"] else 0.0
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número válido!")
        return

    try:
        estoque_minimo = float(dados["EstoqueMinimo"]) if dados["EstoqueMinimo"] else 0.0
    except ValueError:
        messagebox.showerror("Erro", "Estoque mínimo deve ser um número válido!")
        return

    try:
        with sqlite3.connect("banco.db") as conn:
            conn.cursor().execute("""
                INSERT INTO estoque(nome, categoria, unidade, quantidade, estoque_minimo, localizacao, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (dados["Nome"], dados["Categoria"], dados["Unidade"],
                  quantidade, estoque_minimo, dados["Localizacao"], dados["Observacoes"]))
            conn.commit()
        messagebox.showinfo("Sucesso", "Item cadastrado com sucesso!")
        print(f"RELATÓRIO: Item '{dados['Nome']}' cadastrado no estoque.")
        atualizar_tabela_estoque(instancia_tela, "")
        cadastro.destroy()
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível cadastrar: {e}")


# ***********
# Informações
# ***********

def informacao_item_estoque(self, dados_item, instancia_tela):
    info = ctk.CTkToplevel(self)
    info.title("Informações do Item")
    info.geometry("500x480")
    info.attributes("-topmost", True)
    info.grab_set()
    info.configure(fg_color=FUNDO)

    topo = ctk.CTkFrame(info, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    meio = ctk.CTkFrame(info, fg_color="transparent", corner_radius=0, height=40)
    meio.pack(fill="x")
    resto = ctk.CTkFrame(info, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)

    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                 text="Informações do Item").place(relx=0.5, rely=0.5, anchor="center")

    id_item     = dados_item[0]
    nome        = dados_item[1]
    categoria   = dados_item[2]
    quantidade  = dados_item[3]
    est_minimo  = dados_item[4]
    unidade     = dados_item[5]
    localizacao = dados_item[6]
    observacoes = dados_item[7]

    # Botões de ação no topo
    ctk.CTkButton(meio, text="Entrada", font=("Inter", 12), text_color=TEXTO,
                  fg_color=BOTAO_SUCESSO, hover_color=BOTAO_SUCESSO_HOVER, width=90,
                  command=lambda: registrar_movimentacao(info, id_item, nome, "Entrada", instancia_tela)
                  ).pack(side="left", padx=10, pady=5)

    ctk.CTkButton(meio, text="Saída", font=("Inter", 12), text_color=TEXTO,
                  fg_color=BOTAO_ERRO, hover_color=BOTAO_ERRO_HOVER, width=90,
                  command=lambda: registrar_movimentacao(info, id_item, nome, "Saída", instancia_tela)
                  ).pack(side="left", padx=5, pady=5)

    ctk.CTkButton(meio, text="Histórico", font=("Inter", 12), text_color=TEXTO,
                  fg_color=BOTOES, hover_color=BOTOES_HOVER, width=90,
                  command=lambda: historico_movimentacoes(info, id_item, nome)
                  ).pack(side="left", padx=5, pady=5)

    # Informações
    titulos = [
        ("Nome:",         20,  10),
        ("Categoria:",   280,  10),
        ("Quantidade:",   20,  70),
        ("Mínimo:",      200,  70),
        ("Unidade:",     350,  70),
        ("Localização:",  20, 130),
        ("Observações:",  20, 190),
    ]
    for titulo, x, y in titulos:
        ctk.CTkLabel(resto, text=titulo, text_color=TEXTO, fg_color="transparent",
                     font=("Inter", 15, "bold")).place(x=x, y=y)

    valores = [
        (str(nome),        20,  35),
        (str(categoria),  280,  35),
        (str(quantidade), 20,   95),
        (str(est_minimo), 200,  95),
        (str(unidade),    350,  95),
        (str(localizacao), 20, 155),
        (str(observacoes), 20, 215),
    ]
    for valor, x, y in valores:
        ctk.CTkLabel(resto, text=valor, text_color=TEXTO_SECUNDARIO, fg_color="transparent",
                     font=("Inter", 14)).place(x=x, y=y)

    print(f"RELATÓRIO: Informações do item '{nome}' abertas.")


# **************
# Movimentações
# **************

def registrar_movimentacao(pai, id_item, nome_item, tipo, instancia_tela):
    modal = ctk.CTkToplevel(pai)
    modal.title(f"Registrar {tipo}")
    modal.geometry("360x350")
    modal.attributes("-topmost", True)
    modal.grab_set()
    modal.configure(fg_color=FUNDO)

    cor_topo = BOTAO_SUCESSO if tipo == "Entrada" else BOTAO_ERRO

    topo = ctk.CTkFrame(modal, fg_color=cor_topo, height=45, corner_radius=0)
    topo.pack(fill="x")
    ctk.CTkLabel(topo, text=f"Registrar {tipo}", text_color="white",
                 font=("Inter", 16, "bold")).place(relx=0.5, rely=0.5, anchor="center")

    resto = ctk.CTkFrame(modal, fg_color="transparent", corner_radius=0)
    resto.pack(fill="both", expand=True)

    ctk.CTkLabel(resto, text=f"Item: {nome_item}", text_color=TEXTO,
                 font=("Inter", 13, "bold")).place(x=20, y=15)

    campos_mov = [
        ("Quantidade:",                   "Quantidade",   20,  55, 150),
        ("Responsável:",                  "Responsavel",  20, 115, 200),
        ("Data (DD/MM/AAAA):",            "Data",         20, 175, 150),
        ("Motivo:",                       "Motivo",       20, 235, 280),
    ]

    campos = {}
    for label, chave, x, y, larg in campos_mov:
        ctk.CTkLabel(resto, text=label, text_color=TEXTO,
                     font=("Inter", 13, "bold")).place(x=x, y=y - 20)
        entry = ctk.CTkEntry(resto, font=("Inter", 13), width=larg,
                             fg_color="DarkGrey", text_color=TEXTO)
        entry.place(x=x, y=y)
        campos[chave] = entry

    campos["Data"].insert(0, time.strftime("%d/%m/%Y"))

    def salvar():
        qtd_str     = campos["Quantidade"].get().strip()
        responsavel = campos["Responsavel"].get().strip()
        data_raw    = campos["Data"].get().strip()
        motivo      = campos["Motivo"].get().strip()

        if not qtd_str:
            messagebox.showwarning("Aviso", "A quantidade é obrigatória!")
            return
        try:
            qtd = float(qtd_str)
            if qtd <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Digite uma quantidade válida e maior que zero!")
            return

        if not data_raw:
            messagebox.showwarning("Aviso", "A data é obrigatória!")
            return

        try:
            d, m, a = data_raw.split("/")
            data_db = f"{a}-{m.zfill(2)}-{d.zfill(2)}"
        except:
            messagebox.showerror("Erro", "Data inválida! Use DD/MM/AAAA.")
            return

        try:
            with sqlite3.connect("banco.db") as conn:
                # Registra a movimentação
                conn.execute("""
                    INSERT INTO movimentacoes_estoque
                        (item_id, tipo, quantidade, data_movimentacao, responsavel, motivo)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (id_item, tipo, qtd, data_db, responsavel, motivo))

                # Atualiza quantidade no estoque
                if tipo == "Entrada":
                    conn.execute("UPDATE estoque SET quantidade = quantidade + ? WHERE id = ?", (qtd, id_item))
                else:
                    # Verifica se tem saldo suficiente
                    saldo = conn.execute("SELECT quantidade FROM estoque WHERE id = ?", (id_item,)).fetchone()[0]
                    if qtd > saldo:
                        messagebox.showerror("Erro", f"Quantidade insuficiente! Saldo atual: {saldo}")
                        return
                    conn.execute("UPDATE estoque SET quantidade = quantidade - ? WHERE id = ?", (qtd, id_item))

                conn.commit()

            messagebox.showinfo("Sucesso", f"{tipo} de {qtd} registrada!")
            print(f"RELATÓRIO: {tipo} de {qtd} no item '{nome_item}' registrada.")
            atualizar_tabela_estoque(instancia_tela, "")
            modal.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar movimentação: {e}")

    ctk.CTkButton(resto, text="Salvar", text_color=TEXTO, fg_color=BOTOES,
                  hover_color=BOTOES_HOVER, font=("Inter", 14),
                  command=salvar).place(relx=0.5, rely=0.93, anchor="center")


# ***********
# Histórico
# ***********

def historico_movimentacoes(pai, id_item, nome_item):
    hist = ctk.CTkToplevel(pai)
    hist.geometry("800x500")
    hist.title(f"Histórico - {nome_item}")
    hist.attributes("-topmost", True)
    hist.grab_set()
    hist.configure(fg_color=FUNDO)

    topo = ctk.CTkFrame(hist, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    meio = ctk.CTkFrame(hist, fg_color="transparent", corner_radius=0, height=35)
    meio.pack(fill="x")
    resto = ctk.CTkFrame(hist, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)

    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                 text="Histórico de Movimentações").place(relx=0.5, rely=0.5, anchor="center")
    ctk.CTkLabel(meio, text_color=TEXTO, font=("Inter", 13, "bold"),
                 text=f"Item: {nome_item}").pack(side="left", padx=20, pady=5)

    estilo = ttk.Style()
    estilo.theme_use("clam")

    colunas = ("id", "tipo", "quantidade", "data", "responsavel", "motivo")
    tabela = ttk.Treeview(resto, columns=colunas, show="headings")

    tabela.tag_configure("par",    background=LINHA_PAR)
    tabela.tag_configure("impar",  background=LINHA_IMPAR)
    tabela.tag_configure("entrada", background="#DCFCE7")   # verde claro
    tabela.tag_configure("saida",   background="#FEE2E2")   # vermelho claro

    tabela.heading("id",          text="ID")
    tabela.heading("tipo",        text="Tipo")
    tabela.heading("quantidade",  text="Quantidade")
    tabela.heading("data",        text="Data")
    tabela.heading("responsavel", text="Responsável")
    tabela.heading("motivo",      text="Motivo")

    tabela.column("id",          width=40,  anchor="center", stretch=False)
    tabela.column("tipo",        width=80,  anchor="center")
    tabela.column("quantidade",  width=100, anchor="center")
    tabela.column("data",        width=100, anchor="center")
    tabela.column("responsavel", width=150, anchor="center")
    tabela.column("motivo",      width=250, anchor="center")

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            id,
            tipo,
            quantidade,
            strftime('%d/%m/%Y', data_movimentacao),
            responsavel,
            motivo
        FROM movimentacoes_estoque
        WHERE item_id = ?
        ORDER BY data_movimentacao DESC
    """, (id_item,))
    dados = cursor.fetchall()
    conn.close()

    for i, linha in enumerate(dados):
        tag = "entrada" if linha[1] == "Entrada" else "saida"
        tabela.insert("", "end", values=linha, tags=(tag,))

    tabela.pack(fill="both", expand=True, padx=20, pady=10)