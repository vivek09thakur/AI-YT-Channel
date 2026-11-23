import type { Metadata, Viewport } from "next";
import { Archivo_Black, Poppins, Roboto_Mono } from "next/font/google";
import "./globals.css";

const poppins = Poppins({ subsets: ["latin"], weight: ["400", "500", "600"], variable: "--font-poppins", display: "swap" });
const mono = Roboto_Mono({ subsets: ["latin"], weight: ["400", "500"], variable: "--font-roboto-mono", display: "swap" });
const archivo = Archivo_Black({ subsets: ["latin"], weight: "400", variable: "--font-archivo", display: "swap" });

// Applies the saved theme before first paint so a light/dark choice never flashes the other scheme.
const themeScript = `try{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}catch(e){}`;

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
    { media: "(prefers-color-scheme: light)", color: "#f6f7fb" },
    { media: "(prefers-color-scheme: dark)", color: "#151c29" },
  ],
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`h-full ${poppins.variable} ${mono.variable} ${archivo.variable}`} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
