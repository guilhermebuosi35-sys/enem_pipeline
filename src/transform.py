from dotenv import load_dotenv
import os
from sqlalchemy import URL, create_engine, text
from pathlib import Path
import pandas as pd
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


# Dicionário com as regras das colunas da tabela participantes
intervalo_participantes = {
    'faixa_etaria': [1, 20],
    'estado_civil': [0, 4],
    'cor_raca': [0, 6],
    'nacionalidade': [0, 4],
    'st_conclusao': [1, 4],
    'ano_conclusao': [0, 18],
    'ensino': [1, 2],
    'treineiro': [0, 1]
}

# Dicionário com as regras das colunas da tabela resultados
intervalo_resultados = {
    'dependencia_adm_esc': [1, 4],
    'localizacao_esc': [1, 2],
    'sit_func_escola': [1, 4],
    'presenca_cn': [0, 3],
    'presenca_ch': [0, 3],
    'presenca_lc': [0, 3],
    'presenca_mt': [0, 3],
    'nota_cn': [0, 1000],
    'nota_ch': [0, 1000],
    'nota_lc': [0, 1000],
    'nota_mt': [0, 1000],
    'status_redacao': [1, 9]
} 

# Função para checar qualidade dos dados, com base nas suas regras
def checar_qualidade (engine_db, tabela):
    
    if "participantes" in tabela: 

        for col, limites in intervalo_participantes.items():
            with engine_db.begin() as conn:
                resultado = conn.execute(text(
                    f'''
                    SELECT COUNT(*)
                    FROM silver.{tabela} 
                    WHERE {col} IS NOT NULL
                        AND ({col} < {limites[0]} OR {col} > {limites[1]})
                    '''
                )).scalar()

                assert resultado == 0, f"Erro: {col} deve constar entre {limites[0]} e {limites[1]}"

    else:

        for col, limites in intervalo_resultados.items():
            with engine_db.begin() as conn:
                resultado = conn.execute(text(
                    f'''
                    SELECT COUNT(*)
                    FROM silver.{tabela} 
                    WHERE {col} IS NOT NULL
                        AND ({col} < {limites[0]} OR {col} > {limites[1]})
                    '''
                )).scalar()

                assert resultado == 0, f"Erro: {col} deve constar entre {limites[0]} e {limites[1]}"

if __name__ == '__main__':

    # Criação das tabelas silver e transformação dos dados
    print("Executando query de criação das tabelas na camada silver...\n")

    caminho_silver = [Path(__file__).resolve().parent.parent / 'sql' / 'transformation_tables.sql']

    executar_query(engine_db=engine, path_file=caminho_silver)

    # Checagem das qualidade dos dados da camada silver
    print("Checando qualidade dos datos e regras do negócio...\n")

    tabelas = ['vw_resultados_2022', 'vw_resultados_2023', 'vw_resultados_2024', 'vw_participantes_2022', 'vw_participantes_2023', 'vw_participantes_2024' ] 

    for tabela in tabelas:
        checar_qualidade(engine_db=engine, tabela=tabela)