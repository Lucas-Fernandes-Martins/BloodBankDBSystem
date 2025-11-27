from fastapi import APIRouter, HTTPException, status
from database import get_db_connection
from models import DoadorCreate, EstoqueQuery, PesquisaCreate, ProcedimentoCreate, TriagemCreate, BolsaSangueCreate, SolicitacaoCreate
from psycopg.rows import dict_row

router = APIRouter()

import random
import string

def generate_id():
    return 'P' + ''.join(random.choices(string.digits, k=4))

@router.post("/doador", status_code=status.HTTP_201_CREATED)
def create_doador(doador: DoadorCreate):
    try:
        new_id = generate_id()
        
        # Data Cleaning & Formatting
        formatted_telefone = doador.telefone
        if doador.telefone and len(doador.telefone) == 11 and doador.telefone.isdigit():
            # Format: 11999998888 -> 11 99999-8888
            formatted_telefone = f"{doador.telefone[:2]} {doador.telefone[2:7]}-{doador.telefone[7:]}"
            
        clean_estado = doador.estado.upper() if doador.estado else None
        clean_tiposanguineo = doador.tiposanguineo.strip() if doador.tiposanguineo else None

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # 1. Insert into Pessoa
                cur.execute("""
                    INSERT INTO Pessoa (Id, nome, genero, tiposanguineo, cidade, estado, logradouro, dataNascimento, telefone, email, cpf)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    new_id, doador.nome, doador.genero, clean_tiposanguineo, doador.cidade, clean_estado, 
                    doador.logradouro, doador.dataNascimento, formatted_telefone, doador.email, doador.cpf
                ))

                # 2. Insert into TipoPessoa
                cur.execute("""
                    INSERT INTO TipoPessoa (Id, tipo) VALUES (%s, 'DOADOR')
                """, (new_id,))

                # 3. Insert into Doador
                cur.execute("""
                    INSERT INTO Doador (Id, peso, altura) VALUES (%s, %s, %s)
                """, (new_id, doador.peso, doador.altura))
                
                conn.commit()
                return {"message": "Doador cadastrado com sucesso!", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/consultas/estoque")
def get_estoque(hemocentro_cnpj: str = None):
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                query = """
                    SELECT ISaude.nome, E.*
                    FROM EstoqueSangue E
                    JOIN InstituicaoSaude ISaude ON E.InstituicaoSaude = ISaude.CNPJ
                """
                params = []
                
                if hemocentro_cnpj:
                    query += " WHERE E.InstituicaoSaude = %s"
                    params.append(hemocentro_cnpj)
                
                cur.execute(query, params)
                results = cur.fetchall()
                return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/division/hospitals-all-hemocentros")
def get_hospitals_all_hemocentros():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # Division Query: Find hospitals that have solicited from ALL hemocentros
                query = """
                    SELECT I.nome, H.CNPJ
                    FROM Hospital H
                    JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ
                    WHERE NOT EXISTS (
                        (SELECT CNPJ FROM Hemocentro)
                        EXCEPT
                        (SELECT Hemocentro FROM Solicitacao WHERE Hospital = H.CNPJ)
                    );
                """
                cur.execute(query)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pesquisa", status_code=status.HTTP_201_CREATED)
def create_pesquisa(pesquisa: PesquisaCreate):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Pesquisa (Doador, DataHora, AgenteMapeamento, Doou, PrimeiraDoacao, DoariaNovamente, Feedback)
                    VALUES (%s, NOW(), %s, %s, %s, %s, %s)
                """, (pesquisa.doador_id, pesquisa.agente_id, pesquisa.doou, pesquisa.primeira_doacao, pesquisa.doaria_novamente, pesquisa.feedback))
                conn.commit()
                return {"message": "Pesquisa registrada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/procedimento", status_code=status.HTTP_201_CREATED)
def create_procedimento(proc: ProcedimentoCreate):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Procedimento (Receptor, DataHora, Medico, Hospital)
                    VALUES (%s, NOW(), %s, %s)
                """, (proc.receptor_id, proc.medico_id, proc.hospital_cnpj))
                conn.commit()
                return {"message": "Procedimento registrado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/triagem", status_code=status.HTTP_201_CREATED)
def create_triagem(triagem: TriagemCreate):
    try:
        new_id = generate_id() # Using generic ID generator for Triagem ID as well for simplicity, or we can make a specific one
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Triagem (IdTriagem, Doador, DataHora, Enfermeiro, Valido, CentroColeta_CNPJ, CentroColeta_Codigo)
                    VALUES (%s, %s, NOW(), %s, %s, %s, %s)
                """, (new_id, triagem.doador_id, triagem.enfermeiro_id, triagem.valido, triagem.centro_coleta_cnpj, triagem.centro_coleta_codigo))
                conn.commit()
                return {"message": "Triagem registrada com sucesso!", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bolsa", status_code=status.HTTP_201_CREATED)
def create_bolsa(bolsa: BolsaSangueCreate):
    try:
        new_code = generate_id() # Using generic ID for bag code
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO BolsaSangue (Codigo, VolumeDoado, TipoSangue, Valido, Triagem, Biomedico, Hemocentro, DataTestagem)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (new_code, bolsa.volume_doado, bolsa.tipo_sangue, bolsa.valido, bolsa.triagem_id, bolsa.biomedico_id, bolsa.hemocentro_cnpj, bolsa.data_testagem))
                conn.commit()
                return {"message": "Bolsa de sangue registrada com sucesso!", "codigo": new_code}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/solicitacao", status_code=status.HTTP_201_CREATED)
def create_solicitacao(sol: SolicitacaoCreate):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Solicitacao (Hospital, DataHora, Hemocentro, QntOPlus, QntOMinus, QntAPlus, QntAMinus, QntBPlus, QntBMinus, QntABPlus, QntABMinus, AceitaNegada)
                    VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (sol.hospital_cnpj, sol.hemocentro_cnpj, sol.qnt_oplus, sol.qnt_ominus, sol.qnt_aplus, sol.qnt_aminus, sol.qnt_bplus, sol.qnt_bminus, sol.qnt_abplus, sol.qnt_abminus, sol.aceita_negada))
                conn.commit()
                return {"message": "Solicitação registrada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Options Endpoints for Dropdowns ---

@router.get("/options/doadores")
def get_options_doadores():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT P.Id, P.nome, P.cpf FROM Doador D JOIN Pessoa P ON D.Id = P.Id")
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/receptores")
def get_options_receptores():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT P.Id, P.nome, P.cpf FROM Receptor R JOIN Pessoa P ON R.Id = P.Id")
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/agentes")
def get_options_agentes():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT P.Id, P.nome FROM AgenteMapeamento A JOIN Pessoa P ON A.Id = P.Id")
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/medicos")
def get_options_medicos():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT P.Id, P.nome, M.CRM FROM Medico M JOIN Pessoa P ON M.Id = P.Id")
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/enfermeiros")
def get_options_enfermeiros():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT P.Id, P.nome, E.COREN FROM Enfermeiro E JOIN Pessoa P ON E.Id = P.Id")
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/biomedicos")
def get_options_biomedicos():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT P.Id, P.nome, B.CRBM FROM Biomedico B JOIN Pessoa P ON B.Id = P.Id")
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/hospitais")
def get_options_hospitais():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT H.CNPJ, I.nome FROM Hospital H JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ")
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/hemocentros")
def get_options_hemocentros():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT H.CNPJ, I.nome FROM Hemocentro H JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ")
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/centros-coleta")
def get_options_centros_coleta():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT C.CNPJ, C.codigo, I.nome FROM CentroDeColeta C JOIN InstituicaoSaude I ON C.CNPJ = I.CNPJ")
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/triagens")
def get_options_triagens():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # Only valid triages that haven't been used yet (optional logic, but let's just list valid ones)
                cur.execute("""
                    SELECT T.IdTriagem, P.nome as doador_nome, T.DataHora 
                    FROM Triagem T 
                    JOIN Doador D ON T.Doador = D.Id 
                    JOIN Pessoa P ON D.Id = P.Id
                    WHERE T.Valido = TRUE
                """)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Debug Endpoints ---

@router.get("/debug/tables")
def get_all_tables():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                return [row[0] for row in cur.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/debug/table/{table_name}")
def get_table_content(table_name: str):
    try:
        # Validate table name to prevent SQL Injection (basic check)
        allowed_tables = [
            "instituicosaude", "hospital", "hemocentro", "centrodecoleta", "tipoinstituicao", 
            "estoquesangue", "pessoa", "tipopessoa", "biomedico", "enfermeiro", "medico", 
            "agentemapeamento", "doador", "receptor", "istdoador", "motivoreceptor", 
            "triagem", "bolsasangue", "procedimento", "pesquisa", "solicitacao", "transferencia"
        ]
        if table_name.lower() not in allowed_tables:
             raise HTTPException(status_code=400, detail="Invalid table name")

        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(f"SELECT * FROM {table_name} LIMIT 100")
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Metrics Endpoints ---

@router.get("/metrics/blood-stock")
def get_metrics_blood_stock():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # Group By Query: Count valid blood bags by type
                cur.execute("""
                    SELECT TipoSangue, COUNT(*) as total
                    FROM BolsaSangue
                    WHERE Valido = TRUE
                    GROUP BY TipoSangue
                    ORDER BY total DESC
                """)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/solicitations-by-hospital")
def get_metrics_solicitations_by_hospital():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # Left Join Query: List all hospitals and count of solicitations (even if 0)
                cur.execute("""
                    SELECT I.nome, COUNT(S.Hospital) as total_solicitacoes
                    FROM Hospital H
                    JOIN InstituicaoSaude I ON H.CNPJ = I.CNPJ
                    LEFT JOIN Solicitacao S ON H.CNPJ = S.Hospital
                    GROUP BY H.CNPJ, I.nome
                    ORDER BY total_solicitacoes DESC
                """)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Authentication Endpoints ---

from pydantic import BaseModel

class LoginRequest(BaseModel):
    login: str
    senha: str

@router.post("/login")
def login(credentials: LoginRequest):
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT Role FROM Usuario WHERE Login = %s AND Senha = %s", (credentials.login, credentials.senha))
                user = cur.fetchone()
                if user:
                    return {"message": "Login successful", "role": user['role']}
                else:
                    raise HTTPException(status_code=401, detail="Invalid credentials")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/map-data")
def get_metrics_map_data():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # Get all institutions with coordinates and their types
                cur.execute("""
                    SELECT 
                        I.CNPJ, 
                        I.nome, 
                        I.Latitude, 
                        I.Longitude,
                        STRING_AGG(T.tipo, ', ') as tipos
                    FROM InstituicaoSaude I
                    LEFT JOIN TipoInstituicao T ON I.CNPJ = T.CNPJ
                    WHERE I.Latitude IS NOT NULL AND I.Longitude IS NOT NULL
                    GROUP BY I.CNPJ, I.nome, I.Latitude, I.Longitude
                """)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/procedures-by-doctor")
def get_metrics_procedures_by_doctor():
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # Multiple Joins Query: Count procedures per doctor
                cur.execute("""
                    SELECT P.nome, COUNT(Pr.Medico) as total_procedimentos
                    FROM Medico M
                    JOIN Pessoa P ON M.Id = P.Id
                    JOIN Procedimento Pr ON M.Id = Pr.Medico
                    GROUP BY M.Id, P.nome
                    ORDER BY total_procedimentos DESC
                """)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
