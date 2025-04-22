# Consulta SQL - Gestran

```sql
/*-- Script segundo o layout de importar XLS
select --'RECEITA FRETE PESO'+';'+
       --r.Valor_Produto,
       convert(VARCHAR(10), d.Data_Emissao, 103),--+';'+
       convert(varchar(10), rd.conta_debito),--+';'+  -- conta_debito
	   convert(varchar(10), rd.conta_credito),--+';'+ -- conta_credito
	   replace(CONVERT(VARCHAR, convert(money, d.Valor_TotalBruto)), '.', ','),--+';'+
	   convert(varchar(10), rd.cod_historico),--+';'+ -- cod_historico
	   --rd.texto_complemento, rd.var_complemento_a, rd.var_complemento_B, rd.var_complemento_C,
	   isnull(
	   rd.texto_complemento+' | '--
	   +replace(replace(replace(replace(replace(replace(replace(var_complemento_A, 'mes', datename(month,d.Data_Emissao)), 'fornecedor', p.Nome_Fantasia+' - '+p.nome_razaosocial),
	            'caminhao', isnull(v.Modelo, '')), 'funcionario', p.Nome_RazaoSocial), 'nr_documento', d.Numero_Documento), 'placa', isnull(v.Placa, '')), 'trimestre', '4º Trimestre')
	   +' | '+
	   +replace(replace(replace(replace(replace(replace(replace(isnull(var_complemento_B, ''), 'mes', datename(month,d.Data_Emissao)), 'fornecedor', p.Nome_Fantasia+' - '+p.nome_razaosocial),
	            'caminhao', isnull(v.Modelo, '')), 'funcionario', p.Nome_RazaoSocial), 'nr_documento', d.Numero_Documento), 'placa', isnull(v.Placa, '')), 'trimestre', '4º Trimestre')
	   , d.Codigo_ProdutoServico),
	   --'PRESTAÇÃO DE SERV. | '+v.Placa+' | CONF: '+convert(varchar(10), D.numero_documento)+' - '+p.Nome_RazaoSocial,--+';'+
	   +'1',--+';'+
	   case when d.codigo_empresa = 1 then '10'
	        when d.codigo_empresa = 2 then '8'
			when d.codigo_empresa = 3 then '1'
	   end,--+';'
	   case when d.Codigo_ProdutoServico in(984) then 178
	        when d.Codigo_ProdutoServico in(49,50,143,152,206) then 179 -- Se for uso e consumo de combustível para uma conta de rateio
	        when ((d.Codigo_ProdutoServico in(99,101,217,250) and (convert(varchar(10), de_para.centro_custo_dominio) is null))) then 179
			else  isnull(convert(varchar(10), de_para.centro_custo_dominio), 177)
	   end,--CC_Debito
	   ''--+';'+ -- CC_Credito

  from G8BD_BI..Despesas d
  join G8BD_BI..Pessoas p on p.Codigo_Pessoa = d.Codigo_Emitente
  left outer join G8BD_BI..Veiculos v on v.Codigo_Veiculo = d.Codigo_Veiculo
  left outer join Guapo_DW..guapoRegraVeiculoGestran de_para on de_para.cod_veiculo_gestran = d.codigo_veiculo
  join Guapo_DW..guapoRegraDespesas rd on rd.codigo_produto_servico = d.Codigo_ProdutoServico
 where d.Data_Emissao between '20250101' and '20250131'
   and d.Status_Nota <> 'Cancelado'
   --and d.Codigo_ProdutoServico in(250)
   and d.Codigo_Empresa = 1
   --and d.Valor_TotalBruto = 1930.05
 order by d.Data_Emissao
 --where numero_documento = 41351

*/ -- Script segundo o layout de importar XLS

SELECT --'RECEITA FRETE PESO'+';'+
 --r.Valor_Produto,
 convert(VARCHAR(10), d.Data_Emissao, 103)+';'+ --convert(varchar(10), rd.conta_debito)+';'+  -- conta_debito
 convert(varchar(10), CASE
                          WHEN ((d.Codigo_UnidadeNegocio = 2)
                                AND (d.Codigo_ProdutoServico = 984)) THEN 490010
                          ELSE convert(varchar(10), rd.conta_debito)
                      END)+';'+ -- conta_debito
 --convert(varchar(10), rd.conta_credito)+';'+ -- conta_credito
 convert(varchar(10), CASE
                          WHEN ((d.Codigo_UnidadeNegocio = 2)
                                AND (d.Codigo_ProdutoServico = 984)) THEN 490010 --when p.Numero_CNPJCPF like '03626094%' then 170720 --  Debito = 170720

                          ELSE convert(varchar(10), rd.conta_credito) -- conta_credito

                      END)+';'+ replace(CONVERT(VARCHAR, convert(MONEY, d.Valor_TotalBruto)), '.', ',')+';'+ convert(varchar(10), rd.cod_historico)+';'+ -- cod_historico
 --rd.texto_complemento, rd.var_complemento_a, rd.var_complemento_B, rd.var_complemento_C,
 isnull(rd.texto_complemento+' '--
 +replace(replace(replace(replace(replace(replace(replace(var_complemento_A, 'mes ', datename(MONTH, d.Data_Emissao)), 'fornecedor', p.Nome_Fantasia+' - '+p.nome_razaosocial), 'caminhao', isnull(v.Modelo, '')), 'funcionario', p.Nome_RazaoSocial), 'nr_documento', d.Numero_Documento), 'placa', isnull(v.Placa, '')), 'trimestre', '4º Trimestre') +' '+ +replace(replace(replace(replace(replace(replace(replace(isnull(var_complemento_B, ''), 'mes ', datename(MONTH, d.Data_Emissao)), 'fornecedor', p.Nome_Fantasia+' - '+p.nome_razaosocial), 'caminhao', isnull(v.Modelo, '')), 'funcionario', p.Nome_RazaoSocial), 'nr_documento', d.Numero_Documento), 'placa', isnull(v.Placa, '')), 'trimestre', '4º Trimestre') , d.Codigo_ProdutoServico)+';'+ --'PRESTAÇÃO DE SERV. | '+v.Placa+' | CONF: '+convert(varchar(10), D.numero_documento)+' - '+p.Nome_RazaoSocial,--+';'+
 +'1'+';'+ CASE
               WHEN d.codigo_empresa = 1 THEN '10'
               WHEN d.codigo_empresa = 2 THEN '8'
               WHEN d.codigo_empresa = 3 THEN '1'
           END+';'+ convert(varchar(10), CASE
                                             WHEN d.Codigo_ProdutoServico IN(984) THEN 178
                                             WHEN ((d.Codigo_ProdutoServico IN(84, 242, 87, 243)
                                                    AND (convert(varchar(10), de_para.centro_custo_dominio) IS NULL))) THEN 178
                                             WHEN d.Codigo_ProdutoServico IN(49, 50, 143, 152, 206) THEN 179 -- Se for uso e consumo de combustível para uma conta de rateio

                                             WHEN ((d.Codigo_ProdutoServico IN(99, 101, 217, 250)
                                                    AND (convert(varchar(10), de_para.centro_custo_dominio) IS NULL))) THEN 179
                                             ELSE isnull(convert(varchar(10), de_para.centro_custo_dominio), 177)
                                         END)+';'+--CC_Debito ';' -- CC_Creditoa

FROM G8BD_BI..Despesas d
JOIN G8BD_BI..Pessoas p ON p.Codigo_Pessoa = d.Codigo_Emitente
LEFT OUTER JOIN G8BD_BI..Veiculos v ON v.Codigo_Veiculo = d.Codigo_VeiculoPrincipal
LEFT OUTER JOIN Guapo_DW..guapoRegraVeiculoGestran de_para ON de_para.cod_veiculo_gestran = d.Codigo_VeiculoPrincipal
JOIN Guapo_DW..guapoRegraDespesas rd ON rd.codigo_produto_servico = d.Codigo_ProdutoServico
AND isnull(rd.codigo_empresa, d.Codigo_Empresa) = d.Codigo_Empresa
WHERE d.Data_Emissao BETWEEN '20250101' AND '20250131'
  AND d.Status_Nota = 'Faturado'
  AND d.Codigo_Emitente NOT IN (1420)-- 1420 - SIMPLES NACIONAL

  AND d.Codigo_ProdutoServico NOT IN (88)-- 88 - Salario Administrativo
 --and d.Codigo_Classificacao not in (192) -- 192 - Despesas Administrativas
--and d.Codigo_ProdutoServico in(250)

  AND d.Codigo_Empresa = 2 --and d.Numero_Documento in(1386109, 17419)
 --and d.Valor_TotalBruto = 9979.85

ORDER BY d.Data_Emissao --where numero_documento = 41351
 -- Versão de 11/03/2025 - que geramos os dados de Fevereiro
/*-- Script segundo o layout de importar XLS
select --'RECEITA FRETE PESO'+';'+
       --r.Valor_Produto,
       convert(VARCHAR(10), d.Data_Emissao, 103),--+';'+
       convert(varchar(10), rd.conta_debito),--+';'+  -- conta_debito
	   convert(varchar(10), rd.conta_credito),--+';'+ -- conta_credito
	   replace(CONVERT(VARCHAR, convert(money, d.Valor_TotalBruto)), '.', ','),--+';'+
	   convert(varchar(10), rd.cod_historico),--+';'+ -- cod_historico
	   --rd.texto_complemento, rd.var_complemento_a, rd.var_complemento_B, rd.var_complemento_C,
	   isnull(
	   rd.texto_complemento+' | '--
	   +replace(replace(replace(replace(replace(replace(replace(var_complemento_A, 'mes', datename(month,d.Data_Emissao)), 'fornecedor', p.Nome_Fantasia+' - '+p.nome_razaosocial),
	            'caminhao', isnull(v.Modelo, '')), 'funcionario', p.Nome_RazaoSocial), 'nr_documento', d.Numero_Documento), 'placa', isnull(v.Placa, '')), 'trimestre', '4º Trimestre')
	   +' | '+
	   +replace(replace(replace(replace(replace(replace(replace(isnull(var_complemento_B, ''), 'mes', datename(month,d.Data_Emissao)), 'fornecedor', p.Nome_Fantasia+' - '+p.nome_razaosocial),
	            'caminhao', isnull(v.Modelo, '')), 'funcionario', p.Nome_RazaoSocial), 'nr_documento', d.Numero_Documento), 'placa', isnull(v.Placa, '')), 'trimestre', '4º Trimestre')
	   , d.Codigo_ProdutoServico),
	   --'PRESTAÇÃO DE SERV. | '+v.Placa+' | CONF: '+convert(varchar(10), D.numero_documento)+' - '+p.Nome_RazaoSocial,--+';'+
	   +'1',--+';'+
	   case when d.codigo_empresa = 1 then '10'
	        when d.codigo_empresa = 2 then '8'
			when d.codigo_empresa = 3 then '1'
	   end,--+';'
	   case when d.Codigo_ProdutoServico in(984) then 178
	        when d.Codigo_ProdutoServico in(49,50,143,152,206) then 179 -- Se for uso e consumo de combustível para uma conta de rateio
	        when ((d.Codigo_ProdutoServico in(99,101,217,250) and (convert(varchar(10), de_para.centro_custo_dominio) is null))) then 179
			else  isnull(convert(varchar(10), de_para.centro_custo_dominio), 177)
	   end,--CC_Debito
	   ''--+';'+ -- CC_Credito

  from G8BD_BI..Despesas d
  join G8BD_BI..Pessoas p on p.Codigo_Pessoa = d.Codigo_Emitente
  left outer join G8BD_BI..Veiculos v on v.Codigo_Veiculo = d.Codigo_Veiculo
  left outer join Guapo_DW..guapoRegraVeiculoGestran de_para on de_para.cod_veiculo_gestran = d.codigo_veiculo
  join Guapo_DW..guapoRegraDespesas rd on rd.codigo_produto_servico = d.Codigo_ProdutoServico
 where d.Data_Emissao between '20250101' and '20250131'
   and d.Status_Nota <> 'Cancelado'
   --and d.Codigo_ProdutoServico in(250)
   and d.Codigo_Empresa = 1
   --and d.Valor_TotalBruto = 1930.05
 order by d.Data_Emissao
 --where numero_documento = 41351

*/ -- Script segundo o layout de importar XLS

SELECT DISTINCT --'RECEITA FRETE PESO'+';'+
 --r.Valor_Produto,
 convert(VARCHAR(10), d.Data_Emissao, 103)+';'+ --convert(varchar(10), rd.conta_debito)+';'+  -- conta_debito
 convert(varchar(10), CASE
                          WHEN ((d.Codigo_UnidadeNegocio = 2)
                                AND (d.Codigo_ProdutoServico = 984)) THEN 490010
                          ELSE convert(varchar(10), rd.conta_debito)
                      END)+';'+ -- conta_debito
 --convert(varchar(10), rd.conta_credito)+';'+ -- conta_credito
 convert(varchar(10), CASE
                          WHEN ((d.Codigo_UnidadeNegocio = 2)
                                AND (d.Codigo_ProdutoServico = 984)) THEN 490010 --when p.Numero_CNPJCPF like '03626094%' then 170720 --  Debito = 170720

                          ELSE convert(varchar(10), rd.conta_credito) -- conta_credito

                      END)+';'+ replace(CONVERT(VARCHAR, convert(MONEY, d.Valor_TotalBruto)), '.', ',')+';'+ convert(varchar(10), rd.cod_historico)+';'+ -- cod_historico
 --rd.texto_complemento, rd.var_complemento_a, rd.var_complemento_B, rd.var_complemento_C,
 isnull(rd.texto_complemento+' '--
 +replace(replace(replace(replace(replace(replace(replace(var_complemento_A, 'mes ', datename(MONTH, d.Data_Emissao)), 'fornecedor', p.Nome_Fantasia+' - '+p.nome_razaosocial), 'caminhao', isnull(v.Modelo, '')), 'funcionario', p.Nome_RazaoSocial), 'nr_documento', d.Numero_Documento), 'placa', isnull(v.Placa, '')), 'trimestre', '4º Trimestre') +' '+ +replace(replace(replace(replace(replace(replace(replace(isnull(var_complemento_B, ''), 'mes ', datename(MONTH, d.Data_Emissao)), 'fornecedor', p.Nome_Fantasia+' - '+p.nome_razaosocial), 'caminhao', isnull(v.Modelo, '')), 'funcionario', p.Nome_RazaoSocial), 'nr_documento', d.Numero_Documento), 'placa', isnull(v.Placa, '')), 'trimestre', '4º Trimestre') , d.Codigo_ProdutoServico)+';'+ --'PRESTAÇÃO DE SERV. | '+v.Placa+' | CONF: '+convert(varchar(10), D.numero_documento)+' - '+p.Nome_RazaoSocial,--+';'+
 +'1'+';'+ CASE
               WHEN d.codigo_empresa = 1 THEN '10'
               WHEN d.codigo_empresa = 2 THEN '8'
               WHEN d.codigo_empresa = 3 THEN '1'
           END+';'+ convert(varchar(10), CASE
                                             WHEN d.Codigo_ProdutoServico IN(984) THEN 178
                                             WHEN ((d.Codigo_ProdutoServico IN(84, 242, 87, 243)
                                                    AND (convert(varchar(10), de_para.centro_custo_dominio) IS NULL))) THEN 178
                                             WHEN d.Codigo_ProdutoServico IN(49, 50, 143, 152, 206) THEN 179 -- Se for uso e consumo de combustível para uma conta de rateio

                                             WHEN ((d.Codigo_ProdutoServico IN(99, 101, 217, 250)
                                                    AND (convert(varchar(10), de_para.centro_custo_dominio) IS NULL))) THEN 179
                                             ELSE isnull(convert(varchar(10), de_para.centro_custo_dominio), 177)
                                         END)+';'+--CC_Debito ';' -- CC_Creditoa

FROM G8BD_BI..Despesas d
JOIN G8BD_BI..Pessoas p ON p.Codigo_Pessoa = d.Codigo_Emitente
LEFT OUTER JOIN G8BD_BI..Veiculos v ON v.Codigo_Veiculo = d.Codigo_VeiculoPrincipal
LEFT OUTER JOIN Guapo_DW..guapoRegraVeiculoGestran de_para ON de_para.cod_veiculo_gestran = d.Codigo_VeiculoPrincipal
JOIN Guapo_DW..guapoRegraDespesas rd ON rd.codigo_produto_servico = d.Codigo_ProdutoServico
AND isnull(rd.codigo_empresa, d.Codigo_Empresa) = d.Codigo_Empresa
WHERE d.Data_Emissao BETWEEN '20250201' AND '20250228'
  AND d.Status_Nota = 'Faturado'
  AND d.Codigo_Emitente NOT IN (1420)-- 1420 - SIMPLES NACIONAL

  AND d.Codigo_ProdutoServico NOT IN (88)-- 88 - Salario Administrativo
 --and d.Codigo_Classificacao not in (192) -- 192 - Despesas Administrativas
--and d.Codigo_ProdutoServico in(250)

  AND d.Codigo_Empresa = 1 --and d.Numero_Documento in(1386109, 17419)
 --and d.Valor_TotalBruto = 9979.85
 --order by d.Data_Emissao
 --where numero_documento = 41351
```
