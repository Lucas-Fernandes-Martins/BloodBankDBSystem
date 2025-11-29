-- Obter triagens válidas para criação de bolsas de sangue
SELECT T.IdTriagem, P.nome as doador_nome, T.DataHora
FROM Triagem T
JOIN Doador D ON T.Doador = D.Id
JOIN Pessoa P ON D.Id = P.Id
WHERE T.Valido = TRUE;
