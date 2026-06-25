from django.shortcuts import render,redirect

from .engine import generate_answer
from .models import *

from django.shortcuts import get_object_or_404

def chatbot(request):

    answer = ""

    if request.method == "POST":

        question = request.POST.get("question")

        answer = generate_answer(question)

    return render(
        request,
        "index.html",
        {
            "answer": answer
        }
    )


def KnowledgeView(request):
    knowledge_list = Knowledge.objects.all().order_by("-id")
    message = ""

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        Knowledge.objects.create(
            title=title,
            content=content
        )

        message = "Knowledge added successfully."

    return render(
        request,
        "knowledge.html",
        {
            "message": message,
            "knowledge_list": knowledge_list
        }
    )

def EditKnowledge(request, id):

    knowledge = get_object_or_404(
        Knowledge,
        id=id
    )

    if request.method == "POST":

        knowledge.title = request.POST.get("title")
        knowledge.content = request.POST.get("content")

        knowledge.save()

    return redirect("knowledge")


def DeleteKnowledge(request, id):

    knowledge = get_object_or_404(Knowledge, id=id)

    knowledge.delete()

    return redirect("knowledge")

