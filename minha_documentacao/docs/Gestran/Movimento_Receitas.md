# Consulta SQL - Gestran

```sql
/* Gerando em execel
-- Script segundo o layout de importar XLS
select --'RECEITA FRETE PESO'+';'+
       --r.Valor_Produto,
       convert(VARCHAR(10), r.Data_Emissao, 103),--+';'+
       convert(varchar(10), rr.conta_debito),--+';'+  -- conta_debito
	   convert(varchar(10), rr.conta_credito),--+';'+ -- conta_credito
	   replace(CONVERT(VARCHAR, convert(money, r.Valor_Produto)), '.', ','),--+';'+
	   convert(varchar(10), rr.cod_historico),--+';'+ -- cod_historico
	   'PRESTAÇÃO DE SERV. | '+v.Placa+' | CONF: '+convert(varchar(10), r.numero_documento)+' - '+p.Nome_RazaoSocial,--+';'+
	   +'1',--+';'+
	   case when r.codigo_empresa = 1 then '10'
	        when r.codigo_empresa = 2 then '8'
			when r.codigo_empresa = 3 then '1'
	   end,--+';'
	   '',--+';'+
       convert(varchar(10), de_para.centro_custo_dominio)
  from Receitas r
  join Pessoas p on p.Codigo_Pessoa = r.Codigo_Destinatario
  left outer join Veiculos v on v.Codigo_Veiculo = r.Codigo_VeiculoPrincipal
  left outer join Guapo_DW..guapoRegraVeiculoGestran de_para on de_para.cod_veiculo_gestran = r.Codigo_VeiculoPrincipal
  join Guapo_DW..guapoRegraReceitas rr on rr.codigo_produto_servico = r.Codigo_ProdutoServico
 where r.Codigo_ProdutoServico = 1
   and r.Data_Emissao between '20250101' and '20250131'
   and r.Status_Nota <> 'Cancelado'
   and r.Codigo_Empresa = 2
 order by r.Data_Emissao
 --where numero_documento = 41351
 */ -- Retorno em arquivo texto
 -- Script segundo o layout de importar XLS

SELECT --'RECEITA FRETE PESO'+';'+
 --r.Valor_Produto,
 convert(VARCHAR(10), r.Data_Emissao, 103)+';'+ convert(varchar(10), rr.conta_debito)+';'+ -- conta_debito
 convert(varchar(10), rr.conta_credito)+';'+ -- conta_credito
 replace(CONVERT(VARCHAR, convert(MONEY, r.Valor_Produto)), '.', ',')+';'+ convert(varchar(10), rr.cod_historico)+';'+ -- cod_historico
 'PRESTAÇÃO DE SERV. '+v.Placa+' CONF: '+convert(varchar(10), r.numero_documento)+' - '+p.Nome_RazaoSocial+';'+ +'1'+';'+ CASE
                                                                                                                              WHEN r.codigo_empresa = 1 THEN '10'
                                                                                                                              WHEN r.codigo_empresa = 2 THEN '8'
                                                                                                                              WHEN r.codigo_empresa = 3 THEN '1'
                                                                                                                          END+';'+ ''+';'+ convert(varchar(10), de_para.centro_custo_dominio)
FROM Receitas r
JOIN Pessoas p ON p.Codigo_Pessoa = r.Codigo_Destinatario
LEFT OUTER JOIN Veiculos v ON v.Codigo_Veiculo = r.Codigo_VeiculoPrincipal
LEFT OUTER JOIN Guapo_DW..guapoRegraVeiculoGestran de_para ON de_para.cod_veiculo_gestran = r.Codigo_VeiculoPrincipal
JOIN Guapo_DW..guapoRegraReceitas rr ON rr.codigo_produto_servico = r.Codigo_ProdutoServico
WHERE r.Codigo_ProdutoServico = 1
  AND r.Data_Emissao BETWEEN '20250101' AND '20250131'
  AND r.Status_Nota <> 'Cancelado'
  AND r.Codigo_Empresa = 1
ORDER BY r.Data_Emissao --where numero_documento = 41351
```
