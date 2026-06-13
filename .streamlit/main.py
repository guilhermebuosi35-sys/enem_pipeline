import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from mapeamentos import questionario_q7, questionario_q23, cor_raca

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

# Inicia conexão
conn = st.connection("postgresql", type="sql", **secrets)

# Ánalise de desempenho x Renda Familiar
df_nt_renda_familiar = conn.query(
    '''
    WITH tb_renda AS ( 
        SELECT
            r.id_inscricao, 
            r.nota_cn AS nota_cn,
            r.nota_ch AS nota_ch,
            r.nota_lc AS nota_lc,
            r.nota_mt AS nota_mt,
            r.nota_redacao AS nota_redacao,
            p.questionario_q7 AS quest_7
        FROM participantes AS p
        INNER JOIN resultados AS r
            ON p.id_inscricao = r.id_inscricao
    )
    SELECT 
        quest_7,
        ROUND(AVG(nota_cn), 2) AS media_cn,
        ROUND(AVG(nota_ch), 2) AS media_ch,
        ROUND(AVG(nota_lc), 2) AS media_lc,
        ROUND(AVG(nota_mt), 2) AS media_mt,
        ROUND(AVG(nota_redacao), 2) AS media_redacao
    FROM tb_renda
    GROUP BY quest_7
    ORDER BY quest_7;
    '''
)

df_nt_renda_familiar['quest_7'] = df_nt_renda_familiar['quest_7'].map(questionario_q7)

st.dataframe(df_nt_renda_familiar)

# Ánalise de desempenho x cor/raça

df_nt_cor = conn.query(
    '''
    WITH tb_cor AS ( 
        SELECT
            r.id_inscricao, 
            r.nota_cn AS nota_cn,
            r.nota_ch AS nota_ch,
            r.nota_lc AS nota_lc,
            r.nota_mt AS nota_mt,
            r.nota_redacao AS nota_redacao,
            p.cor_raca AS cor_raca
        FROM participantes AS p
        INNER JOIN resultados AS r
            ON p.id_inscricao = r.id_inscricao
    )
    SELECT 
        cor_raca,
        ROUND(AVG(nota_cn), 2) AS media_cn,
        ROUND(AVG(nota_ch), 2) AS media_ch,
        ROUND(AVG(nota_lc), 2) AS media_lc,
        ROUND(AVG(nota_mt), 2) AS media_mt,
        ROUND(AVG(nota_redacao), 2) AS media_redacao
    FROM tb_cor
    GROUP BY cor_raca
    ORDER BY cor_raca;
    '''
) 

df_nt_cor['cor_raca'] = df_nt_cor['cor_raca'].map(cor_raca)

st.dataframe(df_nt_cor)

# Ánalise de desempenho x escola frequentada no ensino médio

df_nt_escola = conn.query(
    '''
    WITH tb_escola AS ( 
        SELECT
            r.id_inscricao, 
            r.nota_cn AS nota_cn,
            r.nota_ch AS nota_ch,
            r.nota_lc AS nota_lc,
            r.nota_mt AS nota_mt,
            r.nota_redacao AS nota_redacao,
            p.questionario_q23 AS quest_23
        FROM participantes AS p
        INNER JOIN resultados AS r
            ON p.id_inscricao = r.id_inscricao
    )
    SELECT 
        quest_23,
        ROUND(AVG(nota_cn), 2) AS media_cn,
        ROUND(AVG(nota_ch), 2) AS media_ch,
        ROUND(AVG(nota_lc), 2) AS media_lc,
        ROUND(AVG(nota_mt), 2) AS media_mt,
        ROUND(AVG(nota_redacao), 2) AS media_redacao
    FROM tb_escola
    GROUP BY quest_23
    ORDER BY quest_23;
    '''
)

df_nt_escola['quest_23'] = df_nt_escola['quest_23'].map(questionario_q23)


st.dataframe(df_nt_escola)