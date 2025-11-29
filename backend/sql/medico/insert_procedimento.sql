-- Inserir um registro de procedimento médico realizado por médico
-- Parâmetros: Receptor, Medico, Hospital
INSERT INTO Procedimento (Receptor, DataHora, Medico, Hospital)
VALUES (%s, NOW(), %s, %s);
