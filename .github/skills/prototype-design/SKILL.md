---
name: prototype-design
description: Stack-agnostic skill for designing and prototyping user interfaces in any repository — new screens in an existing product or a first UI from scratch. Use when asked to design, prototype, mock up, restyle or extend a UI; to extract a design language (tokens, components, patterns) from an existing codebase; or to review a screen for consistency, responsiveness and accessibility.
---

# Prototype Design Skills

A reusable skill for designing and prototyping UI. It is independent of framework (server-rendered HTML, React/Vue/Svelte, mobile, desktop) and of project — the rules describe the *result*, not the tooling.

**How to use**

- Starting a screen: follow the workflow in §1 and keep the checklists in §9 open.
- Joining an existing repo: run the *Discovery* step once, fill in the token table (§3.2) and stack conventions (§1, step 0) for that repo, and commit them next to this file.
- Reviewing a screen: use §9 "Definition of done" and §10 Do / Don't.
- To install as an agent skill, run `npx vivek-ai-skills prototype-design`, or copy this file to `.github/skills/prototype-design/SKILL.md` (or `.agents/skills/` / `.claude/skills/`).
- §12–14 are worked examples from other repositories. Read them as models of the *shape* of a Discovery record, never as values to copy.

---

## 1. Workflow

**Step 0 — Discover before you design (existing repo)**

1. Find the design source of truth: global stylesheet, theme file, design-token file, component library, or design file (Figma etc.).
2. Extract the values actually in use: font family and loaded weights, type sizes, colours, spacing values, border widths, radii, control heights, container widths, breakpoints, motion.
3. List the existing components and page patterns. Note which are reused and which are one-offs.
4. Record the **existing layout** — columns, panels, navigation, where each piece of content lives. This layout is preserved. The skill restyles and tidies *within* it; it does not merge, split, move or remove screens, columns or panels unless the user asks for that explicitly.
5. Record everything in the token table (§3.2). When values conflict, the most-used value wins; list the outliers under *Quirks*.
6. Record the stack conventions in one short table:

   | Concern | Where it lives | Rule |
   | --- | --- | --- |
   | Routes / screens | e.g. `main.py`, `src/pages/` | one function or file per screen |
   | Page markup | e.g. `templates/`, `src/components/` | one screen per file |
   | Shared styles | e.g. `static/style.css`, `theme.ts` | the only place tokens and reusable components are defined |
   | Page-only styles | local `<style>` / CSS module | only for rules no other screen needs |
   | Links to routes & assets | e.g. `url_for`, `<Link>`, router helpers | never hard-code paths |

7. No existing UI? Choose defaults from §3.2 and write them down **before** writing any markup.

**Step 1 — Define the job.** One sentence: *"This screen lets `<who>` `<do what>` so that `<outcome>`."* Name the single primary action, the inputs it needs, and every outcome: success, each error, empty, loading, not-allowed.

**Step 2 — Pick a page pattern** from §6. If a *new* screen fits none, split it into two screens. An existing screen keeps its layout; map each of its regions to a pattern instead.

**Step 3 — Wireframe in text first.** ASCII boxes are enough (notation in §6). Settle order, grouping and the position of the primary action before touching styles.

**Step 4 — Build from tokens and existing components.** Semantic HTML (or the platform's native controls) first, then styling. A rule a second screen will need goes in the shared styles; everything else stays local to the screen.

**Step 5 — Design every state**: default, hover, focus, active, disabled, loading, empty, error, success. A state you did not design will be shipped undesigned.

**Step 6 — Check** by actually rendering it (browser, emulator or screenshot), not by reading the code. Test at ~320, ~768 and ~1280 px wide; keyboard only; screen-reader labels; colour contrast; `prefers-reduced-motion`; light and dark theme if the product has both.

**Step 7 — Close the loop.** Review against §9, add a smoke test for the route/screen, and write any new token or component back into §3/§5 so the next prototype starts from it.

---

## 2. Design principles

1. **One screen, one job.** A *new* screen has one purpose and one primary action. Secondary things are links, not competing buttons. For an *existing* screen, keep the layout the user already has: treat each column or panel as its own job with its own single primary action, and do not restructure it.
2. **Hierarchy follows importance.** Size, weight, colour and position are spent on what matters most. One accent-coloured element per view.
3. **Consistency beats novelty.** Match what already exists before inventing. A new colour, size or component is allowed only when no existing token or component works — and then it is added to the tokens so it exists once.
4. **Quiet by default.** Restrained palette, small type scale, thin borders, no decoration that carries no meaning (shadows, gradients, icons for their own sake).
5. **Content first, chrome last.** When something does not fit, cut content or defer it (progressive disclosure) before adding scrolling, tabs or density.
6. **Feedback is honest and actionable.** Every action produces a visible response. Errors say what happened, the likely cause, and what the user can do next.
7. **Use the platform.** Native elements, real forms and links, semantic markup. Add JavaScript only when it buys something the user can feel.
8. **Accessible in the first draft.** Labels, contrast, focus, keyboard and touch targets are part of the design, not a retrofit.
9. **Mobile-first, few breakpoints.** Fluid widths with a maximum; add a breakpoint only when a layout genuinely changes.
10. **Fast and light.** One font family, minimal assets, no heavy framework for a prototype.

---

## 3. Design tokens

### 3.1 Rules for tokens

- Keep them few. A token exists because it is used in two or more places, or because it is the single value of its kind.
- Name by **role**, not by value: `--color-accent`, `--space-3` — not `--blue`, `--px-12`.
- Define them in one place (CSS custom properties, a theme object, platform resources) and reference them everywhere else.
- Changing a token should restyle the product; if it does not, the token is not being used.

### 3.2 Token table — fill in per repo

Copy this table into the repo (or fill it in here). *Value in this repo* comes from Discovery; *Default* is what to use when starting from nothing.

| Category | Token | Value in this repo | Default when starting fresh |
| --- | --- | --- | --- |
| Type | family | | one family + system fallback (`system-ui, sans-serif`) |
| Type | scale | | xs 12 · sm 13–14 · base 15–16 · lg 18–20 · xl 24–28 |
| Type | weights | | regular 400 · emphasis 600–700 (optional light 300) |
| Type | line-height | | 1.4–1.6 body · 1.2 headings |
| Colour | bg / surface | | white / white or 2–4 % grey |
| Colour | text / text-muted | | near-black / mid grey |
| Colour | border | | light grey (`#ddd`-ish) |
| Colour | accent / on-accent | | one brand colour / white |
| Colour | success / error / warning | | green / red / amber, muted |
| Colour | contrast | | ≥ 4.5:1 text · ≥ 3:1 UI and large text |
| Colour | dark theme | | optional; same token names, values swapped under one selector (`:root.dark` or `prefers-color-scheme`); never a second stylesheet |
| Space | base unit | | 4 px |
| Space | scale | | 4 · 8 · 12 · 16 · 24 · 32 · 48 |
| Shape | radius | | sm 4 · md 8 · pill 999 |
| Shape | border width | | 1 px |
| Size | control height | | 36–44 px (inputs and buttons equal) |
| Size | touch target | | ≥ 44 × 44 px hit area on touch; a smaller visible control (e.g. 40 px) must be padded to reach it. Never below 24 × 24 px (WCAG 2.2 minimum) |
| Size | icon | | 16 · 20 · 24 px; icon-only controls need an accessible name |
| Size | content max-width | | 360 (single form) · 640–720 (reading) · 1200 (dashboard) |
| Layout | breakpoints | | at most 2–3: 480 · 768 · 1024/1280 |
| Motion | duration / easing | | 100–200 ms · ease-out · honour `prefers-reduced-motion` |
| Elevation | shadow | | none, or one subtle shadow |
| Layers | z-index | | content 0 · sticky 10 · drawer 40 · modal 50 · toast 60 (no other values) |

### 3.3 Quirks (per repo)

List values or techniques found in the codebase that new screens must **not** copy, with the preferred alternative.

---

## 4. Layout

- Single column by default. Add columns only at ≥ 768 px and only when the content is genuinely parallel.
- Centre a max-width container; let it be fluid below its maximum (`width: min(100%, var(--content-w))`).
- Vertical rhythm comes from the spacing scale. No arbitrary pixel values.
- Group related controls visibly (card, fieldset). Keep the primary action at the end of the flow and full-width of its group on small screens.
- Let content define height. Avoid fixed heights and avoid global `overflow: hidden`; if content overflows, the design is wrong, not the scrollbar.
- Use a small, deliberate reset (`box-sizing: border-box; margin: 0`) and add spacing explicitly.

---

## 5. Component patterns

For each component: anatomy → rules → states. Reuse the repo's existing implementation when it has one; otherwise build it from tokens and register it.

**Container / card** — bordered or surfaced box that groups one task's controls. `1px` border, `radius-sm`, padding `space-4`, internal gap `space-2`. No nesting of cards.

**Text input** — label (always; visible or `aria-label` when space is tight) → control → helper text → error text. Height = control height, `1px` border, placeholder is an *example*, not the label. States: default, focus (visible ring, ≥ 2 px, accent), error (border + message), disabled.

**Primary button** — one per view. Pick **one** style for the product (filled accent or outlined accent) and never mix. Height = control height, label is a single verb. States: hover, focus-visible, active, disabled, loading (label changes, control stays the same size).

**Secondary button / link** — neutral border or plain text link. Used for "back", "cancel", "learn more". Never styled like the primary.

**Page title and subtitle** — title ≤ 6 words, `lg`/`xl` size; subtitle in `text-muted`, `sm`/`base` size. Exactly one `h1` per page.

**Message block** (success · error · empty) — outcome line → optional reason list → optional next action. Error lists are short, imperative and left-aligned. Empty states say what *would* be here and how to get it.

**List / table row** — one-line primary text, secondary metadata in `text-muted`, action at the end. Rows are the touch target.

**Dialog (modal)** — title → optional subtitle → body → actions at the end; close button top-right. Use for a short, self-contained choice or form that blocks the page. Prefer the native `<dialog>` (or the platform's equivalent): it gives focus trapping, Esc and a backdrop for free. Rules: labelled by its title (`aria-labelledby`); focus moves in on open and returns to the trigger on close; Esc and backdrop click close it unless data would be lost; body scrolls, header and actions do not; never stack two dialogs.

**Drawer** — a panel that replaces a column on small screens. Same rules as a dialog (focus, Esc, backdrop), opens from the edge it lives on, and the toggle that opens it is always visible.

**Chip / badge** — small, read-only label or toggle for a category, status or count. One height (e.g. 24 or 32 px), one radius. State is never colour alone: add an icon or word. Colours that carry domain meaning (e.g. a type or status palette) are a separate, named set, not new accents.

**Select / picker** — native `<select>` for ≤ ~7 options; a searchable dialog or list for more. Always labelled; show the empty option as a muted prompt, not a value.

**Icon-only button** — visible hit area ≥ touch target, accessible name, tooltip/`title` as a hint (not as the name), same hover/focus/active states as other buttons.

**Progress / meter** — a thin bar or ring with the number beside it; animate once on change, honour reduced motion. Indeterminate progress is allowed only when the duration is unknown.

**Navigation** — only when there is more than one destination. Otherwise none.

---

## 6. Page patterns

Wireframe notation: `[ box ]` container · `___` input · `( Verb )` button · `•` list item · `~` muted text.

**Form page** — title → inputs (grouped) → one primary action. Posts to the server or calls one handler.

```
[ Title                       ]
[ Label                       ]
[ ___________________________ ]
( Verb                        )
```

**Result / message page** — outcome line, optional reasons, optional single next action. No navigation chrome.

```
      Outcome line
      ~ optional detail
      • reason / next step
      • reason / next step
      ( Optional action )
```

**List page** — title → optional filter/search → rows → empty state when there are no rows.

```
[ Title                 ( + Add ) ]
[ Search _______________________ ]
[ Row primary      ~meta     > ]
[ Row primary      ~meta     > ]
```

**Detail page** — title → key facts → sections in reading order → actions at the end.

**Workspace (multi-panel)** — for tools where the user edits in one region and reads results in another. Two or three regions, each with its own job and single primary action; on wide screens they sit side by side and scroll independently, below the breakpoint the secondary region becomes a drawer or stacks under the first. Only the regions scroll, never the whole shell, and sticky regions must have a defined height.

```
[ Editor / canvas        ][ Results / insight ]
[  primary action here   ][  ~read-only       ]
[ ( Dock actions )       ][  scrolls itself   ]
```

**Empty, error and loading** are states of the pages above, not separate pages. Loading keeps the layout stable (skeleton or text), never a blank screen.

---

## 7. Copy and tone

- Short, plain, sentence case. One idea per line.
- Titles state the thing or the outcome: "Download video", "Downloaded successfully", "Download failed".
- Button labels are verbs: "Download", "Save", "Try again" — never "OK", "Submit", "Click here".
- Errors: what happened → likely cause → what to do. Avoid blame and jargon.
- Placeholders are examples ("https://…"), labels are instructions ("Video link").
- Keep one voice across the product; reuse existing strings before writing new ones.

---

## 8. Responsive and accessibility baseline

**Responsive**

- Mobile-first CSS; widen at breakpoints, never the reverse.
- Verify at ~320, ~768, ~1280 px. Nothing is clipped, no horizontal scroll.
- Type sizes change at most once across breakpoints; spacing may step down one scale step on the smallest screens; colours never change.

**Accessibility (minimum for a prototype)**

- Semantic landmarks and heading order; one `h1`.
- Every control has an accessible name; every image has `alt` (empty if decorative).
- Contrast ≥ 4.5:1 for text, ≥ 3:1 for UI; never colour alone to convey state.
- Visible focus for everything focusable; full keyboard operation; logical tab order.
- Touch targets ≥ 44 × 44 px; `viewport` meta without disabling zoom; `lang` on `<html>`.
- Honour `prefers-reduced-motion`.
- Anything clickable is a real `<button>` or `<a>`, never a `div`/`span` with `onClick`.
- Modals and drawers: labelled, focus moves in and returns, Esc closes, background is inert.
- Async results and status changes are announced (`aria-live="polite"`); toggles expose state (`aria-pressed`, `aria-expanded`).
- Drag and drop always has a keyboard or button alternative; hover is never the only way to reveal something.
- Text over a coloured background (chips, badges, buttons) is checked for contrast against that background, in both themes.

---

## 9. Checklists

**Discovery (once per repo)**

- [ ] Design source of truth located
- [ ] Token table (§3.2) filled from real values
- [ ] Existing components and page patterns listed
- [ ] Existing layout recorded and kept (columns, panels, navigation)
- [ ] Stack conventions table filled (§1, step 0)
- [ ] Quirks recorded (§3.3)

**Before building a screen**

- [ ] Job sentence written; primary action named
- [ ] All outcomes listed (success, errors, empty, loading, not-allowed)
- [ ] Page pattern chosen (§6)
- [ ] Text wireframe agreed

**Definition of done**

- [ ] Uses only tokens from §3.2 (new ones added to the table)
- [ ] Reuses existing components; new shared rules live in the shared styles
- [ ] Exactly one primary action and one accent element
- [ ] Every state designed (§1, step 5)
- [ ] Passes §8 at 320 / 768 / 1280 px, keyboard only, with a screen reader
- [ ] Copy follows §7
- [ ] Smoke test added for the route/screen

---

## 10. Do / Don't

**Do**

- Match the existing design language before improving it.
- Reuse components; promote a one-off to shared the moment a second screen needs it.
- Keep one accent element and one primary action per view.
- Label every input; use placeholders as examples only.
- Prefer native elements and real forms; make focus visible.
- Record new tokens, components and quirks back into this document.

**Don't**

- Change an existing layout — remove or merge columns, panels or navigation, or move content between screens — unless explicitly asked. Restyle in place.
- Introduce colours, sizes or radii outside the token table.
- Mix filled and outlined primary buttons, or put two primaries on one screen.
- Add navigation, headers, footers or sidebars to *new* single-task screens.
- Use fixed heights or global `overflow: hidden` to force a fit.
- Add JavaScript, client-side validation or animation a prototype does not need. (Anything asynchronous still gets a loading state.)
- Use `div`/`span` as buttons, or hard-code a colour in a component when a token exists.
- Hard-code route or asset paths when the stack has a helper.

---

## 11. Starter template (framework-agnostic)

Plain HTML + CSS custom properties. Paste into any stack's page/template, replace the tokens in `:root` with the repo's values, and swap the hard-coded `action` for the stack's route helper.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Page title</title>
    <style>
      :root {
        --font: system-ui, sans-serif;
        --text-sm: 13px; --text-base: 15px; --text-lg: 20px;
        --color-bg: #fff; --color-text: #111; --color-muted: #909090;
        --color-border: #ddd; --color-accent: #2962ff; --color-error: #c62828;
        --space-2: 8px; --space-3: 12px; --space-4: 16px;
        --radius: 4px; --control-h: 40px; --content-w: 360px;
      }
      * { box-sizing: border-box; margin: 0; }
      body {
        min-height: 100vh; display: grid; place-items: center; padding: var(--space-4);
        font: var(--text-base)/1.5 var(--font); color: var(--color-text); background: var(--color-bg);
      }
      .stack { display: grid; gap: var(--space-3); width: min(100%, var(--content-w)); }
      .card { display: grid; gap: var(--space-2); padding: var(--space-4); border: 1px solid var(--color-border); border-radius: var(--radius); }
      h1 { font-size: var(--text-lg); font-weight: 600; }
      label { font-size: var(--text-sm); color: var(--color-muted); }
      input { width: 100%; height: var(--control-h); padding: 0 var(--space-3); font: inherit; border: 1px solid var(--color-border); border-radius: var(--radius); }
      .btn-primary { height: var(--control-h); font: inherit; color: var(--color-accent); background: transparent; border: 1px solid var(--color-accent); border-radius: var(--radius); cursor: pointer; }
      :focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }
      .error { font-size: var(--text-sm); color: var(--color-error); }
      @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
    </style>
  </head>
  <body>
    <form class="stack" action="/route" method="post">
      <div class="card">
        <h1>Short title</h1>
        <label for="field">What to enter</label>
        <input id="field" name="field" type="text" placeholder="Example value" required />
        <!-- <p class="error">What went wrong and what to do.</p> -->
      </div>
      <button class="btn-primary" type="submit">Verb</button>
    </form>
  </body>
</html>
```

---

## 12. Worked example — YT Downloader (FastAPI + Jinja2)

What Step 0 produced for the YT Downloader app. Use it as a model for the size and shape of a Discovery record; it is **not** the standard for other repos.

**Stack conventions**

| Concern | Where it lives | Rule |
| --- | --- | --- |
| Routes | `main.py` | `templates.TemplateResponse(request, "<page>.html")` |
| Page markup | `templates/*.html` | one full HTML document per page, no inheritance |
| Shared styles | `static/style.css` | tokens + `.container`, `.container input`, `#download`, `h3` |
| Page-only styles | inline `<style>` | e.g. `.reason` on the error page |
| Links to routes & assets | `url_for` | `{{ url_for('static', path='style.css') }}`, `{{ url_for('download') }}` |

**Tokens in use** — Poppins 400 (Google Fonts) · sizes 15 / 13 / 12 px · weights 300 default, 800 error title · accent `#2962ff` · border `#ddd` · muted `rgb(144,144,144)` · radius 4 px · border 1 px · card 350 × 130 · input 330 × 40 · button 350 × 35 · spacing 10 / 15 / 20 / 5 px · one breakpoint `≤ 330px` (all widths −20 px).

**Pages → patterns** — `templates/index.html` = Form page · `templates/error.html` and `static/success.html` = Result page. Primary button is outlined; exactly one per page.

**Quirks (do not copy)** — global `* { overflow: hidden }` clips instead of scrolling · `error.html` aligns its sub-heading with `margin-left: -63px` · inputs are placeholder-labelled only · the primary button is styled by `id` (`#download`), so it cannot appear twice · `success.html` is served as a static file rather than rendered by a route.

---

## 13. Worked example — HIRO (static HTML + Tailwind + vanilla JS)

Static HTML + Tailwind (Play CDN) + vanilla JS client in `app/web/`, FastAPI server in `app/api/`, AI package in `model/`.

**Existing layout (preserved)** — one screen, three columns: **sidebar** (brand, new assessment, help links, history) · **chat** (conversation, composer, consent row) · **insight** (status row, model readings, leading conditions). Below 1200 px the insight column becomes a right-hand drawer; below 768 px the sidebar becomes a left-hand drawer and a small top bar carries the two toggles.

**Stack conventions**

| Concern | Where it lives | Rule |
| --- | --- | --- |
| Layout | `app/web/index.html` | one grid with `aside#sidebar`, `main.chat`, `aside#insight`; each region is its own job |
| Behaviour | `app/web/app.js` | state, rendering, drawers; no framework |
| Reusable DOM | `app/web/components.js` | `el()`, `button()`, `chip()`, `message()`, `diagnosisCard()`, `historyRow()`, `meterRow()` — the only place markup is built in JS |
| Copy and config | `app/web/constants.js` | every user-facing string, API path, limit and storage key |
| Tokens | `<style type="text/tailwindcss">` in `index.html` | CSS variables in `:root` (light/dark) mapped into `tailwind.config` colours; component classes (`.btn`, `.chip`, `.card`, `.row`, `.msg-*`, `.meter`, `.reading`, `.drawer-*`) in `@layer components` |
| API calls | `fetch('/api/...')` | relative paths; locally FastAPI serves `app/web` as static files, on Vercel `vercel.json` routes do the same |
| Assets | `app/web/` | referenced as `/logo.svg`, `/logo-mark.svg` |

**Job sentences (one per column)**

- Chat — *lets a person describe symptoms so that they get a possible condition and precautions.* Primary action: **Send**.
- Sidebar — *lets a person start or reopen an assessment.* Primary action: open a history row; "New assessment" is secondary.
- Insight — *lets a person see which models produced the reading and how sure each one is, so that they can judge the result.* No action; it is a Detail region fed by every chat reply. States: empty (Message block "No reading yet"), live ("updates after every message"), final ("final reading").

**Tokens in use** (CSS variables in `app/web/index.html`, exposed as Tailwind colours `bg-accent`, `text-muted`, `border-border`, …)

| Category | Token | Value |
| --- | --- | --- |
| Type | `font-sans` | Roboto 400/500 (Google Fonts) + `system-ui, sans-serif` |
| Type | `text-xs/sm/base/lg/xl` | 12 · 14 · 16 · 20 · 26 px, line-height 1.5 |
| Colour | `--color-bg` / `--color-surface` | `#fff` / `#f6f8fa` (dark: `#131314` / `#1e1f20`) |
| Colour | `--color-text` / `--color-muted` | `#1f1f1f` / `#5f6368` (dark: `#e3e3e3` / `#a8abae`) |
| Colour | `--color-border` | `#dadce0` (dark `#3c4043`) |
| Colour | `--color-accent` / `--color-on-accent` | `#0b57d0` / `#fff` (dark `#a8c7fa` / `#062e6f`) |
| Colour | success / error / warning | `#146c2e` / `#b3261e` / `#8a5100` with soft backgrounds |
| Space | Tailwind `1..8` | 4 · 8 · 12 · 16 · 24 · 32 px |
| Shape | `rounded` / `rounded-md` | 8 / 12 px; no pills, no circles |
| Size | `h-control` | 40 px (inputs and buttons equal) |
| Size | `max-w-content` | 680 px (chat column content) |
| Size | columns | sidebar 260 px · chat fluid · insight `minmax(400px, 36%)` |
| Layout | breakpoints | two: `xl` 1200 px (insight → drawer) · `md` 768 px (sidebar → drawer, top bar) |
| Motion | `transition` default | 160 ms · `cubic-bezier(0.2,0,0,1)` · reduced-motion honoured |
| Elevation | shadow | none |

**Regions → patterns** — Chat = Form page with a conversation list above the form · Sidebar history = List rows · Insight = Detail region: status line + agreement badge → "Models" rows → "Leading conditions" rows, each row a `meterRow` (label · prediction · % · 1 px bar in accent; a disagreeing model gets a border-coloured bar and the word "differs", never colour alone) · Notices and help = Dialog (native `<dialog>`). Primary button is **filled accent**; one per region.

**Quirks (do not copy)** — an earlier client used three font families, `overflow: hidden` on `html, body`, pill/circular controls, and a Leaflet map column (replaced by the insight panel). The app shell is `h-dvh` with the **message list** and the **insight body** as the only scroll containers — deliberate, and the only fixed heights in the client. Tailwind Play CDN is acceptable for this prototype; swap for the CLI build before a production release.

---

## 14. Worked example — TicTacToe-AI (FastAPI + Jinja2)

FastAPI + Jinja2, one screen, deployed as a single Vercel function. The server is stateless: the client sends the whole board with every request.

**Stack conventions**

| Concern | Where it lives | Rule |
| --- | --- | --- |
| Routes | `main.py` | `GET /` renders the page · `POST /api/move` validates the board and returns the AI's move · `GET /robots.txt` |
| Game logic | `tictactoe.py` | pure functions, no I/O; memoised minimax |
| Page markup | `templates/index.html` | one screen, board buttons rendered server-side; SEO meta, Open Graph and JSON-LD in `<head>` |
| Shared styles | `static/style.css` | tokens in `:root`; components `.brand`/`.logo`, `.status`, `.board`/`.cell`, `.side`, `.btn-primary`, `.credit` |
| Behaviour | `static/app.js` | one module, no framework; state, rendering, fetch with an 8 s timeout |
| Brand | inline `<svg class="logo">` + `static/favicon.svg` | a `#` grid in `currentColor` with an accent dot in the centre cell; the favicon copy carries a dark-scheme stroke |
| Links to routes & assets | `url_for` | `url_for('static', path=…)`, `url_for('move')` passed to the script via `data-move-url` |

**Job** — *lets a player play tic-tac-toe against an unbeatable AI so that they can try to beat it.* Primary action: place a mark (tap an empty square). One primary button: **New game** (filled accent). Side choice is a native radio group.

**Wireframe**

```
[ # Tic-Tac-Toe AI                         ]   logo + h1
[ Your turn                                ]   status, aria-live, fixed one-line height
[ [ ] [ ] [ ]                              ]
[ [ ] [ ] [ ]                              ]
[ [ ] [ ] [ ]                              ]
[ Play as (•) X ( ) O        ( New game )  ]

      ~ Design and developed by …               credit, pinned to the bottom row
```

**Tokens in use** — `system-ui, sans-serif` · 13 / 15 / 26 px + `--text-display` 40 px for board marks · weights 400 / 600 · bg `#fff`, surface `#f4f4f5`, text `#111`, muted `#666`, border `#ddd`, accent `#2962ff` on `#fff`, accent-soft `#e8efff` (winning line), error `#c62828` · hover shades derived with `color-mix()` rather than new tokens · space 4 / 8 / 12 / 16 / 24 · radius 4 / 8 · control 40 px · content 360 px · no breakpoints (the board is fluid) · 150 ms ease-out, reduced motion honoured · no shadow.

**Pattern** — Form page: title → status (Message block) → board (the input) → controls, with the credit in a second `auto` grid row so it never pushes the game around. States: your turn · AI thinking (`aria-busy`, muted status) · AI wins / draw / you win (line tinted, board locked) · error (status in `--color-error`, the player's move is undone; the request times out after 8 s so the busy state cannot hang). Cells use `aria-disabled` instead of `disabled` so keyboard focus is never lost, `user-select: none` and `touch-action: manipulation` so taps never select text or zoom. Status copy is kept to one line so the centred layout never shifts.

**Quirks** — none yet. The original CLI game lived in `main.py` and read moves with `input()`; it was replaced, not restyled.
