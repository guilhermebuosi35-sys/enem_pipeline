import requests
from pathlib import Path
import certifi

links = ["https://download.inep.gov.br/microdados/microdados_enem_2024.zip", "https://download.inep.gov.br/microdados/microdados_enem_2023.zip","https://download.inep.gov.br/microdados/microdados_enem_2022.zip"]
 
for arquivo in links: 
    resposta = requests.get(arquivo, stream=True, verify="/Users/macbook/enem_pipeline/rnp_cert.pem")
    nome = Path(arquivo).name
    pasta = Path("/Users/macbook/enem_pipeline/data/raw")

    pasta.mkdir(parents=True, exist_ok=True) 

    with open (pasta / nome, "wb") as file:
        for chunk in resposta.iter_content(chunk_size=8192):
            file.write(chunk)