from django.contrib import admin
from django.urls import path

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
        path("edit/", admin.site.admin_view(ephe_edit), name="ephe_edit_list"),
        path(
            "edit/<str:filename>/",
            admin.site.admin_view(ephe_edit),
            name="ephe_edit_file",
        ),
    ]
    return custom + urls


admin.site.get_urls = _custom_get_urls
