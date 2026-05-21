import sqlite3
from faker import Faker
import random

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

maquinas = [
    (
        "Trator Principal",
        "Trator",
        "6110J",
        "John Deere",
        2021,
        "QWE1A23",
        2450.5,
        "Ativo",
        "Utilizado no preparo do solo"
    ),

    (
        "Colheitadeira 01",
        "Colheitadeira",
        "S770",
        "John Deere",
        2020,
        "ABC4D56",
        3890.2,
        "Manutenção",
        "Troca de correia programada"
    ),

    (
        "Pulverizador Campo Norte",
        "Pulverizador",
        "Imperador 3000",
        "Stara",
        2022,
        "FGH7J89",
        1120.0,
        "Ativo",
        "Equipamento novo"
    ),

    (
        "Plantadeira Central",
        "Plantadeira",
        "Momentum 40",
        "Fendt",
        2023,
        "KLM2N34",
        540.7,
        "Ativo",
        "Excelente desempenho"
    ),

    (
        "Retroescavadeira",
        "Retroescavadeira",
        "3CX",
        "JCB",
        2019,
        "XYZ9P87",
        4725.9,
        "Inativo",
        "Aguardando peças"
    )
]

# ==========================================
# INSERT
# ==========================================

cursor.executemany("""
INSERT INTO maquinas (
    nome,
    tipo,
    modelo,
    fabricante,
    ano,
    placa,
    horas_uso,
    status,
    observacoes
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", maquinas)

conn.commit()
conn.close()
print("Dados inseridos com sucesso!")
