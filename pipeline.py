import pandas as pd
from sqlalchemy import create_engine

# Caminho do CSV
csv_path = 'data/IOT-temp.csv'  # ajuste o caminho se necessário

# Lê o arquivo CSV
df = pd.read_csv(csv_path)

# Conecta ao PostgreSQL (ajuste se mudou usuário/senha/banco)
engine = create_engine('postgresql://postgres:senha123@localhost:5432/postgres')

# Insere os dados em uma nova tabela chamada temperature_readings
df.to_sql('temperature_readings', engine, if_exists='replace', index=False)

print("Dados inseridos com sucesso!")
