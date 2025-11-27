import React, { useState, useEffect } from 'react';

function AgenteDashboard() {
    const [pesquisa, setPesquisa] = useState({
        doador_id: '',
        agente_id: '',
        doou: false,
        primeira_doacao: false,
        doaria_novamente: false,
        feedback: '',
    });
    const [doadores, setDoadores] = useState([]);
    const [agentes, setAgentes] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const resDoadores = await fetch('http://localhost:8000/api/options/doadores');
                if (resDoadores.ok) setDoadores(await resDoadores.json());
                else console.error("Failed to fetch doadores:", resDoadores.statusText);

                const resAgentes = await fetch('http://localhost:8000/api/options/agentes');
                if (resAgentes.ok) setAgentes(await resAgentes.json());
                else console.error("Failed to fetch agentes:", resAgentes.statusText);
            } catch (error) {
                console.error("Error fetching options:", error);
            }
        };
        fetchData();
    }, []);

    const handleChange = (e) => {
        const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
        setPesquisa({ ...pesquisa, [e.target.name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/api/pesquisa', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(pesquisa),
            });
            if (response.ok) {
                alert('Pesquisa registrada com sucesso!');
            } else {
                alert('Erro ao registrar pesquisa.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="role-dashboard">
            <h3>Agente de Mapeamento - Pesquisa</h3>
            <div className="card">
                <form onSubmit={handleSubmit}>
                    <select name="doador_id" onChange={handleChange} required value={pesquisa.doador_id}>
                        <option value="">Selecione Doador</option>
                        {doadores.map(d => <option key={d.id} value={d.id}>{d.nome} ({d.cpf})</option>)}
                    </select>

                    <select name="agente_id" onChange={handleChange} required value={pesquisa.agente_id}>
                        <option value="">Selecione Agente</option>
                        {agentes.map(a => <option key={a.id} value={a.id}>{a.nome}</option>)}
                    </select>

                    <label>
                        <input type="checkbox" name="doou" onChange={handleChange} />
                        Doou sangue?
                    </label>
                    <label>
                        <input type="checkbox" name="primeira_doacao" onChange={handleChange} />
                        Primeira doação?
                    </label>
                    <label>
                        <input type="checkbox" name="doaria_novamente" onChange={handleChange} />
                        Doaria novamente?
                    </label>

                    <textarea name="feedback" placeholder="Feedback" onChange={handleChange} />

                    <button type="submit">Registrar Pesquisa</button>
                </form>
            </div>
        </div>
    );
}

export default AgenteDashboard;

