# Consulta SQL - Gestran

```sql
/*
select Codigo_Classificacao, tipo_lancamento, codigo_contacorrente, identificacao, tipoconta,
       Codigo_ModeloDocumento, Descricao_Modelo,
	   sum(vl_lancamento)
  from v_LancamentosFinanceiros
 where dataemissao between '20240901' and '20241231'
   and tipoconta = 'Conta Corrente'
   and vl_lancamento > 0
   and identificacao <> 'DUTRANSLOG'
   --and codigo_empresa = 2
 group by Codigo_Classificacao, tipo_lancamento, codigo_contacorrente, identificacao, tipoconta,
       Codigo_ModeloDocumento, Descricao_Modelo

update guapoRegraFinanceiro
   set texto_complemento = '',
       var_complemento_a = 'nr_documento',
	   var_complemento_b = 'fornecedor'
*/ -- Script segundo o layout de importar XLS

SELECT --'RECEITA FRETE PESO'+';'+
 --r.Valor_Produto,
 convert(VARCHAR(10), f.dataemissao, 103)+';'+--DATA convert(varchar(10), rf.conta_credito)+';'+ -- conta_debito -- No arquivo está invertido
 --convert(varchar(10), rf.conta_debito)+';'+ -- conta_credito -- No arquivo está invertido
 convert(varchar(10), CASE
                          WHEN f.Numero_CNPJCPF like '03626094%' THEN 170720 --  Debito = 170720

                          WHEN f.Numero_CNPJCPF like '72469687%' THEN 171985 --  Debito = 171985

                          WHEN f.Numero_CNPJCPF like '10321549%' THEN 501014 --  Debito = 501014

                          WHEN f.Numero_CNPJCPF like '75410118%' THEN 501015 --  Debito = 501015

                          WHEN f.Numero_CNPJCPF like '17569551%' THEN 171979 --  Debito = 171979

                          ELSE convert(varchar(10), rf.conta_debito)
                      END)+';'+ -- conta_credito
 replace(CONVERT(VARCHAR, convert(MONEY, f.vl_lancamento)), '.', ',')+';'+ convert(varchar(10), rf.cod_historico)+';'+ -- cod_historico
 --rd.texto_complemento, rd.var_complemento_a, rd.var_complemento_B, rd.var_complemento_C,
 isnull(rf.texto_complemento+' '--
 +replace(replace(replace(replace(replace(replace(replace(var_complemento_A, 'mes ', datename(MONTH, f.dataemissao)), 'fornecedor', f.Nome_Fantasia+' - '+f.nome_razaosocial), 'caminhao', isnull('', '')), 'funcionario', f.Nome_RazaoSocial), 'nr_documento', (convert(varchar(15), f.NumeroTitulo)+'/'+convert(varchar(5), f.Numero_Parcela))), 'placa', isnull('', '')), 'trimestre', '4º Trimestre') +' '+ +replace(replace(replace(replace(replace(replace(replace(var_complemento_B, 'mes ', datename(MONTH, f.dataemissao)), 'fornecedor', f.Nome_Fantasia+' - '+f.nome_razaosocial), 'caminhao', isnull('', '')), 'funcionario', f.Nome_RazaoSocial), 'nr_documento', (convert(varchar(15), f.NumeroTitulo)+'/'+convert(varchar(5), f.Numero_Parcela))), 'placa', isnull('', '')), 'trimestre', '4º Trimestre') , f.tipo_lancamento)+';'+ --'PRESTAÇÃO DE SERV. | '+v.Placa+' | CONF: '+convert(varchar(10), D.numero_documento)+' - '+p.Nome_RazaoSocial,--+';'+
 +'1'+';'+ CASE
               WHEN f.codigo_empresa = 1 THEN '10'
               WHEN f.codigo_empresa = 2 THEN '8'
               WHEN f.codigo_empresa = 3 THEN '1'
           END+';'+ +';'+--CC_Debito ';' -- CC_Creditoa

FROM v_LancamentosFinanceiros f
JOIN guapoRegraFinanceiro rf ON rf.codigo_classificacao = f.codigo_classificacao
AND rf.tipo_classificacao = f.tipo_lancamento
AND rf.codigo_banco = f.codigo_contacorrente
AND rf.descricao_lancamento = f.descricao_modelo
AND isnull(rf.codigo_empresa, f.Codigo_Empresa) = f.Codigo_Empresa
WHERE dataemissao BETWEEN '20250101' AND '20250131'
  AND tipoconta = 'Conta Corrente'
  AND vl_lancamento > 0
  AND identificacao <> 'DUTRANSLOG'
  AND f.codigo_empresa = 2
ORDER BY dataemissao --where numero_documento = 41351
```
