"use client";

import { useSyncExternalStore } from "react";
import { FiMoon, FiSun } from "react-icons/fi";

type Theme = "light" | "dark";

const STORAGE_KEY = "theme";
const EVENT = "themechange";
const query = () => window.matchMedia("(prefers-color-scheme: dark)");

/** The scheme actually in effect: an explicit choice on <html>, else the system preference. */
function current(): Theme {
  const chosen = document.documentElement.dataset.theme;
  if (chosen === "light" || chosen === "dark") return chosen;
  return query().matches ? "dark" : "light";
}

function subscribe(onChange: () => void) {
  const mq = query();
  mq.addEventListener("change", onChange);
  window.addEventListener(EVENT, onChange);
  return () => {
    mq.removeEventListener("change", onChange);
    window.removeEventListener(EVENT, onChange);
  };
}

function apply(theme: Theme) {
  document.documentElement.dataset.theme = theme;
  try {
    localStorage.setItem(STORAGE_KEY, theme);
  } catch {
    // Private mode or storage disabled: the choice still applies for this page.
  }
  window.dispatchEvent(new Event(EVENT));
}

export function ThemeToggle({ className = "" }: { className?: string }) {
  const theme = useSyncExternalStore(subscribe, current, () => null);
  const next: Theme = theme === "dark" ? "light" : "dark";
  return (
    <button type="button" className={`btn btn-quiet btn-icon ${className}`.trim()} aria-label={theme ? `Switch to ${next} mode` : "Switch theme"} title={theme ? `Switch to ${next} mode` : undefined} onClick={() => apply(next)}>
      {theme === "dark" ? <FiSun aria-hidden /> : <FiMoon aria-hidden />}
    </button>
  );
}
