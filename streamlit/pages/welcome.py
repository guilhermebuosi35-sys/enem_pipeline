import streamlit as st
import pandas as pd
from databricks import sql

# Setup do workspace do Databricks
@st.cache_resource
def get_databricks_connection():
    return sql.connect(
        server_hostname=st.secrets["databricks"]["server_hostname"],
        http_path=st.secrets["databricks"]["http_path"],
        access_token=st.secrets["databricks"]["access_token"]
    )

# Função para buscar dados do Databricks com cache de 10 minutos
@st.cache_data(ttl=600)
def fetch_data(query):
    connection = get_databricks_connection()
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall_arrow().to_pandas()
    return result


st.title("Pipeline ENEM")

query_string = "SELECT * FROM enem_pipeline.silver.resultados LIMIT 10"

try:
    with st.spinner("Fetching data from Databricks..."):
        df = fetch_data(query_string)
    
    st.success("Successfully pulled data!")
    st.dataframe(df)

except Exception as e:
    st.error(f"An error occurred: {e}")