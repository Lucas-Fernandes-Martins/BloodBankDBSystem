-- Obter instituições com coordenadas para visualização no mapa
SELECT 
    I.CNPJ, 
    I.nome, 
    I.Latitude, 
    I.Longitude,
    STRING_AGG(T.tipo, ', ') as tipos
FROM InstituicaoSaude I
LEFT JOIN TipoInstituicao T ON I.CNPJ = T.CNPJ
WHERE I.Latitude IS NOT NULL AND I.Longitude IS NOT NULL
GROUP BY I.CNPJ, I.nome, I.Latitude, I.Longitude;
