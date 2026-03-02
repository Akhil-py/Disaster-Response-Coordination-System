import React, { useState, useEffect } from 'react';
import useGameSocket from './hooks/useGameSocket';
import StatsBar from './components/StatsBar';
import CityGrid from './components/CityGrid';
import ActivityFeed from './components/ActivityFeed';
import './App.css';

export default function App() {
  const { gameState, activityLog, sendAssign, connected } = useGameSocket();
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
      <StatsBar gameState={gameState} connected={connected} />
      <div className="app-body">
        <div className="app-grid-container">
          <CityGrid
            gameState={gameState}
            selectedResourceId={selectedResourceId}
            setSelectedResourceId={setSelectedResourceId}
            sendAssign={sendAssign}
          />
        </div>
        <ActivityFeed activityLog={activityLog} />
      </div>
    </div>
  );
}
