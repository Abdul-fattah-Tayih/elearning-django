from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from dashboard.models import Course
from django.contrib.auth.mixins import LoginRequiredMixin


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dashboard/home.html')


class CourseView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        print(request.user.id)
        return render(request, 'dashboard/courses.html', {
            'courses': Course.objects.filter(participants__id=request.user.id).all()
        })


class CourseDetailView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, course_id: int):
        course = Course.objects.prefetch_related('lesson_set') \
            .filter(participants__id=request.user.id) \
            .get(id=course_id)

        return render(request, 'dashboard/course_detail.html', {
            'course': course
        })
