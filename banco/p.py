import hashlib, sqlite3
conn = sqlite3.connect("banco.db")
senha = hashlib.sha256("123".encode()).hexdigest()
conn.execute("""INSERT INTO usuarios(nome, usuario, senha, cargo, nivel_acesso)
               VALUES(?, ?, ?, ?, ?)""",
               ("Juvenil", "juve00", senha, "Operador", "operador"))
conn.commit()