from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import User, Question, GameSession, Quiz, QuizResult, ProgressTracking, Leaderboard
from .permissions import IsAdminOrTeacher, IsStudent
from .serializers import (
    UserSerializer, QuestionSerializer, GameSessionSerializer, 
    QuizSerializer, QuizResultSerializer, ProgressTrackingSerializer, LeaderboardSerializer
)

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Set permissions based on user roles:
        - admin: full access and can perform CRUD operations
        - teacher: can only view the list of users with role 'student'
        - student: no access
        """
        permission_classes = [IsAuthenticated]  # Default authentication - We add new classes as we need 
        if self.request.user.is_authenticated:
            # Ensure the user has a role attribute
            role = getattr(self.request.user, 'role', None)
            if role == 'admin':
                permission_classes = [IsAuthenticated]
            elif role == 'teacher':
                permission_classes = [IsAuthenticated]
            else:
                 permission_classes = [permissions.IsAuthenticated]  
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        filter the query based on the user's role:
        - Admin can see all users.
        - Teacher can only see users with role 'student'.
        - Students should not be able to see any other users.
        """
        queryset = super().get_queryset()

        role = getattr(self.request.user, 'role', None)

        if role == 'admin':
            return queryset  # Admins see all users
        elif role == 'teacher':
            return queryset.filter(role='student')  # Teachers can only see students
        else:
            return queryset.none()  # Students (or others) cannot access this view

    def perform_create(self, serializer):
        """
        Only admin users can create new users.
        """
        if getattr(self.request.user, 'role', None) != 'admin':
            raise PermissionDenied("Only admin can create users.")
        
        # Save the new user with the data provided
        serializer.save()


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
        permission_classes = [IsAuthenticated]
        if self.request.user.is_authenticated:
             # Ensure the user has a role attribute
            role = getattr(self.request.user, 'role', None)

            if role == 'admin' or role == 'teacher':
                permission_classes = [IsAdminOrTeacher]
            elif role == 'student':
                permission_classes = [IsStudent]

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

# Quiz ViewSet
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_permissions(self):
        """
        Set permissions based on user roles.
        - Only authenticated users can access the view.
        - Only teachers can create quizzes.
        """
        permission_classes = [IsAuthenticated]
        if self.request.user.is_authenticated:
            role = getattr(self.request.user, 'role', None)
            if role == 'teacher':
                permission_classes = [IsAdminOrTeacher]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Ensure that the user creating the quiz is a teacher
        if getattr(self.request.user, 'role', None) != 'teacher':
            raise PermissionDenied("Only teachers can create quizzes.")
        
        # Automatically assign the currently authenticated user as the teacher
        serializer.save(teacher=self.request.user)

# Quiz Result ViewSet
class QuizResultViewSet(viewsets.ModelViewSet):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer

# Progress Tracking ViewSet
class ProgressTrackingViewSet(viewsets.ModelViewSet):
    queryset = ProgressTracking.objects.all()
    serializer_class = ProgressTrackingSerializer

# Leaderboard ViewSet
class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer