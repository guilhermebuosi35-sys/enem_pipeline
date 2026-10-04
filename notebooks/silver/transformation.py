# Bibliotecas importadas
from pathlib import Path

# Caminho do .sql com as criações das tabelas silvers
silver_sql = Path.cwd().parent.parent / "sql" / "silver_tables.sql"

# Execução das criações
with open(silver_sql, "r") as f:
    content = f.read()

statements = content.split(";")

for statement in statements:
    statement = statement.strip()
    if statement:
        spark.sql(statement) 
        print(f"Declaração executada: {statement[0:60]}...")

# Mostra as tabelas silver criadas
display(spark.sql("SHOW TABLES IN enem_pipeline.silver"))