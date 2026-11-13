# Astro

A Django web app that generates **astrological natal charts**, **transit/daily
charts**, and personalized **DOCX birth reports**. Built on Django 5.2 with
flatlib + pyswisseph (Swiss Ephemeris) for chart calculation.

See [`AGENTS.md`](AGENTS.md) for architecture and conventions, and
[`docs/architecture.md`](docs/architecture.md) for module/data-flow details.

## Stack

- Python 3.12+, Django 5.2
- flatlib + pyswisseph (Swiss Ephemeris) — ephemeris data in `sweph/ephe/`
- timezonefinder + pytz for local-time → UTC conversion
- python-docx + docxtpl for report generation
- Django i18n (en, de, fr, it)
- Templates + vanilla JS (Bootstrap, Leaflet) — no frontend build step

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install --force-reinstall --no-deps "pyswisseph>=2.10.3"

cp .env.example .env
python manage.py migrate
python manage.py runserver   # http://localhost:8000
```

## Routes

| URL | View | Purpose |
|-----|------|---------|
| `/` | `Home` | Natal chart |
| `/weel` | `Weel` | Wheel of Destiny (POST → chart JSON) |
| `/getReport` | `getReport` | POST chart data + image → DOCX |
| `/dailyChart` | `DailyChartPage` | Daily/transit chart |
| `/coreChart` | `CoreChart` | Big 4 core chart (Sun, Moon, ASC, MC) |
| `/lunarChart` | `LunarChartPage` | 28 Lunar Mansions chart — daily + birth (POST → chart JSON) |
| `/aboutUs` | `AboutUs` | About page |
| `/astroShop` | `AstroShop` | Shop page |
| `/everythingAbout` | `EverythingAbout` | Astrology encyclopedia |
| `/birthChart`, `/lunar`, `/evolution`, `/ancientwisdom`, `/relationships`,
  `/astrography`, `/soul`, `/magnetism`, `/innerWorld`, `/essentialOils`, `/stars`,
  `/forecast` | `pr*` views | Product pages |
| `/admin/` | Django admin | admin |
