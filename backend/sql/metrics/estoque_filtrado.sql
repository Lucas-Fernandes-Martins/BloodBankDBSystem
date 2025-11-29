-- Obter estoque de sangue por hemocentro com filtro de CNPJ
-- Parâmetros: InstituicaoSaude
SELECT ISaude.nome, E.*
FROM EstoqueSangue E
JOIN InstituicaoSaude ISaude ON E.InstituicaoSaude = ISaude.CNPJ
WHERE E.InstituicaoSaude = %s;
