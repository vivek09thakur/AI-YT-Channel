---
name: prototype-design-beta
description: Beta companion to prototype-design. Builds Material 3 style, token-driven, light/dark, responsive tool UIs (workspace with docked controls, picker dialogs, state-layer buttons, drag-and-drop slots, live analysis panels). Use when asked to design or prototype a data-rich interactive tool, dashboard or editor, or to extract this design language from an existing app.
---

# Prototype Design (beta)

Extends `prototype-design`. Follow its workflow (§1), checklists (§9) and discovery step first; this skill adds a concrete design language distilled from a real, working tool: a two-region team-builder workspace (React + Tailwind, Material 3 tokens). Rules describe the result, not the framework. When the product already has its own design language, **that wins**.

## 1. When to use which

| Situation | Use |
|---|---|
| Minimal screen, few components, no theme | `prototype-design` |
| Interactive tool, dashboard, editor, picker-heavy flow, light and dark theme | this skill |

## 2. Principles

1. **Roles, not values.** Components reference role tokens (`surface`, `on-surface-variant`, `primary-container`), never hex codes. Dark mode swaps token values only.
2. **One shell, two layouts.** The same controls render as a drawer on small screens and a docked panel on wide ones (`variant="drawer" | "dock"`). No duplicate logic.
3. **Regions scroll, the shell does not.** The app is a fixed viewport (`100dvh`); each region owns its scrolling.
4. **Every interactive thing has five states**: default, hover, focus-visible, active, disabled. Add selected/on, loading, empty and error where they apply.
5. **State by layer, not by new colours.** Hover and press are an overlay of the content colour at 8% and 12%.
6. **Live feedback.** Results update as the user edits; transient confirmations ("Copied", 1.8 s) use `aria-live="polite"`.
7. **Isolate failure.** Each independent region has its own error boundary and message; one failure never blanks the app.

## 3. Tokens

### Colour roles (light / dark)

| Role | Light | Dark |
|---|---|---|
| primary | `#0b57d0` | `#a8c7fa` |
| on-primary | `#ffffff` | `#062e6f` |
| primary-container | tinted blue | deep blue |
| surface-container-lowest → highest | five-step neutral ramp | same ramp, inverted |
| on-surface / on-surface-variant | high / medium emphasis text | same roles |
| outline / outline-variant | control border / divider | same roles |
| success, warning, error | each with `-container` and `on-container` | adjusted for contrast |
| scrim | 32% black | same |

Define once as CSS variables (`--md-*`), expose to the framework (e.g. Tailwind `@theme`), switch under `:root.dark`. Set the class from `prefers-color-scheme` with a tiny inline script in `<head>` to avoid a flash; a toggle flips the class and persists the choice.

### Type scale (role names)

headline-sm 24 · title-lg 22 · title-md 16/500 · title-sm 14/500 · body-lg 16 · body-md 14 · body-sm 12 · label-lg 14 · label-md 12 · label-sm 11. Body font Roboto-class sans, headings a display sans, code a mono. Define as utilities/classes, not per-element sizes.

### Shape and elevation

Radius: xs 4 · sm 8 · md 12 · lg 16 · xl 28 · pill 9999. Buttons and chips are pill, cards md/lg, dialogs xl. Elevation: three shadow levels (`shadow-1/2/3`) used only for dialogs, menus and raised cards; surfaces otherwise separate by tone and a 1 px outline.

### Spacing and size

4 px grid. Controls 40 px (compact 28–32 px); text field 56 px (compact 40 px); top bar 56 px; progress 8 px (thin 3–6 px). Breakpoints: 640 (smaller type, tighter gaps) and 1024 (drawer becomes docked panel).

## 4. Components

- **Card** — outlined (default), filled (tonal), elevated. Never nest a card in a card.
- **Button** — filled (primary action), tonal, outlined, text. 40 px, pill, state-layer overlay via a `::before` in `currentColor`. One filled button per region.
- **Icon button** — 40 px, round, accessible name always.
- **Chip** — 32 px action/filter chip; 24 px domain badge (category colour, white text with a subtle text shadow for legibility).
- **Field** — outlined, label or placeholder, visible focus inset ring; compact variant for dialog search.
- **List item** — leading media, title, supporting text, trailing action; `is-current`, hover and disabled states.
- **Dialog** — surface-container-high, xl radius, shadow-3, max height ~85–92 dvh; header (title, optional subtitle, close), optional toolbar (search), scrolling body, optional footer. Backdrop click and Esc close; focus in on open, back to trigger on close; never stack.
- **Drawer** — below 1024 px only; scrim, Esc, toggle in the top bar.
- **Progress / score ring** — SVG ring (stroke-dasharray, one 0.8 s ease) for the headline number, thin bars for sub-scores, percentage beside each.
- **Empty state** — filled card, 40 px primary icon, one title, one sentence saying what to do.
- **Search progress** — 3 px bar under the field; determinate when known, sliding indeterminate otherwise.

## 5. Patterns

**Workspace shell.** Left region = editor (slot grid + docked actions), right region = live results (summary, detail lists, per-item breakdown). Wide: two columns (~11:9), each `100dvh` with its own scroll, 1 px outline divider. Narrow: top bar with menu button and title, single column, controls in a drawer.

```
wide                                   narrow
[ brand        theme ][ summary      ]  [ ☰ title            ]
[ slot slot slot      ][ threats      ]  [ slot slot          ]
[ slot slot slot      ][ breakdown    ]  [ summary / results  ]
[ [actions dock]      ][  (scrolls)   ]  drawer: controls
```

**Slot grid.** N equal slots (2 columns, 3 at ≥640, fill row height at ≥1024). Empty slot: dashed outline, hover tints to primary-container, click opens a picker. Filled slot: tinted surface, name, small selects, compact action buttons.

**Picker dialogs.** One dialog per choice type. Search field in the toolbar, list below; selecting closes the dialog and applies the change.

**Drag and drop.** Native HTML5 drag with a custom MIME type; `is-dragging` and `is-drop-target` states; do not start a drag from selects or buttons. **Always provide a non-drag alternative** (move buttons or keyboard).

**Reveal-on-demand actions.** Compact controls may use a dashed border that turns solid on hover/focus; keep a visible focus ring and a ≥ 44 px hit area on touch.

**Feedback.** Button label swaps for ~1.8 s on success; destructive actions use error tint; toggles use `aria-pressed`.

**Motion.** 150–250 ms colour/opacity transitions, at most one decorative loop, all disabled under `prefers-reduced-motion`.

## 6. Quirks to not copy

The reference app has flaws; do not reproduce them.

- Hard-coded colours outside the token set. Add tokens instead.
- 22–28 px controls, below touch size. Pad the hit area.
- `!important` height/padding overrides on shared button classes. Add a size variant.
- Focus ring on buttons but not on chips or compact selects. Every interactive element gets one.
- Fonts from a third-party CDN with no fallback. Self-host or declare a system stack.
- Drag and drop with no keyboard path.
- Misspelled asset names and personal credits or links in the footer. Keep product chrome neutral.

## 7. Discovery record (worked example)

```
Stack:         Next.js (App Router, client components), Tailwind v4, TypeScript, static export
Source:        globals.css (tokens + component classes), shared components (Dialog, Icon, SearchField, Spinner),
               feature components (Shell, slot, analysis panel, lineup, picker dialogs)
Language:      Material 3 role tokens, light + dark, pill buttons with state layers, tonal cards
Layout:        fixed-viewport workspace, 2 columns at >=1024, drawer + top bar below
Patterns:      picker dialogs, slot grid with DnD, live analysis panel, error boundary per region
Accessibility: Esc/scrim/focus on dialogs, aria-live feedback, reduced motion; gaps in section 6
```

Use this shape for your own Step 0 record and fill it from the target repo, not from this example.

## 8. Checklist (adds to prototype-design §9)

- [ ] All colours are role tokens; dark theme verified by rendering it
- [ ] Each control shows five states; focus ring on every one
- [ ] Narrow layout works at 320 px with the drawer
- [ ] Each region scrolls on its own; the shell does not
- [ ] Dialogs: Esc, backdrop, focus return, no stacking
- [ ] DnD has a keyboard/button alternative
- [ ] Badge colours pass 4.5:1 against their label in both themes
- [ ] Reduced motion respected
- [ ] Rendered and checked in a browser, not just read
