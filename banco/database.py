import sqlite3

def conectar():
    return sqlite3.connect("banco.db")

def criar_tabelas(conn):
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS produtor_rural(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pessoa TEXT NOT NULL,
        nome TEXT NOT NULL,
        registro_mapa TEXT NOT NULL,
        data_nasc TEXT,
        rg TEXT UNIQUE,
        cpf_cnpj TEXT UNIQUE NOT NULL,
        endereco TEXT,
        telefone TEXT,
        celular TEXT,
        email TEXT
        )""") # Pessoa refere-se à Física ou Jurídica
    
    # Tabela usuarios
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL, 
        cargo TEXT, 
        nivel_acesso TEXT,
        ativo INTEGER DEFAULT 1
    )""")
    
    # Tabela funcionarios
    cursor.execute("""CREATE TABLE IF NOT EXISTS funcionarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT,
        telefone TEXT,
        endereco TEXT, 
        cargo TEXT,
        data_admissao TEXT, 
        observacoes TEXT,
        ativo INTEGER DEFAULT 1
    )""")
    
    # Tabela animais
    cursor.execute("""CREATE TABLE IF NOT EXISTS animais(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brinco TEXT UNIQUE,
        nome TEXT,
        tipo TEXT, 
        sexo TEXT,
        raca TEXT,
        data_nascimento TEXT,
        peso_atual REAL,
        lote_id INTEGER,
        status TEXT,
        origem TEXT,
        observacoes TEXT,
        ativo INTEGER DEFAULT 1,
        
        FOREIGN KEY(lote_id) REFERENCES lote(id)
    )""") # Tipo ( Leite ou Corte )
    
    # Tabela de pesagens relacionais
    cursor.execute("""CREATE TABLE IF NOT EXISTS pesagens(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal_id INTEGER,
        data_pesagem TEXT,
        peso REAL,
        observacoes TEXT,
        
        FOREIGN KEY (animal_id) REFERENCES animais(id))
    """)
    
    # Tabela vacinas
    cursor.execute("""CREATE TABLE IF NOT EXISTS vacinas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal_id INTEGER,
        vacina TEXT,
        data_aplicacao TEXT,
        proxima_dose TEXT,
        responsavel TEXT,
        observacoes TEXT,
        
        FOREIGN KEY (animal_id) REFERENCES animais(id)
    )""")
    
    # Tabela produção de leite
    cursor.execute("""CREATE TABLE IF NOT EXISTS producao_leite(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal_id INTEGER,
        data_producao TEXT,
        litros REAL,
        turno TEXT,
        observacoes TEXT,
        
        FOREIGN KEY(animal_id) REFERENCES animais(id)
    )""")
    
    # Reprodução 
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS reproducao(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal_id INTEGER,
        tipo TEXT,
        data_evento TEXT,
        resultado TEXT,
        observacoes TEXT,
        
        FOREIGN KEY(animal_id) REFERENCES animais(id)
    )""")
    
    # Plantações
    cursor.execute("""CREATE TABLE IF NOT EXISTS plantacoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cultura TEXT,
        area TEXT,
        hectares REAL,
        data_plantio TEXT,
        previsao_colheita TEXT,
        status TEXT,
        observacoes TEXT
    )""")
    
    # Aplicações agrícolas
    cursor.execute("""CREATE TABLE IF NOT EXISTS aplicacoes_agricolas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plantacao_id INTEGER,
        produto TEXT,
        tipo TEXT,
        quantidade REAL,
        data_aplicacao TEXT,
        responsavel TEXT,
        observacoes TEXT,

        FOREIGN KEY(plantacao_id) REFERENCES plantacoes(id)
    )""")
    
    # Maquinas
    cursor.execute("""CREATE TABLE IF NOT EXISTS maquinas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        tipo TEXT,
        modelo TEXT,
        fabricante TEXT,
        ano INTEGER,
        placa TEXT,
        horas_uso REAL,
        status TEXT,
        observacoes TEXT
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS manutencoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        maquina_id INTEGER,
        tipo_manutencao TEXT,
        data_manutencao TEXT,
        proxima_manutencao TEXT,
        descricao TEXT,
        responsavel TEXT,

        FOREIGN KEY(maquina_id) REFERENCES maquinas(id)
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS estoque(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        categoria TEXT,
        unidade TEXT,
        quantidade REAL,
        estoque_minimo REAL,
        localizacao TEXT,
        observacoes TEXT
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS movimentacoes_estoque(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        tipo TEXT, 
        quantidade REAL,
        data_movimentacao TEXT,
        responsavel TEXT,
        motivo TEXT,
        observacoes TEXT,

        FOREIGN KEY(item_id) REFERENCES estoque(id)
    )""") # Tipo refere a Entrada ou Saída
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        acao TEXT,
        tabela_afetada TEXT,
        data_hora TEXT,
        descricao TEXT,

        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS lote(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        tamanho REAL,
        localizacao TEXT,
        descricao TEXT,
        ativo INTEGER DEFAULT 1
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS fazenda(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_fazenda TEXT NOT NULL UNIQUE,
        tamanho REAL,
        endereco TEXT,
        data_fundacao TEXT,
        dono TEXT,
        logo_fazenda TEXT
    )""")
    
    conn.commit()