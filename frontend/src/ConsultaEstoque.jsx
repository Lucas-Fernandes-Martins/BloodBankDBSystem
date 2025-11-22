import { useState } from 'react';
import axios from 'axios';

function ConsultaEstoque() {
    const [cnpj, setCnpj] = useState('');
    const [results, setResults] = useState([]);
    const [error, setError] = useState('');

    const handleSearch = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.get('http://localhost:8000/api/consultas/estoque', {
                params: { hemocentro_cnpj: cnpj || undefined }
            });
            setResults(response.data);
            setError('');
        } catch (err) {
            setError('Erro ao buscar estoque');
        }
    };

    return (
        <div className="card">
            <h2>Consulta de Estoque de Sangue</h2>
            <form onSubmit={handleSearch} className="search-form">
                <input
                    placeholder="CNPJ do Hemocentro (Opcional)"
                    value={cnpj}
                    onChange={(e) => setCnpj(e.target.value)}
                />
                <button type="submit">Pesquisar</button>
            </form>

            {error && <p className="error">{error}</p>}

            {results.length > 0 && (
                <table className="results-table">
                    <thead>
                        <tr>
                            <th>Instituição</th>
                            <th>O-</th>
                            <th>O+</th>
                            <th>A-</th>
                            <th>A+</th>
                            <th>B-</th>
                            <th>B+</th>
                            <th>AB-</th>
                            <th>AB+</th>
                        </tr>
                    </thead>
                    <tbody>
                        {results.map((row, index) => (
                            <tr key={index}>
                                <td>{row.nome}</td>
                                <td>{row.numominus}</td>
                                <td>{row.numoplus}</td>
                                <td>{row.numaminus}</td>
                                <td>{row.numaplus}</td>
                                <td>{row.numbminus}</td>
                                <td>{row.numbplus}</td>
                                <td>{row.numabminus}</td>
                                <td>{row.numabplus}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default ConsultaEstoque;
