import sqlite3
from random import randint, uniform, choice
from datetime import datetime

# =========================
# CONEXÃO
# =========================
conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

# =========================
# ANIMAIS
# =========================
cursor.execute("""INSERT INTO lote (nome, tamanho, localizacao, descricao, ativo) VALUES
  ('Pasto Norte', 45.5, 'Setor A', 'Lote principal de gado de corte', 1)""")

cursor.execute("""INSERT INTO lote (nome, tamanho, localizacao, descricao, ativo) VALUES
  ('Pasto Sul', 30.0, 'Setor B', 'Lote de novilhas', 1)""")

cursor.execute("""INSERT INTO lote (nome, tamanho, localizacao, descricao, ativo) VALUES
  ('Curral de Engorda', 12.8, 'Setor C', 'Lote de confinamento', 1)""")
cursor.execute("""INSERT INTO animais (brinco, nome, tipo, sexo, raca, data_nascimento, peso_atual, lote_id, status, origem, observacoes, ativo) VALUES
  ('BRN-001', 'Trovao', 'Bovino', 'M', 'Nelore', '2021-03-15', 485.0, 1, 'Ativo', 'Fazenda Boa Vista', NULL, 1)""")

cursor.execute("""INSERT INTO animais (brinco, nome, tipo, sexo, raca, data_nascimento, peso_atual, lote_id, status, origem, observacoes, ativo) VALUES
  ('BRN-002', 'Estrela', 'Bovino', 'F', 'Angus', '2022-07-20', 360.5, 2, 'Ativo', 'Compra direta', 'Prenha', 1)""")

cursor.execute("""INSERT INTO animais (brinco, nome, tipo, sexo, raca, data_nascimento, peso_atual, lote_id, status, origem, observacoes, ativo) VALUES
  ('BRN-003', 'Rajado', 'Bovino', 'M', 'Brahman', '2020-11-05', 520.0, 3, 'Confinado', 'Fazenda Serra Alta', NULL, 1)""")

cursor.execute("""INSERT INTO maquinas (nome, tipo, modelo, fabricante, ano, placa, horas_uso, status, observacoes) VALUES
  ('Trator Azul', 'Trator', 'New Holland TL75E', 'New Holland', 2018, 'ABC-1234', 1250.5, 'Operacional', NULL)""")

cursor.execute("""INSERT INTO maquinas (nome, tipo, modelo, fabricante, ano, placa, horas_uso, status, observacoes) VALUES
  ('Colheitadeira', 'Colheitadeira', 'Case IH 6130', 'Case IH', 2020, 'DEF-5678', 430.0, 'Operacional', 'Revisao em dia')""")

cursor.execute("""INSERT INTO maquinas (nome, tipo, modelo, fabricante, ano, placa, horas_uso, status, observacoes) VALUES
  ('Pulverizador', 'Implemento', 'Jacto Uniport 2500', 'Jacto', 2019, NULL, 680.0, 'Em manutencao', 'Bomba com vazamento')""")
cursor.execute("""INSERT INTO manutencoes (maquina_id, tipo_manutencao, data_manutencao, proxima_manutencao, descricao, responsavel) VALUES
  (1, 'Preventiva', '2024-01-10', '2024-07-10', 'Troca de oleo e filtros', 'Carlos Mecânico')""")

cursor.execute("""INSERT INTO manutencoes (maquina_id, tipo_manutencao, data_manutencao, proxima_manutencao, descricao, responsavel) VALUES
  (2, 'Preventiva', '2024-02-20', '2024-08-20', 'Lubrificação geral e ajuste de esteira', 'Carlos Mecânico')""")

cursor.execute("""INSERT INTO manutencoes (maquina_id, tipo_manutencao, data_manutencao, proxima_manutencao, descricao, responsavel) VALUES
  (3, 'Corretiva', '2024-03-05', NULL, 'Substituicao da bomba de pressao', 'Assistência Jacto')""")
cursor.execute("""INSERT INTO estoque (nome, categoria, unidade, quantidade, estoque_minimo, localizacao, observacoes) VALUES
  ('Ração Bovinos', 'Alimentação', 'kg', 2500.0, 500.0, 'Galpão 1', NULL)""")

cursor.execute("""INSERT INTO estoque (nome, categoria, unidade, quantidade, estoque_minimo, localizacao, observacoes) VALUES
  ('Herbicida Roundup', 'Defensivo', 'L', 80.0, 20.0, 'Depósito Químico', 'Armazenar longe do sol')""")

cursor.execute("""INSERT INTO estoque (nome, categoria, unidade, quantidade, estoque_minimo, localizacao, observacoes) VALUES
  ('Óleo Lubrificante 15W40', 'Insumo', 'L', 45.0, 10.0, 'Galpão de Máquinas', NULL)""")
# FINALIZAÇÃO
# =========================
conn.commit()
conn.close()

print("Banco simulado criado com sucesso!")