from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User, Question, GameSession, Quiz, QuizResult, ProgressTracking
from .permissions import IsAdminOrTeacher, IsStudent
from .serializers import (
    UserSerializer, QuestionSerializer, GameSessionSerializer, 
    QuizSerializer, QuizResultSerializer, ProgressTrackingSerializer
)

# Login view
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Logout view
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

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
        else:
            return queryset.filter(role='student')  # Teachers can only see students

    def perform_create(self, serializer):
        """
        Only admin users can create new users.
        """
        if getattr(self.request.user, 'role', None) != 'admin':
            raise PermissionDenied("Only admin can create users.")
        
        # Save the new user with the data provided
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        """
        Only admin users can update users.
        """
        if getattr(self.request.user, 'role', None) != 'admin':
            raise PermissionDenied("Only admin can update users.")
        
        # Proceed with the update if the user is an admin
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Only admin users can delete users.
        """
        if getattr(self.request.user, 'role', None) != 'admin':
            raise PermissionDenied("Only admin can delete users.")
        
        # Proceed with the delete if the user is an admin
        return super().destroy(request, *args, **kwargs)

# View that gets logged in user
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve information for the authenticated user.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

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
     
    def get_queryset(self):
        """
        Filter the queryset based on the user's role.
        - Students can only view questions for their assigned  quizzes.
        - Teachers and admins can view all questions.
        """

        user = self.request.user
        quiz_id = self.request.query_params.get('quiz_id', None)

        # If the user is a student, filter questions by their class_year via related quizzes
        if user.is_authenticated and user.role == 'student':
            return self.queryset.filter(quiz__class_year=user.class_year, quiz_id=quiz_id)
        
        # If the user is a teacher or admin, return all questions
        return self.queryset
    
    def perform_create(self, serializer):
        if self.request.user.role != 'teacher':
            raise PermissionDenied("Only teachers can create game questions.")
        serializer.save(teacher=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Only teachers can update questions.
        """
        print("=========")
        print(self.get_object())
        question = self.get_object()  
        if request.user.role != 'teacher' or question.teacher != request.user:
            raise PermissionDenied("Only the teacher who created this question can update it.")
        
        return super().update(request, *args, **kwargs)


# Game Session ViewSet
class GameSessionViewSet(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer

    def get_permissions(self):
        """
        Apply custom permissions for accessing game sessions for students onyl..
        """
        permission_classes = [IsAuthenticated] 
        if self.request.user.is_authenticated:
            if self.request.user.role == 'student':
                permission_classes = [IsStudent]
            else:
                raise PermissionDenied("Game sessions are only associated with student account.")
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Restrict game session viewing to only the current student.
        """
        if self.request.user.role == 'student':
            return GameSession.objects.filter(student=self.request.user)  # Return only the student's game sessions
        return GameSession.objects.none()  
    
    def perform_create(self, serializer):
        if self.request.user.role != 'student':
            raise PermissionDenied("Only students can create game sessions.")
        # Assign the authenticated student as the user in the GameSession
        serializer.save(student=self.request.user)
    
    def perform_update(self, serializer):
        """
        Allow only the student who created the game session to update it.
        """
        game_session = self.get_object()

        # Ensure only the student who created the game session can update it
        if game_session.student != self.request.user:
            raise PermissionDenied("You do not have permission to update this game session.")
        
        # Proceed with the update if permission checks are satisfied
        serializer.save()
    

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
    
    def get_queryset(self):
        """
        Filter the queryset based on the user's role.
        - Students can only view quizzes for their assigned class_year.
        - Teachers and admins can view all quizzes.
        """
        user = self.request.user

        # If the user is a student, filter quizzes by their class_year
        if user.is_authenticated and user.role == 'student':
            return self.queryset.filter(class_year=user.class_year)
        
        # If the user is a teacher or admin, return all quizzes
        return self.queryset

    def perform_create(self, serializer):
        # Ensure that the user creating the quiz is a teacher
        if getattr(self.request.user, 'role', None) != 'teacher':
            raise PermissionDenied("Only teachers can create quizzes.")
        
        # Automatically assign the currently authenticated user as the teacher
        serializer.save(teacher=self.request.user)
    def perform_update(self, serializer):
        """
        Only teachers can edit their own quizzes.
        Admins can edit any quiz.
        """
        quiz = self.get_object()

        # Ensure that the user is a teacher and the quiz belongs to them, or they're an admin
        if getattr(self.request.user, 'role', None) == 'teacher':
            if quiz.teacher != self.request.user:
                raise PermissionDenied("You can only edit quizzes that you created.")
        
        if getattr(self.request.user, 'role', None) != 'admin' and quiz.teacher != self.request.user:
            raise PermissionDenied("You can only edit your own quizzes or you need to be an admin.")
        
        # Proceed with the update if the permissions are satisfied
        serializer.save()

    def perform_destroy(self, instance):
        """
        Only teachers can delete their own quizzes.
        Admins can delete any quiz.
        """
        quiz = self.get_object()

        # Ensure that the user is a teacher and the quiz belongs to them, or they're an admin
        if getattr(self.request.user, 'role', None) == 'teacher':
            if quiz.teacher != self.request.user:
                raise PermissionDenied("You can only delete quizzes that you created.")
        
        if getattr(self.request.user, 'role', None) != 'admin' and quiz.teacher != self.request.user:
            raise PermissionDenied("You can only delete your own quizzes or you need to be an admin.")
        
        # Proceed with the delete if the permissions are satisfied
        instance.delete()

# Quiz Result ViewSet
class QuizResultViewSet(viewsets.ModelViewSet):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return quiz results based on user role:
        - Admin and Teacher: Can view all quiz results.
        - Student: Can view quiz results of students within the same class_year.
        """
        user = self.request.user

        # If the user is an admin or teacher, return all quiz results
        if user.role in ['admin', 'teacher']:
            return QuizResult.objects.all()
        
        # If the user is a student, return only quiz results of students in the same class_year
        elif user.role == 'student':
            class_year = user.class_year  # Assuming `class_year` is an attribute of the User model
            return QuizResult.objects.filter(student__class_year=class_year)
        
        # If the user has an unrecognized role, deny access
        raise PermissionDenied("You do not have permission to view this data.")
    
    def create(self, request, *args, **kwargs):
        """
        Override quiz result if student with same quiz entries existss.
        """
        student = request.data.get("student")
        quiz = request.data.get("quiz")

        # Check if a QuizResult entry already exists
        quiz_result = QuizResult.objects.filter(student=student, quiz=quiz).first()
        
        if quiz_result:
            # If it exists, update the score and feedback instead of creating a new one
            serializer = self.get_serializer(quiz_result, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Otherwise, proceed with creating a new entry
        return super().create(request, *args, **kwargs)
    
# Progress Tracking ViewSet
class ProgressTrackingViewSet(viewsets.ModelViewSet):
    queryset = ProgressTracking.objects.all()
    serializer_class = ProgressTrackingSerializer
    def get_queryset(self):
        # Get the current user
        user = self.request.user

        # If the user is a student return only their progress tracking
        if user.role == 'student':
            return ProgressTracking.objects.filter(student=user)
        
        # If the user is a teacher or admin, return all progress tracking records
        if user.role in ['teacher', 'admin']:
            return ProgressTracking.objects.all()

        # Otherwise, deny access
        raise PermissionDenied("You do not have permission to view this data.")