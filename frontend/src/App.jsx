import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import CadastroDoador from './CadastroDoador';
import ConsultaEstoque from './ConsultaEstoque';
import './index.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="navbar">
          <h1>Blood Bank System</h1>
          <div className="links">
            <Link to="/">Cadastro de Doador</Link>
            <Link to="/consulta">Consulta de Estoque</Link>
          </div>
        </nav>

        <div className="content">
          <Routes>
            <Route path="/" element={<CadastroDoador />} />
            <Route path="/consulta" element={<ConsultaEstoque />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
