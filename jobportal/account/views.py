
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from .models import User
# Create your views here.


@staff_member_required
def pending_recruiter_registrations(request):
    pending_recruiters = User.objects.filter(is_recruiter=True, is_approved=False)
    return render(request, 'pending_recruiters.html', {'pending_recruiters': pending_recruiters})


@staff_member_required
def approve_recruiter_registration(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_approved = True
    user.save()
    return redirect('pending_recruiter_registrations')

def index(request):
    return render(request,'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'User created'
            if user.is_recruiter:
                # Set up logic for admin approval
                msg = 'Your registration is pending approval from the admin.'
            return redirect('login_view')
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_jobseeker:
                login(request, user)
                return redirect('jobseeker')
            elif user is not None and user.is_recruiter:
                login(request, user)
                return redirect('recruiter')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


def admin(request):
    return render(request,'admin.html')


def jobseeker(request):
    return render(request,'jobseeker.html')


def recruiter(request):
    return render(request,'recruiter.html')

def custom_logout(request):
    logout(request)
    
    return redirect('login_view')