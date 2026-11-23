
export class ConfigError extends Error {}

function need(name: string): string {
  const v = process.env[name];
  if (!v) throw new ConfigError(`${name} is not set. Add it to dashboard/.env.local (or the Vercel project settings).`);
  return v;
}

export const env = {
  repo: () => need("GITHUB_REPO"),
  token: () => need("GITHUB_TOKEN"),
  videosBranch: () => process.env.VIDEOS_BRANCH || "videos",
  workflowsBranch: () => process.env.WORKFLOWS_BRANCH || "main",
  authSecret: () => need("AUTH_SECRET"),
  users: () => need("DASHBOARD_USERS"),
  accountsVar: () => process.env.ACCOUNTS_VARIABLE || "DASHBOARD_ACCOUNTS",
  /** Keys that may call /api/trigger: CRON_SECRET is what Vercel's scheduler sends, TRIGGER_SECRET is for any other caller. */
  triggerSecrets: () => [process.env.CRON_SECRET, process.env.TRIGGER_SECRET].filter((s): s is string => Boolean(s)),
};

export function configProblems(): string[] {
  const out: string[] = [];
  for (const k of ["GITHUB_REPO", "GITHUB_TOKEN", "AUTH_SECRET", "DASHBOARD_USERS"]) if (!process.env[k]) out.push(k);
  return out;
}
