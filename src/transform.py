# %% [markdown]
# # Importações

# %%
import pandas as pd
from pathlib import Path

pd.set_option('display.max_columns', None)

# %% [markdown]
# # Definindo localização do dataset "resultados_2024"

# %%
loc_resultados_2024 = Path.cwd().parent / 'data' / 'raw' / '2024' / 'RESULTADOS_2024.csv'

df_resultados_2024_raw = pd.read_csv(loc_resultados_2024, encoding="latin-1", sep=";")

# %% [markdown]
# ### Renomeando as colunas do dataset

# %%
columns = {
    'NU_SEQUENCIAL': 'id_linha', 
    'NU_ANO': 'ano_exame', 
    'CO_MUNICIPIO_ESC': 'id_municipio_escola', 
    'CO_UF_ESC': 'id_uf_escola', 
    'TP_DEPENDENCIA_ADM_ESC': 'dependencia_adm_escola',
    'TP_LOCALIZACAO_ESC': 'localizacao_escola',
    'TP_SIT_FUNC_ESC': 'situacao_func_escola',
    'CO_MUNICIPIO_PROVA': 'id_municipio_prova', 
    'CO_UF_PROVA': 'id_uf_prova',
    'TP_PRESENCA_CN': 'presenca_cn',
    'TP_PRESENCA_CH': 'presenca_ch',
    'TP_PRESENCA_LC': 'presenca_lc',
    'TP_PRESENCA_MT': 'presenca_mt',
    'NU_NOTA_CN': 'nota_cn',
    'NU_NOTA_CH': 'nota_ch',
    'NU_NOTA_LC': 'nota_lc',
    'NU_NOTA_MT': 'nota_mt',
    'NU_NOTA_REDACAO': 'nota_redacao',
    'NU_NOTA_COMP1': 'nota_complementar1', 
    'NU_NOTA_COMP2': 'nota_complementar2',
    'NU_NOTA_COMP3': 'nota_complementar3',
    'NU_NOTA_COMP4': 'nota_complementar4',
    'NU_NOTA_COMP5': 'nota_complementar5',
    'TP_STATUS_REDACAO': 'situacao_redacao'
}

df_resultados_2024 = df_resultados_2024_raw[list(columns.keys())].rename(columns=columns)

# %% [markdown]
# ### Formatando colunas Floats como Int

# %%
colunas_type = ['id_municipio_escola', 'id_uf_escola', 'dependencia_adm_escola', 'localizacao_escola', 'situacao_func_escola', 'id_municipio_prova', 'situacao_redacao']


for col in colunas_type:
    df_resultados_2024[col] = df_resultados_2024[col].astype('Int64')

# %% [markdown]
# ### Garantindo que as colunas seguem as regras do dicionário dos dados

# %%
columns_range = {
    'dependencia_adm_escola': [1, 4],
    'localizacao_escola': [1, 2],
    'situacao_func_escola': [1, 4],
    'presenca_cn': [0, 3],
    'presenca_ch': [0, 3],
    'presenca_lc': [0, 3],
    'presenca_mt': [0, 3],
    'nota_cn': [0, 1000],
    'nota_ch': [0, 1000],
    'nota_lc': [0, 1000],
    'nota_mt': [0, 1000],
    'situacao_redacao': [1, 9]
} 

for col, limites in columns_range.items():
    assert df_resultados_2024[col].dropna().between(limites[0], limites[1]).all(), f"Erro: {col} deve constar entre {limites[0]} e {limites[1]}"

# %% [markdown]
# ### Criando um arquivo CSV com base no DataFrame dentro da pasta de dados processados

# %%
loc_resultados_2024_processed = Path.cwd().parent / 'data' / 'processed' / '2024'

loc_resultados_2024_processed.mkdir(parents=True, exist_ok=True)

df_resultados_2024.to_csv(loc_resultados_2024_processed / 'resultados_2024_processed.csv', index=False)

# %% [markdown]
# # Definindo localização do dataset "participantes_2024"

# %%
loc_participantes_2024 = Path.cwd().parent / 'data' / 'raw' / '2024' / 'PARTICIPANTES_2024.csv'

df_participantes_2024_raw = pd.read_csv(loc_participantes_2024, encoding="latin-1", sep=";")

# %% [markdown]
# ### Renomeando as colunas

# %%
columns = {
    'NU_INSCRICAO': 'id_inscricao',
    'NU_ANO': 'ano_exame',
    'TP_FAIXA_ETARIA': 'faixa_etaria',
    'TP_SEXO': 'sexo',
    'TP_ESTADO_CIVIL': 'estado_civil',
    'TP_COR_RACA': 'cor_raca',
    'TP_NACIONALIDADE': 'nacionalidade',
    'TP_ST_CONCLUSAO': 'st_conclusao',
    'TP_ANO_CONCLUIU': 'ano_conclusao',
    'TP_ENSINO': 'ensino',
    'IN_TREINEIRO': 'treineiro',
    'CO_MUNICIPIO_PROVA': 'municipio_prova',
    'CO_UF_PROVA': 'id_uf_prova',
    'Q001': 'questionario_q1',	
    'Q002': 'questionario_q2',	
    'Q003': 'questionario_q3',	
    'Q004': 'questionario_q4',	
    'Q005': 'questionario_q5',	
    'Q006': 'questionario_q6',	
    'Q007': 'questionario_q7',		
    'Q008': 'questionario_q8',		
    'Q009': 'questionario_q9',		
    'Q010': 'questionario_q10',		
    'Q011': 'questionario_q11',		
    'Q012': 'questionario_q12',		
    'Q013': 'questionario_q13',	
    'Q014': 'questionario_q14',	
    'Q015': 'questionario_q15',		
    'Q016': 'questionario_q16',		
    'Q017': 'questionario_q17',	
    'Q018': 'questionario_q18',		
    'Q019': 'questionario_q19',		
    'Q020': 'questionario_q20',		
    'Q021': 'questionario_q21',		
    'Q022': 'questionario_q22',		
    'Q023': 'questionario_q23'	
}

df_participantes_2024 = df_participantes_2024_raw[list(columns.keys())].rename(columns=columns) 

# %% [markdown]
# ### Formatando valores de Float para Int

# %%
df_participantes_2024['ensino'] = df_participantes_2024['ensino'].astype('Int64')

# %% [markdown]
# ### Garantindo que as colunas seguem as regras do dicionário dos dados

# %%
columns_range = {
    'faixa_etaria': [1, 20],
    'faixa_etaria': [1, 20],
    'sexo': ['F', 'M'],
    'estado_civil': [0, 4],
    'cor_raca': [0, 6],
    'nacionalidade': [0, 4],
    'st_conclusao': [1, 4],
    'ano_conclusao': [0, 18],
    'ensino': [1, 2],
    'treineiro': [0, 1]
}

for col, limites in columns_range.items():
    assert df_participantes_2024[col].dropna().between(limites[0], limites[1]).all(), f"Erro: {col} deve constar entre os códigos {limites[0]} e {limites[1]}"

# %% [markdown]
# ### Criando um arquivo CSV com base no DataFrame dentro da pasta de dados processados

# %%
loc_participantes_2024_processed = Path.cwd().parent / 'data' / 'processed' / '2024'

loc_participantes_2024_processed.mkdir(parents=True, exist_ok=True)

df_participantes_2024.to_csv(loc_participantes_2024_processed / 'participantes_2024_processed.csv', index=False)

# %% [markdown]
# # Definindo localização do dataset "microdados_enem_2023"

# %%
loc_microdados_2023 = Path.cwd().parent / 'data' / 'raw' / '2023' / 'MICRODADOS_ENEM_2023.csv'

df_microdados_2023_raw = pd.read_csv(loc_microdados_2023, encoding="latin-1", sep=";")

# %% [markdown]
# # Renomeando as colunas, e criando dataset de resultados_2023

# %%
columns = {
    'NU_INSCRICAO': 'id_inscricao', 
    'NU_ANO': 'ano_exame', 
    'CO_MUNICIPIO_ESC': 'id_municipio_escola', 
    'CO_UF_ESC': 'id_uf_escola', 
    'TP_DEPENDENCIA_ADM_ESC': 'dependencia_adm_escola',
    'TP_LOCALIZACAO_ESC': 'localizacao_escola',
    'TP_SIT_FUNC_ESC': 'situacao_func_escola',
    'CO_MUNICIPIO_PROVA': 'id_municipio_prova', 
    'CO_UF_PROVA': 'id_uf_prova',
    'TP_PRESENCA_CN': 'presenca_cn',
    'TP_PRESENCA_CH': 'presenca_ch',
    'TP_PRESENCA_LC': 'presenca_lc',
    'TP_PRESENCA_MT': 'presenca_mt',
    'NU_NOTA_CN': 'nota_cn',
    'NU_NOTA_CH': 'nota_ch',
    'NU_NOTA_LC': 'nota_lc',
    'NU_NOTA_MT': 'nota_mt',
    'NU_NOTA_REDACAO': 'nota_redacao',
    'NU_NOTA_COMP1': 'nota_complementar1', 
    'NU_NOTA_COMP2': 'nota_complementar2',
    'NU_NOTA_COMP3': 'nota_complementar3',
    'NU_NOTA_COMP4': 'nota_complementar4',
    'NU_NOTA_COMP5': 'nota_complementar5',
    'TP_STATUS_REDACAO': 'situacao_redacao'
}


df_resultados_2023 = df_microdados_2023_raw[list(columns.keys())].rename(columns=columns)

# %% [markdown]
# ### Formatando valores de Float para Int

# %%
colunas_type = ['id_municipio_escola', 'id_uf_escola', 'dependencia_adm_escola', 'localizacao_escola', 'situacao_func_escola', 'situacao_redacao']


for col in colunas_type:
    df_resultados_2023[col] = df_resultados_2023[col].astype('Int64')

# %% [markdown]
# ### Garantindo que as colunas seguem as regras do dicionário dos dados

# %%
columns_range = {
    'dependencia_adm_escola': [1, 4],
    'localizacao_escola': [1, 2],
    'situacao_func_escola': [1, 4],
    'presenca_cn': [0, 3],
    'presenca_ch': [0, 3],
    'presenca_lc': [0, 3],
    'presenca_mt': [0, 3],
    'nota_cn': [0, 1000],
    'nota_ch': [0, 1000],
    'nota_lc': [0, 1000],
    'nota_mt': [0, 1000],
    'situacao_redacao': [1, 9]
} 

for col, limites in columns_range.items():
    assert df_resultados_2023[col].dropna().between(limites[0], limites[1]).all(), f"Erro: {col} deve constar entre {limites[0]} e {limites[1]}"

# %% [markdown]
# ### Criando um arquivo CSV com base no DataFrame dentro da pasta de dados processados

# %%
loc_resultados_2023_processed = Path.cwd().parent / 'data' / 'processed' / '2023'

loc_resultados_2023_processed.mkdir(parents=True, exist_ok=True)

df_resultados_2023.to_csv(loc_resultados_2023_processed / 'resultados_2023_processed.csv', index=False)

# %% [markdown]
# # Renomeando as colunas, e criando dataset de participantes_2023

# %%
columns = {
    'NU_INSCRICAO': 'id_inscricao',
    'NU_ANO': 'ano_exame',
    'TP_FAIXA_ETARIA': 'faixa_etaria',
    'TP_SEXO': 'sexo',
    'TP_ESTADO_CIVIL': 'estado_civil',
    'TP_COR_RACA': 'cor_raca',
    'TP_NACIONALIDADE': 'nacionalidade',
    'TP_ST_CONCLUSAO': 'st_conclusao',
    'TP_ANO_CONCLUIU': 'ano_conclusao',
    'TP_ENSINO': 'ensino',
    'IN_TREINEIRO': 'treineiro',
    'CO_MUNICIPIO_PROVA': 'municipio_prova',
    'CO_UF_PROVA': 'id_uf_prova',
    'Q001': 'questionario_q1',	
    'Q002': 'questionario_q2',	
    'Q003': 'questionario_q3',	
    'Q004': 'questionario_q4',	
    'Q005': 'questionario_q5',	
    'Q006': 'questionario_q6',	
    'Q007': 'questionario_q7',		
    'Q008': 'questionario_q8',		
    'Q009': 'questionario_q9',		
    'Q010': 'questionario_q10',		
    'Q011': 'questionario_q11',		
    'Q012': 'questionario_q12',		
    'Q013': 'questionario_q13',	
    'Q014': 'questionario_q14',	
    'Q015': 'questionario_q15',		
    'Q016': 'questionario_q16',		
    'Q017': 'questionario_q17',	
    'Q018': 'questionario_q18',		
    'Q019': 'questionario_q19',		
    'Q020': 'questionario_q20',		
    'Q021': 'questionario_q21',		
    'Q022': 'questionario_q22',		
    'Q023': 'questionario_q23'	
}

df_participantes_2023 = df_microdados_2023_raw[list(columns.keys())].rename(columns=columns)

# %% [markdown]
# ### Formatando valores de Float para Int

# %%
df_participantes_2023['ensino'] = df_participantes_2023['ensino'].astype('Int64')

# %% [markdown]
# ### Garantindo que as colunas seguem as regras do dicionário dos dados

# %%
columns_range = {
    'faixa_etaria': [1, 20],
    'faixa_etaria': [1, 20],
    'sexo': ['F', 'M'],
    'estado_civil': [0, 4],
    'cor_raca': [0, 6],
    'nacionalidade': [0, 4],
    'st_conclusao': [1, 4],
    'ano_conclusao': [0, 18],
    'ensino': [1, 2],
    'treineiro': [0, 1]
}

for col, limites in columns_range.items():
    assert df_participantes_2023[col].dropna().between(limites[0], limites[1]).all(), f"Erro: {col} deve constar entre os códigos {limites[0]} e {limites[1]}"

# %% [markdown]
# ### Criando um arquivo CSV com base no DataFrame dentro da pasta de dados processados

# %%
loc_participantes_2023_processed = Path.cwd().parent / 'data' / 'processed' / '2023'

loc_participantes_2023_processed.mkdir(parents=True, exist_ok=True)

df_participantes_2023.to_csv(loc_participantes_2023_processed / 'participantes_2023_processed.csv', index=False)

# %% [markdown]
# # Definindo localização do dataset "microdados_enem_2022"

# %%
loc_microdados_2022 = Path.cwd().parent / 'data' / 'raw' / '2022' / 'MICRODADOS_ENEM_2022.csv'

df_microdados_2022_raw = pd.read_csv(loc_microdados_2022, encoding="latin-1", sep=";")

# %% [markdown]
# # Renomeando as colunas, e criando dataset de resultados_2022

# %%
columns = {
    'NU_INSCRICAO': 'id_inscricao', 
    'NU_ANO': 'ano_exame', 
    'CO_MUNICIPIO_ESC': 'id_municipio_escola', 
    'CO_UF_ESC': 'id_uf_escola', 
    'TP_DEPENDENCIA_ADM_ESC': 'dependencia_adm_escola',
    'TP_LOCALIZACAO_ESC': 'localizacao_escola',
    'TP_SIT_FUNC_ESC': 'situacao_func_escola',
    'CO_MUNICIPIO_PROVA': 'id_municipio_prova', 
    'CO_UF_PROVA': 'id_uf_prova',
    'TP_PRESENCA_CN': 'presenca_cn',
    'TP_PRESENCA_CH': 'presenca_ch',
    'TP_PRESENCA_LC': 'presenca_lc',
    'TP_PRESENCA_MT': 'presenca_mt',
    'NU_NOTA_CN': 'nota_cn',
    'NU_NOTA_CH': 'nota_ch',
    'NU_NOTA_LC': 'nota_lc',
    'NU_NOTA_MT': 'nota_mt',
    'NU_NOTA_REDACAO': 'nota_redacao',
    'NU_NOTA_COMP1': 'nota_complementar1', 
    'NU_NOTA_COMP2': 'nota_complementar2',
    'NU_NOTA_COMP3': 'nota_complementar3',
    'NU_NOTA_COMP4': 'nota_complementar4',
    'NU_NOTA_COMP5': 'nota_complementar5',
    'TP_STATUS_REDACAO': 'situacao_redacao'
}


df_resultados_2022 = df_microdados_2022_raw[list(columns.keys())].rename(columns=columns)

# %% [markdown]
# ### Formatando valores de Float para Int

# %%
colunas_type = ['id_municipio_escola', 'id_uf_escola', 'dependencia_adm_escola', 'localizacao_escola', 'situacao_func_escola', 'situacao_redacao']


for col in colunas_type:
    df_resultados_2022[col] = df_resultados_2022[col].astype('Int64')

# %% [markdown]
# ### Garantindo que as colunas seguem as regras do dicionário de dados

# %%
columns_range = {
    'dependencia_adm_escola': [1, 4],
    'localizacao_escola': [1, 2],
    'situacao_func_escola': [1, 4],
    'presenca_cn': [0, 3],
    'presenca_ch': [0, 3],
    'presenca_lc': [0, 3],
    'presenca_mt': [0, 3],
    'nota_cn': [0, 1000],
    'nota_ch': [0, 1000],
    'nota_lc': [0, 1000],
    'nota_mt': [0, 1000],
    'situacao_redacao': [1, 9]
} 

for col, limites in columns_range.items():
    assert df_resultados_2022[col].dropna().between(limites[0], limites[1]).all(), f"Erro: {col} deve constar entre {limites[0]} e {limites[1]}"

# %% [markdown]
# ### Criando um arquivo CSV com base no DataFrame dentro da pasta de dados processados

# %%
loc_resultados_2022_processed = Path.cwd().parent / 'data' / 'processed' / '2022'

loc_resultados_2022_processed.mkdir(parents=True, exist_ok=True)

df_resultados_2022.to_csv(loc_resultados_2022_processed / 'resultados_2022_processed.csv', index=False)

# %% [markdown]
# # Renomeando as colunas, e criando dataset de participantes_2022

# %%
columns = {
    'NU_INSCRICAO': 'id_inscricao',
    'NU_ANO': 'ano_exame',
    'TP_FAIXA_ETARIA': 'faixa_etaria',
    'TP_SEXO': 'sexo',
    'TP_ESTADO_CIVIL': 'estado_civil',
    'TP_COR_RACA': 'cor_raca',
    'TP_NACIONALIDADE': 'nacionalidade',
    'TP_ST_CONCLUSAO': 'st_conclusao',
    'TP_ANO_CONCLUIU': 'ano_conclusao',
    'TP_ENSINO': 'ensino',
    'IN_TREINEIRO': 'treineiro',
    'CO_MUNICIPIO_PROVA': 'municipio_prova',
    'CO_UF_PROVA': 'id_uf_prova',
    'Q001': 'questionario_q1',	
    'Q002': 'questionario_q2',	
    'Q003': 'questionario_q3',	
    'Q004': 'questionario_q4',	
    'Q005': 'questionario_q5',	
    'Q006': 'questionario_q6',	
    'Q007': 'questionario_q7',		
    'Q008': 'questionario_q8',		
    'Q009': 'questionario_q9',		
    'Q010': 'questionario_q10',		
    'Q011': 'questionario_q11',		
    'Q012': 'questionario_q12',		
    'Q013': 'questionario_q13',	
    'Q014': 'questionario_q14',	
    'Q015': 'questionario_q15',		
    'Q016': 'questionario_q16',		
    'Q017': 'questionario_q17',	
    'Q018': 'questionario_q18',		
    'Q019': 'questionario_q19',		
    'Q020': 'questionario_q20',		
    'Q021': 'questionario_q21',		
    'Q022': 'questionario_q22',		
    'Q023': 'questionario_q23'	
}

df_participantes_2022 = df_microdados_2022_raw[list(columns.keys())].rename(columns=columns)

# %% [markdown]
# ### Formatando os valores de Float para Int

# %%
df_participantes_2022['ensino'] = df_participantes_2022['ensino'].astype('Int64')

# %% [markdown]
# ### Garantindo que as colunas seguem as regras do dicionário dos dados

# %%
columns_range = {
    'faixa_etaria': [1, 20],
    'faixa_etaria': [1, 20],
    'sexo': ['F', 'M'],
    'estado_civil': [0, 4],
    'cor_raca': [0, 6],
    'nacionalidade': [0, 4],
    'st_conclusao': [1, 4],
    'ano_conclusao': [0, 18],
    'ensino': [1, 2],
    'treineiro': [0, 1]
}

for col, limites in columns_range.items():
    assert df_participantes_2022[col].dropna().between(limites[0], limites[1]).all(), f"Erro: {col} deve constar entre os códigos {limites[0]} e {limites[1]}"

# %% [markdown]
# ### Criando um arquivo CSV com base no DataFrame dentro da pasta de dados processados

# %%
loc_participantes_2022_processed = Path.cwd().parent / 'data' / 'processed' / '2022'

loc_participantes_2022_processed.mkdir(parents=True, exist_ok=True)

df_participantes_2022.to_csv(loc_participantes_2022_processed / 'participantes_2022_processed.csv', index=False)


