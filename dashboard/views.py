from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.list import ListView
from dashboard.forms import AddCourseForm, EditCourseForm
from django.contrib import messages
from dashboard.models import Course, Lesson
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required as permission_required_decorator
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
        course = Course.objects.filter(participants__id=self.request.user.id, id=course_id).prefetch_related('participants').get()

        return render(request, 'dashboard/edit_course.html', {
            'form': EditCourseForm(instance=course, initial={
                'participants': [user.id for user in course.participants.all()]
            }),
            'course': course,
        })

    def post(self, request: HttpRequest, course_id: int):
        course = Course.objects.filter(participants__id=self.request.user.id, id=course_id).get()
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
        course = Course.objects.prefetch_related('lesson_set') \
            .filter(participants__id=request.user.id) \
            .get(id=course_id)

        return render(request, 'dashboard/course_detail.html', {
            'course': course
        })

@login_required()
@permission_required_decorator('dashboard.delete_course')
def delete_course(request: HttpRequest, course_id):
    course = Course.objects.filter(id=course_id, participants__id=request.user.id).get()
    
    course.participants.remove()
    course.delete()

    messages.success(request, 'Deleted successfully')

    return redirect('dashboard.courses')

@login_required()
@permission_required_decorator('dashboard.view_lesson')
def lesson_detail(request: HttpRequest, course_id: int, lesson_id: int):
    lesson = Lesson.objects.filter(id=lesson_id, course__id=course_id, course__participants__id=request.user.id).prefetch_related('course').get()

    return render(request, 'dashboard/lesson_detail.html', {
        'lesson': lesson,
        'next_lesson': lesson.next_lesson(request.user.id, course_id),
        'previous_lesson': lesson.previous_lesson(request.user.id, course_id),
    })