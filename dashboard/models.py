from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField()
    description = models.TextField(null=True, blank=True)
    created_by = models.OneToOneField(User)
    participants = models.ManyToManyField(User)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Lesson(models.Model):
    name = models.CharField()
    description = models.CharField(null=True, blank=True)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_by = models.OneToOneField(User)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name