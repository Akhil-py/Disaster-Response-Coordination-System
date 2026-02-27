import React from 'react';
import { formatTimestamp } from '../utils/helpers';
import './ActivityFeed.css';

const DOT_COLORS = {
  spawn: '#0088ff',
  assign: '#00cc66',
  resolve: '#e0e8ff',
  escalate: '#ffaa00',
  conflict: '#ff3333',
};

export default function ActivityFeed({ activityLog }) {
  return (
    <div className="activity-feed-panel">
      <div className="activity-feed-header">ACTIVITY LOG</div>
      <div className="activity-feed-list">
        {activityLog.map((entry, idx) => (
          <div key={idx} className="activity-entry">
            <span className="activity-timestamp">
              {formatTimestamp(entry.timestamp)}
            </span>
            <span
              className="activity-dot"
              style={{ backgroundColor: DOT_COLORS[entry.type] || '#4a6080' }}
            />
            <span className="activity-message">{entry.message}</span>
          </div>
        ))}
        {activityLog.length === 0 && (
          <div className="activity-empty">No activity yet...</div>
        )}
      </div>
    </div>
  );
}
