# streamlit_app.py
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

secrets = {
    "dialect": "postgresql",
    "host": "localhost",
    "port": "5432",
    "database": os.getenv("POSTGRES_DB"),
    "username": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
    
}

# Initialize connection.
conn = st.connection("postgresql", type="sql", **secrets)

# Perform query.
df = conn.query('''
    SELECT 
        ano_exame AS Ano,
        ROUND(AVG(nota_redacao), 2) AS Media
    FROM resultados 
    GROUP BY ano_exame
    ORDER BY Media DESC;
    ''', ttl="10m")

# Print results.
st.dataframe(df)