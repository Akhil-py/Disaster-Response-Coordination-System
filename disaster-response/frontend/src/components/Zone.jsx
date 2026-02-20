import React from 'react';
import { SEVERITY_COLORS } from '../utils/constants';
import './Zone.css';

const CELL_SIZE = 60;

export default function Zone({ zone, onClick }) {
  const x = zone.col * CELL_SIZE;
  const y = zone.row * CELL_SIZE;
  const fill = SEVERITY_COLORS[zone.severity] || SEVERITY_COLORS[0];

  return (
    <rect
      className="zone-cell"
      x={x}
      y={y}
      width={CELL_SIZE}
      height={CELL_SIZE}
      fill={fill}
      stroke="#ffffff22"
      strokeWidth={1}
      onClick={() => onClick(zone.id)}
    />
  );
}
