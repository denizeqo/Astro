# Implementation Plan — Horoskopi Ditor Lunar (28 Lunar Mansions)

Status: **implemented, awaiting client review.**

## Decisions made (pending client confirmation)

| # | Question | Decision |
|---|----------|----------|
| 1 | Replace the Big 4 core chart? | **No — keep both.** `/coreChart` is untouched; the Lunar Mansions chart is a separate feature. |
| 2 | URL | **`/lunarChart`** (matches `coreChart`/`dailyChart` camelCase convention). `/lunar` remains the marketing landing page and now links to it. |
| 3 | Mansion images / pentacles | None existed in the repo. **28 placeholder pentacle SVGs** generated at `static/image/lunarMansions/mansion_01.svg … mansion_28.svg` (ruler-colored pentagram + mansion number + ruler glyph). Client can overwrite these files with final artwork — no code change needed. |
| 4 | Daily or natal? | **Both.** One `LunarChart` class returns a `birth` payload (natal) and a `moment` payload (defaults to *now* at the given location, or an explicit date/time from the form). The UI has a Daily/Birth toggle. |
| 5 | Mansion descriptions | **`sweph/ephe/lunarMansions.json`** — multilingual (en/de/fr/it), following the existing `astro_archetypes_multilingual.json` pattern. Seeded with the traditional 28 Manazil names, rulers cycling Sun → Moon → Mercury → Venus → Mars → Jupiter → Saturn (mansion 1 = Sun, yellow `#FFEA99`). **Descriptions are placeholders — replace with the client's Italian source text.** |
| 6 | Aspects | Only between **Moon, Sun, ASC, Saturn, North/South Node** (the document's reference points), using the existing flatlib machinery (aspect set 0/30/60/90/120/150/180, orb ≤ 2.5°), categorized `lunar` / `solar` / `ascendant` / `saturn` / `nodal`. |

## What was built

- `sweph/ephe/lunarMansions.json` — 28 mansions (name, ruler, image, en/de/fr/it title+description), 8 lunar phases, eclipse labels, ruler glyphs/colors.
- `MainApp/charts/lunarChart.py` — `LunarChart` class (all astronomy here, views stay thin):
  - mansion lookup (`MANSION_SIZE = 360/28 = 12°51'26"`)
  - 8 lunar phases from Sun–Moon elongation (45° windows) + illumination %
  - eclipse detection: New/Full Moon within 12° of a lunar node → solar/lunar eclipse
  - reference points with mansion, house, and `Num` archetype per point
  - categorized aspects between the 6 reference points
  - `to_dict()` → `{mansionSizeLabel, mansions, birth, moment}` (JSON-serializable)
- `MainApp/views.py::LunarChartPage` — thin view: GET renders the page, POST returns `LunarChart.to_dict()` (localized via `request.LANGUAGE_CODE`).
- `MainApp/urls.py` — `path('lunarChart', views.LunarChartPage, name='lunarChart')`.
- `templates/pages/lunarChart.html` — reuses the shared `wheelOfDestiny/form.html` (map + birth fields), adds optional moment date/time fields, Daily/Birth toggle, chart widget, mansion/phase cards, eclipse banner, reference-points and aspects tables.
- `static/js/lunarChart.js` — self-contained SVG renderer: 28-segment static mansion ring (click a segment → mansion card), wheel rotated so ASC is at 9 o'clock, aspect lines (green soft / red dashed hard), de-collided glyph placement, center lunar phase display.
- `static/image/lunarMansions/mansion_01.svg … mansion_28.svg` — placeholder pentacles.
- `templates/pages/products/lunar.html` — both CTAs now link to `/lunarChart`.
- `README.md` — route documented.

## Verified

- `python manage.py check` — no issues
- GET `/`, `/weel`, `/lunar`, `/lunarChart` → 200
- POST `/lunarChart` → 200 JSON (28 mansions, birth + moment payloads)
- Eclipse detection validated against the real 2024-04-08 total solar eclipse (detected, node distance 2.49°)

## Open items for the client

1. Replace placeholder mansion descriptions with the Italian source text (JSON keys are ready).
2. Replace placeholder pentacle SVGs with final artwork (same filenames).
3. Confirm ruler sequence (7 classical planets cycling, mansion 1 = Sun).
4. Confirm eclipse orb (currently 12° from the nodes).
5. DOCX report for the lunar chart (not built yet — the existing `/getReport` flow can be extended).
