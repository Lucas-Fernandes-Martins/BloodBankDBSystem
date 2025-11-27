import React, { useState, useEffect } from 'react';

function InstituicaoDashboard() {
  const [solicitacao, setSolicitacao] = useState({
    hospital_cnpj: '',
    hemocentro_cnpj: '',
    qnt_oplus: 0,
    qnt_ominus: 0,
    qnt_aplus: 0,
    qnt_aminus: 0,
    qnt_bplus: 0,
    qnt_bminus: 0,
    qnt_abplus: 0,
    qnt_abminus: 0,
  });
  const [divisionResult, setDivisionResult] = useState(null);
  const [hospitais, setHospitais] = useState([]);
  const [hemocentros, setHemocentros] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const resHospitais = await fetch('http://localhost:8000/api/options/hospitais');
        if (resHospitais.ok) setHospitais(await resHospitais.json());

        const resHemocentros = await fetch('http://localhost:8000/api/options/hemocentros');
        if (resHemocentros.ok) setHemocentros(await resHemocentros.json());
      } catch (error) {
        console.error("Error fetching options:", error);
      }
    };
    fetchData();
  }, []);

  const handleChange = (e) => {
    setSolicitacao({ ...solicitacao, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/solicitacao', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(solicitacao),
      });
      if (response.ok) {
        alert('Solicitação enviada com sucesso!');
      } else {
        alert('Erro ao enviar solicitação.');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const runDivisionQuery = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/division/hospitals-all-hemocentros');
      if (response.ok) {
        const data = await response.json();
        if (Array.isArray(data)) {
          setDivisionResult(data);
        } else {
          console.error("Expected array, got:", data);
          setDivisionResult([]);
        }
      } else {
        console.error("Failed to fetch division query:", response.statusText);
        setDivisionResult([]);
      }
    } catch (error) {
      console.error('Error:', error);
      setDivisionResult([]);
    }
  };

  return (
    <div className="role-dashboard">
      <h3>Instituição de Saúde - Ações</h3>

      <div className="card">
        <h4>Nova Solicitação de Sangue</h4>
        <form onSubmit={handleSubmit}>
          <select name="hospital_cnpj" onChange={handleChange} required value={solicitacao.hospital_cnpj}>
            <option value="">Selecione Hospital</option>
            {hospitais.map(h => <option key={h.cnpj} value={h.cnpj}>{h.nome}</option>)}
          </select>

          <select name="hemocentro_cnpj" onChange={handleChange} required value={solicitacao.hemocentro_cnpj}>
            <option value="">Selecione Hemocentro</option>
            {hemocentros.map(h => <option key={h.cnpj} value={h.cnpj}>{h.nome}</option>)}
          </select>

          <div className="grid-2">
            <input type="number" name="qnt_oplus" placeholder="Qtd O+" onChange={handleChange} />
            <input type="number" name="qnt_ominus" placeholder="Qtd O-" onChange={handleChange} />
            {/* Add other blood types as needed */}
          </div>
          <button type="submit">Enviar Solicitação</button>
        </form>
      </div>

      <div className="card">
        <h4>Consultas Avançadas</h4>
        <button onClick={runDivisionQuery}>
          Buscar Hospitais que solicitaram a TODOS os Hemocentros (Divisão Relacional)
        </button>
        {divisionResult && (
          <div className="results">
            <h5>Resultados:</h5>
            <ul>
              {divisionResult.map((h, index) => (
                <li key={index}>{h.nome} ({h.CNPJ})</li>
              ))}
            </ul>
            {divisionResult.length === 0 && <p>Nenhum hospital encontrado.</p>}
          </div>
        )}
      </div>
    </div>
  );
}

export default InstituicaoDashboard;

