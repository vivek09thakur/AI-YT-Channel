import type { Metadata } from "next";
import { Doc } from "@/components/Doc";
import { DocsShell } from "@/components/DocsShell";
import { readDoc } from "@/lib/docs";

export const metadata: Metadata = {
  title: "Docs",
  description: "How the daily video workflows work, how to set them up, and where everything lives.",
};

export default function Page() {
  const doc = readDoc("overview")!;
  return (
    <DocsShell slug="overview" headings={doc.headings}>
      <Doc markdown={doc.markdown} />
    </DocsShell>
  );
}
