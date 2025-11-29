-- Consulta Group By: Conta bolsas de sangue válidas por tipo sanguíneo
SELECT TipoSangue, COUNT(*) as total
FROM BolsaSangue
WHERE Valido = TRUE
GROUP BY TipoSangue
ORDER BY total DESC;
