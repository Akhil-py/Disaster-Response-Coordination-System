import React from 'react';
import { RESOURCE_ICONS } from '../utils/constants';
import { zoneIdToCoords } from '../utils/helpers';
import './Resource.css';

const CELL_SIZE = 60;

const RESOURCE_BG = {
  ambulance: '#0066cc',
  fire_truck: '#cc2200',
  shelter: '#00884a',
};

export default function Resource({ resource, isSelected, onSelect }) {
  const { row, col } = zoneIdToCoords(resource.zone_id);
  const cx = col * CELL_SIZE + CELL_SIZE / 2;
  const cy = row * CELL_SIZE + CELL_SIZE / 2;
  const icon = RESOURCE_ICONS[resource.type] || '?';
  const bgColor = RESOURCE_BG[resource.type] || '#555';

  const isPulsing = resource.status === 'responding';
  const isReturning = resource.status === 'returning';
  const onCooldown = resource.cooldown_until > 0 && resource.status === 'returning';

  const handleClick = (e) => {
    e.stopPropagation();
    onSelect(resource.id);
  };

  return (
    <g
      className={`resource-group ${isPulsing ? 'resource-pulsing' : ''}`}
      onClick={handleClick}
      style={{ opacity: isReturning ? 0.5 : 1, cursor: 'pointer' }}
    >
      {isSelected && (
        <circle cx={cx} cy={cy} r={18} fill="none" stroke="#ffdd00" strokeWidth={3} className="resource-selected-ring" />
      )}
      <circle cx={cx} cy={cy} r={14} fill={bgColor} />
      {onCooldown && (
        <circle cx={cx} cy={cy} r={14} fill="rgba(100,100,100,0.6)" />
      )}
      <text
        x={cx}
        y={cy}
        textAnchor="middle"
        dominantBaseline="central"
        fontSize={resource.type === 'fire_truck' ? 14 : 12}
        fill="white"
        style={{ pointerEvents: 'none' }}
      >
        {icon}
      </text>
    </g>
  );
}
