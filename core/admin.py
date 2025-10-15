from django.contrib import admin
from .models import Challenge, Reminder, EmotionLog, Progress

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'duration_seconds', 'created_at')
    search_fields = ('title', 'description')
    def duration_seconds(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days * 24 * 3600
        return "-"
    duration_seconds.short_description = 'Duration (seconds)'

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'remind_time', 'active')
    list_filter = ('active',)

@admin.register(EmotionLog)
class EmotionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'emotion_type', 'intensity', 'created_at')
    search_fields = ('emotion_type', 'note')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'date', 'completed')
    list_filter = ('completed', 'date')
