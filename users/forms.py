from django import forms
from django.contrib.auth import get_user_model
from .models import StudentProfile
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class StudentLoginForm(AuthenticationForm):
    studentID = forms.EmailField(label="Student ID", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ParentRegisterForm(AuthenticationForm):
    studentID = forms.EmailField(label="Student ID", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class StudentRegisterForm(forms.ModelForm):
    fullname = forms.CharField(label="Full name",  widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    studentID = forms.CharField(label="Student ID", widget=forms.TextInput(attrs={'class': 'form-control'}))
    intrestes = forms.CharField(label="Intrests", widget=forms.TextInput(attrs={'class': 'form-control'})) 
    aptitdue = forms.CharField(label="Aptitude", widget=forms.TextInput(attrs={'class': 'form-control'}))
    grade = forms.IntegerField(label="Grade", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    phoneNumber = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={'class': 'form-control'}))
    parentNumber = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={'class': 'form-control'}))


    def clean_studentID(self):
        studentID = self.cleaned_data.get('studentID')
        if User.objects.filter(studentID=studentID).exists():
            raise forms.ValidationError("A student with that ID already exists.")
        return studentID

    def clean_phoneNumber(self):
        phoneNumber = self.cleaned_data.get('phoneNumber')
        if User.objects.filter(phoneNumber=phoneNumber).exists():
            raise forms.ValidationError("A student with that phone number already exists.")
        return phoneNumber

    class Meta:
        model = User
        fields = ['email', 'password', 'phoneNumber']

    def save(self, commit=True):
        user = super().save(commit=True)
        user.user_type = 'student'
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            StudentProfile.objects.create(user=user, student_id=self.cleaned_data['student_id'], grade=self.cleaned_data['grade'])

        return user



class LecturerLoginForm(AuthenticationForm):
    id = forms.EmailField(label="ID", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class LecturerRegisterForm(forms.ModelForm):
    DEPT_CHOICES = (
        ("CSE", "Computer Science and Engineering"),
        ("ECE", "Electrical and Computer Engineering"),
        ("EEE", "Electrical and Electronic Engineering"),
        ("MECH", "Mechanical Engineering"),
    )

    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    ID = forms.CharField(label="ID", widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.CharField(label="Department", widget=forms.ChoiceField(choices=DEPT_CHOICES))
    phoneNumber = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_ID(self):
        studentID = self.cleaned_data.get('ID')
        if User.objects.filter(studentID=ID).exists():
            raise forms.ValidationError("A Lecturer with that ID already exists.")
        return ID

    def clean_phoneNumber(self):
        phoneNumber = self.cleaned_data.get('phoneNumber')
        if User.objects.filter(phoneNumber=phoneNumber).exists():
            raise forms.ValidationError("A student with that phone number already exists.")
        return phoneNumber

    class Meta:
        model = User
        fields = ['email','password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'teacher'
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            StudentProfile.objects.create(user=user, ID=self.cleaned_data['student_id'], grade=self.cleaned_data['grade'])

        return user
