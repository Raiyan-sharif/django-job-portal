from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobs/', views.job_search, name='job_search'),
    path('jobs/new/', views.job_create, name='job_create'),
    path('jobs/mine/', views.my_jobs, name='my_jobs'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/apply/', views.job_apply, name='job_apply'),
    path('applications/', views.my_applications, name='my_applications'),
]