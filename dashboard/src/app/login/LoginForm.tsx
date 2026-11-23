"use client";

import { useActionState } from "react";
import { login, type ActionResult } from "@/app/actions";

export function LoginForm() {
  const [state, action, pending] = useActionState<ActionResult | null, FormData>(login, null);
  return (
    <form action={action} className="flex flex-col gap-4">
      <label className="flex flex-col gap-1 text-[14px] font-medium">
        Name
        <input className="field" name="user" autoComplete="username" required autoFocus />
      </label>
      <label className="flex flex-col gap-1 text-[14px] font-medium">
        Password
        <input className="field" name="password" type="password" autoComplete="current-password" required />
      </label>
      {state && !state.ok && (
        <p role="alert" className="text-sindoor text-[14px]">
          {state.error}
        </p>
      )}
      <button className="btn btn-primary justify-center mt-1" type="submit" disabled={pending}>
        {pending ? "Signing in" : "Sign in"}
      </button>
    </form>
  );
}
