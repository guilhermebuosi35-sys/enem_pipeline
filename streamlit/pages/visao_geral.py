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

# Funções de suporte

# -- Formatador de milhares --

def formatar_milhares(valor):
    return f"{valor:,}".replace(",", ".")

# Configurações do layout da página
st.set_page_config(layout="wide")

ano_global = st.pills(
    "Ano de referência",
    options=["2022", "2023", "2024"],
    selection_mode="single",
    default="2022",
    key="ano_global"
)

card1, card2, card3, card4 = st.columns(4)


if ano_global:
    # SESSÃO 1: Cards com Principais métricas
    with card1:
        df_dist_masculino = conn.query(f'''
            SELECT 
                sexo,
                COUNT(*) AS contagem
            FROM silver.vw_participantes_{ano_global}
            WHERE sexo = 'M'
            GROUP BY sexo
        ''')  

        dist_masculino_int = int(df_dist_masculino['contagem'].iloc[0])

        st.metric(label="Masculino", value=formatar_milhares(dist_masculino_int), border=True)
    
    with card2:
        df_dist_feminino = conn.query(f'''
            SELECT 
                sexo,
                COUNT(*) AS contagem
            FROM silver.vw_participantes_{ano_global}
            WHERE sexo = 'F'
            GROUP BY sexo 
        ''')

        dist_feminino_int = int(df_dist_feminino['contagem'].iloc[0])

        st.metric(label="Feminino", border=True, value=formatar_milhares(dist_feminino_int))

    with card3:
        st.metric(label="A decidir", border=True, value="...")

    with card4:
        st.metric(label="A decidir", border=True, value="...")

    st.divider()

    # SESSÃO 2: Distribuição de Renda
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## Distribuição de Renda Familiar")

        materias_dict = {
            "nota_cn": "Ciências da Natureza",
            "nota_ch": "Ciências Humanas",
            "nota_lc": "Linguagens",
            "nota_mt": "Matemática",
            "nota_redacao": "Redação"
        }

        dic_renda = {
            '2022': 'q006',
            '2023': 'q006',
            '2024': 'q007'
        }

        quest_renda = dic_renda[ano_global]

        with st.spinner("Agregando dados de renda..."):
            df_dist_rend = conn.query(
                f'''
                SELECT 
                    {quest_renda} AS codigo_renda,
                    COUNT(*) AS total_candidatos
                FROM silver.vw_participantes_{ano_global}
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

    # SESSÃO 3: Distribuição de Notas
    with col2:
        st.markdown("## Distribuição de Notas Através dos Anos")
            
        with st.spinner("Carregando amostra e processando quartis..."):
            df_media_nota = conn.query(f'''
                SELECT
                    ano_exame,
                    nota_cn, 
                    nota_ch,
                    nota_lc,
                    nota_mt, 
                    nota_redacao  
                FROM silver.vw_resultados_{ano_global}
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

    # SESSÃO 4: Distribuição de Notas por Região
    st.markdown("## Distribuição de Notas por Região")

    materia_selecionada = st.pills(
        "Matéria da Prova",
        options=materias_dict.values(),
        selection_mode='single',
        default='Ciências da Natureza',
        key='selection_materia'
    )

    with urlopen("https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson") as response:
        brasil_geojson = json.load(response)

    mat_query = [k for k,v in materias_dict.items() if v == materia_selecionada]

    df_media_regiao = conn.query (f'''
        SELECT 
            uf_prova,
            ROUND(AVG({mat_query[0]}), 2) AS media 
        FROM silver.vw_resultados_{ano_global}                 
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