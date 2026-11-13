"""
Client-friendly "Site Texts" editor.

Structured, staff-only editing for the site's text content, exposed under
/admin/texts/. Replaces raw JSON editing with plain-language forms:

- Planet-in-house transit texts (astro_planet_translations_complete.json)
- Archetype numbers             (astro_archetypes_multilingual.json + arketipet.json)
- Aspect texts                  (aspects.json)
- Daily calendar descriptions   (DailyCalendar model)
- Monthly calendar descriptions (MonthlyCalendar model)

Fixed/astronomical data (stars.json, stars2.json, planetNum.json,
sefstars.txt, *.se1) is intentionally NOT editable anywhere in the admin.

Saves are safe by construction: only the edited leaf fields are written back,
the JSON key structure is never altered, a .bak backup is created before each
save, and the file is replaced atomically.
"""

import json
import os
import shutil
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

EPHE_DIR = Path(settings.BASE_DIR) / "sweph" / "ephe"

LANGUAGES = [
    ("it", "Italiano"),
    ("en", "Inglese"),
    ("de", "Tedesco"),
    ("fr", "Francese"),
]
LANG_CODES = [code for code, _name in LANGUAGES]

TRANSITS_FILE = "astro_planet_translations_complete.json"
ARCHETYPES_FILE = "astro_archetypes_multilingual.json"
ARKETIPET_FILE = "arketipet.json"
ASPECTS_FILE = "aspects.json"

TRANSIT_FIELDS = [
    ("title", "Title"),
    ("description", "Description"),
    ("warning", "Warning"),
]

ASPECT_ANGLE_NAMES = {
    "0": "Conjunction",
    "30": "Semi-sextile",
    "60": "Sextile",
    "90": "Square",
    "120": "Trine",
    "150": "Quincunx",
    "180": "Opposition",
}


# ---------------------------------------------------------------------------
# Safe JSON IO
# ---------------------------------------------------------------------------

def _load_json(filename):
    return json.loads((EPHE_DIR / filename).read_text(encoding="utf-8"))


def _save_json(filename, data):
    """Write JSON atomically (temp file + replace) after making a .bak backup."""
    target = EPHE_DIR / filename
    if target.exists():
        shutil.copy2(target, EPHE_DIR / (filename + ".bak"))
    tmp = EPHE_DIR / (filename + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, target)


def _lang_values(get_value):
    """Build the per-language values structure used by entry_form.html."""
    return [
        {"code": code, "name": name, "values": get_value(code)}
        for code, name in LANGUAGES
    ]


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def texts_dashboard(request):
    counts = {}
    try:
        counts["transits"] = len(_load_json(TRANSITS_FILE).get("planet_houses", []))
    except Exception:
        counts["transits"] = 0
    try:
        arch = _load_json(ARCHETYPES_FILE)
        counts["archetypes"] = sum(len(arch.get(k, {})) for k in ("A", "B"))
    except Exception:
        counts["archetypes"] = 0
    try:
        aspects = _load_json(ASPECTS_FILE)
        counts["aspects"] = sum(
            len(degs) for p2s in aspects.values() for degs in p2s.values()
        )
    except Exception:
        counts["aspects"] = 0

    return render(request, "admin/texts/dashboard.html", {"counts": counts})



# ---------------------------------------------------------------------------
# Auto-translate (AJAX)
# ---------------------------------------------------------------------------

def _translate_text(text, source, target):
    """Translate text, chunking on paragraph breaks for long inputs."""
    from deep_translator import GoogleTranslator

    translator = GoogleTranslator(source=source, target=target)
    if len(text) <= 4500:
        return translator.translate(text)

    chunks, current = [], ""
    for part in text.split("\n"):
        if current and len(current) + len(part) + 1 > 4500:
            chunks.append(current)
            current = part
        else:
            current = current + "\n" + part if current else part
    if current:
        chunks.append(current)
    return "\n".join(translator.translate(chunk) for chunk in chunks)


@require_POST
def texts_translate(request):
    """Translate a set of fields from one language into all the others.

    POST body (JSON): {"source": "en", "texts": {"title": "...", ...}}
    Response: {"translations": {"de": {"title": "..."}, ...}}
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid request body."}, status=400)

    source = payload.get("source", "it")
    texts = payload.get("texts", {})
    if source not in LANG_CODES or not isinstance(texts, dict):
        return JsonResponse({"error": "Invalid source language or texts."}, status=400)

    try:
        import deep_translator  # noqa: F401
    except ImportError:
        return JsonResponse(
            {"error": "Auto-translate is not available (deep-translator is not "
                      "installed). Please fill in the other languages manually."},
            status=503,
        )

    translations = {}
    for code in LANG_CODES:
        if code == source:
            continue
        translated = {}
        for field, text in texts.items():
            if not isinstance(text, str) or not text.strip():
                translated[field] = text if isinstance(text, str) else ""
                continue
            try:
                translated[field] = _translate_text(text, source, code)
            except Exception as exc:
                return JsonResponse(
                    {"error": f"Translation to '{code}' failed: {exc}"},
                    status=502,
                )
        translations[code] = translated

    return JsonResponse({"translations": translations})


# ---------------------------------------------------------------------------
# Transit texts (planet in house)
# ---------------------------------------------------------------------------

def texts_transits(request):
    data = _load_json(TRANSITS_FILE)
    entries = data.get("planet_houses", [])

    q = request.GET.get("q", "").strip().lower()
    planet = request.GET.get("planet", "").strip().lower()
    house = request.GET.get("house", "").strip()

    rows = []
    for entry in entries:
        en = entry.get("translations", {}).get("en", {})
        haystack = " ".join([
            entry.get("planet", ""),
            en.get("title", "") or "",
            en.get("description", "") or "",
            en.get("warning", "") or "",
        ]).lower()
        if planet and entry.get("planet") != planet:
            continue
        if house and str(entry.get("house")) != house:
            continue
        if q and q not in haystack:
            continue
        rows.append({
            "planet": entry.get("planet", ""),
            "house": entry.get("house", ""),
            "title": en.get("title", ""),
            "snippet": (en.get("description", "") or "")[:140],
        })

    planets = sorted({e.get("planet", "") for e in entries})
    houses = sorted({e.get("house") for e in entries})

    return render(request, "admin/texts/transits_list.html", {
        "rows": rows,
        "planets": planets,
        "houses": houses,
        "q": request.GET.get("q", ""),
        "selected_planet": planet,
        "selected_house": house,
        "total": len(entries),
    })


def texts_transit_edit(request, planet, house):
    data = _load_json(TRANSITS_FILE)
    entry = next(
        (e for e in data.get("planet_houses", [])
         if e.get("planet") == planet and e.get("house") == house),
        None,
    )
    if entry is None:
        messages.error(request, f"No transit entry found for {planet} in house {house}.")
        return HttpResponseRedirect(reverse("admin:texts_transits"))

    if request.method == "POST":
        translations = entry.setdefault("translations", {})
        for code in LANG_CODES:
            block = translations.setdefault(code, {})
            for field, _label in TRANSIT_FIELDS:
                block[field] = request.POST.get(f"{code}__{field}", "")
        _save_json(TRANSITS_FILE, data)
        messages.success(
            request,
            f"Saved {planet.title()} in House {house}. Backup: {TRANSITS_FILE}.bak",
        )
        return HttpResponseRedirect(
            reverse("admin:texts_transit_edit", kwargs={"planet": planet, "house": house})
        )

    return render(request, "admin/texts/entry_form.html", {
        "heading": f"{planet.title()} in House {house}",
        "sub_heading": "Transit text — shown when this planet moves through this house.",
        "fields": [
            {"key": "title", "label": "Title", "textarea": False},
            {"key": "description", "label": "Description", "textarea": True},
            {"key": "warning", "label": "Warning", "textarea": True},
        ],
        "languages": _lang_values(
            lambda code: {
                field: entry.get("translations", {}).get(code, {}).get(field, "")
                for field, _label in TRANSIT_FIELDS
            }
        ),
        "extras": [],
        "back_url": reverse("admin:texts_transits"),
        "back_label": "Back to transit texts",
    })


# ---------------------------------------------------------------------------
# Archetype numbers
# ---------------------------------------------------------------------------

def _sort_numbers(numbers):
    return sorted(numbers, key=lambda n: int(n))


def texts_archetypes(request):
    data = _load_json(ARCHETYPES_FILE)
    q = request.GET.get("q", "").strip().lower()
    kind_filter = request.GET.get("kind", "").strip().upper()

    rows = []
    for kind in ("B", "A"):
        if kind_filter and kind != kind_filter:
            continue
        for num in _sort_numbers(data.get(kind, {}).keys()):
            node = data[kind][num]
            title = node.get("title", "") or ""
            en_text = node.get("en", "") or ""
            if q and q not in (title + " " + en_text).lower():
                continue
            rows.append({
                "kind": kind,
                "num": num,
                "title": title,
                "snippet": en_text[:140],
            })

    return render(request, "admin/texts/archetypes_list.html", {
        "rows": rows,
        "q": request.GET.get("q", ""),
        "selected_kind": kind_filter,
        "total": sum(len(data.get(k, {})) for k in ("A", "B")),
    })


def texts_archetype_edit(request, kind, num):
    kind = kind.upper()
    if kind not in ("A", "B"):
        messages.error(request, f"Unknown archetype type '{kind}'.")
        return HttpResponseRedirect(reverse("admin:texts_archetypes"))

    data = _load_json(ARCHETYPES_FILE)
    entry = data.get(kind, {}).get(str(num))
    if entry is None:
        messages.error(request, f"No archetype entry found for type {kind}, number {num}.")
        return HttpResponseRedirect(reverse("admin:texts_archetypes"))

    arketipet = _load_json(ARKETIPET_FILE)
    has_arketip = str(num) in arketipet.get(kind, {})

    if request.method == "POST":
        entry["title"] = request.POST.get("title", entry.get("title", ""))
        for code in LANG_CODES:
            entry[code] = request.POST.get(f"{code}__text", "")
        _save_json(ARCHETYPES_FILE, data)

        if has_arketip:
            arketipet[kind][str(num)] = request.POST.get(
                "arketip_name", arketipet[kind][str(num)]
            )
            _save_json(ARKETIPET_FILE, arketipet)

        messages.success(
            request,
            f"Saved archetype {kind} #{num}. Backups created next to the original files.",
        )
        return HttpResponseRedirect(
            reverse("admin:texts_archetype_edit", kwargs={"kind": kind, "num": num})
        )

    extras = [{
        "name": "title",
        "label": "Title (shared across languages)",
        "value": entry.get("title", ""),
        "textarea": False,
    }]
    if has_arketip:
        extras.append({
            "name": "arketip_name",
            "label": "Short name (used on the chart)",
            "value": arketipet[kind][str(num)],
            "textarea": False,
        })

    return render(request, "admin/texts/entry_form.html", {
        "heading": f"Archetype {kind} — Number {num}",
        "sub_heading": "The numbered archetype text shown on the daily chart.",
        "fields": [{"key": "text", "label": "Description", "textarea": True}],
        "languages": _lang_values(lambda code: {"text": entry.get(code, "")}),
        "extras": extras,
        "back_url": reverse("admin:texts_archetypes"),
        "back_label": "Back to archetypes",
    })



# ---------------------------------------------------------------------------
# Aspect texts (planet-to-planet angles)
# ---------------------------------------------------------------------------

def texts_aspects(request):
    data = _load_json(ASPECTS_FILE)
    planets = list(data.keys())

    p1 = request.GET.get("p1", "")
    p2 = request.GET.get("p2", "")
    deg = request.GET.get("deg", "")
    q = request.GET.get("q", "").strip().lower()

    pairs = sorted(data[p1].keys()) if p1 in data else []
    angles = []
    if p1 in data and p2 in data[p1]:
        angles = [
            {"deg": deg_val, "name": ASPECT_ANGLE_NAMES.get(deg_val, f"{deg_val}°")}
            for deg_val in sorted(data[p1][p2].keys(), key=lambda d: int(d))
        ]

    matches = []
    if q:
        for planet1, p2s in data.items():
            for planet2, degs in p2s.items():
                for deg_val, langs in degs.items():
                    text = langs.get("en", "") or ""
                    if q in text.lower():
                        matches.append({
                            "p1": planet1,
                            "p2": planet2,
                            "deg": deg_val,
                            "angle_name": ASPECT_ANGLE_NAMES.get(deg_val, f"{deg_val}°"),
                            "snippet": text[:140],
                        })
                        if len(matches) >= 50:
                            break
                if len(matches) >= 50:
                    break
            if len(matches) >= 50:
                break

    # Embed all data as JSON for dynamic dropdowns (no page reloads)
    aspects_json = json.dumps(data)
    angle_names_json = json.dumps(ASPECT_ANGLE_NAMES)

    return render(request, "admin/texts/aspects_pick.html", {
        "planets": planets,
        "pairs": pairs,
        "angles": angles,
        "selected_p1": p1,
        "selected_p2": p2,
        "selected_deg": deg,
        "aspects_json": aspects_json,
        "angle_names_json": angle_names_json,
        "q": request.GET.get("q", ""),
        "matches": matches,
        "total": sum(len(degs) for p2s in data.values() for degs in p2s.values()),
    })


def texts_aspect_edit(request, p1, p2, deg):
    data = _load_json(ASPECTS_FILE)
    entry = data.get(p1, {}).get(p2, {}).get(deg)
    if entry is None:
        messages.error(request, f"No aspect text found for {p1} / {p2} at {deg}°.")
        return HttpResponseRedirect(reverse("admin:texts_aspects"))

    angle_name = ASPECT_ANGLE_NAMES.get(deg, f"{deg}°")

    if request.method == "POST":
        for code in LANG_CODES:
            entry[code] = request.POST.get(f"{code}__text", "")
        _save_json(ASPECTS_FILE, data)
        messages.success(
            request,
            f"Saved {p1} {angle_name} {p2}. Backup: {ASPECTS_FILE}.bak",
        )
        return HttpResponseRedirect(
            reverse("admin:texts_aspect_edit", kwargs={"p1": p1, "p2": p2, "deg": deg})
        )

    return render(request, "admin/texts/entry_form.html", {
        "heading": f"{p1} {angle_name} {p2} ({deg}°)",
        "sub_heading": "Aspect text — shown when these two bodies form this angle.",
        "fields": [{"key": "text", "label": "Description", "textarea": True}],
        "languages": _lang_values(lambda code: {"text": entry.get(code, "")}),
        "extras": [],
        "back_url": reverse("admin:texts_aspects"),
        "back_label": "Back to aspect texts",
    })



# Daily & monthly calendar DB editors were removed — the DailyCalendar and
# MonthlyCalendar tables are empty and unused by the frontend (which reads
# descriptions from JSON files via the API).

