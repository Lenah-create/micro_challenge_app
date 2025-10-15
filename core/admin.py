from django.contrib import admin
from .models import Challenge, Reminder, EmotionLog, Progress

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'remind_time', 'active')
    list_filter = ('active',)

@admin.register(EmotionLog)
class EmotionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'emotion_type', 'intensity', 'created_at')
    list_filter = ('emotion_type',)

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'date', 'completed')
    list_filter = ('completed',)
