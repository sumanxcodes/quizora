from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, QuestionViewSet, GameSessionViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()

# Register the viewsets to specific endpoints
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'gamesessions', GameSessionViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),  # Include all routes from the router
]
