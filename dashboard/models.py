from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=264)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=264)
    description = models.CharField(max_length=511, null=True, blank=True)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    def next_lesson_exists(self, user_id, course_id = None):
       return Lesson.objects.filter(id__gt=self.id, course__id=course_id or self.course.id, course__participants__id=user_id).exists()
    
    def previous_lesson_exists(self, user_id, course_id = None):
       return Lesson.objects.filter(id__lt=self.id, course__id=course_id or self.course.id, course__participants__id=user_id).exists()