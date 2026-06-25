from django.shortcuts import render,redirect

from .engine import generate_answer
from .models import *

from django.shortcuts import get_object_or_404

from django.views.decorators.cache import never_cache

from django.contrib.auth import authenticate, login


def admin_login(request):

    error = ""

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user and user.is_superuser:

            login(request, user)

            return redirect("knowledge")

        error = "Invalid admin credentials"

    return render(
        request,
        "adminlogin.html",
        {
            "error": error
        }
    )


@never_cache
def Register(request):

    error = ""
    success = ""

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username or not password or not confirm_password:
            error = "All fields are required."

        elif len(username) < 3:
            error = "Username must be at least 3 characters."

        elif len(password) < 8:
            error = "Password must be at least 8 characters."

        elif password != confirm_password:
            error = "Passwords do not match."

        elif Signup.objects.filter(username=username).exists():
            error = "Username already exists."

        else:
            Signup.objects.create(
                username=username,
                password=password
            )

            return redirect("login")

    return render(
        request,
        "login.html",
        {
            "error": error,
            "success": success
        }
    )


@never_cache
def user_login(request):

    error = ""

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:

            error = "Please enter username and password."

        else:

            user = Signup.objects.filter(
                username=username
            ).first()

            if user is None:

                error = "Username does not exist."

            elif user.password != password:

                error = "Incorrect password."

            else:

                request.session["user_id"] = user.id
                request.session["username"] = user.username

                return redirect("chatbot")

    return render(
        request,
        "login.html",
        {
            "error": error
        }
    )



# ── Bot Identity ───────────────────────────────────────────────
BOT_NAME = "Cipher"


# ── Prebuilt Responses ─────────────────────────────────────────
PREBUILT = {

    # Greetings
    "hi"                          : f"Hello! I'm {BOT_NAME}. How can I help you today?",
    "hello"                       : f"Hi there! I'm {BOT_NAME}. What would you like to know?",
    "hey"                         : f"Hey! {BOT_NAME} here. What can I help you with?",
    "good morning"                : f"Good morning! {BOT_NAME} here. How can I assist you today?",
    "good afternoon"              : f"Good afternoon! How can {BOT_NAME} help you today?",
    "good evening"                : f"Good evening! {BOT_NAME} is here to assist you.",
    "how are you"                 : f"I'm doing great, thank you for asking! I'm {BOT_NAME}. How can I help you?",
    "how are you doing"           : f"I'm doing well! {BOT_NAME} is ready to help. What do you need?",
    "what's up"                   : f"Not much! {BOT_NAME} is ready to answer your questions.",
    "bye"                         : f"Goodbye! {BOT_NAME} will be here whenever you need me.",
    "goodbye"                     : f"Goodbye! Have a great day! {BOT_NAME} signing off.",
    "thank you"                   : f"You're welcome! {BOT_NAME} is always happy to help.",
    "thanks"                      : f"Happy to help! Is there anything else {BOT_NAME} can do for you?",

    # FAQ
    "what can you do"             : f"I'm {BOT_NAME}! I can answer questions from the knowledge base, help you find information, and have a conversation with you using voice or text.",
    "what are you"                : f"I am {BOT_NAME}, an intelligent assistant designed to answer your questions from a custom knowledge base.",
    "who are you"                 : f"I am {BOT_NAME}, your personal knowledge base assistant. Ask me anything!",
    "who made you"                : f"I'm {BOT_NAME}, built using Django and powered by AI to help you get answers quickly.",
    "how do you work"             : f"I'm {BOT_NAME}! You can speak or type your question. I search the knowledge base and give you the best answer I can find.",
    "what is your name"           : f"My name is {BOT_NAME}. How can I help you today?",
    "what's your name"            : f"I'm {BOT_NAME}! Your personal AI assistant. What would you like to know?",
    "help"                        : f"Sure! I'm {BOT_NAME}. You can ask me any question by speaking or typing. I will search the knowledge base and answer you.",
    "what languages do you speak" : f"I currently support English. More languages may be added to {BOT_NAME} in the future.",
    "are you a robot"             : f"I am {BOT_NAME}, an AI assistant — so yes, kind of! But I'm here to help you just like a human would.",
    "can you help me"             : f"Of course! I'm {BOT_NAME}. What would you like to know? Just speak or type your question.",
    "tell me about yourself"      : f"I'm {BOT_NAME}, an AI-powered voice assistant built to answer your questions from a custom knowledge base. Just speak or type and I'll do my best to help!",
}


def get_prebuilt(question):
    """Check if question matches a prebuilt response (case insensitive)."""
    q = question.strip().lower()

    # Exact match first
    if q in PREBUILT:
        return PREBUILT[q]

    # Partial match — check if any key is contained in the question
    for key, response in PREBUILT.items():
        if key in q:
            return response

    return None




from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache



from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache


@never_cache
def chatbot(request):

    # Check Login
    if "user_id" not in request.session:
        return redirect("login")

    answer = ""

    if request.method == "POST":

        question = request.POST.get(
            "question",
            ""
        ).strip()

        if question:

            prebuilt = get_prebuilt(question)

            if prebuilt:
                answer = prebuilt
            else:
                answer = generate_answer(question)

    response = render(
        request,
        "index.html",
        {
            "answer": answer,
            "username": request.session.get("username")
        }
    )

    response["Cache-Control"] = (
        "no-cache, no-store, must-revalidate, max-age=0"
    )
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response


@never_cache
def logout(request):

    # Clear Session
    request.session.flush()

    response = redirect("login")

    response["Cache-Control"] = (
        "no-cache, no-store, must-revalidate, max-age=0"
    )
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response




from django.contrib.auth.decorators import user_passes_test

@never_cache
@user_passes_test(lambda u: u.is_superuser)
def KnowledgeView(request):

    knowledge_list = Knowledge.objects.all().order_by("-id")

    response = render(
        request,
        "knowledge.html",
        {
            "knowledge_list": knowledge_list
        }
    )

    response["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response


from django.contrib.auth.decorators import user_passes_test


@never_cache
@user_passes_test(lambda u: u.is_superuser)
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

from django.contrib.auth.decorators import user_passes_test


@never_cache
@user_passes_test(lambda u: u.is_superuser)
def DeleteKnowledge(request, id):

    knowledge = get_object_or_404(Knowledge, id=id)

    knowledge.delete()

    return redirect("knowledge")








@never_cache
def admin_logout(request):

    if request.method == "POST":
        logout(request)

    return redirect("admin_login")





