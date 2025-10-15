from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django import forms

from .models import Challenge, Reminder, EmotionLog, Progress
from .serializers import (
    ChallengeSerializer,
    ReminderSerializer,
    EmotionLogSerializer,
    ProgressSerializer,
)

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        
        fields = ['title', 'description']  


# -----------------------------
# API ViewSets
# -----------------------------
class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer


class EmotionLogViewSet(viewsets.ModelViewSet):
    queryset = EmotionLog.objects.all()
    serializer_class = EmotionLogSerializer


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer


# -----------------------------
# Frontend Views (HTML Templates)
# -----------------------------
def home(request):
    return render(request, 'core/home.html')


def challenge_list(request):
    challenges = Challenge.objects.all()
    return render(request, 'core/challenges.html', {'challenges': challenges})


def emotion_log(request):
    emotions = EmotionLog.objects.all()
    return render(request, 'core/emotions.html', {'emotions': emotions})


def reminder_list(request):
    reminders = Reminder.objects.all()
    return render(request, 'core/reminders.html', {'reminders': reminders})


def progress_view(request):
    progress = Progress.objects.all()
    return render(request, 'core/progress.html', {'progress': progress})


# -----------------------------
# Dashboard + Challenge Creation
# -----------------------------
@login_required
def dashboard(request):
    user = request.user
    challenges = Challenge.objects.filter(created_by=request.user)
    progress = Progress.objects.filter(user=user)
    emotions = EmotionLog.objects.filter(user=user).order_by('-timestamp')
    reminders = Reminder.objects.filter(user=user, active=True)
    return render(request, 'core/dashboard.html', {'challenges': challenges})

    completed_days = progress.filter(completed=True).count()
    total_days = 7  # fixed for your 7-day challenge
    completion_percentage = (completed_days / total_days) * 100 if total_days > 0 else 0

    context = {
        "challenges": challenges,
        "progress": progress,
        "emotions": emotions,
        "reminders": reminders,
        "completion_percentage": completion_percentage,
    }
    return render(request, "core/dashboard.html", context)


# -----------------------------
# Add Challenge Form (Frontend)
# -----------------------------
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'start_date', 'end_date']


@login_required
def create_challenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.created_by = request.user
            challenge.save()
            return redirect('dashboard')
    else:
        form = ChallengeForm()
    return render(request, 'core/add_challenge.html', {'form': form})


# -----------------------------
# User Authentication
# -----------------------------
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
