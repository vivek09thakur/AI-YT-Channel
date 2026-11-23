import { redirect } from "next/navigation";
import type { Metadata } from "next";
import { Suspense } from "react";
import { Loading } from "@/components/Loading";
import { Problem } from "@/components/Problem";
import { Runs } from "@/components/Runs";
import { TopBar } from "@/components/TopBar";
import { getSession } from "@/lib/auth";
import { allActionsUrl } from "@/lib/github";
import { loadOverview } from "@/lib/state";

export const metadata: Metadata = { title: "Runs" };

export default function Page() {
  return (
    <Suspense fallback={<Loading>Loading runs from GitHub</Loading>}>
      <RunsPage />
    </Suspense>
  );
}

async function RunsPage() {
  const session = await getSession();
  if (!session) redirect("/login");

  let overview;
  try {
    overview = await loadOverview();
  } catch (e) {
    return (
      <>
        <TopBar session={session} current="runs" />
        <Problem error={e} />
      </>
    );
  }

  const posted = overview.workflows.reduce((n, w) => n + w.todayCount, 0);
  const target = overview.workflows.reduce((n, w) => n + w.target, 0);

  return (
    <div className="h-dvh flex flex-col">
      <TopBar session={session} current="runs" summary={<>{posted} of {target} videos posted today</>} />
      <Runs overview={overview} actionsUrl={allActionsUrl()} />
    </div>
  );
}
