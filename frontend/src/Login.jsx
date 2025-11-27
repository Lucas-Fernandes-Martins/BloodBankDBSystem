import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
    const [credentials, setCredentials] = useState({ login: '', senha: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setCredentials({ ...credentials, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(credentials),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('userRole', data.role);
                localStorage.setItem('isLoggedIn', 'true');

                // Redirect based on role
                if (data.role === 'admin') {
                    navigate('/debug');
                } else {
                    navigate(`/dashboard/${data.role}`);
                }
            } else {
                setError('Credenciais inválidas');
            }
        } catch (err) {
            console.error(err);
            setError('Erro ao conectar com o servidor');
        }
    };

    return (
        <div className="login-container" style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <h2>Login</h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                <input
                    name="login"
                    placeholder="Usuário"
                    onChange={handleChange}
                    required
                    style={{ padding: '10px', fontSize: '16px' }}
                />
                <input
                    type="password"
                    name="senha"
                    placeholder="Senha"
                    onChange={handleChange}
                    required
                    style={{ padding: '10px', fontSize: '16px' }}
                />
                <button type="submit" style={{ padding: '10px', fontSize: '16px', cursor: 'pointer' }}>Entrar</button>
            </form>
            {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}

            <div style={{ marginTop: '20px', fontSize: '12px', color: '#666' }}>
                <p>Usuários de teste (senha '123' para todos, exceto admin):</p>
                <ul>
                    <li>admin (senha: admin)</li>
                    <li>medico</li>
                    <li>enfermeiro</li>
                    <li>biomedico</li>
                    <li>agente</li>
                    <li>instituicao</li>
                    <li>doador</li>
                </ul>
            </div>
        </div>
    );
}

export default Login;
