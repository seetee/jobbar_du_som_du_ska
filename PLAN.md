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

## Lov (added 2026-07-25)

Arbetsveckor are no longer typed per period — one year-level **Lovveckor** field
(`33,34,44,53,7,15,25`) drives both the h/vecka target and the plan line. This
also fixed a unit bug: `frac` was elapsed *calendar* time while `weeks` was
arbetsveckor, so the plan advanced during lov and reported a phantom deficit
every jullov. Plan now advances only in working weeks.

The `.ics` contains **no** lov or all-day events — lov is only inferable from
weeks with zero lessons (25/26 gaps: v33–34, v44, v52–01, v07, v15, v25). Hence
a typed list rather than derivation: P3/P4 have no VT27 schedule yet, so
derivation would read them as all-lov. A "hitta lov från schemat" button that
*fills* the field is the upgrade path if typing it once a year gets old.

Known ceiling: a week straddling a period boundary counts fully in both periods.
Put boundaries on week edges (Sun→Mon) and it disappears.

## Kenneth's specifics (baked into defaults)

- Front-loads teaching into autumn; spring APL period is not *light* but full of
  untimetabled work (GYARTE, competitions in P3; grading/evaluation in P4).
- APL administration is a colleague's assignment, not his.
- `FROT200TX` and `DIGD100TX` are the coverage risks — only ~half delivered by
  January, then most of spring lost to the 12-week APL pause. Confirm once the
  VT27 schedule exists.
- `GYARTE` and `Mentorstid` aren't reliable calendar events → manual entry.
- M365 connector is blocked by the tenant. Route is Outlook → Save Calendar →
  `.ics`. Skola24 support (2026-07-25) confirms iCal export *can* be enabled in
  Schemavisaren, but it is **static** (never reflects later schedule changes) and
  yields **one file per week** — ~40 files per läsår, one "calendar" each in
  Outlook. Worse than the Outlook export on both counts, and the staleness defeats
  the whole point of the coverage check, so Outlook stays the source.

## Tomorrow / open

- [ ] Publish as a private Claude Artifact → phone home-screen URL; visually
      verify the läsårsband alignment (couldn't screenshot locally).
- [ ] Enter real numbers: employment % (~81, not 80), real period boundaries on
      week edges, correct lovveckor from kalendariet, måltimmar weighted for
      front-loading.
- [ ] Import the autumn `.ics` — **already in `docs/calendar.ics`**, which spans
      2025-08-11 → 2027-01-19 (all of 25/26 plus HT26). Sanity-check FROT200 /
      DIGD coverage.
- [ ] Course aliases: `WEUWEB01`→`WEBB Nivå 1` (25/26 only, course retired),
      `ARTART01`→`ARTI1000X`, and `WEUWEB02`→`WEBB Nivå 2` from 27/28. Needed
      only if the 25/26 year should compute; harmless in a 26/27 window.
- [ ] Import VT27 `.ics` when it lands (replaces the spring projection).
- [ ] Decide if a real offline PWA (manifest + service worker) is worth it, or if
      the Artifact URL is enough.
- [ ] Maybe: a small "h/vecka × veckor" helper for projecting the truncated
      spring term (only if manual Tillägg gets tedious).
- [ ] Create a real standardized PWA. 
