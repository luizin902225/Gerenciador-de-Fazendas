import sqlite3
from faker import Faker
import random

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

cursor.execute("""INSERT INTO usuarios(nome, usuario, senha, cargo, nivel_acesso) VALUES (?, ?, ?, ?, ?)""", ("admin", "admin", "123", "admin", "admin"))

conn.commit()
conn.close()
print("Dados inseridos com sucesso!")
