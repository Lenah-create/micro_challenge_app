from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

User = settings.AUTH_USER_MODEL  # Django's built-in user model


class Challenge(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Reminder(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reminders'
    )
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, related_name='reminders'
    )
    remind_time = models.TimeField()  # user-chosen time of day (HH:MM:SS)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.challenge.title} at {self.remind_time}"


class EmotionLog(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='emotion_logs'
    )
    emotion_type = models.CharField(max_length=50)  # e.g., sad, anxious, tired
    intensity = models.PositiveSmallIntegerField(
        null=True, blank=True
    )  # 1..10
    note = models.TextField(blank=True)  # optional note
    related_challenge = models.ForeignKey(
        Challenge,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='emotion_logs',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emotion_type} ({self.intensity or '-'} / 10)"


class Progress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='progress_entries'
    )
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, related_name='progress_entries'
    )
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'challenge', 'date')  # one record per user/challenge/day

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"{self.challenge.title} - {status} ({self.date})"
