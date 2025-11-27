# Testing Guide - Blood Bank System

Follow these steps to run and test the system.

## 1. Start the Database
Ensure the database is running (it should be if you followed the previous steps):
```bash
docker-compose up -d
```

## 2. Start the Backend
Open a **new terminal** and run:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*Keep this terminal open.*

## 3. Start the Frontend
Open **another new terminal** and run:
```bash
cd frontend
npm install
npm run dev
```
*Keep this terminal open.*

## 4. Test Features via Browser
Open your browser to `http://localhost:5173`.

### Test 1: Register a Donor (Cadastro)
1.  Go to the **Cadastro de Doador** page (Home).
2.  Fill in the form with test data:
    - **ID**: `P999`
    - **Nome**: `Teste User`
    - **Peso**: `75.5`
    - **Altura**: `1.80`
    - **Data Nascimento**: `1990-01-01`
    - **Outros campos**: Fill as desired.
3.  Click **Cadastrar**.
4.  You should see a success message: "Doador cadastrado com sucesso!".

### Test 2: Query Stock (Consulta)
1.  Click on **Consulta de Estoque** in the navigation bar.
2.  (Optional) Enter a Hemocentro CNPJ (e.g., `98.765.432/0001-10`) or leave blank to see all.
3.  Click **Pesquisar**.
4.  You should see a table with blood stock levels.

## 5. Test SQL Queries
To test the 5 complex queries required by the project:

Run the `consultas.sql` script inside the container:
```bash
docker exec -i bloodbank_db psql -U admin -d bloodbank < consultas.sql
```
This will execute all the queries and show the results in your terminal.
