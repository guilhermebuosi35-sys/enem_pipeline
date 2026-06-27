CREATE OR REPLACE VIEW gold.vw_renda AS
SELECT *
FROM (
    WITH tb_renda AS (
    SELECT 
        vr.id_inscricao, 
        vr.nota_cn AS nota_cn,
        vr.nota_ch AS nota_ch,
        vr.nota_lc AS nota_lc,
        vr.nota_mt AS nota_mt,
        vr.nota_redacao AS nota_redacao,
        vp.q006  AS quest_6
    FROM SILVER.vw_participantes_2022 AS vp 
    INNER JOIN silver.vw_resultados_2022 AS vr 
    ON vp.id_inscricao = vr.id_inscricao 

    UNION ALL

    SELECT
        vr.id_inscricao, 
        vr.nota_cn AS nota_cn,
        vr.nota_ch AS nota_ch,
        vr.nota_lc AS nota_lc,
        vr.nota_mt AS nota_mt,
        vr.nota_redacao AS nota_redacao,
        vp.q006  AS quest_6
    FROM SILVER.vw_participantes_2023 AS vp 
    INNER JOIN silver.vw_resultados_2023 AS vr 
    ON vp.id_inscricao = vr.id_inscricao 
    )
    SELECT 
        quest_6,
        round(avg(nota_cn), 2) AS media_cn,
        round(avg(nota_ch), 2) AS media_ch,
        round(avg(nota_lc), 2) AS media_lc,
        round(avg(nota_mt), 2) AS media_mt,
        round(avg(nota_redacao), 2) AS media_redacao
    FROM tb_renda
    GROUP BY quest_6 
    ORDER BY quest_6
);

CREATE OR REPLACE VIEW gold.vw_cor_raca AS
SELECT *
FROM (
    WITH tb_cor_raca AS (
    SELECT 
        vr.id_inscricao, 
        vr.nota_cn AS nota_cn,
        vr.nota_ch AS nota_ch,
        vr.nota_lc AS nota_lc,
        vr.nota_mt AS nota_mt,
        vr.nota_redacao AS nota_redacao,
        vp.cor_raca  AS cor_raca
    FROM SILVER.vw_participantes_2022 AS vp 
    INNER JOIN silver.vw_resultados_2022 AS vr 
    ON vp.id_inscricao = vr.id_inscricao 

    UNION ALL

    SELECT 
        vr.id_inscricao, 
        vr.nota_cn AS nota_cn,
        vr.nota_ch AS nota_ch,
        vr.nota_lc AS nota_lc,
        vr.nota_mt AS nota_mt,
        vr.nota_redacao AS nota_redacao,
        vp.cor_raca  AS cor_raca
    FROM SILVER.vw_participantes_2023 AS vp 
    INNER JOIN silver.vw_resultados_2023 AS vr 
    ON vp.id_inscricao = vr.id_inscricao 
    )
    SELECT 
        cor_raca,
        round(avg(nota_cn), 2) AS media_cn,
        round(avg(nota_ch), 2) AS media_ch,
        round(avg(nota_lc), 2) AS media_lc,
        round(avg(nota_mt), 2) AS media_mt,
        round(avg(nota_redacao), 2) AS media_redacao
    FROM tb_cor_raca 
    GROUP BY cor_raca  
    ORDER BY cor_raca
); 

CREATE OR REPLACE VIEW gold.vw_dep_escola AS
SELECT *
FROM (
    WITH tb_dep_escola AS (
    SELECT
        vr.id_inscricao, 
        vr.nota_cn AS nota_cn,
        vr.nota_ch AS nota_ch,
        vr.nota_lc AS nota_lc,
        vr.nota_mt AS nota_mt,
        vr.nota_redacao AS nota_redacao,
        vp.escola AS escola
    FROM SILVER.vw_participantes_2022 AS vp 
    INNER JOIN silver.vw_resultados_2022 AS vr 
    ON vp.id_inscricao = vr.id_inscricao 

    UNION ALL

    SELECT
        vr.id_inscricao, 
        vr.nota_cn AS nota_cn,
        vr.nota_ch AS nota_ch,
        vr.nota_lc AS nota_lc,
        vr.nota_mt AS nota_mt,
        vr.nota_redacao AS nota_redacao,
        vp.escola AS escola
    FROM SILVER.vw_participantes_2023 AS vp 
    INNER JOIN silver.vw_resultados_2023 AS vr 
    ON vp.id_inscricao = vr.id_inscricao 
    )
    SELECT 
        escola,
        round(avg(nota_cn), 2) AS media_cn,
        round(avg(nota_ch), 2) AS media_ch,
        round(avg(nota_lc), 2) AS media_lc,
        round(avg(nota_mt), 2) AS media_mt,
        round(avg(nota_redacao), 2) AS media_redacao
    FROM tb_dep_escola 
    GROUP BY escola
    ORDER BY escola 
); 

CREATE OR REPLACE VIEW gold.vw_pai_escolaridade AS 
SELECT *
FROM (
    WITH tb_pai_escolaridade AS (
    SELECT
        vr.id_inscricao,
        vr.nota_cn AS nota_cn,
        vr.nota_ch AS nota_ch,
        vr.nota_lc AS nota_lc,
        vr.nota_mt AS nota_mt,
        vr.nota_redacao AS nota_redacao,
        vp.q001 AS quest_1
    FROM SILVER.vw_participantes_2022 AS vp 
    INNER JOIN silver.vw_resultados_2022 AS vr 
    ON vp.id_inscricao = vr.id_inscricao

    UNION ALL

    SELECT 
        vr.id_inscricao, 
        vr.nota_cn AS nota_cn,
        vr.nota_ch AS nota_ch,
        vr.nota_lc AS nota_lc,
        vr.nota_mt AS nota_mt,
        vr.nota_redacao AS nota_redacao,
        vp.q001 AS quest_1
    FROM SILVER.vw_participantes_2023 AS vp 
    INNER JOIN silver.vw_resultados_2023 AS vr 
    ON vp.id_inscricao = vr.id_inscricao
    )
    SELECT
        quest_1 AS serie_pai,
        round(avg(nota_cn), 2) AS media_cn,
        round(avg(nota_ch), 2) AS media_ch,
        round(avg(nota_lc), 2) AS media_lc,
        round(avg(nota_mt), 2) AS media_mt,
        round(avg(nota_redacao), 2) AS media_redacao
    FROM tb_pai_escolaridade
    GROUP BY serie_pai
    ORDER BY serie_pai    
);

CREATE OR REPLACE VIEW gold.vw_mae_escolaridade AS 
SELECT *
FROM (
    WITH tb_mae_escolaridade AS (
    SELECT
        vr.id_inscricao,
        vr.nota_cn AS nota_cn,
        vr.nota_ch AS nota_ch,
        vr.nota_lc AS nota_lc,
        vr.nota_mt AS nota_mt,
        vr.nota_redacao AS nota_redacao,
        vp.q002 AS quest_2
    FROM SILVER.vw_participantes_2022 AS vp 
    INNER JOIN silver.vw_resultados_2022 AS vr 
    ON vp.id_inscricao = vr.id_inscricao

    UNION ALL

    SELECT 
        vr.id_inscricao, 
        vr.nota_cn AS nota_cn,
        vr.nota_ch AS nota_ch,
        vr.nota_lc AS nota_lc,
        vr.nota_mt AS nota_mt,
        vr.nota_redacao AS nota_redacao,
        vp.q002 AS quest_2
    FROM SILVER.vw_participantes_2023 AS vp 
    INNER JOIN silver.vw_resultados_2023 AS vr 
    ON vp.id_inscricao = vr.id_inscricao
    )
    SELECT
        quest_2 AS serie_mae,
        round(avg(nota_cn), 2) AS media_cn,
        round(avg(nota_ch), 2) AS media_ch,
        round(avg(nota_lc), 2) AS media_lc,
        round(avg(nota_mt), 2) AS media_mt,
        round(avg(nota_redacao), 2) AS media_redacao
    FROM tb_mae_escolaridade
    GROUP BY serie_mae
    ORDER BY serie_mae    
);