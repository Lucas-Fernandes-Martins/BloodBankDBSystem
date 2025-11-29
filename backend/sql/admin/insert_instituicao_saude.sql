-- Inserir registro base de instituição de saúde
-- Parâmetros: CNPJ, nome, cidade, estado, logradouro, Latitude, Longitude
INSERT INTO InstituicaoSaude (CNPJ, nome, cidade, estado, logradouro, Latitude, Longitude)
VALUES (%s, %s, %s, %s, %s, %s, %s);
