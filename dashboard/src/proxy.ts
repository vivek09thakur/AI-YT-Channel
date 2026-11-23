import { NextResponse, type NextRequest } from "next/server";
import { SESSION_COOKIE, readSession } from "@/lib/session";

export async function proxy(req: NextRequest) {
  const { pathname } = req.nextUrl;
  const valid = Boolean(await readSession(req.cookies.get(SESSION_COOKIE)?.value));
  if (pathname === "/login") {
    return valid ? NextResponse.redirect(new URL("/", req.url)) : NextResponse.next();
  }
  if (!valid) {
    const url = new URL("/login", req.url);
    if (pathname !== "/") url.searchParams.set("next", pathname);
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next|api/trigger|favicon.ico|icon|.*\\.(?:png|svg|ico|woff2?)$).*)"],
};