import "server-only";
import { env } from "./env";

const API = "https://api.github.com";

export class GitHubError extends Error {
  constructor(public status: number, message: string, public path: string) {
    super(message);
  }
}

type Init = RequestInit & { raw?: boolean; allow404?: boolean };

async function gh<T>(path: string, init: Init = {}): Promise<T> {
  const { raw, allow404, ...rest } = init;
  const res = await fetch(`${API}/repos/${env.repo()}${path}`, {
    ...rest,
    cache: "no-store",
    headers: {
      Authorization: `Bearer ${env.token()}`,
      Accept: raw ? "application/vnd.github.raw+json" : "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "ai-yt-channel-dashboard",
      ...(rest.body ? { "Content-Type": "application/json" } : {}),
      ...(rest.headers ?? {}),
    },
  });
  if (res.status === 404 && allow404) return null as T;
  if (!res.ok) {
    let msg = res.statusText;
    try {
      const j = (await res.json()) as { message?: string };
      if (j.message) msg = j.message;
    } catch {
    }
    throw new GitHubError(res.status, `${res.status} ${msg}`, path);
  }
  if (res.status === 204) return undefined as T;
  if (raw) return (await res.text()) as T;
  return (await res.json()) as T;
}

async function paged<T>(path: string, key: string): Promise<T[]> {
  const out: T[] = [];
  for (let page = 1; page < 20; page++) {
    const sep = path.includes("?") ? "&" : "?";
    const data = await gh<Record<string, T[]>>(`${path}${sep}per_page=100&page=${page}`);
    const items = data[key] ?? [];
    out.push(...items);
    if (items.length < 100) break;
  }
  return out;
}

export type SecretMeta = { name: string; created_at: string; updated_at: string };

export const listSecrets = () => paged<SecretMeta>("/actions/secrets", "secrets");

export type VariableMeta = { name: string; value: string; created_at: string; updated_at: string };

export const listVariables = () => paged<VariableMeta>("/actions/variables", "variables");

export type IndexEntry = {
  dir: string;
  slug: string;
  run: number | string;
  run_url: string;
  title: string;
  topic?: string;
  date: string;
  duration?: number;
  genre?: string;
  format?: string;
};

export async function readIndex(file: string): Promise<IndexEntry[]> {
  const text = await gh<string | null>(`/contents/${file}?ref=${env.videosBranch()}`, { raw: true, allow404: true });
  if (!text) return [];
  try {
    const data = JSON.parse(text);
    return Array.isArray(data) ? data.filter((e) => e && typeof e === "object") : [];
  } catch {
    return [];
  }
}

export function videoUrl(dir: string, file: string) {
  return `https://github.com/${env.repo()}/raw/${env.videosBranch()}/${dir}/${file}`;
}

export type Run = {
  id: number;
  run_number: number;
  name: string;
  event: string;
  status: "queued" | "in_progress" | "completed" | string;
  conclusion: "success" | "failure" | "cancelled" | "skipped" | "timed_out" | null;
  created_at: string;
  updated_at: string;
  html_url: string;
};

export async function listRuns(workflowFile: string, perPage = 12): Promise<Run[]> {
  const data = await gh<{ workflow_runs: Run[] }>(`/actions/workflows/${workflowFile}/runs?per_page=${perPage}&exclude_pull_requests=true`);
  return data.workflow_runs;
}

/** Starts a workflow_dispatch run on the workflows branch. Needs a token with Actions: read and write. */
export async function dispatchWorkflow(workflowFile: string, inputs: Record<string, string> = {}): Promise<void> {
  await gh<void>(`/actions/workflows/${workflowFile}/dispatches`, {
    method: "POST",
    body: JSON.stringify({ ref: env.workflowsBranch(), inputs }),
  });
}

export type Job = { id: number; name: string; status: string; conclusion: string | null; html_url: string; completed_at: string | null };

export async function listJobs(runId: number): Promise<Job[]> {
  const data = await gh<{ jobs: Job[] }>(`/actions/runs/${runId}/jobs?per_page=100`);
  return data.jobs;
}

export type Issue = { number: number; title: string; html_url: string; created_at: string };

export async function openFailureIssues(): Promise<Issue[]> {
  const data = await gh<Issue[]>("/issues?state=open&labels=pipeline-failure&per_page=20");
  return data;
}

export function actionsUrl(workflowFile: string) {
  return `https://github.com/${env.repo()}/actions/workflows/${workflowFile}`;
}

export function secretsSettingsUrl() {
  return `https://github.com/${env.repo()}/settings/secrets/actions`;
}
