from django.contrib import admin

from users.models import User, StudentProfile, LecturerProfile, ParentProfile, Interest, Aptitude

admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(LecturerProfile)
admin.site.register(ParentProfile)
admin.site.register(Interest)
admin.site.register(Aptitude)