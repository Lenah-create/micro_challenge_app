from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Challenge, Reminder, EmotionLog, Progress
from .serializers import (
    ChallengeSerializer,
    ReminderSerializer,
    EmotionLogSerializer,
    ProgressSerializer
)


# --- CHALLENGE VIEWSET ---
class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all().order_by('-created_at')
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the creator
        serializer.save(created_by=self.request.user)


# --- REMINDER VIEWSET ---
class ReminderViewSet(viewsets.ModelViewSet):
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only reminders belonging to the logged-in user
        return Reminder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- EMOTION LOG VIEWSET ---
class EmotionLogViewSet(viewsets.ModelViewSet):
    serializer_class = EmotionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only emotions logged by the current user
        return EmotionLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- PROGRESS VIEWSET ---
class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return progress entries belonging to the logged-in user
        return Progress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Custom endpoint to view completed challenges"""
        completed_entries = Progress.objects.filter(user=request.user, completed=True)
        serializer = self.get_serializer(completed_entries, many=True)
        return Response(serializer.data)
