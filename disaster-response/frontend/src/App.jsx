import React, { useState, useEffect } from 'react';
import StatsBar from './components/StatsBar';
import CityGrid from './components/CityGrid';
import ActivityFeed from './components/ActivityFeed';
import './App.css';

export default function App() {
  const [selectedResourceId, setSelectedResourceId] = useState(null);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        setSelectedResourceId(null);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="app">
      <StatsBar gameState={null} connected={false} />
      <div className="app-body">
        <div className="app-grid-container">
          <CityGrid
            gameState={null}
            selectedResourceId={selectedResourceId}
            setSelectedResourceId={setSelectedResourceId}
            sendAssign={() => {}}
          />
        </div>
        <ActivityFeed activityLog={[]} />
      </div>
    </div>
  );
}
