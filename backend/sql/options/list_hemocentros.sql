-- Obter todos os hemocentros para opções de dropdown
SELECT H.CNPJ, I.nome
FROM Hemocentro H
JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ;
