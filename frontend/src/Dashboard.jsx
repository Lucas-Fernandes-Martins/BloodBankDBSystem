import React from 'react';
import { useParams, Link } from 'react-router-dom';
import AgenteDashboard from './components/AgenteDashboard';
import MedicoDashboard from './components/MedicoDashboard';
import EnfermeiroDashboard from './components/EnfermeiroDashboard';
import BiomedicoDashboard from './components/BiomedicoDashboard';
import InstituicaoDashboard from './components/InstituicaoDashboard';
import DoadorDashboard from './components/DoadorDashboard'; // We can reuse or wrap the existing one
import ReceptorDashboard from './components/ReceptorDashboard';

function Dashboard() {
    const { role } = useParams();

    const renderDashboard = () => {
        switch (role) {
            case 'agente':
                return <AgenteDashboard />;
            case 'medico':
                return <MedicoDashboard />;
            case 'enfermeiro':
                return <EnfermeiroDashboard />;
            case 'biomedico':
                return <BiomedicoDashboard />;
            case 'instituicao':
                return <InstituicaoDashboard />;
            case 'doador':
                return <DoadorDashboard />;
            case 'receptor':
                return <ReceptorDashboard />;
            default:
                return <div>Role not found</div>;
        }
    };

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <Link to="/" className="back-link">← Voltar</Link>
                <h2>Painel do {role.charAt(0).toUpperCase() + role.slice(1)}</h2>
            </div>
            <div className="dashboard-content">
                {renderDashboard()}
            </div>
        </div>
    );
}

export default Dashboard;
