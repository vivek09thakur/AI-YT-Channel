import { ConfigError } from "@/lib/env";
import { GitHubError } from "@/lib/github";

export function Problem({ error }: { error: unknown }) {
  const msg = error instanceof Error ? error.message : String(error);
  const hint =
    error instanceof ConfigError
      ? "Add the missing variable to dashboard/.env.local (or the Vercel project) and reload."
      : error instanceof GitHubError && error.status === 401
        ? "GITHUB_TOKEN was rejected. Create a fine-grained token for the repo with read access to Actions, Secrets, Variables, Contents and Issues."
        : error instanceof GitHubError && (error.status === 403 || error.status === 404)
          ? "The token cannot see this repo or lacks a permission. Check GITHUB_REPO is owner/name and the token has read access to Secrets, Variables, Actions, Contents and Issues."
          : "GitHub did not answer. Reload in a moment.";
  return (
    <main className="p-6 max-w-[640px]">
      <h1 className="text-[22px] mb-2">The page could not load</h1>
      <p className="text-sindoor mb-2 break-words">{msg}</p>
      <p className="text-ink-soft">{hint}</p>
    </main>
  );
}
