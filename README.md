# Sistema de Banco de Dados de Banco de Sangue

Este projeto implementa um sistema de gerenciamento para bancos de sangue, utilizando PostgreSQL e uma interface de linha de comando (CLI) em Python.

## Pré-requisitos
- Docker & Docker Compose
- Python 3.9+

## 1. Configuração do Banco de Dados
Inicie o banco de dados PostgreSQL usando Docker:
```bash
docker-compose up -d
```
Isso irá automaticamente:
- Iniciar um container PostgreSQL na porta **5433** (para evitar conflitos).
- Criar o esquema (`esquema.sql`).
- Popular dados iniciais (`dados.sql`).
- Habilitar a extensão `unaccent` para buscas insensíveis a acentos.

## 2. Configuração da Aplicação
Instale as dependências do Python (recomendado usar um ambiente virtual):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Executando a Aplicação
Para iniciar a interface de linha de comando:
```bash
python3 shell_app.py
```

## Funcionalidades e Perfis de Usuário

O sistema possui diferentes menus baseados no perfil do usuário logado. Abaixo estão as credenciais padrão para teste:

### Perfis de Teste
| Perfil | Usuário | Senha | Descrição |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin` | Acesso total a métricas, cadastro de usuários e gestão. |
| **Médico** | `medico` | `123` | Visualiza doadores, receptores e tendências de atendimento. |
| **Enfermeiro** | `enfermeiro` | `123` | Realiza triagens e visualiza histórico de doadores. |
| **Biomédico** | `biomedico` | `123` | Gerencia estoque, testagens e visualiza dados anonimizados. |
| **Agente** | `agente` | `123` | Visualiza doadores anonimizados e campanhas. |

### Consultas Avançadas (*)
As consultas marcadas com `(*)` no menu são análises avançadas implementadas especificamente para este projeto:

1.  **Estoque por Cidade (Admin)**: Busca insensível a acentos (ex: "sao paulo" encontra "São Paulo").
2.  **Análise de Tendências (Médico)**: Identifica o dia da semana com mais atendimentos para o médico logado.
3.  **Compatibilidade Doador-Receptor (Médico)**: Lista pares compatíveis baseados no tipo sanguíneo.
4.  **Procedimentos Anonimizados (Biomédico)**: Exibe procedimentos com nomes de pacientes mascarados.
5.  **Efetividade de Testagens (Biomédico)**: Calcula % de bolsas aprovadas pelo biomédico logado.
6.  **Doadores Anonimizados (Agente)**: Lista doadores com dados sensíveis ocultos.
7.  **Campanhas de Doação (Agente)**: Contagem de doações em um período específico.

## Arquivos Principais
- `shell_app.py`: Aplicação principal (CLI).
- `consultas.sql`: Arquivo contendo todas as queries SQL utilizadas.
- `esquema.sql`: Definição das tabelas e relacionamentos.
- `dados.sql`: Dados fictícios para teste.
