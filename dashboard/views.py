from django.shortcuts import render
from django.views import View

class Dashboard(View):
    def get(self, request):
        return render(request, 'dashboard/home.html')

class CourseView(View):
    def get(self, request):
        return render(request, 'dashboard/courses.html')

class CourseDetailView(View):
    def get(self, request, course_id: int):
        return render(request, 'dashboard/course_detail.html', {
            'course_id': course_id
        })
