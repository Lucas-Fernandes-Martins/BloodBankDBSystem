-- Obter todos os biomédicos com CRBM para opções de dropdown
SELECT P.Id, P.nome, B.CRBM
FROM Biomedico B
JOIN Pessoa P ON B.Id = P.Id;
