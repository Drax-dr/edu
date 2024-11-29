class StudentListView(ListView):
    model = StudentProfile
    template_name = 'student_list.html'
    context_object_name = 'students'


class StudentDetailView(DetailView):
    model = StudentProfile
    template_name = 'student_detail.html'
    context_object_name = 'student'


class StudentCreateView(CreateView):
    model = StudentProfile
    template_name = 'student_form.html'
    fields = ['name', 'studentID', 'phoneNumber', 'ParentNumber', 'profilePic', 'grade', 'assignments_completed']
    success_url = reverse_lazy('student_list')


class StudentUpdateView(UpdateView):
    model = StudentProfile
    StudentProfile = 'student_form.html'
    fields = ['name', 'studentID', 'phoneNumber', 'ParentNumber', 'profilePic', 'grade', 'assignments_completed']
    success_url = reverse_lazy('student_list')


class StudentDeleteView(DeleteView):
    model = StudentProfile
    template_name = 'student_confirm_delete.html'
    success_url = reverse_lazy('student_list')


# Views for Lecturer
class LecturerListView(ListView):
    model = LecturerProfile
    template_name = 'lecturer_list.html'
    context_object_name = 'lecturers'


class LecturerDetailView(DetailView):
    model = LecturerProfile
    template_name = 'lecturer_detail.html'
    context_object_name = 'lecturer'


class LecturerCreateView(CreateView):
    model = LecturerProfile
    template_name = 'lecturer_form.html'
    fields = ['Name', 'mID', 'Phone number', 'Photo']
    success_url = reverse_lazy('lecturer_list')


class LecturerUpdateView(UpdateView):
    model = LecturerProfile
    template_name = 'lecturer_form.html'
    fields = ['Name', 'mID', 'Phone number', 'Photo']
    success_url = reverse_lazy('lecturer_list')


class LecturerDeleteView(DeleteView):
    model = LecturerProfile
    template_name = 'lecturer_confirm_delete.html'
    success_url = reverse_lazy('lecturer_list')