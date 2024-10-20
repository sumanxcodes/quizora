
from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to only allow users with the 'teacher' role to access certain views.
    """
    message = "You must be a teacher to access this resource."
    def has_permission(self, request, view):
        # Ensure that the user is authenticated and has the role 'teacher'
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsAdminOrTeacher(permissions.BasePermission):
    """
    Custom permission to allow:
    - Admin (school admin) to view questions (read-only)
    - Teachers to fully manage questions (create, update, delete)
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                # Allow admin to view but not modify
                if request.method in permissions.SAFE_METHODS:
                    return True
            if request.user.role == 'teacher':
                # Teachers can view and modify
                return True
        return False
    
class IsStudent(permissions.BasePermission):
    """
    Custom permission to allow students to only access questions
    in a quiz or test context (read-only).
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'student':
            # Allow read-only, POST, and PUT methods for students
            if request.method in permissions.SAFE_METHODS or request.method in ['POST', 'PUT', 'PATCH']:
                return True
        return False