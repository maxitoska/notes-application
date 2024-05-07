from django.urls import path, include

from notes_library.views import (
    index,
    get_notes_view,
    get_categories_view,
    create_note_view,
    delete_note_view,
    change_note_view,
    register_request,
    create_category_view, change_status_view
)

urlpatterns = [
    path("", index, name="index"),
    path("register/", register_request, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("get_notes/", get_notes_view, name="get_notes"),
    path("get_categories/", get_categories_view, name="get_categories"),
    path("create_note/", create_note_view, name="create_note"),
    path('delete_note/<int:note_id>/', delete_note_view, name='delete_note'),
    path('change_note/<int:note_id>/', change_note_view, name='change_note'),
    path('create_category/', create_category_view, name='create_category'),
    path(
        'change_status/<int:note_id>/',
        change_status_view,
        name='change_status'
    ),

]
app_name = "notes_library"
