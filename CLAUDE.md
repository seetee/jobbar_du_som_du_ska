# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A private tool for a Swedish gymnasium teacher on *ferietjänst* to (1) verify the
timetable delivers each course's contracted hours and (2) plan regulated work time
across the läsår's four avstämningsperioder. `PLAN.md` holds the current status,
domain reasoning, and open checklist — read it before changing behaviour, and keep
it updated when shipping something from its list.

## Commands

There is no build, no package manager, no test runner, no backend.

- Quick look: open `index.html` directly (`xdg-open index.html`). The app works
  fully from `file://`, but the service worker will not register there.
- Anything PWA-related **must** be served, since service workers require a secure
  context: `python3 -m http.server 8765` then `http://127.0.0.1:8765/`. Verify
  install/precache from the server's access log — `GET /index.html` and the icons
  appear only when `cache.addAll(SHELL)` runs, since the page never requests them.
- Tests: an `assert`-based self-test at the bottom of the app `<script>` runs on
  every page load and logs to the console. Extend that IIFE rather than adding a
  framework. Note `index.html` has **two** script blocks now (app, then service
  worker registration) — take the longest when extracting for `node --check`.
- Validating markup: `npx html-validate index.html`. The Nu validator (`vnu.jar`)
  needs Java 11+ and this machine has 8 — `vnu-jar@17.11.0` runs on 8 but is from
  2022 and reports stale complaints (`media` on `theme-color`, `type=date` and
  `inputmode` "not supported in all browsers"); all four are fine today. Most of
  the markup is generated, so validate the **rendered DOM** too: run the page in
  jsdom (needs a `structuredClone` shim) and validate the serialized output.

## Accessibility

Non-negotiable, and worth stating because it has already been got wrong once: date
fields are native `<input type="date">`. Display format is decided by the OS/browser
locale, not by the page, so a "wrong" format is never a reason to reach for a text
input — that discards the picker, keyboard stepping and date semantics AT depends
on. Same principle throughout: keep native controls, and if ARIA roles are added,
wire the whole pattern (the tabs once had `role="tab"` and nothing else, which is
worse than no ARIA at all).

## Architecture

Four tracked parts: `index.html` (all markup, CSS and app logic — vanilla JS, no
modules, `localStorage`), `manifest.webmanifest`, `sw.js`, and `icons/`. It stopped
being a single self-contained file when it became a PWA: a service worker must be
its own file at the right scope, and a manifest cannot be inlined reliably. UI
strings are Swedish; keep them Swedish.

`sw.js` is network-first with cache fallback, deliberately: there is no build step
and no versioned filenames, so cache-first would serve stale code indefinitely.
Bump `CACHE` whenever `SHELL` changes — `activate` deletes every other cache.

State: one `state` object, seeded from `DEFAULTS`, persisted under the `KEY`
constant. `load()` shallow-merges saved state over a `structuredClone(DEFAULTS)`
and back-fills `budget.periods[].activities`. **Adding a nested field to
`DEFAULTS` will not reach existing users** — either back-fill it in `load()` the
way `activities` is, or bump `KEY` (which discards their data).

Rendering: two full re-render functions, `render()` (coverage tab) and
`renderBudget()` (budget tab + `renderYearband()`). Both rebuild `innerHTML` from
scratch, so a re-render blows away focus and caret position. That is why the
delegated listeners split by event type: text fields (`code`, `note`, activity
names) save on `input` *without* re-rendering, numeric fields re-render because
their values feed the totals. Preserve that split.

Course matching is exact, case-insensitive, whitespace-trimmed equality between a
calendar event's `SUMMARY` and a course `code` (`norm()`). No fuzzy matching by
design — anything that misses lands in the "unmatched events" list, which is the
user's cue to fix the code. Don't add substring matching; it silently
double-counts.

`parseICS()` is a deliberately minimal line parser: unfolds continuations, reads
only `SUMMARY`/`DTSTART`/`DTEND`, treats timestamps as local wall-clock (ignores
`TZID` and `Z`), and drops events outside `0 < h < 24` to skip all-day entries.
Source is Outlook → Save Calendar → full detail `.ics`. The M365 connector is
blocked by the tenant. Skola24 *can* have iCal export enabled in Schemavisaren
(per their support, 2026-07-25), but it is static — it never reflects later
schedule changes — and exports one file per week, so a läsår is ~40 files. The
tool takes a single file and replaces `state.events` wholesale; if the weekly
route is ever needed it wants `multiple` on the file input plus event dedup.
Outlook remains the route.

Budget hours have two sources that must not overlap: **auto** = imported
calendar events whose summary matches a course code, dated from period start
through today (capped at period end); **manual** (`logged`) = *övrigt arbete*
only — prep, grading, GYARTE, konferens. Anything that would let scheduled
teaching be entered by hand double-counts it. Period `activities` are estimates
for making untimetabled work visible; they are not added to `logged`.

## Data

`docs/` holds the real schedule, tjänstefördelning, and employer slides. It is
git-ignored and must stay that way. `DEFAULTS` carries the contract model
(1767 h årsarbetstid, 1360 h reglerad, 194 A-dagar, 4 periods) and real course
codes as seed values — these are editable in the UI, so treat them as defaults,
not constants to compute against.
