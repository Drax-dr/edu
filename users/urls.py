from django.contrib import admin
from django.urls import include, path
# from .api import api
from .views import StudentDasboardView,LecturerDashboardView, HomeView, RegisterView, StudentRegisterView, StudentLoginForm, StudentLoginView,ParentRegisterView, LecturerRegisterView,student_login
from users import views

urlpatterns = [
    path("", view=HomeView.as_view(), name="home"),
    path("register.html/", view=RegisterView.as_view(), name="register"),
    path("register/student/", view=StudentRegisterView.as_view(), name="student_register"),
    path("login/student/", view=StudentLoginView.as_view(), name="login_student"),
    path("student/login/", views.student_login, name="student_login"),
    # student_login
    path("register/lecturer/", view=LecturerRegisterView.as_view(), name="lecturer_register"),
    path("login/lecturer/", view=StudentRegisterView.as_view(), name="lecturer_login"),
    path("register/parent/", view=ParentRegisterView.as_view(), name="paretn_register"),
    path('dashboard/student/', StudentDasboardView.as_view(), name='user_dashboard'),
    # path("register/student/", view=StudentRegisterView.as_view(), name="register"),
    path('dashboard/lecturer/', LecturerDashboardView.as_view(), name='lecturer_dashboard'),
]
