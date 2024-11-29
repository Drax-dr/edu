from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
import uuid
from django.utils.translation import gettext_lazy as _
import json

# Constants
GRADE_CHOICES = [
    (8, 'EIGHT'),
    (9, 'NINTH'),
    (10, 'TENTH'),
    (11, 'INTERMEDIATE 1'),
    (12, 'INTERMEDIATE 2'),
]

INTERESTS_CHOICES = [
    ('math', 'Mathematics'),
    ('science', 'Science'),
    ('computer_science', 'Computer Science'),
    ('literature', 'Literature'),
    ('art', 'Art'),
]

APTITUDE_CHOICES = [
    ('logical', 'Logical Reasoning'),
    ('technical', 'Technical Skills'),
    ('artistic', 'Artistic Aptitude'),
    ('problem_solving', 'Problem Solving'),
]


class UserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, fullname, password, **extra_fields)
    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
            )
            queryset = queryset.filter(
                or_lookup
            ).distinct()
        return queryset

    def get_student_count(self):
        return self.model.objects.filter(is_student=True).count()

    def get_lecturer_count(self):
        return self.model.objects.filter(is_lecturer=True).count()

    def get_superuser_count(self):
        return self.model.objects.filter(is_superuser=True).count()


GENDERS = ((_("M"), _("Male")), (_("F"), _("Female")))



class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    )
    # profile = models.FilePathField(null=True, blank=True)
    email = models.EmailField(unique=True)
    # registerd_id = models.CharField(unique=True, primary_key=True,max_length=10, default= (lambda : str(uuid.uuid4()))())
    fullname = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'user_type']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set', 
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions',
        blank=True
    )

    def __str__(self):
        return f"{self.fullname} ({self.email})"



class Interest(models.Model):
    name = models.CharField(max_length=100, choices=INTERESTS_CHOICES)

    def __str__(self):
        return self.name


class Aptitude(models.Model):
    name = models.CharField(max_length=100, choices=APTITUDE_CHOICES)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    student_id = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=15)
    parent_contact = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to="users/images", blank=True, null=True)
    grade = models.IntegerField(choices=GRADE_CHOICES, default=8)
    interests = models.ManyToManyField(Interest, blank=True)
    aptitudes = models.ManyToManyField(Aptitude, blank=True)
    courses_enrolled = models.ManyToManyField('course.Course', blank=True)
    assignment_completed = models.ManyToManyField('assignments.CompletedAssignment', blank=True)
    # courses_enrolled = models.ManyToManyField('course.Course',blank=True,null=True)
    # assignment_completed = models.ManyToManyField('assignments.CompletedAssignment', blank=True, null=True)
    insights = models.JSONField(default="", blank=True, null=True)

    def __str__(self):
        return f"{self.user.fullname} (Student)"
    
    def add_insight(self, action):
        insight = {
            'action': action,
            'timestamp': self.get_current_timestamp(),
        }
        self.insights.append(insight)
        self.save()

    def get_current_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

class LecturerProfile(models.Model):
    DEPARTMENT_CHOICES = (
        ("CSE", "Computer Science and Engineering"),
        ("ECE", "Electrical and Computer Engineering"),
        ("MECH", "Mechanical Engineering"),
        ("EEE", "Electrical And Electronical Engineering"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="lecturer_profile")
    lecturer_id = models.CharField(max_length=15, unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default="CSE")
    profile_pic = models.ImageField(upload_to="users/images", blank=True, null=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.fullname} (Lecturer)"


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="parent_profile")
    phone_number = models.CharField(max_length=15)
    students = models.ManyToManyField(StudentProfile, related_name="parents")

    def __str__(self):
        return f"{self.user.fullname} (Parent)"
