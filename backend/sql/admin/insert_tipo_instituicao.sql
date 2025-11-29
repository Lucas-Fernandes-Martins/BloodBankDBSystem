-- Inserir classificação de tipo de instituição
-- Parâmetros: CNPJ, tipo
INSERT INTO TipoInstituicao (CNPJ, tipo)
VALUES (%s, %s);
