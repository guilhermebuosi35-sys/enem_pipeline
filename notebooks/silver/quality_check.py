# Dicionário com as regras das colunas da tabela participantes
range_participants = {
    'TP_FAIXA_ETARIA': [1, 20],
    'TP_ESTADO_CIVIL': [0, 4],
    'TP_COR_RACA': [0, 6],
    'TP_NACIONALIDADE': [0, 4],
    'TP_ST_CONCLUSAO': [1, 4],
    'TP_ANO_CONCLUIU': [0, 18],
    'TP_ENSINO': [1, 2],
    'IN_TREINEIRO': [0, 1]
}

# Dicionário com as regras das colunas da tabela resultados
range_results = {
    'TP_DEPENDENCIA_ADM_ESC': [1, 4],
    'TP_LOCALIZACAO_ESC': [1, 2],
    'TP_SIT_FUNC_ESC': [1, 4],
    'TP_PRESENCA_CN': [0, 3],
    'TP_PRESENCA_CH': [0, 3],
    'TP_PRESENCA_LC': [0, 3],
    'TP_PRESENCA_MT': [0, 3],
    'NU_NOTA_CN': [0, 1000],
    'NU_NOTA_CH': [0, 1000],
    'NU_NOTA_LC': [0, 1000],
    'NU_NOTA_MT': [0, 1000],
    'TP_STATUS_REDACAO': [1, 9]
} 

# Levantamento das tabelas na camada bronze
tables_ls = spark.sql("SHOW TABLES IN enem_pipeline.bronze")

# Função de checagem de qualidade dos dados, conforme dicionário descrito pela INEP
def quality_checker(range_rules, table):
    errors = []
    for col, (minimum, maximum) in range_rules.items():
        r = spark.sql(f'''
            SELECT
              COUNT_IF({col} IS NOT NULL AND try_cast({col} AS DOUBLE) IS NULL) AS non_number,
              COUNT_IF(try_cast({col} AS DOUBLE) NOT BETWEEN {minimum} AND {maximum}) AS out_of_range
            FROM enem_pipeline.bronze.{table}
        ''').first()
        if r.non_number:  errors.append(f"{col}: {r.non_number} valores não numéricos")
        if r.out_of_range: errors.append(f"{col}: {r.out_of_range} fora de [{minimum}, {maximum}]")
    assert not errors, f"{table}:\n" + "\n".join(errors)

# Checagem das qualidade dos dados, usando a função criada
for table in tables_ls.select("tableName").collect():
    if 'participantes' in table.tableName:
        quality_checker(range_participants, table.tableName)
    elif 'resultados' in table.tableName:
        quality_checker(range_results, table.tableName)
    else:
        sum_ranges = range_participants | range_results
        quality_checker(sum_ranges, table.tableName)

    print(f"Checagem de qualidade da tabela {table.tableName} concluída com sucesso!\n")



