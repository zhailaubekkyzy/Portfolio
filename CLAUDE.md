# Portfolio — Tomiris (Gulsara) Zhailaubekkyzy

Static product-portfolio site, bilingual (Russian + English). Deployed on Vercel from this repo: every push to `main` updates the live site.
The owner writes in Russian; reply in Russian unless she switches.

## Structure
- `index.html` — home page with the project list (built from `src/home.src.html`). RU/EN toggle; `#en` opens English.
- `rfm-smartflow.html`, `rfm-dashboard.html` — Russian pages of the RFM case. `en/…` — English versions.
- `files/` — PDFs and Excel attached to cases (Russian only; English links say "(RU)").
- `src/` — sources. **Edit only `src/`, then run `python3 src/build.py`** — it regenerates all pages above and prints any untranslated Russian text.
  - `home.src.html` — home page. Projects are the `PROJECTS` array; every text field has `ru` and `en`.
  - `case.src.html` + `en_case.py` — case page; `en_case.py` holds (Russian, English) pairs.
  - `crm.src.html` + `en_crm.py` — CRM-style dashboard; `sim.js` (demo-data generator) and `analytics.js` are inlined by the build. `en_crm.py` holds a fragment → English table.
  - `build_xlsx.py`, `data.json`, `sample.json`, `strat.json` — the Excel file and figures behind the case.
  - `booklover.src.html` + `booklover_text.py` — BookLover retention case (training case, data from the course brief). The page uses `{{key}}` placeholders; `booklover_text.py` holds every text as (Russian, English). Builds `booklover-retention.html` + `en/booklover-retention.html`. SQL in `files/booklover-retention.sql`.

## Adding a project
1. Put the case page in `src/` (or as a plain page at the root plus `en/` copy) and files in `files/`.
2. Add an object to `PROJECTS` in `src/home.src.html` with `ru` and `en` for every text and URL.
3. `python3 src/build.py`, check both languages in a browser, commit, push.

## Rules
- Every page must exist in both languages; the home page keeps one bilingual file.
- Data in the RFM case is simulated demo data — always label it as such, never present it as real SmartFlow data.
- Name on the site: «Томирис (Гулсара) Жайлаубеккызы» / "Tomiris (Gulsara) Zhailaubekkyzy".
- Number format: RU `15,7%`, `1 000`, `109 млн ₸`; EN `15.7%`, `1,000`, `₸109M`.
- There is also a Claude artifact copy of the site: https://claude.ai/artifact/1jttGZmaZsrLGkAfmY7avA (publish `src/home.src.html` as the page, other pages and files via the files map with the same paths).
