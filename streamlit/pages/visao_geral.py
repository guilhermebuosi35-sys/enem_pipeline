import os
import streamlit as st
from dotenv import load_dotenv
import plotly.express as px
from mapeamentos import *

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

# Inicializa conexão via cache do Streamlit
conn = st.connection("postgresql", type="sql", **secrets)

# SESSÃO 1: Distribuição de Renda
st.markdown("## Distribuição de Renda Familiar")

option_map = ["2022", "2023", "2024"]

ano_renda = st.pills(
    "Ano de referência (Renda)",
    options=option_map,
    selection_mode="single",
    default="2022",
    key="pill_renda"
)

if ano_renda:
    dic_renda = {
        '2022': 'q006',
        '2023': 'q006',
        '2024': 'q007'
    }

    quest_renda = dic_renda[ano_renda]

    with st.spinner("Agregando dados de renda..."):
        df_dist_rend = conn.query(
            f'''
            SELECT 
                {quest_renda} AS codigo_renda,
                COUNT(*) AS total_candidatos
            FROM silver.vw_participantes_{ano_renda}
            WHERE {quest_renda} IS NOT NULL
            GROUP BY {quest_renda}
            ORDER BY {quest_renda};
            '''
        )

        df_dist_rend['faixa_renda'] = df_dist_rend['codigo_renda'].map(histo_renda)

        fig_dis_renda = px.bar(
            df_dist_rend, 
            x="faixa_renda", 
            y="total_candidatos",
            labels={"faixa_renda": "Renda Familiar", "total_candidatos": "Número de Candidatos"}
        )

    st.plotly_chart(fig_dis_renda, use_container_width=True)

st.divider()

# SESSÃO 2: Distribuição de Notas
st.markdown("## Distribuição de Notas Através dos Anos")

ano_media_nota = st.pills(
    "Ano de referência (Notas)",
    options=option_map,
    selection_mode="single",
    default="2022",
    key="selection_media"
)

if ano_media_nota:
    
    with st.spinner("Carregando amostra e processando quartis..."):
        df_media_nota = conn.query(f'''
            SELECT
                ano_exame,
                nota_cn, 
                nota_ch,
                nota_lc,
                nota_mt, 
                nota_redacao  
            FROM silver.vw_resultados_{ano_media_nota}
            LIMIT 75000
            '''
        )

        df_media_nota_rn = df_media_nota.rename(columns={
            "nota_cn": "Ciências da Natureza",
            "nota_ch": "Ciências Humanas",
            "nota_lc": "Linguagens",
            "nota_mt": "Matemática",
            "nota_redacao": "Redação"
        })

        fig_media_nota = px.box(
            df_media_nota_rn, 
            y=["Ciências da Natureza", "Ciências Humanas", "Linguagens", "Matemática", "Redação"],
            labels={
                "variable": "Área de Conhecimento",
                "value": "Pontuação"
            }
        )
        
        fig_media_nota.update_layout(showlegend=False)

    st.plotly_chart(fig_media_nota, use_container_width=True)