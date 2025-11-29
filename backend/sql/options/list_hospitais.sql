-- Obter todos os hospitais para opções de dropdown
SELECT H.CNPJ, I.nome
FROM Hospital H
JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ;
