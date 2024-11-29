from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DeleteView, DetailView, CreateView, UpdateView,FormView
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import StudentLoginForm, StudentRegisterForm, ParentRegisterForm, LecturerRegisterForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from .models import User, StudentProfile, LecturerProfile
# from .forms import LoginForm, StudentRegistrationForm
#
User = get_user_model()


class HomeView(TemplateView):
    template_name = "home.html"

class RegisterView(TemplateView):
    template_name = 'register.html'

class _StudentRegisterView(TemplateView):
    template_name = 'student/register.html'

class LecturerRegisterView(TemplateView):
    template_name = 'register.html'

class StudentDasboardView(View):
    model = StudentProfile
    def get(slef,request):
        print(dir(User))
        print(User.is_authenticated)
        if not User.is_authenticated:
            return redirect("home")
            # print("not registerd")
        return render(request,"student/student-dashboard.html")

class LecturerDashboardView(TemplateView):
    model = LecturerProfile
    template_name = "lecturer/educator-dashboard.html"

class AdminProfileView:
    pass

class StudentLoginView(LoginView):
    template_name = 'student/login.html'
    form_class = StudentLoginForm

    def form_valid(self, form):
        user = form.get_user()
        if user.user_type == 'student':
            login(self.request, user)
            return redirect('student_dashboard')
        else:
            return redirect('student_dashboard')

class StudentRegisterView(View):
    def get(self, request):
        form = StudentRegisterForm()
        return render(request, 'student/register.html', {'form': form})

    def post(self, request):
        form = StudentRegisterForm(request.POST)
        print(form)
        if form.is_valid():
            print("Form is valid")
            form.save()
            return redirect('student_dashboard')
        else:
            print(form.errors)
        return render(request, 'student/register.html', {'form': form})

class ParentRegisterView(View):
    def get(self, request):
        form = ParentRegisterForm()
        return render(request, 'parent/parent-register.html', {'form': form})

    def post(self, request):
        form = StudentRegisterForm(request.POST)
        print(form)
        if form.is_valid():

            form.save()
            return redirect('student_dashboard')
        return render(request, 'parent/parent-register.html', {'form': form})

class LecturerRegisterView(FormView):
    template_name = "lecturer/register.html"
    form_class = LecturerRegisterForm
    success_url = reverse_lazy('lecturer_dashboard')

    def form_valid(self, form):
        # Extract form data
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        id = form.cleaned_data['ID']
        department = form.cleaned_data['department']
        phone_number = form.cleaned_data['phoneNumber']

        # Create the User object (you can customize this based on your User model)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            user_type="teacher"
        )
        user.first_name = id  # Or map it to your custom fields
        user.save()

        # Assuming you have a Lecturer model with additional fields
        Lecturer.objects.create(
            user=user,
            department=department,
            phone_number=phone_number
        )

        messages.success(self.request, "Lecturer registered successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error in the form. Please try again.")
        return super().form_invalid(form)

class _LecturerRegisterView(View):
    def get(self, request):
        form = LecturerRegisterForm()
        return render(request, 'lecturer/register.html', {'form': form})

    def post(self, request):
        form = LecturerRegisterForm(request.POST)
        print(form)
        if form.is_valid():

            form.save()
            return redirect('lecturer_dashboard')
        return render(request, 'lecturer/login.html', {'form': form})

def student_login(request):
    student_id = request.POST.get('studentId')
    password = request.POST.get('password')
    if not student_id:
        print("Student ID is missing.")
    user = authenticate(request, student_id=student_id, password=password)
    if user is not None and user.user_type == 'student':
        login(request, user)
        return HttpResponse("Student logged in successfully.")
    else:
        return redirect("user_dashboard")
    return render(request, "student/login.html")

def login_student(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            studentID = form.cleaned_data['studentID']
            password = form.cleaned_data['password']

            try:
                student = User.objects.get(studentID=studentID)
                if check_password(password, student.password):
                    login(request, student)
                    request.session['student_id'] = student.id  # Save student ID in session
                    messages.success(request, 'Login successful.')
                    return redirect('dashboard')  # Redirect to a student dashboard or home page
                else:
                    messages.error(request, 'Invalid password.')
            except StudentProfile.DoesNotExist:
                messages.error(request, 'Student ID not found.')
    else:
        form = LoginForm()

    return render(request, 'register.html', {'form': form})

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Student instance without saving to hash the password first
            student = form.save(commit=False)
            student.password = make_password(form.cleaned_data['password'])
            student.save()  # Save the hashed password instance to the database
            messages.success(request, 'Registration successful.')
            return redirect('login')  # Redirect to a login page or another page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register_student.html', {'form': form})


