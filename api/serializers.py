'''
This file contains serialisers code which converts Django models to JSON format 
and vice-versa.
'''
from rest_framework import serializers
from .models import User, Quiz, Question, GameSession, QuizResult, ProgressTracking

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'email', 'first_name', 'last_name', 'class_year']

# Quiz Serializer
class QuizSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()  # Display the teacher username

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'class_year', 'teacher', 'created_at', 'updated_at']

# Question Serializer
class QuestionSerializer(serializers.ModelSerializer):
    # setting quiz by ID so that it can be passed during question creation.
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())  
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'question_text', 'question_type', 'options', 'correct_answer', 'points', 'created_at', 'updated_at']

    # def to_representation(self, instance):
    #     """
    #     Custom representation to hide the 'correct_answer' field for students.
    #     """
    #     representation = super().to_representation(instance)
    #     request = self.context.get('request')
        
    #     return representation

# Game Session Serializer
class GameSessionSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # Display the user's username

    class Meta:
        model = GameSession
        fields = ['id', 'student', 'quiz', 'duration', 'status', 'score', 'correct_answers_count', 'date_played', 'last_updated']


# Quiz Result Serializer
class QuizResultSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())  

    class Meta:
        model = QuizResult
        fields = ['id', 'student', 'quiz', 'score', 'feedback', 'completed_at', 'updated_at']
        extra_kwargs = {
            'student': {'required': True},
            'quiz': {'required': True},
        }

# Progress Tracking Serializer
class ProgressTrackingSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # Display the student's username
    quiz = serializers.StringRelatedField()     # Display the quiz title

    class Meta:
        model = ProgressTracking
        fields = ['id', 'student', 'quiz', 'status', 'score', 'started_at', 'completed_at']
