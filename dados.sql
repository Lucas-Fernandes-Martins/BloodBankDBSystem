-- Alimentação Inicial da Base de Dados

-- 1. InstituicaoSaude
INSERT INTO InstituicaoSaude (CNPJ, nome, cidade, estado, logradouro, Latitude, Longitude) VALUES 
('12.345.678/0001-90', 'Hospital Santa Casa', 'São Paulo', 'SP', 'Rua Dr. Cesario Motta Jr, 112', -23.5423, -46.6492),
('98.765.432/0001-10', 'Hemocentro Regional', 'Campinas', 'SP', 'Rua Carlos Chagas, 480', -22.8298, -47.0626),
('11.222.333/0001-44', 'Posto de Coleta Centro', 'São Paulo', 'SP', 'Av. Paulista, 1000', -23.5617, -46.6560),
('55.666.777/0001-88', 'Hospital das Clinicas', 'São Paulo', 'SP', 'Av. Dr. Enéas Carvalho de Aguiar, 255', -23.5573, -46.6688);

-- 2. Subtypes
INSERT INTO Hospital (CNPJ) VALUES 
('12.345.678/0001-90'),
('55.666.777/0001-88');

INSERT INTO Hemocentro (CNPJ) VALUES 
('98.765.432/0001-10');

INSERT INTO CentroDeColeta (CNPJ, codigo, cidade, estado, logradouro, ativo, dataAbertura, dataFechamento) VALUES 
('11.222.333/0001-44', 'C001', 'São Paulo', 'SP', 'Av. Paulista, 1000', TRUE, '2020-01-01', NULL),
('98.765.432/0001-10', 'C002', 'Campinas', 'SP', 'Rua Carlos Chagas, 480', TRUE, '2019-05-15', NULL);

-- 3. TipoInstituicao
INSERT INTO TipoInstituicao (CNPJ, tipo) VALUES 
('12.345.678/0001-90', 'HOSPITAL'),
('98.765.432/0001-10', 'HEMOCENTRO'),
('98.765.432/0001-10', 'BANCO DE SANGUE'),
('11.222.333/0001-44', 'CENTRO COLETA');

-- 4. EstoqueSangue
INSERT INTO EstoqueSangue (InstituicaoSaude, NumOMinus, NumAMinus, NumBMinus, NumABMinus, NumOPlus, NumAPlus, NumBPlus, NumABPlus) VALUES 
('98.765.432/0001-10', 10, 5, 2, 1, 20, 15, 8, 4),
('12.345.678/0001-90', 5, 2, 1, 0, 10, 8, 4, 2);

-- 5. Pessoa
INSERT INTO Pessoa (Id, nome, genero, tiposanguineo, cidade, estado, logradouro, dataNascimento, telefone, email, cpf) VALUES 
('P001', 'João Silva', 'MASCULINO', 'O+', 'São Paulo', 'SP', 'Rua A, 123', '1990-05-20', '11 99999-1111', 'joao@email.com', '111.111.111-11'),
('P002', 'Maria Santos', 'FEMININO', 'A-', 'Campinas', 'SP', 'Rua B, 456', '1985-10-10', '19 98888-2222', 'maria@email.com', '222.222.222-22'),
('P003', 'Dr. Roberto', 'MASCULINO', NULL, 'São Paulo', 'SP', 'Rua C, 789', '1975-03-15', '11 97777-3333', 'roberto@med.com', '333.333.333-33'),
('P004', 'Enf. Ana', 'FEMININO', NULL, 'São Paulo', 'SP', 'Rua D, 101', '1988-07-22', '11 96666-4444', 'ana@enf.com', '444.444.444-44'),
('P005', 'Bio. Carlos', 'MASCULINO', NULL, 'Campinas', 'SP', 'Rua E, 202', '1992-12-05', '19 95555-5555', 'carlos@bio.com', '555.555.555-55'),
('P006', 'Agente Lucas', 'MASCULINO', NULL, 'São Paulo', 'SP', 'Rua F, 303', '1995-08-30', '11 94444-6666', 'lucas@agente.com', '666.666.666-66');

-- 6. TipoPessoa
INSERT INTO TipoPessoa (Id, tipo) VALUES 
('P001', 'DOADOR'),
('P002', 'RECEPTOR'),
('P003', 'MEDICO'),
('P004', 'ENFERMEIRO'),
('P005', 'BIOMEDICO'),
('P006', 'AGENTE');

-- 7. Profissionais
INSERT INTO Medico (Id, CRM) VALUES ('P003', '123456');
INSERT INTO Enfermeiro (Id, COREN) VALUES ('P004', '654321');
INSERT INTO Biomedico (Id, CRBM) VALUES ('P005', '112233');
INSERT INTO AgenteMapeamento (Id) VALUES ('P006');

-- 8. Clientes
INSERT INTO Doador (Id, peso, altura) VALUES 
('P001', 80.5, 1.75),
('P002', 65.0, 1.65); -- Maria também pode ser doadora em outro contexto, mas aqui é Receptor primário

INSERT INTO Receptor (Id) VALUES 
('P002'),
('P001'); -- João pode ser receptor também

-- 9. Multivalued Attributes
INSERT INTO ISTDoador (Id, IST) VALUES 
('P001', 'Nenhuma');

INSERT INTO MotivoReceptor (Id, motivo) VALUES 
('P002', 'Cirurgia Cardíaca');

-- 10. Triagem
INSERT INTO Triagem (IdTriagem, Doador, DataHora, Enfermeiro, Valido, CentroColeta_CNPJ, CentroColeta_Codigo) VALUES 
('T001', 'P001', '2023-10-01 08:00:00', 'P004', TRUE, '11.222.333/0001-44', 'C001'),
('T002', 'P001', '2023-11-01 09:00:00', 'P004', TRUE, '11.222.333/0001-44', 'C001');

-- 11. BolsaSangue
INSERT INTO BolsaSangue (Codigo, VolumeDoado, TipoSangue, Valido, Triagem, Biomedico, Hemocentro, DataTestagem) VALUES 
('B001', 450, 'O+', TRUE, 'T001', 'P005', '98.765.432/0001-10', '2023-10-02'),
('B002', 460, 'O+', TRUE, 'T002', 'P005', '98.765.432/0001-10', '2023-11-02');

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
('55.666.777/0001-88', '2023-10-05 11:00:00', '98.765.432/0001-10', 0, 0, 10, 5, 0, 0, 0, 0, FALSE);

-- 15. Transferencia
INSERT INTO Transferencia (HemoOrigem, HemoDestino, DataHora, QntOPlus, QntOMinus, QntAPlus, QntAMinus, QntBPlus, QntBMinus, QntABPlus, QntABMinus, AceitaNegada) VALUES 
('98.765.432/0001-10', '98.765.432/0001-10', '2023-10-10 15:00:00', 2, 0, 0, 0, 0, 0, 0, 0, TRUE); -- Self transfer for example, or need another Hemocentro

-- 16. Usuarios
INSERT INTO Usuario (Login, Senha, Role) VALUES
('admin', 'admin', 'admin'),
('medico', '123', 'medico'),
('enfermeiro', '123', 'enfermeiro'),
('biomedico', '123', 'biomedico'),
('agente', '123', 'agente'),
('instituicao', '123', 'instituicao'),
('doador', '123', 'doador'),
('receptor', '123', 'receptor');
