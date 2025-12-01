-- name: list_agentes
-- Obter todos os agentes de mapeamento
SELECT P.Id, P.nome
FROM AgenteMapeamento A
JOIN Pessoa P ON A.Id = P.Id;

-- name: check_permission
-- Verificar se o papel (role) tem permissao especifica
SELECT 1
FROM RolePermissao RP
JOIN Permissao P ON RP.PermissaoId = P.Id
WHERE RP.Role = %s AND P.Nome = %s;

-- name: login
-- Autenticar usuario
SELECT Role, PessoaId
FROM Usuario
WHERE Login = %s AND Senha = %s;

-- name: list_biomedicos
-- Obter todos os biomedicos
SELECT P.Id, P.nome, B.CRBM
FROM Biomedico B
JOIN Pessoa P ON B.Id = P.Id;

-- name: list_doadores
-- Obter todos os doadores
SELECT P.Id, P.nome, P.cpf
FROM Doador D
JOIN Pessoa P ON D.Id = P.Id;

-- name: list_enfermeiros
-- Obter todos os enfermeiros
SELECT P.Id, P.nome, E.COREN
FROM Enfermeiro E
JOIN Pessoa P ON E.Id = P.Id;

-- name: list_triagens
-- Obter triagens validas
SELECT T.IdTriagem, P.nome as doador_nome, T.DataHora
FROM Triagem T
JOIN Doador D ON T.Doador = D.Id
JOIN Pessoa P ON D.Id = P.Id
WHERE T.Valido = TRUE;

-- name: list_medicos
-- Obter todos os medicos
SELECT P.Id, P.nome, M.CRM
FROM Medico M
JOIN Pessoa P ON M.Id = P.Id;

-- name: blood_stock_by_type
-- Estoque por tipo sanguineo
SELECT TipoSangue, COUNT(*) as total
FROM BolsaSangue
WHERE Valido = TRUE
GROUP BY TipoSangue
ORDER BY total DESC;

-- name: doadores_anonimos
-- Doadores anonimizados
SELECT 
    CONCAT(LEFT(nome, 1), REPEAT('*', 5)) as nome_anonimizado,
    CONCAT(LEFT(cpf, 3), '.***.***-**') as cpf_mascarado,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, dataNascimento)) as idade,
    genero,
    tiposanguineo
FROM Pessoa P
JOIN Doador D ON P.Id = D.Id;

-- name: estoque
-- Estoque completo (opcionalmente filtrado por instituicao se adicionar WHERE)
SELECT ISaude.nome, E.*
FROM EstoqueSangue E
JOIN InstituicaoSaude ISaude ON E.InstituicaoSaude = ISaude.CNPJ;

-- name: estoque_filtrado
-- Estoque filtrado por instituicao
SELECT ISaude.nome, E.*
FROM EstoqueSangue E
JOIN InstituicaoSaude ISaude ON E.InstituicaoSaude = ISaude.CNPJ
WHERE E.InstituicaoSaude = %s;

-- name: hospitals_all_hemocentros
-- Divisao Relacional: Hospitais que pediram a todos os hemocentros
SELECT I.nome, H.CNPJ
FROM Hospital H
JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ
WHERE NOT EXISTS (
    (SELECT CNPJ FROM Hemocentro)
    EXCEPT
    (SELECT Hemocentro FROM Solicitacao WHERE Hospital = H.CNPJ)
);

-- name: procedures_by_doctor
-- Procedimentos por medico
SELECT P.nome, COUNT(Pr.Medico) as total_procedimentos
FROM Medico M
JOIN Pessoa P ON M.Id = P.Id
JOIN Procedimento Pr ON M.Id = Pr.Medico
GROUP BY M.Id, P.nome
ORDER BY total_procedimentos DESC;

-- name: solicitations_by_hospital
-- Solicitacoes por hospital
SELECT I.nome, COUNT(S.Hospital) as total_solicitacoes
FROM Hospital H
JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ
LEFT JOIN Solicitacao S ON H.CNPJ = S.Hospital
GROUP BY H.CNPJ, I.nome
ORDER BY total_solicitacoes DESC;

-- name: list_centros_coleta
-- Listar centros de coleta
SELECT C.CNPJ, C.codigo, I.nome
FROM CentroDeColeta C
JOIN InstituicaoSaude I ON C.CNPJ = I.CNPJ;

-- name: list_hemocentros
-- Listar hemocentros
SELECT H.CNPJ, I.nome
FROM Hemocentro H
JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ;

-- name: list_hospitais
-- Listar hospitais
SELECT H.CNPJ, I.nome
FROM Hospital H
JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ;

-- name: list_receptores
-- Listar receptores
SELECT P.Id, P.nome, P.cpf
FROM Receptor R
JOIN Pessoa P ON R.Id = P.Id;

-- name: insert_pessoa
-- Inserir nova pessoa
INSERT INTO Pessoa (Id, Nome, Genero, TipoSanguineo, Cidade, Estado, Logradouro, DataNascimento, Telefone, Email, CPF)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);

-- name: insert_tipopessoa
-- Inserir tipo de pessoa
INSERT INTO TipoPessoa (Id, Tipo)
VALUES (%s, %s);

-- name: insert_usuario
-- Inserir novo usuário
INSERT INTO Usuario (Login, Senha, Role, PessoaId)
VALUES (%s, %s, %s, %s);

-- name: insert_medico
-- Inserir médico
INSERT INTO Medico (Id, CRM)
VALUES (%s, %s);

-- name: insert_enfermeiro
-- Inserir enfermeiro
INSERT INTO Enfermeiro (Id, COREN)
VALUES (%s, %s);

-- name: insert_biomedico
-- Inserir biomédico
INSERT INTO Biomedico (Id, CRBM)
VALUES (%s, %s);

-- name: insert_agente
-- Inserir agente
INSERT INTO AgenteMapeamento (Id)
VALUES (%s);

-- name: insert_doador
-- Inserir doador
INSERT INTO Doador (Id, Peso, Altura)
VALUES (%s, %s, %s);

-- name: procedimentos_anonimos
-- (*) Procedimentos anonimizados (Biomédico)
SELECT 
    CONCAT(LEFT(P.nome, 1), REPEAT('*', 5)) as paciente_anonimizado,
    Pr.DataHora,
    Pr.Hospital,
    M.CRM as medico_crm
FROM Procedimento Pr
JOIN Receptor R ON Pr.Receptor = R.Id
JOIN Pessoa P ON R.Id = P.Id
JOIN Medico M ON Pr.Medico = M.Id;

-- name: stock_by_city
-- (*) Estoque por Cidade
SELECT 
    I.cidade,
    SUM(E.NumOPlus + E.NumOMinus + E.NumAPlus + E.NumAMinus + E.NumBPlus + E.NumBMinus + E.NumABPlus + E.NumABMinus) as total_bolsas
FROM EstoqueSangue E
JOIN InstituicaoSaude I ON E.InstituicaoSaude = I.CNPJ
WHERE UNACCENT(I.cidade) ILIKE UNACCENT(%s)
GROUP BY I.cidade;

-- name: attendance_trends
-- (*) Analise de Tendencias em Atendimentos (Dia da semana mais frequente)
SELECT 
    -- Traduz o dia da semana para portugues
    CASE TRIM(TO_CHAR(Pr.DataHora, 'Day'))
        WHEN 'Sunday' THEN 'Domingo'
        WHEN 'Monday' THEN 'Segunda-feira'
        WHEN 'Tuesday' THEN 'Terça-feira'
        WHEN 'Wednesday' THEN 'Quarta-feira'
        WHEN 'Thursday' THEN 'Quinta-feira'
        WHEN 'Friday' THEN 'Sexta-feira'
        WHEN 'Saturday' THEN 'Sábado'
        ELSE TO_CHAR(Pr.DataHora, 'Day')
    END as dia_semana,
    COUNT(*) as frequencia
FROM Procedimento Pr
JOIN Medico M ON Pr.Medico = M.Id
JOIN Receptor R ON Pr.Receptor = R.Id
WHERE M.Id = %s AND R.Id = %s
GROUP BY dia_semana
ORDER BY frequencia DESC
LIMIT 1;

-- name: donations_per_month
-- (*) Doacoes por Mes em determinado centro
SELECT 
    TO_CHAR(T.DataHora, 'YYYY-MM') as mes,
    COUNT(*) as total_doacoes
FROM Triagem T
WHERE T.CentroColeta_CNPJ = %s
GROUP BY mes
ORDER BY mes DESC;

-- name: receptors_by_blood_type
-- (*) Receptores por Tipo Sanguineo Compativel
SELECT P.nome, P.tiposanguineo, P.cidade
FROM Receptor R
JOIN Pessoa P ON R.Id = P.Id
WHERE 
    -- Regras de compatibilidade sanguinea simplificadas
    CASE 
        WHEN %s = 'O-' THEN TRUE -- O- doa para todos
        WHEN %s = 'O+' THEN P.tiposanguineo IN ('O+', 'A+', 'B+', 'AB+')
        WHEN %s = 'A-' THEN P.tiposanguineo IN ('A-', 'A+', 'AB-', 'AB+')
        WHEN %s = 'A+' THEN P.tiposanguineo IN ('A+', 'AB+')
        WHEN %s = 'B-' THEN P.tiposanguineo IN ('B-', 'B+', 'AB-', 'AB+')
        WHEN %s = 'B+' THEN P.tiposanguineo IN ('B+', 'AB+')
        WHEN %s = 'AB-' THEN P.tiposanguineo IN ('AB-', 'AB+')
        WHEN %s = 'AB+' THEN P.tiposanguineo = 'AB+'
        ELSE FALSE
    END;

-- name: donor_history
-- (*) Historico de Doacoes de um Doador
SELECT 
    T.DataHora as data_triagem,
    T.Valido as triagem_aprovada,
    B.Codigo as codigo_bolsa,
    B.Valido as bolsa_valida,
    B.TipoSangue
FROM Triagem T
LEFT JOIN BolsaSangue B ON T.IdTriagem = B.Triagem
WHERE T.Doador = %s
ORDER BY T.DataHora DESC;

-- name: testing_effectiveness
-- (*) Efetividade de Testagens (Biomedico)
SELECT 
    COUNT(B_Valid.Codigo) * 100.0 / COUNT(B_Total.Codigo) as percentual_aprovacao
FROM BolsaSangue B_Total
LEFT JOIN BolsaSangue B_Valid ON B_Total.Codigo = B_Valid.Codigo AND B_Valid.Valido = TRUE
WHERE B_Total.Biomedico = %s
GROUP BY B_Total.Biomedico;

-- name: solicitations_fulfilled
-- (*) Solicitacoes Atendidas (Hospital)
SELECT 
    COUNT(*) FILTER (WHERE AceitaNegada = TRUE) * 100.0 / COUNT(*) as percentual_atendidas
FROM Solicitacao
WHERE Hospital = %s;

-- name: stock_turnover
-- (*) Rotatividade de Estoque (Média de dias em estoque)
-- Proxy: Media de dias desde testagem para bolsas validas atualmente em estoque
SELECT 
    AVG(CURRENT_DATE - DataTestagem) as media_dias_estoque
FROM BolsaSangue
WHERE Valido = TRUE AND Hemocentro = %s;

-- name: donor_receptor_compatibility
-- (*) Compatibilidade Doador-Receptor (Todos os pares)
SELECT 
    D_P.nome as doador, 
    D_P.tiposanguineo as tipo_doador,
    R_P.nome as receptor, 
    R_P.tiposanguineo as tipo_receptor
FROM Doador D
JOIN Pessoa D_P ON D.Id = D_P.Id
CROSS JOIN Receptor R
JOIN Pessoa R_P ON R.Id = R_P.Id
WHERE 
    (D_P.tiposanguineo = 'O-') OR
    (D_P.tiposanguineo = 'O+' AND R_P.tiposanguineo IN ('O+', 'A+', 'B+', 'AB+')) OR
    (D_P.tiposanguineo = 'A-' AND R_P.tiposanguineo IN ('A-', 'A+', 'AB-', 'AB+')) OR
    (D_P.tiposanguineo = 'A+' AND R_P.tiposanguineo IN ('A+', 'AB+')) OR
    (D_P.tiposanguineo = 'B-' AND R_P.tiposanguineo IN ('B-', 'B+', 'AB-', 'AB+')) OR
    (D_P.tiposanguineo = 'B+' AND R_P.tiposanguineo IN ('B+', 'AB+')) OR
    (D_P.tiposanguineo = 'AB-' AND R_P.tiposanguineo IN ('AB-', 'AB+')) OR
    (D_P.tiposanguineo = 'AB+' AND R_P.tiposanguineo = 'AB+')
LIMIT 50;

-- name: campaign_analysis
-- (*) Campanhas de Doacao (Doacoes por periodo)
SELECT 
    COUNT(*) as total_doadores
FROM Triagem
WHERE DataHora BETWEEN %s AND %s;

-- name: hospitals_all_hemocentros_div
-- (*) Hospitais que solicitaram a todos os Hemocentros (Divisao Relacional com EXCEPT/MINUS)
SELECT I.nome, H.CNPJ
FROM Hospital H
JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ
WHERE NOT EXISTS (
    -- Subtrai os que ja pediu do total de hemocentros
    -- Se sobrar zero, entao pediu pra todos
    -- Conjunto de todos os Hemocentros
    (SELECT CNPJ FROM Hemocentro)
    EXCEPT
    -- Conjunto dos Hemocentros que este hospital ja solicitou
    (SELECT Hemocentro FROM Solicitacao S WHERE S.Hospital = H.CNPJ)
);
