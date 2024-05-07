from django.db.models import QuerySet

from notes_library.models import Categories, Colors
from notes_library.repositories import (
    UserRepository,
    NotesRepository,
    CategoriesRepository,
    ColorsRepository
)
from django.contrib.auth.models import User


def get_user_by_id(pk: int):
    repository = UserRepository()
    return repository.get(pk=pk)


def get_notes(user_id: int):
    repository = NotesRepository()
    return repository.get_user_notes(user_id=user_id)


def create_note(
        user: User,
        text: str,
        color: str = 'White',
        category_id: int = None,

):
    repository = NotesRepository()
    return repository.create_new_note(
        user=user,
        text=text,
        color=color,
        category_id=category_id
    )


def change_note_status(user_id: int, note_id: int) -> dict[str, str]:
    repository = NotesRepository()
    return repository.change_note_status(user_id=user_id, note_id=note_id)


def delete_note_by_id(note_id: int, user: User) -> bool:
    repository = NotesRepository()
    return repository.delete_note_by_id(note_id=note_id, user=user)


def change_note_text(text: str, note_id: int) -> dict[str, str]:
    repository = NotesRepository()
    return repository.change_note_text(text=text, note_id=note_id)


def get_categories(user_id: int) -> QuerySet[Categories]:
    repository = CategoriesRepository()
    return repository.get_categories(user_id=user_id)


def get_id_by_category(
        category_name: str, user_id: int
) -> QuerySet[Categories]:
    repository = CategoriesRepository()
    return repository.get_id_by_category(
        category_name=category_name,
        user_id=user_id
    )


def get_color_by_category_id(category_id: int) -> QuerySet[Colors]:
    repository = ColorsRepository()
    return repository.get_color_by_category_id(category_id=category_id)


def create_new_category(category_name: str, user: User) -> bool:
    repository = CategoriesRepository()
    return repository.create_new_category(
        category_name=category_name,
        user=user
    )
