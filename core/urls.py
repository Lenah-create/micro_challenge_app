from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'challenges', views.ChallengeViewSet)
router.register(r'reminders', views.ReminderViewSet)
router.register(r'emotions', views.EmotionLogViewSet)
router.register(r'progress', views.ProgressViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard and frontend pages
    path('', views.dashboard, name='dashboard'),  # root goes to dashboard
    path('challenges/', views.challenge_list, name='challenge_list'),
    path('emotions/', views.emotion_log, name='emotion_log'),
    path('reminders/', views.reminder_list, name='reminder_list'),
    path('progress/', views.progress_view, name='progress_view'),
    path('create/', views.create_challenge, name='create_challenge'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # API
    path('api/', include(router.urls)),
]
