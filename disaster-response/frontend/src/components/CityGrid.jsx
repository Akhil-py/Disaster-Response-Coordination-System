import React from 'react';
import Zone from './Zone';
import './CityGrid.css';

const GRID_SIZE = 600;

export default function CityGrid({ gameState, selectedResourceId, setSelectedResourceId, sendAssign }) {
  if (!gameState) return null;

  const zones = Object.values(gameState.zones || {});

  const handleZoneClick = (zoneId) => {
    // placeholder for assign logic
  };

  return (
    <div className="city-grid-panel">
      <div className="city-grid-header">
        <span className="live-dot" />
        CITY GRID — LIVE
      </div>
      <svg
        width={GRID_SIZE}
        height={GRID_SIZE}
        viewBox={`0 0 ${GRID_SIZE} ${GRID_SIZE}`}
        className="city-grid-svg"
      >
        {zones.map((zone) => (
          <Zone key={zone.id} zone={zone} onClick={handleZoneClick} />
        ))}
      </svg>
    </div>
  );
}
