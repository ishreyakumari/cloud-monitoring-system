import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

function StatsChart({ stats }) {
  const chartData = {
    labels: ['ERROR', 'WARNING', 'INFO'],
    datasets: [
      {
        label: 'Log Distribution',
        data: [
          stats.severity_distribution.ERROR,
          stats.severity_distribution.WARNING,
          stats.severity_distribution.INFO
        ],
        backgroundColor: [
          'rgba(231, 76, 60, 0.8)',
          'rgba(243, 156, 18, 0.8)',
          'rgba(52, 152, 219, 0.8)'
        ],
        borderColor: [
          'rgba(231, 76, 60, 1)',
          'rgba(243, 156, 18, 1)',
          'rgba(52, 152, 219, 1)'
        ],
        borderWidth: 2
      }
    ]
  };

  return (
    <div>
      <div className="stats-grid">
        <div className="stat-card error">
          <h3>Errors</h3>
          <div className="value">{stats.error_count}</div>
        </div>
        <div className="stat-card warning">
          <h3>Warnings</h3>
          <div className="value">{stats.warning_count}</div>
        </div>
        <div className="stat-card info">
          <h3>Info</h3>
          <div className="value">{stats.info_count}</div>
        </div>
        <div className="stat-card">
          <h3>Total Logs</h3>
          <div className="value">{stats.total_logs}</div>
        </div>
      </div>

      <div className="chart-container">
        <h3>Log Distribution</h3>
        <div style={{ maxWidth: '400px', margin: '0 auto' }}>
          <Doughnut data={chartData} />
        </div>
      </div>
    </div>
  );
}

export default StatsChart;
