import React, { useState, useEffect } from 'react';

function BiomedicoDashboard() {
  const [bolsa, setBolsa] = useState({
    volume_doado: 450,
    tipo_sangue: '',
    valido: true,
    triagem_id: '',
    biomedico_id: '',
    hemocentro_cnpj: '',
    data_testagem: new Date().toISOString().split('T')[0],
  });
  const [triagens, setTriagens] = useState([]);
  const [biomedicos, setBiomedicos] = useState([]);
  const [hemocentros, setHemocentros] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const resTriagens = await fetch('http://localhost:8000/api/options/triagens');
        if (resTriagens.ok) setTriagens(await resTriagens.json());

        const resBiomedicos = await fetch('http://localhost:8000/api/options/biomedicos');
        if (resBiomedicos.ok) setBiomedicos(await resBiomedicos.json());

        const resHemocentros = await fetch('http://localhost:8000/api/options/hemocentros');
        if (resHemocentros.ok) setHemocentros(await resHemocentros.json());
      } catch (error) {
        console.error("Error fetching options:", error);
      }
    };
    fetchData();
  }, []);

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setBolsa({ ...bolsa, [e.target.name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/bolsa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bolsa),
      });
      if (response.ok) {
        const data = await response.json();
        alert(`Bolsa registrada com sucesso! Código: ${data.codigo}`);
      } else {
        alert('Erro ao registrar bolsa.');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="role-dashboard">
      <h3>Biomédico - Registro de Bolsa de Sangue</h3>
      <div className="card">
        <form onSubmit={handleSubmit}>
          <select name="triagem_id" onChange={handleChange} required value={bolsa.triagem_id}>
            <option value="">Selecione Triagem</option>
            {triagens.map(t => <option key={t.idtriagem} value={t.idtriagem}>Triagem {t.idtriagem} - {t.doador_nome}</option>)}
          </select>

          <select name="biomedico_id" onChange={handleChange} required value={bolsa.biomedico_id}>
            <option value="">Selecione Biomédico</option>
            {biomedicos.map(b => <option key={b.id} value={b.id}>{b.nome} (CRBM: {b.crbm})</option>)}
          </select>

          <select name="hemocentro_cnpj" onChange={handleChange} required value={bolsa.hemocentro_cnpj}>
            <option value="">Selecione Hemocentro</option>
            {hemocentros.map(h => <option key={h.cnpj} value={h.cnpj}>{h.nome}</option>)}
          </select>

          <div className="grid-2">
            <input type="number" name="volume_doado" placeholder="Volume (ml)" value={bolsa.volume_doado} onChange={handleChange} required />
            <select name="tipo_sangue" onChange={handleChange} required value={bolsa.tipo_sangue}>
              <option value="">Selecione Tipo Sanguíneo</option>
              <option value="A+">A+</option>
              <option value="A-">A-</option>
              <option value="B+">B+</option>
              <option value="B-">B-</option>
              <option value="AB+">AB+</option>
              <option value="AB-">AB-</option>
              <option value="O+">O+</option>
              <option value="O-">O-</option>
            </select>
          </div>

          <label>
            <input type="checkbox" name="valido" checked={bolsa.valido} onChange={handleChange} />
            Bolsa Válida?
          </label>

          <input type="date" name="data_testagem" value={bolsa.data_testagem} onChange={handleChange} required />

          <button type="submit">Registrar Bolsa</button>
        </form>
      </div>
    </div>
  );
}

export default BiomedicoDashboard;

