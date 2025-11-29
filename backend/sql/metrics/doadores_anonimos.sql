-- Consulta de Anonimização: Doadores com dados pessoais mascarados
-- Usa funções SQL para anonimização:
-- - Nome: Primeira letra + '*****'
-- - CPF: Primeiros 3 dígitos + '.***.***-**'
-- - Idade: Calculada a partir da Data de Nascimento (Generalização)
SELECT 
    CONCAT(LEFT(nome, 1), REPEAT('*', 5)) as nome_anonimizado,
    CONCAT(LEFT(cpf, 3), '.***.***-**') as cpf_mascarado,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, dataNascimento)) as idade,
    genero,
    tiposanguineo
FROM Pessoa P
JOIN Doador D ON P.Id = D.Id;
