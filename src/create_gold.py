from dotenv import load_dotenv
import os
from sqlalchemy import URL, create_engine
from pathlib import Path
from load import executar_query

# Conexão com o Banco de Dados
load_dotenv()

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
db = os.getenv('POSTGRES_DB')


url_object = URL.create(
    "postgresql+psycopg2",
    username=user,
    password=password,
    host="localhost",
    database=db
)

engine = create_engine(url_object)


# Criação das tabelas gold
print("Executando query de criação das tabelas na camada gold...")

caminho_gold = [Path(__file__).resolve().parent.parent / 'sql' / 'gold_tables.sql']

executar_query(engine_db=engine, path_file=caminho_gold)