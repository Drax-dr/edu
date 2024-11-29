from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
import uuid

# Constants
GRADE_CHOICES = [
    (8, 'EIGHT'),
    (9, 'NINTH'),
    (10, 'TENTH'),
    (11, 'INTERMEDIATE 1'),
    (12, 'INTERMEDIATE 2')
]

GRADE_SUBJECTS = [
    ('math', 'Mathematics'),
    ('english', 'English'),
    ('science', 'Science'),
    ('social_studies', 'Social Studies'),
    ('language', 'Language'),
    ('physical_education', 'Physical Education'),
]

INTERMEDIATE_SUBJECTS = [
    ('math', 'Mathematics'),
    ('physics', 'Physics'),
    ('chemistry', 'Chemistry'),
    ('biology', 'Biology'),
    ('computer_science', 'Computer Science'),
    ('english', 'English'),
    ('physical_education', 'Physical Education'),
]

COMPUTER_SCIENCE_TOPICS = [
    ('programming', 'Programming'),
    ('algorithms', 'Algorithms'),
    ('data_structures', 'Data Structures'),
    ('networking', 'Networking'),
    ('database', 'Database Systems'),
    ('web_development', 'Web Development'),
    ('artificial_intelligence', 'Artificial Intelligence'),
]

INTERESTS_CHOICES = GRADE_SUBJECTS + INTERMEDIATE_SUBJECTS + COMPUTER_SCIENCE_TOPICS

APTITUDE_CHOICES = [
    ('mathematical', 'Mathematical Aptitude'),
    ('logical', 'Logical Reasoning'),
    ('verbal', 'Verbal Aptitude'),
    ('artistic', 'Artistic Aptitude'),
    ('creative', 'Creative Thinking'),
    ('technical', 'Technical Skills'),
    ('analytical', 'Analytical Skills'),
    ('problem_solving', 'Problem Solving'),
]



class UserManager(BaseUserManager):
    def create_user(self, studentID, name, password=None, **extra_fields):
        if not studentID:
            raise ValueError('The Student ID is required')
        user = self.model(studentID=studentID, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, studentID, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(studentID, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    )
    fullname = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Avoids the clash with default auth.User groups
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users',  # Avoids clash with default auth.User user_permissions
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def __str__(self):
        return self.email

# Interest and Aptitude Models (for choices)
class InterestChoice(models.Model):
    choice = models.CharField(max_length=154, choices=INTERESTS_CHOICES, blank=True, null=True)

class AptitudeChoice(models.Model):
    choice = models.CharField(max_length=500, choices=APTITUDE_CHOICES, blank=True, null=True)

# Student Profile Model
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    studentID = models.CharField(max_length=10, unique=True)
    phoneNumber = models.CharField(max_length=10, unique=True)
    parentNumber = models.CharField(max_length=10)
    profilePic = models.ImageField(upload_to="users/assets/images")
    grade = models.IntegerField(default=8)
    aptitudes = models.ManyToManyField(AptitudeChoice)
    interests = models.ManyToManyField(InterestChoice)
    assignments_completed = models.ManyToManyField(
        'assignments.Assignment',
        through='assignments.CompletedAssignment',
        related_name='students'
    )

    def __str__(self):
        return self.user.email


# LecturerProfile Model
class LecturerProfile(models.Model):
    DEPT_CHOICES = (
        ("CSE", "Computer Science and Engineering"),
        ("ECE", "Electrical and Computer Engineering"),
        ("EEE", "Electrical and Electronic Engineering"),
        ("MECH", "Mechanical Engineering"),
    )

    lecturer_id = models.CharField(max_length=10, unique=True, default="")
    uid = models.CharField(max_length=30, default=str(uuid.uuid4())[:8])
    name = models.CharField(max_length=30, default="")
    phone_number = models.CharField(max_length=10, default="")
    profilePic = models.ImageField(default="")
    Department = models.CharField(max_length=41, choices=DEPT_CHOICES, default="CSE")

    def __str__(self):
        return self.name

# Parent Model
class Parent(models.Model):
    name = models.CharField(max_length=30)
    studentID = models.CharField(max_length=10, unique=True)
    phoneNumber = models.CharField(max_length=10, unique=True)
