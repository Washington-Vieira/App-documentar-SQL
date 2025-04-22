# Consulta SQL - Sigilo

```sql
WITH Contas AS
  (-- Traz todas as contas possíveis
 SELECT DISTINCT pc.cod_plano AS cod_conta,
                 pc.nome AS nome_conta
   FROM plano_contas pc),
     FiltroPendencias AS
  (SELECT pf.cod_conta,
          pf.cod_empresa,
          pf.cod_lanc_financeiro,
          pf.data_movimento,
          CASE
              WHEN pf.cod_conta IN (1556,
                                    252,
                                    1859,
                                    1735,
                                    658,
                                    806,
                                    805,
                                    1596,
                                    1578,
                                    1625,
                                    830,
                                    831,
                                    1366,
                                    1567,
                                    162,
                                    165,
                                    167,
                                    413,
                                    423,
                                    425,
                                    744)
                   AND pf.data_vencimento IS NULL THEN pf.data_movimento
              ELSE pf.data_vencimento -- Tratando contas com data vencimento vazia

          END AS data_vencimento,
          pf.valor_pendencia,
          pf.valor_baixado,
          p.nome AS nome_empresa
   FROM pendencias_financeiras pf
   LEFT JOIN pessoas p ON pf.cod_empresa = p.cod_pessoa
   WHERE pf.data_movimento > '2024-12-31'
     AND pf.data_ult_baixa IS NULL
     AND pf.cod_empresa NOT IN (65532,
                                66844,
                                8549)
     AND pf.cod_conta NOT IN (1732,
                              1347,
                              833,
                              1487,
                              806)),
     Movimentacoes AS
  (SELECT COALESCE(fp.nome_empresa, 'E') AS nome_empresa,
          fp.cod_conta,
          fp.cod_empresa,
          fp.cod_lanc_financeiro,
          fp.data_movimento, -- Adiciona 2 dias à data de vencimento para os códigos de conta especificados
 CAST(CASE
          WHEN fp.cod_conta IN (81, 658, 830, 831, 1426, 1430) THEN fp.data_vencimento + INTERVAL '2 days' -- Cheques Pré-datados | Cheques à vista | Cheques Troco | Cheques emitidos | Cheque pré em Trânsito | Cheques custodiados

          WHEN fp.cod_conta IN (159, 747, 156)
               AND fp.data_vencimento IS NULL THEN (fp.data_movimento + INTERVAL '1 month' + INTERVAL '5 days')-- Conta 159

          WHEN fp.cod_conta IN (404, 421)
               AND fp.data_vencimento IS NULL THEN (fp.data_movimento + INTERVAL '1 month' + INTERVAL '20 days')-- FGTS a recolher | INSS a pagar

          WHEN fp.cod_conta IN (422)
               AND fp.data_vencimento IS NULL THEN (fp.data_movimento + INTERVAL '28 days')---Fornecedores nacionais 43421;6869432;"2025-04-08";""

          WHEN fp.cod_conta IN (1562, 1557, 828, 1373, 1521, 1542, 1377, 763)
               AND fp.data_vencimento IS NULL THEN (fp.data_movimento + INTERVAL '31 days')
          ELSE fp.data_vencimento
      END AS DATE) AS data_vencimento, -- Corrige a lógica para considerar a data tratada
 SUM(CASE
         WHEN fp.data_vencimento IS NULL
              AND fp.cod_conta NOT IN (159, 747, 156, 404, 421, 422, 1562, 1557, 828, 1373, 1521, 1542, 1377, 763)-- Não trata códigos já ajustados
 THEN fp.valor_pendencia
         ELSE 0
     END) AS valor_data_vencimento_vazio, -- Define centro de custo
 CASE
     WHEN fp.cod_conta IN(1592,
                          779,
                          754,
                          756,
                          1339,
                          1375,
                          1382,
                          1396,
                          1497,
                          1510,
                          1515,
                          1538,
                          1540,
                          1555,
                          1556,
                          1562,
                          1625,
                          1825,
                          764,
                          759,
                          100,
                          760,
                          761,
                          1826,
                          762,
                          1340,
                          1369,
                          1370,
                          1371,
                          1372,
                          1373,
                          1374,
                          1376,
                          1377,
                          1383,
                          1397,
                          1398,
                          1399,
                          763,
                          1475,
                          1486,
                          1498,
                          1501,
                          1507,
                          1519,
                          1521,
                          1527,
                          1530,
                          1531,
                          1532,
                          1533,
                          1541,
                          1591,
                          1622,
                          1841,
                          755,
                          767,
                          1557,
                          1576,
                          1585,
                          1542,
                          828) THEN 'Cartões'
     WHEN fp.cod_conta IN(81,
                          142,
                          436,
                          658,
                          776,
                          829,
                          830,
                          831,
                          1347,
                          1385,
                          1426,
                          1430,
                          1485,
                          1570) THEN 'Cheques'
     WHEN fp.cod_conta IN(855,
                          4,
                          5,
                          148,
                          149,
                          766,
                          835,
                          838,
                          1587,
                          1735) THEN 'Clientes'
     WHEN fp.cod_conta IN(422,
                          410,
                          411,
                          1336,
                          1797) THEN 'Mercadorias e Serviços'
     WHEN fp.cod_conta IN(402,
                          409,
                          720,
                          747,
                          1594,
                          725,
                          403,
                          421,
                          404,
                          405,
                          406,
                          407,
                          408,
                          159) THEN 'Responsabilidades Trabalhistas'
     WHEN fp.cod_conta IN(413,
                          425,
                          426,
                          427,
                          428,
                          429,
                          430,
                          1765,
                          1767,
                          1840,
                          414,
                          415,
                          416,
                          350,
                          417,
                          418,
                          419,
                          423,
                          162,
                          165,
                          167,
                          744) THEN 'Tributárias e Fiscais'
     WHEN fp.cod_conta IN(443,
                          444,
                          445,
                          446,
                          447,
                          449,
                          459,
                          460,
                          462,
                          463,
                          464,
                          1366,
                          1361,
                          451,
                          452,
                          453,
                          454,
                          455,
                          456,
                          458,
                          1567,
                          1571,
                          1574) THEN 'Curto Prazo'
     WHEN fp.cod_conta IN(490,
                          491,
                          1495,
                          1447,
                          1449,
                          1548,
                          1618) THEN 'Longo Prazo'
     ELSE 'Outros'
 END AS centro_custo, -- Define subcategoria dentro de cartões
 CASE
     WHEN fp.cod_conta IN (754,
                           756,
                           1339,
                           1375,
                           1825,
                           755,
                           1625) THEN 'Débito'
     WHEN fp.cod_conta IN (759,
                           761,
                           762,
                           763,
                           1340,
                           1371,
                           1373,
                           1377,
                           1475,
                           1521,
                           1533,
                           1541,
                           1622,
                           1369,
                           1374,
                           1383,
                           1527,
                           1591,
                           1370,
                           1542,
                           828) THEN 'Crédito'
     WHEN fp.cod_conta IN (1556) THEN 'PIX'
     WHEN fp.cod_conta IN (775,
                           1497,
                           1519,
                           1538,
                           1562,
                           1583,
                           767,
                           1585) THEN 'VR'
     WHEN fp.cod_conta IN (1399,
                           1540,
                           1555,
                           1557,
                           1576) THEN 'Alelo'
     ELSE NULL
 END AS subcategoria_cartoes,
 SUM(fp.valor_pendencia) AS total_valor_pendencia,
 SUM(fp.valor_baixado) AS total_baixado, --SUM(CASE WHEN fp.data_vencimento BETWEEN current_date + 1 AND current_date + 15 THEN fp.valor_pendencia ELSE 0 END) AS valor_15_dias,
 SUM(CASE
         WHEN CAST(CASE
                       WHEN fp.cod_conta IN (81, 658, 830, 831, 1426, 1430) THEN fp.data_vencimento + INTERVAL '2 days' -- Cheques Pré-datados

                       WHEN fp.cod_conta IN (159, 747, 156)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '5 days' -- Conta 159

                       WHEN fp.cod_conta IN (404, 421)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '20 days' -- FGTS a recolher | INSS a pagar

                       WHEN fp.cod_conta IN (422)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '28 days' -- Fornecedores nacionais

                       WHEN fp.cod_conta IN (1562, 1557, 828, 1373, 1521, 1542, 1377, 763)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '31 days' -- Contas específicas

                       ELSE fp.data_vencimento -- Caso padrão

                   END AS DATE) BETWEEN CURRENT_DATE + 1 AND CURRENT_DATE + 15 THEN fp.valor_pendencia
         ELSE 0
     END) AS valor_15_dias,
 SUM(CASE
         WHEN CAST(CASE
                       WHEN fp.cod_conta IN (81, 658, 830, 831, 1426, 1430) THEN fp.data_vencimento + INTERVAL '2 days' -- Cheques Pré-datados, etc.

                       WHEN fp.cod_conta IN (159, 747, 156)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '5 days' -- Conta 159

                       WHEN fp.cod_conta IN (404, 421)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '20 days' -- FGTS a recolher, INSS a pagar

                       WHEN fp.cod_conta IN (422)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '28 days' -- Fornecedores nacionais

                       WHEN fp.cod_conta IN (1562, 1557, 828, 1373, 1521, 1542, 1377, 763)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '31 days' -- Contas específicas

                       ELSE fp.data_vencimento
                   END AS DATE) > CURRENT_DATE + 15
              AND CAST(CASE
                           WHEN fp.cod_conta IN (81, 658, 830, 831, 1426, 1430) THEN fp.data_vencimento + INTERVAL '2 days'
                           WHEN fp.cod_conta IN (159, 747, 156)
                                AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '5 days'
                           WHEN fp.cod_conta IN (404, 421)
                                AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '20 days'
                           WHEN fp.cod_conta IN (422)
                                AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '28 days'
                           WHEN fp.cod_conta IN (1562, 1557, 828, 1373, 1521, 1542, 1377, 763)
                                AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '31 days'
                           ELSE fp.data_vencimento
                       END AS DATE) <= CURRENT_DATE + 45 THEN fp.valor_pendencia
         ELSE 0
     END) AS valor_30_dias,
 SUM(CASE
         WHEN CAST(CASE
                       WHEN fp.cod_conta IN (81, 658, 830, 831, 1426, 1430) THEN fp.data_vencimento + INTERVAL '2 days' -- Cheques Pré-datados, etc.

                       WHEN fp.cod_conta IN (159, 747, 156)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '5 days' -- Conta 159

                       WHEN fp.cod_conta IN (404, 421)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '20 days' -- FGTS a recolher, INSS a pagar

                       WHEN fp.cod_conta IN (422)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '28 days' -- Fornecedores nacionais

                       WHEN fp.cod_conta IN (1562, 1557, 828, 1373, 1521, 1542, 1377, 763)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '31 days' -- Contas específicas

                       ELSE fp.data_vencimento
                   END AS DATE) > CURRENT_DATE + 45
              AND CAST(CASE
                           WHEN fp.cod_conta IN (81, 658, 830, 831, 1426, 1430) THEN fp.data_vencimento + INTERVAL '2 days'
                           WHEN fp.cod_conta IN (159, 747, 156)
                                AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '5 days'
                           WHEN fp.cod_conta IN (404, 421)
                                AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '20 days'
                           WHEN fp.cod_conta IN (422)
                                AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '28 days'
                           WHEN fp.cod_conta IN (1562, 1557, 828, 1373, 1521, 1542, 1377, 763)
                                AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '31 days'
                           ELSE fp.data_vencimento
                       END AS DATE) <= CURRENT_DATE + 75 THEN fp.valor_pendencia
         ELSE 0
     END) AS valor_60_dias,
 SUM(CASE
         WHEN CAST(CASE
                       WHEN fp.cod_conta IN (81, 658, 830, 831, 1426, 1430) THEN fp.data_vencimento + INTERVAL '2 days' -- Cheques Pré-datados, etc.

                       WHEN fp.cod_conta IN (159, 747, 156)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '5 days' -- Conta 159

                       WHEN fp.cod_conta IN (404, 421)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '20 days' -- FGTS a recolher, INSS a pagar

                       WHEN fp.cod_conta IN (422)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '28 days' -- Fornecedores nacionais

                       WHEN fp.cod_conta IN (1562, 1557, 828, 1373, 1521, 1542, 1377, 763)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '31 days' -- Contas específicas

                       ELSE fp.data_vencimento
                   END AS DATE) > CURRENT_DATE + 75
              AND CAST(CASE
                           WHEN fp.cod_conta IN (81, 658, 830, 831, 1426, 1430) THEN fp.data_vencimento + INTERVAL '2 days'
                           WHEN fp.cod_conta IN (159, 747, 156)
                                AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '5 days'
                           WHEN fp.cod_conta IN (404, 421)
                                AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '20 days'
                           WHEN fp.cod_conta IN (422)
                                AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '28 days'
                           WHEN fp.cod_conta IN (1562, 1557, 828, 1373, 1521, 1542, 1377, 763)
                                AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '31 days'
                           ELSE fp.data_vencimento
                       END AS DATE) <= CURRENT_DATE + 105 THEN fp.valor_pendencia
         ELSE 0
     END) AS valor_90_dias,
 SUM(CASE
         WHEN CAST(CASE
                       WHEN fp.cod_conta IN (81, 658, 830, 831, 1426, 1430) THEN fp.data_vencimento + INTERVAL '2 days' -- Cheques Pré-datados

                       WHEN fp.cod_conta IN (159, 747, 156)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '5 days' -- Conta 159

                       WHEN fp.cod_conta IN (404, 421)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '1 month' + INTERVAL '20 days' -- FGTS a recolher | INSS a pagar

                       WHEN fp.cod_conta IN (422)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '28 days' -- Fornecedores nacionais

                       WHEN fp.cod_conta IN (1562, 1557, 828, 1373, 1521, 1542, 1377, 763)
                            AND fp.data_vencimento IS NULL THEN fp.data_movimento + INTERVAL '31 days' -- Contas específicas

                       ELSE fp.data_vencimento -- Caso padrão

                   END AS DATE) > CURRENT_DATE + 105 THEN fp.valor_pendencia
         ELSE 0
     END) AS valor_acima_90_dias
   FROM FiltroPendencias fp
   GROUP BY fp.nome_empresa,
            fp.cod_conta,
            fp.cod_empresa,
            fp.cod_lanc_financeiro,
            fp.data_movimento,
            fp.data_vencimento)
SELECT c.cod_conta,
       c.nome_conta,
       COALESCE(m.nome_empresa, 'E') AS nome_empresa,
       COALESCE(m.cod_empresa, 0) AS cod_empresa,
       COALESCE(m.cod_lanc_financeiro, 0) AS cod_lanc_financeiro,
       COALESCE(m.data_movimento, NULL) AS data_movimento,
       COALESCE(m.data_vencimento, NULL) AS data_vencimento,
       COALESCE(m.centro_custo, 'Outros') AS centro_custo,
       COALESCE(m.subcategoria_cartoes, c.nome_conta) AS subcategoria_cartoes, -- Preenche com o nome da subcategoria se não tiver nome preeenche com nome da conta
 COALESCE(m.total_valor_pendencia, 0) AS total_valor_pendencia,
 COALESCE(m.valor_data_vencimento_vazio, 0) AS valor_data_vencimento_vazio,
 COALESCE(m.total_baixado, 0) AS total_baixado,
 COALESCE(m.valor_15_dias, 0) AS valor_15_dias,
 COALESCE(m.valor_30_dias, 0) AS valor_30_dias,
 COALESCE(m.valor_60_dias, 0) AS valor_60_dias,
 COALESCE(m.valor_90_dias, 0) AS valor_90_dias,
 COALESCE(m.valor_acima_90_dias, 0) AS valor_acima_90_dias
FROM Contas c
LEFT JOIN Movimentacoes m ON c.cod_conta = m.cod_conta
WHERE m.nome_empresa <> 'E' --WHERE
--AND c.cod_conta IN (1562, 1557, 828, 1373, 1521, 1542, 1377, 763)
--AND m.valor_data_vencimento_vazio <> 0
--AND m.cod_lanc_financeiro = 217529401
---AND data_vencimento IS NULL --- EMPRESTIMOS A PAGAR É O QUE ??? 145135320;"2025-03-31";""
ORDER BY c.nome_conta
```
