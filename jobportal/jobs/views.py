from django.shortcuts import render, redirect
from .models import Job 
from .forms import JobForm
from django.contrib import messages
from .models import Job ,JobApplication
from .forms import UpdateStatusForm
from django.shortcuts import render, get_object_or_404
from .forms import JobApplicationForm

from django.core.mail import send_mail
from django.conf import settings
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.company_logo = form.cleaned_data['company_logo']
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs:job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/create_job.html', {'form': form})




def job_list(request):
    # Query all job postings from the database
    jobs = Job.objects.all()

    # Render the job list template with the list of jobs
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})



def recruiter_jobs(request):
    recruiter_user = request.user
    jobs_by_recruiter = Job.objects.filter(recruiter_id=recruiter_user.id)
    return render(request, 'jobs/recruiter_jobs.html', {'jobs': jobs_by_recruiter})

def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            
            return redirect('jobs:recruiter_jobs')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/edit_job.html', {'form': form})


def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('jobs:recruiter_jobs')
    return render(request, 'jobs/delete_job.html', {'job': job})



# views.py


from django.shortcuts import redirect

def job_application(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.job = job  # Link the job application to the specific job
            job_application.save()
            
            
            # Redirect to the 'application_success' URL
            return redirect('jobs:application_success')  # Using the named URL with namespace
    else:
        form = JobApplicationForm()

    return render(request, 'jobs/application_form.html', {'form': form, 'job': job})

def application_success(request):
    return render(request, 'jobs/application_success.html')




def view_applicants(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    # Assuming 'job_id' is the foreign key field in JobApplication model linking to Job
    job_applications = JobApplication.objects.filter(job_id=job_id)
    
    return render(request, 'jobs/view_applicants.html', {'job': job, 'job_applications': job_applications})


def update_status(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    if request.method == 'POST':
        form = UpdateStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('jobs:view_applicants', job_id=application.job.id)
    else:
        form = UpdateStatusForm(instance=application)

    return render(request, 'jobs/update_status.html', {'form': form})



# views.py


def view_user_applications(request):
    # Retrieve all JobApplications
    all_job_applications = JobApplication.objects.all()

    # Pass the applications to the template
    return render(request, 'jobs/user_applications.html', {'applications': all_job_applications})

# def view_user_applications(request):
#     # Retrieve job applications associated with the current user
#     user = request.user
#     user_job_applications = JobApplication.objects.filter(applicant=user)

#     return render(request, 'jobs/user_applications.html', {'user_job_applications': user_job_applications})



# def update_status(request, application_id):
#     application = get_object_or_404(JobApplication, id=application_id)

#     if request.method == 'POST':
#         form = UpdateStatusForm(request.POST, instance=application)
#         if form.is_valid():
#             updated_application = form.save()
#             # Send email notification to the applicant
#             subject = 'Job Application Status Update'
#             message = f'Your application for {updated_application.job.title} has been updated to {updated_application.get_status_display()}.Thank you for using Nexahire.'
#             recipient_email = updated_application.email
#             send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])

#             return redirect('jobs:view_applicants', job_id=updated_application.job.id)
#     else:
#         form = UpdateStatusForm(instance=application)

#     return render(request, 'jobs/update_status.html', {'form': form})

def update_status(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    if request.method == 'POST':
        form = UpdateStatusForm(request.POST, instance=application)
        if form.is_valid():
            updated_application = form.save()

            # Determine the new status and prepare the email message accordingly
            if updated_application.status == 'rejected':
                # Send rejection email
                subject = 'Job Application Status Update - Rejected'
                message = f'We regret to inform you that your application for {updated_application.job.title} has been rejected. \n\n' \
                          f'After carefully reviewing all applications, we have selected candidates whose skills and qualifications more closely align with our current needs. \n\n' \
                          f'We sincerely appreciate your interest and encourage you to keep an eye on our careers page for future opportunities that match your skills and experience. \n\n' \
                          f'Thank you for using Nexahire.'
            elif updated_application.status == 'shortlisted':
                # Send shortlisting email
                subject = 'Job Application Status Update - Shortlisted'
                message = f'Congratulations! Your application for {updated_application.job.title} has been shortlisted. \n\n' \
                          f'We are impressed with your qualifications and would like to invite you for the next stage of our selection process. \n\n' \
                          f'Please stay tuned for further communication from our team. \n\n' \
                          f'Thank you for using Nexahire.'
            else:
                # Default status update email
                subject = 'Job Application Status Update'
                message = f'Your application for {updated_application.job.title} has been updated to {updated_application.get_status_display()}. \n\n' \
                          f'Thank you for using Nexahire.'

            recipient_email = updated_application.email

            # Send email notification to the applicant
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])

            return redirect('jobs:view_applicants', job_id=updated_application.job.id)
    else:
        form = UpdateStatusForm(instance=application)

    return render(request, 'jobs/update_status.html', {'form': form})


def about(request):
    return render(request, 'jobs/about.html')


