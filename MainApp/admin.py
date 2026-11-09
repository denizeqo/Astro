from django.contrib import admin
from django.urls import path

from . import content_admin
from .models import DailyCalendar, MonthlyCalendar, Transit
from .admin_views import ephe_edit

# Register the existing models so they appear in the admin.
admin.site.register(DailyCalendar)
admin.site.register(MonthlyCalendar)
admin.site.register(Transit)

# ---------------------------------------------------------------------------
# Hook /admin/edit/ into Django's admin URL resolver.
# ---------------------------------------------------------------------------

_original_get_urls = admin.site.get_urls


def _custom_get_urls():
    urls = _original_get_urls()
    custom = [
        path("texts/", admin.site.admin_view(content_admin.texts_dashboard), name="texts_dashboard"),
        path("texts/translate/", admin.site.admin_view(content_admin.texts_translate), name="texts_translate"),
        path("texts/transits/", admin.site.admin_view(content_admin.texts_transits), name="texts_transits"),
        path(
            "texts/transits/<str:planet>/<int:house>/",
            admin.site.admin_view(content_admin.texts_transit_edit),
            name="texts_transit_edit",
        ),
        path("texts/archetypes/", admin.site.admin_view(content_admin.texts_archetypes), name="texts_archetypes"),
        path(
            "texts/archetypes/<str:kind>/<int:num>/",
            admin.site.admin_view(content_admin.texts_archetype_edit),
            name="texts_archetype_edit",
        ),
        path("texts/aspects/", admin.site.admin_view(content_admin.texts_aspects), name="texts_aspects"),
        path(
            "texts/aspects/<str:p1>/<str:p2>/<str:deg>/",
            admin.site.admin_view(content_admin.texts_aspect_edit),
            name="texts_aspect_edit",
        ),
        path("edit/", admin.site.admin_view(ephe_edit), name="ephe_edit_list"),
        path(
            "edit/<str:filename>/",
            admin.site.admin_view(ephe_edit),
            name="ephe_edit_file",
        ),
    ]
    return custom + urls


admin.site.get_urls = _custom_get_urls
