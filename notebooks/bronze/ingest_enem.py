# Variáveis iniciais
files_ls = dbutils.fs.ls("/Volumes/enem_pipeline/bronze/raw/")
table_names = []

# Função nomeadora das tabelas
def table_namer (file_name):
    return file_name.replace(".csv", "").lower()

# Loop para caminho e nome das tabelas da camada bronze
for item in files_ls:
    table_names.append((item.path, table_namer(item.name))) 

# Loop de criação das tabelas na camada bronze
for path, table in table_names:
    spark.sql(f"""
        CREATE OR REPLACE TABLE enem_pipeline.bronze.{table}
        COMMENT 'Bronze raw de {table}. Todas as colunas STRING, como vêm do INEP. Recriada a cada execução.'
        AS SELECT
            * EXCEPT (_rescued_data),
            _rescued_data,
            _metadata.file_path AS arquivo_origem,
            _metadata.file_modification_time AS arquivo_modificado_em,
            current_timestamp() AS ingerido_em
        FROM read_files(
            '{path}',
            format => 'csv', 
            header => true, 
            sep => ';',
            multiLine => true, 
            inferColumnTypes => false)
    """)

    print (f"Tabela {table} criada!")