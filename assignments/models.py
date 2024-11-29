from django.db import models


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    course = models.ForeignKey("course.Course", on_delete=models.DO_NOTHING, related_name="assignments")  # Changed to CASCADE for logical integrity

    def __str__(self):
        return self.title


class Question(models.Model):
    assignment = models.ForeignKey(
        Assignment, related_name="questions", on_delete=models.DO_NOTHING
    )
    question_text = models.TextField()
    marks = models.IntegerField(default=0)
    ANSWER_TYPES = [
        ("multiple_choice", "Multiple Choice"),
        ("short_answer", "Short Answer"),
    ]
    answer_type = models.CharField(max_length=50, choices=ANSWER_TYPES, default="short_answer")

    def __str__(self):
        return f"Question: {self.question_text[:50]}..."


class CompletedAssignment(models.Model):
    student = models.ForeignKey(
        "users.StudentProfile", on_delete=models.DO_NOTHING, related_name="completed_assignments"
    )
    assignment = models.ForeignKey(
        Assignment, on_delete=models.DO_NOTHING, related_name="completed_assignments"
    )
    completed_on = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[("completed", "Completed"), ("pending", "Pending")],
        default="pending",
    )

    score = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title} - {self.status}"
