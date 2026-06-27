# Composição das páginas

# PLANO DE AÇÃO 

1. Truncar as tabelas criadas até o momento, e deletar schema atual
2. Criar schemas na arquitetura medallion: Bronze, Silver, Gold
3. Criar tabelas na camada bronze, com a mesma  estrutura do CSV --> Fazer a alteração necessária no transform.py (olhar quais questionários estão sendo levados para o banco)
4. Examinar o load.py para conseguir fazer a inserção dos dados direto no schema raw (tende a ficar mais simples ainda -- apenas verificar se está caindo na chamada certa)
5. Estudar o uso de classe e funções para executar as tarefas, e usar if __name__ == "__main__": para facilitar quando for criar o orquestrador
6. Com os dados dentro da camada bronze, o seu trasnform.py vai usar sqlaclhemy para fazer a mensageria das queries, e vc conseguir criar as tabelas nas demais camadas
7. Você volta a conectar com o streamlit, mas agora com a arquitetura mais segura e a orquestração encaminhada

## `app.py`

Faz a simples contrução das navegações emtre as páginas. Verificar demais funcionalidades.

## `welcome.py`

A ideia é fazer umas boas-vindas ao usuário do dashboard final, através de uma introdução ao projeto, com intuito da pesquisa, dados coletados, distribuição das páginas e conteúdo. 

1. Deve ser democrático der ler
2. Conter o link do repositório no Github
3. Constar todas as fontes dos dados
4. Suas informações de contato

Qualquer tipo de intrução sobre como ler as informações ali dispostas devem ser realizadas através dessa página, e garantidas que o usuário consuma elas.

**OBS:** Deixar um disclaimer que a análise socioeconômica utiliza os anos 2022 e 2023, únicos anos em que o INEP disponibilizou os dados de forma que permite o cruzamento entre perfil e desempenho do mesmo candidato.

## `main.py`

O objetivo dessa página é ser o foco principal do projeto. Trabalhar a influência da situação socioecônomica no desempenho dos prestadores do vestibular. Os dados devem ser, principalmente, cruzados com os questionários socioecônomicos dados pelo dataset `participantes`.

Possíveis distribuições:

1. Desempenho de notas por faixa de renda familiar (questionario_q6 no dicionário do INEP é renda, e questionario_q7 é a renda mensal familiar) 
2. Desempenho de notas por cor/raça (possuímos a coluna de raca_cor dentro do dataset dos participantes)
3. Desempenho de notas por tipo de escola (questionario_q23 do dataset de participantes)
4. Desempenho por nível de escolaridade dos pais (questionario_q1 e questionario_q2)

As inferências devem, preferencialmente, acompanhadas de uma conclusão lógica e fudamentada nos dados e charts que acompanham a análise. 

## `secundary.py`

Como página secundária, ela trará a visão geral do dataset, sem um foco especifíco do foco, diferentemente da página anterior — foco será na comporação macro entre os anos. Possíveis pontos de trabalho são:

1. Média das notas por ano
2. Média por região/UF (usar de gráfico de região)
3. Distribuição de presença vs ausência
4. Cards com distribuição por Sexo, Estado Civil, Faixa Etária, etc.

O foco aqui é apresentar mais sobre o dataset e a composição das informações, além do foco em desempenho.