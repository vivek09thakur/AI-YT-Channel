import "server-only";
import fs from "node:fs";
import path from "node:path";
import GithubSlugger from "github-slugger";
import { imageSize } from "image-size";

export type DocPage = { slug: string; file: string; title: string; blurb: string };
export type Heading = { id: string; text: string; depth: number };

/** The handbook, in reading order. Markdown lives in dashboard/content/docs; each repo folder's README is a stub that links here. */
export const PAGES: DocPage[] = [
  { slug: "overview", file: "overview.md", title: "Overview", blurb: "What the pipeline makes, setup, which account gets which video, every secret and variable, costs." },
  { slug: "notebooklm", file: "notebooklm.md", title: "NotebookLM short", blurb: "NotebookLM token, Instagram and YouTube upload with screenshots, more accounts, run options, jobs, errors." },
  { slug: "story", file: "story.md", title: "Story video", blurb: "The folk-art animation engine behind the story video and how to use it locally." },
  { slug: "stickman", file: "stickman.md", title: "Stickman fact reel", blurb: "The stickman reel action: schedule, manual runs, pipeline, local checks." },
  { slug: "dashboard", file: "dashboard.md", title: "Dashboard", blurb: "Environment variables, running locally, deploying on Vercel, the external trigger, how accounts map to secrets." },
];

export const docHref = (slug: string) => (slug === "overview" ? "/docs" : `/docs/${slug}`);

export function findPage(slug: string): DocPage | undefined {
  return PAGES.find((p) => p.slug === slug);
}

export function readDoc(slug: string): { page: DocPage; markdown: string; headings: Heading[] } | null {
  const page = findPage(slug);
  if (!page) return null;
  const markdown = fs.readFileSync(path.join(process.cwd(), "content", "docs", page.file), "utf8");
  return { page, markdown, headings: extractHeadings(markdown) };
}

/** Section list for the "On this page" rail. Ids follow github-slugger, the same as rehype-slug, so GitHub-style anchors keep working. */
export function extractHeadings(markdown: string, depths: number[] = [2]): Heading[] {
  const slugger = new GithubSlugger();
  const out: Heading[] = [];
  let fence: string | null = null;
  for (const raw of markdown.split(/\r?\n/)) {
    const line = raw.trimEnd();
    const f = /^\s*(`{3,}|~{3,})/.exec(line);
    if (f) {
      if (!fence) fence = f[1][0];
      else if (f[1][0] === fence) fence = null;
      continue;
    }
    if (fence) continue;
    const m = /^(#{1,6})\s+(.+?)\s*#*$/.exec(line);
    if (!m) continue;
    const text = plain(m[2]);
    const id = slugger.slug(text);
    if (depths.includes(m[1].length)) out.push({ id, text, depth: m[1].length });
  }
  return out;
}

function plain(md: string): string {
  return md
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/`([^`]*)`/g, "$1")
    .replace(/(\*\*|__)(.*?)\1/g, "$2")
    .replace(/(\*|_)(.*?)\1/g, "$2")
    .trim();
}

const sizes = new Map<string, { width: number; height: number } | null>();

/** Pixel size of a file under public/, so images in the docs reserve their space and anchors land where they should. */
export function publicImageSize(src: string): { width: number; height: number } | null {
  if (!src.startsWith("/") || src.includes("..")) return null;
  let hit = sizes.get(src);
  if (hit === undefined) {
    try {
      const { width, height } = imageSize(fs.readFileSync(path.join(process.cwd(), "public", src)));
      hit = width && height ? { width, height } : null;
    } catch {
      hit = null;
    }
    sizes.set(src, hit);
  }
  return hit;
}
