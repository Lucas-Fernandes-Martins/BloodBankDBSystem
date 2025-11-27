import React from 'react';
import CadastroDoador from '../CadastroDoador';

function DoadorDashboard() {
    return (
        <div className="role-dashboard">
            <h3>Área do Doador</h3>
            <p>Bem-vindo! Aqui você pode realizar seu cadastro ou atualizar seus dados.</p>
            <div className="card">
                <CadastroDoador />
            </div>
        </div>
    );
}

export default DoadorDashboard;
