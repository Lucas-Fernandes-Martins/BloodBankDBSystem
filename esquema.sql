------- CRIACAO DAS TABELAS

-- 1. InstituicaoSaude (Supertype)
CREATE TABLE InstituicaoSaude (
    CNPJ CHAR(18) PRIMARY KEY,
    nome VARCHAR(40) NOT NULL,
    cidade VARCHAR(40),
    estado VARCHAR(2),
    logradouro VARCHAR(100),
    CHECK (CNPJ ~ '^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$')
);

-- 2. Subtypes of InstituicaoSaude
CREATE TABLE Hospital (
    CNPJ CHAR(18) PRIMARY KEY,
    FOREIGN KEY (CNPJ) REFERENCES InstituicaoSaude(CNPJ) ON DELETE CASCADE
);

CREATE TABLE Hemocentro (
    CNPJ CHAR(18) PRIMARY KEY,
    FOREIGN KEY (CNPJ) REFERENCES InstituicaoSaude(CNPJ) ON DELETE CASCADE
);

CREATE TABLE CentroDeColeta (
    CNPJ CHAR(18),
    codigo VARCHAR(10),
    cidade VARCHAR(40),
    estado VARCHAR(2),
    logradouro VARCHAR(100),
    ativo BOOLEAN NOT NULL,
    dataAbertura DATE,
    dataFechamento DATE,
    PRIMARY KEY (CNPJ, codigo),
    FOREIGN KEY (CNPJ) REFERENCES InstituicaoSaude(CNPJ) ON DELETE CASCADE
);

-- 3. TipoInstituicao (Multivalued Attribute / Classification)
CREATE TABLE TipoInstituicao (
    CNPJ CHAR(18),
    tipo VARCHAR(20),
    PRIMARY KEY (CNPJ, tipo),
    FOREIGN KEY (CNPJ) REFERENCES InstituicaoSaude(CNPJ) ON DELETE CASCADE,
    CONSTRAINT CHK_TIPO CHECK (tipo IN ('CENTRO COLETA', 'BANCO DE SANGUE', 'HOSPITAL', 'HEMOCENTRO'))
);

-- 4. EstoqueSangue
CREATE TABLE EstoqueSangue (
    InstituicaoSaude CHAR(18) PRIMARY KEY,
    NumOMinus INTEGER,
    NumAMinus INTEGER,
    NumBMinus INTEGER,
    NumABMinus INTEGER,
    NumOPlus INTEGER,
    NumAPlus INTEGER,
    NumBPlus INTEGER,
    NumABPlus INTEGER,
    FOREIGN KEY (InstituicaoSaude) REFERENCES InstituicaoSaude(CNPJ) ON DELETE CASCADE
);

-- 5. Pessoa (Supertype)
CREATE TABLE Pessoa (
    Id VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(40) NOT NULL,
    genero VARCHAR(20),
    tiposanguineo CHAR(3),
    cidade VARCHAR(40),
    estado CHAR(2),
    logradouro VARCHAR(100),
    dataNascimento DATE NOT NULL,
    telefone CHAR(13),
    email VARCHAR(30),
    cpf CHAR(14) UNIQUE,
    CONSTRAINT CHK_GENERO CHECK (genero IN ('MASCULINO', 'FEMININO', 'OUTRO')),
    CONSTRAINT CHK_CPF CHECK (cpf ~ '^\d{3}\.\d{3}\.\d{3}-\d{2}$'),
    CONSTRAINT CHK_TELEFONE CHECK (telefone ~ '^\d{2} \d{5}-\d{4}$'),
    CONSTRAINT CHK_EMAIL CHECK (email LIKE '%_@_%._%'),
    CONSTRAINT CHK_TIPOSANGUINEO CHECK (tiposanguineo IN ('O-', 'A-', 'B-', 'AB-', 'O+', 'A+', 'B+', 'AB+'))
);

-- 6. TipoPessoa (Multivalued Attribute)
CREATE TABLE TipoPessoa (
    Id VARCHAR(10),
    tipo VARCHAR(20),
    PRIMARY KEY (Id, tipo),
    FOREIGN KEY (Id) REFERENCES Pessoa(Id) ON DELETE CASCADE
);

-- 7. Subtypes of Pessoa (Profesionais)
CREATE TABLE Biomedico (
    Id VARCHAR(10) PRIMARY KEY,
    CRBM VARCHAR(10) UNIQUE,
    FOREIGN KEY (Id) REFERENCES Pessoa(Id) ON DELETE CASCADE
);

CREATE TABLE Enfermeiro (
    Id VARCHAR(10) PRIMARY KEY,
    COREN VARCHAR(10) UNIQUE,
    FOREIGN KEY (Id) REFERENCES Pessoa(Id) ON DELETE CASCADE
);

CREATE TABLE Medico (
    Id VARCHAR(10) PRIMARY KEY,
    CRM VARCHAR(10) UNIQUE,
    FOREIGN KEY (Id) REFERENCES Pessoa(Id) ON DELETE CASCADE
);

CREATE TABLE AgenteMapeamento (
    Id VARCHAR(10) PRIMARY KEY,
    FOREIGN KEY (Id) REFERENCES Pessoa(Id) ON DELETE CASCADE
);

-- 8. Subtypes of Pessoa (Clients)
CREATE TABLE Doador (
    Id VARCHAR(10) PRIMARY KEY,
    peso DECIMAL(5,2),
    altura DECIMAL(3,2),
    FOREIGN KEY (Id) REFERENCES Pessoa(Id) ON DELETE CASCADE
);

CREATE TABLE Receptor (
    Id VARCHAR(10) PRIMARY KEY,
    FOREIGN KEY (Id) REFERENCES Pessoa(Id) ON DELETE CASCADE
);

-- 9. Multivalued Attributes for Clients
CREATE TABLE ISTDoador (
    Id VARCHAR(10),
    IST VARCHAR(50),
    PRIMARY KEY (Id, IST),
    FOREIGN KEY (Id) REFERENCES Doador(Id) ON DELETE CASCADE
);

CREATE TABLE MotivoReceptor (
    Id VARCHAR(10),
    motivo VARCHAR(100),
    PRIMARY KEY (Id, motivo),
    FOREIGN KEY (Id) REFERENCES Receptor(Id) ON DELETE CASCADE
);

-- 10. Triagem
CREATE TABLE Triagem (
    IdTriagem VARCHAR(10) PRIMARY KEY,
    Doador VARCHAR(10) NOT NULL,
    DataHora TIMESTAMP NOT NULL,
    Enfermeiro VARCHAR(10) NOT NULL,
    Valido BOOLEAN,
    CentroColeta_CNPJ CHAR(18) NOT NULL,
    CentroColeta_Codigo VARCHAR(10) NOT NULL,
    FOREIGN KEY (Doador) REFERENCES Doador(Id),
    FOREIGN KEY (Enfermeiro) REFERENCES Enfermeiro(Id),
    FOREIGN KEY (CentroColeta_CNPJ, CentroColeta_Codigo) REFERENCES CentroDeColeta(CNPJ, codigo)
);

-- 11. BolsaSangue
CREATE TABLE BolsaSangue (
    Codigo VARCHAR(20) PRIMARY KEY,
    VolumeDoado INTEGER,
    TipoSangue CHAR(3),
    Valido BOOLEAN,
    Triagem VARCHAR(10) NOT NULL,
    Biomedico VARCHAR(10),
    Hemocentro VARCHAR(40),
    DataTestagem DATE,
    FOREIGN KEY (Triagem) REFERENCES Triagem(IdTriagem),
    FOREIGN KEY (Biomedico) REFERENCES Biomedico(Id),
    FOREIGN KEY (Hemocentro) REFERENCES Hemocentro(CNPJ)
);

-- 12. Procedimento
CREATE TABLE Procedimento (
    Receptor VARCHAR(10),
    DataHora TIMESTAMP,
    Medico VARCHAR(10),
    Hospital VARCHAR(40),
    PRIMARY KEY (Receptor, DataHora, Medico, Hospital),
    FOREIGN KEY (Receptor) REFERENCES Receptor(Id),
    FOREIGN KEY (Medico) REFERENCES Medico(Id),
    FOREIGN KEY (Hospital) REFERENCES Hospital(CNPJ)
);

-- 13. Pesquisa
CREATE TABLE Pesquisa (
    Doador VARCHAR(10),
    DataHora TIMESTAMP,
    AgenteMapeamento VARCHAR(10),
    Doou BOOLEAN,
    PrimeiraDoacao BOOLEAN,
    DoariaNovamente BOOLEAN,
    Feedback VARCHAR(255),
    PRIMARY KEY (Doador, DataHora, AgenteMapeamento),
    FOREIGN KEY (Doador) REFERENCES Doador(Id),
    FOREIGN KEY (AgenteMapeamento) REFERENCES AgenteMapeamento(Id)
);

-- 14. Solicitacao
CREATE TABLE Solicitacao (
    Hospital VARCHAR(40),
    DataHora TIMESTAMP,
    Hemocentro VARCHAR(40),
    QntOPlus INTEGER,
    QntOMinus INTEGER,
    QntAPlus INTEGER,
    QntAMinus INTEGER,
    QntBPlus INTEGER,
    QntBMinus INTEGER,
    QntABPlus INTEGER,
    QntABMinus INTEGER,
    AceitaNegada BOOLEAN,
    PRIMARY KEY (Hospital, DataHora, Hemocentro),
    FOREIGN KEY (Hospital) REFERENCES Hospital(CNPJ),
    FOREIGN KEY (Hemocentro) REFERENCES Hemocentro(CNPJ)
);

-- 15. Transferencia
CREATE TABLE Transferencia (
    HemoOrigem VARCHAR(40),
    HemoDestino VARCHAR(40),
    DataHora TIMESTAMP,
    QntOPlus INTEGER,
    QntOMinus INTEGER,
    QntAPlus INTEGER,
    QntAMinus INTEGER,
    QntBPlus INTEGER,
    QntBMinus INTEGER,
    QntABPlus INTEGER,
    QntABMinus INTEGER,
    AceitaNegada BOOLEAN,
    PRIMARY KEY (HemoOrigem, HemoDestino, DataHora),
    FOREIGN KEY (HemoOrigem) REFERENCES Hemocentro(CNPJ),
    FOREIGN KEY (HemoDestino) REFERENCES Hemocentro(CNPJ)
);
