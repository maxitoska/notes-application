from django.urls import path, include

from notes_library.views import index

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
]
app_name = "notes_library"
