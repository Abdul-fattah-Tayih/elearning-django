from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.list import ListView
from dashboard.models import Course
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required as permission_required_decorator


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dashboard/home.html')


class CourseView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    permission_required = ['dashboard.view_course']
    paginate_by = 15

    def get_queryset(self) -> QuerySet[Any]:
        return Course.objects.filter(participants__id=self.request.user.id)

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
