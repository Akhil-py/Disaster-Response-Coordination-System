import React from 'react';
import { INCIDENT_COLORS, RESOURCE_ICONS } from '../utils/constants';
import { zoneIdToCoords } from '../utils/helpers';
import './IncidentMarker.css';

const CELL_SIZE = 60;

const INCIDENT_ICONS = {
  fire: '🔥',
  collapse: '💥',
  medical: '🚑',
};

export default function IncidentMarker({ incident }) {
  const { row, col } = zoneIdToCoords(incident.zone_id);
  const cx = col * CELL_SIZE + CELL_SIZE / 2;
  const cy = row * CELL_SIZE + CELL_SIZE / 2;
  const color = INCIDENT_COLORS[incident.type] || '#ff0000';
  const icon = INCIDENT_ICONS[incident.type] || '⚠';
  const isCritical = incident.severity >= 4;

  return (
    <g className="incident-marker" style={{ pointerEvents: 'none' }}>
      {isCritical && (
        <circle
          cx={cx}
          cy={cy}
          r={20}
          fill="none"
          stroke="#ff0000"
          strokeWidth={2}
          className="incident-critical-glow"
        />
      )}
      <circle cx={cx} cy={cy} r={8} fill={color} opacity={0.8} />
      <text
        x={cx}
        y={cy - 20}
        textAnchor="middle"
        fontSize={11}
        fill="#e0e8ff"
        className="incident-label"
      >
        {icon} {incident.lives_at_risk}
      </text>
    </g>
  );
}
