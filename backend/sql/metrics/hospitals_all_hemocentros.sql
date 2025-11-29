-- Consulta de Divisão: Encontra hospitais que solicitaram de TODOS os hemocentros
SELECT I.nome, H.CNPJ
FROM Hospital H
JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ
WHERE NOT EXISTS (
    (SELECT CNPJ FROM Hemocentro)
    EXCEPT
    (SELECT Hemocentro FROM Solicitacao WHERE Hospital = H.CNPJ)
);
