-- Obter todos os agentes de mapeamento para opções de dropdown
SELECT P.Id, P.nome
FROM AgenteMapeamento A
JOIN Pessoa P ON A.Id = P.Id;
