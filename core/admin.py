from django.contrib import admin
from .models import Challenge, Reminder, EmotionLog, Progress

# ---------------- Challenge ----------------
@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'start_date', 'end_date', 'duration_seconds']
    search_fields = ('title', 'description')

    def duration_seconds(self, obj):
        if obj.start_date and obj.end_date:
            delta = obj.end_date - obj.start_date
            return delta.days * 24 * 3600  # convert days to seconds
        return "-"
    duration_seconds.short_description = 'Duration (seconds)'

# ---------------- Reminder ----------------
@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'remind_time', 'active')
    list_filter = ('active',)

# ---------------- EmotionLog ----------------
@admin.register(EmotionLog)
class EmotionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'emotion_type', 'intensity', 'created_at')
    search_fields = ('emotion_type', 'note')

# ---------------- Progress ----------------
@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'date', 'completed')
    list_filter = ('completed', 'date')
