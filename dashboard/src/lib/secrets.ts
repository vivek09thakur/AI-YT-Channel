import { ACCOUNT_FIELDS, CATALOGUE, LEGACY, type CatalogueItem, type Platform } from "@/lib/model";
import type { AccountInfo } from "@/lib/state";

export type SecretRow = { name: string; updatedAt: string };
export type VariableRow = { name: string; value: string; updatedAt: string };

export type Row = {
  name: string;
  type: "secret" | "variable";
  hint: string;
  link?: string;
  required: boolean;
  present: boolean;
  updatedAt?: string;
  value?: string;
};

export type SecretSection = { key: string; label: string; platform?: Platform; note?: string; rows: Row[] };

export function buildSecretSections(secrets: SecretRow[], variables: VariableRow[], accounts: AccountInfo[], accountsVar: string): SecretSection[][] {
  const secretMap = new Map(secrets.map((s) => [s.name, s]));
  const varMap = new Map(variables.map((v) => [v.name, v]));

  const row = (item: CatalogueItem): Row => {
    const required = item.required === "Fact short" || item.required === "for YouTube";
    if (item.type === "variable") {
      const v = varMap.get(item.name);
      return { name: item.name, type: "variable", hint: item.what, link: item.link, required, present: !!v, updatedAt: v?.updatedAt, value: v?.value };
    }
    const s = secretMap.get(item.name);
    return { name: item.name, type: "secret", hint: item.what, link: item.link, required, present: !!s, updatedAt: s?.updatedAt };
  };

  const shared: SecretSection[] = CATALOGUE.map((s) => ({
    key: s.section.toLowerCase(),
    label: s.section,
    rows: s.items.map(row).filter((r) => r.present || !s.items.find((i) => i.name === r.name)?.required.startsWith("alternative")),
  })).filter((s) => s.rows.length);

  const perAccount: SecretSection[] = accounts.map((acc) => {
    const fields = acc.legacy ? LEGACY[acc.platform].fields : ACCOUNT_FIELDS[acc.platform];
    const rows = fields
      .map((f): Row => {
        const name = acc.legacy ? f.suffix : `${acc.key}_${f.suffix}`;
        const s = secretMap.get(name);
        return { name, type: "secret", hint: f.kind === "group" && !s ? "Posts videos from, empty = every workflow" : f.label, required: !!f.required, present: !!s, updatedAt: s?.updatedAt };
      })
      .filter((r, i) => r.required || r.present || fields[i].kind === "group");
    return { key: acc.key, label: acc.name, platform: acc.platform, note: acc.legacy ? "legacy secrets" : acc.key, rows };
  });

  const known = new Set([
    ...CATALOGUE.flatMap((s) => s.items.map((i) => i.name)),
    ...accounts.flatMap((acc) => (acc.legacy ? LEGACY[acc.platform].fields.map((f) => f.suffix) : ACCOUNT_FIELDS[acc.platform].map((f) => `${acc.key}_${f.suffix}`))),
  ]);
  const otherSecrets = secrets.filter((s) => !known.has(s.name)).map<Row>((s) => ({ name: s.name, type: "secret", hint: "Not used by the workflows", required: false, present: true, updatedAt: s.updatedAt }));
  const otherVars = variables
    .filter((v) => !known.has(v.name))
    .map<Row>((v) => ({
      name: v.name,
      type: "variable",
      hint: v.name === accountsVar ? `Board names and links for ${accounts.length} accounts` : "Not used by the workflows",
      required: false,
      present: true,
      updatedAt: v.updatedAt,
      value: v.value,
    }));
  const other: SecretSection[] = otherSecrets.length || otherVars.length ? [{ key: "other", label: "Other", rows: [...otherSecrets, ...otherVars] }] : [];

  return [shared, perAccount, other].filter((g) => g.length);
}
