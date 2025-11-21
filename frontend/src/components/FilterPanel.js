import React from 'react';

function FilterPanel({ filters, setFilters }) {
  return (
    <div className="filter-panel">
      <h3>Filters</h3>
      <div className="filter-group">
        <label>
          Severity:
          <select
            value={filters.severity}
            onChange={(e) => setFilters({ ...filters, severity: e.target.value })}
          >
            <option value="">All</option>
            <option value="ERROR">Error</option>
            <option value="WARNING">Warning</option>
            <option value="INFO">Info</option>
          </select>
        </label>

        <label>
          Limit:
          <input
            type="number"
            value={filters.limit}
            onChange={(e) => setFilters({ ...filters, limit: parseInt(e.target.value) })}
            min="10"
            max="1000"
          />
        </label>
      </div>
    </div>
  );
}

export default FilterPanel;
