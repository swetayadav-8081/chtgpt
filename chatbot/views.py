
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import ChatMessage
from .forms import SignUpForm
import uuid

# Signup view
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "chatbot/signup.html", {"form": form})

# Home view with new chat and previous chats
@login_required
def home(request, chat_id=None):
    if chat_id is None:
        chat_id = str(uuid.uuid4())  # new chat id

    # Messages of current chat and user
    messages = ChatMessage.objects.filter(user=request.user, chat_id=chat_id).order_by("created_at")

    # Previous chats of user
    previous_chats = ChatMessage.objects.filter(user=request.user).values_list('chat_id', flat=True).distinct()

    if request.method == "POST":
        user_input = request.POST.get("message")
        if user_input:
            bot_reply = f"You said: {user_input}"
            ChatMessage.objects.create(
                user=request.user,
                
                chat_id=chat_id,
                input_text=user_input,
                output_text=bot_reply
            )
        return redirect("home", chat_id=chat_id)

    return render(request, "chatbot/home.html", {
        "messages": messages,
        "chat_id": chat_id,
        "previous_chats": previous_chats
    })

# Logout view
@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')
