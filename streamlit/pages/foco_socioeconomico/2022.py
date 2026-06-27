import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, URL, text
from dotenv import load_dotenv
from mapeamentos import *
import plotly.express as px

load_dotenv()

# Setup do Banco de Dados
secrets = {
    "dialect": "postgresql",
    "host": "localhost",
    "port": "5432",
    "database": os.getenv("POSTGRES_DB"),
    "username": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
    
}

# Inicia conexão com streamlit
conn = st.connection("postgresql", type="sql", **secrets)

# Ánalise de desempenho x Renda Familiar
df_nt_renda_familiar = conn.query(
    '''
    SELECT *
    FROM gold.vw_renda;
    '''
)

df_nt_renda_familiar['quest_6'] = df_nt_renda_familiar['quest_6'].map(questionario_q7)

st.dataframe(df_nt_renda_familiar)

# Ánalise de desempenho x cor/raça
df_nt_cor = conn.query(
    '''
    SELECT *
    FROM gold.vw_cor_raca;
    '''
) 

df_nt_cor['cor_raca'] = df_nt_cor['cor_raca'].map(cor_raca)

st.dataframe(df_nt_cor)

# Ánalise de desempenho x escola frequentada no ensino médio
df_nt_escola = conn.query(
    '''
    SELECT *
    FROM gold.vw_dep_escola;
    '''
)

df_nt_escola['escola'] = df_nt_escola['escola'].map(escola_ens_medio)

st.dataframe(df_nt_escola)

# Ánalise de desempenho x série máxima frequentada pelos pais

categoria_selecionada = st.selectbox("Filtro de pai ou mãe", ("Mãe", "Pai"), placeholder="Selecione", index=None)


if categoria_selecionada is not None:
    st.dataframe()

elif categoria_selecionada == "Pai":

    df_nt_pai_escolaridade = conn.query(
        '''
        SELECT *
        FROM gold.vw_pai_escolaridade;
        '''
    )

    df_nt_pai_escolaridade['serie_pai'] = df_nt_pai_escolaridade['serie_pai'].map(questionario_q1)

    st.dataframe(df_nt_pai_escolaridade)

else:

    df_nt_mae_escolaridade = conn.query(
        '''
        SELECT *
        FROM gold.vw_mae_escolaridade;
        '''
    )

    df_nt_mae_escolaridade['serie_mae'] = df_nt_mae_escolaridade['serie_mae'].map(questionario_q1)

    st.dataframe(df_nt_mae_escolaridade)