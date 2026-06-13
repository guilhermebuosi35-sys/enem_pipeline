# enem_pipeline

## Requisitos

### É necessário baixar o certificado da RNP antes de rodar o extract.py

Instalar o certificado para conseguir realizar o download a partir do site da INEP

Rode os seguintes comandos no PowerShell

**Passo 1:**
*Verifica o certificado que a INEP está utilizando*

```
openssl s_client -connect download.inep.gov.br:443 -showcerts 2>$null | openssl x509 -out <caminho-do-seu-projeto>\rnp_cert.pem
```

- Use `2>$null` para o PowerShell
- Ou `2>/dev/null` para Git Bash

**Passo 2:**
*Acerte o caminho do certificado*

Aloque dentro da varíavel `cert_path` (no Path do extract.py) o caminho para o certificado gerado

## Setup

### Como configurar o ambiente no docker

1. Antes de tudo, crie o seu .env com base na estrutura dada em .env.example
2. Garanta que você possui o Docker instalado no seu ambiente com `docker -v`
3. Rode `docker-compose up -d db` para subir o container referente ao banco de dados
4. Após isso, rode `docker compose ps` para verificar o status
5. Use o seguinte código para criar os schemas e as tabelas: `docker exec -it postgres_db psql -U usuario -d banco < sql/create_schemas.sql < sql/create_tables.sql` (Lembre-se de substituir o "usuario" e "banco" pelos seus nomes alocados no .env)
6. Rode `docker exec -it postgres_db psql -U usuario -d banco` para acessar o terminal do database, e então `\dt` para verificar se as tabelas foram criadas 