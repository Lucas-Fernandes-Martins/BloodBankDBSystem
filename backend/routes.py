from fastapi import APIRouter, HTTPException, status
from database import get_db_connection, read_sql_file
from psycopg.rows import dict_row
import random
import string

router = APIRouter()

def generate_id():
    """Gera um ID aleatório para Pessoa, Triagem e BolsaSangue"""
    return 'P' + ''.join(random.choices(string.digits, k=4))

# ========================================
# ENDPOINTS DE DOADOR
# ========================================

@router.post("/doador", status_code=status.HTTP_201_CREATED)
def create_doador(doador: dict):
    """Cria um novo doador (Doador) com dados completos de Pessoa"""
    try:
        # Validação manual para campos obrigatórios
        required_fields = ['nome', 'genero', 'dataNascimento', 'peso', 'altura']
        for field in required_fields:
            if field not in doador or not doador[field]:
                raise HTTPException(status_code=400, detail=f"Campo '{field}' é obrigatório")
        
        # Valida se peso e altura são positivos
        if doador['peso'] <= 0 or doador['altura'] <= 0:
            raise HTTPException(status_code=400, detail="peso e altura devem ser maiores que 0")
        
        new_id = generate_id()
        
        # Limpeza e Formatação de Dados
        formatted_telefone = doador.get('telefone')
        if formatted_telefone and len(formatted_telefone) == 11 and formatted_telefone.isdigit():
            # Formato: 11999998888 -> 11 99999-8888
            formatted_telefone = f"{formatted_telefone[:2]} {formatted_telefone[2:7]}-{formatted_telefone[7:]}"
        
        clean_estado = doador.get('estado', '').upper() if doador.get('estado') else None
        clean_tiposanguineo = doador.get('tiposanguineo', '').strip() if doador.get('tiposanguineo') else None

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # 1. Inserir em Pessoa
                sql_pessoa = read_sql_file('sql/doador/insert_pessoa.sql')
                cur.execute(sql_pessoa, (
                    new_id, doador['nome'], doador['genero'], clean_tiposanguineo, 
                    doador.get('cidade'), clean_estado, doador.get('logradouro'), 
                    doador['dataNascimento'], formatted_telefone, doador.get('email'), 
                    doador.get('cpf')
                ))

                # 2. Inserir em TipoPessoa
                sql_tipopessoa = read_sql_file('sql/doador/insert_tipopessoa.sql')
                cur.execute(sql_tipopessoa, (new_id, 'DOADOR'))

                # 3. Inserir em Doador
                sql_doador = read_sql_file('sql/doador/insert_doador.sql')
                cur.execute(sql_doador, (new_id, doador['peso'], doador['altura']))
                
                conn.commit()
                return {"message": "Doador cadastrado com sucesso!", "id": new_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========================================
# ENDPOINTS DE AGENTE DE MAPEAMENTO
# ========================================

@router.post("/pesquisa", status_code=status.HTTP_201_CREATED)
def create_pesquisa(pesquisa: dict):
    """Cria um registro de pesquisa"""
    try:
        # Validação manual
        required_fields = ['doador_id', 'agente_id', 'doou', 'primeira_doacao', 'doaria_novamente']
        for field in required_fields:
            if field not in pesquisa:
                raise HTTPException(status_code=400, detail=f"Campo '{field}' é obrigatório")
        
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                sql = read_sql_file('sql/agente/insert_pesquisa.sql')
                cur.execute(sql, (
                    pesquisa['doador_id'], pesquisa['agente_id'], pesquisa['doou'], 
                    pesquisa['primeira_doacao'], pesquisa['doaria_novamente'], 
                    pesquisa.get('feedback')
                ))
                conn.commit()
                return {"message": "Pesquisa registrada com sucesso!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========================================
# ENDPOINTS DE ENFERMEIRO
# ========================================

@router.post("/triagem", status_code=status.HTTP_201_CREATED)
def create_triagem(triagem: dict):
    """Cria um registro de triagem"""
    try:
        # Validação manual
        required_fields = ['doador_id', 'enfermeiro_id', 'centro_coleta_cnpj', 'centro_coleta_codigo', 'valido']
        for field in required_fields:
            if field not in triagem:
                raise HTTPException(status_code=400, detail=f"Campo '{field}' é obrigatório")
        
        new_id = generate_id()
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                sql = read_sql_file('sql/enfermeiro/insert_triagem.sql')
                cur.execute(sql, (
                    new_id, triagem['doador_id'], triagem['enfermeiro_id'], 
                    triagem['valido'], triagem['centro_coleta_cnpj'], 
                    triagem['centro_coleta_codigo']
                ))
                conn.commit()
                return {"message": "Triagem registrada com sucesso!", "id": new_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========================================
# ENDPOINTS DE BIOMÉDICO
# ========================================

@router.post("/bolsa", status_code=status.HTTP_201_CREATED)
def create_bolsa(bolsa: dict):
    """Cria um registro de bolsa de sangue"""
    try:
        # Validação manual
        required_fields = ['volume_doado', 'tipo_sangue', 'valido', 'triagem_id', 'biomedico_id', 'hemocentro_cnpj', 'data_testagem']
        for field in required_fields:
            if field not in bolsa:
                raise HTTPException(status_code=400, detail=f"Campo '{field}' é obrigatório")
        
        new_code = generate_id()
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                sql = read_sql_file('sql/biomedico/insert_bolsa.sql')
                cur.execute(sql, (
                    new_code, bolsa['volume_doado'], bolsa['tipo_sangue'], 
                    bolsa['valido'], bolsa['triagem_id'], bolsa['biomedico_id'], 
                    bolsa['hemocentro_cnpj'], bolsa['data_testagem']
                ))
                conn.commit()
                return {"message": "Bolsa de sangue registrada com sucesso!", "codigo": new_code}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========================================
# ENDPOINTS DE MÉDICO
# ========================================

@router.post("/procedimento", status_code=status.HTTP_201_CREATED)
def create_procedimento(proc: dict):
    """Cria um registro de procedimento médico"""
    try:
        # Validação manual
        required_fields = ['receptor_id', 'medico_id', 'hospital_cnpj']
        for field in required_fields:
            if field not in proc:
                raise HTTPException(status_code=400, detail=f"Campo '{field}' é obrigatório")
        
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                sql = read_sql_file('sql/medico/insert_procedimento.sql')
                cur.execute(sql, (proc['receptor_id'], proc['medico_id'], proc['hospital_cnpj']))
                conn.commit()
                return {"message": "Procedimento registrado com sucesso!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========================================
# ENDPOINTS DE SOLICITAÇÃO
# ========================================

@router.post("/solicitacao", status_code=status.HTTP_201_CREATED)
def create_solicitacao(sol: dict):
    """Cria uma solicitação de sangue do hospital para o hemocentro"""
    try:
        # Validação manual
        required_fields = ['hospital_cnpj', 'hemocentro_cnpj']
        for field in required_fields:
            if field not in sol:
                raise HTTPException(status_code=400, detail=f"Campo '{field}' é obrigatório")
        
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                sql = read_sql_file('sql/solicitacao/insert_solicitacao.sql')
                cur.execute(sql, (
                    sol['hospital_cnpj'], sol['hemocentro_cnpj'], 
                    sol.get('qnt_oplus', 0), sol.get('qnt_ominus', 0), 
                    sol.get('qnt_aplus', 0), sol.get('qnt_aminus', 0), 
                    sol.get('qnt_bplus', 0), sol.get('qnt_bminus', 0), 
                    sol.get('qnt_abplus', 0), sol.get('qnt_abminus', 0), 
                    sol.get('aceita_negada', False)
                ))
                conn.commit()
                return {"message": "Solicitação registrada com sucesso!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========================================
# ENDPOINTS DE OPÇÕES (para dropdowns)
# ========================================

@router.get("/options/doadores")
def get_options_doadores():
    """Obtém todos os doadores para opções de dropdown"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/doador/list_doadores.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/receptores")
def get_options_receptores():
    """Obtém todos os receptores de sangue para opções de dropdown"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/options/list_receptores.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/agentes")
def get_options_agentes():
    """Obtém todos os agentes de mapeamento para opções de dropdown"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/agente/list_agentes.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/medicos")
def get_options_medicos():
    """Obtém todos os médicos para opções de dropdown"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/medico/list_medicos.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/enfermeiros")
def get_options_enfermeiros():
    """Obtém todos os enfermeiros para opções de dropdown"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/enfermeiro/list_enfermeiros.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/biomedicos")
def get_options_biomedicos():
    """Obtém todos os biomédicos para opções de dropdown"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/biomedico/list_biomedicos.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/hospitais")
def get_options_hospitais():
    """Obtém todos os hospitais para opções de dropdown"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/options/list_hospitais.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/hemocentros")
def get_options_hemocentros():
    """Obtém todos os hemocentros para opções de dropdown"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/options/list_hemocentros.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/centros-coleta")
def get_options_centros_coleta():
    """Obtém todos os centros de coleta para opções de dropdown"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/options/list_centros_coleta.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/triagens")
def get_options_triagens():
    """Obtém triagens válidas para criação de bolsas de sangue"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/enfermeiro/list_triagens.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========================================
# ENDPOINTS DE MÉTRICAS
# ========================================

@router.get("/consultas/estoque")
def get_estoque(hemocentro_cnpj: str = None):
    """Obtém o estoque de sangue, opcionalmente filtrado por CNPJ do hemocentro"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                if hemocentro_cnpj:
                    sql = read_sql_file('sql/metrics/estoque_filtrado.sql')
                    cur.execute(sql, [hemocentro_cnpj])
                else:
                    sql = read_sql_file('sql/metrics/estoque.sql')
                    cur.execute(sql)
                results = cur.fetchall()
                return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/division/hospitals-all-hemocentros")
def get_hospitals_all_hemocentros():
    """Consulta de Divisão: Encontra hospitais que solicitaram de TODOS os hemocentros"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/metrics/hospitals_all_hemocentros.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/blood-stock")
def get_metrics_blood_stock():
    """Consulta Group By: Conta bolsas de sangue válidas por tipo"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/metrics/blood_stock_by_type.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/solicitations-by-hospital")
def get_metrics_solicitations_by_hospital():
    """Consulta Left Join: Lista todos os hospitais e contagem de solicitações"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/metrics/solicitations_by_hospital.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/map-data")
def get_metrics_map_data():
    """Obtém instituições com coordenadas para visualização no mapa"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/metrics/map_data.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/procedures-by-doctor")
def get_metrics_procedures_by_doctor():
    """Consulta de Múltiplos Joins: Conta procedimentos por médico"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/metrics/procedures_by_doctor.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/relatorios/doadores-anonimos")
def get_doadores_anonimos():
    """Consulta de Anonimização: Obtém doadores com dados pessoais mascarados"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/metrics/doadores_anonimos.sql')
                cur.execute(sql)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========================================
# ENDPOINTS DE AUTENTICAÇÃO
# ========================================

@router.post("/login")
def login(credentials: dict):
    """Autentica usuário por login e senha"""
    try:
        # Validação manual
        if 'login' not in credentials or 'senha' not in credentials:
            raise HTTPException(status_code=400, detail="login e senha são obrigatórios")
        
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = read_sql_file('sql/auth/login.sql')
                cur.execute(sql, (credentials['login'], credentials['senha']))
                user = cur.fetchone()
                if user:
                    return {"message": "Login realizado com sucesso", "role": user['role']}
                else:
                    raise HTTPException(status_code=401, detail="Credenciais inválidas")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========================================
# ENDPOINTS DE ADMIN
# ========================================

def check_permission(role: str, permission_name: str):
    """Verifica se o papel (role) tem permissão específica (RBAC)"""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            sql = read_sql_file('sql/auth/check_permission.sql')
            cur.execute(sql, (role, permission_name))
            if not cur.fetchone():
                raise HTTPException(status_code=403, detail=f"Papel '{role}' não tem permissão '{permission_name}'")

@router.post("/instituicao")
def create_instituicao(inst: dict):
    """Cria uma instituição de saúde com integridade de transação"""
    try:
        # Validação manual
        required_fields = ['CNPJ', 'nome', 'cidade', 'estado', 'logradouro', 'latitude', 'longitude', 'tipo', 'user_role']
        for field in required_fields:
            if field not in inst:
                raise HTTPException(status_code=400, detail=f"Campo '{field}' é obrigatório")
        
        # 1. Verificação RBAC
        check_permission(inst['user_role'], 'CADASTRAR_INSTITUICAO')

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # 2. Integridade de Transação: Inserir em Supertipo
                sql_instituicao = read_sql_file('sql/admin/insert_instituicao_saude.sql')
                cur.execute(sql_instituicao, (
                    inst['CNPJ'], inst['nome'], inst['cidade'], inst['estado'], 
                    inst['logradouro'], inst['latitude'], inst['longitude']
                ))

                # Inserir em Subtipo baseado no tipo
                if inst['tipo'] == 'HOSPITAL':
                    sql_hospital = read_sql_file('sql/admin/insert_hospital.sql')
                    cur.execute(sql_hospital, (inst['CNPJ'],))
                elif inst['tipo'] == 'HEMOCENTRO':
                    sql_hemocentro = read_sql_file('sql/admin/insert_hemocentro.sql')
                    cur.execute(sql_hemocentro, (inst['CNPJ'],))
                
                # Inserir em TipoInstituicao (Classificação)
                sql_tipo = read_sql_file('sql/admin/insert_tipo_instituicao.sql')
                cur.execute(sql_tipo, (inst['CNPJ'], inst['tipo']))
                
                # 3. Commit apenas se todos os passos tiverem sucesso
                conn.commit()
                return {"message": "Instituição criada com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========================================
# ENDPOINTS DE DEBUG
# ========================================

@router.get("/debug/tables")
def get_all_tables():
    """Obtém lista de todas as tabelas do banco de dados"""
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
    """Obtém conteúdo de uma tabela específica (com validação para prevenir injeção de SQL)"""
    try:
        # Valida nome da tabela para prevenir Injeção de SQL
        allowed_tables = [
            "instituicaosaude", "hospital", "hemocentro", "centrodecoleta", "tipoinstituicao", 
            "estoquesangue", "pessoa", "tipopessoa", "biomedico", "enfermeiro", "medico", 
            "agentemapeamento", "doador", "receptor", "istdoador", "motivoreceptor", 
            "triagem", "bolsasangue", "procedimento", "pesquisa", "solicitacao", "transferencia"
        ]
        if table_name.lower() not in allowed_tables:
            raise HTTPException(status_code=400, detail="Nome de tabela inválido")

        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(f"SELECT * FROM {table_name} LIMIT 100")
                return cur.fetchall()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
