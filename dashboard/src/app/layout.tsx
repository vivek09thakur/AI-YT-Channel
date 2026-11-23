import type { Metadata, Viewport } from "next";
import { IBM_Plex_Sans } from "next/font/google";
import "./globals.css";

const plex = IBM_Plex_Sans({ subsets: ["latin"], weight: ["400", "500", "600"], variable: "--font-plex", display: "swap" });

const name = "AI YT Channel";
const description = "The production board for the daily video workflows: what posted today, where it went, and which runs need a look.";
const siteUrl = process.env.VERCEL_PROJECT_PRODUCTION_URL ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}` : "http://localhost:3000";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: { default: name, template: `%s | ${name}` },
  description,
  applicationName: name,
  robots: { index: false, follow: false },
  openGraph: { type: "website", siteName: name, title: name, description, url: "/" },
  twitter: { card: "summary_large_image", title: name, description },
};

export const viewport: Viewport = {
  colorScheme: "light dark",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0e1013" },
  ],
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`h-full ${plex.variable}`}>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
