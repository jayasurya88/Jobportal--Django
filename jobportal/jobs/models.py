from django.db import models
from django.conf import settings  # Import settings module
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Job(models.Model):
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField()
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    company_logo = models.ImageField(upload_to='company_logos', default='https://cdn3.vectorstock.com/i/1000x1000/24/92/find-job-logo-icon-design-vector-22742492.jpg')
    def __str__(self):
        return self.title





class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=1)
    
    name = models.CharField(max_length=255, blank=True)  # Make name optional
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    year_of_passout = models.IntegerField()
    qualification = models.CharField(max_length=100)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        if self.name:
            return f"{self.name} - {self.email}"
        else:
            return self.email  # Fallback to email if name is not provided

    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"