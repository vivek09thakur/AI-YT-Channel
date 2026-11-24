import { redirect } from "next/navigation";
import { Suspense } from "react";
import { Board } from "@/components/Board";
import { Loading } from "@/components/Loading";
import { Problem } from "@/components/Problem";
import { TopBar } from "@/components/TopBar";
import { getSession } from "@/lib/auth";
import { dailyTotals, loadOverview } from "@/lib/state";

export default function Page() {
  return (
    <Suspense fallback={<Loading>Loading the board from GitHub</Loading>}>
      <BoardPage />
    </Suspense>
  );
}

async function BoardPage() {
  const session = await getSession();
  if (!session) redirect("/login");

  let overview;
  try {
    overview = await loadOverview();
  } catch (e) {
    return (
      <>
        <TopBar session={session} current="board" />
        <Problem error={e} />
      </>
    );
  }

  const ready = overview.accounts.filter((a) => a.configured).length;
  const { posted, target } = dailyTotals(overview.workflows);

  return (
    <div className="h-dvh flex flex-col">
      <TopBar
        session={session}
        current="board"
        summary={
          <>
            {posted} of {target} videos posted today, {ready} of {overview.accounts.length} accounts ready
          </>
        }
      />
      <div className="flex-1 min-h-0 flex">
        <Board overview={overview} />
      </div>
    </div>
  );
}
