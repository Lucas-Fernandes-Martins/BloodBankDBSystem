import React from 'react';
import { Navigate } from 'react-router-dom';

function ProtectedRoute({ children, allowedRoles }) {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    const userRole = localStorage.getItem('userRole');

    if (!isLoggedIn) {
        return <Navigate to="/login" replace />;
    }

    if (allowedRoles && !allowedRoles.includes(userRole) && userRole !== 'admin') {
        // Admin can access everything, otherwise check role
        return <div style={{ padding: '20px', textAlign: 'center' }}>
            <h2>Acesso Negado</h2>
            <p>Você não tem permissão para acessar esta página.</p>
            <button onClick={() => window.history.back()}>Voltar</button>
        </div>;
    }

    return children;
}

export default ProtectedRoute;
