from django.db import models
import uuid

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=10, default=str(uuid.uuid4())[:8])
    assignments = models.ManyToManyField("assignments.Assignment", related_name='courses')
    students_enrolled = models.ManyToManyField('users.User', related_name='courses')
    course_videos = models.ManyToManyField('course.Video', related_name='courses', blank=True)
    course_texts = models.ManyToManyField('course.TextContent', related_name='courses', blank=True)
    course_duration = models.PositiveIntegerField(help_text="Duration of the course in weeks")
    course_content = models.JSONField(default=list, blank=True, help_text="List of course content such as videos, texts, and files.")

    def __str__(self):
        return f"Course {self.uid}: {self.course_duration} weeks"

    def total_students_enrolled(self):
        return self.students_enrolled.count()

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=10, default=str(uuid.uuid4())[:8])
    title = models.CharField(max_length=255)
    video_url = models.URLField(help_text="URL of the video hosted on a platform like YouTube, Vimeo, etc.")
    video_file = models.FileField(upload_to="courses/videos/", blank=True, null=True)

    def __str__(self):
        return self.title

class TextContent(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=10, default=str(uuid.uuid4())[:8])
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Text content for the course")

    def __str__(self):
        return self.title
