import streamlit as st

welcome_page = st.Page("pages/welcome.py", title="README", icon=":material/info:", default=True)
page_2022 = st.Page("pages/foco_socioeconomico/2022.py", title="2022", icon=":material/looks_two:")
page_2023 = st.Page("pages/foco_socioeconomico/2023.py", title="2023", icon=":material/looks_3:")
page_2024 = st.Page("pages/foco_socioeconomico/2024.py", title="2024", icon=":material/looks_4:")
secundary_page = st.Page("pages/visao_geral.py", title="Comparativo", icon=":material/south_america:")

pg = st.navigation({
    "Bem vindo(a)!": [welcome_page], 
    "Visão Geral": [secundary_page],
    "Foco Socioeconômico": [page_2022, page_2023, page_2024]     
    }
)

pg.run()