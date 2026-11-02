# Bibliotecas importadas
from pathlib import Path
from pyspark.sql import SparkSession

spark_session = SparkSession.builder.getOrCreate()

# Caminho do .sql com as criações das tabelas silvers
silver_sql = Path.cwd().parent.parent / "sql" / "silver_tables.sql"

# Função de execução de um arquivo .sql
def sql_executor(path_sql):
    with open(path_sql, "r") as f:
        content = f.read()

    statements = content.split(";")

    for statement in statements:
        statement = statement.strip()
        if statement:
            spark_session.sql(statement) 
            print(f"Declaração executada: {statement[0:60]}...")

if __name__ == "__main__":
    # Execução das criações
    sql_executor(silver_sql)

    # Mostra as tabelas silver criadas
    display(spark.sql("SHOW TABLES IN enem_pipeline.silver"))