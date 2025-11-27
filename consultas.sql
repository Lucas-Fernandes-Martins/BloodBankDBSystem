-- Consultas do Sistema

-- 1. Divisão Relacional
-- Encontrar doadores que doaram TODOS os tipos de sangue que o Hospital 'Hospital Santa Casa' já solicitou.
-- (Neste exemplo simplificado, verificamos se o doador doou sangue do mesmo tipo que TODAS as solicitações de um hospital específico exigiram O+)
-- Uma aplicação mais prática: Encontrar Hemocentros que atenderam a TODAS as solicitações de um determinado Hospital.

SELECT H.nome
FROM Hemocentro H
JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ
WHERE NOT EXISTS (
    SELECT S.DataHora
    FROM Solicitacao S
    WHERE S.Hospital = (SELECT CNPJ FROM InstituicaoSaude WHERE nome = 'Hospital Santa Casa')
    AND NOT EXISTS (
        SELECT S2.DataHora
        FROM Solicitacao S2
        WHERE S2.Hemocentro = H.CNPJ
        AND S2.Hospital = S.Hospital
        AND S2.DataHora = S.DataHora
        AND S2.AceitaNegada = TRUE
    )
);

-- 2. Junção Interna com Agrupamento (GROUP BY) e Ordenação
-- Listar a quantidade total de bolsas de sangue coletadas por cada Centro de Coleta, ordenado do maior para o menor.
SELECT ISaude.nome, COUNT(B.Codigo) as TotalBolsas
FROM CentroDeColeta CC
JOIN InstituicaoSaude ISaude ON CC.CNPJ = ISaude.CNPJ
JOIN Triagem T ON CC.CNPJ = T.CentroColeta_CNPJ AND CC.codigo = T.CentroColeta_Codigo
JOIN BolsaSangue B ON T.IdTriagem = B.Triagem
GROUP BY ISaude.nome
ORDER BY TotalBolsas DESC;

-- 3. Junção Externa (LEFT JOIN)
-- Listar todas as Pessoas cadastradas e mostrar se são Doadores (exibindo o peso) ou não.
SELECT P.nome, D.peso
FROM Pessoa P
LEFT JOIN Doador D ON P.Id = D.Id;

-- 4. Subconsulta Correlacionada
-- Listar os Doadores que doaram um volume de sangue ACIMA da média de volume de todas as doações.
SELECT P.nome, B.VolumeDoado
FROM Pessoa P
JOIN Doador D ON P.Id = D.Id
JOIN Triagem T ON D.Id = T.Doador
JOIN BolsaSangue B ON T.IdTriagem = B.Triagem
WHERE B.VolumeDoado > (
    SELECT AVG(VolumeDoado)
    FROM BolsaSangue
);

-- 5. Consulta com Múltiplas Junções e Filtro
-- Relatório detalhado de doações: Nome do Doador, Data da Doação, Nome do Enfermeiro responsável e Nome do Centro de Coleta, apenas para doações Válidas.
SELECT P_Doador.nome AS Doador, T.DataHora, P_Enf.nome AS Enfermeiro, ISaude.nome AS CentroColeta
FROM Triagem T
JOIN Doador D ON T.Doador = D.Id
JOIN Pessoa P_Doador ON D.Id = P_Doador.Id
JOIN Enfermeiro E ON T.Enfermeiro = E.Id
JOIN Pessoa P_Enf ON E.Id = P_Enf.Id
JOIN CentroDeColeta CC ON T.CentroColeta_CNPJ = CC.CNPJ AND T.CentroColeta_Codigo = CC.CentroColeta_Codigo
JOIN InstituicaoSaude ISaude ON CC.CNPJ = ISaude.CNPJ
WHERE T.Valido = TRUE;
