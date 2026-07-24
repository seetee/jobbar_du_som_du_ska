# Arbetstid — plan & status

A private tool for a gymnasium teacher (ferietjänst) to (1) check the timetable
delivers each course's contracted hours, and (2) plan/track regulated work-time
across the läsår's four avstämningsperioder so the yearly hour-budget balances.

Single self-contained file: `index.html` — vanilla JS, `localStorage`, no build,
no backend, works offline. Personal source data lives in `docs/` (git-ignored).

## The contract model (verified vs Sveriges Lärare)

Kommunal ferietjänst: årsarbetstid **1767 h**, reglerad tid **1360 h**,
förtroendetid **407 h**, **194** A-dagar, reglerad tid split into **4
avstämningsperioder** (equal-hours-ish, unequal length). At 80% tjänst →
reglerad ≈ **1088 h**, förtroende ≈ **326 h**.

## Built today

- **Coverage tab** — imports Outlook `.ics`, filters to a läsår window, matches
  events to tjänstefördelning course codes, shows scheduled vs required hours per
  course + surplus/deficit, a manual "Tillägg" per course, an unmatched-events
  list, and per-course notes.
- **Budget tab** — reglerad tid split into 4 editable periods (dates / weeks /
  måltimmar). Per period: target h/vecka, date-based balance (ahead/behind),
  pace-to-finish. Year-level **"mot plan i år"** banking indicator. Förtroendetid
  shown as awareness only.
- **Auto teaching** — lessons from the imported calendar auto-fill each period's
  logged hours (course-code events, up to today); you hand-log only *övrigt
  arbete* (prep, grading, GYARTE, konferens…) as a lump.
- **Per-period activity breakdown** — "Innehåll" checklist (name + est. hours) to
  make untimetabled work visible; P3/P4 pre-seeded (GYARTE, UF, Blixtlåset;
  rättning, betyg, GYARTE-bedömning).
- **Design pass** — logbook/instrument look: monospace figures, graph-paper
  palette, and the signature **läsårsband** (period tubes that fill with logged
  hours, live "idag" line, hatched sommar cap).

## Kenneth's specifics (baked into defaults)

- Front-loads teaching into autumn; spring APL period is not *light* but full of
  untimetabled work (GYARTE, competitions in P3; grading/evaluation in P4).
- APL administration is a colleague's assignment, not his.
- `FROT200TX` and `DIGD100TX` are the coverage risks — only ~half delivered by
  January, then most of spring lost to the 12-week APL pause. Confirm once the
  VT27 schedule exists.
- `GYARTE` and `Mentorstid` aren't reliable calendar events → manual entry.
- Skola24 has no usable export; M365 connector is blocked by the tenant. Route is
  Outlook → Save Calendar → `.ics`.

## Tomorrow / open

- [ ] Publish as a private Claude Artifact → phone home-screen URL; visually
      verify the läsårsband alignment (couldn't screenshot locally).
- [ ] Enter real numbers: employment %, real period boundaries (carve out lov via
      arbetsveckor), måltimmar weighted for front-loading.
- [ ] Import the real autumn `.ics`; sanity-check FROT200 / DIGD coverage.
- [ ] Import VT27 `.ics` when it lands (replaces the spring projection).
- [ ] Decide if a real offline PWA (manifest + service worker) is worth it, or if
      the Artifact URL is enough.
- [ ] Maybe: a small "h/vecka × veckor" helper for projecting the truncated
      spring term (only if manual Tillägg gets tedious).
- [ ] Create a real standardized PWA. 
