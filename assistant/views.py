from django.shortcuts import render

from .models import Conversation
from .services.ai_engine import get_cipher_response


def home(request):

    if request.method == "POST":

        message = request.POST.get("message")

        answer = get_cipher_response(message)

        Conversation.objects.create(
            question=message,
            answer=answer
        )

    conversations = Conversation.objects.all().order_by("-id")

    return render(
        request,
        "index.html",
        {
            "conversations": conversations
        }
    )