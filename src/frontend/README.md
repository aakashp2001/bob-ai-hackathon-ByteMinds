# Missing Person Investigation Assistant — frontend

Phases 1–6 of the IBM Bob Hackathon frontend. React, Vite, Tailwind CSS, React Router, and JavaScript. This is a fictional case coordination prototype.

## Current status

- Shared navy sidebar, header, active navigation, and all four routes are complete.
- The Case Dashboard displays case information, evidence counts, the subject's last known appearance, and the mock analysis workflow.
- Lead Analysis presents the supplied leads, score breakdowns, evidence, uncertainty, and next actions.
- Public Appeal presents the supplied draft as a document, with clipboard copying, review status, and print styling.
- Case File presents all ten structured sections, full source-record tables, compact lead summaries, supplied actions, and limitations.
- Canonical fixture: **MP-2026-0042 / Aarav Shah**, with 8 tips, 6 CCTV records, and 3 fixed potential leads.
- Async mock services are ready for a future agreed FastAPI contract.
- No backend, MCP, AI reasoning, correlation, score calculation, or HTTP endpoints are implemented.
- Phase 6 polish and hardening are complete. Stopped before backend integration.

## Run

Use Node.js 20.19+ in the 20.x line, or 22.12+ (Node 24 was used here). Dependencies are locked with pnpm.

```powershell
pnpm install --frozen-lockfile
pnpm run dev --host 127.0.0.1 --port 5173 --strictPort
```

Open http://127.0.0.1:5173/. Stop the development server with Ctrl+C in its terminal.

This Codex shell has Node but no `npm` command. Its bundled pnpm can be invoked directly:

```powershell
& 'C:\Users\hpanc\.cache\codex-runtimes\codex-primary-runtime\dependencies\bin\fallback\pnpm.cmd' run dev --host 127.0.0.1 --port 5173 --strictPort
```

On another machine, use your normal pnpm installation. The application does not depend on the bundled path. Avoid mixing lockfiles from different package managers.

Production build and local production preview:

```powershell
pnpm run build
pnpm test
pnpm run preview
```

Production hosting must rewrite frontend routes to `index.html` for direct deep links (BrowserRouter).

## Routes

| View | Route |
| --- | --- |
| Case Dashboard | `/case/MP-2026-0042` |
| Lead Analysis | `/case/MP-2026-0042/leads` |
| Public Appeal | `/case/MP-2026-0042/public-appeal` |
| Case File | `/case/MP-2026-0042/case-file` |

The root and unknown paths redirect to the canonical case dashboard. The prototype supports one case.

## Files created

```text
.env.example
.gitignore
README.md
index.html
package.json
pnpm-lock.yaml
pnpm-workspace.yaml
vite.config.js
src/
  App.jsx
  main.jsx
  styles.css
  components/
    common/PageHeader.jsx
    common/Button.jsx
    common/SectionCard.jsx
    common/LoadingState.jsx
    common/ErrorState.jsx
    common/EmptyState.jsx
    case/CaseInfoCard.jsx
    case/EvidenceSummary.jsx
    case/AnalysisStatus.jsx
    leads/LeadCard.jsx
    leads/PriorityBadge.jsx
    leads/ScoreBreakdown.jsx
    leads/EvidenceList.jsx
    appeal/AppealDocument.jsx
    case-file/DetailList.jsx
    case-file/RecordTable.jsx
    case-file/LeadSummaryTable.jsx
    layout/Header.jsx
    layout/Sidebar.jsx
  mocks/caseData.js
  services/api.js
  utils/formatters.js
  pages/CaseDashboard.jsx
  pages/LeadAnalysis.jsx
  pages/PublicAppeal.jsx
  pages/CaseFile.jsx
tests/data-contract.test.js
```

Generated local directories: `node_modules/`, `.pnpm-store/`, and `dist/` (ignored).

There were no pre-existing files in the workspace, no Git repository, and no applicable AGENTS.md files. No existing template files or validation workflows were changed. The supplied workspace root is therefore assumed to be the intended frontend location. If the team later supplies the submission repository, place this frontend in its agreed source location while preserving the template.

## Data and API handoff

`src/mocks/caseData.js` is the only case fixture source. Profile fields use the supplied canonical values. Tip/CCTV descriptions, lead details, recommendations, and draft copy are illustrative frontend fixtures, pending alignment with the backend/MCP team. Missing gender, created date, and circumstances are not inferred. Record timestamps use IST offsets.

`src/services/api.js` exports `getCase()`, `analyzeCase()`, `getLeads()`, `getPublicAppeal()`, and `getCaseFile()`. They return copies of mock data. `analyzeCase()` only waits 900 ms and returns a mock completion result with fixed leads. None of these services calculate or rank anything.

The dashboard disables Analyze Case while the promise is pending, announces progress, then displays Analysis complete and a View Lead Analysis link. It does not navigate automatically. The analysis status is held in `App` so it survives route changes; refreshing starts a new demo session. Re-running analysis is supported, and rejected or incomplete results show a retry message. The three provided mock leads appear in the overview count even before analysis; the count is explicitly labeled as provided mock leads, not newly calculated results.

`VITE_API_BASE_URL` is reserved in `.env.example` and read by the service module, but is unused until the backend contract arrives. Do not place secrets in Vite environment variables. Replace service implementations only after the real contract is supplied.

## Dependencies installed

| Dependency | Installed version |
| --- | --- |
| react / react-dom | 19.3.0 |
| react-router-dom | 7.18.4 |
| vite | 7.3.6 |
| @vitejs/plugin-react | 5.2.0 |
| tailwindcss / @tailwindcss/vite | 4.3.3 |

Tailwind uses its official Vite plugin and CSS import; a separate Tailwind configuration file is not required for this setup. References: [Tailwind Vite installation](https://tailwindcss.com/docs/installation/using-vite), [Vite guide](https://vite.dev/guide/).

## Commands and verification

Main commands executed using the bundled pnpm path:

```powershell
pnpm install --store-dir .pnpm-store
pnpm approve-builds esbuild
pnpm run build
pnpm run dev --host 127.0.0.1 --port 5173 --strictPort
```

The first install attempt was blocked by sandbox network permissions; the approved retry downloaded dependencies. pnpm initially blocked esbuild's installation script, resolved by explicitly approving only esbuild in `pnpm-workspace.yaml`.

- Production build passed.
- Browser checked all four route headings via navigation and direct URL loading.
- Keyboard activation and active navigation state checked.
- Browser console reported no warnings or errors during navigation checks.
- A Node fixture check confirmed canonical name/number, exact record counts, and valid lead source references.

Phase 6 adds regression checks using Node's built-in test runner, with no additional test dependency. Historical phase checks are recorded below.

## Phase 2 implementation and verification

Created `CaseInfoCard`, `EvidenceSummary`, `AnalysisStatus`, and `SectionCard`. Updated `CaseDashboard.jsx`, `App.jsx`, this README, and the shared mock case status to the requested `Active Investigation`. The canonical subject and source records remain unchanged.

Reused the existing sidebar, header, routes, base styles, shared case data loaded by `getCase()`, and unchanged `analyzeCase()` service. No dependencies were added.

- Case Dashboard loads at `/case/MP-2026-0042` with the canonical profile, last known location/date/time, and counts 8 / 6 / 3.
- Browser verified Not Analyzed, disabled/loading, and completed states using the real 900 ms mock delay.
- Completion remains on the dashboard; View Lead Analysis opens `/case/MP-2026-0042/leads`.
- Return navigation preserves completion; browser refresh resets the demo state and hides the completion link.
- Laptop and narrower responsive layouts were visually checked, with no horizontal overflow detected.
- Browser console reported no warnings or errors.
- `pnpm run build` passed. No separate test framework was added; the error fallback was implemented but not fault-injected in browser testing.

## Phase 3 implementation and verification

Created `LeadCard`, `PriorityBadge`, `ScoreBreakdown`, `EvidenceList`, and the reusable `LoadingState`, `ErrorState`, and `EmptyState` components. Updated `LeadAnalysis.jsx`, its case-data prop in `App.jsx`, and this README. Reused `SectionCard`, the shared layout, navigation, focus styles, case data, and unchanged `getLeads()` mock service. No dependencies were added.

Cards remain fully expanded. Each includes the supplied rank, ID, title, priority score, priority badge, source IDs, five breakdown rows, separate evidence lists, uncertainty, and recommended action. Cards stack internally at narrower widths. Evidence arrays render in full without truncation or reinterpretation; empty arrays use neutral fallback messages, and missing arrays say the evidence data was not supplied.

The UI preserves the supplied array order and rank fields. It assumes the backend/MCP will supply leads in rank order, as the current fixtures do. It does not sort by scores, assign ranks, calculate totals, or generate evidence/actions. Score denominators are display labels from the supplied contract. Unknown/missing values are labeled as not supplied rather than inferred. The current service returns the three mock leads on direct navigation even before the demo Analyze Case action is run.

The page identifies scores as Investigative Priority Scores, retains the independent verification notice, and states that scores support triage only and do not establish identity. Every card repeats the investigator-verification requirement beside uncertainty.

Verification:

- All three leads displayed in supplied rank order (L001/L002/L003), with scores 70/45/25, original source IDs, five score breakdown values each, evidence, uncertainty, and recommended actions.
- Direct route loading, Back to Case Dashboard, sidebar return navigation, and the active Lead Analysis item passed.
- Empty-response verification displayed the requested empty state and dashboard link, with no lead cards.
- A temporary delayed/rejected mock response verified loading, error, Try again, retry loading, and successful recovery.
- Temporary empty/missing evidence arrays verified the distinct neutral messages. The canonical fixtures were never edited.
- The original mock service was restored byte-for-byte, confirmed by SHA-256. Public Appeal and Case File were also verified unchanged.
- Laptop and tablet layouts were visually reviewed; no horizontal page overflow was detected.
- An intermediate hot-reload warning occurred while the page and its parent prop were being updated. A fresh browser session subsequently loaded all leads and navigated both directions without console warnings or errors.
- The final production build passed. No fault-injection code or test-only responses remain in the application.

## Phase 4 implementation and verification

Created `src/components/appeal/AppealDocument.jsx`. Updated `PublicAppeal.jsx`, its case-data prop in `App.jsx`, `styles.css`, the appeal's status metadata in `caseData.js`, and this README. Reused `SectionCard`, `LoadingState`, `ErrorState`, `EmptyState`, navigation, layout, focus styles, and the unchanged `getPublicAppeal()` service. No dependencies were added.

Data structure: the page uses the existing `publicAppeal.heading`, `status`, `reviewNotice`, `text`, and `contact` fields. Added static `draftStatus: 'Generated'`, `reviewStatus: 'Required'`, and `publicationStatus: 'Not Approved'` metadata. The existing appeal text, canonical profile, lead data, and source records were not rewritten. The document renders the supplied text as paragraphs and displays its opening heading once. Copy preserves the entire original text and its line breaks.

The document component receives only the appeal, case reference, and person profile. It never receives investigator tips, CCTV records, lead scores, evidence, uncertainty, or recommendations. The mock appeal contains only the supplied profile, last-seen facts, case reference, demo contact, and review/demonstration notices. Later integration must supply similarly reviewed public-safe text through the agreed service contract; the frontend does not generate or sanitize investigative prose into an appeal.

Copy Text uses `navigator.clipboard.writeText(appeal.text)`, announces success for three seconds, and provides an inline manual-copy message on failure. Clipboard use requires a secure browser context (localhost is supported). Print calls `window.print()` directly. No PDF generation or publication action exists.

Print CSS uses A4 page sizing with 16 mm margins, hides the sidebar, app header/footer, navigation, notices outside the document, and action controls, and removes the preview border/shadow. The document's draft status, review requirement, and fictional-data notices remain printed. Text size and paragraph breaks are adjusted for print.

Verification:

- Direct appeal route and the active sidebar item passed; Back to Lead Analysis and return navigation passed.
- The document displayed MP-2026-0042, Aarav Shah, the supplied profile/last-seen details, and the demo contact without speculative investigative content.
- Copy showed success, and pasting into a temporary local verification field reproduced the supplied text with line breaks. A temporary thrown clipboard error verified the inline failure message.
- Temporary null, delayed, and rejected service responses verified empty, loading, error, retry, and recovery states. Missing/blank text does not create fallback appeal content, and unavailable drafts have no Copy or Print controls.
- Print was invoked without an application error. This in-app browser did not expose a native print-preview surface. The print-only CSS was temporarily applied to the screen for inspection: only the document remained, with review notices intact. Native print-dialog rendering and pagination remain unverified; check these in the demo browser before presenting.
- Laptop/tablet layouts were reviewed with no horizontal overflow.
- Temporary test fields, failures, response changes, and print-preview overrides were removed. Hashes confirmed the mock service, Lead Analysis page, and Case File page remained unchanged.
- A fresh browser navigation check reported no console warnings or errors. The final production build passed.

## Phase 5 implementation and verification

Created `DetailList.jsx`, `RecordTable.jsx`, `LeadSummaryTable.jsx`, and presentation-only `formatters.js` under `src/components/case-file/`. Updated `CaseFile.jsx`, added an optional `id` prop to the shared `SectionCard` for section anchors, and updated this README. Existing SectionCard callers keep their previous behavior. No dependencies were added.

Reused the shared sidebar, header, routes, `SectionCard`, `PriorityBadge`, `LoadingState`, `ErrorState`, `EmptyState`, and the existing `getCaseFile()` service. The page loads the same shared case structure asynchronously; it does not introduce another fixture or integration contract.

All ten requested sections appear in order. The optional On this page links jump to those sections. Tips and CCTV use semantic tables with column/row headers and full wrapped descriptions. Focusable, labeled scroll containers keep wider tables usable with the keyboard at tablet widths. IDs and description text remain unchanged. Record timestamps are formatted in the timezone supplied by `lastSeen.timeZone` (Asia/Kolkata for this case), while date-only fields avoid browser-timezone shifts.

Lead summaries preserve the supplied order, rank, score, priority, source IDs, and uncertainty. Source IDs are displayed as compact badges, and View Lead Analysis opens the detailed existing page. No investigative values are computed. Follow-up actions come directly from the case-level `recommendedActions` array in its existing order. All supplied limitations remain visible in a separate section with a restrained navy accent.

Missing created date, gender, and circumstances are displayed as Not provided; the current fixture's Not supplied sentinel is normalized only for display. No operational details are inferred. The gender field is omitted when the property itself is absent. Missing subsections show their requested empty messages, and missing clothing/limitations or a wholly unavailable file also receive neutral empty states. Loading and failures use the shared state components with retry support.

No optional Case File print action was added: the existing print styles are specific to the Public Appeal document. No PDF support or changes to other page layouts were introduced.

Verification:

- Production build passed.
- The dev server was restarted after the interrupted session; the final Case File route loads directly.
- Browser inspection confirmed the canonical profile, appearance, last-known information, all 8 tips, all 6 CCTV descriptions, 3 lead summaries with source IDs, 3 case-level actions, and all 5 limitations.
- Temporarily empty tips, CCTV, leads, actions, and limitations verified the respective empty states without fallback records.
- A temporary delayed failure verified Loading case file, the load-error message, Try again, retry loading, and recovery to all three tables.
- Temporary mock overrides were removed. SHA-256 checks confirmed the service, canonical data, and Dashboard/Lead Analysis/Public Appeal source files remained unchanged.
- Laptop and tablet layouts were visually inspected. At 800 px viewport width, page content stayed within the viewport while wide tables scrolled internally. Keyboard right-arrow scrolling was verified.
- Section anchors, View Lead Analysis, Back to Case Dashboard, return navigation, and the active Case File sidebar state passed.
- Browser console reported no warnings or errors on the final preview tab.

## Phase 6 polish and hardening

All four screens now use a shared PageHeader and primary/secondary Button components. Header metadata, action sizes, status badges, spacing, and retry controls follow the same pattern. The sidebar is slightly narrower at tablet widths and scrolls vertically when necessary. Lead evidence columns stack until wider desktop widths. The appeal retains its distinct document treatment.

Route changes update the browser title, focus the page heading for keyboard/screen-reader orientation, and return to the top without interfering with Case File section anchors. Interactive focus outlines, semantic table headers, labeled keyboard-scrollable table regions, and the skip link remain available. No images or icon-only controls require additional labels.

The root case loader now separates loading, error, empty, and ready states and supports retry. A null case no longer leaves the app loading indefinitely. Dashboard counts and appearance fields tolerate missing values; presentation formatting is shared with Case File. Unknown dates/timezones preserve the supplied text instead of crashing or inventing facts. Height retains the correct lowercase cm unit.

The source audit found no prohibited identity claims, obsolete subject/case values, debug logging, or randomized demo data. Independent investigator verification wording was strengthened in the Dashboard, Case File, and shared footer. No records, scores, ranks, or appeal text changed. The canonical fixture's SHA-256 remains `0A5FA6BEC8E9F53161B7897B610EC1E91C91895670C263F1E82476C97F80EECB`.

Changed files:

- Added `src/components/common/Button.jsx`, `src/components/common/PageHeader.jsx`, and `tests/data-contract.test.js`.
- Removed unused `src/components/common/PagePlaceholder.jsx`.
- Moved `src/components/case-file/formatters.js` to `src/utils/formatters.js`; updated `DetailList.jsx`, `RecordTable.jsx`, and `LeadSummaryTable.jsx` imports.
- Updated `src/App.jsx`, all four `src/pages/*.jsx`, `CaseInfoCard.jsx`, `EvidenceSummary.jsx`, `LeadCard.jsx`, `ErrorState.jsx`, `Header.jsx`, and `Sidebar.jsx`.
- Updated `src/styles.css`, `src/services/api.js`, `.env.example`, `package.json`, and this README.

The service module documents unavailable/empty/error results and preserving supplied values/order. The blank `VITE_API_BASE_URL` remains reserved only. There are no HTTP calls, invented endpoints, new dependencies, backend changes, or new major screens.

Verification:

- All four routes checked at actual viewport widths 1440, 1280, 1024, and 768 px. No horizontal page overflow in any of the 16 combinations. Wide tables scroll only inside their containers; keyboard right-arrow scrolling and visible focus passed.
- Complete demo sequence checked: Dashboard → Analyze Case (disabled while pending) → completion → Lead Analysis → Public Appeal → Case File. Supplied ranks/scores, 8 tips, 6 CCTV records, 3 lead summaries, all 10 sections, and all 5 limitations remained present. Active routes, page-heading focus, section anchors, and back navigation passed.
- Temporary delayed/rejected responses verified loading, error, retry loading, and recovery for the root case and each asynchronous page. Null/empty results verified all page empty states. Empty Case File subsections and missing Dashboard appearance/date values rendered neutral fallbacks. Analysis rejection followed by a successful retry passed.
- Copy Text announced success. A temporary local clipboard read-back control confirmed the entire appeal text, including line breaks. The browser automation's separate virtual clipboard could not paste the native clipboard, so verification used the browser's Clipboard API in that temporary control.
- Print invoked without an application error. Temporarily applying print CSS to screen verified that sidebar, navigation, header/footer, and actions disappear while all document content and draft/review notices remain readable with no clipping. Native print dialog and paper pagination are not exposed by this in-app browser and remain a manual demo-browser check. Case File has no print action.
- Temporary overrides and clipboard controls were removed; restored service, appeal page, and stylesheet hashes matched their saved versions.
- `pnpm test`: four regression tests pass (canonical service consistency and source references, copy isolation/determinism, public-copy safety boundaries, and missing/date/time formatting).
- `pnpm run build`: passes with no warnings. After restoring the source, a fresh browser tab visited all four routes with no console warnings or errors. Earlier transient hot-reload errors during the formatter move were resolved by the completed imports and reload. The development server was restarted after the interrupted session and is serving port 5173.
- Final preview: `phase6-dashboard.png`. Responsive viewport overrides were reset after testing.

Phase 6 is the stopping point. Backend integration requires the real agreed contract in a separate phase.

## IBM Carbon UI update

Added IBM's official `@carbon/react` 1.117.0, Sass 1.105.0, and locally bundled IBM Plex fonts. The four existing routes use Carbon Button (including router links), Tag, Tile, InlineLoading, InlineNotification, Table/TableHead/TableBody/TableRow/TableCell, and Carbon navigation icons. The custom responsive sidebar remains in place with Carbon colors and iconography; Tailwind continues to handle the existing page layouts. This is a component integration, not a claim that every custom layout is an official Carbon component.

`src/carbon.scss` imports only the relevant component styles plus required layout/layer tokens, applies the g10 theme, and loads three local Latin font files. `vite.config.js` resolves Carbon's font paths and suppresses dependency-owned Sass deprecations while retaining application warnings. Package postinstall telemetry is disabled in the pnpm build policy; no runtime telemetry integration was added.

Changed: `package.json`, `pnpm-lock.yaml`, `pnpm-workspace.yaml`, `vite.config.js`, `src/main.jsx`, `src/styles.css`, new `src/carbon.scss`, shared Button/SectionCard/LoadingState/ErrorState, AnalysisStatus, PriorityBadge, Header, Sidebar, RecordTable, and this README. Case fixtures and service behavior are unchanged.

Run from VS Code with `npm run dev` (existing installed dependencies), or `pnpm run dev`. For a reproducible fresh installation use `pnpm install --frozen-lockfile`, since pnpm is the project's lockfile owner.

Verified the production build, all four existing tests, Analyze Case progress/completion, Carbon router links, all four routes, Copy Text success, Print invocation, and 8/6/3 table records across all 10 Case File sections. All 16 combinations of four routes and 1440/1280/1024/768px widths fit the page; record tables scroll internally. Production browser console has no warnings/errors. Native print pagination remains the previously documented manual check. The dev server recovered after dependency optimization and serves port 5173. Final preview: `carbon-dashboard.png`.

Reference: [IBM Carbon React documentation](https://carbondesignsystem.com/developing/frameworks/react/).
