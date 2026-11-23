"use server";

import { redirect } from "next/navigation";
import { checkCredentials, clearSessionCookie, setSessionCookie } from "@/lib/auth";

export type ActionResult = { ok: true; message?: string } | { ok: false; error: string };

export async function login(_prev: ActionResult | null, form: FormData): Promise<ActionResult> {
  const user = String(form.get("user") ?? "");
  const password = String(form.get("password") ?? "");
  try {
    const session = checkCredentials(user, password);
    if (!session) return { ok: false, error: "That name and password do not match." };
    await setSessionCookie(session);
  } catch (e) {
    console.error("login: sign-in is not configured correctly", e);
    return { ok: false, error: "Sign-in is not set up correctly on this server. Check the server logs." };
  }
  redirect("/");
}

export async function logout() {
  await clearSessionCookie();
  redirect("/login");
}
