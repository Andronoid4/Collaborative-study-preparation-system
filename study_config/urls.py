from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("students/", include("students.urls")),
    path("groups/", include("groups.urls")),
    path("topics/", include("topics.urls")),
    path("tasks/", include("tasks.urls")),
]
