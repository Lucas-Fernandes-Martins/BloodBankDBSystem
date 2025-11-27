import React, { useState, useEffect } from 'react';

function MedicoDashboard() {
    const [procedimento, setProcedimento] = useState({
        receptor_id: '',
        medico_id: '',
        hospital_cnpj: '',
    });
    const [receptores, setReceptores] = useState([]);
    const [medicos, setMedicos] = useState([]);
    const [hospitais, setHospitais] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const resReceptores = await fetch('http://localhost:8000/api/options/receptores');
                if (resReceptores.ok) setReceptores(await resReceptores.json());

                const resMedicos = await fetch('http://localhost:8000/api/options/medicos');
                if (resMedicos.ok) setMedicos(await resMedicos.json());

                const resHospitais = await fetch('http://localhost:8000/api/options/hospitais');
                if (resHospitais.ok) setHospitais(await resHospitais.json());
            } catch (error) {
                console.error("Error fetching options:", error);
            }
        };
        fetchData();
    }, []);

    const handleChange = (e) => {
        setProcedimento({ ...procedimento, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/api/procedimento', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(procedimento),
            });
            if (response.ok) {
                alert('Procedimento registrado com sucesso!');
            } else {
                alert('Erro ao registrar procedimento.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="role-dashboard">
            <h3>Médico - Registrar Procedimento</h3>
            <div className="card">
                <form onSubmit={handleSubmit}>
                    <select name="receptor_id" onChange={handleChange} required value={procedimento.receptor_id}>
                        <option value="">Selecione Receptor</option>
                        {receptores.map(r => <option key={r.id} value={r.id}>{r.nome} ({r.cpf})</option>)}
                    </select>

                    <select name="medico_id" onChange={handleChange} required value={procedimento.medico_id}>
                        <option value="">Selecione Médico</option>
                        {medicos.map(m => <option key={m.id} value={m.id}>{m.nome} (CRM: {m.crm})</option>)}
                    </select>

                    <select name="hospital_cnpj" onChange={handleChange} required value={procedimento.hospital_cnpj}>
                        <option value="">Selecione Hospital</option>
                        {hospitais.map(h => <option key={h.cnpj} value={h.cnpj}>{h.nome}</option>)}
                    </select>

                    <button type="submit">Registrar</button>
                </form>
            </div>
        </div>
    );
}

export default MedicoDashboard;

