# ai/search_engine.py

from .models import *


def search_database(question):

    matches = []

    words = question.lower().split()

    for item in Knowledge.objects.all():

        score = 0

        text = f"{item.title} {item.content}".lower()

        for word in words:

            if word in text:
                score += 1

        if score > 0:

            matches.append({
                "title": item.title,
                "content": item.content,
                "score": score
            })

    matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    print(matches)  # Debug

    return matches


