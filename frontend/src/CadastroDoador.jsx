
import { useState } from 'react';
import axios from 'axios';

function CadastroDoador() {
    const [formData, setFormData] = useState({
        nome: '',
        genero: 'MASCULINO',
        tiposanguineo: 'O+',
        cidade: '',
        estado: '',
        logradouro: '',
        dataNascimento: '',
        telefone: '',
        email: '',
        cpf: '',
        peso: '',
        altura: ''
    });

    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/api/doador', formData);
            setMessage('Doador cadastrado com sucesso! ID: ' + response.data.id);
        } catch (error) {
            const detail = error.response?.data?.detail;
            const errorMsg = typeof detail === 'object' ? JSON.stringify(detail) : (detail || error.message);
            setMessage('Erro ao cadastrar: ' + errorMsg);
        }
    };

    return (
        <div className="card">
            <h2>Cadastro de Doador</h2>
            <form onSubmit={handleSubmit} className="form-grid">
                <input name="nome" placeholder="Nome Completo" onChange={handleChange} required />
                <select name="genero" onChange={handleChange}>
                    <option value="MASCULINO">Masculino</option>
                    <option value="FEMININO">Feminino</option>
                    <option value="OUTRO">Outro</option>
                </select>
                <select name="tiposanguineo" onChange={handleChange}>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                </select>
                <input name="cidade" placeholder="Cidade" onChange={handleChange} />
                <input name="estado" placeholder="Estado (UF)" maxLength="2" onChange={handleChange} />
                <input name="logradouro" placeholder="Logradouro" onChange={handleChange} />
                <input type="date" name="dataNascimento" onChange={handleChange} required />
                <input name="telefone" placeholder="Telefone (11 dígitos)" onChange={handleChange} />
                <input type="email" name="email" placeholder="Email" onChange={handleChange} />
                <input name="cpf" placeholder="CPF (11 dígitos)" onChange={handleChange} />
                <input type="number" step="0.1" name="peso" placeholder="Peso (kg)" onChange={handleChange} required />
                <input type="number" step="0.01" name="altura" placeholder="Altura (m)" onChange={handleChange} required />

                <button type="submit" className="full-width">Cadastrar</button>
            </form>
            {message && <p className="message">{message}</p>}
        </div>
    );
}

export default CadastroDoador;
