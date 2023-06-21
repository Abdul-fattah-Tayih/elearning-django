from django.contrib import admin
from django.urls import path

from dashboard import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard.home'),
    path('courses', views.CourseView.as_view(), name='dashboard.courses'),
    path('courses/add', views.AddCoursesView.as_view(), name='dashboard.add_courses'),
    path('courses/<course_id>', views.CourseDetailView.as_view(), name='dashboard.course_detail'),
    path('courses/<int:course_id>/edit', views.EditCoursesView.as_view(), name='dashboard.edit_course'),
    path('courses/<int:course_id>/delete', views.delete_course, name='dashboard.delete_course'),
    path('courses/<course_id>/lessons/<lesson_id>', views.lesson_detail, name='dashboard.lesson_detail'),
]