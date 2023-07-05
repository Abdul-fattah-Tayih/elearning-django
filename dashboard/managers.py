from typing import List
from django.db import models
from django.db.models import Count, Exists
from django.apps import apps


class CourseManager(models.Manager):
    def find_for_user(self, course_id: int, user_id: int, prefetch: List[str] = None):
        query = self.get_queryset()

        if prefetch:
            query = query.prefetch_related(*prefetch)

        return query.filter(participants__id=user_id).get(id=course_id)

    def latest_assigned_course(self, user_id: int):
        try:
            return self.filter(participants__id=user_id).annotate(
                lesson_count=Count('lesson', distinct=True),
                completed_lesson_count=Count(
                    'lesson__lessoncompletion',
                    apps.get_registered_model('dashboard', 'LessonCompletion').objects.only('id').filter(user_id=user_id)
                )
            ).order_by('-courseparticipants__id').all()[0]
        except IndexError:
            return None

    def courses_for_user_with_lesson_counts(self, user_id: int) -> models.QuerySet:
        return self.filter(
            participants__id=user_id
        ).annotate(
            lesson_count=Count('lesson', distinct=True),
            completed_lesson_count=Count(
                'lesson__lessoncompletion',
                apps.get_registered_model('dashboard', 'LessonCompletion').objects.only('id').filter(user_id=user_id)
            )
        )


class LessonManager(models.Manager):
    def find_for_user(self, lesson_id: int, course_id: int, user_id: int, prefetch: List[str] = None):
        query = self.get_queryset()

        if prefetch:
            query = query.prefetch_related(*prefetch)

        return query.filter(
            id=lesson_id,
            course__id=course_id,
            course__participants__id=user_id
        ).get()

    def find_for_user_with_completion(self, lesson_id: int, course_id: int, user_id: int):
        return self.annotate(
            is_complete=Exists(
                apps.get_registered_model('dashboard', 'LessonCompletion').objects.filter(
                    user_id=user_id,
                    lesson_id__in=self.get_queryset().filter(
                        id=lesson_id,
                        course__id=course_id,
                        course__participants__id=user_id
                    )
                )
            )
        ).filter(
            id=lesson_id,
            course__id=course_id,
            course__participants__id=user_id
        ).get()

class LessonCommentManager(models.Manager):
    def find_for_user(self, comment_id: int, lesson_id: int, course_id: int, user_id: int, prefetch: List[str] = None):
        query = self.get_queryset()

        if prefetch:
            query = query.prefetch_related(*prefetch)

        return query.filter(
            id=comment_id,
            lesson_id=lesson_id,
            lesson__course__id=course_id,
            lesson__course__participants__id=user_id,
            user_id=user_id,
        ).get()