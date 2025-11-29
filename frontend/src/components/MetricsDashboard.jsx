import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icon
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

function MetricsDashboard() {
    const [bloodStock, setBloodStock] = useState([]);
    const [solicitations, setSolicitations] = useState([]);
    const [procedures, setProcedures] = useState([]);
    const [mapData, setMapData] = useState([]);
    const [anonDonors, setAnonDonors] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const resStock = await fetch('http://localhost:8000/api/metrics/blood-stock');
                if (resStock.ok) setBloodStock(await resStock.json());

                const resSolicitations = await fetch('http://localhost:8000/api/metrics/solicitations-by-hospital');
                if (resSolicitations.ok) setSolicitations(await resSolicitations.json());

                const resProcedures = await fetch('http://localhost:8000/api/metrics/procedures-by-doctor');
                if (resProcedures.ok) setProcedures(await resProcedures.json());

                const resMap = await fetch('http://localhost:8000/api/metrics/map-data');
                if (resMap.ok) setMapData(await resMap.json());

                const resAnon = await fetch('http://localhost:8000/api/relatorios/doadores-anonimos');
                if (resAnon.ok) setAnonDonors(await resAnon.json());
            } catch (error) {
                console.error("Error fetching metrics:", error);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="role-dashboard">
            <h3>Dashboard de Métricas e Relatórios</h3>

            <div className="card full-width">
                <h4>Mapa de Instituições (Doação e Coleta)</h4>
                <div style={{ height: '400px', width: '100%' }}>
                    <MapContainer center={[-23.5505, -46.6333]} zoom={10} style={{ height: '100%', width: '100%' }}>
                        <TileLayer
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        />
                        {mapData.map((inst, index) => (
                            <Marker key={index} position={[inst.latitude, inst.longitude]}>
                                <Popup>
                                    <strong>{inst.nome}</strong><br />
                                    {inst.tipos}
                                </Popup>
                            </Marker>
                        ))}
                    </MapContainer>
                </div>
            </div>

            <div className="card full-width">
                <h4>Relatório de Doadores (Anonimizado - LGPD)</h4>
                <p>Dados sensíveis mascarados via SQL para análise estatística.</p>
                <table className="results-table">
                    <thead>
                        <tr>
                            <th>Nome (Mascarado)</th>
                            <th>CPF (Mascarado)</th>
                            <th>Idade (Generalizada)</th>
                            <th>Gênero</th>
                            <th>Tipo Sanguíneo</th>
                        </tr>
                    </thead>
                    <tbody>
                        {anonDonors.map((item, index) => (
                            <tr key={index}>
                                <td>{item.nome_anonimizado}</td>
                                <td>{item.cpf_mascarado}</td>
                                <td>{item.idade} anos</td>
                                <td>{item.genero}</td>
                                <td>{item.tiposanguineo}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="card full-width">
                <h4>Estoque de Sangue por Tipo (Group By)</h4>
                <table className="results-table">
                    <thead>
                        <tr>
                            <th>Tipo Sanguíneo</th>
                            <th>Total de Bolsas Válidas</th>
                        </tr>
                    </thead>
                    <tbody>
                        {bloodStock.map((item, index) => (
                            <tr key={index}>
                                <td>{item.tiposangue}</td>
                                <td>{item.total}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="card full-width">
                <h4>Solicitações por Hospital (Left Join)</h4>
                <p>Lista todos os hospitais, mesmo os que não fizeram solicitações.</p>
                <table className="results-table">
                    <thead>
                        <tr>
                            <th>Hospital</th>
                            <th>Total de Solicitações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {solicitations.map((item, index) => (
                            <tr key={index}>
                                <td>{item.nome}</td>
                                <td>{item.total_solicitacoes}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="card full-width">
                <h4>Procedimentos por Médico (Multiple Joins)</h4>
                <table className="results-table">
                    <thead>
                        <tr>
                            <th>Médico</th>
                            <th>Total de Procedimentos</th>
                        </tr>
                    </thead>
                    <tbody>
                        {procedures.map((item, index) => (
                            <tr key={index}>
                                <td>{item.nome}</td>
                                <td>{item.total_procedimentos}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default MetricsDashboard;
