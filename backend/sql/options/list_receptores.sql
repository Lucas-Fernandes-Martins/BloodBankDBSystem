-- Obter todos os receptores de sangue para opções de dropdown
SELECT P.Id, P.nome, P.cpf
FROM Receptor R
JOIN Pessoa P ON R.Id = P.Id;
