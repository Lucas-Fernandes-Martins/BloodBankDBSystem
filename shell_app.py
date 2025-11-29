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
                    ('Registrar Usuário', register_user),
                    ('Listar Doadores', 'list_doadores'),
                    ('Listar Médicos', 'list_medicos'),
                    ('Ver Estoque', 'estoque'),
                    ('Métricas: Estoque de Sangue por Tipo', 'blood_stock_by_type'),
                    ('Métricas: Procedimentos por Médico', 'procedures_by_doctor'),
                    ('Métricas: Solicitações por Hospital', 'solicitations_by_hospital'),
                    ('Métricas: Hospitais (Todos os Hemocentros)', 'hospitals_all_hemocentros'),
                    ('Métricas: Dados do Mapa', 'map_data'),
                    ('Métricas: Doadores Anônimos', 'doadores_anonimos'),
                    ('(*) Estoque por Cidade', 'stock_by_city'),
                    ('(*) Solicitações Atendidas (Hospital)', 'solicitations_fulfilled')
                ]
            elif role == 'medico':
                options = [
                    ('Listar Doadores', 'list_doadores'),
                    ('Listar Receptores', 'list_receptores'),
                    ('Listar Hospitais', 'list_hospitais'),
                    ('(*) Análise de Tendências em Atendimentos', 'attendance_trends'),
                    ('(*) Receptores por Tipo Sanguíneo Compatível', 'receptors_by_blood_type'),
                    ('(*) Compatibilidade Doador-Receptor', 'donor_receptor_compatibility')
                ]
            elif role == 'enfermeiro':
                options = [
                    ('Listar Triagens', 'list_triagens'),
                    ('Listar Doadores', 'list_doadores'),
                    ('(*) Histórico de Doações de um Doador', 'donor_history')
                ]
            elif role == 'biomedico':
                options = [
                    ('Listar Biomédicos', 'list_biomedicos'),
                    ('Ver Estoque', 'estoque'),
                    ('(*) Procedimentos Anonimizados', 'procedimentos_anonimos'),
                    ('(*) Efetividade de Testagens', 'testing_effectiveness'),
                    ('(*) Rotatividade de Estoque', 'stock_turnover')
                ]
            elif role == 'agente':
                 options = [
                    ('Listar Agentes', 'list_agentes'),
                    ('(*) Doadores Anonimizados', 'doadores_anonimos'),
                    ('(*) Campanhas de Doação', 'campaign_analysis')
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
                    _, action = options[idx]
                    if callable(action):
                        action(queries)
                    else:
                        print(f"\n--- Executando: {action} ---")
                        # Handle specific params if needed (simplified for now)
                        params = None
                        if action == 'estoque_filtrado':
                             cnpj = get_input("CNPJ", "98.765.432/0001-10")
                             params = (cnpj,)
                        elif action == 'stock_by_city':
                             city = get_input("Cidade (ex: São Paulo)", "São Paulo")
                             params = (f"%{city}%",)
                        elif action == 'attendance_trends':
                             if role == 'medico':
                                 medico_id = user['pessoaid']
                                 print(f"Usando ID do Médico logado: {medico_id}")
                             else:
                                 medico_id = get_input("ID do Médico", "P003")
                             receptor_id = get_input("ID do Receptor", "P002")
                             params = (medico_id, receptor_id)
                        elif action == 'donations_per_month':
                             centro_cnpj = get_input("CNPJ do Centro de Coleta", "11.222.333/0001-44")
                             params = (centro_cnpj,)
                        elif action == 'receptors_by_blood_type':
                             blood_type = get_input("Tipo Sanguíneo do Doador (ex: O+)", "O+")
                             params = (blood_type, blood_type, blood_type, blood_type, blood_type, blood_type, blood_type, blood_type)
                        elif action == 'donor_history':
                             doador_id = get_input("ID do Doador", "P001")
                             params = (doador_id,)
                        elif action == 'testing_effectiveness':
                             if role == 'biomedico':
                                 biomedico_id = user['pessoaid']
                                 print(f"Usando ID do Biomédico logado: {biomedico_id}")
                             else:
                                 biomedico_id = get_input("ID do Biomédico", "P005")
                             params = (biomedico_id,)
                        elif action == 'solicitations_fulfilled':
                             hospital_cnpj = get_input("CNPJ do Hospital", "12.345.678/0001-90")
                             params = (hospital_cnpj,)
                        elif action == 'stock_turnover':
                             hemocentro_cnpj = get_input("CNPJ do Hemocentro", "98.765.432/0001-10")
                             params = (hemocentro_cnpj,)
                        elif action == 'campaign_analysis':
                             start_date = get_input("Data Início (AAAA-MM-DD)", "2023-01-01")
                             end_date = get_input("Data Fim (AAAA-MM-DD)", "2023-12-31")
                             params = (start_date, end_date)
                        
                        results = execute_query(action, queries[action], params)
                        if results:
                            print_results(results)
                        input("\nPressione Enter para continuar...")
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Entrada inválida.")

if __name__ == "__main__":
    main()
