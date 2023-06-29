from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.list import ListView
from dashboard.forms import AddCourseForm, EditCourseForm, LessonCompletionForm, LessonForm
from django.contrib import messages
from dashboard.models import Course, Lesson, LessonCompletion
from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required as permission_required_decorator
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Exists, Avg


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dashboard/home.html')


class CourseView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    permission_required = ['dashboard.view_course']
    paginate_by = 15

    def get_queryset(self) -> QuerySet[Any]:
        return Course.objects.filter(participants__id=self.request.user.id).annotate(lesson_count=Count('lesson', distinct=True), completed_lesson_count=Count('lesson__lessoncompletion', LessonCompletion.objects.only('id').filter(user_id=self.request.user.id)))


class AddCoursesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['dashboard.add_course']

    def get(self, request: HttpRequest):
        return render(request, 'dashboard/add_course.html', {
            'form': AddCourseForm(initial={'participants': (self.request.user.id, self.request.user.username)}),
        })

    def post(self, request: HttpRequest):
        form = AddCourseForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Added course')
            return redirect('dashboard.courses')

        return render(request, 'dashboard/add_course.html', {
            'form': form
        })


class EditCoursesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['dashboard.change_course']

    def get(self, request: HttpRequest, course_id: int):
        course = Course.objects.filter(
            participants__id=self.request.user.id, id=course_id).prefetch_related('participants').get()

        return render(request, 'dashboard/edit_course.html', {
            'form': EditCourseForm(instance=course, initial={
                'participants': [user.id for user in course.participants.all()]
            }),
            'course': course,
        })

    def post(self, request: HttpRequest, course_id: int):
        course = Course.objects.filter(
            participants__id=self.request.user.id, id=course_id).get()
        form = EditCourseForm(request.POST, instance=course)

        if form.is_valid():
            form.save()
            messages.success(request, 'Updated course')
            return redirect('dashboard.courses')

        return render(request, 'dashboard/edit_course.html', {
            'form': form
        })


class CourseDetailView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, course_id: int):
        course = Course.objects.prefetch_related('lesson_set', 'lesson_set__lessoncompletion_set').filter(participants__id=request.user.id).get(id=course_id)

        return render(request, 'dashboard/course_detail.html', {
            'course': course,
            'course_completion_percentage': course.get_course_completion_percentage(request.user.id)
        })


@login_required()
@permission_required_decorator('dashboard.delete_course')
def delete_course(request: HttpRequest, course_id):
    course = Course.objects.filter(
        id=course_id, participants__id=request.user.id).get()

    course.participants.remove()
    course.delete()

    messages.success(request, 'Deleted successfully')

    return redirect('dashboard.courses')


@login_required()
@permission_required_decorator('dashboard.view_lesson')
def lesson_detail(request: HttpRequest, course_id: int, lesson_id: int):
    course = Course.objects.prefetch_related('lesson_set', 'lesson_set__lessoncompletion_set').filter(participants__id=request.user.id).get(id=course_id)
    lesson = Lesson.objects.annotate(is_complete=Exists(LessonCompletion.objects.filter(user_id=request.user.id, lesson_id__in=Lesson.objects.filter(
        id=lesson_id, course__id=course_id, course__participants__id=request.user.id)))).filter(id=lesson_id, course__id=course_id, course__participants__id=request.user.id).get()

    return render(request, 'dashboard/lesson_detail.html', {
        'course': course,
        'course_completion_percentage': course.get_course_completion_percentage(request.user.id),
        'lesson': lesson,
        'next_lesson': lesson.next_lesson(request.user.id, course_id),
        'previous_lesson': lesson.previous_lesson(request.user.id, course_id),
    })


@login_required()
@permission_required_decorator('dashboard.view_lesson')
@require_http_methods(['POST'])
def lesson_completion(request: HttpRequest, course_id: int, lesson_id: int):
    form = LessonCompletionForm(request.POST)

    if form.is_valid():
        Lesson.objects.filter(course_id=course_id).get(id=lesson_id).mark_lesson(
            request.POST.get('completion'), request.user.id)
        messages.success(request, 'Marked successfully')

    return redirect('dashboard.lesson_detail', course_id, lesson_id)


class AddLessonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['dashboard.add_lesson']

    def get(self, request: HttpRequest, course_id):
        course = Course.objects.filter(
            participants__id=request.user.id, id=course_id).get()

        return render(request, 'dashboard/add_lesson.html', {
            'form': LessonForm(),
            'course': course,
        })

    def post(self, request: HttpRequest, course_id: int):
        form = LessonForm(request.POST)
        course = Course.objects.filter(
            participants__id=request.user.id, id=course_id).get()

        if form.is_valid():
            Lesson.objects.create(name=form.cleaned_data.get('name'), content=form.cleaned_data.get(
                'content'), course=course, created_by=request.user)
            messages.success(request, 'Added lesson')
            return redirect('dashboard.course_detail', course_id)

        return render(request, 'dashboard/add_lesson.html', {
            'form': form,
            'course': course
        })


class EditLessonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['dashboard.change_lesson']

    def get(self, request: HttpRequest, course_id: int, lesson_id: int):
        lesson = lesson = Lesson.objects.filter(
            id=lesson_id, course__id=course_id, course__participants__id=request.user.id).get()

        return render(request, 'dashboard/edit_lesson.html', {
            'form': LessonForm(instance=lesson),
            'lesson': lesson,
        })

    def post(self, request: HttpRequest, course_id: int, lesson_id: int):
        form = LessonForm(request.POST)
        lesson = Lesson.objects.filter(
            id=lesson_id, course__id=course_id, course__participants__id=request.user.id).get()

        if form.is_valid():
            lesson.name = form.cleaned_data.get('name')
            lesson.content = form.cleaned_data.get('content')
            lesson.save()

            messages.success(request, 'Added lesson')
            return redirect('dashboard.course_detail', course_id)

        return render(request, 'dashboard/edit_lesson.html', {
            'form': form,
            'course': lesson
        })


@login_required()
@permission_required_decorator('dashboard.delete_lesson')
def delete_lesson(request: HttpRequest, course_id, lesson_id: int):
    lesson = Lesson.objects.filter(
        id=lesson_id, course__id=course_id, course__participants__id=request.user.id).get()
    lesson.delete()

    messages.success(request, 'Deleted successfully')

    return redirect('dashboard.course_detail', course_id)
