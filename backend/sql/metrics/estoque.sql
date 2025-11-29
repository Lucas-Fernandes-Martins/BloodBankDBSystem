-- Obter estoque de sangue por hemocentro (com filtro opcional)
-- Esta consulta pode ser executada com ou sem a cláusula WHERE
-- Parâmetros: InstituicaoSaude (opcional)
SELECT ISaude.nome, E.*
FROM EstoqueSangue E
JOIN InstituicaoSaude ISaude ON E.InstituicaoSaude = ISaude.CNPJ;
