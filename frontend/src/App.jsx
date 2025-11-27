import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import RoleSelector from './RoleSelector';
import Dashboard from './Dashboard';
import MetricsDashboard from './components/MetricsDashboard';
import DebugDashboard from './components/DebugDashboard';
import Login from './Login';
import ProtectedRoute from './ProtectedRoute';
import './index.css';

function LogoutButton() {
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem('userRole');
    localStorage.removeItem('isLoggedIn');
    navigate('/login');
  };
  return <button onClick={handleLogout} style={{ marginLeft: '10px', background: 'none', border: '1px solid white', color: 'white', cursor: 'pointer' }}>Sair</button>;
}

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="navbar">
          <h1>Blood Bank System</h1>
          <div className="links">
            <Link to="/">Início</Link>
            <Link to="/metrics">Métricas</Link>
            <Link to="/debug">Debug DB</Link>
            <LogoutButton />
          </div>
        </nav>

        <div className="content">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<RoleSelector />} />

            <Route path="/dashboard/:role" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />

            <Route path="/metrics" element={
              <ProtectedRoute allowedRoles={['admin', 'instituicao']}>
                <MetricsDashboard />
              </ProtectedRoute>
            } />

            <Route path="/debug" element={
              <ProtectedRoute allowedRoles={['admin']}>
                <DebugDashboard />
              </ProtectedRoute>
            } />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
