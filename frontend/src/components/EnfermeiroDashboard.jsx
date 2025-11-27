import React, { useState, useEffect } from 'react';

function EnfermeiroDashboard() {
    const [triagem, setTriagem] = useState({
        doador_id: '',
        enfermeiro_id: '',
        centro_coleta_cnpj: '',
        centro_coleta_codigo: '',
        valido: false,
    });
    const [doadores, setDoadores] = useState([]);
    const [enfermeiros, setEnfermeiros] = useState([]);
    const [centrosColeta, setCentrosColeta] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const resDoadores = await fetch('http://localhost:8000/api/options/doadores');
                if (resDoadores.ok) setDoadores(await resDoadores.json());

                const resEnfermeiros = await fetch('http://localhost:8000/api/options/enfermeiros');
                if (resEnfermeiros.ok) setEnfermeiros(await resEnfermeiros.json());

                const resCentros = await fetch('http://localhost:8000/api/options/centros-coleta');
                if (resCentros.ok) setCentrosColeta(await resCentros.json());
            } catch (error) {
                console.error("Error fetching options:", error);
            }
        };
        fetchData();
    }, []);

    const handleChange = (e) => {
        const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
        // Special handling for Centro de Coleta composite key
        if (e.target.name === 'centro_coleta_composite') {
            const [cnpj, codigo] = e.target.value.split('|');
            setTriagem({ ...triagem, centro_coleta_cnpj: cnpj, centro_coleta_codigo: codigo });
        } else {
            setTriagem({ ...triagem, [e.target.name]: value });
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/api/triagem', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(triagem),
            });
            if (response.ok) {
                const data = await response.json();
                alert(`Triagem registrada com sucesso! ID: ${data.id}`);
            } else {
                alert('Erro ao registrar triagem.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="role-dashboard">
            <h3>Enfermeiro - Triagem</h3>
            <div className="card">
                <form onSubmit={handleSubmit}>
                    <select name="doador_id" onChange={handleChange} required value={triagem.doador_id}>
                        <option value="">Selecione Doador</option>
                        {doadores.map(d => <option key={d.id} value={d.id}>{d.nome} ({d.cpf})</option>)}
                    </select>

                    <select name="enfermeiro_id" onChange={handleChange} required value={triagem.enfermeiro_id}>
                        <option value="">Selecione Enfermeiro</option>
                        {enfermeiros.map(e => <option key={e.id} value={e.id}>{e.nome} (COREN: {e.coren})</option>)}
                    </select>

                    <select name="centro_coleta_composite" onChange={handleChange} required>
                        <option value="">Selecione Centro de Coleta</option>
                        {centrosColeta.map(c => (
                            <option key={`${c.cnpj}-${c.codigo}`} value={`${c.cnpj}|${c.codigo}`}>
                                {c.nome} - {c.codigo}
                            </option>
                        ))}
                    </select>

                    <label>
                        <input type="checkbox" name="valido" onChange={handleChange} />
                        Apto para doação?
                    </label>

                    <button type="submit">Registrar Triagem</button>
                </form>
            </div>
        </div>
    );
}

export default EnfermeiroDashboard;
