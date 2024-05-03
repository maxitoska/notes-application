import random

from django.contrib.auth.models import User
from django.db import models


def get_random_color() -> str:
    # List of all colors in the database
    all_colors = list(Colors.objects.values_list('color', flat=True))

    # Generate a random color
    random_color = "#" + "%06x" % random.randint(0, 0xFFFFFF)

    # Check for uniqueness of the color
    while random_color in all_colors:
        random_color = "#" + "%06x" % random.randint(0, 0xFFFFFF)

    return random_color


## <div style="background-color: {{ your_model_instance.color }}"></div>


class Categories(models.Model):
    title = models.CharField(max_length=55)


class Notes(models.Model):
    text = models.CharField(max_length=255)
    color = models.CharField(max_length=55, default='white')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Colors(models.Model):
    color = models.CharField(max_length=55, default=get_random_color)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
