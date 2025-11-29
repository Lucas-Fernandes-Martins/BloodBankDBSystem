-- Inserir um registro de triagem realizado por enfermeiro
-- Parâmetros: IdTriagem, Doador, Enfermeiro, Valido, CentroColeta_CNPJ, CentroColeta_Codigo
INSERT INTO Triagem (IdTriagem, Doador, DataHora, Enfermeiro, Valido, CentroColeta_CNPJ, CentroColeta_Codigo)
VALUES (%s, %s, NOW(), %s, %s, %s, %s);
