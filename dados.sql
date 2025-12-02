-- Alimentacao Inicial da Base de Dados

-- 1. InstituicaoSaude
INSERT INTO InstituicaoSaude (CNPJ, nome, cidade, estado, logradouro) VALUES 
('12.345.678/0001-90', 'Hospital Santa Casa', 'São Paulo', 'SP', 'Rua Dr. Cesario Motta Jr, 112'),
('98.765.432/0001-10', 'Hemocentro Regional', 'Campinas', 'SP', 'Rua Carlos Chagas, 480'),
('11.222.333/0001-44', 'Posto de Coleta Centro', 'São Paulo', 'SP', 'Av. Paulista, 1000'),
('55.666.777/0001-88', 'Hospital das Clinicas', 'São Paulo', 'SP', 'Av. Dr. Enéas Carvalho de Aguiar, 255'),
('22.333.444/0001-55', 'Hemocentro Capital', 'São Paulo', 'SP', 'Av. Brasil, 500');

-- 2. Subtipos
INSERT INTO Hospital (CNPJ) VALUES 
('12.345.678/0001-90'),
('55.666.777/0001-88');

INSERT INTO Hemocentro (CNPJ) VALUES 
('98.765.432/0001-10'),
('22.333.444/0001-55');

INSERT INTO CentroDeColeta (CNPJ, codigo, cidade, estado, logradouro, ativo, dataAbertura, dataFechamento) VALUES 
('11.222.333/0001-44', 'C001', 'São Paulo', 'SP', 'Av. Paulista, 1000', TRUE, '2020-01-01', NULL),
('98.765.432/0001-10', 'C002', 'Campinas', 'SP', 'Rua Carlos Chagas, 480', TRUE, '2019-05-15', NULL);

-- 3. TipoInstituicao
INSERT INTO TipoInstituicao (CNPJ, tipo) VALUES 
('12.345.678/0001-90', 'HOSPITAL'),
('98.765.432/0001-10', 'HEMOCENTRO'),
('98.765.432/0001-10', 'BANCO DE SANGUE'),
('11.222.333/0001-44', 'CENTRO COLETA'),
('22.333.444/0001-55', 'HEMOCENTRO');

-- 4. EstoqueSangue
INSERT INTO EstoqueSangue (InstituicaoSaude, NumOMinus, NumAMinus, NumBMinus, NumABMinus, NumOPlus, NumAPlus, NumBPlus, NumABPlus) VALUES 
('98.765.432/0001-10', 0, 0, 0, 0, 1, 1, 0, 0),
('22.333.444/0001-55', 0, 0, 0, 1, 1, 0, 0, 0);

-- 5. Pessoa
INSERT INTO Pessoa (Id, nome, genero, tiposanguineo, cidade, estado, logradouro, dataNascimento, telefone, email, cpf) VALUES 
('P001', 'João Silva', 'MASCULINO', 'O+', 'São Paulo', 'SP', 'Rua A, 123', '1990-05-20', '11 99999-1111', 'joao@email.com', '111.111.111-11'),
('P002', 'Maria Santos', 'FEMININO', 'A-', 'Campinas', 'SP', 'Rua B, 456', '1985-10-10', '19 98888-2222', 'maria@email.com', '222.222.222-22'),
('P003', 'Roberto', 'MASCULINO', NULL, 'São Paulo', 'SP', 'Rua C, 789', '1975-03-15', '11 97777-3333', 'roberto@med.com', '333.333.333-33'),
('P004', 'Ana', 'FEMININO', NULL, 'São Paulo', 'SP', 'Rua D, 101', '1988-07-22', '11 96666-4444', 'ana@enf.com', '444.444.444-44'),
('P005', 'Carlos', 'MASCULINO', NULL, 'Campinas', 'SP', 'Rua E, 202', '1992-12-05', '19 95555-5555', 'carlos@bio.com', '555.555.555-55'),
('P006', 'Lucas', 'MASCULINO', NULL, 'São Paulo', 'SP', 'Rua F, 303', '1995-08-30', '11 94444-6666', 'lucas@agente.com', '666.666.666-66'),
('P007', 'Julia', 'FEMININO', NULL, 'São Paulo', 'SP', 'Rua G, 404', '1980-01-01', '11 93333-7777', 'julia@med.com', '777.777.777-77'),
('P008', 'Pedro', 'MASCULINO', NULL, 'Campinas', 'SP', 'Rua H, 505', '1989-02-02', '19 92222-8888', 'pedro@enf.com', '888.888.888-88'),
('P009', 'Fernanda', 'FEMININO', NULL, 'São Paulo', 'SP', 'Rua I, 606', '1993-03-03', '11 91111-9999', 'fernanda@bio.com', '999.999.999-99'),
('P010', 'Marcos', 'MASCULINO', NULL, 'Campinas', 'SP', 'Rua J, 707', '1996-04-04', '19 90000-0000', 'marcos@agente.com', '000.000.000-00'),
('P011', 'Andre Ribeiro', 'MASCULINO', 'AB-', 'São Paulo', 'SP', 'Rua Ribeirao, 123', '1930-05-20', '11 99741-1111', 'andre@email.com', '123.456.789-11'),
('P012', 'Elaine', 'FEMININO', 'A+', 'Rio Claro', 'SP', 'Rua Sim, 54', '1910-05-20', '11 99985-1111', 'elaine@email.com', '123.456.789-12'),
('P013', 'Jose Marcos', 'MASCULINO', 'B-', 'São Carlos', 'SP', 'Rua Padre, 2', '1958-05-20', '11 99785-1111', 'jm@email.com', '183.456.789-12');

-- 6. TipoPessoa
INSERT INTO TipoPessoa (Id, tipo) VALUES 
('P001', 'DOADOR'),
('P002', 'RECEPTOR'),
('P003', 'MEDICO'),
('P004', 'ENFERMEIRO'),
('P005', 'BIOMEDICO'),
('P006', 'AGENTE'),
('P007', 'MEDICO'),
('P008', 'ENFERMEIRO'),
('P009', 'BIOMEDICO'),
('P010', 'AGENTE'),
('P011', 'DOADOR'),
('P012', 'DOADOR'),
('P013', 'DOADOR');

-- 7. Profissionais
INSERT INTO Medico (Id, CRM) VALUES ('P003', '123456'), ('P007', '654321');
INSERT INTO Enfermeiro (Id, COREN) VALUES ('P004', '654321'), ('P008', '123456');
INSERT INTO Biomedico (Id, CRBM) VALUES ('P005', '112233'), ('P009', '332211');
INSERT INTO AgenteMapeamento (Id) VALUES ('P006'), ('P010');

-- 8. Clientes
INSERT INTO Doador (Id, peso, altura) VALUES 
('P001', 80.5, 1.75),
('P002', 65.0, 1.65), -- Maria tambem pode ser doadora em outro contexto, mas aqui eh Receptor primario
('P011', 80.0, 1.99),
('P012', 56.0, 1.64),
('P013', 120.0, 1.65);

INSERT INTO Receptor (Id) VALUES 
('P011'),
('P012'),
('P002'),
('P001'); -- Joao pode ser receptor tambem

-- 9. Atributos Multivalorados
INSERT INTO ISTDoador (Id, IST) VALUES 
('P013', 'Gonorreia'),
('P013', 'Sifilis');

INSERT INTO MotivoReceptor (Id, motivo) VALUES 
('P002', 'Cirurgia Cardíaca'),
('P001', 'Transplante de Medula');

-- 10. Triagem
INSERT INTO Triagem (IdTriagem, Doador, DataHora, Enfermeiro, Valido, CentroColeta_CNPJ, CentroColeta_Codigo) VALUES 
('T001', 'P001', '2023-10-01 08:00:00', 'P004', TRUE, '11.222.333/0001-44', 'C001'),
('T002', 'P001', '2023-11-01 09:00:00', 'P004', TRUE, '11.222.333/0001-44', 'C001'),
('T003', 'P011', '2024-10-01 08:00:00', 'P004', TRUE, '11.222.333/0001-44', 'C001'),
('T004', 'P012', '2024-11-01 09:00:00', 'P004', TRUE, '11.222.333/0001-44', 'C001');

-- 11. BolsaSangue
INSERT INTO BolsaSangue (Codigo, VolumeDoado, TipoSangue, Valido, Triagem, Biomedico, Hemocentro, DataTestagem) VALUES 
('B001', 450, 'O+', TRUE, 'T001', 'P005', '98.765.432/0001-10', '2023-10-02'),
('B002', 460, 'O+', TRUE, 'T002', 'P005', '22.333.444/0001-55', '2023-11-02'),
('B003', 440, 'AB-', TRUE, 'T003', 'P005', '22.333.444/0001-55', '2023-10-02'),
('B004', 470, 'A+', TRUE, 'T004', 'P005', '98.765.432/0001-10', '2023-10-02');

-- 12. Procedimento
INSERT INTO Procedimento (Receptor, DataHora, Medico, Hospital) VALUES 
('P002', '2023-10-05 14:00:00', 'P003', '12.345.678/0001-90'),
('P002', '2023-10-06 10:00:00', 'P003', '12.345.678/0001-90');

-- 13. Pesquisa
INSERT INTO Pesquisa (Doador, DataHora, AgenteMapeamento, Doou, PrimeiraDoacao, DoariaNovamente, Feedback) VALUES 
('P001', '2023-10-01 08:30:00', 'P006', TRUE, TRUE, TRUE, 'Ótimo atendimento'),
('P001', '2023-11-01 09:30:00', 'P006', TRUE, FALSE, TRUE, 'Rápido e eficiente');

-- 14. Solicitacao
INSERT INTO Solicitacao (Hospital, DataHora, Hemocentro, QntOPlus, QntOMinus, QntAPlus, QntAMinus, QntBPlus, QntBMinus, QntABPlus, QntABMinus, AceitaNegada) VALUES 
('12.345.678/0001-90', '2023-10-04 10:00:00', '98.765.432/0001-10', 5, 2, 0, 0, 0, 0, 0, 0, TRUE),
('12.345.678/0001-90', '2023-10-05 11:00:00', '22.333.444/0001-55', 5, 2, 0, 0, 0, 0, 0, 0, TRUE),
('55.666.777/0001-88', '2023-10-05 11:00:00', '98.765.432/0001-10', 0, 0, 10, 5, 0, 0, 0, 0, FALSE);

-- 15. Transferencia
INSERT INTO Transferencia (HemoOrigem, HemoDestino, DataHora, QntOPlus, QntOMinus, QntAPlus, QntAMinus, QntBPlus, QntBMinus, QntABPlus, QntABMinus, AceitaNegada) VALUES 
('98.765.432/0001-10', '98.765.432/0001-10', '2023-10-10 15:00:00', 2, 0, 0, 0, 0, 0, 0, 0, TRUE), -- Transferencia propria por exemplo, ou precisa de outro Hemocentro
('98.765.432/0001-10', '22.333.444/0001-55', '2023-11-15 10:00:00', 0, 0, 5, 0, 0, 0, 0, 0, TRUE);

-- 16. Usuarios
INSERT INTO Usuario (Login, Senha, Role, PessoaId) VALUES
('admin', 'admin', 'admin', NULL),
('medico', '123', 'medico', 'P003'),
('enfermeiro', '123', 'enfermeiro', 'P004'),
('biomedico', '123', 'biomedico', 'P005'),
('agente', '123', 'agente', 'P006'),
('instituicao', '123', 'instituicao', NULL),
('doador', '123', 'doador', 'P001'),
('receptor', '123', 'receptor', 'P002');

-- 17. Permissoes
INSERT INTO Permissao (Id, Nome) VALUES
(1, 'CADASTRAR_INSTITUICAO'),
(2, 'VER_METRICAS'),
(3, 'VER_DADOS_SENSIVEIS');

-- 18. RolePermissao
INSERT INTO RolePermissao (Role, PermissaoId) VALUES
('admin', 1), -- Admin pode criar instituicoes
('admin', 2), -- Admin pode ver metricas
('admin', 3), -- Admin pode ver dados sensiveis
('instituicao', 2), -- Instituicao pode ver metricas
('medico', 3), -- Medico pode ver dados sensiveis (ex: pacientes)
('enfermeiro', 3); -- Enfermeiro pode ver dados sensiveis
