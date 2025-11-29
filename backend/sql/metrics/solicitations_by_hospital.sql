-- Consulta Left Join: Lista todos os hospitais e contagem de solicitações (mesmo se 0)
SELECT I.nome, COUNT(S.Hospital) as total_solicitacoes
FROM Hospital H
JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ
LEFT JOIN Solicitacao S ON H.CNPJ = S.Hospital
GROUP BY H.CNPJ, I.nome
ORDER BY total_solicitacoes DESC;
