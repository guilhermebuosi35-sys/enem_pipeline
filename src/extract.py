import requests
from pathlib import Path
import certifi
import zipfile

links = ["https://download.inep.gov.br/microdados/microdados_enem_2024.zip", "https://download.inep.gov.br/microdados/microdados_enem_2023.zip","https://download.inep.gov.br/microdados/microdados_enem_2022.zip"]
cert_path = Path.cwd().parent/ "rnp_cert.pem"
raw_folder_path = Path.cwd().parent / "data" / "raw"

for arquivo in links: 
    resposta = requests.get(arquivo, stream=True, verify=cert_path)
    nome = Path(arquivo).name 
    caminho_zip = raw_folder_path / nome

    raw_folder_path.mkdir(parents=True, exist_ok=True) 

    print (f"Iniciando download do arquivo: '{nome}'...")

    with open (caminho_zip, "wb") as a:
        for parte in resposta.iter_content(chunk_size=8192):
            a.write(parte)

    print (f"\nDownload finalizado com sucesso!")

    print (f"\nRealizando o descomprimento do arquivo: '{nome}' na pasta '{raw_folder_path}'")

    with zipfile.ZipFile(caminho_zip, 'r') as descomprimido:

        inicio = nome.find(".") - 4
        fim = nome.find(".")
        pasta_download = Path(raw_folder_path / nome[inicio:fim])

        pasta_download.mkdir(parents=True, exist_ok=True) 

        pasta_alvo = 'DADOS/'

        for membro in descomprimido.namelist():
            if membro.startswith(pasta_alvo) and not membro.endswith('/'):
                with descomprimido.open(membro) as origem:
                    with open(pasta_download / Path(membro).name, "wb") as destino:
                        destino.write(origem.read())

    print(f"\nDeletendo arquivo {nome} para desocupar armazenamento...")

    caminho_zip.unlink()

    print("\nArquivos extraídos com sucesso!")