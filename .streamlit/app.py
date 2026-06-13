import streamlit as st

welcome_page = st.Page("welcome.py", title="Bem vindo(a)!", icon=":material/home:", default=True)
main_page = st.Page("main.py", title="Foco Socioeconômico", icon=":material/group:")
secundary_page = st.Page("secundary.py", title="Visão Geral", icon=":material/south_america:")

pg = st.navigation([welcome_page, main_page, secundary_page])

pg.run()