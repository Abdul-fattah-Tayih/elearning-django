from django.contrib import admin

from dashboard.models import Course, Lesson, LessonComment, LessonCompletion

# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(LessonCompletion)
admin.site.register(LessonComment)