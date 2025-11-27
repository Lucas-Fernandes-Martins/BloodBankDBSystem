import React, { useState, useEffect } from 'react';

function DebugDashboard() {
    const [tables, setTables] = useState([]);
    const [selectedTable, setSelectedTable] = useState('');
    const [tableData, setTableData] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/api/debug/tables')
            .then(res => {
                if (!res.ok) throw new Error('Failed to fetch tables');
                return res.json();
            })
            .then(data => {
                if (Array.isArray(data)) {
                    setTables(data);
                } else {
                    console.error('Expected array of tables, got:', data);
                    setTables([]);
                }
            })
            .catch(err => {
                console.error(err);
                setTables([]);
            });
    }, []);

    useEffect(() => {
        if (selectedTable) {
            fetch(`http://localhost:8000/api/debug/table/${selectedTable}`)
                .then(res => res.json())
                .then(data => setTableData(data))
                .catch(err => console.error(err));
        }
    }, [selectedTable]);

    return (
        <div className="role-dashboard">
            <h3>Debug Dashboard - Database Viewer</h3>

            <div className="card">
                <label>Select Table:</label>
                <select onChange={(e) => setSelectedTable(e.target.value)} value={selectedTable}>
                    <option value="">-- Select a Table --</option>
                    {tables.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
            </div>

            {selectedTable && (
                <div className="card full-width">
                    <h4>Table: {selectedTable}</h4>
                    {tableData.length > 0 ? (
                        <div style={{ overflowX: 'auto' }}>
                            <table className="results-table">
                                <thead>
                                    <tr>
                                        {Object.keys(tableData[0]).map(key => <th key={key}>{key}</th>)}
                                    </tr>
                                </thead>
                                <tbody>
                                    {tableData.map((row, i) => (
                                        <tr key={i}>
                                            {Object.values(row).map((val, j) => <td key={j}>{String(val)}</td>)}
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    ) : (
                        <p>No data found in this table.</p>
                    )}
                </div>
            )}
        </div>
    );
}

export default DebugDashboard;
