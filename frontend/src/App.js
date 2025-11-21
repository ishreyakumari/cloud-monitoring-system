import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './App.css';
import LogTable from './components/LogTable';
import StatsChart from './components/StatsChart';
import FilterPanel from './components/FilterPanel';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';
const API_KEY = process.env.REACT_APP_API_KEY || '';

function App() {
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    severity: '',
    source: '',
    limit: 100
  });

  const fetchLogs = useCallback(async () => {
    try {
      const params = new URLSearchParams();
      if (filters.severity) params.append('severity', filters.severity);
      if (filters.source) params.append('source', filters.source);
      params.append('limit', filters.limit);

      const response = await axios.get(`${API_URL}/api/logs?${params}`, {
        headers: API_KEY ? { 'X-API-Key': API_KEY } : {}
      });
      setLogs(response.data.logs);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching logs:', error);
      setLoading(false);
    }
  }, [filters]);

  const fetchStats = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}/api/stats`, {
        headers: API_KEY ? { 'X-API-Key': API_KEY } : {}
      });
      setStats(response.data.stats);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  }, []);

  useEffect(() => {
    fetchLogs();
    fetchStats();
    const interval = setInterval(() => {
      fetchLogs();
      fetchStats();
    }, 10000);
    return () => clearInterval(interval);
  }, [fetchLogs, fetchStats]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔍 Cloud Log Monitoring System</h1>
        <p>Real-time log analysis and monitoring dashboard</p>
      </header>

      <div className="container">
        <FilterPanel filters={filters} setFilters={setFilters} />
        
        {stats && <StatsChart stats={stats} />}
        
        <div className="log-section">
          <h2>Recent Logs ({logs.length})</h2>
          {loading ? (
            <div className="loading">Loading logs...</div>
          ) : (
            <LogTable logs={logs} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
