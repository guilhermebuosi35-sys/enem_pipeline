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