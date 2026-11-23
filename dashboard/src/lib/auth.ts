import "server-only";
import { io } from "next/cache";
import { cookies } from "next/headers";
import { SESSION_COOKIE, SESSION_DAYS, readSession, signSession, type Session } from "./session";

export { checkCredentials, parseUsers, readSession, signSession, SESSION_COOKIE, type Session } from "./session";

export async function getSession(): Promise<Session | null> {
  const jar = await cookies();
  // jwtVerify reads the clock; keep it out of prerenders (cookies can resolve during runtime prefetch).
  await io();
  return readSession(jar.get(SESSION_COOKIE)?.value);
}

export async function setSessionCookie(s: Session) {
  const jar = await cookies();
  jar.set(SESSION_COOKIE, await signSession(s), {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: SESSION_DAYS * 24 * 3600,
  });
}

export async function clearSessionCookie() {
  const jar = await cookies();
  jar.delete(SESSION_COOKIE);
}