import sqlite3
from faker import Faker
import random

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

animais_fixos = [
    ('11', 'Aurora',    'Leite', 'Fêmea', 'Jersey',    '2020-08-09', 498.1, 'Lote A', 'Seca',      'Nascimento na fazenda', 'Período seco'),
]

cursor.executemany("""
    INSERT INTO animais (brinco, nome, tipo, sexo, raca, data_nascimento, peso_atual, lote, status, origem, observacoes, ativo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
""", animais_fixos)

# Animais aleatórios
fake = Faker("pt_BR")
tipos = ["Leite", "Corte"]  # <- corrigido para bater com os valores do sistema
racas = {
    "Leite": ["Holandesa", "Jersey", "Gir", "Girolando"],
    "Corte": ["Nelore", "Angus", "Brahman", "Bonsmara"]
}
sexos = ["Macho", "Fêmea"]
status_list = ["Ativo", "Tratamento", "Seca", "Prenha", "Abate"]  # <- igual ao sistema
lotes = ["Lote A", "Lote B", "Lote C", "Lote D"]
origens = ["Nascimento na fazenda", "Compra", "Leilão"]

for i in range(11, 61):
    tipo = random.choice(tipos)
    cursor.execute("""
        INSERT INTO animais (brinco, nome, tipo, sexo, raca, data_nascimento, peso_atual, lote, status, origem, observacoes, ativo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"BR{i:04d}",
        fake.first_name(),
        tipo,
        random.choice(sexos),
        random.choice(racas[tipo]),
        fake.date_between(start_date="-8y", end_date="-6m").strftime("%Y-%m-%d"),
        round(random.uniform(40, 850), 2),
        random.choice(lotes),
        random.choice(status_list),
        random.choice(origens),
        fake.sentence(nb_words=6),
        1
    ))

conn.commit()
conn.close()
print("Dados inseridos com sucesso!")

