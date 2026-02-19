import { useState, useEffect, useRef, useCallback } from 'react';
import { MESSAGE_TYPES } from '../utils/constants';

const WS_URL = 'ws://localhost:8000/ws';
const RECONNECT_DELAY = 3000;

export default function useGameSocket() {
  const [gameState, setGameState] = useState(null);
  const [activityLog, setActivityLog] = useState([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null);
  const reconnectTimer = useRef(null);

  useEffect(() => {
    let unmounted = false;

    function connect() {
      if (unmounted) return;
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
        if (!unmounted) {
          reconnectTimer.current = setTimeout(connect, RECONNECT_DELAY);
        }
      };

      ws.onerror = () => {
        ws.close();
      };
    }

    connect();

    return () => {
      unmounted = true;
      if (reconnectTimer.current) {
        clearTimeout(reconnectTimer.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const sendAssign = useCallback((resourceId, zoneId) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: MESSAGE_TYPES.ASSIGN,
        payload: { resource_id: resourceId, zone_id: zoneId },
      }));
    }
  }, []);

  return { gameState, activityLog, sendAssign, connected };
}
