from django.db import models
from django.contrib.auth.models import User

# Extend the User model with a profile
class UserProfile(models.Model):
    USER_ROLES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('parent', 'Parent'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES)

# Course model
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")

# Assignment model
class Assignment(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

# Question model for MCQs
class Question(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=1)  # A, B, C, or D

# Enrollment model to track student enrollments
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_assignments = models.ManyToManyField(Assignment, blank=True)
