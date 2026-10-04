-- Criação da tabela de resultados na camada silver
CREATE TABLE IF NOT EXISTS enem_pipeline.silver.resultados (
    id_inscricao STRING COMMENT "Número de inscrição do candidato (NULL a partir de 2024 na tabela de resultados: INEP não divulga mais a inscrição)",
    ano_exame INT COMMENT "Ano da prestação do Exame",
    municipio_esc STRING COMMENT "Município da Escola do participante",
    uf_esc STRING COMMENT "UF da Escola do participante",
    dependencia_adm_esc INT COMMENT "Dependência Administrativa da Escola do participante",
    localizacao_esc INT COMMENT "Localização da Escola do participante",
    sit_func_esc INT COMMENT "Situação Funcional da Escola do participante",
    municipio_prova STRING COMMENT "Município em que o Exame foi prestado",
    uf_prova STRING COMMENT "UF em que o Exame foi prestado",
    presenca_cn INT COMMENT "Presença na prova objetiva de Ciências da Natureza",
    presenca_ch INT COMMENT "Presença na prova objetiva de Ciências Humanas",
    presenca_lc INT COMMENT "Presença na prova objetiva de Linguagens e Códigos",
    presenca_mt INT COMMENT "Presença na prova objetiva de Matemática",
    nota_cn NUMERIC(10,2) COMMENT "Nota na prova objetiva de Ciências da Natureza",
    nota_ch NUMERIC(10,2) COMMENT "Nota na prova objetiva de Ciências Humanas",
    nota_lc NUMERIC(10,2) COMMENT "Nota na prova objetiva de Linguagens e Códigos",
    nota_mt NUMERIC(10,2) COMMENT "Nota na prova objetiva de Matemática",
    nota_redacao NUMERIC(10,2) COMMENT "Nota da prova de Redação",
    nota_comp1 NUMERIC(10,2) COMMENT "Nota da competência 1 em Redação - Demonstrar domínio da modalidade escrita formal da Língua Portuguesa",
    nota_comp2 NUMERIC(10,2) COMMENT "Nota da competência 2 em Redação - Compreender a proposta de redação e aplicar conceitos das várias áreas de conhecimento para desenvolver o tema, dentro dos limites estruturais do texto dissertativo-argumentativo em prosa",
    nota_comp3 NUMERIC(10,2) COMMENT "Nota da competência 3 em Redação - Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista",
    nota_comp4 NUMERIC(10,2) COMMENT "Nota da competência 4 em Redação - Demonstrar conhecimento dos mecanismos linguísticos necessários para a construção da argumentação",
    nota_comp5 NUMERIC(10,2) COMMENT "Nota da competência 5 em Redação - Elaborar proposta de intervenção para o problema abordado, respeitando os direitos humanos",
    status_redacao INT COMMENT "Situação da redação do participante" 
)
COMMENT "
Dados dos Resultados do ENEM em 2022, 2023 e 2024

Fonte: INEP - Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira
";

-- Inserção dos dados de 2022 na tabela de resultados 
INSERT INTO enem_pipeline.silver.resultados BY NAME
REPLACE WHERE ano_exame = 2022
SELECT
    NU_INSCRICAO AS id_inscricao,
    CAST(NU_ANO AS INT) AS ano_exame,
    INITCAP(NO_MUNICIPIO_ESC) AS municipio_esc,
    UPPER(SG_UF_ESC) AS uf_esc,
    CAST(TP_DEPENDENCIA_ADM_ESC AS INT) AS dependencia_adm_esc,
    CAST(TP_LOCALIZACAO_ESC AS INT) AS localizacao_esc,
    CAST(TP_SIT_FUNC_ESC AS INT) AS sit_func_esc,
    INITCAP(NO_MUNICIPIO_PROVA) AS municipio_prova,
    UPPER(SG_UF_PROVA) AS uf_prova,
    CAST(TP_PRESENCA_CN AS INT) AS presenca_cn,
    CAST(TP_PRESENCA_CH AS INT) AS presenca_ch,
    CAST(TP_PRESENCA_LC AS INT) AS presenca_lc,
    CAST(TP_PRESENCA_MT AS INT) AS presenca_mt,
    CAST(NU_NOTA_CN AS NUMERIC(10,2)) AS nota_cn,
    CAST(NU_NOTA_CH AS NUMERIC(10,2)) AS nota_ch,
    CAST(NU_NOTA_LC AS NUMERIC(10,2)) AS nota_lc,
    CAST(NU_NOTA_MT AS NUMERIC(10,2)) AS nota_mt,
    CAST(NU_NOTA_REDACAO AS NUMERIC(10,2)) AS nota_redacao,
    CAST(NU_NOTA_COMP1 AS NUMERIC(10,2)) AS nota_comp1,
    CAST(NU_NOTA_COMP2 AS NUMERIC(10,2)) AS nota_comp2,
    CAST(NU_NOTA_COMP3 AS NUMERIC(10,2)) AS nota_comp3,
    CAST(NU_NOTA_COMP4 AS NUMERIC(10,2)) AS nota_comp4,
    CAST(NU_NOTA_COMP5 AS NUMERIC(10,2)) AS nota_comp5,
    CAST(TP_STATUS_REDACAO AS INT) AS status_redacao
FROM enem_pipeline.bronze.microdados_enem_2022;

-- Inserção dos dados de 2023 na tabela de resultados
INSERT INTO enem_pipeline.silver.resultados BY NAME
REPLACE WHERE ano_exame = 2023
SELECT
    NU_INSCRICAO AS id_inscricao,
    CAST(NU_ANO AS INT) AS ano_exame,
    INITCAP(NO_MUNICIPIO_ESC) AS municipio_esc,
    UPPER(SG_UF_ESC) AS uf_esc,
    CAST(TP_DEPENDENCIA_ADM_ESC AS INT) AS dependencia_adm_esc,
    CAST(TP_LOCALIZACAO_ESC AS INT) AS localizacao_esc,
    CAST(TP_SIT_FUNC_ESC AS INT) AS sit_func_esc,
    INITCAP(NO_MUNICIPIO_PROVA) AS municipio_prova,
    UPPER(SG_UF_PROVA) AS uf_prova,
    CAST(TP_PRESENCA_CN AS INT) AS presenca_cn,
    CAST(TP_PRESENCA_CH AS INT) AS presenca_ch,
    CAST(TP_PRESENCA_LC AS INT) AS presenca_lc,
    CAST(TP_PRESENCA_MT AS INT) AS presenca_mt,
    CAST(NU_NOTA_CN AS NUMERIC(10,2)) AS nota_cn,
    CAST(NU_NOTA_CH AS NUMERIC(10,2)) AS nota_ch,
    CAST(NU_NOTA_LC AS NUMERIC(10,2)) AS nota_lc,
    CAST(NU_NOTA_MT AS NUMERIC(10,2)) AS nota_mt,
    CAST(NU_NOTA_REDACAO AS NUMERIC(10,2)) AS nota_redacao,
    CAST(NU_NOTA_COMP1 AS NUMERIC(10,2)) AS nota_comp1,
    CAST(NU_NOTA_COMP2 AS NUMERIC(10,2)) AS nota_comp2,
    CAST(NU_NOTA_COMP3 AS NUMERIC(10,2)) AS nota_comp3,
    CAST(NU_NOTA_COMP4 AS NUMERIC(10,2)) AS nota_comp4,
    CAST(NU_NOTA_COMP5 AS NUMERIC(10,2)) AS nota_comp5,
    CAST(TP_STATUS_REDACAO AS INT) AS status_redacao
FROM enem_pipeline.bronze.microdados_enem_2023;

-- Inserção dos dados de 2024 na tabela de resultados
INSERT INTO enem_pipeline.silver.resultados BY NAME
REPLACE WHERE ano_exame = 2024
SELECT
    CAST(NULL AS STRING) AS id_inscricao,
    CAST(NU_ANO AS INT) AS ano_exame,
    INITCAP(NO_MUNICIPIO_ESC) AS municipio_esc,
    UPPER(SG_UF_ESC) AS uf_esc,
    CAST(TP_DEPENDENCIA_ADM_ESC AS INT) AS dependencia_adm_esc,
    CAST(TP_LOCALIZACAO_ESC AS INT) AS localizacao_esc,
    CAST(TP_SIT_FUNC_ESC AS INT) AS sit_func_esc,
    INITCAP(NO_MUNICIPIO_PROVA) AS municipio_prova,
    UPPER(SG_UF_PROVA) AS uf_prova,
    CAST(TP_PRESENCA_CN AS INT) AS presenca_cn,
    CAST(TP_PRESENCA_CH AS INT) AS presenca_ch,
    CAST(TP_PRESENCA_LC AS INT) AS presenca_lc,
    CAST(TP_PRESENCA_MT AS INT) AS presenca_mt,
    CAST(NU_NOTA_CN AS NUMERIC(10,2)) AS nota_cn,
    CAST(NU_NOTA_CH AS NUMERIC(10,2)) AS nota_ch,
    CAST(NU_NOTA_LC AS NUMERIC(10,2)) AS nota_lc,
    CAST(NU_NOTA_MT AS NUMERIC(10,2)) AS nota_mt,
    CAST(NU_NOTA_REDACAO AS NUMERIC(10,2)) AS nota_redacao,
    CAST(NU_NOTA_COMP1 AS NUMERIC(10,2)) AS nota_comp1,
    CAST(NU_NOTA_COMP2 AS NUMERIC(10,2)) AS nota_comp2,
    CAST(NU_NOTA_COMP3 AS NUMERIC(10,2)) AS nota_comp3,
    CAST(NU_NOTA_COMP4 AS NUMERIC(10,2)) AS nota_comp4,
    CAST(NU_NOTA_COMP5 AS NUMERIC(10,2)) AS nota_comp5,
    CAST(TP_STATUS_REDACAO AS INT) AS status_redacao
FROM enem_pipeline.bronze.resultados_2024;

-- Criação da tabela de participantes na camada silver
CREATE TABLE IF NOT EXISTS enem_pipeline.silver.participantes (
    id_inscricao STRING COMMENT "Número de inscrição do candidato (NULL a partir de 2024: INEP não divulga mais a inscrição)",
    ano_exame INT COMMENT "Ano da prestação do Exame",
    faixa_etaria INT COMMENT "Faixa etária do participante",
    sexo STRING COMMENT "Sexo do participante",
    estado_civil INT COMMENT "Estado civil do participante",
    cor_raca INT COMMENT "Cor ou Raça do participante",
    nacionalidade INT COMMENT "Nacionalidade do participante",
    st_conclusao INT COMMENT "Situação de conclusão do ensino médio",
    ano_conclusao INT COMMENT "Ano de conclusão do ensino médio",
    escola INT COMMENT "Tipo de escola do ensino médio",
    ensino INT COMMENT "Tipo de instituição que concluiu ou concluirá o Ensino Médio",
    in_treineiro INT COMMENT "Indica se o inscrito fez a prova com intuito de apenas treinar seus conhecimentos",
    municipio_prova STRING COMMENT "Município em que o Exame foi prestado",
    uf_prova STRING COMMENT "UF em que o Exame foi prestado",
    q_escolaridade_pai STRING COMMENT "Questionário Socioeconômico: Até que série seu pai, ou o homem responsável por você, estudou?",
    q_escolaridade_mae STRING COMMENT "Questionário Socioeconômico: Até que série sua mãe, ou a mulher responsável por você, estudou?",
    q_ocupacao_pai STRING COMMENT "Questionário Socioeconômico: A partir da apresentação de algumas ocupações divididas em grupos ordenados, indique o grupo que contempla a ocupação mais próxima da ocupação do seu pai ou do homem responsável por você. (Se ele não estiver trabalhando, escolha uma ocupação pensando no último trabalho dele).",
    q_ocupacao_mae STRING COMMENT "Questionário Socioeconômico: A partir da apresentação de algumas ocupações divididas em grupos ordenados, indique o grupo que contempla a ocupação mais próxima da ocupação da sua mãe ou da mulher responsável por você. (Se ela não estiver trabalhando, escolha uma ocupação pensando no último trabalho dela).",
    q_pessoas_residencia INT COMMENT "Questionário Socioeconômico: Incluindo você, quantas pessoas moram atualmente em sua residência?",
    q_renda_familiar STRING COMMENT "Questionário Socioeconômico: Qual é a renda mensal de sua família? (Some a sua renda com a dos seus familiares.)",
    q_empregado_domestico STRING COMMENT "Questionário Socioeconômico: Em sua residência trabalha empregado(a) doméstico(a)?"
)
COMMENT "
Dados dos participantes do ENEM em 2022, 2023 e 2024.

Obs.: Questionário socioeconômico foi restrito às perguntas comparáveis entre 2022-2024.

Fonte: INEP - Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira
";

-- Inserção dos dados de 2022 na tabela de participantes 
INSERT INTO enem_pipeline.silver.participantes BY NAME   
REPLACE WHERE ano_exame = 2022
SELECT 
    NU_INSCRICAO AS id_inscricao,
    CAST(NU_ANO AS INT) AS ano_exame,
    CAST(TP_FAIXA_ETARIA AS INT) AS faixa_etaria, 
    UPPER(TP_SEXO) AS sexo,
    CAST(TP_ESTADO_CIVIL AS INT) AS estado_civil, 
    CAST(TP_COR_RACA AS INT) AS cor_raca,
    CAST(TP_NACIONALIDADE AS INT) AS nacionalidade,
    CAST(TP_ST_CONCLUSAO AS INT) AS st_conclusao,
    CAST(TP_ANO_CONCLUIU AS INT) AS ano_conclusao,
    CAST(TP_ESCOLA AS INT) AS escola,
    CAST(TP_ENSINO AS INT) AS ensino,
    CAST(IN_TREINEIRO AS INT) AS in_treineiro,
    NO_MUNICIPIO_PROVA AS municipio_prova,
    SG_UF_PROVA AS uf_prova,
    CAST(UPPER(q001) AS STRING) AS q_escolaridade_pai,
    CAST(UPPER(q002) AS STRING) AS q_escolaridade_mae,
    CAST(UPPER(q003) AS STRING) AS q_ocupacao_pai,
    CAST(UPPER(q004) AS STRING) AS q_ocupacao_mae,
    CAST(q005 AS INT) AS q_pessoas_residencia,
    CAST(UPPER(q006) AS STRING) AS q_renda_familiar,
    CAST(UPPER(q007) AS STRING) AS q_empregado_domestico
FROM enem_pipeline.bronze.microdados_enem_2022;

-- Inserção dos dados de 2023 na tabela de participantes 
INSERT INTO enem_pipeline.silver.participantes BY NAME   
REPLACE WHERE ano_exame = 2023
SELECT 
    NU_INSCRICAO AS id_inscricao,
    CAST(NU_ANO AS INT) AS ano_exame,
    CAST(TP_FAIXA_ETARIA AS INT) AS faixa_etaria, 
    UPPER(TP_SEXO) AS sexo,
    CAST(TP_ESTADO_CIVIL AS INT) AS estado_civil, 
    CAST(TP_COR_RACA AS INT) AS cor_raca,
    CAST(TP_NACIONALIDADE AS INT) AS nacionalidade,
    CAST(TP_ST_CONCLUSAO AS INT) AS st_conclusao,
    CAST(TP_ANO_CONCLUIU AS INT) AS ano_conclusao,
    CAST(TP_ESCOLA AS INT) AS escola,
    CAST(TP_ENSINO AS INT) AS ensino,
    CAST(IN_TREINEIRO AS INT) AS in_treineiro,
    NO_MUNICIPIO_PROVA AS municipio_prova,
    SG_UF_PROVA AS uf_prova,
    CAST(UPPER(q001) AS STRING) AS q_escolaridade_pai,
    CAST(UPPER(q002) AS STRING) AS q_escolaridade_mae,
    CAST(UPPER(q003) AS STRING) AS q_ocupacao_pai,
    CAST(UPPER(q004) AS STRING) AS q_ocupacao_mae,
    CAST(q005 AS INT) AS q_pessoas_residencia,
    CAST(UPPER(q006) AS STRING) AS q_renda_familiar,
    CAST(UPPER(q007) AS STRING) AS q_empregado_domestico
FROM enem_pipeline.bronze.microdados_enem_2023;

-- Inserção dos dados de 2024 na tabela de participantes 
INSERT INTO enem_pipeline.silver.participantes BY NAME   
REPLACE WHERE ano_exame = 2024
SELECT 
    NU_INSCRICAO AS id_inscricao,
    CAST(NU_ANO AS INT) AS ano_exame,
    CAST(TP_FAIXA_ETARIA AS INT) AS faixa_etaria, 
    UPPER(TP_SEXO) AS sexo,
    CAST(TP_ESTADO_CIVIL AS INT) AS estado_civil, 
    CAST(TP_COR_RACA AS INT) AS cor_raca,
    CAST(TP_NACIONALIDADE AS INT) AS nacionalidade,
    CAST(TP_ST_CONCLUSAO AS INT) AS st_conclusao,
    CAST(TP_ANO_CONCLUIU AS INT) AS ano_conclusao,
    CAST(NULL AS INT) AS escola,
    CAST(TP_ENSINO AS INT) AS ensino,
    CAST(IN_TREINEIRO AS INT) AS in_treineiro,
    NO_MUNICIPIO_PROVA AS municipio_prova,
    SG_UF_PROVA AS uf_prova,
    CAST(UPPER(q001) AS STRING) AS q_escolaridade_pai,
    CAST(UPPER(q002) AS STRING) AS q_escolaridade_mae,
    CAST(UPPER(q003) AS STRING) AS q_ocupacao_pai,
    CAST(UPPER(q004) AS STRING) AS q_ocupacao_mae,
    CAST(q005 AS INT) AS q_pessoas_residencia,
    CAST(UPPER(q007) AS STRING) AS q_renda_familiar,
    CAST(UPPER(q008) AS STRING) AS q_empregado_domestico
FROM enem_pipeline.bronze.participantes_2024;
