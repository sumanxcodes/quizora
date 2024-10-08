from django.urls import path, include
from .views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, QuestionViewSet, GameSessionViewSet, QuizViewSet, 
    QuizResultViewSet, ProgressTrackingViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()

# Register the viewsets to specific endpoints
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'gamesessions', GameSessionViewSet)
router.register(r'quizresults', QuizResultViewSet)
router.register(r'progresstracking', ProgressTrackingViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),  # Include all routes from the router
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
