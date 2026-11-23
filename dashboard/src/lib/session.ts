import "server-only";
import { createHash, createHmac, timingSafeEqual } from "node:crypto";
import { SignJWT, jwtVerify } from "jose";
import { ConfigError, env } from "./env";

export type Session = { user: string };
type User = { user: string; password: string };

export const SESSION_COOKIE = "dash_session";
export const SESSION_DAYS = 30;

export function parseUsers(raw: string): User[] {
  const text = raw.trim();
  if (!text) return [];
  if (text.startsWith("[")) {
    let list: Partial<User>[];
    try {
      list = JSON.parse(text) as Partial<User>[];
    } catch {
      throw new ConfigError("DASHBOARD_USERS is not valid JSON. Fix the value in dashboard/.env.local (or the Vercel project settings).");
    }
    if (!Array.isArray(list)) throw new ConfigError("DASHBOARD_USERS must be a JSON list of {user, password} objects.");
    return list.filter((u) => u.user && u.password).map((u) => ({ user: String(u.user), password: String(u.password) }));
  }
  return text
    .split(/[,\n]/)
    .map((s) => s.trim())
    .filter(Boolean)
    .map((entry) => {
      const [user, ...rest] = entry.split(":");
      if (rest.length > 1 && /^(admin|viewer)$/i.test(rest[0])) rest.shift();
      return { user: user.trim(), password: rest.join(":") };
    })
    .filter((u) => u.user && u.password);
}

function same(a: string, b: string) {
  const ha = createHash("sha256").update(a).digest();
  const hb = createHash("sha256").update(b).digest();
  return timingSafeEqual(ha, hb);
}

function findUser(name: string): User | undefined {
  const wanted = name.trim().toLowerCase();
  return parseUsers(env.users()).find((u) => u.user.toLowerCase() === wanted);
}

function fingerprint(password: string) {
  return createHmac("sha256", env.authSecret()).update(password).digest("hex").slice(0, 16);
}

export function checkCredentials(user: string, password: string): Session | null {
  const found = findUser(user);
  if (!found || !same(found.password, password)) return null;
  return { user: found.user };
}

const key = () => new TextEncoder().encode(env.authSecret());

export async function signSession(s: Session): Promise<string> {
  const found = findUser(s.user);
  if (!found) throw new Error("Cannot sign a session for a user that is not in DASHBOARD_USERS.");
  return new SignJWT({ pw: fingerprint(found.password) })
    .setProtectedHeader({ alg: "HS256" })
    .setSubject(found.user)
    .setIssuedAt()
    .setExpirationTime(`${SESSION_DAYS}d`)
    .sign(key());
}

export async function readSession(token: string | undefined): Promise<Session | null> {
  if (!token) return null;
  try {
    const { payload } = await jwtVerify(token, key());
    if (!payload.sub) return null;
    const found = findUser(payload.sub);
    if (!found || payload.pw !== fingerprint(found.password)) return null;
    return { user: found.user };
  } catch {
    return null;
  }
}
