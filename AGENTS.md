# AGENTS.md — Guide for AI agents and contributors

Read this first. Single source of truth for what this project is and how to
work in it safely.

## What Astro is

A Django web app that generates astrological natal charts, transit/daily
charts, and personalized DOCX birth reports.
## Request flow

1. **Form POST** (`/weel`) with birth data
2. `MainApp/views.py::_build_chart_payload` →
   `MainApp/charts/motherChart.py::MotherChart`
3. Response JSON: `userData`, `fourAngles`, `planets`, `stars`,
   `staticChartSymbols`, `dynamicChartSymbols`, `aspects`
4. Frontend (`static/js/chart.js`) draws the chart wheel
5. **Report download**: POST JSON + image to `/getReport` → DOCX
## Where things live

| Path | Purpose |
|------|---------|
| `Astro/` | Django project settings/urls/wsgi |
| `MainApp/views.py` | HTTP views only |
| `MainApp/charts/motherChart.py` | Astronomy: chart, planets, angles, stars |
| `MainApp/charts/dailyChart.py` | Daily/transit charts |
| `MainApp/models.py` | DailyCalendar, MonthlyCalendar, Transit |
| `MainApp/urls.py` | URL routing |
| `MainApp/assets/report_template.docx` | docxtpl template |
| `sweph/ephe/` | Swiss Ephemeris data |
| `templates/` | pages + components |
| `static/css|js|image/` | frontend assets |
| `locale/` | i18n translations (en, de, fr, it) |
## Golden rules

1. **Views stay thin** — all astronomy goes in `charts/motherChart.py` or
   `charts/dailyChart.py`. Never import flatlib/swisseph in views.
2. **No hardcoded absolute paths** — build paths from `settings.BASE_DIR`.
3. **Service functions return plain JSON-serializable dicts/lists**.
4. **The `/weel` URL and `getReport`/`weel` URL names are public API** — keep stable.
5. **Never commit** `.venv/`, `db.sqlite3`, `staticfiles/`, `__pycache__/`, `.env`.
6. **Quality gate**: `python manage.py check` plus smoke-test GET `/`, `/weel`, POST `/getReport`.
## Intentional quirks — do NOT "fix" without asking

- URL path `/weel` is a typo for "wheel" but kept for link compatibility.
- `db.sqlite3` holds only Django's built-in tables; run
  `python3 manage.py migrate` to create it.
- The Django admin is enabled but unused.
