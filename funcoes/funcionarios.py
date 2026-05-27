import sqlite3
import customtkinter as ctk
from tkinter import messagebox, ttk
import time

# Paleta de Cores
FUNDO = "#F8FAFC"
MENU_LATERAL = "#E2E8F0"
LINHA_PAR = "#F8FAFC"
LINHA_IMPAR = "#EEF2F7"
BOTOES = "#2563EB"
BOTOES_HOVER = "#1D4ED8"
BOTAO_SUCESSO = "#16A34A"
BOTAO_SUCESSO_HOVER = "#15803D"
BOTAO_ERRO = "#DC2626"
BOTAO_ERRO_HOVER = "#B91C1C"
TEXTO = "#0F172A"
TEXTO_SECUNDARIO = "#475569"
SCROLLBAR = "#CBD5E1"

# *********
# Contagem
# *********

def funcionarios_qnt():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) FROM funcionarios WHERE ativo = 1")
    contador = cursor.fetchone()
    conn.close()
    return contador[0]

# *********
# Banco
# *********

def buscar_funcionarios(event, instancia_tela):
    termo = instancia_tela.entrada_pesquisa.get()
    atualizar_tabela_funcionarios(instancia_tela, termo)

def atualizar_tabela_funcionarios(instancia_tela, termo=""):
    for item in instancia_tela.tabela.get_children():
        instancia_tela.tabela.delete(item)
    dados = buscar_funcionarios_db(termo)
    for i, linha in enumerate(dados):
        cor = "par" if i % 2 == 0 else "impar"
        instancia_tela.tabela.insert("", "end", values=linha, tags=(cor,))

def buscar_funcionarios_db(nome):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            id, nome, cpf, cargo, telefone,
            strftime('%d/%m/%Y', data_admissao) as data_admissao
        FROM funcionarios
        WHERE nome LIKE ?
        AND ativo = 1
        ORDER BY nome ASC
    """, (f'%{nome}%',))
    dados = cursor.fetchall()
    conn.close()
    return dados

# *********
# Cadastro
# *********

def novo_funcionario(self):
    cadastro = ctk.CTkToplevel()
    cadastro.geometry("500x500")
    cadastro.title("Novo Funcionário")
    cadastro.attributes("-topmost", True)
    cadastro.grab_set()
    cadastro.configure(fg_color=FUNDO)

    topo = ctk.CTkFrame(cadastro, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(cadastro, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)
    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                 text="Cadastro de Funcionário").place(relx=0.5, rely=0.5, anchor="center")

    titulos = [
        ("Nome:",               20,  10),
        ("CPF:",               370,  10),
        ("Cargo:",              20,  70),
        ("Telefone:",          250,  70),
        ("Endereço:",           20, 130),
        ("Data Admissão\n(DD/MM/AAAA):", 20, 190),
        ("Observações:",        20, 270),
    ]
    for nome, x, y in titulos:
        ctk.CTkLabel(resto, text=nome, text_color=TEXTO, fg_color="transparent",
                     font=("Inter", 15, "bold")).place(x=x, y=y)

    campos = {}

    entradas = [
        (320, 20,  35, "Nome"),
        (100, 370, 35, "CPF"),
        (200, 20,  95, "Cargo"),
        (180, 250, 95, "Telefone"),
        (440, 20, 155, "Endereco"),
        (120, 20, 230, "DataAdmissao"),
        (440, 20, 295, "Observacoes"),
    ]
    for largura, x, y, nome in entradas:
        entry = ctk.CTkEntry(resto, text_color=TEXTO, font=("Inter", 14),
                             width=largura, fg_color="DarkGrey")
        entry.place(x=x, y=y)
        campos[nome] = entry

    campos["DataAdmissao"].insert(0, time.strftime("%d/%m/%Y"))

    ctk.CTkButton(resto, text_color="black", font=("Inter", 14),
                  fg_color=BOTOES, hover_color=BOTOES_HOVER, text="Cadastrar",
                  command=lambda: cadastrar_funcionario(cadastro, campos, self)
                  ).place(relx=0.5, rely=0.93, anchor="center")


def cadastrar_funcionario(cadastro, campos, instancia_tela):
    dados = {campo: entry.get().strip() for campo, entry in campos.items()}

    if dados["Nome"] == "":
        messagebox.showwarning("Aviso", "O campo Nome é obrigatório!")
        return

    data_db = None
    if dados["DataAdmissao"]:
        try:
            d, m, a = dados["DataAdmissao"].split("/")
            data_db = f"{a}-{m.zfill(2)}-{d.zfill(2)}"
        except:
            messagebox.showerror("Erro", "Data de admissão inválida! Use DD/MM/AAAA.")
            return

    try:
        with sqlite3.connect("banco.db") as conn:
            conn.cursor().execute("""
                INSERT INTO funcionarios(nome, cpf, telefone, endereco, cargo, data_admissao, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (dados["Nome"], dados["CPF"], dados["Telefone"], dados["Endereco"],
                  dados["Cargo"], data_db, dados["Observacoes"]))
            conn.commit()
        messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
        print(f"RELATÓRIO: Funcionário '{dados['Nome']}' cadastrado.")
        atualizar_tabela_funcionarios(instancia_tela, "")
        cadastro.destroy()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "CPF já cadastrado!")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível cadastrar: {e}")


# ***********
# Informações
# ***********

def informacao_funcionario(self, dados_func, instancia_tela):
    info = ctk.CTkToplevel(self)
    info.title("Informações do Funcionário")
    info.geometry("480x420")
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
                 text="Informações do Funcionário").place(relx=0.5, rely=0.5, anchor="center")

    id_func      = dados_func[0]
    nome         = dados_func[1]
    cpf          = dados_func[2]
    cargo        = dados_func[3]
    telefone     = dados_func[4]
    endereco     = dados_func[5]
    data_adm     = dados_func[6]
    observacoes  = dados_func[7]

    # Botão editar no topo
    ctk.CTkButton(meio, text="Editar", font=("Inter", 12), text_color=TEXTO,
                  fg_color=BOTAO_SUCESSO, hover_color=BOTAO_SUCESSO_HOVER, width=90,
                  command=lambda: editar_funcionario(info, id_func, dados_func, instancia_tela)
                  ).pack(side="left", padx=10, pady=5)

    titulos_valores = [
        ("Nome:",           str(nome or "—"),      20,  10),
        ("CPF:",            str(cpf or "—"),       280,  10),
        ("Cargo:",          str(cargo or "—"),      20,  70),
        ("Telefone:",       str(telefone or "—"),  280,  70),
        ("Endereço:",       str(endereco or "—"),   20, 130),
        ("Data Admissão:", str(data_adm or "—"),   20, 190),
        ("Observações:",    str(observacoes or "—"), 20, 250),
    ]

    for titulo, valor, x, y in titulos_valores:
        ctk.CTkLabel(resto, text=titulo, text_color=TEXTO, fg_color="transparent",
                     font=("Inter", 15, "bold")).place(x=x, y=y)
        ctk.CTkLabel(resto, text=valor, text_color=TEXTO_SECUNDARIO, fg_color="transparent",
                     font=("Inter", 14)).place(x=x, y=y + 25)

    print(f"RELATÓRIO: Informações do funcionário '{nome}' abertas.")


# *******
# Editar
# *******

def editar_funcionario(pai, id_func, dados_func, instancia_tela):
    modal = ctk.CTkToplevel(pai)
    modal.geometry("500x400")
    modal.title("Editar Funcionário")
    modal.attributes("-topmost", True)
    modal.grab_set()
    modal.configure(fg_color=FUNDO)

    topo = ctk.CTkFrame(modal, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(modal, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)
    ctk.CTkLabel(topo, text_color=TEXTO, font=("Inter", 18, "bold"),
                 text="Editar Funcionário").place(relx=0.5, rely=0.5, anchor="center")

    # dados_func: (id, nome, cpf, cargo, telefone, endereco, data_admissao, observacoes)
    nome_val     = dados_func[1] or ""
    cpf_val      = dados_func[2] or ""
    cargo_val    = dados_func[3] or ""
    telefone_val = dados_func[4] or ""
    endereco_val = dados_func[5] or ""
    data_val     = dados_func[6] or ""
    obs_val      = dados_func[7] or ""

    titulos = [
        ("Nome:",          20,  10),
        ("CPF:",          370,  10),
        ("Cargo:",         20,  70),
        ("Telefone:",     250,  70),
        ("Endereço:",      20, 130),
        ("Data Admissão\n(DD/MM/AAAA):", 20, 190),
        ("Observações:",   20, 270),
    ]
    for nome, x, y in titulos:
        ctk.CTkLabel(resto, text=nome, text_color=TEXTO, fg_color="transparent",
                     font=("Inter", 15, "bold")).place(x=x, y=y)

    campos = {}
    entradas_config = [
        (320, 20,  35, "Nome",         nome_val),
        (100, 370, 35, "CPF",          cpf_val),
        (200, 20,  95, "Cargo",        cargo_val),
        (180, 250, 95, "Telefone",     telefone_val),
        (440, 20, 155, "Endereco",     endereco_val),
        (120, 20, 230, "DataAdmissao", data_val),
        (440, 20, 295, "Observacoes",  obs_val),
    ]
    for largura, x, y, chave, valor_inicial in entradas_config:
        entry = ctk.CTkEntry(resto, text_color=TEXTO, font=("Inter", 14),
                             width=largura, fg_color="DarkGrey")
        entry.insert(0, valor_inicial)
        entry.place(x=x, y=y)
        campos[chave] = entry

    def salvar_edicao():
        dados = {campo: entry.get().strip() for campo, entry in campos.items()}

        if not dados["Nome"]:
            messagebox.showwarning("Aviso", "O campo Nome é obrigatório!")
            return

        data_db = None
        if dados["DataAdmissao"]:
            try:
                d, m, a = dados["DataAdmissao"].split("/")
                data_db = f"{a}-{m.zfill(2)}-{d.zfill(2)}"
            except:
                messagebox.showerror("Erro", "Data inválida! Use DD/MM/AAAA.")
                return

        try:
            with sqlite3.connect("banco.db") as conn:
                conn.execute("""
                    UPDATE funcionarios
                    SET nome=?, cpf=?, telefone=?, endereco=?, cargo=?, data_admissao=?, observacoes=?
                    WHERE id=?
                """, (dados["Nome"], dados["CPF"], dados["Telefone"], dados["Endereco"],
                      dados["Cargo"], data_db, dados["Observacoes"], id_func))
                conn.commit()
            messagebox.showinfo("Sucesso", "Funcionário atualizado!")
            print(f"RELATÓRIO: Funcionário id={id_func} atualizado.")
            atualizar_tabela_funcionarios(instancia_tela, "")
            modal.destroy()
            pai.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível atualizar: {e}")

    ctk.CTkButton(resto, text="Salvar", text_color="black", font=("Inter", 14),
                  fg_color=BOTOES, hover_color=BOTOES_HOVER,
                  command=salvar_edicao).place(relx=0.5, rely=0.93, anchor="center")