import { useState, useEffect, useRef, useCallback } from 'react';
import { MESSAGE_TYPES } from '../utils/constants';

const WS_URL = 'ws://localhost:8000/ws';

export default function useGameSocket() {
  const [gameState, setGameState] = useState(null);
  const [activityLog, setActivityLog] = useState([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null);

  useEffect(() => {
    function connect() {
      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;

      ws.onopen = () => {
        setConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          if (msg.type === MESSAGE_TYPES.STATE_SYNC) {
            setGameState(msg.payload);
            if (msg.payload.activity_log) {
              setActivityLog(msg.payload.activity_log.slice(-10).reverse());
            }
          } else if (msg.type === MESSAGE_TYPES.ACTIVITY) {
            setActivityLog((prev) => {
              const updated = [msg.payload, ...prev];
              return updated.slice(0, 10);
            });
          }
        } catch (e) {
          // ignore malformed messages
        }
      };

      ws.onclose = () => {
        setConnected(false);
      };

      ws.onerror = () => {
        ws.close();
      };
    }

    connect();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return { gameState, activityLog, connected };
}
