-- Obter todos os centros de coleta para opções de dropdown
SELECT C.CNPJ, C.codigo, I.nome
FROM CentroDeColeta C
JOIN InstituicaoSaude I ON C.CNPJ = I.CNPJ;
