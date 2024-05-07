from django.contrib.auth.models import User
from django.db.models import QuerySet

from notes_library.models import (
    Notes,
    Colors,
    Categories
)
from source import get_random_color


class UserRepository:
    def __init__(self):
        self.model = User

    def get(self, pk) -> QuerySet[User]:
        return self.model.objects.get(id=pk)


class NotesRepository:
    def __init__(self):
        self.model = Notes

    def get_user_notes(self, user_id: int) -> QuerySet[Notes]:
        return self.model.objects.filter(user_id=user_id)

    def create_new_note(
            self,
            user: User,
            text: str,
            color: str | None,
            category_id: int | None
    ) -> QuerySet[Notes]:
        note = self.model.objects.create(
            text=text,
            color=color,
            user=user,
            category_id=category_id,
            status="active"
        )
        return note

    def delete_note_by_id(self, note_id: int, user: User) -> bool:
        try:
            note = self.model.objects.get(id=note_id, user=user)
            note.delete()
            return True
        except Exception as e:
            print(f"Error deleting note: {e}")
            return False  # Deletion failed

    def change_note_text(self, text: str, note_id: int) -> dict[str, str]:
        try:
            note = self.model.objects.get(id=note_id)
            note.text = text
            note.save()
            return {'message': 'Note updated successfully'}
        except Exception as e:
            print(f"error: {e}")
            return {'message': 'Failed Note update'}

    def change_note_status(self, user_id: int, note_id: int) -> dict[str, str]:
        try:
            note = self.model.objects.get(id=note_id, user_id=user_id)
            note.status = "archive"
            note.save()
            return {'message': 'Note status updated successfully'}
        except Exception as e:
            print(f"error: {e}")
            return {'message': 'Failed Note status update'}


class CategoriesRepository:
    def __init__(self):
        self.model = Categories

    def get_categories(self, user_id: int) -> QuerySet[Categories]:
        return self.model.objects.filter(user_id=user_id)

    def get_id_by_category(
            self,
            category_name: str,
            user_id: int
    ) -> QuerySet[Categories]:
        return self.model.objects.get(title=category_name, user_id=user_id)

    def create_new_category(self, category_name: str, user: User) -> bool:
        try:
            category = self.model.objects.create(
                title=category_name,
                user=user
            )
            color = get_random_color()
            Colors.objects.create(color=color, category=category)
            return True
        except Exception as e:
            print(f"Error creating new category: {e}")
            return False


class ColorsRepository:
    def __init__(self):
        self.model = Colors

    def get_color_by_category_id(
            self,
            category_id: int
    ) -> QuerySet[Colors]:
        return self.model.objects.get(category_id=category_id)
