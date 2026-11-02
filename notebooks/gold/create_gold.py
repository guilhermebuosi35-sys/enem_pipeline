# Bibliotecas importadas
import sys
from pathlib import Path

# Importando função que executa SQL
sql_exec_function = Path.cwd().parent / "silver" 
sys.path.append(str(sql_exec_function))

from create_silver import sql_executor

# Caminho do .sql com as criações das tabelas golds
gold_sql = Path.cwd().parent.parent / "sql" / "gold_tables.sql"

# Executando as criações das tabelas golds
if __name__ == "__main__":
    sql_executor(gold_sql)