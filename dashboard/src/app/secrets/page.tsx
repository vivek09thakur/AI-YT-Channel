import { redirect } from "next/navigation";
import type { Metadata } from "next";
import { Suspense } from "react";
import { Loading } from "@/components/Loading";
import { Problem } from "@/components/Problem";
import { SecretsView } from "@/components/SecretsView";
import { TopBar } from "@/components/TopBar";
import { getSession } from "@/lib/auth";
import { env } from "@/lib/env";
import { listSecrets, listVariables, secretsSettingsUrl } from "@/lib/github";
import { buildSecretSections } from "@/lib/secrets";
import { accountsFromSecrets, parseMapping } from "@/lib/state";

export const metadata: Metadata = { title: "Secrets" };

export default function Page() {
  return (
    <Suspense fallback={<Loading>Loading secrets from GitHub</Loading>}>
      <SecretsPage />
    </Suspense>
  );
}

async function SecretsPage() {
  const session = await getSession();
  if (!session) redirect("/login");
  let secrets, variables;
  try {
    [secrets, variables] = await Promise.all([listSecrets(), listVariables()]);
  } catch (e) {
    return (
      <>
        <TopBar session={session} current="secrets" />
        <Problem error={e} />
      </>
    );
  }
  const mapping = parseMapping(variables.find((v) => v.name === env.accountsVar())?.value);
  const accounts = accountsFromSecrets(secrets, mapping);
  const groups = buildSecretSections(
    secrets.map((s) => ({ name: s.name, updatedAt: s.updated_at })),
    variables.map((v) => ({ name: v.name, value: v.value, updatedAt: v.updated_at })),
    accounts,
    env.accountsVar(),
  );
  return (
    <div className="h-dvh flex flex-col">
      <TopBar session={session} current="secrets" summary={<>{secrets.length} secrets, {variables.length} variables in {env.repo()}</>} />
      <SecretsView groups={groups} settingsUrl={secretsSettingsUrl()} />
    </div>
  );
}
