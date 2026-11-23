
const IST = "Asia/Kolkata";

export function fmtTime(iso: string) {
  return new Intl.DateTimeFormat("en-IN", { hour: "numeric", minute: "2-digit", hour12: true, timeZone: IST }).format(new Date(iso));
}

export function fmtClock(hhmm: string) {
  const h = Number(hhmm.slice(0, 2));
  return `${h % 12 || 12}:${hhmm.slice(3, 5)} ${h < 12 ? "am" : "pm"}`;
}

export function fmtDay(iso: string) {
  return new Intl.DateTimeFormat("en-IN", { weekday: "short", day: "numeric", month: "short", timeZone: IST }).format(new Date(iso));
}

export function fmtDayLong(iso: string) {
  return new Intl.DateTimeFormat("en-IN", { weekday: "long", day: "numeric", month: "long", timeZone: IST }).format(new Date(iso));
}

export function fmtDuration(sec: number | null | undefined) {
  if (sec === null || sec === undefined) return "";
  if (sec < 60) return "<1 min";
  const m = Math.round(sec / 60);
  if (m < 60) return `${m} min`;
  const h = Math.floor(m / 60);
  const rest = m % 60;
  return rest ? `${h} h ${rest} min` : `${h} h`;
}

export function ago(iso: string | undefined, now = Date.now()) {
  if (!iso) return "";
  const s = Math.max(0, Math.round((now - new Date(iso).getTime()) / 1000));
  if (s < 60) return "just now";
  const m = Math.round(s / 60);
  if (m < 60) return `${m} min ago`;
  const h = Math.round(m / 60);
  if (h < 36) return `${h} h ago`;
  const d = Math.round(h / 24);
  if (d < 60) return `${d} days ago`;
  return fmtDay(iso);
}
