# Consulta SQL - Sigilo

```sql
WITH params AS
  (SELECT 0 AS cod_empresa,
          0 AS cod_conta),
     saldo_dez AS
  (SELECT (saldos).cod_empresa AS cod_empresa, (saldos).cod_conta AS cod_plano,
                                                        COALESCE((saldos).saldo, 0) AS saldo_final_dez
   FROM
     (SELECT calcula_saldo_conta(CASE
                                     WHEN
                                            (SELECT cod_empresa
                                             FROM params) = 0 THEN NULL
                                     ELSE
                                            (SELECT cod_empresa
                                             FROM params)
                                 END::INTEGER, CASE
                                                   WHEN
                                                          (SELECT cod_conta
                                                           FROM params) = 0 THEN NULL
                                                   ELSE
                                                          (SELECT cod_conta
                                                           FROM params)
                                               END::VARCHAR, '2024-12-31'::DATE) AS saldos) subquery),
     monthly_debits AS
  (SELECT l.cod_empresa,
          l.cod_plano_debito AS cod_plano,
          date_trunc('month', l.data_movimento)::DATE AS mes,
          SUM(l.valor) AS total_debit
   FROM lancamentos_financeiros l
   WHERE l.situacao = 2
     AND l.data_movimento BETWEEN '2025-01-01'::DATE AND '2025-12-31'::DATE
     AND (
            (SELECT cod_empresa
             FROM params) = 0
          OR l.cod_empresa =
            (SELECT cod_empresa
             FROM params))
     AND ((
             (SELECT cod_conta
              FROM params) = 0
           AND l.cod_plano_debito IS NOT NULL)
          OR l.cod_plano_debito =
            (SELECT cod_conta
             FROM params))
     AND l.cod_empresa NOT IN (8549,
                               66844,
                               65532)
   GROUP BY l.cod_empresa,
            l.cod_plano_debito,
            date_trunc('month', l.data_movimento)),
     monthly_credits AS
  (SELECT l.cod_empresa,
          l.cod_plano_credito AS cod_plano,
          date_trunc('month', l.data_movimento)::DATE AS mes,
          SUM(l.valor) AS total_credit
   FROM lancamentos_financeiros l
   WHERE l.situacao = 2
     AND l.data_movimento BETWEEN '2025-01-01'::DATE AND '2025-12-31'::DATE
     AND (
            (SELECT cod_empresa
             FROM params) = 0
          OR l.cod_empresa =
            (SELECT cod_empresa
             FROM params))
     AND ((
             (SELECT cod_conta
              FROM params) = 0
           AND l.cod_plano_credito IS NOT NULL)
          OR l.cod_plano_credito =
            (SELECT cod_conta
             FROM params))
     AND l.cod_empresa NOT IN (8549,
                               66844,
                               65532)
   GROUP BY l.cod_empresa,
            l.cod_plano_credito,
            date_trunc('month', l.data_movimento)),
     meses AS
  (SELECT generate_series('2025-01-01'::DATE, '2025-12-01'::DATE, INTERVAL '1 month')::DATE AS mes),
     contas_ativas AS
  (SELECT DISTINCT cod_empresa,
                   cod_plano
   FROM monthly_debits
   UNION SELECT DISTINCT cod_empresa,
                         cod_plano
   FROM monthly_credits
   UNION SELECT DISTINCT cod_empresa,
                         cod_plano
   FROM saldo_dez),
     base_completa AS
  (SELECT ca.cod_empresa,
          ca.cod_plano,
          m.mes
   FROM contas_ativas ca
   CROSS JOIN meses m),
     monthly AS
  (SELECT bc.cod_empresa,
          bc.cod_plano,
          bc.mes,
          COALESCE(d.total_debit, 0) AS total_debit,
          COALESCE(c.total_credit, 0) AS total_credit,
          COALESCE(d.total_debit, 0) - COALESCE(c.total_credit, 0) AS delta
   FROM base_completa bc
   LEFT JOIN monthly_debits d ON d.cod_empresa = bc.cod_empresa
   AND d.cod_plano = bc.cod_plano
   AND d.mes = bc.mes
   LEFT JOIN monthly_credits c ON c.cod_empresa = bc.cod_empresa
   AND c.cod_plano = bc.cod_plano
   AND c.mes = bc.mes),
     cumulative AS
  (SELECT cod_empresa,
          cod_plano,
          mes,
          total_debit,
          total_credit,
          delta,
          SUM(delta) OVER (PARTITION BY cod_empresa, cod_plano
                           ORDER BY mes ROWS UNBOUNDED PRECEDING) AS cum_delta
   FROM monthly)
SELECT COALESCE(c.cod_empresa, sd.cod_empresa) AS cod_empresa,
       COALESCE(c.cod_plano, sd.cod_plano) AS cod_plano,
       pc.id,
       pc.nome,
       c.mes, -- Saldo Inicial corrigido
 CASE
     WHEN c.mes = '2025-01-01' THEN COALESCE(sd.saldo_final_dez, 0)
     ELSE LAG(COALESCE(sd.saldo_final_dez, 0) + c.cum_delta) OVER (PARTITION BY c.cod_empresa, c.cod_plano
                                                                   ORDER BY c.mes)
 END AS saldo_inicial,
 c.total_debit,
 c.total_credit, -- Saldo Final corrigido
 CASE
     WHEN c.mes = '2025-01-01' THEN COALESCE(sd.saldo_final_dez, 0) + COALESCE(c.total_debit, 0) - COALESCE(c.total_credit, 0)
     ELSE COALESCE(sd.saldo_final_dez, 0) + COALESCE(c.cum_delta, 0)
 END AS saldo_final, -- Subcategoria dos cartões
 CASE
     WHEN c.cod_plano IN (754,
                          756,
                          1339,
                          1375,
                          1825,
                          755,
                          1625,
                          1382,
                          1510,
                          1515,
                          1382) THEN 'Débito'
     WHEN c.cod_plano IN (759,
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
                          828,
                          100,
                          760,
                          1507,
                          1398,
                          1397,
                          1376,
                          1531) THEN 'Crédito'
     WHEN c.cod_plano IN (1556) THEN 'PIX'
     WHEN c.cod_plano IN (775,
                          1497,
                          1519,
                          1538,
                          1562,
                          1583,
                          767,
                          1585,
                          1498) THEN 'VR'
     WHEN c.cod_plano IN (1399,
                          1540,
                          1555,
                          1557,
                          1576) THEN 'Alelo'
     ELSE pc.nome
 END AS subcategoria_cartoes
FROM cumulative c
FULL OUTER JOIN saldo_dez sd ON c.cod_empresa = sd.cod_empresa
AND c.cod_plano = sd.cod_plano
LEFT JOIN plano_contas pc ON COALESCE(c.cod_plano, sd.cod_plano) = pc.cod_plano
WHERE (
         (SELECT cod_empresa
          FROM params) = 0
       OR COALESCE(c.cod_empresa, sd.cod_empresa) =
         (SELECT cod_empresa
          FROM params))
  AND (
         (SELECT cod_conta
          FROM params) = 0
       OR COALESCE(c.cod_plano, sd.cod_plano) =
         (SELECT cod_conta
          FROM params))
  AND COALESCE(c.cod_empresa, sd.cod_empresa) NOT IN (8549,
                                                      66844,
                                                      65532)
  AND c.cod_plano NOT IN (1487,
                          1596,
                          806)
  AND (CAST(pc.id AS TEXT) LIKE '1%'
       OR CAST(pc.id AS TEXT) LIKE '2%')
ORDER BY COALESCE(c.cod_empresa, sd.cod_empresa),
         COALESCE(c.cod_plano, sd.cod_plano),
         c.mes
```
