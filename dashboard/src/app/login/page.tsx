import type { Metadata } from "next";
import { configProblems } from "@/lib/env";
import { LoginForm } from "./LoginForm";

export const metadata: Metadata = { title: "Sign in" };

export default function LoginPage() {
  const problems = configProblems();
  return (
    <main className="flex-1 grid place-items-center p-6">
      <div className="w-full max-w-[360px]">
        <h1 className="text-[24px] mb-1">AI YT Channel</h1>
        <p className="text-ink-soft mb-8">Sign in to see today&apos;s board.</p>
        {problems.length > 0 ? (
          <div className="rounded-[10px] bg-sindoor-tint p-4 text-[14px]">
            <p className="font-medium text-sindoor mb-1">The dashboard is not configured yet.</p>
            <p>
              Set {problems.join(", ")} in <code>dashboard/.env.local</code> or the Vercel project. See <code>dashboard/README.md</code>.
            </p>
          </div>
        ) : (
          <LoginForm />
        )}
      </div>
    </main>
  );
}
