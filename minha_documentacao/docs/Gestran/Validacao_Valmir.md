# Consulta SQL - Gestran

```sql
SELECT f.*,
       rf.conta_credito conta_debito,
       rf.conta_debito conta_credito,
       rf.cod_historico
FROM v_LancamentosFinanceiros f
JOIN guapoRegraFinanceiro rf ON rf.codigo_classificacao = f.codigo_classificacao
AND rf.tipo_classificacao = f.tipo_lancamento
AND rf.codigo_banco = f.codigo_contacorrente
AND rf.descricao_lancamento = f.descricao_modelo
WHERE dataemissao BETWEEN '20250101' AND '20250131'
  AND tipoconta = 'Conta Corrente'
  AND vl_lancamento > 0
  AND identificacao <> 'DUTRANSLOG'
  AND f.codigo_empresa = 2
ORDER BY dataemissao
```
