from databricks.sdk import WorkspaceClient
from pathlib import Path

w = WorkspaceClient()

# Confirma a conexão 
user = w.current_user.me()
print(f"Conectado como: {user.user_name}\n")

warehouses = list(w.warehouses.list())
warehouse_id = warehouses[0].id

# Criação do Catálogo para o projeto
w.statement_execution.execute_statement(
    statement="""
    CREATE CATALOG IF NOT EXISTS enem_pipeline
        COMMENT 'Catálogo que contempla os dados referente aos anos de 2022, 2023 e 2024 das provas realizadas pelo vestibular do Enem.'
    """,
    warehouse_id=warehouse_id
)

created_catalog = w.catalogs.get(name="enem_pipeline")
print(f"Catálogo criado: {created_catalog.full_name}\n")

# Criação dos Schemas para o projeto
layers = ["bronze", "silver", "gold"]
created_layers = []

for layer in layers:

    w.statement_execution.execute_statement(
        statement=f"""
        CREATE SCHEMA IF NOT EXISTS enem_pipeline.{layer}
            COMMENT 'Schema {layer} para o projeto enem_pipeline, seguindo a arquitetura Medallion.'
        """,
        warehouse_id=warehouse_id
    )

    created_layers.append(w.schemas.get(full_name=f"{created_catalog.name}.{layer}"))

print(f"Schemas criado com sucesso: {created_layers}\n")

# Criação do volume na camada Bronze
w.statement_execution.execute_statement(
    statement="""
    CREATE VOLUME IF NOT EXISTS enem_pipeline.bronze.raw 
    """,
    warehouse_id=warehouse_id
)

created_volume = w.volumes.read(name=f"{created_catalog.name}.bronze.raw")
print(f"Volume criado com sucesso: Raw\n")

# Função de Upload dos arquivos CSVs
def upload_csv_volume (year, name_csv):

    file_path = f"/Volumes/{created_volume.catalog_name}/{created_volume.schema_name}/{created_volume.name}/{name_csv}"
    source_path = Path(__file__).resolve().parent.parent / 'data' / year / name_csv

    w.files.upload_from(file_path, source_path, overwrite=True)

# Loop de upload dos arquivos
print("Ambiente configurado com sucesso.")

years_collected = ['2022', '2023', '2024']

for year in years_collected:

    print(f"Iniciando Upload do CSV referente ao período de {year}...")

    if year in ['2022', '2023']:
        upload_csv_volume(year=year, name_csv=f'MICRODADOS_ENEM_{year}.csv')
    else:
        upload_csv_volume(year=year, name_csv=f'PARTICIPANTES_{year}.csv')
        upload_csv_volume(year=year, name_csv=f'RESULTADOS_{year}.csv')

print("\nDados carregados com sucesso.")