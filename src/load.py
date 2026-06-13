from dotenv import load_dotenv
import os
from sqlalchemy import URL, create_engine, text
from pathlib import Path
import pandas as pd

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

# Criação do Schema e das tabelas
arquivos_sql = [Path(__file__).resolve().parent.parent / 'sql' / 'create_schemas.sql']

def executar_query (engine_db, path_file):

    for caminho in path_file:

        with engine_db.begin() as conn:
            with open(caminho, mode='r', encoding='utf-8') as arquivo:
                query = arquivo.read()
                conn.execute(text(query))

# Colunas que serão mantidas para ánalise
colunas_participantes = {
    '2022':
        ['nu_inscricao', 'nu_ano', 'tp_faixa_etaria', 'tp_sexo', 'tp_estado_civil', 'tp_cor_raca', 'tp_nacionalidade', 'tp_st_conclusao', 'tp_ano_concluiu', 'tp_escola', 'tp_ensino', 'in_treineiro', 'no_municipio_prova', 'sg_uf_prova', 'q001', 'q002', 'q003', 'q004', 'q005', 'q006', 'q007', 'q008', 'q009', 'q010', 'q011', 'q012', 'q013', 'q014', 'q015', 'q016', 'q017', 'q018', 'q019', 'q020', 'q021', 'q022', 'q023', 'q024', 'q025'],
    '2023': 
        ['nu_inscricao', 'nu_ano', 'tp_faixa_etaria', 'tp_sexo', 'tp_estado_civil', 'tp_cor_raca', 'tp_nacionalidade', 'tp_st_conclusao', 'tp_ano_concluiu', 'tp_escola', 'tp_ensino', 'in_treineiro', 'no_municipio_prova', 'sg_uf_prova', 'q001', 'q002', 'q003', 'q004', 'q005', 'q006', 'q007', 'q008', 'q009', 'q010', 'q011', 'q012', 'q013', 'q014', 'q015', 'q016', 'q017', 'q018', 'q019', 'q020', 'q021', 'q022', 'q023', 'q024', 'q025'],
    '2024':
        ['nu_inscricao', 'nu_ano', 'tp_faixa_etaria', 'tp_sexo', 'tp_estado_civil', 'tp_cor_raca', 'tp_nacionalidade', 'tp_st_conclusao', 'tp_ano_concluiu', 'tp_ensino', 'in_treineiro', 'no_municipio_prova', 'sg_uf_prova', 'q001',  'q002', 'q003', 'q004', 'q005', 'q006', 'q007', 'q008', 'q009', 'q010', 'q011', 'q012', 'q013', 'q014', 'q015', 'q016', 'q017', 'q018', 'q019', 'q020', 'q021', 'q022', 'q023']
}


colunas_resultados = {
    '2022':
        ['nu_inscricao', 'nu_ano', 'no_municipio_esc', 'sg_uf_esc', 'tp_dependencia_adm_esc','tp_localizacao_esc','tp_sit_func_esc','no_municipio_prova', 'sg_uf_prova','tp_presenca_cn','tp_presenca_ch','tp_presenca_lc','tp_presenca_mt','nu_nota_cn','nu_nota_ch','nu_nota_lc','nu_nota_mt','nu_nota_redacao','nu_nota_comp1', 'nu_nota_comp2','nu_nota_comp3','nu_nota_comp4','nu_nota_comp5','tp_status_redacao'],
    '2023':
        ['nu_inscricao', 'nu_ano', 'no_municipio_esc', 'sg_uf_esc', 'tp_dependencia_adm_esc','tp_localizacao_esc','tp_sit_func_esc','no_municipio_prova', 'sg_uf_prova','tp_presenca_cn','tp_presenca_ch','tp_presenca_lc','tp_presenca_mt','nu_nota_cn','nu_nota_ch','nu_nota_lc','nu_nota_mt','nu_nota_redacao','nu_nota_comp1', 'nu_nota_comp2','nu_nota_comp3','nu_nota_comp4','nu_nota_comp5','tp_status_redacao'],    
    '2024':
        ['nu_sequencial', 'nu_ano', 'no_municipio_esc', 'sg_uf_esc', 'tp_dependencia_adm_esc','tp_localizacao_esc','tp_sit_func_esc','no_municipio_prova', 'sg_uf_prova','tp_presenca_cn','tp_presenca_ch','tp_presenca_lc','tp_presenca_mt','nu_nota_cn','nu_nota_ch','nu_nota_lc','nu_nota_mt','nu_nota_redacao','nu_nota_comp1', 'nu_nota_comp2','nu_nota_comp3','nu_nota_comp4','nu_nota_comp5','tp_status_redacao']
}

# Função que carrega os dados para o Schema Bronze
def carregar_bronze (colunas, ano_exame, nome_tabela, nome_csv):
    
    caminho_csv = Path(__file__).resolve().parent.parent / 'data' / ano_exame / nome_csv

    print(f"Lendo arquivo [{caminho_csv}]...\n")

    df_participantes = pd.read_csv(
        caminho_csv, 
        encoding='latin-1', 
        sep=";",
        usecols=[col.upper() for col in colunas[ano_exame]],
        dtype=str
    )

    df_participantes.columns = df_participantes.columns.str.lower()

    nome = f'raw_{nome_tabela}_{ano_exame}'

    print(f"Leitura realizada com sucesso!\nCarregando dados da tabela [{nome}] na camada bronze...\n")

    df_participantes.to_sql(name=nome, con=engine, schema='bronze', if_exists='replace', index=False, chunksize=8192)

    print("Dados escritos no banco de dados com sucesso!\n")

# Loop com todas os arquivos CSVs
periodos = ['2022', '2023', '2024']

if __name__ == '__main__':

    executar_query(engine_db=engine, path_file=arquivos_sql)

    for ano in periodos:

        if ano in ['2022', '2023']:
            carregar_bronze(colunas=colunas_participantes, ano_exame=ano, nome_tabela='participantes', nome_csv=f'MICRODADOS_ENEM_{ano}.csv')
            carregar_bronze(colunas=colunas_resultados, ano_exame=ano, nome_tabela='resultados', nome_csv=f'MICRODADOS_ENEM_{ano}.csv')
        else:
            carregar_bronze(colunas=colunas_participantes, ano_exame=ano, nome_tabela='participantes', nome_csv=f'PARTICIPANTES_{ano}.csv')
            carregar_bronze(colunas=colunas_resultados, ano_exame=ano, nome_tabela='resultados', nome_csv=f'RESULTADOS_{ano}.csv')