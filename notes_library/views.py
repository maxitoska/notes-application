from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse


@login_required
def index(request):
    user = request.user
    context = {
        'username': user.username
    }
    return render(request, "notes_library/index.html", context=context)


def register_request(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        try:
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Registration successful.")

                return redirect(reverse('login'))
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
