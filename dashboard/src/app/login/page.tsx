import type { Metadata } from "next";
import Link from "next/link";
import { ThemeToggle } from "@/components/ThemeToggle";
import { configProblems } from "@/lib/env";
import { LoginForm } from "./LoginForm";

export const metadata: Metadata = { title: "Sign in" };

export default function LoginPage() {
  const problems = configProblems();
  return (
    <main className="relative flex-1 grid place-items-center p-6">
      <ThemeToggle className="absolute top-3 right-3" />
      <div className="w-full max-w-[360px]">
        <h1 className="font-display text-[26px] font-normal mb-1">AI YT Channel</h1>
        <p className="text-ink-soft mb-8">Sign in to see today&apos;s board.</p>
        {problems.length > 0 ? (
          <div className="rounded-[10px] bg-sindoor-tint p-4 text-[14px]">
            <p className="font-medium text-sindoor mb-1">The dashboard is not configured yet.</p>
            <p>
              Set {problems.join(", ")} in <code>dashboard/.env.local</code> or the Vercel project. See the{" "}
              <Link href="/docs/dashboard" className="text-violet underline">
                dashboard docs
              </Link>
              .
            </p>
          </div>
        ) : (
          <LoginForm />
        )}
      </div>
    </main>
  );
}
