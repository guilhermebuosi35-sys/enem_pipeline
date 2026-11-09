# enem_pipeline

## Requisitos

- Python >= 3.10

### É necessário baixar o certificado da RNP antes de rodar o extract.py

Instalar o certificado para conseguir realizar o download a partir do site da INEP

Rode os seguintes comandos no PowerShell

**Passo 1:**
*Verifica o certificado que a INEP está utilizando*

```
openssl s_client -connect download.inep.gov.br:443 -showcerts 2>$null | openssl x509 -out <caminho-do-seu-projeto>/rnp_cert.pem
```

- Use `2>$null` para o PowerShell
- Ou `2>/dev/null` para Git Bash

## Setup

### Realizando o download das dependências

1. Cria o ambiente python dentro do diretório clonado: `python -m venv .venv`
2. Ative o ambiente antes de qualquer download
    - Linux/MacOS: `source  .venv/bin/activate`
    - Powershell: `.venv\Scripts\Activate.ps1`
3. Instale as depêndencias com `pip install -r requirements.txt`

### Como configurar o ambiente no docker

1. Antes de tudo, crie o seu .env com base na estrutura dada em .env.example
2. Garanta que você possui o Docker instalado no seu ambiente com `docker -v`
3. Rode `docker-compose up -d db` para subir o container referente ao banco de dados
4. Após isso, rode `docker compose ps` para verificar o status


## Databricks

### Set Up

1. Realize a instalação da depêndencia da API do Databricks 

`pip3 install databricks-sdk`

2. Instale o Databricks CLI

    a. Rode `databricks auth login --host <seu-workspace-url> --account-id <seu-account-id>`
    b. Isso cria/atualiza o `~/.databrickscfg` local. Não precisa configurar nada dentro do projeto

3. Com a credencial configurada, Importe a biblioteca

`from databricks.sdk import WorkspaceClient`

`w = WorkspaceClient()`

### Streamlit <> Databricks

Para executar a conexão entre o streamlit e o seu workspace, você precisa iniciar configurando o arquivo .streamlit/secrets.toml com as seguintes variáveis de conexão:

```
# .streamlit/secrets.toml

[databricks]
server_hostname = "SEU_DATABRICKS_SERVER_HOSTNAME"
http_path = "SEU_DATABRICKS_HTTP_PATH"
access_token = "SEU_DATABRICKS_PERSONAL_ACCESS_TOKEN"
```

**Como encontra-los no databricks** 

1. server_hostname e http_path: menu lateral → SQL Warehouses → clica no seu warehouse → aba Connection details. O hostname vai sem o https:// na frente.
2. access_token: clica no seu avatar (canto superior direito) → Settings → Developer → Access tokens → Generate new token. Dá um nome (tipo “streamlit-enem”) e uma validade. O token aparece uma vez só: copia direto para o secrets.toml.