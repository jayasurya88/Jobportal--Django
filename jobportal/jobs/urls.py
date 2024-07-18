from django.urls import path
from . import views
from .views import job_list

app_name = 'jobs'
urlpatterns = [
    path('create/', views.create_job, name='create_job'),
    path('jobs/', job_list, name='job_list'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('recruiter-jobs/', views.recruiter_jobs, name='recruiter_jobs'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('jobs/delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('apply/', views.job_application, name='apply'),
    path('jobs/apply/<int:job_id>/', views.job_application, name='job_application'),
    path('application/success/', views.application_success, name='application_success'),
    path('view-applicants/<int:job_id>/', views.view_applicants, name='view_applicants'),
    path('update-status/<int:application_id>/', views.update_status, name='update_status'),
    path('my-applications/', views.view_user_applications, name='my_applications'),
    path('about', views.about, name='about'),
    
   ]
