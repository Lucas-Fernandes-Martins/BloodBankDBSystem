-- Inserir um registro de pesquisa preenchido pelo agente de mapeamento
-- Parâmetros: Doador, AgenteMapeamento, Doou, PrimeiraDoacao, DoariaNovamente, Feedback
INSERT INTO Pesquisa (Doador, DataHora, AgenteMapeamento, Doou, PrimeiraDoacao, DoariaNovamente, Feedback)
VALUES (%s, NOW(), %s, %s, %s, %s, %s);
