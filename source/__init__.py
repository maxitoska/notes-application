import random
import re

from collections import Counter

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


def count_unique_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    unique_word_count = len(word_counts)
    return unique_word_count
