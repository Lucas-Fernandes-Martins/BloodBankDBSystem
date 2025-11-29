-- Consulta de Múltiplos Joins: Conta procedimentos por médico
SELECT P.nome, COUNT(Pr.Medico) as total_procedimentos
FROM Medico M
JOIN Pessoa P ON M.Id = P.Id
JOIN Procedimento Pr ON M.Id = Pr.Medico
GROUP BY M.Id, P.nome
ORDER BY total_procedimentos DESC;
