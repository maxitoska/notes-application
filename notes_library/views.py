import json

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from notes_library.services import (
    get_user_by_id,
    get_notes,
    create_note,
    get_categories,
    get_id_by_category,
    get_color_by_category_id,
    delete_note_by_id,
    create_new_category, change_note, change_note_status
)


def index(request):
    user = request.user
    categories = get_categories(user_id=user.id)
    context = {
        'username': user.username,
        'categories': categories
    }
    return render(request, "notes_library/index.html", context=context)


def delete_note_view(request, note_id: int):
    user = get_user_by_id(request.user.id)
    deletion_successful = delete_note_by_id(note_id=note_id, user=user)
    if deletion_successful:
        return JsonResponse({'message': 'Note deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Failed to delete note'}, status=500)


def change_note_view(request, note_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            new_text = data.get('text', '')
            changed_note = change_note(text=new_text, note_id=note_id)
            return JsonResponse(changed_note)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def create_note_view(request):
    if request.method == "POST":
        note_text = request.POST.get("note_text")
        user = request.user
        user_id = request.user.id
        if request.POST.get('category_name') != "Select a category":
            category = request.POST.get('category_name')
            category_id = get_id_by_category(category_name=category, user_id=user_id).id
            color = get_color_by_category_id(category_id=category_id).color
        else:
            color = "White"
            category_id = None

        create_note(
            user=user,
            text=note_text,
            color=color,
            category_id=category_id

        )
        return JsonResponse({"data": "sucess"})


def get_categories_view(request):
    formatted_notes = []
    user_id = request.user.id
    categories = get_categories(user_id=user_id)

    for category in categories:
        formatted_notes.append({'id': category.id, 'name': category.title})
    data = {"data": formatted_notes}
    return JsonResponse(data)


def get_notes_view(request):
    user_id = request.user.id
    notes = get_notes(user_id=user_id)
    formatted_notes = [
        {
            "id": note.id,
            "text": note.text,
            "color": note.color,
            "status": note.status,
            "category": note.category.title
        }
        for note in notes
    ]

    data = {"data": formatted_notes}
    return JsonResponse(data)


def create_category_view(request):
    user = request.user
    if request.method == "POST":
        category_name = request.POST.get("category_text")
        creating_successful = create_new_category(category_name=category_name, user=user)
        if creating_successful:
            return JsonResponse({'message': 'Category created successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Failed to created category'}, status=500)


def change_status_view(request, note_id: int):
    user_id = request.user.id
    if request.method == "POST":
        changing_successful = change_note_status(user_id=user_id, note_id=note_id)
        return JsonResponse(changing_successful)


def register_request(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        try:
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Registration successful.")

                return redirect(reverse("notes_library:index"))
            else:
                # Если форма не валидна, добавьте сообщения об ошибках.
                if "username" in form.errors:
                    messages.error(request, "Username is already taken.")
        except Exception as ex:
            print(ex)
    else:
        form = UserCreationForm()

    return render(
        request=request,
        template_name="registration/register.html",
        context={"register_form": form},
    )
