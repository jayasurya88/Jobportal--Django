from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import pending_recruiter_registrations, approve_recruiter_registration

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('jobseeker/', views.jobseeker, name='jobseeker'),
    path('recruiter/', views.recruiter, name='recruiter'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('pending-recruiters/', pending_recruiter_registrations, name='pending_recruiter_registrations'),
    path('approve-recruiter/<int:user_id>/', approve_recruiter_registration, name='approve_recruiter'),
]