import "server-only";
import { io } from "next/cache";
import { env } from "./env";
import {
  actionsUrl,
  listJobs,
  listRuns,
  listSecrets,
  listVariables,
  openFailureIssues,
  readIndex,
  videoUrl,
  type IndexEntry,
  type Job,
  type Run,
  type SecretMeta,
} from "./github";
import {
  ACCOUNT_FIELDS,
  ACCOUNT_KEY_RE,
  LEGACY,
  PLATFORMS,
  SHARED_YT,
  WORKFLOWS,
  parseGroups,
  type Group,
  type Platform,
} from "./model";

export type AccountMapping = Record<string, { name?: string; owner?: string; for?: Group[]; privacy?: string }>;

export type LinkSource = "recorded" | "observed" | "all" | "unknown";

export type FieldState = {
  suffix: string;
  secretName: string;
  present: boolean;
  updatedAt?: string;
};

export type AccountInfo = {
  key: string;
  matrixName: string;
  platform: Platform;
  legacy: boolean;
  name: string;
  nameRecorded: boolean;
  owner?: string;
  for: Group[] | null;
  forSource: LinkSource;
  privacy?: string;
  configured: boolean;
  missing: string[];
  fields: FieldState[];
  updatedAt?: string;
};

export type UploadOutcome = {
  platform: Platform;
  matrixName: string;
  accountKey: string;
  ok: boolean | null;
  jobUrl: string;
  variant: "landscape" | null;
};

export type Posted = {
  title: string;
  dir: string;
  run: number;
  runUrl: string;
  date: string;
  videoUrl: string;
  uploads: UploadOutcome[];
};

export type RunInfo = {
  id: number;
  number: number;
  status: string;
  conclusion: string | null;
  createdAt: string;
  url: string;
  event: string;
  durationSec: number | null;
};

export type DayCount = { date: string; count: number };

export type RunStats = {
  completed: number;
  ok: number;
  failed: number;
  typicalSec: number | null;
  today: { total: number; failed: number; running: number };
};

export type WorkflowInfo = {
  id: Group;
  title: string;
  lane: string;
  subtitle: string;
  file: string;
  target: number;
  todayCount: number;
  today: Posted[];
  recent: Posted[];
  runs: RunInfo[];
  /** Every fetched run from today, so each publishing window can be matched to its attempts. */
  todayRuns: RunInfo[];
  runStats: RunStats;
  week: DayCount[];
  observedAccounts: string[];
  latestRun: RunInfo | null;
  nextSlot: string | null;
  slots: string[];
  windows: [string, string][];
  due: string[];
  state: "done" | "partial" | "waiting" | "running" | "failed" | "idle";
  issueUrl: string | null;
  actionsUrl: string;
};

export type Overview = {
  date: string;
  nowIST: string;
  repo: string;
  accounts: AccountInfo[];
  workflows: WorkflowInfo[];
  sharedYt: boolean;
  secrets: SecretMeta[];
  variables: { name: string; value: string; updatedAt: string }[];
  mapping: AccountMapping;
  notes: string[];
};

const IST_OFFSET_MIN = 330;

export function todayUTC(d = new Date()) {
  return d.toISOString().slice(0, 10);
}

export function nowIST(d = new Date()) {
  const t = new Date(d.getTime() + IST_OFFSET_MIN * 60_000);
  return `${String(t.getUTCHours()).padStart(2, "0")}:${String(t.getUTCMinutes()).padStart(2, "0")}`;
}

export function parseMapping(raw: string | undefined): AccountMapping {
  if (!raw) return {};
  try {
    const data = JSON.parse(raw);
    if (Array.isArray(data)) {
      const out: AccountMapping = {};
      for (const a of data) if (a && a.key) out[a.key] = { name: a.name, owner: a.owner, for: a.for, privacy: a.privacy };
      return out;
    }
    return data && typeof data === "object" ? (data as AccountMapping) : {};
  } catch {
    return {};
  }
}

export function accountsFromSecrets(secrets: SecretMeta[], mapping: AccountMapping): AccountInfo[] {
  const byName = new Map(secrets.map((s) => [s.name, s]));
  const sharedYt = SHARED_YT.every((n) => byName.has(n));
  const keys = new Map<string, Platform>();
  for (const s of secrets) {
    const m = ACCOUNT_KEY_RE.exec(s.name);
    if (m) keys.set(`${m[1]}${m[2]}`, m[1] === "YT_USER" ? "youtube" : "instagram");
  }
  for (const key of Object.keys(mapping)) {
    if (key.startsWith("YT_USER")) keys.set(key, "youtube");
    else if (key.startsWith("IG_USER")) keys.set(key, "instagram");
  }

  const out: AccountInfo[] = [];
  for (const [key, platform] of keys) {
    const n = key.replace(PLATFORMS[platform].prefix, "");
    const fields: FieldState[] = ACCOUNT_FIELDS[platform].map((f) => {
      const secretName = `${key}_${f.suffix}`;
      const meta = byName.get(secretName);
      return { suffix: f.suffix, secretName, present: !!meta, updatedAt: meta?.updated_at };
    });
    const missing = ACCOUNT_FIELDS[platform]
      .filter((f) => f.required || f.sharedFallback)
      .filter((f) => {
        const own = byName.has(`${key}_${f.suffix}`);
        if (own) return false;
        if (f.sharedFallback) return !sharedYt;
        return true;
      })
      .map((f) => `${key}_${f.suffix}`);
    const map = mapping[key] ?? {};
    const hasFor = byName.has(`${key}_FOR`);
    const hasName = byName.has(`${key}_NAME`);
    const recorded = map.for ? parseGroups(map.for.join(",")) : null;
    const updated = fields.map((f) => f.updatedAt).filter(Boolean).sort().at(-1);
    out.push({
      key,
      matrixName: `user${n}`,
      platform,
      legacy: false,
      name: map.name || key,
      nameRecorded: !!map.name || !hasName,
      owner: map.owner,
      for: recorded ?? (hasFor ? null : []),
      forSource: recorded ? "recorded" : hasFor ? "unknown" : "all",
      privacy: map.privacy,
      configured: missing.length === 0,
      missing,
      fields,
      updatedAt: updated,
    });
  }

  for (const platform of Object.keys(LEGACY) as Platform[]) {
    const legacy = LEGACY[platform];
    const required = legacy.fields.filter((f) => f.required);
    const anyPresent = required.some((f) => byName.has(f.suffix));
    if (!anyPresent) continue;
    const fields: FieldState[] = legacy.fields.map((f) => {
      const meta = byName.get(f.suffix);
      return { suffix: f.suffix, secretName: f.suffix, present: !!meta, updatedAt: meta?.updated_at };
    });
    const missing = required.filter((f) => !byName.has(f.suffix)).map((f) => f.suffix);
    if (platform === "youtube" && !sharedYt) missing.push(...SHARED_YT.filter((n) => !byName.has(n)));
    const forName = legacy.fields.find((f) => f.kind === "group")!.suffix;
    const map = mapping[legacy.key] ?? {};
    const recorded = map.for ? parseGroups(map.for.join(",")) : null;
    const hasFor = byName.has(forName);
    out.push({
      key: legacy.key,
      matrixName: "default",
      platform,
      legacy: true,
      name: map.name || `${PLATFORMS[platform].label} (legacy default)`,
      nameRecorded: true,
      owner: map.owner,
      for: recorded ?? (hasFor ? null : []),
      forSource: recorded ? "recorded" : hasFor ? "unknown" : "all",
      configured: missing.length === 0,
      missing,
      fields,
      updatedAt: fields.map((f) => f.updatedAt).filter(Boolean).sort().at(-1),
    });
  }

  return out.sort((a, b) => (a.platform === b.platform ? a.key.localeCompare(b.key, undefined, { numeric: true }) : a.platform === "youtube" ? -1 : 1));
}

const UPLOAD_JOB_RE = /^(?:(.*?) \/ )?Upload (youtube|instagram)\/(\S+)\s*$/;
const OBSERVE_RUNS = 5;
const jobsCache = new Map<number, Promise<Job[]>>();

function jobsFor(run: Run): Promise<Job[]> {
  if (run.status !== "completed") return listJobs(run.id).catch(() => []);
  let p = jobsCache.get(run.id);
  if (!p) {
    if (jobsCache.size > 300) jobsCache.clear();
    p = listJobs(run.id).catch(() => [] as Job[]);
    jobsCache.set(run.id, p);
  }
  return p;
}

function parseUploads(jobs: Job[]): UploadOutcome[] {
  return jobs
    .map((j) => ({ j, m: UPLOAD_JOB_RE.exec(j.name) }))
    .filter((x) => x.m)
    .map(({ j, m }) => {
      const platform = m![2] as Platform;
      const matrixName = m![3];
      const num = /^user(\d+)$/.exec(matrixName)?.[1];
      const accountKey = num ? `${PLATFORMS[platform].prefix}${num}` : LEGACY[platform].key;
      const ok = j.status !== "completed" ? null : j.conclusion === "success";
      const variant = /landscape/i.test(m![1] ?? "") ? "landscape" : null;
      return { platform, matrixName, accountKey, ok, jobUrl: j.html_url, variant };
    });
}

function toRunInfo(r: Run): RunInfo {
  const durationSec = r.status === "completed" ? Math.max(0, Math.round((Date.parse(r.updated_at) - Date.parse(r.created_at)) / 1000)) : null;
  return { id: r.id, number: r.run_number, status: r.status, conclusion: r.conclusion, createdAt: r.created_at, url: r.html_url, event: r.event, durationSec };
}

export function runStats(runs: RunInfo[], today: string): RunStats {
  const isFailure = (r: RunInfo) => r.status === "completed" && r.conclusion !== "success" && r.conclusion !== "skipped" && r.conclusion !== "cancelled";
  const done = runs.filter((r) => r.status === "completed" && r.conclusion !== "skipped" && r.conclusion !== "cancelled");
  const ok = done.filter((r) => r.conclusion === "success");
  const secs = ok.map((r) => r.durationSec).filter((s): s is number => s !== null).sort((a, b) => a - b);
  const todays = runs.filter((r) => r.createdAt.slice(0, 10) === today);
  return {
    completed: done.length,
    ok: ok.length,
    failed: done.length - ok.length,
    typicalSec: secs.length ? secs[Math.floor(secs.length / 2)] : null,
    today: {
      total: todays.length,
      failed: todays.filter(isFailure).length,
      running: todays.filter((r) => r.status !== "completed").length,
    },
  };
}

export function weekCounts(entries: { date: string }[], today: string, days = 7): DayCount[] {
  const end = Date.parse(`${today}T00:00:00Z`);
  return Array.from({ length: days }, (_, i) => {
    const date = new Date(end - (days - 1 - i) * 86_400_000).toISOString().slice(0, 10);
    return { date, count: entries.filter((e) => e.date === date).length };
  });
}

async function uploadsForRun(run: Run | undefined): Promise<UploadOutcome[]> {
  if (!run) return [];
  return parseUploads(await jobsFor(run));
}

async function observedAccounts(runs: Run[]): Promise<string[]> {
  const completed = runs.filter((r) => r.status === "completed").slice(0, OBSERVE_RUNS);
  const uploads = await Promise.all(completed.map((r) => uploadsForRun(r)));
  return [...new Set(uploads.flat().map((u) => u.accountKey))];
}

export function nextSlot(slots: string[], due: string[], now: string, posted: number, target: number): string | null {
  if (posted >= target) return null;
  const dueBy = (slot: string) => Math.max(1, due.filter((d) => d <= slot).length);
  return slots.find((s) => s > now && dueBy(s) > posted) ?? null;
}

async function workflowInfo(
  def: (typeof WORKFLOWS)[number],
  today: string,
  now: string,
  issues: { title: string; html_url: string }[],
): Promise<WorkflowInfo> {
  const [entries, runs] = await Promise.all([
    readIndex(def.index).catch(() => [] as IndexEntry[]),
    listRuns(def.file, 20).catch(() => [] as Run[]),
  ]);
  const todayEntries = entries.filter((e) => e.date === today);
  const runByNumber = new Map(runs.map((r) => [r.run_number, r]));
  const runById = new Map(runs.map((r) => [r.id, r]));
  const findRun = (e: IndexEntry) => {
    const id = Number(/\/runs\/(\d+)/.exec(e.run_url ?? "")?.[1]);
    return runById.get(id) ?? runByNumber.get(Number(e.run));
  };

  const toPosted = async (e: IndexEntry): Promise<Posted> => ({
    title: e.title || e.slug,
    dir: e.dir,
    run: Number(e.run),
    runUrl: e.run_url,
    date: e.date,
    videoUrl: videoUrl(e.dir, def.video),
    uploads: e.date === today ? await uploadsForRun(findRun(e)) : [],
  });

  const todayPosted = await Promise.all(todayEntries.map(toPosted));
  const recent = await Promise.all(entries.filter((e) => e.date !== today).slice(0, 4).map(toPosted));
  const observed = await observedAccounts(runs);
  const runInfos = runs.map(toRunInfo);
  const latest = runInfos[0] ?? null;
  const remaining = def.target - todayPosted.length;
  const slot = nextSlot(def.slotsIST, def.dueIST, now, todayPosted.length, def.target);

  let state: WorkflowInfo["state"] = "idle";
  if (remaining <= 0) state = "done";
  else if (latest && latest.status !== "completed") state = "running";
  else if (latest && latest.createdAt.slice(0, 10) === today && latest.conclusion === "failure") state = "failed";
  else if (todayPosted.length > 0) state = "partial";
  else if (slot) state = "waiting";

  const issue = issues.find((i) => i.title.toLowerCase().includes(def.title.toLowerCase()) || i.title.toLowerCase().includes(def.id));
  return {
    id: def.id,
    title: def.title,
    lane: def.lane,
    subtitle: def.subtitle,
    file: def.file,
    target: def.target,
    todayCount: todayPosted.length,
    today: todayPosted,
    recent,
    runs: runInfos.slice(0, 6),
    todayRuns: runInfos.filter((r) => r.createdAt.slice(0, 10) === today),
    runStats: runStats(runInfos, today),
    week: weekCounts(entries, today),
    observedAccounts: observed,
    latestRun: latest,
    nextSlot: slot,
    slots: def.slotsIST,
    windows: def.windowsIST,
    due: def.dueIST,
    state,
    issueUrl: issue?.html_url ?? null,
    actionsUrl: actionsUrl(def.file),
  };
}

export async function loadOverview(): Promise<Overview> {
  await io();
  const today = todayUTC();
  const now = nowIST();
  const [secrets, variables, issues] = await Promise.all([
    listSecrets(),
    listVariables(),
    openFailureIssues().catch(() => []),
  ]);
  const mapping = parseMapping(variables.find((v) => v.name === env.accountsVar())?.value);
  const accounts = accountsFromSecrets(secrets, mapping);
  const workflows = await Promise.all(WORKFLOWS.map((w) => workflowInfo(w, today, now, issues)));
  for (const acc of accounts) {
    if (acc.forSource !== "unknown") continue;
    const seen = workflows.filter((w) => w.observedAccounts.includes(acc.key)).map((w) => w.id);
    if (seen.length) {
      acc.for = seen;
      acc.forSource = "observed";
    }
  }

  const names = new Set(secrets.map((s) => s.name));
  const notes: string[] = [];
  const list = (keys: string[]) => (keys.length > 1 ? `${keys.slice(0, -1).join(", ")} and ${keys.at(-1)}` : keys[0]);
  for (const n of ["YT_ACCOUNTS_JSON", "IG_ACCOUNTS_JSON"]) if (names.has(n)) notes.push(`${n} is set: accounts inside it also receive videos but are not shown on the board.`);
  const unnamed = accounts.filter((a) => !a.nameRecorded).map((a) => a.key);
  if (unnamed.length) notes.push(`${list(unnamed)}: the name is stored on GitHub but cannot be read back. Open each one and type the name to show it on the board.`);
  const observed = accounts.filter((a) => a.forSource === "observed").map((a) => a.key);
  if (observed.length) notes.push(`${list(observed)}: linked from the upload jobs of recent runs. Open each one and save it once to record the link.`);
  const unlinked = accounts.filter((a) => a.forSource === "unknown").map((a) => a.key);
  if (unlinked.length) notes.push(`${list(unlinked)}: no recent run has posted here, so it is not linked to a workflow yet. Open it and tick its workflows.`);
  for (const wf of workflows) {
    if (wf.state === "failed" && wf.latestRun) notes.push(`${wf.title}: the latest run failed. Open the workflow to see the run.`);
    if (wf.issueUrl) notes.push(`${wf.title}: there is an open pipeline-failure issue.`);
  }

  return {
    date: today,
    nowIST: now,
    repo: env.repo(),
    accounts,
    workflows,
    sharedYt: SHARED_YT.every((n) => names.has(n)),
    secrets,
    variables: variables.map((v) => ({ name: v.name, value: v.value, updatedAt: v.updated_at })),
    mapping,
    notes,
  };
}
