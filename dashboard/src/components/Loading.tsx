export function Loading({ children }: { children: React.ReactNode }) {
  return (
    <div className="h-dvh flex flex-col">
      <div className="h-[52px] border-b border-line bg-inset" />
      <p className="p-6 text-ink-soft">{children}</p>
    </div>
  );
}
