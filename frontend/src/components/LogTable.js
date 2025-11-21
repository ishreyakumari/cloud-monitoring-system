import React from 'react';

function LogTable({ logs }) {
  return (
    <div style={{ overflowX: 'auto' }}>
      <table className="log-table">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Severity</th>
            <th>Message</th>
            <th>Source</th>
          </tr>
        </thead>
        <tbody>
          {logs.length === 0 ? (
            <tr>
              <td colSpan="4" style={{ textAlign: 'center', padding: '2rem' }}>
                No logs found
              </td>
            </tr>
          ) : (
            logs.map((log, index) => (
              <tr key={log.id || index}>
                <td>{new Date(log.timestamp).toLocaleString()}</td>
                <td>
                  <span className={`severity-badge ${log.severity}`}>
                    {log.severity}
                  </span>
                </td>
                <td>{log.message}</td>
                <td>{log.source}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default LogTable;
