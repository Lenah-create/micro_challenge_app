from django.core.checks import messages
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import viewsets
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import ChallengeForm, ReminderForm
from .models import Challenge
from django.contrib.auth.models import User

from .models import Challenge, Reminder, EmotionLog, Progress
from .serializers import (
    ChallengeSerializer,
    ReminderSerializer,
    EmotionLogSerializer,
    ProgressSerializer,
    UserSerializer
)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# -----------------------------
# Challenge Form
# -----------------------------
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter challenge title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your challenge'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and start > end:
            raise forms.ValidationError("End date cannot be before start date.")
        return cleaned_data


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

def perform_create(self, serializer):
    serializer.save(created_by=self.request.user)
    
# -----------------------------
# Dashboard
# -----------------------------
@login_required
def dashboard(request):
    user = request.user
    challenges = Challenge.objects.filter(created_by=user)
    progress = Progress.objects.filter(user=user)
    emotions = EmotionLog.objects.filter(user=user).order_by('-created_at')
    reminders = Reminder.objects.filter(user=user, active=True)
    form = ReminderForm()

    # Calculate challenge completion
    completed_days = progress.filter(completed=True).count()
    total_days = 7  # assuming a 7-day challenge
    completion_percentage = (completed_days / total_days) * 100 if total_days > 0 else 0

    # Handle reminder form submission
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = user
            reminder.save()
            return redirect("dashboard")

    context = {
        "challenges": challenges,
        "progress": progress,
        "emotions": emotions,
        "reminders": reminders,
        "completion_percentage": completion_percentage,
        "form": form,
    }

    return render(request, "core/dashboard.html", context)

# -----------------------------
# Add Challenge Form (Frontend)
# -----------------------------
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
    return render(request, 'core/create_challenge.html', {'form': form})

@login_required
def set_reminder(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)

    if request.method == "POST":
        remind_time = request.POST.get("remind_time")
        print("DEBUG remind_time:", remind_time)
        if not remind_time:
            messages.error(request, "Please select a reminder time.")
            return redirect("dashboard")

        Reminder.objects.create(
            user=request.user,
            challenge=challenge,
            remind_time=remind_time
        )

        messages.success(request, "Reminder set successfully!")
        return redirect("dashboard")

    return redirect("dashboard")


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
            # Show why it failed
            print(form.errors)
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


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def set_reminder(request, challenge_id):
    if request.method == 'POST':
        remind_time = request.POST.get('remind_time')
        challenge = get_object_or_404(Challenge, id=challenge_id)
        Reminder.objects.create(
            user=request.user,
            challenge=challenge,
            remind_time=remind_time
        )
    return redirect('dashboard')