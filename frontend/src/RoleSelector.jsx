import React from 'react';
import { useNavigate } from 'react-router-dom';
import './index.css';

const roles = [
    { id: 'doador', label: 'Doador', icon: '🩸' },
    { id: 'receptor', label: 'Receptor', icon: '🤲' },
    { id: 'agente', label: 'Agente de Mapeamento', icon: '🗺️' },
    { id: 'medico', label: 'Médico', icon: '👨‍⚕️' },
    { id: 'enfermeiro', label: 'Enfermeiro', icon: '👩‍⚕️' },
    { id: 'biomedico', label: 'Biomédico', icon: '🔬' },
    { id: 'instituicao', label: 'Instituição de Saúde', icon: '🏥' },
];

function RoleSelector() {
    const navigate = useNavigate();

    return (
        <div className="role-selector-container">
            <h1>Bem-vindo ao Blood Bank System</h1>
            <p>Selecione seu perfil para continuar:</p>
            <div className="roles-grid">
                {roles.map((role) => (
                    <div key={role.id} className="role-card" onClick={() => navigate(`/dashboard/${role.id}`)}>
                        <div className="role-icon">{role.icon}</div>
                        <h3>{role.label}</h3>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default RoleSelector;
