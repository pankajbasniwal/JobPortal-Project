
from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.job_list, name='job_list'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('jobs/<int:id>/', views.job_detail, name='job_detail'),
]
