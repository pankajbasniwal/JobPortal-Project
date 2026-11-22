from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('recruiter-dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('jobs/', views.jobs_page, name='jobs'),
    path('apply/<int:job_id>/', views.apply_page, name='apply'),
    path('post-job/', views.post_job_page, name='post_job'),
]