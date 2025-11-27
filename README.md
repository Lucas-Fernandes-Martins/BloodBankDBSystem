# Blood Bank Database System - Part 3

## Prerequisites
- Docker & Docker Compose
- Python 3.9+
- Node.js 16+

## 1. Database Setup
Start the PostgreSQL database using Docker:
```bash
docker-compose up -d
```
This will automatically:
- Start a PostgreSQL 15 container on port **5433** (to avoid conflicts).
- Create the schema (`esquema.sql`).
- Populate initial data (`dados.sql`).

## 2. Backend Setup
Navigate to the `backend` directory:
```bash
cd backend
```

Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
The API will be available at `http://localhost:8000`.
Documentation: `http://localhost:8000/docs`

## 3. Frontend Setup
Navigate to the `frontend` directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Run the React application:
```bash
npm run dev
```
The application will be available at `http://localhost:5173`.

## Features
- **Cadastro de Doador**: Register a new donor (inserts into `Pessoa`, `TipoPessoa`, `Doador`).
- **Consulta de Estoque**: View blood stock per Hemocentro (parameterized query).

## Files
- `esquema.sql`: Database schema.
- `dados.sql`: Initial data population.
- `consultas.sql`: 5 complex SQL queries.
- `backend/`: Python/FastAPI backend.
- `frontend/`: React/Vite frontend.
