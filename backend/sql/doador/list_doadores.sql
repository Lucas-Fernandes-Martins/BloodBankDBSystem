-- Obter todos os doadores com suas informações pessoais para opções de dropdown
SELECT P.Id, P.nome, P.cpf
FROM Doador D
JOIN Pessoa P ON D.Id = P.Id;
