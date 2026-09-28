// Presentation only: do not infer missing case facts or investigative values.
export function provided(value) {
  return value == null || value === '' || value === 'Not supplied' ? 'Not provided' : value;
}

export function formatDate(value) {
  if (!value) return 'Not provided';
  const date = new Date(`${value}T00:00:00Z`);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric', timeZone: 'UTC',
  }).format(date);
}

export function formatRecordTime(value, timeZone) {
  if (!value) return 'Not provided';
  const date = new Date(value);
  if (!timeZone || Number.isNaN(date.getTime())) return value;
  try {
    return new Intl.DateTimeFormat('en-GB', {
      day: '2-digit', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZone,
    }).format(date);
  } catch {
    // An unsupported timezone must not crash the record page or invent a time.
    return value;
  }
}
