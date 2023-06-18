from django.contrib import admin
from django.urls import path

from dashboard import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard.home'),
    path('courses', views.CourseView.as_view(), name='dashboard.courses'),
    path('courses/<course_id>', views.CourseDetailView.as_view(), name='dashboard.course_detail'),
]