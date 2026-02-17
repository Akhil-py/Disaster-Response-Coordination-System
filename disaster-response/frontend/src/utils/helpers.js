export function zoneIdToCoords(zoneId) {
  const parts = zoneId.split('_');
  return {
    row: parseInt(parts[1], 10),
    col: parseInt(parts[2], 10),
  };
}

export function formatTimestamp(unixTs) {
  const date = new Date(unixTs * 1000);
  const h = String(date.getHours()).padStart(2, '0');
  const m = String(date.getMinutes()).padStart(2, '0');
  const s = String(date.getSeconds()).padStart(2, '0');
  return `${h}:${m}:${s}`;
}

export function getSeverityLabel(severity) {
  switch (severity) {
    case 0: return 'none';
    case 1: return 'low';
    case 2: return 'medium';
    case 3: return 'high';
    case 4: return 'critical';
    default: return 'none';
  }
}
