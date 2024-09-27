from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User, Question, GameSession
from .serializers import UserSerializer, QuestionSerializer, GameSessionSerializer
from .permissions import IsAdminOrTeacher, IsStudent
from rest_framework import permissions

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Default authentication, customize as needed


# Question ViewSet
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        """
        Set permissions based on user roles.
        - Admins have read-only access (safe methods).
        - Teachers have full access.
        - Students have read-only access (safe methods).
        """
        if self.request.user.role == 'admin' or self.request.user.role == 'teacher':
            permission_classes = [IsAdminOrTeacher]
        elif self.request.user.role == 'student':
            permission_classes = [IsStudent]
        else:
            permission_classes = [IsAuthenticated]  # Default permission for other roles
        return [permission() for permission in permission_classes]


# Game Session ViewSet
class GameSessionViewSet(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer

    def get_permissions(self):
        """
        Apply custom permissions for accessing game sessions.
        """
        if self.request.user.role == 'admin' or self.request.user.role == 'teacher':
            permission_classes = [IsAdminOrTeacher]
        elif self.request.user.role == 'student':
            permission_classes = [IsStudent]
        else:
            permission_classes = [IsAuthenticated]  # Default permission for other roles
        return [permission() for permission in permission_classes]
