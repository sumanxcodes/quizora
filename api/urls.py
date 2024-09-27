from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, QuestionViewSet, QuestionOptionViewSet, GameSessionViewSet, QuizViewSet, 
    QuizResultViewSet, ProgressTrackingViewSet, LeaderboardViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()

# Register the viewsets to specific endpoints
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'questionoptions', QuestionOptionViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'quizresults', QuizResultViewSet)
router.register(r'gamesessions', GameSessionViewSet)
router.register(r'progresstracking', ProgressTrackingViewSet)
router.register(r'leaderboard', LeaderboardViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),  # Include all routes from the router
]
