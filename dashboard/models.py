from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(blank=False, max_length=264)
    description = models.TextField(max_length= 263, null=True, blank=True)
    participants = models.ManyToManyField(User)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Lesson(models.Model):
    name = models.CharField(blank=False, max_length=264)
    content = models.TextField(blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def next_lesson(self, user_id, course_id = None):
       return Lesson.objects.filter(id__gt=self.id, course__id=course_id, course__participants__id=user_id).first()
    
    def previous_lesson(self, user_id, course_id = None):
       return Lesson.objects.filter(id__lt=self.id, course__id=course_id or self.course.id, course__participants__id=user_id).first()