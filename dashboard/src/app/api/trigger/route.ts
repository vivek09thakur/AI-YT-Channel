import { NextResponse, type NextRequest } from "next/server";
import { createHash, timingSafeEqual } from "node:crypto";
import { WORKFLOWS } from "@/lib/model";
import { decide, type Decision } from "@/lib/trigger";
import { dispatchWorkflow, listRuns, readIndex, GitHubError } from "@/lib/github";
import { nowIST, todayUTC } from "@/lib/state";
import { ConfigError, env } from "@/lib/env";
import { fmtClock } from "@/lib/time";

// External trigger for the daily workflows, for when GitHub's own cron does not create scheduled runs.
// Vercel's scheduler (the "schedules" entry in vercel.json) calls GET /api/trigger every 15 minutes, 7 to 11 am and
// 3 to 6 pm IST,
// with "Authorization: Bearer <CRON_SECRET>"; any other scheduler can do the same with TRIGGER_SECRET. The route
// works out which workflow is due right now and starts it with workflow_dispatch and auto=true, so the workflow's
// guard job applies exactly as it does for a scheduled slot.
//   Authorization: Bearer <secret>   (or header x-trigger-key, or ?key=)
//   ?dry=1          report what would be started, start nothing
//   ?workflow=nlm   only this workflow (nlm | story | stickman)
//   ?formats=both   story only: shorts | landscape | both (the workflow's own default, shorts, applies when omitted)

export const maxDuration = 30;

const STORY_FORMATS = ["shorts", "landscape", "both"] as const;

function authorized(req: NextRequest, expected: string[]) {
  const header = req.headers.get("authorization");
  const given = (header ? header.replace(/^Bearer\s+/i, "") : null) ?? req.headers.get("x-trigger-key") ?? req.nextUrl.searchParams.get("key") ?? "";
  const a = createHash("sha256").update(given).digest();
  return expected.some((s) => timingSafeEqual(a, createHash("sha256").update(s).digest()));
}

function minutesSince(iso: string, now: number) {
  return Math.max(0, Math.round((now - new Date(iso).getTime()) / 60_000));
}

async function handle(req: NextRequest) {
  const secrets = env.triggerSecrets();
  if (secrets.length === 0) return NextResponse.json({ error: "CRON_SECRET (or TRIGGER_SECRET) is not set on the server" }, { status: 503 });
  if (!authorized(req, secrets)) return NextResponse.json({ error: "wrong or missing key" }, { status: 401 });

  const dry = req.nextUrl.searchParams.get("dry") === "1";
  const only = req.nextUrl.searchParams.get("workflow");
  const formats = req.nextUrl.searchParams.get("formats");
  if (formats && !(STORY_FORMATS as readonly string[]).includes(formats)) {
    return NextResponse.json({ error: `formats must be one of ${STORY_FORMATS.join(", ")}` }, { status: 400 });
  }
  const now = new Date();
  const ist = nowIST(now);
  const today = todayUTC(now);
  const results: (Decision & { dry: boolean })[] = [];

  try {
    for (const def of WORKFLOWS) {
      if (only && def.id !== only) continue;
      if (def.paused) {
        results.push({ ...decide(def, { nowIST: ist, publishedToday: 0 }), dry });
        continue;
      }
      const [entries, runs] = await Promise.all([readIndex(def.index), listRuns(def.file, 10)]);
      const active = runs.find((r) => r.status !== "completed");
      const latest = runs[0];
      const d = decide(def, {
        nowIST: ist,
        publishedToday: entries.filter((e) => e.date === today).length,
        activeRunUrl: active?.html_url,
        lastRunStartedMinAgo: latest ? minutesSince(latest.created_at, now.getTime()) : undefined,
      });
      if (d.action === "dispatch" && !dry) {
        const inputs: Record<string, string> = { auto: "true" };
        if (formats && def.id === "story") inputs.formats = formats;
        await dispatchWorkflow(def.file, inputs);
      }
      results.push({ ...d, dry });
    }
  } catch (e) {
    if (e instanceof ConfigError) return NextResponse.json({ error: e.message, results }, { status: 503 });
    if (e instanceof GitHubError) return NextResponse.json({ error: `GitHub: ${e.message} (${e.path})`, results }, { status: 502 });
    throw e;
  }

  return NextResponse.json({
    time: `${fmtClock(ist)} IST`,
    date: today,
    started: results.filter((r) => r.action === "dispatch").map((r) => r.workflow),
    results,
  });
}

export const GET = handle;
export const POST = handle;
