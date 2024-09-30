from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

'''
User model class that defines
'''
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

     # Add unique related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(Group, related_name='api_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='api_user_permissions', blank=True)

    def __str__(self):
        return self.username
    

'''
Quiz model
'''
class Quiz(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


'''
    Model Quiestion    
'''
class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('multiple_choice', 'Multiple Choice'),
        ('drag_and_drop', 'Drag and Drop'),
        ('fill_in_the_blank', 'Fill in the Blank'),
        ('matching_pairs', 'Matching Pairs'),
     )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES)

    # Insted of creating a separate model for answer, for simplicity a JSON filed is used to store the options
    # and correct answers
    options = models.JSONField(null=True, blank=True)
    # Stored answer only for non multiple choice question type
    correct_answer = models.JSONField() 
    points = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text
    
    
'''
Game Session
'''
class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_played = models.DateTimeField(auto_now_add=True)

'''
QuizResult
'''
class QuizResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.username} - {self.quiz.title}'

'''
Progress tracking
'''
class ProgressTracking(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='in_progress')
    score = models.IntegerField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.student.username} - {self.quiz.title} - {self.status}'

'''
Leader Board
'''
class Leaderboard(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    ranking = models.IntegerField()
    total_score = models.IntegerField()

    def __str__(self):
        return f'{self.student.username} - {self.quiz.title} - Rank: {self.ranking}'
