
export type Group = "nlm" | "story" | "stickman";
export type Platform = "youtube" | "instagram";

export type WorkflowDef = {
  id: Group;
  title: string;
  lane: string;
  subtitle: string;
  file: string;
  index: string;
  dueIST: string[];
  slotsIST: string[];
  target: number;
  video: string;
  needs: string;
};

function every30(from: string, to: string): string[] {
  const toMin = (t: string) => Number(t.slice(0, 2)) * 60 + Number(t.slice(3));
  const out: string[] = [];
  for (let m = toMin(from); m <= toMin(to); m += 30) {
    out.push(`${String(Math.floor(m / 60)).padStart(2, "0")}:${String(m % 60).padStart(2, "0")}`);
  }
  return out;
}

export const WORKFLOWS: WorkflowDef[] = [
  {
    id: "nlm",
    title: "Fact short",
    lane: "Fact",
    subtitle: "NotebookLM video overview",
    file: "notebooklm-short.yml",
    index: "nlm.json",
    dueIST: ["09:07", "15:07"],
    slotsIST: every30("09:07", "20:07"),
    target: 2,
    video: "reel.mp4",
    needs: "NOTEBOOKLM_MASTER_TOKEN_JSON",
  },
  {
    id: "story",
    title: "Mythology story",
    lane: "Mythology",
    subtitle: "Folk-art narrated story",
    file: "generate-video.yml",
    index: "videos.json",
    dueIST: ["11:17", "16:47"],
    slotsIST: every30("11:17", "19:47"),
    target: 2,
    video: "shorts.mp4",
    needs: "one LLM key",
  },
  {
    id: "stickman",
    title: "Stickman explainer",
    lane: "Explainer",
    subtitle: "Stick-figure fact reel",
    file: "generate-stickman-reel.yml",
    index: "stickman.json",
    dueIST: ["13:27", "17:57"],
    slotsIST: every30("13:27", "19:57"),
    target: 2,
    video: "reel.mp4",
    needs: "one LLM key",
  },
];

export const GROUPS = WORKFLOWS.map((w) => w.id);

export const PLATFORMS: Record<Platform, { label: string; short: string; prefix: string }> = {
  youtube: { label: "YouTube", short: "YT", prefix: "YT_USER" },
  instagram: { label: "Instagram", short: "IG", prefix: "IG_USER" },
};

export type FieldKind = "secret" | "text" | "group" | "privacy" | "name";
export type FieldDef = {
  suffix: string;
  label: string;
  kind: FieldKind;
  required?: boolean;
  sharedFallback?: string;
  help?: string;
};

export const ACCOUNT_FIELDS: Record<Platform, FieldDef[]> = {
  youtube: [
    { suffix: "NAME", label: "Channel name", kind: "name", help: "Shown here and in the upload job summary" },
    { suffix: "FOR", label: "Posts videos from", kind: "group" },
    {
      suffix: "REFRESH_TOKEN",
      label: "Refresh token",
      kind: "secret",
      required: true,
      help: "python pipeline/notebooklm/yt_get_refresh_token.py --client-id ID --client-secret SECRET, logged in as this channel",
    },
    { suffix: "CLIENT_ID", label: "OAuth client id", kind: "secret", sharedFallback: "YT_CLIENT_ID", help: "Leave empty to use the shared YT_CLIENT_ID" },
    { suffix: "CLIENT_SECRET", label: "OAuth client secret", kind: "secret", sharedFallback: "YT_CLIENT_SECRET", help: "Leave empty to use the shared YT_CLIENT_SECRET" },
    { suffix: "PRIVACY", label: "Upload privacy", kind: "privacy", help: "Empty = the workflow's yt_privacy input (public)" },
  ],
  instagram: [
    { suffix: "NAME", label: "Page name", kind: "name", help: "Shown here and in the upload job summary" },
    { suffix: "FOR", label: "Posts videos from", kind: "group" },
    { suffix: "ID", label: "Instagram account id", kind: "secret", required: true, help: "Numeric id of the professional account (guide section 2)" },
    { suffix: "TOKEN", label: "Access token", kind: "secret", required: true, help: "Long-lived token with instagram_business_content_publish" },
  ],
};

export const LEGACY: Record<Platform, { key: string; fields: FieldDef[] }> = {
  youtube: {
    key: "YT_DEFAULT",
    fields: [
      { suffix: "YT_FOR", label: "Posts videos from", kind: "group" },
      { suffix: "YT_REFRESH_TOKEN", label: "Refresh token", kind: "secret", required: true },
    ],
  },
  instagram: {
    key: "IG_DEFAULT",
    fields: [
      { suffix: "IG_FOR", label: "Posts videos from", kind: "group" },
      { suffix: "IG_USER_ID", label: "Instagram account id", kind: "secret", required: true },
      { suffix: "IG_ACCESS_TOKEN", label: "Access token", kind: "secret", required: true },
    ],
  },
};

export const SHARED_YT = ["YT_CLIENT_ID", "YT_CLIENT_SECRET"];

export type CatalogueItem = {
  name: string;
  type: "secret" | "variable";
  required: string;
  what: string;
  link?: string;
};

export const CATALOGUE: { section: string; items: CatalogueItem[] }[] = [
  {
    section: "Generation",
    items: [
      { name: "NOTEBOOKLM_MASTER_TOKEN_JSON", type: "secret", required: "Fact short", what: "NotebookLM login, one line" },
      { name: "GEMINI_API_KEY", type: "secret", required: "one LLM key", what: "Google AI Studio, free", link: "https://aistudio.google.com/apikey" },
      { name: "MISTRAL_API_KEY", type: "secret", required: "one LLM key", what: "Mistral", link: "https://console.mistral.ai/api-keys" },
      { name: "CEREBRAS_API_KEY", type: "secret", required: "one LLM key", what: "Cerebras, free tier", link: "https://cloud.cerebras.ai" },
      { name: "META_AI_API", type: "secret", required: "one LLM key", what: "Meta Model API, paid", link: "https://dev.meta.ai" },
      { name: "OPENROUTER_API_KEY", type: "secret", required: "one LLM key", what: "OpenRouter, needs credits", link: "https://openrouter.ai/settings/keys" },
      { name: "OPENAI_API_KEY", type: "secret", required: "one LLM key", what: "OpenAI, needs credits", link: "https://platform.openai.com/api-keys" },
      { name: "ANTHROPIC_API_KEY", type: "secret", required: "one LLM key", what: "Anthropic, needs credits", link: "https://console.anthropic.com" },
      { name: "AZURE_SPEECH_KEY", type: "secret", required: "optional", what: "Azure voice, else free edge-tts" },
      { name: "AZURE_SPEECH_REGION", type: "variable", required: "with Azure key", what: "Azure region, e.g. centralindia" },
      { name: "BILLING_TOKEN", type: "secret", required: "optional", what: "Stops a run when Actions minutes run out", link: "https://github.com/settings/personal-access-tokens" },
      { name: "ACTIONS_INCLUDED_MINUTES", type: "variable", required: "optional", what: "Monthly minutes, default 2000" },
      { name: "ACTIONS_ALLOW_OVERAGE", type: "variable", required: "optional", what: "1 = keep running on paid minutes" },
    ],
  },
  {
    section: "Uploads",
    items: [
      { name: "YT_CLIENT_ID", type: "secret", required: "for YouTube", what: "Google OAuth client, shared by every channel" },
      { name: "YT_CLIENT_SECRET", type: "secret", required: "for YouTube", what: "Secret of that client" },
      { name: "IG_GRAPH_HOST", type: "variable", required: "optional", what: "graph.facebook.com or graph.instagram.com" },
      { name: "YT_ACCOUNTS_JSON", type: "secret", required: "alternative", what: "JSON channel list, not shown on the board" },
      { name: "IG_ACCOUNTS_JSON", type: "secret", required: "alternative", what: "JSON account list, not shown on the board" },
    ],
  },
];

export const KNOWN_NAMES = new Set([
  ...CATALOGUE.flatMap((s) => s.items.map((i) => i.name)),
  ...Object.values(LEGACY).flatMap((l) => l.fields.map((f) => f.suffix)),
]);

export const ACCOUNT_KEY_RE = /^(YT_USER|IG_USER)(\d+)_([A-Z_]+)$/;

export function parseGroups(raw: string | undefined | null): Group[] {
  if (!raw) return [];
  const parts = raw
    .split(/[,\s]+/)
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);
  if (parts.includes("all")) return [];
  return parts.filter((p): p is Group => (GROUPS as string[]).includes(p));
}
