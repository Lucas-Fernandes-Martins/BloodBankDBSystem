import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import RoleSelector from './RoleSelector';
import Dashboard from './Dashboard';
import DebugDashboard from './components/DebugDashboard';
import './index.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="navbar">
          <h1>Blood Bank System</h1>
          <div className="links">
            <Link to="/">Início</Link>
            <Link to="/debug">Debug DB</Link>
          </div>
        </nav>

        <div className="content">
          <Routes>
            <Route path="/" element={<RoleSelector />} />
            <Route path="/dashboard/:role" element={<Dashboard />} />
            <Route path="/debug" element={<DebugDashboard />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
