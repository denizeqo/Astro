# Astro — Architecture

Module breakdown, data flow, JSON schemas, and data-file layout for the Astro
Django project. Complements [`AGENTS.md`](AGENTS.md) (conventions/golden rules)
and [`README.md`](README.md) (setup + routes).

> Note: the URL path `/weel` is a typo for "wheel" but is kept for link
> compatibility. Do not rename it without coordinating with the frontend.

---

## 1. Module breakdown

| Module | Responsibility |
|--------|----------------|
| `Astro/settings.py` | Django settings. `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` read from env vars with safe dev defaults. `BASE_DIR` used for all path construction. |
| `MainApp/urls.py` | URL routing. Public API names: `Home` (`/`), `weel` (`/weel`), `getReport` (`/getReport`), `dailyChart` (`/dailyChart`), `aboutUs`, `astroShop`, `everythingAbout`, product `pr*` pages, `/admin/`. |
| `MainApp/views.py` | Thin HTTP views only. No astronomy imports. Views: `Home`, `Weel` (POST → chart JSON), `getReport` (POST chart data + image → DOCX), `DailyChartPage`, `EverythingAbout`, `AboutUs`, `AstroShop`, `pr*` product pages, `DailyCalendarDescription`, `MonthlyCalendarCreated`, `MonthlyCalendarDescription`. |
| `MainApp/charts/motherChart.py` | **All natal-chart astronomy.** `MotherChart` class: planets, four angles, fixed stars, aspects, talisman, `userData`. Uses flatlib + pyswisseph (Swiss Ephemeris). `ephePath = str(Path(settings.BASE_DIR) / "sweph" / "ephe")`. |
| `MainApp/charts/dailyChart.py` | **Daily / transit charts.** `DailyChart` class builds a `birthChart` (MotherChart) and a `todayChart` (MotherChart) and exposes combined data: `birthChartPlanets/FourAngles/Stars/UserData/Talisman`, `todayChart*`, `combinePlanets`, `combineStars`, `todayChartPlanets`, `getStarsForPlanet()`, `getTransitTitle()`. |
| `MainApp/chartUtility.py` | Legacy/shared chart helpers used by `Weel`/`getReport`: `createChart`, `getPlanets`, `getFourAngles`, `getStars`, `getChartSymbols`, `get_all_aspects`, `getUserData`, plus DOCX report table builders. Also reads `sweph/ephe/` via `Path(settings.BASE_DIR)`. |
| `MainApp/models.py` | `DailyCalendar`, `MonthlyCalendar`, `Transit` (Django ORM; `db.sqlite3` holds only built-in + these tables). |
| `MainApp/assets/report_template.docx` | docxtpl template for the personalized birth report (POST `/getReport`). |
| `static/js/chart.js` | Canvas chart-wheel renderer (consumes POST `/weel` JSON). |
| `templates/` | Django templates (`pages/`, `components/`). No frontend build step; Bootstrap + Leaflet. |
| `sweph/ephe/` | Swiss Ephemeris + fixed-star data files (see §4). |
| `locale/` | i18n translations (en, de, fr, it). |

**Golden rule:** views stay thin; all astronomy lives in `charts/motherChart.py` or
`charts/dailyChart.py` (or the shared `chartUtility.py` helpers). Never import
flatlib/swisseph in a view.
---

## 2. Request flow

### 2.1 Natal chart / wheel — `GET /` (`Home`) and `POST /weel` (`Weel`)

1. Browser POSTs birth data to `/weel`.
2. `Weel` → `MainApp/charts/motherChart.py::MotherChart` computes the chart.
3. Response JSON:
   ```json
   {
     "userData": { ... },
     "fourAngles": [ ... ],
     "planets": [ ... ],
     "stars": [ ... ],
     "staticChartSymbols": [ ... ],
     "dynamicChartSymbols": [ ... ],
     "aspects": [ ... ]
   }
   ```
4. `static/js/chart.js` draws the chart wheel from the JSON.

`Home` renders the natal-chart page directly (server-side template context)
using the same `MotherChart` fields.

### 2.2 Daily / transit chart — `GET/POST /dailyChart` (`DailyChartPage`)

`DailyChart` builds both a birth chart and a today/transit chart and combines
them (combined planets/stars, transit titles per planet/house).

### 2.3 Report download — `POST /getReport` (`getReport`)

Accepts chart JSON + chart image, renders `MainApp/assets/report_template.docx`
via docxtpl, returns a ~400 KB DOCX.

---

## 3. Chart JSON schema (POST `/weel`)

Top-level keys:

| Key | Type | Description |
|-----|------|-------------|
| `userData` | dict | First/last name, city, country, lat/lng, local & UTC time, `talisman` list |
| `fourAngles` | list[dict] | Ascendant/MC/etc. with `position` |
| `planets` | list[dict] | 13 planets with `name`, `position`, `house`, `color`, `num`, etc. |
| `stars` | list[dict] | ~35 fixed stars with `name`, `position`, `color`, `house`, `orbite` |
| `staticChartSymbols` | list | Symbols computed at rotation 0 |
| `dynamicChartSymbols` | list | Symbols rotated to the ascendant position |
| `aspects` | list[dict] | 12 aspects with `active`, `passive`, `type`, `orb`, `deg`, `movement`, colors |

Planet dict fields (representative): `name`, `position`, `house` (`{num, symbol}`),
`color`, `num` (`{value, color, sup, supColor}`).


---

## 4. Data files in `sweph/ephe/`

| File | Purpose |
|------|---------|
| `seas_18.se1`, `sepl_18.se1`, `semo_18.se1` | Swiss Ephemeris planetary ephemeris segments |
| `sefstars.txt` | Fixed-star data |
| `stars.json`, `stars2.json` | Fixed stars used by chart calculation |
| `astro_planet_translations_complete.json` | Planet → house transit titles (consumed by `DailyChartPage`) |
| `astro_archetypes_multilingual.json` | Archetype translations |
| `aspects.json` | Aspect data |
| `planetNum.json` | Planet numerology data |
| `arketipet.json` | Arketipet (numerology) lookup |

All are read through `MotherChart.ephePath` =
`str(Path(settings.BASE_DIR) / "sweph" / "ephe")` and joined with
`Path(MotherChart.ephePath) / "<file>"` — **never** string concatenation with
backslashes, so paths work on Linux and Windows.

---

## 5. Template structure

```
templates/
├── pages/           # full page templates (home.html, wheelOfDestiny.html,
│                    # aboutUs.html, everythingAboutAstro.html, product pages)
└── components/      # reusable includes (chart/, aboutUs/, etc.)
```

Template includes use forward slashes (e.g. `components/aboutUs/style.html`);
backslashes were removed because they break on Linux.

---

## 6. Conventions & quality gate

- No hardcoded absolute paths — build from `settings.BASE_DIR` (`AGENTS.md` rule 2).
- Service functions return plain JSON-serializable dicts/lists (rule 3).
- `/weel` and `getReport`/`weel` URL names are public API — keep stable (rule 4).
- Never commit `.venv/`, `db.sqlite3`, `staticfiles/`, `__pycache__/`, `.env` (rule 5).
- Quality gate: `python manage.py check` + smoke-test GET `/`, `/weel`, POST `/getReport`.

