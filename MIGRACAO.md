# ENEM Pipeline — Plano de Migração para Lakehouse (S3 + Delta Lake)

> Migração faseada, com validação em paralelo antes do cutover. Postgres só é desligado depois que o Delta provar paridade.

> **Correção (confirmada na comunidade Databricks):** Databricks Free Edition (sucessor da Community Edition) não lê/escreve S3 externo diretamente — nem via mount, nem via access key. A fonte suportada é **Unity Catalog Volumes** (storage gerenciado pelo próprio Databricks). Em vez de encadear S3 → Databricks (o que exigiria baixar de volta pro disco), o desenho final bifurca a extração em duas pernas independentes a partir do mesmo arquivo local: **Storage Leg** (S3, arquivo versionado/durável) e **Medallion Leg** (Volume do Databricks, fonte de leitura operacional).

---

## Stack final

| Camada | Antes | Depois |
|---|---|---|
| Raw — Storage Leg | Local (`data/`) | S3 (bucket com versionamento, Free Plan) — arquivo durável, não alimenta o Databricks |
| Raw — Medallion Leg | Local (`data/`) | Unity Catalog Volume (upload direto via Databricks CLI) — fonte de leitura do pipeline |
| Bronze / Silver | Postgres (schemas `bronze`/`silver`) | Delta Lake (Databricks) |
| Gold | Postgres (schema `gold`) | Delta Lake (Databricks) |
| BI | Streamlit → Postgres via `psycopg2`/`SQLAlchemy` | **Streamlit mantido** → Databricks via `databricks-sql-connector` |
| Qualidade de dado | `checar_qualidade()` em `transform.py`, contra Postgres | Mesma lógica, reapontada para as tabelas Delta |

Streamlit fica porque é publicável via URL pública (Streamlit Community Cloud) sem exigir login de quem visualiza — diferente de dashboard nativo do Databricks, que pede acesso ao workspace. Isso importa pra portfólio: recrutador abre sem fricção.

---

## Guardrails de custo AWS (antes de criar qualquer recurso)

- [ ] Criar a conta AWS como **Free Plan** (não Paid Plan) — bloqueia serviços de consumo mais caro por padrão
- [ ] Configurar um **Billing Budget** com alerta por e-mail em ~US$1
- [ ] Bucket S3 dentro dos 5GB **Always Free** — subir só os CSVs já filtrados (mesmo subset usado hoje no `carregar_bronze`), não os zips brutos
- [ ] Credencial IAM com permissão mínima (só o bucket específico) para o mount do Databricks — nunca a chave root da conta
- [ ] EC2/compute usado na extração: nunca deixar rodando parado — sobe, roda, desliga

---

## Fases

### Fase 1 — Bifurcar a extração: Storage Leg + Medallion Leg
A partir do mesmo arquivo local extraído, dois uploads independentes — sem encadeamento, sem redundância:

- **Storage Leg**: `extract.py` sobe os CSVs filtrados para o S3 (AWS CLI/boto3), com versionamento ativado no bucket. Papel: arquivo durável e versionado, não alimenta o Databricks.
- **Medallion Leg**: o mesmo arquivo local sobe direto para um Unity Catalog Volume (Databricks CLI). Papel: fonte de leitura operacional do pipeline.
- Postgres e Streamlit continuam funcionando normalmente — nada é tocado ainda

### Fase 2 — Validar as duas pernas
- Confirmar que o objeto aparece versionado no S3
- Confirmar que o arquivo aparece corretamente no Volume e é legível por um notebook Databricks
- Só segue para a Fase 3 se as duas validações passarem

### Fase 3 — Bronze e Silver em Delta
- Recriar a lógica de `carregar_bronze` (hoje em `load.py`) lendo do Volume (não do S3 direto) e escrevendo Delta em vez de `to_sql`
- Reaproveitar as regras de `checar_qualidade()` de `transform.py`, agora contra as tabelas Delta
- Mesmas colunas/schema já validados no Postgres — não redesenhar do zero

### Fase 4 — Rodar em paralelo e comparar
- Por um período curto, Postgres continua servindo o Streamlit normalmente enquanto o Delta roda ao lado
- Comparar contagens de linha e métricas agregadas (por ano, por UF) entre os dois — só avança se baterem

### Fase 5 — Migrar Gold e o Streamlit
- Reescrever `create_gold.py` para ler do Delta
- Trocar o conector do `streamlit/app.py`: sai `psycopg2`/`SQLAlchemy`, entra `databricks-sql-connector`
- Páginas, gráficos e lógica do dashboard não mudam

### Fase 6 — Desligar o Postgres
- Com tudo validado e o Streamlit já lendo do Delta, remover o `docker-compose.yml`/container Postgres
- Migração completa — e com a narrativa de cutover real (fases + validação), não uma troca no escuro

---

## Fora do escopo desta migração (não mexer agora)

- **Carga incremental** e **orquestração** — entram depois que a migração estiver estável, aplicadas já em cima do Delta (evita reforçar lógica que vai ser trocada)
- **MongoDB** — projeto satélite separado, não entra no ENEM
- **API IBGE** — enriquecimento via `no_municipio_prova`/`sg_uf_prova`, fica para depois da migração
- **Git flow completo** — sem dependência técnica, pode rodar em paralelo a qualquer fase