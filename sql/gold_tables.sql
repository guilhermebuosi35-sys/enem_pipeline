-- Metric View que contempla as métricas de média para os principais dados socieconômicos
CREATE OR REPLACE VIEW enem_pipeline.gold.mv_desempenho_socioeconomico WITH METRICS LANGUAGE YAML 
COMMENT "Média dos candidatos com base nos principais dados socioeconômicos disponíveis para os anos de 2022 e 2023 (2024 não é contemplado pela impossibilidade de Joins)"
AS $$
version: 1.1
source: enem_pipeline.silver.participantes
joins: 
    - name: resultados
      source: enem_pipeline.silver.resultados
      'on': source.id_inscricao = resultados.id_inscricao
filter: source.ano_exame IN (2022, 2023)
dimensions:
    - name: ano_exame
      expr: source.ano_exame
      comment: Ano do exame prestado pelo participante
    - name: sexo
      expr: CASE WHEN source.sexo = 'F' THEN 'Feminino'
            WHEN source.sexo = 'M' THEN 'Masculino'
            ELSE NULL END
      comment: Gênero do participante
    - name: cor_raca
      expr: CASE WHEN source.cor_raca = 0 THEN 'Não declarado'
            WHEN source.cor_raca = 1 THEN 'Branca'
            WHEN source.cor_raca = 2 THEN 'Preta'
            WHEN source.cor_raca = 3 THEN 'Parda'
            WHEN source.cor_raca = 4 THEN 'Amarela'
            WHEN source.cor_raca = 5 THEN 'Indígena'
            ELSE 'Não dispõe da informação' END
      comment: Raça do participante 
    - name: escola
      expr: CASE WHEN source.escola = 1 THEN 'Não Respondeu'
            WHEN source.escola = 2 THEN 'Pública'
            WHEN source.escola = 3 THEN 'Privada' END
      comment: Tipo de escola do ensino médio do participante
    - name: escolaridade_pai
      expr: CASE WHEN source.q_escolaridade_pai = 'A' THEN 'Nunca estudou'
            WHEN source.q_escolaridade_pai = 'B' THEN 'Não completou a 4ª série/5º ano do Ensino Fundamental'
            WHEN source.q_escolaridade_pai = 'C' THEN 'Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental'
            WHEN source.q_escolaridade_pai = 'D' THEN 'Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio'
            WHEN source.q_escolaridade_pai = 'E' THEN 'Completou o Ensino Médio, mas não completou a Faculdade'
            WHEN source.q_escolaridade_pai = 'F' THEN 'Completou a Faculdade, mas não completou a Pós-graduação'
            WHEN source.q_escolaridade_pai = 'G' THEN 'Completou a Pós-graduação'
            WHEN source.q_escolaridade_pai = 'H' THEN 'Não sei' END
      comment: Escolaridade do pai do participante 
    - name: escolaridade_mae
      expr: CASE WHEN source.q_escolaridade_mae = 'A' THEN 'Nunca estudou'
            WHEN source.q_escolaridade_mae = 'B' THEN 'Não completou a 4ª série/5º ano do Ensino Fundamental'
            WHEN source.q_escolaridade_mae = 'C' THEN 'Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental'
            WHEN source.q_escolaridade_mae = 'D' THEN 'Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio'
            WHEN source.q_escolaridade_mae = 'E' THEN 'Completou o Ensino Médio, mas não completou a Faculdade'
            WHEN source.q_escolaridade_mae = 'F' THEN 'Completou a Faculdade, mas não completou a Pós-graduação'
            WHEN source.q_escolaridade_mae = 'G' THEN 'Completou a Pós-graduação'
            WHEN source.q_escolaridade_mae = 'H' THEN 'Não sei' END
      comment: Escolaridade da mãe do participante
    - name: renda_familiar
      expr: CASE WHEN source.q_renda_familiar = 'A' THEN 'Nenhuma Renda'
            WHEN source.q_renda_familiar = 'B' THEN 'Até 1 salário mínimo'
            WHEN source.q_renda_familiar = 'C' THEN 'De 1 a 1,5 salários mínimos'
            WHEN source.q_renda_familiar = 'D' THEN 'De 1,5 a 2 salários mínimos'
            WHEN source.q_renda_familiar = 'E' THEN 'De 2 a 2,5 salários mínimos'
            WHEN source.q_renda_familiar = 'F' THEN 'De 2,5 a 3 salários mínimos'
            WHEN source.q_renda_familiar = 'G' THEN 'De 3 a 4 salários mínimos'
            WHEN source.q_renda_familiar = 'H' THEN 'De 4 a 5 salários mínimos'
            WHEN source.q_renda_familiar = 'I' THEN 'De 5 a 6 salários mínimos'
            WHEN source.q_renda_familiar = 'J' THEN 'De 6 a 7 salários mínimos'
            WHEN source.q_renda_familiar = 'K' THEN 'De 7 a 8 salários mínimos'
            WHEN source.q_renda_familiar = 'L' THEN 'De 8 a 9 salários mínimos'
            WHEN source.q_renda_familiar = 'M' THEN 'De 9 a 10 salários mínimos'
            WHEN source.q_renda_familiar = 'N' THEN 'De 10 a 12 salários mínimos'
            WHEN source.q_renda_familiar = 'O' THEN 'De 12 a 15 salários mínimos'
            WHEN source.q_renda_familiar = 'P' THEN 'De 15 a 20 salários mínimos'
            WHEN source.q_renda_familiar = 'Q' THEN 'Acima de 20 salários mínimos'
            ELSE 'Não informado' END
      comment: Renda familiar do participante
measures:
    - name: media_nota_cn
      expr: avg(resultados.nota_cn)
      comment: Média da nota de ciências da natureza
    - name: media_nota_ch
      expr: avg(resultados.nota_ch)
      comment: Média da nota de ciências humanas
    - name: media_nota_mt
      expr: avg(resultados.nota_mt)
      comment: Média da nota de matemática 
    - name: media_nota_lc
      expr: avg(resultados.nota_lc)
      comment: Média da nota de linguagens e códigos
    - name: media_nota_comp1
      expr: avg(resultados.nota_comp1)
      comment: Média da nota da competência 1 (Demonstrar domínio da modalidade escrita formal da Língua Portuguesa)
    - name: media_nota_comp2
      expr: avg(resultados.nota_comp2)
      comment: Média da nota da competência 2 (Compreender a proposta de redação e aplicar conceitos das várias áreas de conhecimento para desenvolver o tema, dentro dos limites estruturais do texto dissertativo-argumentativo em prosa)
    - name: media_nota_comp3
      expr: avg(resultados.nota_comp3)
      comment: Média da nota da competência 3 (Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista)
    - name: media_nota_comp4
      expr: avg(resultados.nota_comp4)
      comment: Média da nota da competência 4 (Demonstrar conhecimento dos mecanismos linguísticos necessários para a construção da argumentação)
    - name: media_nota_comp5
      expr: avg(resultados.nota_comp5)
      comment: Média da nota da competência 5 (Elaborar proposta de intervenção para o problema abordado, respeitando os direitos humanos)
    - name: media_nota_redacao
      expr: avg(resultados.nota_redacao)
      comment: Média da nota da redação 
    - name: participantes_cn
      expr: count(resultados.nota_cn)
      comment: Contagem de participantes da prova de ciências da natureza
    - name: participantes_ch
      expr: count(resultados.nota_ch)
      comment: Contagem de participantes da prova de ciências humanas
    - name: participantes_mt
      expr: count(resultados.nota_mt)
      comment: Contagem de participantes da prova de matemática
    - name: participantes_lc
      expr: count(resultados.nota_lc)
      comment: Contagem de participantes da prova de linguagens e códigos
    - name: participantes_redacao
      expr: count (resultados.nota_redacao)
      comment: Contagem de participantes da prova de redação
    - name: inscritos
      expr: count (distinct source.id_inscricao)
      comment: Contagem de participantes
$$;

CREATE OR REPLACE VIEW enem_pipeline.gold.mv_resultados WITH METRICS LANGUAGE YAML
COMMENT "Métricas agregadas sobre os resultados para os anos 2022, 2023 e 2024"
AS $$
version: 1.1
source: enem_pipeline.silver.resultados
dimensions:
    - name: ano_exame
      expr: source.ano_exame
      comment: Ano do exame prestado pelo participante 
    - name: municipio_prova
      expr: source.municipio_prova
      comment: Munícipio da escola em que o participante realizou o exame 
    - name: uf_prova
      expr: source.uf_prova
      comment: UF da escola em que o participante realizou o exame
    - name: municipio_esc
      expr: source.municipio_esc
      comment: Municipio da escola em que o participante estudou
    - name: uf_esc
      expr: source.uf_esc
      comment: UF da escola em que o participante estudou
    - name: dependencia_adm_esc
      expr: CASE WHEN source.dependencia_adm_esc = 1 THEN 'Federal'
            WHEN source.dependencia_adm_esc = 2 THEN 'Estadual'
            WHEN source.dependencia_adm_esc = 3 THEN 'Municipal'
            WHEN source.dependencia_adm_esc = 4 THEN 'Privada'
            END
      comment: Dependência administrativa da escola em que o participante estudou
    - name: localizacao_esc
      expr: CASE WHEN source.localizacao_esc = 1 THEN 'Urbana'
            WHEN source.localizacao_esc = 2 THEN 'Rural'
            END
      comment: Localização da escola em que o participante estudou
measures:
    - name: media_nota_cn
      expr: avg(source.nota_cn)
      comment: Média da nota de ciências da natureza
    - name: media_nota_ch
      expr: avg(source.nota_ch)
      comment: Média da nota de ciências humanas
    - name: media_nota_mt
      expr: avg(source.nota_mt)
      comment: Média da nota de matemática 
    - name: media_nota_lc
      expr: avg(source.nota_lc)
      comment: Média da nota de linguagens e códigos
    - name: media_nota_comp1
      expr: avg(source.nota_comp1)
      comment: Média da nota da competência 1 (Demonstrar domínio da modalidade escrita formal da Língua Portuguesa)
    - name: media_nota_comp2
      expr: avg(source.nota_comp2)
      comment: Média da nota da competência 2 (Compreender a proposta de redação e aplicar conceitos das várias áreas de conhecimento para desenvolver o tema, dentro dos limites estruturais do texto dissertativo-argumentativo em prosa)
    - name: media_nota_comp3
      expr: avg(source.nota_comp3)
      comment: Média da nota da competência 3 (Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista)
    - name: media_nota_comp4
      expr: avg(source.nota_comp4)
      comment: Média da nota da competência 4 (Demonstrar conhecimento dos mecanismos linguísticos necessários para a construção da argumentação)
    - name: media_nota_comp5
      expr: avg(source.nota_comp5)
      comment: Média da nota da competência 5 (Elaborar proposta de intervenção para o problema abordado, respeitando os direitos humanos)
    - name: media_nota_redacao
      expr: avg(source.nota_redacao)
      comment: Média da nota da redação
    - name: faltantes_cn
      expr: count_if(source.presenca_cn = 0)
      comment: Contagem de faltantes da prova de ciências da natureza
    - name: faltantes_ch
      expr: count_if(source.presenca_ch = 0)
      comment: Contagem de faltantes da prova de ciências humanas
    - name: faltantes_mt
      expr: count_if(source.presenca_mt = 0)
      comment: Contagem de faltantes da prova de matemática
    - name: faltantes_lc
      expr: count_if(source.presenca_lc = 0) 
      comment: Contagem de faltantes da prova de linguagens e códigos
    - name: presentes_cn
      expr: count_if(source.presenca_cn = 1)
      comment: Contagem de presentes da prova de ciências da natureza
    - name: presentes_ch
      expr: count_if(source.presenca_ch = 1)
      comment: Contagem de presentes da prova de ciências humanas
    - name: presentes_mt
      expr: count_if(source.presenca_mt = 1)
      comment: Contagem de presentes da prova de matemática
    - name: presentes_lc
      expr: count_if(source.presenca_lc = 1) 
      comment: Contagem de presentes da prova de linguagens e códigos
    - name: eliminados_cn
      expr: count_if(source.presenca_cn = 2)
      comment: Contagem de eliminados da prova de ciências da natureza
    - name: eliminados_ch
      expr: count_if(source.presenca_ch = 2)
      comment: Contagem de eliminados da prova de ciências humanas
    - name: eliminados_mt
      expr: count_if(source.presenca_mt = 2)
      comment: Contagem de eliminados da prova de matemática
    - name: eliminados_lc
      expr: count_if(source.presenca_lc = 2) 
      comment: Contagem de eliminados da prova de linguagens e códigos
$$