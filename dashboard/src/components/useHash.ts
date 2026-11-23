"use client";

import { useSyncExternalStore } from "react";

const subscribe = (cb: () => void) => {
  window.addEventListener("hashchange", cb);
  return () => window.removeEventListener("hashchange", cb);
};
const read = () => decodeURIComponent(window.location.hash.slice(1));

/** The URL fragment without its "#", kept in sync with the address bar; "" on the server. */
export function useHash() {
  return useSyncExternalStore(subscribe, read, () => "");
}

/** Replace the fragment without adding a history entry, and tell listeners. */
export function setHash(key: string) {
  window.history.replaceState(null, "", `#${key}`);
  window.dispatchEvent(new Event("hashchange"));
}
