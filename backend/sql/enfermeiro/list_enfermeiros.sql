-- Obter todos os enfermeiros com COREN para opções de dropdown
SELECT P.Id, P.nome, E.COREN
FROM Enfermeiro E
JOIN Pessoa P ON E.Id = P.Id;
