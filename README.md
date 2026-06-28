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

