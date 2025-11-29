import React, { useState, useEffect } from 'react';

function DebugDashboard() {
    const [tables, setTables] = useState([]);
    const [selectedTable, setSelectedTable] = useState('');
    const [tableData, setTableData] = useState([]);
    const [newInst, setNewInst] = useState({
        CNPJ: '', nome: '', cidade: '', estado: '', logradouro: '', latitude: '', longitude: '', tipo: 'HOSPITAL'
    });

    const handleInstChange = (e) => {
        setNewInst({ ...newInst, [e.target.name]: e.target.value });
    };

    const handleInstSubmit = async (e) => {
        e.preventDefault();
        const userRole = localStorage.getItem('userRole');
        try {
            const response = await fetch('http://localhost:8000/api/instituicao', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...newInst, user_role: userRole }),
            });
            if (response.ok) {
                alert('Instituição criada com sucesso!');
                setNewInst({ CNPJ: '', nome: '', cidade: '', estado: '', logradouro: '', latitude: '', longitude: '', tipo: 'HOSPITAL' });
            } else {
                const err = await response.json();
                alert('Erro ao criar instituição: ' + err.detail);
            }
        } catch (error) {
            console.error(error);
            alert('Erro de conexão');
        }
    };

    useEffect(() => {
        fetch('http://localhost:8000/api/debug/tables')
            .then(res => {
                if (!res.ok) throw new Error('Failed to fetch tables');
                return res.json();
            })
            .then(data => {
                if (Array.isArray(data)) {
                    setTables(data);
                } else {
                    console.error('Expected array of tables, got:', data);
                    setTables([]);
                }
            })
            .catch(err => {
                console.error(err);
                setTables([]);
            });
    }, []);

    useEffect(() => {
        if (selectedTable) {
            fetch(`http://localhost:8000/api/debug/table/${selectedTable}`)
                .then(res => res.json())
                .then(data => setTableData(data))
                .catch(err => console.error(err));
        }
    }, [selectedTable]);

    return (
        <div className="role-dashboard">
            <h3>Debug Database & Admin</h3>

            <div className="card full-width">
                <h4>Cadastrar Nova Instituição</h4>
                <form onSubmit={handleInstSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                    <input name="CNPJ" placeholder="CNPJ (XX.XXX.XXX/XXXX-XX)" value={newInst.CNPJ} onChange={handleInstChange} required />
                    <input name="nome" placeholder="Nome" value={newInst.nome} onChange={handleInstChange} required />
                    <input name="cidade" placeholder="Cidade" value={newInst.cidade} onChange={handleInstChange} required />
                    <input name="estado" placeholder="Estado (UF)" value={newInst.estado} onChange={handleInstChange} required maxLength="2" />
                    <input name="logradouro" placeholder="Logradouro" value={newInst.logradouro} onChange={handleInstChange} required />
                    <input name="latitude" placeholder="Latitude" type="number" step="any" value={newInst.latitude} onChange={handleInstChange} required />
                    <input name="longitude" placeholder="Longitude" type="number" step="any" value={newInst.longitude} onChange={handleInstChange} required />
                    <select name="tipo" value={newInst.tipo} onChange={handleInstChange}>
                        <option value="HOSPITAL">Hospital</option>
                        <option value="HEMOCENTRO">Hemocentro</option>
                        <option value="BANCO DE SANGUE">Banco de Sangue</option>
                        <option value="CENTRO COLETA">Centro de Coleta</option>
                    </select>
                    <button type="submit" style={{ gridColumn: 'span 2' }}>Cadastrar</button>
                </form>
            </div>

            <div className="card full-width">
                <h4>Inspecionar Tabelas</h4>
                <div className="debug-controls">
                    <label>Select Table:</label>
                    <select onChange={(e) => setSelectedTable(e.target.value)} value={selectedTable}>
                        <option value="">-- Select a Table --</option>
                        {tables.map(t => <option key={t} value={t}>{t}</option>)}
                    </select>
                </div>
            </div>

            {selectedTable && (
                <div className="card full-width">
                    <h4>Table: {selectedTable}</h4>
                    {tableData.length > 0 ? (
                        <div style={{ overflowX: 'auto' }}>
                            <table className="results-table">
                                <thead>
                                    <tr>
                                        {Object.keys(tableData[0]).map(key => <th key={key}>{key}</th>)}
                                    </tr>
                                </thead>
                                <tbody>
                                    {tableData.map((row, i) => (
                                        <tr key={i}>
                                            {Object.values(row).map((val, j) => <td key={j}>{String(val)}</td>)}
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    ) : (
                        <p>No data found in this table.</p>
                    )}
                </div>
            )}
        </div>
    );
}

export default DebugDashboard;
