import sqlite3
import customtkinter as ctk
from tkinter import messagebox

FUNDO = "#F5F7FA"
MENU_LATERAL = "#1E293B"
BOTOES = "#2563EB"
CARDS = "#FFFFFF"
TABELAS = "#FFFFFF"
HOVER_TABELA = "#EFF6FF"
TEXTO = "black"

    # *********
    # Cadastros
    # *********

def novo_animal(self):
    cadastro = ctk.CTkToplevel()
    cadastro.geometry("540x500")
    cadastro.title("Novo Animal")
    cadastro.attributes("-topmost", True)
    cadastro.grab_set()
    cadastro.configure(fg_color=FUNDO)
    
    topo = ctk.CTkFrame(cadastro, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(cadastro, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)
    title = ctk.CTkLabel(topo, text_color="white", font=("Inter", 18, "bold"), text="Cadastro de Animais")
    title.place(relx=0.5, rely=0.5, anchor="center")
    
    # Labels
    titulos = [
        ("Nome:", 20, 10),
        ("Brinco:", 300, 10),
        ("Lote:", 420, 10),
        ("Peso Atual:", 20, 70),
        ("Data Nasc.:", 160, 70),
        ("Raça:", 300, 70),
        ("Origem:", 20, 130),
        ("Tipo:", 420, 130),
        ("Sexo:", 300, 130),
        ("Status:", 180,130),
        ("Observações:", 20, 190)
    ]
    
    for nome, x, y in titulos:
        entradas = ctk.CTkLabel(resto, text=nome, text_color="black", fg_color="transparent", font=("Inter", 16, "bold"))
        entradas.place(x=x, y=y)
        
    # Entrys
    campos = {}
    
    entradas = [
        (250, 20, 35, "Nome"),              # Nome
        (75, 300, 35, "Brinco"),            # Brinco
        (75, 420, 35, "Lote"),              # Lote
        (75, 20, 95, "Peso Atual"),         # Peso Atual
        (95, 160, 95, "Data Nascimento"),   # Data Nascimento
        (75, 300, 95, "Raça"),              # Raça
        (150, 20, 155, "Origem"),           # Origem
        (150, 20, 215, "Observações")
    ]
    
    for largura, x, y, nome in entradas:
        entry = ctk.CTkEntry(resto,text_color="black", font=("Inter", 14), width=largura, fg_color="DarkGrey")
        entry.place(x=x, y=y)

        campos[nome] = entry
    

    opcoes_selecionaveis = [
        ("Sexo", ["Leite", "Corte"], 180, 155),                                     # Tipo 
        ("Tipo", ["Macho", "Fêmea"], 300, 155),                                     # Sexo
        ("Status", ["Ativo", "Tratamento", "Seca", "Prenha", "Abate"], 420, 155)    # Status
    ]
    
    for i, (nome, valores, x, y) in enumerate(opcoes_selecionaveis):
        opcoes_combo = ctk.CTkComboBox(resto, values=valores, width=100)
        opcoes_combo.place(x=x, y=y)
        
        campos[nome] = opcoes_combo
    
    btn_salvar = ctk.CTkButton(resto, text_color="black", font=("Inter", 14), fg_color=BOTOES, text="Cadastrar", command= lambda: cadastrar_animais(cadastro, campos, self))
    btn_salvar.place(relx=0.5, rely=0.9, anchor="center")
    
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
        if i % 2 == 0:
            cor = "par"
        else:
            cor = "impar"
        instancia_tela.tabela.insert("", "end", values=linha, tags=(cor,))

def buscar_animais_db(nome):
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                id, 
                brinco,
                nome, 
                tipo, 
                sexo,
                printf('%.2f KG', peso_atual) as peso_atual,
                strftime('%d/%m/%Y', data_nascimento) as data_nascimento, 
                status,
                lote
            FROM animais
            WHERE nome LIKE ?
            ORDER BY sexo DESC, nome ASC
        """, (f'%{nome}%',))
        dados = cursor.fetchall()
        conn.close()
        return dados
    

def cadastrar_animais(cadastro, campos, instancia_tela):
    dados = {}

    for campo, entry in campos.items():
        valor = entry.get().strip()
        dados[campo] = valor

    obrigatorios = [
        "Nome",
        "Lote",
        "Peso Atual",
        "Raça",
        "Brinco"
    ]

    for campo in obrigatorios:
        if dados[campo] == "":
            messagebox.showwarning("Aviso", f"O campo {campo} é obrigatório!")
            return
    try:
        peso = float(dados["Peso Atual"])
    except:
        messagebox.showerror("Erro", "Digite um peso válido!")
        return
    try:
        with sqlite3.connect("banco.db") as conn:
            cursor = conn.cursor()
        
            cursor.execute("""
                INSERT INTO animais(
                    nome,
                    brinco,
                    lote,
                    peso_atual,
                    data_nascimento,
                    raca,
                    origem,
                    status,
                    sexo,
                    tipo,
                    observacoes
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dados["Nome"],
                dados["Brinco"],
                dados["Lote"],
                peso,
                dados["Data Nascimento"],
                dados["Raça"],
                dados["Origem"],
                dados["Status"],
                dados["Sexo"],
                dados["Tipo"],
                dados["Observações"]
            ))

            conn.commit()
        messagebox.showinfo("Sucesso", "Animal cadastrado com sucesso!")
        atualizar_tabela_animais(instancia_tela, "")
        cadastro.destroy()
    except sqlite3.IntegrityError:
        brinco = dados["Brinco"]
        messagebox.showerror("Erro", f"Brinco {brinco}, já cadastrado! \nPor favor, coloque outro")

    

def animais_qnt():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(id) FROM animais")
    contador = cursor.fetchone()
    
    conn.close()
    return contador[0]

# Informações

def informacao_animal(self, dados_animais):
    info = ctk.CTkToplevel(self)
    info.title("Informações do animal")
    info.geometry("500x480")
    info.attributes("-topmost", True)
    info.grab_set()
    info.configure(fg_color=FUNDO)
    
    topo = ctk.CTkFrame(info, fg_color=MENU_LATERAL, height=50, corner_radius=0)
    topo.pack(fill="x")
    resto = ctk.CTkFrame(info, corner_radius=0, fg_color="transparent")
    resto.pack(fill="both", expand=True)
    title = ctk.CTkLabel(topo, text_color="white", font=("Inter", 18, "bold"), text="Informações do animal")
    title.place(relx=0.5, rely=0.5, anchor="center")
    
    # Lista para armazenar informações para o laço for ( Títulos )
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
    
    for title, x, y in titulos:
        entradas = ctk.CTkLabel(resto, text=title, text_color="black", fg_color="transparent", font=("Inter", 16, "bold"))
        entradas.place(x=x, y=y)
    
    brinco = dados_animais[1]
    nome = dados_animais[2]
    tipo = dados_animais[3]
    sexo = dados_animais[4]
    raca = dados_animais[5]
    data_nascimento = dados_animais[6]
    peso_atual = dados_animais[7]
    lote = dados_animais[8]
    status = dados_animais[9]
    origem = dados_animais[10]
    observacoes = dados_animais[11]
    
    # Lista para armazenar informações para o laço for ( Informações )
    entradas = [ 
        (20, 35, f"{nome}"),                # Nome
        (300, 35, f"{brinco}"),             # Brinco
        (420, 35, f"{lote}"),               # Lote
        (20, 95, f"{peso_atual}"),          # Peso Atual
        (160, 95, f"{data_nascimento}"),    # Data Nascimento
        (300, 95, f"{raca}"),               # Raça
        (20, 155, f"{status}"),             # Status
        (300, 155, f"{tipo}"),              # Tipo 
        (160, 155, f"{sexo}"),              # Sexo
        (20, 215, f"{origem}"),             # Origem
        (20, 275, f"{observacoes}")         # Observações
    ]
    
    for x, y, escrita in entradas:
        informacoes = ctk.CTkLabel(resto,text_color="black", font=("Inter", 14), fg_color="transparent", text=escrita)
        informacoes.place(x=x, y=y)
    
    btn_salvar = ctk.CTkButton(resto, text_color="black", font=("Inter", 14), fg_color=BOTOES, text="Concluído", command= lambda: info.destroy())
    btn_salvar.place(relx=0.5, rely=0.9, anchor="center")
    
    print(f"RELATÓRIO: Informação animal funcionando! Nome: {nome}. Brinco: {brinco}")
    