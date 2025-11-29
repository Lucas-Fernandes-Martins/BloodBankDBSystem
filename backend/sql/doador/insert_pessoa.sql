-- Inserir um novo registro de pessoa
-- Parâmetros: Id, nome, genero, tiposanguineo, cidade, estado, logradouro, dataNascimento, telefone, email, cpf
INSERT INTO Pessoa (Id, nome, genero, tiposanguineo, cidade, estado, logradouro, dataNascimento, telefone, email, cpf)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
