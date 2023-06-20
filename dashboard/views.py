from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from dashboard.models import Course, Lesson
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required as permission_required_decorator
from django.db.models import Count


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dashboard/home.html')


class CourseView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    permission_required = ['dashboard.view_course']
    paginate_by = 15

    def get_queryset(self) -> QuerySet[Any]:
        return Course.objects.filter(participants__id=self.request.user.id).annotate(Count('lesson', distinct=True))

    @method_decorator(permission_required_decorator('dashboard.add_course'))
    def post(self, request: HttpRequest):
        course = Course.objects.create(name=request.POST.get('name'), description=request.POST.get('description'))

        course.participants.add(request.POST.get('participants'))

        return redirect('dashboard.courses')


class CourseDetailView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, course_id: int):
        course = Course.objects.prefetch_related('lesson_set') \
            .filter(participants__id=request.user.id) \
            .get(id=course_id)

        return render(request, 'dashboard/course_detail.html', {
            'course': course
        })

@permission_required_decorator('dashboard.view_lesson')
def lesson_detail(request: HttpRequest, course_id: int, lesson_id: int):
    lesson = Lesson.objects.filter(id=lesson_id, course__id=course_id, course__participants__id=request.user.id).prefetch_related('course').get()

    return render(request, 'dashboard/lesson_detail.html', {
        'lesson': lesson,
        'next_lesson_exists': lesson.next_lesson_exists(request.user.id, course_id),
        'previous_lesson_exists': lesson.previous_lesson_exists(request.user.id, course_id),
    })

@permission_required_decorator('dashboard.view_lesson')
def next_lesson(request: HttpRequest, course_id: int, lesson_id: int):
    lesson = Lesson.objects.filter(id__gt=lesson_id, course__id=course_id, course__participants__id=request.user.id).prefetch_related('course').get()

    return render(request, 'dashboard/lesson_detail.html', {
        'lesson': lesson,
        'next_lesson_exists': lesson.next_lesson_exists(request.user.id, course_id),
        'previous_lesson_exists': lesson.previous_lesson_exists(request.user.id, course_id),
    })

@permission_required_decorator('dashboard.view_lesson')
def previous_lesson(request: HttpRequest, course_id: int, lesson_id: int):
    lesson = Lesson.objects.filter(id__lt=lesson_id, course__id=course_id, course__participants__id=request.user.id).prefetch_related('course').get()

    return render(request, 'dashboard/lesson_detail.html', {
        'lesson': lesson,
        'next_lesson_exists': lesson.next_lesson_exists(request.user.id, course_id),
        'previous_lesson_exists': lesson.previous_lesson_exists(request.user.id, course_id),
    })