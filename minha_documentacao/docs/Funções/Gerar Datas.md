# Consulta SQL - Funções

```sql
SELECT generate_series(CURRENT_DATE::DATE, '2025-12-31'::DATE, '1 day'::INTERVAL)::DATE AS data_movimento
```
