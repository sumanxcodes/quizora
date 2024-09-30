from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Import your custom User model

class CustomUserAdmin(UserAdmin):
    # Define which fields will be displayed in the admin
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info',{'fields':('first_name','last_name', 'role', 'class_year')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Make 'class_year' read-only if not a student
        """
        if obj and obj.role != 'student':
            return self.readonly_fields + ('class_year',) 
        return self.readonly_fields

    def get_fields(self, request, obj=None):
        """
        Dynamically hide class_year for non-students.
        """
        fields = super().get_fields(request, obj)
        if obj and obj.role != 'student':
            fields.remove('class_year') 
        return fields
    
    search_fields = ('username', 'email')
    ordering = ('username',)

# Register the custom User model with the custom UserAdmin
admin.site.register(User, CustomUserAdmin)

