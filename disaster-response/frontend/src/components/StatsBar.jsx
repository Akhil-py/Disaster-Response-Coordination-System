import React from 'react';
import './StatsBar.css';

export default function StatsBar({ gameState, connected }) {
  if (!gameState) {
    return (
      <div className="stats-bar">
        <div className="stats-title">DISASTER RESPONSE COMMAND</div>
        <div className="stats-values">
          <span className="stat-item">Connecting...</span>
        </div>
      </div>
    );
  }

  const connectedUsers = gameState.connected_users || 0;
  const activeIncidents = Object.keys(gameState.incidents || {}).length;

  return (
    <div className="stats-bar">
      <div className="stats-title">DISASTER RESPONSE COMMAND</div>
      <div className="stats-values">
        <span className="stat-item">
          <span className={`connection-dot ${connectedUsers > 1 ? 'dot-green' : 'dot-yellow'}`} />
          Connected Users: <span className="stat-value">{connectedUsers}</span>
        </span>
        <span className="stat-item">
          Lives Saved: <span className="stat-value stat-green">{gameState.lives_saved}</span>
        </span>
        <span className="stat-item">
          Lives Lost: <span className="stat-value stat-red">{gameState.lives_lost}</span>
        </span>
        <span className="stat-item">
          Active Incidents: <span className="stat-value stat-amber">{activeIncidents}</span>
        </span>
        <span className="stat-item">
          Tick: <span className="stat-value">{gameState.tick}</span>
        </span>
      </div>
    </div>
  );
}
