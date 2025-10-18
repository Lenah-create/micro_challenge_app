from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Challenge, Reminder, EmotionLog, Progress

# --- USER SERIALIZER ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# --- CHALLENGE SERIALIZER ---
class ChallengeSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # nested user data

    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'duration_seconds', 'created_by', 'created_at']

# --- REMINDER SERIALIZER ---
class ReminderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    challenge = serializers.PrimaryKeyRelatedField(queryset=Challenge.objects.all())

    class Meta:
        model = Reminder
        fields = ['id', 'user', 'challenge', 'remind_time', 'active', 'created_at']

# --- EMOTION LOG SERIALIZER ---
class EmotionLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    related_challenge = serializers.PrimaryKeyRelatedField(queryset=Challenge.objects.all(), allow_null=True)

    class Meta:
        model = EmotionLog
        fields = ['id', 'user', 'emotion_type', 'intensity', 'note', 'related_challenge', 'created_at']

# --- PROGRESS SERIALIZER ---
class ProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    challenge = serializers.PrimaryKeyRelatedField(queryset=Challenge.objects.all())

    class Meta:
        model = Progress
        fields = ['id', 'user', 'challenge', 'date', 'completed', 'created_at']
