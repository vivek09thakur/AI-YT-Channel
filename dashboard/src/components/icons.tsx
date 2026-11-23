import { FaInstagram, FaYoutube } from "react-icons/fa6";
import type { Platform } from "@/lib/model";

export function PlatformIcon({ platform, className }: { platform: Platform; className?: string }) {
  const Icon = platform === "youtube" ? FaYoutube : FaInstagram;
  return <Icon className={className} aria-label={platform === "youtube" ? "YouTube" : "Instagram"} />;
}
