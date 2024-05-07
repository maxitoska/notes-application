from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from source import NOTE_STATUS_CHOICES, get_random_color


class Categories(models.Model):
    title = models.CharField(max_length=55)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Notes(models.Model):
    text = models.CharField(max_length=255)
    color = models.CharField(max_length=55, default='white')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=NOTE_STATUS_CHOICES)


class Colors(models.Model):
    color = models.CharField(max_length=55, default=get_random_color)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_categories_for_new_user(sender, instance, created, **kwargs):
    if created:
        predefined_categories = [
            "Study",
            "Work",
            "Daily tasks",
            "Personal notes",
            "Shopping",
            "Events",
            "Travel",
            "Health",
            "Finances",
            "Hobby"
        ]
        for category_name in predefined_categories:
            category = Categories.objects.create(title=category_name, user=instance)
            color = get_random_color()
            Colors.objects.create(color=color, category=category)


post_save.connect(create_categories_for_new_user, sender=User)
