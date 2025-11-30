import os
import sys
import random
from database import get_db_connection
from psycopg.rows import dict_row

CONSULTAS_FILE = 'consultas.sql'

def get_input(prompt, default=None):
    """Helper to get input with a default value."""
    if default:
        user_input = input(f"{prompt} (padrão: {default}): ")
        return user_input.strip() if user_input.strip() else default
    return input(f"{prompt}: ")

def load_queries(filepath):
    """Parses the SQL file and returns a dictionary of {name: sql}."""
    queries = {}
    current_name = None
    current_sql = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('-- name:'):
                    if current_name:
                        queries[current_name] = '\n'.join(current_sql).strip()
                    current_name = line.split(':', 1)[1].strip()
                    current_sql = []
                elif current_name:
                    current_sql.append(line)
            
            if current_name:
                queries[current_name] = '\n'.join(current_sql).strip()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado.")
        sys.exit(1)
        
    return queries

def execute_query(query_name, sql, params=None, fetch_results=True):
    """Executes a SQL query and returns results or prints them."""
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(sql, params)
                if fetch_results:
                    results = cur.fetchall()
                    return results
                conn.commit()
                return None
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return None

def print_results(results):
    if not results:
        print("Nenhum resultado encontrado.")
        return

    headers = results[0].keys()
    print(" | ".join(headers))
    print("-" * (len(" | ".join(headers))))
    
    for row in results:
        values = [str(val) for val in row.values()]
        print(" | ".join(values))

def login(queries):
    print("\n=== Login ===")
    username = input("Usuário: ")
    password = input("Senha: ")
    
    results = execute_query('login', queries['login'], (username, password))
    if results:
        return results[0] # Returns dict with 'role' and 'pessoaid'
    else:
        print("Credenciais inválidas.")
        return None

def generate_id():
    return f"P{random.randint(1000, 9999)}"

def register_user(queries):
    print("\n=== Registrar Novo Usuário ===")
    nome = get_input("Nome", "Novo Usuário")
    cpf = get_input("CPF", "000.000.000-00")
    data_nascimento = get_input("Data Nascimento (AAAA-MM-DD)", "2000-01-01")
    login_user = get_input("Login", "novo_user")
    senha = get_input("Senha", "123")
    role = get_input("Função (medico, enfermeiro, biomedico, agente, doador, admin)", "doador").lower()
    
    new_id = generate_id()
    
    try:
        # 1. Insert Pessoa
        execute_query('insert_pessoa', queries['insert_pessoa'], (
            new_id, nome, 'OUTRO', None, None, None, None, data_nascimento, None, None, cpf
        ), fetch_results=False)
        
        # 2. Insert TipoPessoa
        execute_query('insert_tipopessoa', queries['insert_tipopessoa'], (new_id, role.upper()), fetch_results=False)
        
        # 3. Insert Specific Role Data
        if role == 'medico':
            crm = get_input("CRM", "000000")
            execute_query('insert_medico', queries['insert_medico'], (new_id, crm), fetch_results=False)
        elif role == 'enfermeiro':
            coren = get_input("COREN", "000000")
            execute_query('insert_enfermeiro', queries['insert_enfermeiro'], (new_id, coren), fetch_results=False)
        elif role == 'biomedico':
            crbm = get_input("CRBM", "000000")
            execute_query('insert_biomedico', queries['insert_biomedico'], (new_id, crbm), fetch_results=False)
        elif role == 'agente':
            execute_query('insert_agente', queries['insert_agente'], (new_id,), fetch_results=False)
        elif role == 'doador':
             peso = get_input("Peso", "70.0")
             altura = get_input("Altura", "1.75")
             execute_query('insert_doador', queries['insert_doador'], (new_id, peso, altura), fetch_results=False)

        # 4. Insert Usuario
        execute_query('insert_usuario', queries['insert_usuario'], (login_user, senha, role, new_id), fetch_results=False)
        
        print(f"Usuário {login_user} registrado com sucesso!")
        
    except Exception as e:
        print(f"Falha no registro: {e}")
def run_estoque_filtrado(queries, user):
    cnpj = get_input("CNPJ", "98.765.432/0001-10")
    results = execute_query('estoque_filtrado', queries['estoque_filtrado'], (cnpj,))
    print_results(results)

def run_stock_by_city(queries, user):
    city = get_input("Cidade (ex: São Paulo)", "São Paulo")
    results = execute_query('stock_by_city', queries['stock_by_city'], (f"%{city}%",))
    print_results(results)

def run_attendance_trends(queries, user):
    role = user['role']
    if role == 'medico':
        medico_id = user['pessoaid']
        print(f"Usando ID do Médico logado: {medico_id}")
    else:
        medico_id = get_input("ID do Médico", "P003")
    receptor_id = get_input("ID do Receptor", "P002")
    results = execute_query('attendance_trends', queries['attendance_trends'], (medico_id, receptor_id))
    print_results(results)

def run_donations_per_month(queries, user):
    centro_cnpj = get_input("CNPJ do Centro de Coleta", "11.222.333/0001-44")
    results = execute_query('donations_per_month', queries['donations_per_month'], (centro_cnpj,))
    print_results(results)

def run_receptors_by_blood_type(queries, user):
    blood_type = get_input("Tipo Sanguíneo do Doador (ex: O+)", "O+")
    results = execute_query('receptors_by_blood_type', queries['receptors_by_blood_type'], (blood_type, blood_type, blood_type, blood_type, blood_type, blood_type, blood_type, blood_type))
    print_results(results)

def run_donor_history(queries, user):
    doador_id = get_input("ID do Doador", "P001")
    results = execute_query('donor_history', queries['donor_history'], (doador_id,))
    print_results(results)

def run_testing_effectiveness(queries, user):
    role = user['role']
    if role == 'biomedico':
        biomedico_id = user['pessoaid']
        print(f"Usando ID do Biomédico logado: {biomedico_id}")
    else:
        biomedico_id = get_input("ID do Biomédico", "P005")
    results = execute_query('testing_effectiveness', queries['testing_effectiveness'], (biomedico_id,))
    print_results(results)

def run_solicitations_fulfilled(queries, user):
    hospital_cnpj = get_input("CNPJ do Hospital", "12.345.678/0001-90")
    results = execute_query('solicitations_fulfilled', queries['solicitations_fulfilled'], (hospital_cnpj,))
    print_results(results)

def run_stock_turnover(queries, user):
    hemocentro_cnpj = get_input("CNPJ do Hemocentro", "98.765.432/0001-10")
    results = execute_query('stock_turnover', queries['stock_turnover'], (hemocentro_cnpj,))
    print_results(results)

def run_campaign_analysis(queries, user):
    start_date = get_input("Data Início (AAAA-MM-DD)", "2023-01-01")
    end_date = get_input("Data Fim (AAAA-MM-DD)", "2023-12-31")
    results = execute_query('campaign_analysis', queries['campaign_analysis'], (start_date, end_date))
    print_results(results)

def run_simple_query(query_name):
    def _run(queries, user):
        results = execute_query(query_name, queries[query_name])
        print_results(results)
    return _run

def register_user_wrapper(queries, user):
    register_user(queries)
def main():
    queries = load_queries(CONSULTAS_FILE)
    
    while True:
        user = login(queries)
        if not user:
            continue
            
        role = user['role']
        print(f"\nBem-vindo, {role}!")
        
        while True:
            print(f"\n=== Menu {role.capitalize()} ===")
            
            options = []
            if role == 'admin' or role == 'instituicao':
                options = [
                    ('Registrar Usuário', register_user_wrapper),
                    ('Listar Doadores', run_simple_query('list_doadores')),
                    ('Listar Médicos', run_simple_query('list_medicos')),
                    ('Ver Estoque', run_simple_query('estoque')),
                    ('Métricas: Estoque Total por Tipo Sanguíneo', run_simple_query('blood_stock_by_type')),
                    ('Métricas: Volume de Procedimentos por Médico', run_simple_query('procedures_by_doctor')),
                    ('Métricas: Volume de Solicitações por Hospital', run_simple_query('solicitations_by_hospital')),
                    ('Métricas: Doadores Anônimos', run_simple_query('doadores_anonimos')),
                    ('(*) Estoque por Cidade', run_stock_by_city),
                    ('(*) Solicitações Atendidas (Hospital)', run_solicitations_fulfilled),
                    ('(*) Hospitais que solicitaram a todos os Hemocentros', run_simple_query('hospitals_all_hemocentros_div'))
                ]
            elif role == 'medico':
                options = [
                    ('Listar Doadores', run_simple_query('list_doadores')),
                    ('Listar Receptores', run_simple_query('list_receptores')),
                    ('Listar Hospitais', run_simple_query('list_hospitais')),
                    ('(*) Análise de Tendências em Atendimentos', run_attendance_trends),
                    ('(*) Receptores por Tipo Sanguíneo Compatível', run_receptors_by_blood_type),
                    ('(*) Compatibilidade Doador-Receptor', run_simple_query('donor_receptor_compatibility'))
                ]
            elif role == 'enfermeiro':
                options = [
                    ('Listar Triagens', run_simple_query('list_triagens')),
                    ('Listar Doadores', run_simple_query('list_doadores')),
                    ('(*) Histórico de Doações de um Doador', run_donor_history)
                ]
            elif role == 'biomedico':
                options = [
                    ('Listar Biomédicos', run_simple_query('list_biomedicos')),
                    ('Ver Estoque', run_simple_query('estoque')),
                    ('(*) Procedimentos Anonimizados', run_simple_query('procedimentos_anonimos')),
                    ('(*) Efetividade de Testagens', run_testing_effectiveness),
                    ('(*) Rotatividade de Estoque', run_stock_turnover)
                ]
            elif role == 'agente':
                 options = [
                    ('Listar Agentes', run_simple_query('list_agentes')),
                    ('(*) Doadores Anonimizados', run_simple_query('doadores_anonimos')),
                    ('(*) Campanhas de Doação', run_campaign_analysis)
                ]
            
            for i, (label, _) in enumerate(options):
                print(f"{i + 1}. {label}")
            print("0. Sair")
            
            choice = input("\nSelecione uma opção: ")
            
            if choice == '0':
                break
                
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    label, action = options[idx]
                    print(f"\n=== {label} ===")
                    if callable(action):
                        action(queries, user)
                    else:
                        print("Erro: Ação não é executável.")
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Entrada inválida.")

if __name__ == "__main__":
    main()
