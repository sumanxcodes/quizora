'''
This file contains serialisers code which converts Django models to JSON format 
and vice-versa.
'''
from rest_framework import serializers
from .models import User, Quiz, Question, QuestionOption, GameSession, QuizResult, ProgressTracking, Leaderboard

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'email']

# Quiz Serializer
class QuizSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()  # Display the teacher username

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'teacher', 'created_at', 'updated_at']

# Question Serializer
class QuestionSerializer(serializers.ModelSerializer):
    # setting quiz by ID so that it can be passed during question creation.
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())  
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'question_text', 'question_type', 'correct_answer', 'points', 'created_at', 'updated_at']

# Question Option Serializer
class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'question', 'option_text', 'is_correct', 'created_at', 'updated_at']

# Game Session Serializer
class GameSessionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the user's username

    class Meta:
        model = GameSession
        fields = ['id', 'user', 'score', 'date_played']

# Quiz Result Serializer
class QuizResultSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # Display the student's username
    quiz = serializers.StringRelatedField()     # Display the quiz title

    class Meta:
        model = QuizResult
        fields = ['id', 'student', 'quiz', 'score', 'feedback', 'completed_at', 'updated_at']

# Progress Tracking Serializer
class ProgressTrackingSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # Display the student's username
    quiz = serializers.StringRelatedField()     # Display the quiz title

    class Meta:
        model = ProgressTracking
        fields = ['id', 'student', 'quiz', 'status', 'score', 'started_at', 'completed_at']

# Leaderboard Serializer
class LeaderboardSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # Display the student's username
    quiz = serializers.StringRelatedField()     # Display the quiz title

    class Meta:
        model = Leaderboard
        fields = ['id', 'student', 'quiz', 'ranking', 'total_score']


