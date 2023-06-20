from django.contrib import admin
from django.urls import path

from dashboard import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard.home'),
    path('courses', views.CourseView.as_view(), name='dashboard.courses'),
    path('courses/<course_id>', views.CourseDetailView.as_view(), name='dashboard.course_detail'),
    path('courses/<course_id>/lessons/<lesson_id>', views.lesson_detail, name='dashboard.lesson_detail'),
    path('courses/<course_id>/lessons/<lesson_id>/next', views.next_lesson, name='dashboard.next_lesson'),
    path('courses/<course_id>/lessons/<lesson_id>/previous', views.previous_lesson, name='dashboard.previous_lesson'),
]