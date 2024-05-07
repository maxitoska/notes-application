import random

NOTE_STATUS_CHOICES = {
    "active": "Active",
    "archive": "Archive"
}


def get_random_color() -> str:
    random_color = "#" + "%02x%02x%02x" % (
        random.randint(180, 255),
        random.randint(180, 255),
        random.randint(180, 255)
    )

    return random_color
