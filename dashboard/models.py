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
    
    def get_course_completion_percentage(self, user_id: int) -> int:
        lesson_count = Lesson.objects.filter(course_id=self.id).count()

        if lesson_count == 0:
            return 0
        
        completed_count = LessonCompletion.objects.filter(lesson_id__in=Lesson.objects.filter(course_id=self.id), user_id=user_id).count()

        return round(completed_count / lesson_count * 100)

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
    
    def is_complete(self, user_id):
        return LessonCompletion.objects.filter(lesson_id=self.id, user_id=user_id).exists()
    
    def mark_lesson(self, action: str, user_id: int):
        if action == LessonCompletion.ACTION_COMPLETE:
            self.lessoncompletion_set.update_or_create(user_id=user_id)
        elif action == LessonCompletion.ACTION_INCOMPLETE:
            self.lessoncompletion_set.filter(user_id=user_id).delete()
    
class LessonCompletion(models.Model):
    ACTION_INCOMPLETE = 'incomplete'
    ACTION_COMPLETE = 'complete'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'lesson'], name='user_lesson')
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    



class LessonComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)