import os
import streamlit as st
from dotenv import load_dotenv
import plotly.express as px
from mapeamentos import *
import json
from urllib.request import urlopen

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
materias_dict = {
    "nota_cn": "Ciências da Natureza",
    "nota_ch": "Ciências Humanas",
    "nota_lc": "Linguagens",
    "nota_mt": "Matemática",
    "nota_redacao": "Redação"
}

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

        df_media_nota_rn = df_media_nota.rename(columns=materias_dict)

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

# SESSÃO 2: Distribuição de Notas por Região
st.markdown("## Distribuição de Notas por Região")

ano_media_regiao = st.pills(
    "Ano de referência (Região)",
    options=option_map,
    selection_mode="single",
    default="2022",
    key="selection_regiao"
)

materia_selecionada = st.pills(
    "Matéria da Prova",
    options=materias_dict.values(),
    selection_mode='single',
    default='Ciências da Natureza',
    key='selection_materia'
)

if ano_media_regiao:

    with urlopen("https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson") as response:
        brasil_geojson = json.load(response)

    mat_query = [k for k,v in materias_dict.items() if v == materia_selecionada]

    df_media_regiao = conn.query (f'''
        SELECT 
            uf_prova,
            ROUND(AVG({mat_query[0]}), 2) AS media 
        FROM silver.vw_resultados_{ano_media_regiao}                 
        GROUP BY uf_prova 
        ORDER BY media DESC
    ''')

    tab1, tab2 = st.tabs(["Gŕafico", "Tabela"])

    fig = px.choropleth_map(
        data_frame=df_media_regiao,
        geojson=brasil_geojson,
        locations='uf_prova',
        featureidkey='properties.sigla',
        center = {"lat": -14.235004, "lon": -51.92528},
        color='media',
        labels={'media': 'Média'},
        zoom=3,
        color_continuous_scale='blues' 
    )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    with tab1:
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        st.dataframe({'UF': df_media_regiao['uf_prova'], 'Média': df_media_regiao['media']})