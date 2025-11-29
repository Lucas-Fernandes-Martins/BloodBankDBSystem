-- Obter todos os médicos com CRM para opções de dropdown
SELECT P.Id, P.nome, M.CRM
FROM Medico M
JOIN Pessoa P ON M.Id = P.Id;
