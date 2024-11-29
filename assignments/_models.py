from django.db import models

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    course = models.ForeignKey("course.Course", on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.title

class CompletedAssignment(models.Model):
    student = models.ForeignKey('users.StudentProfile', on_delete=models.DO_NOTHING)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    completed_on = models.DateTimeField(null=True, blank=True)
    students_completed = models.ManyToManyField("users.User")
    status = models.CharField(
        max_length=10,
        choices=[('completed', 'Completed'), ('pending', 'Pending')],
        default='pending'
    )

    def __str__(self):
        return f"{self.student.name} - {self.assignment.title} - {self.status}"


class Question(models.Model):
    assignment = models.ForeignKey(Assignment, related_name="questions", on_delete=models.DO_NOTHING)
    question_text = models.TextField()
    marks = models.IntegerField(default=0)
    answer_type = models.CharField(max_length=50, choices=[('multiple_choice', 'Multiple Choice'), ('short_answer', 'Short Answer')], default='short_answer')

    def __str__(self):
        return f"Question: {self.question_text[:50]}..."