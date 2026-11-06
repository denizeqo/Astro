"""
Simple staff-only file editor for sweph/ephe/ text/JSON files.

Exposes /admin/edit/ (file list) and /admin/edit/<filename>/ (edit + save).

Binary .se1 Swiss Ephemeris files are intentionally excluded — they are raw
planetary data consumed directly by pyswisseph and are not human-editable.
"""

import json
import shutil

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from pathlib import Path

EPHE_DIR = Path(settings.BASE_DIR) / "sweph" / "ephe"

# Files the client may edit. Binary .se1 files are excluded.
EDITABLE_FILES = [
    "arketipet.json",
    "planetNum.json",
    "aspects.json",
    "astro_planet_translations_complete.json",
    "astro_archetypes_multilingual.json",
    "stars.json",
    "stars2.json",
    "sefstars.txt",
]


def _editable_files():
    """Return a sorted list of {name, size} dicts for files that exist on disk."""
    result = []
    for name in EDITABLE_FILES:
        path = EPHE_DIR / name
        if path.exists():
            result.append({"name": name, "size": path.stat().st_size})
    result.sort(key=lambda f: f["name"])
    return result


@staff_member_required
def ephe_edit(request, filename=None):
    """List editable files (no filename) or edit/save one file."""

    # Security: only allow known filenames (no path traversal).
    if filename is not None and filename not in EDITABLE_FILES:
        messages.error(request, f"File '{filename}' is not editable.")
        return HttpResponseRedirect("/admin/edit/")

    target = EPHE_DIR / filename if filename else None

    # ---------------- POST: save a file ----------------
    if request.method == "POST" and filename:
        content = request.POST.get("content", "")

        # Validate JSON before writing so we never write a broken file.
        if filename.endswith(".json"):
            try:
                json.loads(content)
            except json.JSONDecodeError as exc:
                messages.error(request, f"Invalid JSON — not saved: {exc}")
                return render(
                    request,
                    "admin/edit_files.html",
                    {
                        "filename": filename,
                        "content": content,
                        "is_edit": True,
                    },
                )

        # Create a .bak backup before overwriting.
        if target and target.exists():
            backup = EPHE_DIR / (filename + ".bak")
            shutil.copy2(target, backup)

        target.write_text(content, encoding="utf-8")
        messages.success(
            request,
            f"Saved '{filename}'. Backup created as '{filename}.bak'.",
        )
        return HttpResponseRedirect(f"/admin/edit/{filename}/")

    # ---------------- GET: show edit form ----------------
    if filename:
        content = target.read_text(encoding="utf-8") if target and target.exists() else ""
        return render(
            request,
            "admin/edit_files.html",
            {"filename": filename, "content": content, "is_edit": True},
        )

    # ---------------- GET: show file list ----------------
    return render(
        request,
        "admin/edit_files.html",
        {"files": _editable_files(), "is_edit": False},
    )